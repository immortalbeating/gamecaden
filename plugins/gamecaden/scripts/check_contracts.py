"""Read-only self-check for the v1 contract, templates, and illustrative examples.

Requires Python, PyYAML and jsonschema. This is not a record writer, a game
validator, or a concurrency/authorization implementation.
"""
from __future__ import annotations

if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from gamecaden_runtime import bootstrap_cli
    bootstrap_cli("contracts")

import copy
import hashlib
import json
from pathlib import Path
import re

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "v1"
PROJECT = EXAMPLES / "project"
WORKSPACE = PROJECT / "game-workflow"


def unique_mapping(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate key: {key}")
        result[key] = value
    return result


def json_read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_mapping)


class NativeLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader, node, deep=False):
    return unique_mapping((loader.construct_object(k, deep=deep),
                           loader.construct_object(v, deep=deep))
                          for k, v in node.value)


NativeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def yaml_read(text):
    if any(isinstance(token, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken))
           for token in yaml.scan(text)):
        raise ValueError("Native v1 YAML does not use aliases/anchors")
    return yaml.load(text, Loader=NativeLoader)


SCHEMA = json_read(ROOT / "schemas" / "workflow-v1.schema.json")


def validate(kind, value):
    schema = dict(SCHEMA, **{"$ref": f"#/$defs/{kind}"})
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(value)


def metadata(text):
    if not text.startswith("---\n"):
        raise ValueError("Missing frontmatter")
    header, body = text[4:].split("\n---\n", 1)
    return yaml_read(header), body


def unique_ids(values, label):
    if len(values) != len(set(values)):
        raise ValueError(f"Duplicate {label}")


def workspace_checks(value):
    validate("Workspace", value)
    unique_ids([item["id"] for item in value["sources"]], "source id")
    unique_ids([item["id"] for item in value["runtime_roots"]], "runtime id")
    unique_ids([item["id"] for item in value["rule_sources"]], "rule source id")
    sources = {item["id"]: item for item in value["sources"]}
    for field, role in (("default_task_source", "task"), ("default_epic_source", "epic")):
        source = value[field]
        if source is not None and (source not in sources or sources[source]["role"] != role):
            raise ValueError(f"{field} must reference a {role} source")


def decision_checks(value):
    validate("Decision", value)
    unique_ids([event["event_id"] for event in value["events"]], "decision event id")
    for event in value["events"]:
        for replaced in event.get("replaces", []):
            if not replaced.get("fragment"):
                raise ValueError("Replacement must name its target event")


def ledger_checks(value):
    validate("AssetLedger", value)
    unique_ids([asset["id"] for asset in value["assets"]], "asset id")
    for asset in value["assets"]:
        candidates = [candidate["id"] for candidate in asset["candidates"]]
        unique_ids(candidates, "candidate id")
        unique_ids([use["use_id"] for use in asset["selected_uses"]], "use id")
        for use in asset["selected_uses"]:
            if use["candidate_id"] not in candidates:
                raise ValueError("Selected use references unknown candidate")


BLOCK = re.compile(
    r"<!-- workflow:record (evidence|decision) ([A-Za-z0-9_.-]+) -->\n"
    r"```yaml\n(.*?)\n```\n(.*?)\n<!-- workflow:endrecord \2 -->", re.S)


def embedded(text):
    blocks = list(BLOCK.finditer(text))
    if text.count("<!-- workflow:record ") != len(blocks):
        raise ValueError("Malformed or nested native record block")
    result = []
    for block in blocks:
        if "<!-- workflow:record " in block.group(4):
            raise ValueError("Nested native record")
        value = yaml_read(block.group(3))
        if value["id"] != block.group(2):
            raise ValueError("Embedded marker id differs from metadata id")
        kind = block.group(1).title()
        validate(kind, value)
        result.append((kind, value))
    return result


def refs(value):
    if isinstance(value, dict):
        if (set(value) <= {"id", "path", "source", "project_id", "fragment"}
                and ("id" in value or "path" in value)):
            yield value
        else:
            for child in value.values():
                yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def fixture_path(base, relative):
    path = (base / relative).resolve()
    if not path.is_relative_to(PROJECT.resolve()) or not path.exists():
        raise ValueError(f"Invalid fixture reference: {relative} from {base}")
    return path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def request_digest(value):
    content = {key: item for key, item in value.items() if key != "request_id"}
    encoded = json.dumps(content, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def example_address(address):
    """Translate fixture addresses only; not an OS path/permission resolver."""
    prefix = "C:/ExampleGame"
    if not (address == prefix or address.startswith(prefix + "/")):
        raise ValueError(f"Unexpected example address: {address}")
    return (PROJECT / address[len(prefix):].lstrip("/")).resolve()


def extract_fixture_checks(request, locations):
    """Check the example's initial extraction preconditions, without writing."""
    validate("Request", request)
    base = example_address(request["context"].get("base_dir", request["context"]["project_root"]))
    source = locations[request["payload"]["target"]["id"]].resolve()
    destination = (base / request["payload"]["destination"]).resolve()
    if not destination.is_relative_to(PROJECT.resolve()) or destination.exists():
        raise ValueError("Extraction fixture expects an absent project-local destination")
    actual = {}
    for condition in request["preconditions"]:
        ref = condition["target"]
        path = (locations[ref["id"]] if "id" in ref else base / ref["path"]).resolve()
        if path in actual:
            raise ValueError("Duplicate precondition target")
        actual[path] = condition["expected_revision"]
    if actual != {source: "sha256:" + digest(source), destination: None}:
        raise ValueError("Extraction fixture must protect its actual carrier and destination")


def io_fixture_checks(locations):
    read = lambda name: json_read(EXAMPLES / "io" / name)
    create = read("create-task.request.json")
    prepared = read("create-unknown.response.json")
    replayed = read("create-replayed.response.json")
    for response in (prepared, replayed):
        if response["receipt"]["request_digest"] != request_digest(create):
            raise ValueError("Create receipt digest differs from the request vector")
    if prepared["receipt"]["allocations"] != replayed["receipt"]["allocations"]:
        raise ValueError("Replay example allocated a second identity")
    if not replayed["replayed"] or replayed["receipt"]["outcome"] != "ok":
        raise ValueError("Incorrect replay example")
    reordered = dict(reversed(list(create.items())))
    reordered["request_id"] = "another-request-id"
    if request_digest(create) != request_digest(reordered):
        raise ValueError("Digest must ignore request_id and object key order")
    for key in ("context", "payload", "preconditions"):
        changed = copy.deepcopy(create)
        changed[key] = {"different": True} if key != "preconditions" else [{"different": True}]
        if request_digest(create) == request_digest(changed):
            raise ValueError(f"Request digest omitted {key}")
    if "receipt" in read("request-id-conflict.response.json"):
        raise ValueError("A conflicting request cannot borrow the old success receipt")

    extraction = read("extract.request.json")
    extract_fixture_checks(extraction, locations)
    partial = read("extract-partial.response.json")
    queried = read("operation-status.response.json")
    if partial["receipt"]["request_digest"] != request_digest(extraction):
        raise ValueError("Extraction receipt digest mismatch")
    if queried["receipt"] != partial["receipt"] or queried["writes"] != partial["writes"]:
        raise ValueError("Status query lost the original partial write facts")
    if queried["request_id"] == queried["receipt"]["request_id"]:
        raise ValueError("Query identity must differ from queried operation in this fixture")
    expected = {"C:/ExampleGame/game-workflow/evidence/EV-001.md": "written",
                "C:/ExampleGame/game-workflow/tasks/T-001-copy.md": "not_attempted"}
    if {item["target"]["path"]: item["status"] for item in partial["writes"]} != expected:
        raise ValueError("Partial extraction example misstates source/destination results")
    recovery = partial["receipt"]["recovery_actions"][0]
    if recovery["action"] != "finish_extract" or {r["path"] for r in recovery["targets"]} != set(expected):
        raise ValueError("Recovery example must identify both actual files")

    for name in ("read-task.response.json", "legacy-read.response.json"):
        data = read(name)["data"]
        path = example_address(data["path"])
        if data["revision"] != "sha256:" + digest(path):
            raise ValueError("Read fixture revision differs from actual sample bytes")
        if data["interpretation"] == "raw":
            if (data["metadata"] is not None or data["reference_base"] is not None
                    or data["capabilities"] != ["record.read"] or data["ref"]["path"] != data["path"]
                    or data["body"] != path.read_text(encoding="utf-8")):
                raise ValueError("Legacy example lost raw content or claimed unsupported capabilities")
        else:
            meta, body = metadata(path.read_text(encoding="utf-8"))
            if data["metadata"] != meta or data["body"] != body or example_address(data["reference_base"]) != path.parent:
                raise ValueError("Native read example changed its source or reference base")
    listing = read("list-tasks.response.json")["data"]
    if listing["complete"] or not listing["diagnostics"]:
        raise ValueError("Unadapted source must not silently yield a complete task inventory")
    for item in listing["items"]:
        path = example_address(item["path"])
        if item["revision"] != "sha256:" + digest(path) or example_address(item["reference_base"]) != path.parent:
            raise ValueError("List item lost source revision or reference base")


def main():
    Draft202012Validator.check_schema(SCHEMA)
    workspace = yaml_read((WORKSPACE / "workspace.yaml").read_text(encoding="utf-8"))
    workspace_checks(workspace)
    records, locations, numeric_ids = {}, {}, set()
    for folder, kind in (("tasks", "Task"), ("epics", "Epic"),
                         ("evidence", "Evidence"), ("decisions", "Decision")):
        for path in (WORKSPACE / folder).rglob("*.md"):
            value, body = metadata(path.read_text(encoding="utf-8"))
            validate(kind, value)
            if kind == "Decision": decision_checks(value)
            for record_kind, item in [(kind, value)] + embedded(body):
                key = item["id"]
                number = re.fullmatch(r"([A-Z]+)-(\d+)", key)
                normalized = (number.group(1), int(number.group(2))) if number else key
                if key in records or normalized in numeric_ids:
                    raise ValueError(f"Duplicate native record identity: {key}")
                records[key], locations[key] = item, path
                numeric_ids.add(normalized)
    ledger = yaml_read((WORKSPACE / "assets/ledger.yaml").read_text(encoding="utf-8"))
    ledger_checks(ledger)
    for asset in ledger["assets"]:
        if asset["id"] in records: raise ValueError("Duplicate asset record id")
        records[asset["id"]], locations[asset["id"]] = asset, WORKSPACE / "assets/ledger.yaml"
    source_ids = {source["id"] for source in workspace["sources"]}
    runtime_ids = {item["id"] for item in workspace["runtime_roots"]}
    for rid, value in records.items():
        if value.get("epic") and value["epic"] not in records:
            raise ValueError(f"Missing Epic: {value['epic']}")
        for reference in refs(value):
            validate("Ref", reference)
            if reference.get("source") and reference["source"] not in source_ids:
                raise ValueError("Unknown source")
            if "path" in reference:
                fixture_path(locations[rid].parent, reference["path"])
            elif not reference.get("source") and reference["id"] not in records:
                raise ValueError(f"Missing native reference: {reference['id']}")
        for use in value.get("selected_uses", []):
            if use["runtime_id"] not in runtime_ids: raise ValueError("Unknown runtime")
        for candidate in value.get("candidates", []):
            path = fixture_path(locations[rid].parent, candidate["manifest"]["path"])
            if candidate["version"]["kind"] == "sha256" and digest(path) != candidate["version"]["value"]:
                raise ValueError("Candidate manifest content differs")
    manifest_path = PROJECT / "assets/flash/manifest.json"
    manifest = json_read(manifest_path); validate("Manifest", manifest)
    for file in manifest["files"]:
        if digest(fixture_path(manifest_path.parent, file["path"])) != file["sha256"]:
            raise ValueError("Manifest file digest mismatch")
    io_count = 0
    for path in (EXAMPLES / "io").glob("*.json"):
        value = json_read(path)
        validate("Request" if path.name.endswith("request.json") else "Response", value)
        if "context" in value:
            # Fixture-only address translation, not runtime authorization/path handling.
            prefix = "C:/ExampleGame"
            base = value["context"].get("base_dir", value["context"]["project_root"])
            if not (base == prefix or base.startswith(prefix + "/")):
                raise ValueError("Unexpected example address")
            base_path = PROJECT / base[len(prefix):].lstrip("/")
            for reference in refs(value.get("expected_subjects", [])):
                if "path" in reference: fixture_path(base_path, reference["path"])
        io_count += 1
    io_fixture_checks(locations)

    # Templates are blueprints. Bind only metadata for a shape check; this is not
    # a general template renderer and never renders project files.
    bindings = {"task_id":"T-901", "epic_id":"E-901", "evidence_id":"EV-901",
                "decision_id":"D-901", "title":"Sample", "kind":"feature",
                "actual_status":"active", "subject_id":"A-001", "checked_scope":"Sample",
                "actual_result":"not_run", "actual_recorded_at":"2026-09-22T00:00:00Z",
                "actual_decider_kind":"agent", "actual_decider_id":"example-agent",
                "actual_action":"choose", "subject_scope":"Sample", "decision_scope":"Sample",
                "actual_conclusion":"Illustrative choice", "project_id":"example",
                "project_name":"Example", "project_root_relative_to_workspace":"..",
                "asset_id":"A-901", "purpose":"Sample", "candidate_id":"C-001",
                "manifest_path_relative_to_ledger":"../../assets/flash/manifest.json",
                "actual_manifest_sha256":digest(manifest_path), "file_path_relative_to_manifest":"flash.json",
                "actual_file_sha256":digest(manifest_path.parent/'flash.json'), "file_role":"runtime-input"}
    def bind(value):
        if isinstance(value, str) and re.fullmatch(r"\{\{[a-z0-9_]+\}\}", value):
            return bindings[value[2:-2]]
        if isinstance(value, dict): return {key:bind(child) for key,child in value.items()}
        if isinstance(value, list): return [bind(child) for child in value]
        return value
    for name, kind in (("task.md.tpl","Task"),("quick-task.md.tpl","Task"),
                       ("epic.md.tpl","Epic"),("evidence.md.tpl","Evidence"),
                       ("decision.md.tpl","Decision")):
        value,_ = metadata((ROOT/'templates'/name).read_text(encoding='utf-8'))
        validate(kind,bind(value))
    for name, kind in (("workspace.yaml.tpl","Workspace"),("asset-ledger.yaml.tpl","AssetLedger")):
        validate(kind,bind(yaml_read((ROOT/'templates'/name).read_text(encoding='utf-8'))))
    validate("Manifest",bind(json_read(ROOT/'templates/manifest.json.tpl')))
    for path in PROJECT.rglob('*'):
        if path.is_file() and '{{' in path.read_text(encoding='utf-8'):
            raise ValueError(f'Unfilled sample: {path}')

    negatives = 0
    def reject(label, operation):
        nonlocal negatives
        try: operation()
        except (ValueError, yaml.YAMLError, ValidationError):
            negatives += 1
        else: raise AssertionError(f'Invalid sample unexpectedly accepted: {label}')
    task=copy.deepcopy(records['T-002'])
    reject('paused lifecycle',lambda:validate('Task',dict(task,status='paused')))
    reject('multiple Epic owners',lambda:validate('Task',dict(task,epic=['E-001','E-002'])))
    reject('duplicate state field',lambda:validate('Task',dict(task,approved=True)))
    reject('reference with id and path',lambda:validate('Ref',{'id':'T-001','path':'tasks/other.md'}))
    reject('unbound named version',lambda:validate('Version',{'kind':'named','value':'latest'}))
    reject('invalid digest',lambda:validate('Version',{'kind':'sha256','value':'r1'}))
    bad=copy.deepcopy(workspace); bad['default_task_source']='spec'
    reject('wrong default role',lambda:workspace_checks(bad))
    bad=copy.deepcopy(workspace); bad['sources'].append(copy.deepcopy(bad['sources'][0]))
    reject('duplicate source',lambda:workspace_checks(bad))
    bad=copy.deepcopy(records['D-001']); bad['events'].append(copy.deepcopy(bad['events'][0]))
    reject('duplicate event',lambda:decision_checks(bad))
    bad=copy.deepcopy(ledger); bad['assets'][0]['selected_uses'][0]['candidate_id']='missing'
    reject('unknown candidate',lambda:ledger_checks(bad))
    reject('empty passed coverage',lambda:validate('Evidence',dict(records['EV-002'],coverage=[])))
    reject('missing write preconditions',lambda:validate('Request',{key:value for key,value in json_read(EXAMPLES/'io/update-task.request.json').items() if key!='preconditions'}))
    reject('duplicate YAML key',lambda:yaml_read('status: active\nstatus: closed\n'))
    reject('duplicate JSON key',lambda:json.loads('{"status":"active","status":"closed"}',object_pairs_hook=unique_mapping))
    reject('YAML alias',lambda:yaml_read('a: &a [1]\nb: *a\n'))
    reject('embedded mismatch',lambda:embedded('<!-- workflow:record evidence EV-1 -->\n```yaml\nid: EV-2\n```\ntext\n<!-- workflow:endrecord EV-1 -->'))
    bad=json_read(EXAMPLES/'io/extract.request.json'); bad['preconditions'][1]['target']={'path':'tasks/unrelated.md'}
    reject('unrelated extraction precondition',lambda:extract_fixture_checks(bad,locations))
    bad=json_read(EXAMPLES/'io/extract.request.json'); bad['preconditions'][1]=copy.deepcopy(bad['preconditions'][0])
    reject('duplicate extraction precondition',lambda:extract_fixture_checks(bad,locations))
    bad=json_read(EXAMPLES/'io/extract.request.json'); bad['preconditions'][1]['expected_revision']='sha256:'+'a'*64
    reject('wrong destination precondition',lambda:extract_fixture_checks(bad,locations))
    bad=json_read(EXAMPLES/'io/create-replayed.response.json'); del bad['receipt']
    reject('successful mutation without receipt',lambda:validate('Response',bad))
    bad=json_read(EXAMPLES/'io/request-id-conflict.response.json'); bad['receipt']=json_read(EXAMPLES/'io/create-replayed.response.json')['receipt']
    reject('conflict with old successful receipt',lambda:validate('Response',bad))
    bad=json_read(EXAMPLES/'io/read-task.response.json'); del bad['data']['reference_base']
    reject('read without reference base',lambda:validate('Response',bad))
    bad=json_read(EXAMPLES/'io/asset-clear.request.json'); bad['payload']['use']=ledger['assets'][0]['selected_uses'][0]
    reject('clear with contradictory selection',lambda:validate('Request',bad))
    reject('nonfinite request digest',lambda:request_digest({'payload':float('nan')}))
    view={'protocol_version':1,'request_id':'example-unsaved-view','operation':'view.build',
          'status':'ok','data':{},'writes':[],'errors':[]}
    validate('Response',view)
    view['writes']=[{'target':{'path':'C:/ExampleGame/game-workflow/views/progress.json'},'status':'written'}]
    reject('saved view without receipt',lambda:validate('Response',view))
    print(f'PASS: schema, {len(records)} native identities, manifest bytes, {io_count} I/O samples, 8 metadata templates, {negatives} negative cases.')
    print('PASS: fixture digest/replay vectors, extraction preconditions/recovery, source readback, and raw-read boundaries.')
    print('Read-only contract check only; write/CAS/idempotency/authorization and game execution are not implemented or tested here.')


if __name__ == '__main__':
    main()
