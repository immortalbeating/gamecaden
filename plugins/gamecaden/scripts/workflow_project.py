"""Source discovery, record resolution and semantic checks for a bound project."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import re

from workflow_formats import (Document, PREFIXES, Record, WorkflowError, canonical, normalized_id,
                              json_load, plain, require, revision, validate, walk_refs, yaml_load)
from workflow_storage import STATE_NAME, file_revision


DEFAULTS = {"vision": ("file", "vision.md"), "spec": ("collection", "spec"),
            "roadmap": ("file", "roadmap.md"), "task": ("collection", "tasks"),
            "epic": ("collection", "epics"), "evidence": ("collection", "evidence"),
            "decision": ("collection", "decisions"), "asset-ledger": ("file", "assets/ledger.yaml"),
            "notes": ("collection", "notes"), "parking-lot": ("file", "parking-lot.md")}


class Project:
    def __init__(self, root, context):
        self.root = Path(root).resolve(strict=True)
        require(self.root.is_dir(), "invalid_scope", "Project root must be a directory")
        require(Path(context["project_root"]).is_absolute(), "invalid_scope", "project_root must be absolute")
        require(Path(context["project_root"]).resolve() == self.root, "permission_denied", "Request root differs from host-bound root")
        self.base = self.path(context.get("base_dir", str(self.root)), self.root)
        self.workspace = self.path(context.get("workspace", "game-workflow/workspace.yaml"), self.root)
        self.home = self.workspace.parent
        self.observed = {}
        self.documents, self.records, self.forwards, self.diagnostics = {}, [], [], []
        self.sources, self.mapping = [], None
        if self.workspace.exists():
            self.mapping = yaml_load(self.read_bytes(self.workspace).decode("utf-8-sig"))
            self.validate_workspace(self.mapping, check_files=False)
            self.sources = plain(self.mapping["sources"])
        else:
            for role, (kind, name) in DEFAULTS.items():
                self.sources.append({"id": role, "role": role, "kind": kind, "path": name,
                                     "owner": "flow", "format": "native-yaml-v1" if role == "asset-ledger" else "native-markdown-v1"})

    def path(self, value, base=None):
        candidate = Path(value)
        if not candidate.is_absolute():
            candidate = (base or self.base) / candidate
        candidate = Path(os.path.abspath(candidate))
        require(candidate.is_relative_to(self.root), "permission_denied", "Path leaves the bound project", {"path": str(candidate)})
        current = self.root
        for part in candidate.relative_to(self.root).parts:
            require(part.lower() not in (".git", STATE_NAME), "permission_denied", "Reserved operational/VCS location")
            current /= part
            require(not current.is_symlink() and not current.is_junction(), "invalid_scope", "Linked paths require an explicit adapter", {"path": str(current)})
        require(candidate.resolve() == candidate, "invalid_scope", "Path resolution changed")
        return candidate

    def read_bytes(self, path):
        path = self.path(path)
        require(path.is_file(), "not_found", "Source file not found", {"path": str(path)})
        data = path.read_bytes()
        observed = revision(data)
        require(str(path) not in self.observed or self.observed[str(path)] == observed,
                "revision_conflict", "Source changed while reading", {"path": str(path)})
        self.observed[str(path)] = observed
        return data

    def validate_workspace(self, value, check_files=True):
        validate("Workspace", value)
        for field in ("sources", "runtime_roots", "rule_sources"):
            ids = [row["id"] for row in value[field]]
            require(len(ids) == len(set(ids)), "invalid_record", f"Duplicate {field} ID")
        require(self.path(value["project"]["root"], self.home) == self.root, "invalid_scope", "Workspace declares another project")
        sources = {row["id"]: row for row in value["sources"]}
        for field, role in (("default_task_source", "task"), ("default_epic_source", "epic")):
            choice = value[field]
            require(choice is None or choice in sources and sources[choice]["role"] == role,
                    "invalid_record", f"{field} does not name a {role} source")
        for row in value["sources"]:
            path = self.path(row["path"], self.home)
            if check_files and row["kind"] == "file":
                require(path.is_file(), "not_found", "Mapped file does not exist", {"path": str(path)})
        for row in value["runtime_roots"]:
            location = self.path(row["path"], self.home)
            marker = self.path(row["marker"], self.home) if row.get("marker") else None
            if check_files:
                require(location.is_dir(), "not_found", "Runtime root missing")
                require(marker is None or marker.is_file(), "not_found", "Runtime marker missing")
        for row in value["rule_sources"]:
            location = self.path(row["path"], self.home)
            if check_files:
                require(location.is_file(), "not_found", "Rule source missing")

    def source_path(self, source):
        return self.path(source["path"], self.home)

    def source_for(self, path, source_id=None):
        matches = []
        if source_id and source_id != "support":
            require(any(s["id"] == source_id for s in self.sources), "invalid_scope", "Unknown source qualifier")
        for source in self.sources:
            if source_id and source["id"] != source_id:
                continue
            location = self.source_path(source)
            if path == location or source["kind"] == "collection" and path.is_relative_to(location):
                matches.append(source)
        if not matches and (source_id is None or source_id == "support") and (path == self.home / "index.md" or path.is_relative_to(self.home / "rules")
                            or path.is_relative_to(self.home / "handoffs") or path.is_relative_to(self.home / "views")):
            return {"id": "support", "role": "document", "kind": "file", "path": str(path), "format": "native-markdown-v1"}
        require(len(matches) <= 1, "ambiguous_ref", "Overlapping source mappings require scoped adapters", {"path": str(path)})
        require(matches or source_id is None, "invalid_scope", "Path does not belong to the qualified source")
        return matches[0] if matches else None

    def document(self, path, source_id=None):
        path = self.path(path)
        source = self.source_for(path, source_id)
        if path in self.documents:
            require(self.documents[path].main.source == (source["id"] if source else None),
                    "ambiguous_ref", "One file has conflicting source interpretations", {"path":str(path)})
        if path not in self.documents:
            data = self.read_bytes(path)
            native = bool(source and source.get("format", "").startswith("native-"))
            if source and not source.get("format") and source.get("owner") in ("flow", "project"):
                # Detect only a valid typed header/ledger, never infer old-system ownership from a filename.
                try:
                    detected = Document(path, data, True, source["role"], source["id"])
                    native = bool(detected.main.id or detected.main.kind == "asset-ledger")
                except (WorkflowError, ValueError):
                    native = False
            self.documents[path] = Document(path, data, native, source["role"] if source else "document",
                                            source["id"] if source else None)
        return self.documents[path]

    def scan(self):
        self.records, self.forwards, self.diagnostics = [], [], []
        self.scan_complete = True
        seen = set()
        for source in self.sources:
            try:
                path = self.source_path(source)
                if self.mapping is None and not path.exists():
                    continue  # Defaults are optional locations, not missing authoritative records.
                if source["kind"] == "collection":
                    files = []
                    if path.exists():
                        for directory, folders, names in os.walk(path, followlinks=False):
                            folders[:] = [name for name in folders if name not in (".git", STATE_NAME)
                                          and not (Path(directory) / name).is_symlink()
                                          and not (Path(directory) / name).is_junction()]
                            files.extend(Path(directory) / name for name in names if Path(name).suffix.lower() in (".md", ".json", ".yaml", ".yml"))
                else:
                    files = [path]
                for file in sorted(files):
                    if file in seen:
                        self.diagnostics.append({"code": "ambiguous_ref", "message": "File belongs to overlapping sources", "target": {"path": str(file)}})
                        continue
                    seen.add(file)
                    try:
                        doc = self.document(file, source["id"])
                        self.records.extend(doc.records if doc.native else [doc.main])
                        self.forwards.extend(doc.forwards)
                        if not doc.native:
                            self.scan_complete = False
                            self.diagnostics.append({"code": "unsupported_format", "message": "Raw source has no structural adapter", "target": {"path": str(file)}})
                    except (WorkflowError, ValueError, TypeError) as exc:
                        self.scan_complete = False
                        error = exc if isinstance(exc, WorkflowError) else WorkflowError("invalid_record", str(exc), {"path": str(file)})
                        self.diagnostics.append(error.item())
            except WorkflowError as exc:
                self.scan_complete = False
                self.diagnostics.append(exc.item())
        groups = {}
        for record in self.records:
            if record.id:
                groups.setdefault(normalized_id(record.id), []).append(record)
        for records in groups.values():
            if len(records) > 1:
                self.diagnostics.append({"code": "duplicate_id", "message": "Multiple active bodies share an identity", "target": {"id": records[0].id}})
        return self.records

    def resolve(self, ref, base=None, chain=()):
        validate("Ref", ref)
        if ref.get("source"):
            require(any(s["id"] == ref["source"] for s in self.sources), "invalid_scope", "Unknown source qualifier")
        if ref.get("project_id"):
            require(self.mapping and ref["project_id"] == self.mapping["project"]["id"], "invalid_scope", "Cross-project references need another bound service")
        if "path" in ref:
            path = self.path(ref["path"], base or self.base)
            doc = self.document(path, ref.get("source"))
            fragment = ref.get("fragment")
            options = [r for r in doc.records + doc.forwards if fragment and r.id == fragment]
            record = options[0] if len(options) == 1 else doc.main
        else:
            if not self.records:
                self.scan()
            options = [r for r in self.records if r.id and normalized_id(r.id) == normalized_id(ref["id"])
                       and (not ref.get("source") or r.source == ref["source"])]
            if not options:
                options = [r for r in self.forwards if r.id and normalized_id(r.id) == normalized_id(ref["id"])
                           and (not ref.get("source") or r.source == ref["source"])]
            require(options, "not_found", "Record ID not found", ref)
            bodies = [r for r in options if r.kind != "forward"]
            require(len(bodies or options) == 1, "ambiguous_ref", "Identity has multiple bodies/forwards", ref)
            record = (bodies or options)[0]
        if record.kind == "forward":
            key = (str(record.path), record.id)
            require(key not in chain, "ambiguous_ref", "Forward cycle", ref)
            target = self.resolve(record.forward, record.path.parent, chain + (key,))
            require(target.id == record.id, "invalid_record", "Forward target has a different identity")
            record = target
        fragment = ref.get("fragment")
        if fragment and fragment != record.id:
            if record.kind == "decision":
                require(any(e["event_id"] == fragment for e in record.metadata["events"]), "not_found", "Decision event not found", ref)
            else:
                body = record.body or ""
                anchors = re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)[\"\']', body)
                headings = [re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in re.findall(r"^#+\s+(.+)$", body, re.M)]
                require(fragment in anchors + headings, "not_found", "Markdown anchor not found", ref)
        return record

    def ensure_writable(self, record):
        require(record.format.startswith("native-"), "unsupported_write", "Source has no native write adapter", {"path": str(record.path)})
        source = self.source_for(record.path, record.source)
        require(source is not None and source.get("format", "").startswith("native-") or
                source is not None and source.get("owner") in ("flow", "project"),
                "unsupported_write", "Source is not owned by the native writer")

    def read_record(self, record, include_body=True):
        native = record.format.startswith("native-")
        caps = ["record.read"]
        if native:
            caps += ["asset.upsert", "asset.select"] if record.kind in ("asset", "asset-ledger") else ["record.update"]
            if record.kind in ("task", "epic"):
                caps += ["record.transition"]
            if record.span is not None:
                caps += ["record.extract"]
            if record.kind == "decision":
                caps += ["decision.record"]
        return {"ref": {"id": record.id} if record.id else {"path": str(record.path)},
                "path": str(record.path), "reference_base": str(record.path.parent) if native else None,
                "format": record.format, "interpretation": "native" if native else "raw",
                "revision": self.observed[str(record.path)], "metadata": plain(record.metadata),
                "body": record.body if include_body else None, "capabilities": caps,
                "diagnostics": [] if native else [{"code": "unsupported_write", "message": "No write adapter", "target": {"path": str(record.path)}}]}

    def check_refs(self, value, base):
        for ref in walk_refs(value):
            self.resolve(ref, base)

    def check_subject(self, subject, base, verify_version=True):
        record = self.resolve(subject["ref"], base)
        version = subject.get("version")
        candidate = None
        if subject.get("use"):
            ids = [r["id"] for r in self.mapping["runtime_roots"]] if self.mapping else []
            require(subject["use"]["runtime_id"] in ids, "invalid_scope", "Unknown runtime in subject")
        if subject.get("candidate_id"):
            require(record.kind == "asset", "invalid_scope", "Candidate subject must reference an asset")
            matches = [c for c in record.metadata["candidates"] if c["id"] == subject["candidate_id"]]
            require(len(matches) == 1, "invalid_scope", "Candidate not found")
            candidate = matches[0]
            if verify_version:
                self.check_candidate(candidate, record.path.parent, record.id)
                if version:
                    require(version["kind"] == candidate["version"]["kind"] and version["value"] == candidate["version"]["value"],
                            "version_mismatch", "Subject does not name the candidate version")
        if not version or not verify_version:
            return
        require(version["kind"] == "sha256", "unsupported_format", "Current-version verification requires sha256; other version kinds need a producer adapter")
        if version.get("proof"):
            path = self.resolve(version["proof"], base).path
        elif candidate is not None:
            path = self.resolve(candidate["manifest"], record.path.parent).path
        else:
            require("path" in subject["ref"], "invalid_scope", "sha256 needs an explicit file proof")
            path = record.path
        require(revision(self.read_bytes(path))[7:] == version["value"], "version_mismatch", "Subject file bytes changed", {"path": str(path)})

    def check_candidate(self, candidate, base, asset_id):
        manifest_path = self.resolve(candidate["manifest"], base).path
        data = self.read_bytes(manifest_path)
        if candidate["version"].get("proof"):
            require(self.resolve(candidate["version"]["proof"], base).path == manifest_path, "invalid_scope", "Candidate proof must point to its manifest")
        require(candidate["version"]["kind"] == "sha256", "unsupported_format", "Candidate version requires a manifest SHA-256 adapter")
        require(revision(data)[7:] == candidate["version"]["value"], "version_mismatch", "Manifest changed")
        try:
            manifest = json_load(data.decode("utf-8-sig"))
            validate("Manifest", manifest)
        except (ValueError, WorkflowError) as exc:
            raise WorkflowError("unsupported_format", "Manifest has no supported content-check adapter") from exc
        require(manifest["asset_id"] == asset_id and manifest["candidate_id"] == candidate["id"], "invalid_record", "Manifest identity mismatch")
        paths = []
        for row in manifest["files"]:
            path = self.path(row["path"], manifest_path.parent)
            require(path not in paths, "invalid_record", "Duplicate manifest file")
            paths.append(path)
            require(revision(self.read_bytes(path))[7:] == row["sha256"], "version_mismatch", "Manifest member changed", {"path": str(path)})

    def semantic(self, kind, metadata, base, changed=None):
        validate(kind.title() if kind != "asset-ledger" else "AssetLedger", metadata)
        if kind == "task" and metadata.get("epic"):
            epic = self.resolve({"id": metadata["epic"]}, base)
            require(epic.kind == "epic", "invalid_scope", "Task parent is not an Epic")
        if kind == "decision":
            events = metadata["events"]
            require(len({e["event_id"] for e in events}) == len(events), "invalid_record", "Duplicate Decision event")
        if kind in ("asset", "asset-ledger"):
            assets = [metadata] if kind == "asset" else metadata["assets"]
            require(len({a["id"] for a in assets}) == len(assets), "duplicate_id", "Duplicate asset")
            for asset in assets:
                candidates = asset["candidates"]
                require(len({c["id"] for c in candidates}) == len(candidates), "invalid_record", "Duplicate candidate")
                uses = asset["selected_uses"]
                require(len({u["use_id"] for u in uses}) == len(uses), "invalid_record", "Duplicate use")
                for use in uses:
                    require(use["candidate_id"] in {c["id"] for c in candidates}, "invalid_scope", "Unknown selected candidate")
                    runtime_ids = {r["id"] for r in self.mapping["runtime_roots"]} if self.mapping else set()
                    require(use["runtime_id"] in runtime_ids, "invalid_scope", "Unknown selected runtime")
        self.check_refs(metadata if changed is None else changed, base)
