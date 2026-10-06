"""Build and stage immutable Gamecaden packages; never edit game records or Codex config."""
from __future__ import annotations

import argparse
import base64
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import zipfile

NAME = "gamecaden"
SKILLS = {"flow", "init", "brainstorm", "design", "develop", "assets", "verify", "close"}
DIRECTORIES = {"skills", "shared", "profiles", "templates", "schemas", "scripts", "examples", "panels", ".codex-plugin"}
ROOT_FILES = {"plugin.json", "INSTALL.md", "THIRD_PARTY_NOTICES.md", "LICENSE"}
MANIFEST = ".gamecaden-package.json"
SEMVER = r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?"
LINK = re.compile(r"!?\[[^\]]*\]\(([^\n)]+)\)")
UNSET = object()


class DistributionError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def require(condition, code, message):
    if not condition:
        raise DistributionError(code, message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def unique(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, "invalid_json", f"Duplicate key: {key}")
        value[key] = item
    return value


def decode(data):
    return json.loads(data.decode("utf-8-sig"), object_pairs_hook=unique)


def safe_path(value):
    path = Path(os.path.abspath(value))
    if os.name == "nt" and not str(path).startswith("\\\\?\\"):
        raw = str(path)
        path = Path("\\\\?\\UNC\\" + raw[2:] if raw.startswith("\\\\") else "\\\\?\\" + raw)
    for part in (path, *path.parents):
        require(not part.is_symlink() and not getattr(part, "is_junction", lambda: False)(),
                "unsafe_path", f"Links/junctions are not supported: {part}")
    return path


def display(path):
    value = str(path)
    if value.startswith("\\\\?\\UNC\\"):
        return "\\\\" + value[8:]
    return value[4:] if value.startswith("\\\\?\\") else value


def separate(a, b):
    require(not a.is_relative_to(b) and not b.is_relative_to(a), "path_overlap", "Source and target must not overlap")


def read_optional(path):
    safe_path(path)
    require(not path.exists() or path.is_file(), "invalid_path", f"Expected file: {path}")
    return path.read_bytes() if path.exists() else None


def atomic(path, data, expected=UNSET):
    safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".gamecaden-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if expected is not UNSET:
            require(read_optional(path) == expected, "recovery_conflict", f"Source changed before replacement: {path}")
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def files(root, source=False):
    result = {}
    def scan(folder):
        for item in sorted(folder.iterdir()):
            safe_path(item)
            rel = item.relative_to(root).as_posix()
            if source and (item.name == "__pycache__" or item.suffix in {".pyc", ".pyo"} or
                           (rel.startswith("scripts/") and item.name.startswith("test_"))):
                continue
            require(item.name not in {"private", "connection.json", ".env", "node_modules", ".git"} and
                    not item.name.startswith(".env.") and item.suffix != ".log", "excluded_resource", f"Non-public resource: {rel}")
            if item.is_dir():
                scan(item)
            else:
                require(item.is_file(), "unsafe_path", f"Unsupported file: {rel}")
                if rel != MANIFEST:
                    data = item.read_bytes()
                    result[rel] = {"sha256": sha(data), "size": len(data)}
    scan(root)
    return result


def package_checks(root):
    portable = decode((root / "plugin.json").read_bytes())
    compat = decode((root / ".codex-plugin/plugin.json").read_bytes())
    require(portable.get("name") == compat.get("name") == NAME and
            portable.get("version") == compat.get("version") and
            isinstance(portable.get("version"), str) and re.fullmatch(SEMVER, portable["version"]),
            "invalid_identity", "Manifest identity/version mismatch")
    require(compat.get("skills") == "./skills/", "invalid_identity", "Skills must use the shared package root")
    actual = {p.name for p in (root / "skills").iterdir() if p.is_dir()}
    require(actual == SKILLS, "invalid_skills", "Expected the eight Gamecaden skills")
    for skill in SKILLS:
        text = (root / "skills" / skill / "SKILL.md").read_text(encoding="utf-8-sig")
        require(text.startswith("---\n") and re.search(rf"(?m)^name: {skill}$", text), "invalid_skills", f"Invalid skill: {skill}")
    for path in root.rglob("*.md"):
        for match in LINK.finditer(path.read_text(encoding="utf-8-sig")):
            target = match[1].strip().strip("<>")
            if ":" in target or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            destination = safe_path(path.parent / target)
            require(destination.is_relative_to(root) and destination.exists(), "broken_link", f"{path.relative_to(root)} -> {target}")
    return portable["version"]


def verify(package):
    root = safe_path(package)
    require(root.is_dir(), "not_found", f"Package is missing: {root}")
    metadata = decode((root / MANIFEST).read_bytes())
    require(metadata.get("format_version") == 1 and metadata.get("name") == NAME, "invalid_manifest", "Unsupported package manifest")
    actual = files(root)
    require(actual == metadata.get("files"), "package_modified", "Package file set or bytes differ from the manifest")
    digest = sha(encode(actual))
    require(digest == metadata.get("digest"), "invalid_manifest", "Package digest differs")
    version = package_checks(root)
    require(version == metadata.get("version"), "invalid_manifest", "Package version differs")
    return {"digest": digest, "version": version, "plugin_root": display(root), "file_count": len(actual)}


def marketplace(entry=None):
    return {"name": "gamecaden-local", "interface": {"displayName": "Gamecaden Local"}, "plugins": [entry] if entry else []}


def plugin_entry(path):
    return {"name": NAME, "source": {"source": "local", "path": path},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"}, "category": "Developer Tools"}


def build(source, output, version=None):
    source, output = safe_path(source), safe_path(output)
    separate(source, output)
    require(source.is_dir() and not output.exists(), "invalid_output", "Source must exist and output must be new")
    require({p.name for p in source.iterdir()} <= DIRECTORIES | ROOT_FILES | {MANIFEST}, "excluded_resource", "Unknown top-level source resources")
    inventory = files(source, source=True)
    require(not version or re.fullmatch(SEMVER, version), "invalid_version", "Expected a semantic version")
    output.mkdir(parents=True)
    package = output / "plugins" / NAME
    package.mkdir(parents=True)
    for rel in inventory:
        target = package / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / rel, target)
    if version:
        for rel in ("plugin.json", ".codex-plugin/plugin.json"):
            data = decode((package / rel).read_bytes())
            data["version"] = version
            atomic(package / rel, encode(data))
    current_version = package_checks(package)
    inventory = files(package)
    digest = sha(encode(inventory))
    atomic(package / MANIFEST, encode({"format_version": 1, "name": NAME, "version": current_version,
                                     "digest": digest, "files": inventory}))
    atomic(output / ".agents/plugins/marketplace.json", encode(marketplace(plugin_entry("./plugins/gamecaden"))))
    archive = output / f"gamecaden-{current_version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as writer:
        for path in sorted(p for p in package.rglob("*") if p.is_file()):
            item = zipfile.ZipInfo("gamecaden/" + path.relative_to(package).as_posix(), (2020, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            writer.writestr(item, path.read_bytes())
    return {**verify(package), "archive": display(archive), "archive_sha256": sha(archive.read_bytes()), "marketplace_name": "gamecaden-local"}


@contextmanager
def locked(root):
    state_dir = safe_path(root / ".gamecaden-install")
    state_dir.mkdir(parents=True, exist_ok=True)
    lock_path = safe_path(state_dir / "lock")
    with lock_path.open("a+b") as stream:
        stream.seek(0, 2)
        if not stream.tell():
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise DistributionError("installation_busy", "Another install operation holds the lock") from exc
        try:
            yield state_dir
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def owned_entry(catalog):
    require(isinstance(catalog, dict) and isinstance(catalog.get("name"), str) and
            isinstance(catalog.get("plugins"), list), "invalid_catalog", "Invalid marketplace catalog")
    entries = [e for e in catalog["plugins"] if isinstance(e, dict) and e.get("name") == NAME]
    require(len(entries) <= 1, "ownership_conflict", "Duplicate Gamecaden entries")
    return entries[0] if entries else None


def load_state(root):
    data = read_optional(root / ".gamecaden-install/state.json")
    if data is None:
        return {"format_version": 1, "name": NAME, "current": None, "history": []}, None
    value = decode(data)
    require(value.get("format_version") == 1 and value.get("name") == NAME and isinstance(value.get("history"), list), "invalid_state", "Invalid installation receipt")
    return value, data


def validate_current(root, state, catalog):
    entry = owned_entry(catalog)
    current = state.get("current")
    if current:
        require(isinstance(current.get("digest"), str) and re.fullmatch(r"[a-f0-9]{64}", current["digest"]), "invalid_state", "Invalid installed digest")
        expected = "./plugins/gamecaden/" + current["digest"]
        require(current.get("source_path") == expected and entry == plugin_entry(expected), "installation_conflict", "Owned marketplace entry changed")
        actual = verify(root / "plugins/gamecaden" / current["digest"])
        require(actual["digest"] == current["digest"] and actual["version"] == current["version"], "installation_conflict", "Installed package changed")
    else:
        require(entry is None, "ownership_conflict", "An unmanaged Gamecaden entry already exists")
    return current


def catalog_data(root):
    raw = read_optional(root / ".agents/plugins/marketplace.json")
    return (decode(raw) if raw is not None else marketplace()), raw


def transaction(root, before_catalog, after_catalog, before_state, after_state):
    journal = root / ".gamecaden-install/transaction.json"
    pack = lambda data: base64.b64encode(data).decode("ascii") if data is not None else None
    atomic(journal, encode({"format_version": 1, "catalog": {"before": pack(before_catalog), "after": pack(after_catalog)},
                           "state": {"before": pack(before_state), "after": pack(after_state)}}))
    recover_locked(root)


def recover_locked(root):
    journal = safe_path(root / ".gamecaden-install/transaction.json")
    if not journal.exists():
        return False
    value = decode(journal.read_bytes())
    require(value.get("format_version") == 1, "invalid_state", "Unsupported transaction")
    changes = []
    for key, rel in (("catalog", ".agents/plugins/marketplace.json"), ("state", ".gamecaden-install/state.json")):
        record = value[key]
        unpack = lambda data: base64.b64decode(data, validate=True) if data is not None else None
        before, after = unpack(record["before"]), unpack(record["after"])
        require(after is not None, "invalid_state", "Transaction requires a resulting document")
        actual = read_optional(root / rel)
        require(actual in (before, after), "recovery_conflict", f"External modification: {rel}")
        changes.append((root / rel, before, after))
    # Validate the intended resulting source before any recovery writes.
    validate_current(root, decode(changes[1][2]), decode(changes[0][2]))
    for path, before, after in changes:
        actual = read_optional(path)
        require(actual in (before, after), "recovery_conflict", f"Source changed during recovery: {path}")
        if actual != after:
            atomic(path, after, expected=actual)
    require(all(read_optional(path) == after for path, _, after in changes), "recovery_conflict", "Recovery readback differs")
    journal.unlink()
    return True


def status(root):
    root = safe_path(root)
    require(not (root / ".gamecaden-install/transaction.json").exists(), "recovery_required", "Use recover before further installation work")
    state, _ = load_state(root)
    catalog, _ = catalog_data(root)
    current = validate_current(root, state, catalog)
    return {"current": current, "history_depth": len(state["history"]), "marketplace_name": catalog["name"], "target_root": display(root)}


def stage(package, target):
    package, root = safe_path(package), safe_path(target)
    separate(package, root)
    candidate = verify(package)
    root.mkdir(parents=True, exist_ok=True)
    with locked(root):
        require(not (root / ".gamecaden-install/transaction.json").exists(), "recovery_required", "Use recover to settle the previous transaction")
        state, state_raw = load_state(root)
        catalog, catalog_raw = catalog_data(root)
        current = validate_current(root, state, catalog)
        store = safe_path(root / "plugins/gamecaden")
        require(state_raw is not None or not store.exists(), "ownership_conflict", "Unmanaged Gamecaden directory exists")
        if store.exists():
            for stored in store.iterdir():
                require(stored.is_dir() and re.fullmatch(r"[a-f0-9]{64}", stored.name), "ownership_conflict", "Unknown resource in the owned package store")
                previous = verify(stored)
                require(previous["digest"] == stored.name, "package_modified", "Stored package identity changed")
                require(previous["version"] != candidate["version"] or previous["digest"] == candidate["digest"],
                        "version_conflict", "This version already identifies different stored content")
        if current and current["digest"] == candidate["digest"]:
            return {**status(root), "unchanged": True}
        require(not current or current["version"] != candidate["version"], "version_conflict", "Different content requires a new version")
        destination = safe_path(store / candidate["digest"])
        if destination.exists():
            require(verify(destination)["digest"] == candidate["digest"], "package_modified", "Stored candidate changed")
        else:
            store.mkdir(parents=True, exist_ok=True)
            temporary = Path(tempfile.mkdtemp(prefix=".stage-", dir=root / ".gamecaden-install"))
            shutil.copytree(package, temporary / "package")
            verify(temporary / "package")
            os.replace(temporary / "package", destination)
            temporary.rmdir()
        source_path = "./plugins/gamecaden/" + candidate["digest"]
        state["history"].append(current)
        state["current"] = {"digest": candidate["digest"], "version": candidate["version"], "source_path": source_path}
        catalog["plugins"] = [e for e in catalog["plugins"] if e.get("name") != NAME] + [plugin_entry(source_path)]
        require(read_optional(root / ".agents/plugins/marketplace.json") == catalog_raw, "installation_conflict", "Catalog changed before transaction")
        transaction(root, catalog_raw, encode(catalog), state_raw, encode(state))
        return {**status(root), "unchanged": False}


def rollback(target):
    root = safe_path(target)
    with locked(root):
        require(not (root / ".gamecaden-install/transaction.json").exists(), "recovery_required", "Use recover before rollback")
        state, state_raw = load_state(root)
        catalog, catalog_raw = catalog_data(root)
        validate_current(root, state, catalog)
        require(state["current"] is not None and state["history"], "no_history", "No prior deployment to restore")
        state["current"] = state["history"].pop()
        catalog["plugins"] = [e for e in catalog["plugins"] if e.get("name") != NAME]
        if state["current"]:
            catalog["plugins"].append(plugin_entry(state["current"]["source_path"]))
        validate_current(root, state, catalog)
        transaction(root, catalog_raw, encode(catalog), state_raw, encode(state))
        return status(root)


def recover(target):
    root = safe_path(target)
    with locked(root):
        changed = recover_locked(root)
        return {**status(root), "recovered": changed}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    cmd = commands.add_parser("build")
    cmd.add_argument("--source", default=str(Path(__file__).resolve().parents[1]))
    cmd.add_argument("--output", required=True)
    cmd.add_argument("--version")
    for name in ("verify", "stage"):
        cmd = commands.add_parser(name)
        cmd.add_argument("--package", required=True)
        if name == "stage":
            cmd.add_argument("--target-root", required=True)
    for name in ("status", "rollback", "recover"):
        commands.add_parser(name).add_argument("--target-root", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            data = build(args.source, args.output, args.version)
        elif args.command == "verify":
            data = verify(args.package)
        elif args.command == "stage":
            data = stage(args.package, args.target_root)
        else:
            data = {"status": status, "rollback": rollback, "recover": recover}[args.command](args.target_root)
        print(json.dumps({"status": "ok", **data}, ensure_ascii=False, indent=2))
        return 0
    except (DistributionError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "rejected", "errors": [{"code": getattr(exc, "code", "invalid_input"), "message": str(exc)}]}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
