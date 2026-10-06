"""Project-scoped cooperative locking and recoverable file writes.

The journal is operational data, never the source of task/approval state.
"""
from __future__ import annotations

import base64
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
import time

from workflow_formats import WorkflowError, json_load, require, revision


STATE_NAME = ".game-workflow-io"


def file_revision(path):
    physical = filesystem_path(path)
    return revision(physical.read_bytes()) if physical.is_file() else None


def sync_directory(path):
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def filesystem_path(path):
    """Keep logical paths unchanged; use extended Windows names for physical I/O."""
    value = os.path.abspath(path)
    if os.name != "nt" or value.startswith("\\\\?\\"):
        return path
    if value.startswith("\\\\"):
        return Path("\\\\?\\UNC\\" + value[2:])
    return Path("\\\\?\\" + value)


def atomic_write(path, data, expected, guard):
    guard(path)
    physical = filesystem_path(path)
    physical.parent.mkdir(parents=True, exist_ok=True)
    guard(path)
    fd, temp_name = tempfile.mkstemp(prefix=".workflow-", suffix=".tmp", dir=physical.parent)
    temp = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if physical.exists():
            os.chmod(temp, stat.S_IMODE(physical.stat().st_mode))
        guard(path)
        require(file_revision(path) == expected, "revision_conflict", "Source changed before replacement", {"path": str(path)})
        os.replace(temp, physical)
        sync_directory(path.parent)
        require(physical.read_bytes() == data, "indeterminate", "Written content failed readback", {"path": str(path)})
    finally:
        if temp.exists():
            temp.unlink()


class Store:
    def __init__(self, root, guard, fault=None):
        self.root, self.guard, self.fault = root, guard, fault
        self.state = root / STATE_NAME
        self.scope = "local:" + hashlib.sha256(os.path.normcase(str(root)).encode("utf-8")).hexdigest()

    def safe_state(self, path):
        path = Path(path)
        require(path.is_relative_to(self.state), "invalid_scope", "Not an operational path")
        current = self.root
        for part in path.relative_to(self.root).parts:
            current /= part
            physical = filesystem_path(current)
            require(not physical.is_symlink() and not physical.is_junction(), "invalid_scope", "Linked operational path")
        return path

    @contextmanager
    def lock(self, write=False):
        lock_path = filesystem_path(self.safe_state(self.state / "lock"))
        if write:
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            # Concurrent initial creators use append, never truncate the lock inode.
            with lock_path.open("ab") as handle:
                if handle.tell() == 0:
                    handle.write(b"0")
                    handle.flush()
        if not lock_path.exists():
            yield
            require(not lock_path.exists(), "operation_pending", "A writer started during this read; retry")
            return
        # ponytail: one project lock; split only after measured contention, retaining namespace safety.
        with lock_path.open("rb") as handle:
            deadline = time.monotonic() + 10
            while True:
                try:
                    if os.name == "nt":
                        import msvcrt
                        handle.seek(0)
                        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError as exc:
                    if time.monotonic() >= deadline:
                        raise WorkflowError("operation_pending", "Project I/O lock is busy") from exc
                    time.sleep(0.025)
            try:
                yield
            finally:
                if os.name == "nt":
                    import msvcrt
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def path(self, request_id):
        key = hashlib.sha256(request_id.encode("utf-8")).hexdigest()
        return self.safe_state(self.state / "operations" / f"{key}.json")

    def load(self, request_id):
        path = filesystem_path(self.path(request_id))
        if not path.exists():
            return None
        try:
            value = json_load(path.read_text(encoding="utf-8"))
            require(value["receipt"]["scope_id"] == self.scope, "invalid_scope", "Receipt belongs to another project root")
            require(value["receipt"]["request_id"] == request_id, "indeterminate", "Receipt identity mismatch")
            return value
        except (ValueError, KeyError, TypeError) as exc:
            raise WorkflowError("indeterminate", "Unreadable operation receipt; preserve it for inspection") from exc

    def all(self):
        folder = self.safe_state(self.state / "operations")
        physical_folder = filesystem_path(folder)
        if not physical_folder.exists():
            return []
        result = []
        for physical in physical_folder.glob("*.json"):
            path = self.safe_state(folder / physical.name)
            try:
                data = json_load(physical.read_text(encoding="utf-8"))
                require(data["receipt"]["scope_id"] == self.scope, "invalid_scope", "Foreign receipt scope")
                result.append(data)
            except (ValueError, KeyError, TypeError) as exc:
                raise WorkflowError("indeterminate", f"Invalid operational receipt: {path.name}") from exc
        return result

    def save(self, value):
        path = self.path(value["receipt"]["request_id"])
        data = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
        atomic_write(path, data, file_revision(path), self.safe_state)

    def pending(self, except_id=None):
        return [value for value in self.all() if value["receipt"]["phase"] != "settled"
                and value["receipt"]["request_id"] != except_id]

    def prepare(self, request, digest, plans, allocations, guards, data):
        value = {"receipt": {"request_id": request["request_id"], "operation": request["operation"],
                             "scope_id": self.scope, "request_digest": digest, "phase": "prepared",
                             "outcome": None, "allocations": allocations, "recovery_actions": []},
                 "request": request, "guards": guards, "plans": plans, "data": data,
                 "errors": [], "writes": []}
        for plan in plans:
            value["writes"].append({"target": {"path": plan["path"]}, "status": "not_attempted",
                                    "before_revision": plan["before"]})
        self.save(value)
        return value

    def checkpoint(self, stage, value):
        if self.fault:
            self.fault(stage, value)

    def reconcile(self, value):
        """Observe a crash window without changing source files or the receipt."""
        import copy
        value = copy.deepcopy(value)
        for plan, result in zip(value["plans"], value["writes"]):
            try:
                path = self.guard(Path(plan["path"]))
                current = file_revision(path)
            except (WorkflowError, OSError) as exc:
                result.update(status="failed", error=f"Unable to observe current target: {exc}")
                continue
            if current == plan["after"]:
                known_write = result["status"] == "written" and plan["before"] != plan["after"]
                result.update(status="written" if known_write else "unchanged", after_revision=current)
                if not known_write and plan["before"] != plan["after"]:
                    result["note"] = "Expected bytes observed; this receipt does not prove who wrote them."
            elif current != plan["before"] or result["status"] == "written":
                result.update(status="failed", error="revision_conflict", note="Current target differs from the recorded/expected result.")
        if value["receipt"]["phase"] != "settled":
            done = any(w["status"] in ("written", "unchanged") for w in value["writes"])
            value["receipt"]["outcome"] = "partial" if done else "indeterminate"
            action = "finish_extract" if value["receipt"]["operation"] == "record.extract" else "retry_same_request"
            if any(w["status"] == "failed" for w in value["writes"]):
                action = "resolve_conflict"
            value["receipt"]["recovery_actions"] = [{"action": action,
                "targets": [w["target"] for w in value["writes"]],
                "reason": "Read current files and retry the original request only while its conditions remain valid."}]
        return value

    def apply(self, value):
        target_paths = {plan["path"] for plan in value["plans"]}
        try:
            self.checkpoint("prepared", value)
            value["receipt"]["phase"] = "applying"
            self.save(value)
            for index, (plan, result) in enumerate(zip(value["plans"], value["writes"])):
                for name, expected in value["guards"].items():
                    if name not in target_paths:
                        require(file_revision(self.guard(Path(name))) == expected, "revision_conflict",
                                "Referenced source changed during the operation", {"path": name})
                path = self.guard(Path(plan["path"]))
                current = file_revision(path)
                if current == plan["after"]:
                    known_write = result["status"] == "written" and plan["before"] != plan["after"]
                    result.update(status="written" if known_write else "unchanged", after_revision=current)
                    if not known_write and plan["before"] != plan["after"]:
                        result["note"] = "Expected bytes already present; no new replacement was performed."
                else:
                    require(result["status"] != "written", "revision_conflict", "A previously written result was changed/reverted; preserved it", {"path": str(path)})
                    require(current == plan["before"], "revision_conflict", "Source changed; preserved current file", {"path": str(path)})
                    self.checkpoint(f"before_write:{index}", value)
                    atomic_write(path, base64.b64decode(plan["content"]), plan["before"], self.guard)
                    self.checkpoint(f"after_replace:{index}", value)
                    result.update(status="written", after_revision=plan["after"])
                self.save(value)
                self.checkpoint(f"after_write:{index}", value)
            # A late external edit must not be reported as successful final readback.
            for plan in value["plans"]:
                require(file_revision(self.guard(Path(plan["path"]))) == plan["after"], "indeterminate",
                        "Source changed before final readback", {"path": plan["path"]})
            value["receipt"].update(phase="settled", outcome="ok", recovery_actions=[])
            value["errors"] = []
            self.save(value)
        except (WorkflowError, OSError) as exc:
            if value["receipt"]["phase"] == "settled":
                value["receipt"]["phase"] = "applying"  # Final receipt persistence was not confirmed.
            value = self.reconcile(value)
            error = exc if isinstance(exc, WorkflowError) else WorkflowError("write_failed", str(exc))
            value["errors"] = [error.item()]
            written = any(w["status"] in ("written", "unchanged") and p["after"] != p["before"]
                          for p, w in zip(value["plans"], value["writes"]))
            status = "partial" if written else ("conflict" if error.code == "revision_conflict" else "indeterminate")
            value["receipt"]["outcome"] = status
            if error.code == "revision_conflict":
                value["receipt"]["phase"] = "settled"
                value["receipt"]["recovery_actions"] = [{"action": "resolve_conflict",
                    "targets": [w["target"] for w in value["writes"]],
                    "reason": "Preserved the external edit. Read current revisions and submit a new request; extraction can cite recovery_of."}]
            try:
                self.save(value)
            except (WorkflowError, OSError) as persist_error:
                value["errors"].append({"code": "indeterminate", "message": f"Recovery receipt persistence not confirmed: {persist_error}"})
                value["receipt"]["phase"] = "applying"
        return value


def plan_write(path, before, data):
    return {"path": str(path), "before": before, "after": revision(data),
            "content": base64.b64encode(data).decode("ascii")}
