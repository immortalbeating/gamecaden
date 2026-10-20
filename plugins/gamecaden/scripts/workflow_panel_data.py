"""Read-only, host-bound data adapter for the local workflow panel."""
from __future__ import annotations

import base64
import copy
import hashlib
import json
from pathlib import Path
import uuid

from workflow_formats import WorkflowError, canonical, json_load, revision
from workflow_io import Workflow
from workflow_project import Project
from workflow_storage import Store


MEDIA_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif", ".wav": "audio/wav",
    ".mp3": "audio/mpeg", ".ogg": "audio/ogg", ".mp4": "video/mp4",
    ".webm": "video/webm",
}
MAX_MEDIA = 32 * 1024 * 1024
MAX_RECORDS = 50000
MAX_SNAPSHOT_BYTES = 64 * 1024 * 1024


class PanelDataError(Exception):
    def __init__(self, code, message, status=400, details=None):
        super().__init__(message)
        self.code, self.message, self.status, self.details = code, message, status, details


class PanelData:
    def __init__(self, root, *, workspace=None, external_sources=None, name=None, project_id=None):
        self.root = Path(root).resolve(strict=True)
        if not self.root.is_dir():
            raise PanelDataError("invalid_scope", "Project root must be a directory")
        self.workspace = workspace
        self.name, self.project_id = name, project_id
        self.external_sources = list(external_sources or [])
        ids = set()
        for source in self.external_sources:
            if not isinstance(source, dict) or not all(isinstance(source.get(k), str) and source[k] for k in ("id", "label", "role", "path")):
                raise PanelDataError("invalid_source", "External source needs id, label, role and path")
            if source["id"] in ids:
                raise PanelDataError("invalid_source", "Duplicate external source id")
            ids.add(source["id"])
            if Path(source["path"]).is_absolute():
                raise PanelDataError("invalid_scope", "External source path must be project-relative")
        self.workflow = Workflow(self.root)
        self._records = {}
        self._media = {}
        self._snapshot_model = None
        self._snapshot_guard = None

    def _context(self):
        value = {"project_root": str(self.root), "base_dir": str(self.root)}
        if self.workspace is not None:
            value["workspace"] = str(self.workspace)
        return value

    def _call(self, operation, payload):
        response = self.workflow.execute({"protocol_version": 1, "request_id": uuid.uuid4().hex,
                                          "operation": operation, "context": self._context(), "payload": payload})
        if response["status"] != "ok":
            error = (response.get("errors") or [{"code": "workflow_error", "message": "Workflow read failed"}])[0]
            code = error.get("code", "workflow_error")
            raise PanelDataError(code, error.get("message", "Workflow read failed"),
                                 404 if code == "not_found" else 409 if code in ("stale_cursor", "revision_conflict", "version_mismatch") else 400,
                                 error.get("target"))
        return response["data"]

    def _project(self):
        try:
            return Project(self.root, self._context())
        except WorkflowError as exc:
            raise PanelDataError(exc.code, str(exc)) from exc

    def _as_raw(self, data, guard=None):
        guard = guard or self._project()
        path = guard.path(data["path"])
        content = guard.read_bytes(path)
        if revision(content) != data["revision"]:
            raise PanelDataError("revision_conflict", "Original source changed while reading", 409)
        try:
            body = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            body = None
        data.update(ref={"path": str(path)}, reference_base=None, body=body,
                    interpretation="raw", capabilities=["record.read"], metadata=None)
        return data

    @staticmethod
    def _key(source, path, ref):
        material = json.dumps([source, path, ref], sort_keys=True, ensure_ascii=False).encode()
        return hashlib.sha256(material).hexdigest()

    def _row(self, data, record_type, source="native", extra=None):
        key = self._key(source, data["path"], data["ref"])
        metadata = data.get("metadata") or {}
        title = next((value for value in (metadata.get("title"), metadata.get("name"), (extra or {}).get("label"))
                      if isinstance(value, str) and value), Path(data["path"]).name)
        row = {"key": key, "record_type": record_type,
               "title": title,
               "ref": data["ref"], "path": data["path"], "reference_base": data.get("reference_base"),
               "revision": data["revision"], "metadata": data.get("metadata"),
               "capabilities": data.get("capabilities", ["record.read"]),
               "interpretation": data.get("interpretation", "raw"),
               "diagnostics": data.get("diagnostics", [])}
        if extra:
            row.update(extra)
        self._records[key] = (row, data["ref"])
        return row

    def revisions(self):
        from workflow_panel_revisions import source_revisions
        return source_revisions(self)

    def _pending_signature(self, guard):
        return revision(canonical(Store(self.root, guard.path).pending()).encode("utf-8"))

    def _check_model(self, model):
        model["guard"].check_snapshot()
        for path in model.get("unread", ()):
            try:
                model["guard"].read_bytes(Path(path))
            except (WorkflowError, OSError):
                continue  # Keep the explicit failed-source diagnostic while it persists.
            raise WorkflowError("revision_conflict", "A previously unreadable source is now available", {"path": path})
        if self._pending_signature(model["guard"]) != model["pending"]:
            raise WorkflowError("revision_conflict", "Operational state changed while reading")

    def _project_info(self, guard):
        identity = (guard.mapping or {}).get("project") or {}
        return {"id": self.project_id or identity.get("id") or self.root.name,
                "name": self.name or identity.get("name") or self.root.name,
                "root": str(self.root), "workspace": str(guard.workspace),
                "configured": guard.mapping is not None,
                "kind": "external" if self.external_sources else "native"}

    def _build_snapshot(self):
        guard = self._project()
        pending = self._pending_signature(guard)
        records = guard.scan(retain_payloads=False)
        if len(records) > MAX_RECORDS:
            raise PanelDataError("too_many_records", "Sources exceed the record limit for this request", 413)
        rows = [self._row(guard.read_record(record, False), record.kind)
                for record in sorted(records, key=lambda record: (str(record.path), record.id or ""))]
        diagnostics = copy.deepcopy(guard.diagnostics)
        if Store(self.root, guard.path).pending():
            diagnostics.append({"code": "operation_pending", "message": "Some records have unfinished operations"})
        data = {"project": self._project_info(guard), "records": rows, "next_cursor": None,
                "complete": guard.scan_complete, "diagnostics": diagnostics,
                "source_revisions": [{"ref": {"path": path}, "revision": value}
                                     for path, value in sorted(guard.observed.items())]}
        encoded = canonical(data).encode("utf-8")
        if len(encoded) > MAX_SNAPSHOT_BYTES:
            raise PanelDataError("output_too_large", "Source metadata exceeds the snapshot output limit", 413)
        unread = [path for source in guard.inventory if not source.get("error")
                  for path in source["files"] if path not in guard.observed]
        model = {"guard": guard, "pending": pending, "data": data, "digest": revision(encoded), "unread": unread}
        self._check_model(model)
        self._records = {row["key"]: self._records[row["key"]] for row in rows}
        return model

    def _model(self, cursor=None):
        model = self._snapshot_model
        if model is not None:
            try:
                self._check_model(model)
            except (WorkflowError, OSError) as exc:
                self._snapshot_model = None
                if cursor:
                    raise PanelDataError("stale_cursor", "Sources or operational state changed; start a new listing", 409) from exc
                model = None
        if model is None:
            if cursor:
                raise PanelDataError("stale_cursor", "Snapshot is no longer retained; start a new listing", 409)
            model = self._build_snapshot()
            self._snapshot_model = model
        self._snapshot_guard = model["guard"]
        return model

    def check_snapshot(self):
        """Recheck both source bytes/membership and operational diagnostics."""
        try:
            if self._snapshot_model is not None:
                self._check_model(self._snapshot_model)
            elif self._snapshot_guard is not None:
                self._snapshot_guard.check_snapshot()
        except (WorkflowError, OSError) as exc:
            raise PanelDataError(getattr(exc, "code", "read_failed"), str(exc), 409) from exc

    def _external_snapshot(self, cursor=None):
        guard = self._project()
        project = self._project_info(guard)
        if self.external_sources:
            if cursor:
                raise PanelDataError("stale_cursor", "External sources do not use a cursor", 409)
            rows, diagnostics, revisions = [], [], []
            for source in self.external_sources:
                try:
                    path = guard.path(source["path"], self.root)
                    raw = self._call("record.read", {"target": {"path": str(path)}})
                    self._as_raw(raw, guard)
                    rows.append(self._row(raw, "external", source["id"],
                                          {"source_id": source["id"], "role": source["role"], "label": source["label"]}))
                    revisions.append({"ref": {"path": str(path)}, "revision": raw["revision"]})
                except (PanelDataError, WorkflowError) as exc:
                    diagnostics.append({"code": exc.code, "message": str(exc), "source_id": source["id"]})
            try:
                guard.check_snapshot()
            except (WorkflowError, OSError) as exc:
                raise PanelDataError(getattr(exc, "code", "read_failed"), str(exc), 409) from exc
            self._snapshot_guard = guard
            return {"project": project, "records": rows, "next_cursor": None,
                    "complete": not diagnostics, "diagnostics": diagnostics,
                    "source_revisions": revisions}

    def snapshot_all(self):
        """Return one complete, process-local source model for derived consumers."""
        if self.external_sources:
            return self._external_snapshot()
        try:
            model = self._model()
            data = copy.deepcopy(model["data"])
            self._check_model(model)
            return data
        except (WorkflowError, OSError) as exc:
            raise PanelDataError(getattr(exc, "code", "read_failed"), str(exc), 409) from exc

    def snapshot(self, cursor=None, limit=100):
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 1000:
            raise PanelDataError("invalid_request", "limit must be between 1 and 1000")
        if self.external_sources:
            return self._external_snapshot(cursor)
        try:
            model = self._model(cursor)
            fingerprint = revision(canonical([model["digest"], limit]).encode("utf-8"))
            offset = 0
            if cursor:
                try:
                    value = json_load(base64.urlsafe_b64decode(cursor).decode("utf-8"))
                    if (value["snapshot"] != fingerprint or type(value["offset"]) is not int or value["offset"] < 0):
                        raise ValueError("Cursor does not match this source model")
                    offset = value["offset"]
                except (ValueError, KeyError, TypeError, UnicodeError) as exc:
                    raise PanelDataError("stale_cursor", "Invalid or changed listing cursor", 409) from exc
            data = model["data"]
            page = {key: copy.deepcopy(value) for key, value in data.items()
                    if key not in ("records", "diagnostics", "source_revisions", "next_cursor")}
            for key in ("records", "diagnostics", "source_revisions"):
                page[key] = copy.deepcopy(data[key][offset:offset + limit])
            next_offset = offset + limit
            page["next_cursor"] = (base64.urlsafe_b64encode(canonical({"snapshot": fingerprint, "offset": next_offset}).encode()).decode()
                                   if next_offset < max(len(data[key]) for key in ("records", "diagnostics", "source_revisions")) else None)
            self._check_model(model)
            return page
        except (WorkflowError, OSError) as exc:
            raise PanelDataError(getattr(exc, "code", "read_failed"), str(exc), 409) from exc

    def read(self, key):
        try:
            row, ref = self._records[key]
        except (KeyError, TypeError):
            raise PanelDataError("not_found", "Unknown record key", 404) from None
        target = {name: value for name, value in ref.items() if name not in ("id", "path")}
        target["path"] = row["path"]
        if "id" in ref:
            target["fragment"] = ref["id"]
        data = self._call("record.read", {"target": target})
        if data["path"] != row["path"] or "id" in ref and data["ref"].get("id") != ref["id"]:
            raise PanelDataError("revision_conflict", "Record reference moved", 409)
        if row["record_type"] == "external":
            self._as_raw(data)
        return {**self._row(data, row["record_type"], row.get("source_id", "native"),
                            {k: row[k] for k in ("source_id", "role", "label") if k in row}),
                "body": data.get("body")}

    def candidate(self, key, candidate_id):
        record = self.read(key)
        if record["record_type"] != "asset" or record["interpretation"] != "native":
            raise PanelDataError("invalid_scope", "Candidate requires a native asset record")
        metadata = record["metadata"]
        matches = [c for c in metadata["candidates"] if c["id"] == candidate_id]
        if len(matches) != 1:
            raise PanelDataError("not_found", "Candidate not found", 404)
        candidate = matches[0]
        project = self._project()
        base = Path(record["reference_base"])
        check = {"status": "verified", "errors": []}
        manifest_path = None
        try:
            manifest_path = project.resolve(candidate["manifest"], base).path
            project.check_candidate(candidate, base, metadata["id"])
        except WorkflowError as exc:
            check = {"status": "unsupported" if exc.code == "unsupported_format" else "invalid",
                     "errors": [exc.item()]}
        media = []
        if check["status"] == "verified":
            manifest_bytes = project.path(manifest_path).read_bytes()
            if revision(manifest_bytes)[7:] != candidate["version"]["value"]:
                raise PanelDataError("revision_conflict", "Manifest changed after candidate verification", 409)
            manifest = json_load(manifest_bytes.decode("utf-8-sig"))
            pending_media = {}
            for file in manifest["files"]:
                path = project.path(file["path"], manifest_path.parent)
                mime = MEDIA_TYPES.get(path.suffix.lower())
                if mime and path.stat().st_size <= MAX_MEDIA:
                    file_revision = revision(path.read_bytes())
                    if file_revision[7:] != file["sha256"]:
                        check = {"status": "invalid", "errors": [{"code": "version_mismatch", "message": "Manifest member changed while registering media"}]}
                        media = []
                        break
                    media_key = self._key("media", str(path), file_revision)
                    pending_media[media_key] = (str(path), file_revision, mime, path.name)
                    media.append({"key": media_key, "mime": mime, "role": file["role"], "name": path.name,
                                  "revision": file_revision, "size": path.stat().st_size})
            if check["status"] == "verified":
                self._media.update(pending_media)
        uses = metadata["selected_uses"]
        return {"asset_id": metadata["id"], "asset_ref": record["ref"], "ledger_path": record["path"],
                "ledger_revision": record["revision"], "reference_base": record["reference_base"],
                "candidate_id": candidate_id, "version": candidate["version"],
                "manifest_path": str(manifest_path) if manifest_path else None,
                "selected_uses": [u for u in uses if u["candidate_id"] == candidate_id],
                "all_uses": uses, "check": check, "media": media}

    def media(self, media_key):
        try:
            raw_path, expected, mime, name = self._media[media_key]
        except (KeyError, TypeError):
            raise PanelDataError("not_found", "Unknown media key", 404) from None
        try:
            path = self._project().path(raw_path)
            if path.stat().st_size > MAX_MEDIA:
                raise PanelDataError("media_too_large", "Media exceeds 32 MiB", 413)
            data = path.read_bytes()
        except WorkflowError as exc:
            raise PanelDataError(exc.code, str(exc)) from exc
        except FileNotFoundError:
            raise PanelDataError("not_found", "Media file missing", 404) from None
        if revision(data) != expected:
            raise PanelDataError("revision_conflict", "Media bytes changed", 409)
        return {"data": data, "mime": mime, "revision": expected, "name": name}
