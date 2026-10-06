"""Local v1 workflow API and JSON-file/stdin CLI. Run --help for invocation."""
from __future__ import annotations

import argparse
import base64
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import threading

import yaml

from workflow_formats import (Document, PREFIXES, WorkflowError, canonical, forward_block, json_load,
                              normalized_id, plain, rebase, rebase_markdown, record_block, request_digest,
                              require, revision, validate, walk_refs, yaml_dump)
from workflow_project import DEFAULTS, Project
from workflow_storage import Store, file_revision, plan_write


READS = {"workspace.inspect", "record.list", "record.read", "record.resolve", "operation.status"}


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class Workflow:
    """Bound root/identity are host inputs, never trusted from the JSON request.

    decision_authorizer(event, request) is an optional trusted host callback.
    The CLI does not impersonate a user or expose this callback in request JSON.
    fault is a library-only test hook; it is not a request or CLI capability.
    """
    def __init__(self, project_root, *, actor=None, decision_authorizer=None, fault=None):
        self.root = Path(project_root).resolve(strict=True)
        self.actor = actor or {"kind": "agent", "id": "local-cli"}
        self.authorize_decision = decision_authorizer
        self.fault = fault
        self.call_lock = threading.RLock()

    def response(self, request, status="ok", data=None, writes=None, errors=None, receipt=None, replayed=False):
        operations = READS | {"workspace.configure", "record.create", "record.update", "record.transition", "record.extract",
                              "decision.record", "asset.upsert", "asset.select", "view.build"}
        if not isinstance(request.get("operation"), str) or request["operation"] not in operations or not isinstance(request.get("request_id"), str) or not request.get("request_id"):
            return {"status": "rejected", "errors": errors or [{"code": "invalid_request", "message": "Invalid request envelope"}]}
        result = {"protocol_version": 1, "request_id": request.get("request_id", "invalid-request"),
                  "operation": request.get("operation", "workspace.inspect"), "status": status,
                  "writes": writes or [], "errors": errors or []}
        if data is not None:
            result["data"] = plain(data)
        if receipt is not None:
            result["receipt"] = plain(receipt)
        if replayed:
            result["replayed"] = True
        return result

    def execute(self, request):
        if not isinstance(request, dict):
            return {"status": "rejected", "errors": [{"code": "invalid_request", "message": "Request must be a JSON object"}]}
        with self.call_lock:
            return self._execute(request)

    def _execute(self, request):
        self.request = copy.deepcopy(request)
        self.plans, self.allocations = [], []
        self.preconditions, self.covered = {}, set()
        self.touched = []
        try:
            validate("Request", request)
            self.project = Project(self.root, request["context"])
            self.store = Store(self.root, self.project.path, self.fault)
            op = request["operation"]
            readonly = op in READS or op == "view.build" and not request["payload"].get("output_path")
            with self.store.lock(write=not readonly):
                # Re-read mappings after obtaining the lock; previous context grants no stale capability.
                self.project = Project(self.root, request["context"])
                self.store.guard = self.project.path
                if op == "operation.status":
                    value = self.store.load(request["payload"]["request_id"])
                    require(value is not None, "not_found", "No receipt exists; absence alone does not prove no manual write occurred")
                    observed = value if value["receipt"]["phase"] == "settled" else self.store.reconcile(value)
                    return self.response(request, data={"queried_at": now(), "files_rechecked": value["receipt"]["phase"] != "settled"}, writes=observed["writes"],
                                         errors=observed["errors"], receipt=observed["receipt"])
                digest = request_digest(request)
                if not readonly:
                    existing = self.store.load(request["request_id"])
                    if existing:
                        require(existing["receipt"]["request_digest"] == digest, "request_id_conflict", "request_id already names different content; query operation.status")
                        if existing["receipt"]["phase"] != "settled":
                            self.check_replay_authority(existing)
                            existing = self.store.apply(existing)
                        return self.response(request, existing["receipt"]["outcome"], existing["data"],
                                             existing["writes"], existing["errors"], existing["receipt"], True)
                if readonly:
                    data = self.read_operation(op, request["payload"])
                    self.check_read_snapshot()
                    return self.response(request, data=data)
                self.project.scan()
                for condition in request["preconditions"]:
                    path = self.ref_path(condition["target"])
                    require(path not in self.preconditions, "invalid_record", "Duplicate precondition target")
                    self.preconditions[path] = condition["expected_revision"]
                for subject in request.get("expected_subjects", []):
                    self.project.check_subject(subject, self.project.base)
                data = self.write_operation(op, request["payload"])
                for pending in self.store.pending():
                    owned = {Path(plan["path"]) for plan in pending["plans"]}
                    require(not owned.intersection({Path(p["path"]) for p in self.plans}), "operation_pending", "An earlier operation owns this file; resume it first")
                # All supplied conditions, including non-write dependencies, must hold.
                for path, expected in self.preconditions.items():
                    require(file_revision(path) == expected, "revision_conflict", "Precondition no longer holds", {"path": str(path)})
                    self.project.observed[str(path)] = expected
                self.check_read_snapshot()
                value = self.store.prepare(request, digest, self.plans, self.allocations, self.project.observed, data)
                value = self.store.apply(value)
                return self.response(request, value["receipt"]["outcome"], value["data"], value["writes"], value["errors"], value["receipt"])
        except (WorkflowError, ValueError, TypeError, KeyError, OSError, yaml.YAMLError) as exc:
            error = exc if isinstance(exc, WorkflowError) else WorkflowError("invalid_record", str(exc))
            status = "indeterminate" if error.code == "indeterminate" else "conflict" if error.code in ("revision_conflict", "request_id_conflict", "version_mismatch", "stale_cursor", "duplicate_id", "operation_pending") else "rejected"
            writes = [{"target": {"path": str(path)}, "status": "not_attempted"} for path in dict.fromkeys(self.touched)]
            return self.response(request, status, writes=writes, errors=[error.item()])

    def ref_path(self, ref):
        if "path" in ref:
            return self.project.path(ref["path"])
        return self.project.resolve(ref).path

    def check_read_snapshot(self):
        for name, expected in self.project.observed.items():
            require(file_revision(self.project.path(name)) == expected, "revision_conflict", "Source changed during planning/read", {"path": name})

    def pending_for(self, record):
        for value in self.store.pending():
            if any(Path(p["path"]) == record.path for p in value["plans"]):
                raise WorkflowError("operation_pending", "Record has an unfinished write; query its operation", {"path": str(record.path)})

    def checked_record(self, ref):
        record = self.project.resolve(ref)
        self.touched.append(record.path)
        self.pending_for(record)
        self.project.ensure_writable(record)
        return record

    def write(self, path, data, *, allocated=False):
        path = self.project.path(path)
        self.touched.append(path)
        require(not path.is_dir(), "invalid_scope", "Write target is a directory")
        current = file_revision(path)
        require(path in self.preconditions or allocated and current is None,
                "precondition_required", "Provide a precondition for this actual file", {"path": str(path)})
        expected = self.preconditions.get(path)
        require(expected == current, "revision_conflict", "File does not match expected revision", {"path": str(path)})
        require(not any(Path(p["path"]) == path for p in self.plans), "invalid_record", "Multiple writes to one file in a request")
        self.plans.append(plan_write(path, current, data))

    def allocate(self, kind, wanted=None, path=None):
        self.project.scan()
        blockers = [d for d in self.project.diagnostics if d["code"] not in ("unsupported_format",)]
        require(not blockers, "invalid_record", "Cannot allocate with unresolved native source/identity errors")
        used = {normalized_id(r.id) for r in self.project.records + self.project.forwards if r.id}
        for record in self.project.records:
            for ref in walk_refs(record.metadata):
                if ref.get("id") and not ref.get("project_id") and not ref.get("source"):
                    used.add(normalized_id(ref["id"]))
            if record.kind == "task" and record.metadata and record.metadata.get("epic"):
                used.add(normalized_id(record.metadata["epic"]))
        for value in self.store.all():
            used.update(normalized_id(a["ref"]["id"]) for a in value["receipt"]["allocations"])
        prefix = PREFIXES[kind]
        if wanted:
            require(re.fullmatch(prefix + r"-\d+", wanted), "invalid_record", "Wrong identity prefix")
            require(normalized_id(wanted) not in used, "duplicate_id", "Identity is already used/reserved")
            return wanted
        maximum = max((value[1] for value in used if isinstance(value, tuple) and value[0] == prefix), default=0)
        return f"{prefix}-{maximum + 1:03d}"

    def allocation(self, kind, rid, path):
        self.allocations.append({"ref": {"id": rid}, "path": str(path), "record_type": kind})

    def default_path(self, kind, rid=None, owner=None):
        if kind in ("design", "plan", "history"):
            require(owner is not None, "invalid_record", "Attachment needs its owning work")
            work = self.project.resolve(owner)
            require(work.kind in ("task", "epic"), "invalid_scope", "Attachment owner must be a Task or Epic")
            folder = work.path.parent / work.id if work.kind == "task" else work.path.parent
            return folder / (kind + ".md")
        if kind == "index":
            return self.project.home / "index.md"
        require(kind not in ("rule", "handoff"), "invalid_record", "Supply an explicit path for a rule/handoff")
        role = kind
        sources = [s for s in self.project.sources if s["role"] == role]
        if self.project.mapping and kind in ("task", "epic"):
            source_id = self.project.mapping[f"default_{kind}_source"]
            sources = [s for s in sources if s["id"] == source_id]
        if not sources and kind in DEFAULTS and not any(s["role"] == kind for s in self.project.sources):
            form, name = DEFAULTS[kind]
            sources = [{"id":kind,"role":kind,"kind":form,"path":name,"owner":"project","format":"native-markdown-v1"}]
        require(len(sources) == 1, "ambiguous_ref", f"Select a unique {kind} source/path")
        source = sources[0]
        require(source.get("format", "").startswith("native-"), "unsupported_write", "Default source has no native writer")
        folder = self.project.source_path(source)
        if source["kind"] == "file":
            return folder
        if kind == "task":
            return folder / f"{rid}-work.md"
        if kind == "epic":
            return folder / f"{rid}-work" / "epic.md"
        if rid:
            return folder / f"{rid}.md"
        require(kind == "spec", "invalid_record", "Supply a descriptive filename for this document")
        return folder / "index.md"

    def new_destination(self, path, kind, *, allow_unmapped=False):
        path = self.project.path(path)
        source = self.project.source_for(path)
        require(source is None and allow_unmapped or source is not None and source.get("format", "").startswith("native-"),
                "unsupported_write", "Destination has no suitable native source")
        require(not path.exists(), "revision_conflict", "Creation target already exists", {"path": str(path)})
        return path

    def registration(self, kind, path):
        if self.project.source_for(path) is not None:
            return {}
        role = kind if kind in DEFAULTS else None
        if role is None:
            return {"source_registration_required": True}
        used = {s["id"] for s in self.project.sources}
        source_id = role
        suffix = 2
        while source_id in used:
            source_id = f"{role}-{suffix}"
            suffix += 1
        fmt = "native-json-v1" if path.suffix == ".json" else "native-yaml-v1" if path.suffix in (".yaml", ".yml") else "native-markdown-v1"
        form, location = "file", path
        default_form, default_name = DEFAULTS[role]
        if default_form == "collection" and path.is_relative_to(self.project.home / default_name):
            form, location = "collection", self.project.home / default_name
        return {"source_registration_required": True, "source_proposal": {"id":source_id,"role":role,"kind":form,
                    "path":Path(os.path.relpath(location,self.project.home)).as_posix(),"owner":"project","format":fmt}}

    def read_operation(self, operation, payload):
        if operation == "workspace.inspect":
            self.project.scan()
            return {"project_root": str(self.root), "workspace": str(self.project.workspace),
                    "configured": self.project.mapping is not None, "mapping": plain(self.project.mapping),
                    "sources": [{**s, "resolved_path": str(self.project.source_path(s))} for s in self.project.sources],
                    "diagnostics": self.project.diagnostics, "runtime_verified": False}
        if operation in ("record.read", "record.resolve"):
            self.project.scan()
            record = self.project.resolve(payload["target"])
            self.pending_for(record)
            return self.project.read_record(record, payload.get("include_body", True))
        if operation == "record.list":
            return self.list_records(payload)
        if operation == "view.build":
            return self.build_view(payload)
        raise WorkflowError("unsupported_format", "Unknown read operation")

    def list_records(self, payload):
        import base64
        records = self.project.scan()
        source_revisions = [{"ref": {"path": p}, "revision": rev} for p, rev in sorted(self.project.observed.items())]
        fingerprint = revision(canonical({"sources": source_revisions, "diagnostics": self.project.diagnostics,
                                          "filter": {k: v for k, v in payload.items() if k != "cursor"}}).encode("utf-8"))
        offset = 0
        if payload.get("cursor"):
            try:
                cursor = json_load(base64.urlsafe_b64decode(payload["cursor"]).decode("utf-8"))
                require(cursor["snapshot"] == fingerprint and isinstance(cursor["offset"], int) and cursor["offset"] >= 0,
                        "stale_cursor", "Sources or list query changed; start a new listing")
                offset = cursor["offset"]
            except (ValueError, KeyError, TypeError) as exc:
                raise WorkflowError("stale_cursor", "Invalid cursor") from exc
        selected = []
        for record in records:
            if payload.get("types") and record.kind not in payload["types"]:
                continue
            if payload.get("status") and (not record.metadata or record.metadata.get("status") not in payload["status"]):
                continue
            if payload.get("text") and payload["text"].casefold() not in canonical(record.metadata).casefold() + (record.body or "").casefold():
                continue
            selected.append(record)
        selected.sort(key=lambda r: (str(r.path), r.id or ""))
        page = selected[offset:offset + payload.get("limit", 100)]
        items = []
        for record in page:
            data = self.project.read_record(record, False)
            items.append({k: data[k] for k in ("ref", "path", "reference_base", "revision", "metadata", "diagnostics")} | {"record_type": record.kind})
        next_offset = offset + len(page)
        cursor = base64.urlsafe_b64encode(canonical({"snapshot": fingerprint, "offset": next_offset}).encode()).decode() if next_offset < len(selected) else None
        diagnostics = copy.deepcopy(self.project.diagnostics)
        if self.store.pending():
            diagnostics.append({"code": "operation_pending", "message": "Some records have unfinished operations"})
        return {"items": items, "next_cursor": cursor, "complete": self.project.scan_complete,
                "source_revisions": source_revisions, "diagnostics": diagnostics}

    def build_view(self, payload):
        records = self.project.scan()
        if payload.get("scope_refs"):
            records = [self.project.resolve(ref) for ref in payload["scope_refs"]]
        kinds = {"progress": {"task", "epic"}, "timeline": {"task", "epic", "decision", "evidence"}, "assets": {"asset"}}[payload["view"]]
        entries = []
        for record in records:
            if record.kind in kinds:
                entry = self.project.read_record(record)
                if payload["view"] == "assets":
                    entry["runtime_adoption"] = "unknown"
                    entry["acceptance"] = "needs_review"
                entries.append(entry)
        return {"view": payload["view"], "generated_at": now(), "entries": entries,
                "source_revisions": [{"ref": {"path": p}, "revision": r} for p, r in sorted(self.project.observed.items())],
                "diagnostics": self.project.diagnostics,
                "interpretation": "Source excerpts; lifecycle does not prove delivery, acceptance or runtime adoption."}

    def write_operation(self, operation, payload):
        if operation == "workspace.configure":
            document = payload["document"]
            self.project.validate_workspace(document)
            old = self.project.mapping
            if old:
                merged = copy.deepcopy(old)
                merged.update(document)
                document = merged
            path = self.project.workspace
            data = Document(path, path.read_bytes(), True, "workspace").render(metadata=document) if path.exists() else yaml_dump(document).encode("utf-8")
            self.write(path, data)
            return {"workspace": str(path)}
        if operation == "record.create":
            return self.create_record(payload)
        if operation in ("record.update", "record.transition"):
            return self.update_record(payload, transition=operation == "record.transition")
        if operation == "record.extract":
            return self.extract_record(payload)
        if operation == "decision.record":
            return self.record_decision(payload)
        if operation in ("asset.upsert", "asset.select"):
            return self.asset_operation(payload, select=operation == "asset.select")
        if operation == "view.build":
            data = self.build_view(payload)
            path = self.project.path(payload["output_path"])
            self.check_view_destination(path)
            self.write(path, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
            return data
        raise WorkflowError("unsupported_format", "Unknown write operation")

    def check_view_destination(self, path):
        require(path.suffix == ".json", "unsupported_format", "The local view builder saves JSON projections")
        source = self.project.source_for(path)
        require(source is None or path.is_relative_to(self.project.home / "views") and source["id"] == "support",
                "invalid_scope", "A derived view cannot overwrite an authoritative source")

    def create_record(self, payload):
        kind = payload["record_type"]
        if kind in ("design", "plan", "history"):
            owner = self.project.resolve(payload["owner"])
            require(owner.kind in ("task", "epic"), "invalid_scope", "Attachment owner must be a real Task/Epic")
        metadata = copy.deepcopy(payload.get("metadata"))
        body = payload["body"].replace("\r\n", "\n")
        if kind in PREFIXES:
            require(isinstance(metadata, dict), "invalid_record", "Typed record requires metadata")
            metadata["id"] = self.allocate(kind, metadata.get("id"))
        else:
            require(not metadata or not metadata.get("id"), "invalid_record", "Plain/attachment documents do not allocate a management ID")
        if payload.get("storage") == "embedded":
            require(kind == "evidence" and payload.get("container") and not payload.get("path"), "invalid_record", "Only Evidence uses embedded record.create; provide its container")
            container = self.checked_record(payload["container"])
            require(container.kind in ("task", "epic") and container.span is None, "invalid_scope", "Embed in a Task/Epic main document")
            path = container.path
            metadata = rebase(metadata, self.project.base, path.parent, self.project.path)
            self.project.semantic(kind, metadata, path.parent)
            doc = self.project.document(path)
            text = container.body.rstrip() + "\n\n" + record_block(kind, metadata, body) + "\n"
            self.write(path, doc.render(body=text))
        else:
            require(not payload.get("container"), "invalid_record", "Standalone creation cannot name a container")
            path = self.project.path(payload["path"]) if payload.get("path") else self.default_path(kind, metadata.get("id") if metadata else None, payload.get("owner"))
            path = self.new_destination(path, kind, allow_unmapped=True)
            if metadata:
                if kind in PREFIXES:
                    metadata = rebase(metadata, self.project.base, path.parent, self.project.path)
                    self.project.semantic(kind, metadata, path.parent)
            require(path.suffix == ".md", "unsupported_format", "record.create writes native Markdown")
            text = ("---\n" + yaml_dump(metadata) + "---\n" if metadata is not None else "") + body
            data = text.encode("utf-8")
            created = Document(path, data, True, kind)
            require(not any(r.span is not None for r in created.records) and not created.forwards,
                    "invalid_record", "Create addressed embedded records with their dedicated operation")
            source = self.project.source_for(path)
            if source is not None:
                # Validate the same source interpretation used by later reads and enumeration.
                Document(path, data, True, source["role"], source["id"])
            self.write(path, data, allocated=not payload.get("path"))
        if kind in PREFIXES:
            self.allocation(kind, metadata["id"], path)
        return {"ref": {"id": metadata["id"]} if kind in PREFIXES else {"path": str(path)}, "path": str(path), **self.registration(kind,path)}

    def protect(self, before, after, allow_events=False):
        require(before.id == after.id and before.kind == after.kind, "invalid_record", "Record identity/type cannot change")
        if before.kind == "decision":
            old, new = before.metadata["events"], after.metadata["events"]
            require(new[:len(old)] == old and (allow_events or new == old), "invalid_record", "Formal events are append-only through decision.record")
        if before.kind == "evidence":
            def facts(meta):
                return {k: v for k, v in meta.items() if k not in ("title", "extensions")}
            require(facts(before.metadata) == facts(after.metadata), "invalid_record", "Substantive Evidence correction needs a new record")
        if before.kind in ("decision", "evidence") and before.body:
            require((after.body or "").startswith(before.body), "invalid_record", "Append explanatory corrections; preserve original observations/reasons")

    def protect_blocks(self, doc, data):
        updated = Document(doc.path, data, True, doc.main.kind, doc.main.source)
        old = {r.id: r for r in doc.records if r.span is not None}
        new = {r.id: r for r in updated.records if r.span is not None}
        require(set(old) == set(new), "invalid_record", "Use creation/extraction operations to change embedded identities")
        for rid, record in old.items():
            self.protect(record, new[rid])
        require([(r.id, r.forward) for r in doc.forwards] == [(r.id, r.forward) for r in updated.forwards],
                "invalid_record", "Existing forwards must be preserved")

    def update_record(self, payload, transition=False):
        record = self.checked_record(payload["target"])
        require(record.kind not in ("asset", "asset-ledger"), "unsupported_write", "Use asset operations for the ledger")
        doc = self.project.document(record.path)
        metadata = copy.deepcopy(record.metadata)
        body = payload.get("body", record.body)
        fields = payload.get("set_fields", {})
        require(not set(fields).intersection({"id", "status", "events"}), "invalid_record", "Use the owning operation for identity/lifecycle/events")
        if fields:
            require(metadata is not None, "invalid_record", "This document has no metadata block")
            metadata.update(rebase(fields, self.project.base, record.path.parent, self.project.path) if record.kind in PREFIXES else fields)
        if transition:
            require(record.kind in ("task", "epic"), "invalid_transition", "Only Task/Epic has a lifecycle")
            metadata["status"] = payload["to"]
            note = f"\n\n<!-- workflow:transition -->\n{now()} · {record.metadata['status']} → {payload['to']}\n\n{payload['reason']}\n"
            for key in ("evidence_refs", "decision_refs"):
                for ref in payload.get(key, []):
                    self.project.resolve(ref)
                    note += f"\n{key}: `{canonical(rebase(ref, self.project.base, record.path.parent, self.project.path))}`\n"
            body = (body or "").rstrip() + note
        if metadata and record.kind in PREFIXES:
            self.project.semantic(record.kind, metadata, record.path.parent, fields)
        data = doc.data if metadata == record.metadata and body == record.body else doc.replace_record(record, metadata, body)
        updated = Document(record.path, data, True, doc.main.kind, doc.main.source)
        after = next((r for r in updated.records if r.id == record.id), updated.main)
        self.protect(record, after)
        self.protect_blocks(doc, data)
        self.write(record.path, data)
        return {"ref": {"id": record.id} if record.id else {"path": str(record.path)}, "path": str(record.path)}

    def extract_record(self, payload):
        record = self.checked_record(payload["target"])
        require(record.span is not None and record.kind in ("evidence", "decision"), "invalid_scope", "Extraction needs an embedded native record")
        destination = self.project.path(payload["destination"])
        if destination.exists():
            require(payload.get("recovery_of"), "revision_conflict", "Existing extraction target needs an explicit interrupted-operation reference")
            prior = self.store.load(payload["recovery_of"])
            require(prior and prior["receipt"]["operation"] == "record.extract"
                    and prior["receipt"]["phase"] == "settled" and prior["receipt"]["outcome"] == "partial",
                    "invalid_scope", "recovery_of must name a settled partial extraction")
            require(prior["data"]["ref"]["id"] == record.id and Path(prior["data"]["path"]) == destination
                    and Path(prior["data"]["previous_path"]) == record.path, "invalid_scope", "Recovery does not match the original extraction")
            target_doc = self.project.document(destination)
            self.project.ensure_writable(target_doc.main)
        else:
            self.new_destination(destination, record.kind)
        require(destination.suffix == ".md", "unsupported_format", "Extraction destination must be Markdown")
        metadata = rebase(record.metadata, record.path.parent, destination.parent, self.project.path)
        body = rebase_markdown(record.body, record.path.parent, destination.parent, self.project.path)
        original_base = Path(os.path.relpath(record.path.parent, destination.parent)).as_posix()
        body += f"\n\n<!-- workflow:extraction-origin -->\n未另行声明基准、且未被重定位的代码/自由文本相对路径，仍以本文件旁的 `{original_base}/` 为原始基准。\n"
        target = ("---\n" + yaml_dump(metadata) + "---\n" + body + "\n").encode("utf-8")
        Document(destination, target, True, record.kind)
        if destination.exists():
            require(plain(target_doc.main.metadata) == plain(metadata) and target_doc.main.body.rstrip() == body.rstrip(),
                    "revision_conflict", "Interrupted target differs; inspect it instead of overwriting")
            target = target_doc.data
        self.write(destination, target)
        doc = self.project.document(record.path)
        start, end = record.span
        relative = Path(os.path.relpath(destination, record.path.parent)).as_posix()
        body = doc.main.body[:start] + forward_block(record.id, relative) + doc.main.body[end:]
        self.write(record.path, doc.render(body=body))
        return {"ref": {"id": record.id}, "path": str(destination), "previous_path": str(record.path)}

    def authorize_event(self, event):
        actor = {k: event["actor"][k] for k in ("kind", "id")}
        trusted = actor == self.actor and actor["kind"] != "user"
        if not trusted and self.authorize_decision:
            trusted = bool(self.authorize_decision(plain(event), copy.deepcopy(self.request)))
        require(trusted, "permission_denied", "Decision actor needs matching host identity or a trusted host decision callback")

    def check_event(self, event, base):
        validate("DecisionEvent", event)
        self.project.check_refs(event, base)
        def identity(subject, origin):
            record = self.project.resolve(subject["ref"], origin)
            return record.id, record.path
        def version_key(subject):
            version = subject.get("version", {})
            return version.get("kind"), version.get("value")
        prior_subjects = []
        for replacement in event.get("replaces", []):
            require(replacement.get("fragment"), "invalid_scope", "Replacement must identify an event")
            old = self.project.resolve(replacement, base)
            require(old.kind == "decision", "invalid_scope", "Replacement target is not a Decision")
            old_event = next(e for e in old.metadata["events"] if e["event_id"] == replacement["fragment"])
            prior_subjects.extend((s, old.path.parent) for s in old_event["subjects"])
        for subject in event["subjects"]:
            if prior_subjects:
                candidates = [s for s, origin in prior_subjects if identity(s, origin) == identity(subject, base)]
                candidates = [s for s in candidates if s.get("use") == subject.get("use") and
                              (s.get("use") or s["scope"] == subject["scope"])]
                require(candidates, "invalid_scope", "Replacement must identify a previously named object and exact use/scope")
                if event["action"] == "withdraw":
                    require(any(s.get("candidate_id") == subject.get("candidate_id") and version_key(s) == version_key(subject) for s in candidates),
                            "invalid_scope", "Withdrawal must name the previously accepted candidate/version")
            expected = self.request.get("expected_subjects", [])
            if expected:
                require(any(identity(s, self.project.base) == identity(subject, base) and version_key(s) == version_key(subject)
                            and s.get("candidate_id") == subject.get("candidate_id") and s.get("use") == subject.get("use")
                            and s["scope"] == subject["scope"] for s in expected),
                        "invalid_scope", "Current-review preconditions do not cover this decision subject")
        # Historical recording is allowed; current applicability requires expected_subjects.
        for subject in event["subjects"]:
            self.project.check_subject(subject, base, verify_version=False)

    def record_decision(self, payload):
        event = copy.deepcopy(payload["event"])
        self.authorize_event(event)
        event["recorded_at"] = now()
        if payload.get("target"):
            require(not any(key in payload for key in ("storage", "container", "path")), "invalid_scope", "Appending does not relocate a Decision")
            record = self.checked_record(payload["target"])
            require(record.kind == "decision", "invalid_scope", "Target is not a Decision")
            event = rebase(event, self.project.base, record.path.parent, self.project.path)
            self.check_event(event, record.path.parent)
            metadata = copy.deepcopy(record.metadata)
            require(event["event_id"] not in {e["event_id"] for e in metadata["events"]}, "invalid_record", "Decision event ID is already used")
            metadata["events"].append(event)
            data = self.project.document(record.path).replace_record(record, metadata, record.body)
            self.write(record.path, data)
            return {"ref": {"id": record.id, "fragment": event["event_id"]}, "path": str(record.path)}
        require(payload.get("title"), "invalid_record", "New Decision needs a title")
        rid = self.allocate("decision")
        metadata = {"id": rid, "title": payload["title"], "events": [event]}
        if payload.get("storage") == "embedded":
            require(payload.get("container") and not payload.get("path"), "invalid_record", "Embedded Decision needs a container")
            container = self.checked_record(payload["container"])
            require(container.kind in ("task", "epic") and container.span is None, "invalid_scope", "Decision container must be a Task/Epic main record")
            path = container.path
            metadata = rebase(metadata, self.project.base, path.parent, self.project.path)
            self.check_event(metadata["events"][0], path.parent)
            data = self.project.document(path).render(body=container.body.rstrip() + "\n\n" + record_block("decision", metadata, "") + "\n")
            self.write(path, data)
        else:
            require(not payload.get("container"), "invalid_record", "Standalone Decision cannot name a container")
            path = self.project.path(payload["path"]) if payload.get("path") else self.default_path("decision", rid)
            self.new_destination(path, "decision", allow_unmapped=True)
            metadata = rebase(metadata, self.project.base, path.parent, self.project.path)
            self.check_event(metadata["events"][0], path.parent)
            require(path.suffix in (".md", ".json"), "unsupported_format", "Decision uses Markdown or JSON")
            text = "---\n" + yaml_dump(metadata) + "---\n" if path.suffix == ".md" else json.dumps(metadata, ensure_ascii=False, indent=2) + "\n"
            self.write(path, text.encode("utf-8"), allocated=not payload.get("path"))
        self.allocation("decision", rid, path)
        return {"ref": {"id": rid, "fragment": event["event_id"]}, "path": str(path), **self.registration("decision",path)}

    def asset_operation(self, payload, select=False):
        ledger_path = self.ref_path(payload["ledger"])
        self.touched.append(ledger_path)
        if ledger_path.exists():
            record = self.checked_record({"path": str(ledger_path)})
            require(record.kind == "asset-ledger", "invalid_scope", "Target is not a native asset ledger")
            doc = self.project.document(ledger_path)
            ledger = copy.deepcopy(record.metadata)
        else:
            require(not select and payload["mode"] == "create", "not_found", "Ledger is missing")
            self.new_destination(ledger_path, "asset-ledger", allow_unmapped=True)
            require(ledger_path.suffix in (".yaml", ".yml", ".json"), "unsupported_format", "Native ledger uses YAML/JSON")
            ledger, doc = {"schema_version": 1, "assets": []}, None
        if not select:
            asset = rebase(payload["asset"], self.project.base, ledger_path.parent, self.project.path)
            if payload["mode"] == "create":
                asset["id"] = self.allocate("asset", asset.get("id"))
                require(not asset["selected_uses"], "invalid_record", "Create assets without selections")
                ledger["assets"].append(asset)
                self.allocation("asset", asset["id"], ledger_path)
            else:
                old = next((a for a in ledger["assets"] if a["id"] == asset["id"]), None)
                require(old is not None, "not_found", "Asset is missing")
                require(old["selected_uses"] == asset["selected_uses"], "invalid_record", "Use asset.select to change selections")
                new_candidates = {c["id"]: c for c in asset["candidates"]}
                for candidate in old["candidates"]:
                    require(candidate["id"] in new_candidates and candidate["version"] == new_candidates[candidate["id"]]["version"]
                            and candidate["manifest"] == new_candidates[candidate["id"]]["manifest"], "invalid_record", "Existing candidate identity/content must be preserved")
                old.update(asset)
                asset = old
            self.project.semantic("asset", asset, ledger_path.parent)
            for candidate in asset["candidates"]:
                self.project.check_candidate(candidate, ledger_path.parent, asset["id"])
        else:
            asset = next((a for a in ledger["assets"] if a["id"] == payload["asset_id"]), None)
            require(asset is not None, "not_found", "Asset is missing")
            self.project.check_refs(payload.get("basis", []), self.project.base)
            if payload["action"] == "set":
                use = rebase(payload["use"], self.project.base, ledger_path.parent, self.project.path)
                candidates = [c for c in asset["candidates"] if c["id"] == use["candidate_id"]]
                require(len(candidates) == 1, "invalid_scope", "Selected candidate is missing")
                self.project.check_candidate(candidates[0], ledger_path.parent, asset["id"])
                position = next((i for i, u in enumerate(asset["selected_uses"]) if u["use_id"] == use["use_id"]), None)
                if position is None:
                    asset["selected_uses"].append(use)
                else:
                    asset["selected_uses"][position] = use
            else:
                require(any(u["use_id"] == payload["use_id"] for u in asset["selected_uses"]), "not_found", "Selected use is missing")
                asset["selected_uses"] = [u for u in asset["selected_uses"] if u["use_id"] != payload["use_id"]]
            self.project.semantic("asset", asset, ledger_path.parent)
        validate("AssetLedger", ledger)
        data = doc.render(metadata=ledger) if doc else (json.dumps(plain(ledger), ensure_ascii=False, indent=2) + "\n").encode() if ledger_path.suffix == ".json" else yaml_dump(ledger).encode("utf-8")
        self.write(ledger_path, data)
        return {"ref": {"id": asset["id"]}, "path": str(ledger_path), "runtime_adoption": "unknown", **self.registration("asset-ledger",ledger_path)}

    def check_replay_authority(self, value):
        # Re-check capability binding before applying a previously prepared plan.
        require(value["request"]["context"] == self.request["context"], "invalid_scope", "Replay context changed")
        for plan in value["plans"]:
            path = self.project.path(plan["path"])
            if self.request["operation"] == "workspace.configure":
                require(path == self.project.workspace, "invalid_scope", "Workspace target changed")
            elif self.request["operation"] == "view.build":
                self.check_view_destination(path)
            else:
                source = self.project.source_for(path)
                new_unmapped = source is None and plan["before"] is None and value["data"].get("source_registration_required")
                require(new_unmapped or source and source.get("format", "").startswith("native-"), "unsupported_write", "Replay source is no longer writable")
        if self.request["operation"] == "decision.record":
            self.authorize_event(self.request["payload"]["event"])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Bound-project v1 JSON I/O; does not run game engines or Git delivery.")
    parser.add_argument("--project-root", required=True, help="Host-authorized absolute project root")
    parser.add_argument("--request", default="-", help="UTF-8 JSON request file, or - for stdin")
    parser.add_argument("--actor-id", default="local-cli", help="Local agent identity; cannot claim user identity")
    args = parser.parse_args(argv)
    try:
        text = sys.stdin.read() if args.request == "-" else Path(args.request).read_text(encoding="utf-8-sig")
        request = json_load(text)
        result = Workflow(args.project_root, actor={"kind": "agent", "id": args.actor_id}).execute(request)
    except (WorkflowError, ValueError, OSError) as exc:
        result = {"status": "rejected", "errors": [{"code": "invalid_request", "message": str(exc)}]}
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if result["status"] == "ok" else 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    raise SystemExit(main())
