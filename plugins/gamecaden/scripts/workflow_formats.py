"""Native record parsing and lossless YAML editing for the local workflow CLI."""
from __future__ import annotations

import copy
import hashlib
import io
import json
import os
from pathlib import Path
import re
from dataclasses import dataclass

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError as RoundTripError


class WorkflowError(Exception):
    def __init__(self, code, message, target=None):
        super().__init__(message)
        self.code, self.target = code, target

    def item(self):
        result = {"code": self.code, "message": str(self)}
        if self.target is not None:
            result["target"] = self.target
        return result


def require(condition, code, message, target=None):
    if not condition:
        raise WorkflowError(code, message, target)


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, "invalid_record", f"Duplicate key: {key}")
        result[key] = value
    return result


def json_load(text):
    def invalid(value):
        raise WorkflowError("invalid_record", f"Non-finite JSON: {value}")
    return json.loads(text, object_pairs_hook=pairs, parse_constant=invalid)


def plain(value):
    return json_load(json.dumps(value, ensure_ascii=False, allow_nan=False))


def rt_yaml():
    parser = YAML(typ="rt")
    parser.preserve_quotes = True
    parser.allow_duplicate_keys = False
    parser.width = 4096
    return parser


def yaml_load(text):
    require(not any(isinstance(t, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken))
                    for t in yaml.scan(text)), "invalid_record", "Native YAML aliases/anchors are unsupported")
    # SafeLoader rejects executable/custom tags; round-trip parsing keeps comments.
    yaml.safe_load(text)
    try:
        value = rt_yaml().load(text)
    except RoundTripError as exc:
        raise WorkflowError("invalid_record", str(exc)) from exc
    plain(value)  # Reject timestamps/custom values outside the JSON data model.
    return value


def yaml_dump(value):
    output = io.StringIO()
    rt_yaml().dump(value, output)
    return output.getvalue()


SCHEMA = json_load((Path(__file__).resolve().parents[1] / "schemas/workflow-v1.schema.json").read_text(encoding="utf-8"))
VALIDATORS = {name: Draft202012Validator(dict(SCHEMA, **{"$ref": f"#/$defs/{name}"}),
                                        format_checker=FormatChecker()) for name in SCHEMA["$defs"]}


def validate(kind, value):
    errors = list(VALIDATORS[kind].iter_errors(plain(value)))
    require(not errors, "invalid_record", f"{kind}: {errors[0].message}" if errors else "")


def revision(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def request_digest(request):
    return revision(canonical({k: v for k, v in request.items() if k != "request_id"}).encode("utf-8"))


PREFIXES = {"task": "T", "epic": "E", "evidence": "EV", "decision": "D", "asset": "A"}
KINDS = {value: key for key, value in PREFIXES.items()}
FRONT = re.compile(r"\A---\n(.*?)\n---(?:\n|$)", re.S)
BLOCK = re.compile(r"<!-- workflow:record (evidence|decision) ([A-Za-z0-9_.-]+) -->\n```yaml\n(.*?)\n```\n(.*?)\n<!-- workflow:endrecord \2 -->", re.S)
FORWARD = re.compile(r"<!-- workflow:forward ([A-Za-z0-9_.-]+) -->\n```yaml\n(.*?)\n```\n<!-- workflow:endforward \1 -->", re.S)


def normalized_id(value):
    match = re.fullmatch(r"([A-Z]+)-(\d+)", value)
    return (match[1], int(match[2])) if match else value


def identity_kind(metadata):
    value = metadata.get("id", "") if isinstance(metadata, dict) else ""
    return KINDS.get(value.rsplit("-", 1)[0])


@dataclass
class Record:
    path: Path
    kind: str
    metadata: dict | None
    body: str | None
    format: str
    source: str | None = None
    span: tuple | None = None
    forward: dict | None = None

    @property
    def id(self):
        return self.metadata.get("id") if self.metadata else None


class Document:
    def __init__(self, path, data, native=False, role="document", source=None):
        self.path, self.data, self.native = path, data, native
        try:
            raw = data.decode("utf-8-sig")
        except UnicodeError as exc:
            if not native:
                self.main = Record(path, role, None, None, "external", source)
                self.records, self.forwards = [], []
                return
            raise WorkflowError("unsupported_format", "Only UTF-8 text is supported", {"path": str(path)}) from exc
        self.bom = data.startswith(b"\xef\xbb\xbf")
        self.newline = "\r\n" if "\r\n" in raw else "\n"
        self.text = raw.replace("\r\n", "\n")
        self.header = None
        self.records, self.forwards = [], []
        if not native:
            self.main = Record(path, role, None, self.text, "external", source)
            return
        suffix = path.suffix.lower()
        metadata, body = None, self.text
        if suffix in (".yaml", ".yml", ".json"):
            metadata = json_load(self.text) if suffix == ".json" else yaml_load(self.text)
            body = None
        elif suffix == ".md":
            self.header = FRONT.match(self.text)
            if self.header:
                metadata = yaml_load(self.header[1])
                body = self.text[self.header.end():]
        else:
            raise WorkflowError("unsupported_format", f"Unsupported native extension: {suffix}")
        kind = identity_kind(metadata) or ("asset-ledger" if role == "asset-ledger" else role)
        if role in PREFIXES and metadata is None:
            attachment = path.stem.lower()
            if attachment in ("design", "plan", "history", "readme", "index"):
                kind = attachment
            else:
                raise WorkflowError("invalid_record", f"Native {role} is missing required frontmatter", {"path": str(path)})
        fmt = {".json": "native-json-v1", ".yaml": "native-yaml-v1", ".yml": "native-yaml-v1"}.get(suffix, "native-markdown-v1")
        self.main = Record(path, kind, metadata, body, fmt, source)
        if kind in PREFIXES and metadata is not None:
            validate(kind.title(), metadata)
        if kind == "asset-ledger":
            validate("AssetLedger", metadata)
            self.records.extend(Record(path, "asset", item, None, fmt, source) for item in metadata["assets"])
        else:
            self.records.append(self.main)
        if body is not None:
            self.records.extend(self.parse_blocks(body, source))
            matches = list(FORWARD.finditer(body))
            require(body.count("<!-- workflow:forward ") == len(matches), "invalid_record", "Malformed forward block")
            for match in matches:
                value = yaml_load(match[2])
                require(set(value) == {"id", "to"} and value["id"] == match[1], "invalid_record", "Forward identity mismatch")
                validate("Ref", value["to"])
                self.forwards.append(Record(path, "forward", {"id": match[1]}, None, fmt, source, match.span(), value["to"]))
        identities = [normalized_id(r.id) for r in self.records + self.forwards if r.id]
        require(len(identities) == len(set(identities)), "duplicate_id", "Duplicate identity inside one document")
        for record in self.records:
            if record.kind == "decision":
                ids = [e["event_id"] for e in record.metadata["events"]]
                require(len(ids) == len(set(ids)), "invalid_record", "Duplicate Decision event")

    def parse_blocks(self, body, source):
        matches = list(BLOCK.finditer(body))
        require(body.count("<!-- workflow:record ") == len(matches), "invalid_record", "Malformed/nested record block")
        result = []
        for match in matches:
            require("<!-- workflow:record " not in match[4], "invalid_record", "Nested record")
            value = yaml_load(match[3])
            require(value.get("id") == match[2], "invalid_record", "Embedded identity mismatch")
            validate(match[1].title(), value)
            result.append(Record(self.path, match[1], value, match[4], "native-markdown-v1", source, match.span()))
        return result

    def encode(self, text):
        return (b"\xef\xbb\xbf" if self.bom else b"") + text.replace("\n", self.newline).encode("utf-8")

    def render(self, metadata=None, body=None):
        metadata = self.main.metadata if metadata is None else metadata
        body = self.main.body if body is None else body
        if self.path.suffix == ".json":
            text = json.dumps(plain(metadata), ensure_ascii=False, indent=2) + "\n"
        elif self.path.suffix in (".yaml", ".yml"):
            text = yaml_dump(metadata)
        elif self.header:
            text = "---\n" + yaml_dump(metadata) + "---\n" + body
        else:
            text = body
        return self.encode(text)

    def replace_record(self, record, metadata, body):
        if record.span is None:
            return self.render(metadata, body)
        start, end = record.span
        content = self.main.body[:start] + record_block(record.kind, metadata, body) + self.main.body[end:]
        return self.render(body=content)


def record_block(kind, metadata, body):
    rid = metadata["id"]
    return f"<!-- workflow:record {kind} {rid} -->\n```yaml\n{yaml_dump(metadata)}```\n{body}\n<!-- workflow:endrecord {rid} -->"


def forward_block(rid, path):
    return f"<!-- workflow:forward {rid} -->\n```yaml\n{yaml_dump({'id': rid, 'to': {'path': path}})}```\n<!-- workflow:endforward {rid} -->"


def walk_refs(value):
    if isinstance(value, dict):
        if set(value) <= {"id", "path", "source", "project_id", "fragment"} and ("id" in value or "path" in value):
            yield value
        else:
            for key, child in value.items():
                if key not in ("extensions", "technical", "parameters"):
                    yield from walk_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_refs(child)


def rebase(value, old_base, new_base, resolve):
    result = copy.deepcopy(value)
    for ref in walk_refs(result):
        if "path" in ref:
            ref["path"] = Path(os.path.relpath(resolve(ref["path"], old_base), new_base)).as_posix()
    return result


def rebase_markdown(body, old_base, new_base, resolve):
    """Rewrite Markdown destinations; reject ambiguous HTML/wiki destinations."""
    from urllib.parse import unquote, quote
    require(not re.search(r'\[\[|\b(?:src|href)\s*=', body), "unsupported_format", "Extraction needs explicit handling of wiki/HTML links")
    def target(value):
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value) and not re.match(r"^[A-Za-z]:[/\\]", value):
            return value
        if value.startswith(("#", "//")):
            return value
        name, sep, anchor = value.partition("#")
        absolute = resolve(unquote(name), old_base)
        relative = Path(os.path.relpath(absolute, new_base)).as_posix()
        return quote(relative, safe="/:@-._~") + sep + anchor
    def inline(match):
        dest = match[1]
        if dest.startswith("<"):
            return "](<" + target(dest[1:-1]) + ">" + (match[2] or "") + ")"
        return "](" + target(dest) + (match[2] or "") + ")"
    # Code examples retain their bytes; only prose links carry document-relative meaning.
    lines, fence = [], None
    for line in body.splitlines(keepends=True):
        mark = re.match(r"\s*(`{3,}|~{3,})", line)
        if mark:
            if fence and mark[1][0] == fence[0] and len(mark[1]) >= fence[1]:
                fence = None
            elif not fence:
                fence = (mark[1][0], len(mark[1]))
            lines.append(line)
            continue
        if not fence:
            spans = re.split(r"(`+[^`]*`+)", line)
            for index in range(0, len(spans), 2):
                spans[index] = re.sub(r'\]\((<[^>]+>|[^\s()]+)(\s+"[^"\n]*")?\)', inline, spans[index])
            line = "".join(spans)
            match = re.match(r"(\s*\[[^\]]+\]:\s*)(<[^>]+>|\S+)(.*)", line)
            if match:
                token = match[2]
                dest = "<" + target(token[1:-1]) + ">" if token.startswith("<") else target(token)
                line = match[1] + dest + match[3] + ("\n" if line.endswith("\n") else "")
        lines.append(line)
    return "".join(lines)
