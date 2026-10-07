"""Prepare an isolated Gamecaden runtime and dispatch the package's tools."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "scripts/requirements.txt"
TOOLS = {"io": "workflow_io.py", "governance": "workflow_governance.py",
         "panel": "workflow_panel_server.py", "contracts": "check_contracts.py"}
MODULES = {"pyyaml": "yaml", "jsonschema": "jsonschema", "ruamel-yaml": "ruamel.yaml"}
MINIMUM = (3, 12)
sys.dont_write_bytecode = True


class RuntimeErrorInfo(Exception):
    def __init__(self, code, message, **details):
        super().__init__(message)
        self.code, self.details = code, details


def declarations():
    result = []
    for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)((?:[<>=!]+[0-9.]+)(?:,[<>=!]+[0-9.]+)*)", line)
        if not match or re.sub(r"[-_.]+", "-", match[1]).lower() not in MODULES:
            raise RuntimeErrorInfo("invalid_requirements", "Unsupported runtime requirement: " + line)
        for clause in match[2].split(","):
            if not re.fullmatch(r"(>=|<=|==|!=|>|<)\d+(?:\.\d+)*", clause):
                raise RuntimeErrorInfo("invalid_requirements", "Unsupported version constraint: " + clause)
        result.append({"distribution": match[1], "module": MODULES[re.sub(r"[-_.]+", "-", match[1]).lower()],
                       "specifier": match[2]})
    if not result:
        raise RuntimeErrorInfo("invalid_requirements", "Runtime requirements are empty.")
    return result


PROBE = r'''
import importlib, importlib.metadata, json, re, sys
def version(text):
    if not re.fullmatch(r"\d+(?:\.\d+)*", text):
        raise ValueError("A stable numeric version is required")
    return tuple(map(int, text.split('.')))
def satisfies(installed, specifier):
    for clause in specifier.split(','):
        match = re.fullmatch(r"(>=|<=|==|!=|>|<)(\d+(?:\.\d+)*)", clause)
        left, right = version(installed), version(match[2])
        length = max(len(left), len(right))
        left += (0,) * (length-len(left)); right += (0,) * (length-len(right))
        if not {">=":left>=right, "<=":left<=right, "==":left==right,
                "!=":left!=right, ">":left>right, "<":left<right}[match[1]]:
            return False
    return True
rows = []
for entry in json.loads(sys.argv[1]):
    row = dict(entry, installed_version=None, ready=False)
    try:
        row['installed_version'] = importlib.metadata.version(entry['distribution'])
        importlib.import_module(entry['module'])
        row['ready'] = satisfies(row['installed_version'], entry['specifier'])
        if not row['ready']: row['error'] = 'version_mismatch'
    except importlib.metadata.PackageNotFoundError:
        row['error'] = 'dependency_missing'
    except Exception as exc:
        row['error'] = type(exc).__name__ + ': ' + str(exc)
    rows.append(row)
print(json.dumps({'python_version':list(sys.version_info[:3]), 'prefix':sys.prefix,
                 'base_prefix':sys.base_prefix, 'dependencies':rows,
                 'ready':sys.version_info[:2]>=(3,12) and all(row['ready'] for row in rows)}))
'''


def child_env():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1", PYTHONUTF8="1")
    for key in ("PYTHONPATH", "PYTHONHOME"):
        env.pop(key, None)
    return env


def pip_env():
    env = child_env()
    network = {"PIP_INDEX_URL", "PIP_EXTRA_INDEX_URL", "PIP_TRUSTED_HOST", "PIP_PROXY",
               "PIP_CERT", "PIP_CLIENT_CERT", "PIP_TIMEOUT", "PIP_RETRIES", "PIP_NO_INDEX", "PIP_FIND_LINKS"}
    for key in list(env):
        if key.startswith("PIP_") and key not in network:
            env.pop(key)
    env.update(PIP_CONFIG_FILE=os.devnull, PIP_REQUIRE_VIRTUALENV="true")
    return env


def probe(python):
    result = {"python_executable": str(python), "ready": False, "dependencies": []}
    if not Path(python).is_file():
        return dict(result, error="runtime_missing")
    try:
        process = subprocess.run([str(python), "-I", "-B", "-X", "utf8", "-c", PROBE,
                                  json.dumps(declarations())], capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", env=child_env(), stdin=subprocess.DEVNULL, timeout=30)
        if process.returncode:
            return dict(result, error="runtime_probe_failed", exit_code=process.returncode)
        return dict(result, **json.loads(process.stdout))
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        return dict(result, error="runtime_probe_failed", message=str(exc))


def default_home():
    override = os.environ.get("GAMECADEN_RUNTIME_HOME")
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "Gamecaden/runtimes"
    if sys.platform == "darwin":
        return Path.home() / "Library/Caches/Gamecaden/runtimes"
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "Gamecaden/runtimes"


def layout(home=None):
    home = Path(home or default_home()).expanduser().resolve()
    if home == ROOT or home.is_relative_to(ROOT):
        raise RuntimeErrorInfo("invalid_runtime_home", "Choose a runtime directory outside the installed package.")
    digest = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()
    identity = {"requirements_sha256": digest, "implementation": sys.implementation.name,
                "python_version": list(sys.version_info[:2]), "platform": sys.platform, "machine": platform.machine()}
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:24]
    folder = home / key
    python = folder / "env" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return home, folder, python, identity


def atomic_json(path, value):
    descriptor, temporary = tempfile.mkstemp(prefix=".runtime-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def locked(home, key):
    folder = home / ".locks"
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / (key + ".lock")).open("a+b") as stream:
        stream.seek(0, 2)
        if not stream.tell():
            stream.write(b"0"); stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise RuntimeErrorInfo("runtime_busy", "Another process is preparing this runtime; retry after it completes.") from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def setup_step(command, stage):
    print("Gamecaden runtime: " + stage, file=sys.stderr, flush=True)
    try:
        process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                                 errors="replace", env=pip_env(), stdin=subprocess.DEVNULL, timeout=300)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeErrorInfo("runtime_setup_failed", "Runtime preparation timed out; retry setup.", stage=stage) from exc
    if process.returncode:
        diagnostic = (process.stderr or process.stdout)[-3000:]
        diagnostic = re.sub(r"(https?://)[^\s/@]+:[^\s/@]+@", r"\1[redacted]@", diagnostic)
        raise RuntimeErrorInfo("runtime_setup_failed", "Runtime preparation failed; check network, package access and directory permissions.",
                               stage=stage, exit_code=process.returncode, diagnostic=diagnostic)


def check(home=None, python=None):
    if python:
        # POSIX venv executables are symlinks; resolving them selects the base Python.
        result = probe(Path(os.path.abspath(Path(python).expanduser())))
        return dict(result, managed=False)
    _, folder, executable, identity = layout(home)
    owner = folder / "owner.json"
    if folder.exists() and (not owner.is_file() or json.loads(owner.read_text(encoding="utf-8")) != identity):
        result = {"python_executable": str(executable), "ready": False,
                  "dependencies": [], "error": "runtime_ownership_conflict"}
    else:
        result = probe(executable)
        if executable.is_file() and Path(result.get("prefix", "")).resolve() != (folder / "env").resolve():
            result.update(ready=False, error="runtime_not_isolated")
    return dict(result, managed=True, runtime_root=str(folder), requirements_sha256=identity["requirements_sha256"])


def setup(home=None, python=None):
    if python:
        result = check(home, python)
        if not result["ready"]:
            raise RuntimeErrorInfo("external_runtime_not_ready", "The selected Python is not ready. Omit --python to prepare a managed environment.", runtime=result)
        return dict(result, prepared=False)
    home, folder, executable, identity = layout(home)
    with locked(home, folder.name):
        owner = folder / "owner.json"
        if folder.exists():
            if not owner.is_file() or json.loads(owner.read_text(encoding="utf-8")) != identity:
                raise RuntimeErrorInfo("runtime_ownership_conflict", "An unmanaged or incompatible directory occupies this runtime path.")
        else:
            temporary = Path(tempfile.mkdtemp(prefix=".prepare-", dir=home))
            try:
                atomic_json(temporary / "owner.json", identity)
                os.rename(temporary, folder)
            finally:
                if temporary.exists():
                    (temporary / "owner.json").unlink(missing_ok=True)
                    temporary.rmdir()
        result = check(home)
        if result["ready"]:
            return dict(result, prepared=False)
        if not executable.is_file() or result.get("error") == "runtime_not_isolated":
            setup_step([sys.executable, "-I", "-B", "-m", "venv", str(folder / "env")], "create isolated environment")
        isolated = probe(executable)
        if Path(isolated.get("prefix", "")).resolve() != (folder / "env").resolve():
            raise RuntimeErrorInfo("runtime_not_isolated", "The managed Python is not bound to its isolated environment; no packages were installed.")
        pip = subprocess.run([str(executable), "-I", "-B", "-m", "pip", "--version"],
                             capture_output=True, env=pip_env(), stdin=subprocess.DEVNULL, timeout=30)
        if pip.returncode:
            setup_step([str(executable), "-I", "-B", "-m", "ensurepip", "--upgrade"], "restore bundled pip")
        setup_step([str(executable), "-I", "-B", "-m", "pip", "install", "--disable-pip-version-check",
                    "-r", str(REQUIREMENTS)], "install declared dependencies")
        result = check(home)
        if not result["ready"]:
            raise RuntimeErrorInfo("runtime_not_ready", "Installed dependencies did not pass the runtime check.", runtime=result)
        atomic_json(folder / "ready.json", result)
        return dict(result, prepared=True)


def bootstrap_cli(tool):
    """Keep legacy script calls usable; importing the library never installs anything."""
    if sys.version_info[:2] < MINIMUM or not probe(sys.executable)["ready"]:
        if "--help" in sys.argv[1:] or "-h" in sys.argv[1:]:
            print("Use gamecaden_runtime.py setup, then run " + tool + " --help.", file=sys.stderr)
            raise SystemExit(main(["check"]))
        raise SystemExit(main(["run", tool, "--", *sys.argv[1:]]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "setup", "run"):
        command = commands.add_parser(name)
        command.add_argument("--runtime-home", help="Independent cache root; defaults to the user's Gamecaden cache")
        command.add_argument("--python", help="Reuse a ready Python by absolute executable path; never install into it")
        if name == "run":
            command.add_argument("--no-install", action="store_true", help="Check only; reject instead of preparing a missing runtime")
            command.add_argument("tool", choices=TOOLS)
            command.add_argument("tool_args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        if sys.version_info[:2] < MINIMUM:
            raise RuntimeErrorInfo("python_version_unsupported", "Start this entry with Python 3.12 or newer.")
        declarations()
        if args.command == "check":
            result = check(args.runtime_home, args.python)
        elif args.command == "setup":
            result = setup(args.runtime_home, args.python)
        else:
            script = ROOT / "scripts" / TOOLS[args.tool]
            if not script.is_file():
                raise RuntimeErrorInfo("tool_missing", "The installed package is incomplete: " + script.name)
            result = check(args.runtime_home, args.python)
            if not result["ready"]:
                if args.no_install:
                    raise RuntimeErrorInfo("runtime_not_ready", "Prepare the runtime with setup, or select a ready --python.", runtime=result)
                result = setup(args.runtime_home, args.python)
            tool_args = args.tool_args[1:] if args.tool_args[:1] == ["--"] else args.tool_args
            return subprocess.call([result["python_executable"], "-B", "-s", "-X", "utf8", str(script), *tool_args], env=child_env())
        print(json.dumps(dict(result, status="ok" if result["ready"] else "not_ready"), ensure_ascii=False, indent=2))
        return 0 if result["ready"] else 2
    except (RuntimeErrorInfo, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "not_ready", "ready": False, "errors": [{"code": getattr(exc, "code", "runtime_error"),
                          "message": str(exc), **getattr(exc, "details", {})}]}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
