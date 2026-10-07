"""First-use runtime boundaries; no network or global package installation."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
BUNDLE = REPO / "plugins/gamecaden"
CLI = BUNDLE / "scripts/gamecaden_runtime.py"
spec = importlib.util.spec_from_file_location("runtime_entry", CLI)
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file()}


class RuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        work = REPO / "work/runtime-tests"
        work.mkdir(parents=True, exist_ok=True)
        cls.suite = Path(tempfile.mkdtemp(prefix="suite-", dir=work))
        cls.empty = cls.suite / "empty-python"
        subprocess.run([sys.executable, "-I", "-B", "-m", "venv", "--without-pip", str(cls.empty)],
                       check=True, capture_output=True, env=runtime.child_env())
        cls.empty_python = cls.empty / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

    def setUp(self):
        self.case = Path(tempfile.mkdtemp(prefix="case-", dir=self.suite))
        self.home = self.case / "cache"

    def command(self, *args, python=None, input=None, env=None):
        process = subprocess.run([str(python or sys.executable), "-B", "-X", "utf8", str(CLI), *map(str, args)],
                                 input=input, capture_output=True, text=True, encoding="utf-8",
                                 env=env or runtime.child_env())
        return process, json.loads(process.stdout)

    def direct(self, args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = runtime.main(args)
        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_check_does_not_prepare_or_create_cache(self):
        process, result = self.command("check", "--runtime-home", self.home, python=self.empty_python)
        self.assertEqual(process.returncode, 2)
        self.assertFalse(result["ready"])
        self.assertEqual(result["error"], "runtime_missing")
        self.assertFalse(self.home.exists())
        self.assertNotIn("Traceback", process.stderr)

    def test_empty_interpreter_reports_all_missing_requirements_without_mutation(self):
        before = snapshot(self.empty)
        process, result = self.command("check", "--python", self.empty_python, python=self.empty_python)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(len(result["dependencies"]), 3)
        self.assertTrue(all(row["error"] == "dependency_missing" for row in result["dependencies"]))
        self.assertEqual(Path(result["prefix"]).resolve(), self.empty.resolve())
        self.assertFalse(result["managed"])
        self.assertEqual(snapshot(self.empty), before)

    def test_external_python_is_never_automatically_installed_into(self):
        before = snapshot(self.empty)
        process, result = self.command("run", "--python", self.empty_python, "io", "--project-root", self.case,
                                       python=self.empty_python)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(result["errors"][0]["code"], "external_runtime_not_ready")
        self.assertEqual(snapshot(self.empty), before)
        self.assertNotIn("install declared", process.stderr)

    def test_no_install_stops_before_business_writes(self):
        project = self.case / "game"
        shutil.copytree(BUNDLE / "examples/v1/project", project)
        before = snapshot(project)
        request = {"protocol_version": 1, "request_id": "must-not-create", "operation": "record.create",
                   "context": {"project_root": str(project)}, "preconditions": [],
                   "payload": {"record_type": "task", "metadata": {"title": "Never written", "mode": "quick",
                               "kind": "bug", "status": "active", "epic": None}, "body": "Must not write."}}
        process, result = self.command("run", "--runtime-home", self.home, "--no-install", "io",
                                       "--project-root", project, "--request", "-", input=json.dumps(request),
                                       python=self.empty_python)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(result["errors"][0]["code"], "runtime_not_ready")
        self.assertEqual(snapshot(project), before)
        self.assertFalse(self.home.exists())

    def test_setup_failure_prevents_tool_dispatch_and_can_be_retried(self):
        failure = runtime.RuntimeErrorInfo("runtime_setup_failed", "Offline fixture", stage="install dependencies")
        with patch.object(runtime, "setup_step", side_effect=failure), patch.object(runtime.subprocess, "call") as tool:
            code, result, _ = self.direct(["run", "--runtime-home", str(self.home), "io", "--project-root", str(self.case)])
            self.assertEqual(code, 2)
            self.assertEqual(result["errors"][0]["code"], "runtime_setup_failed")
            tool.assert_not_called()
        _, folder, _, identity = runtime.layout(self.home)
        self.assertEqual(json.loads((folder / "owner.json").read_text(encoding="utf-8")), identity)
        # An interrupted preparation retains ownership and can reach setup again.
        with patch.object(runtime, "setup_step", side_effect=failure) as retry:
            code, result, _ = self.direct(["setup", "--runtime-home", str(self.home)])
            self.assertEqual(code, 2)
            retry.assert_called_once()
            self.assertEqual(result["errors"][0]["code"], "runtime_setup_failed")

    def test_unmanaged_directory_is_preserved_and_never_executed(self):
        _, folder, executable, _ = runtime.layout(self.home)
        executable.parent.mkdir(parents=True)
        executable.write_bytes(b"Unmanaged executable fixture")
        before = snapshot(folder)
        with patch.object(runtime, "probe") as probe:
            result = runtime.check(self.home)
            self.assertEqual(result["error"], "runtime_ownership_conflict")
            probe.assert_not_called()
        with self.assertRaises(runtime.RuntimeErrorInfo) as caught:
            runtime.setup(self.home)
        self.assertEqual(caught.exception.code, "runtime_ownership_conflict")
        self.assertEqual(snapshot(folder), before)

    def test_interrupted_venv_with_python_but_no_pip_is_repaired_offline(self):
        _, folder, executable, identity = runtime.layout(self.home)
        folder.mkdir(parents=True)
        runtime.atomic_json(folder / "owner.json", identity)
        subprocess.run([sys.executable, "-I", "-B", "-m", "venv", "--without-pip", str(folder / "env")],
                       check=True, capture_output=True, env=runtime.child_env())
        self.assertTrue(executable.is_file())
        stages = []
        original_step = runtime.setup_step
        def stop_before_download(command, stage):
            stages.append(stage)
            if stage == "install declared dependencies":
                raise runtime.RuntimeErrorInfo("runtime_setup_failed", "Network deliberately unused by this test")
            original_step(command, stage)
        with patch.object(runtime, "setup_step", side_effect=stop_before_download):
            with self.assertRaises(runtime.RuntimeErrorInfo):
                runtime.setup(self.home)
        self.assertIn("restore bundled pip", stages)
        self.assertNotIn("create isolated environment", stages)
        check = subprocess.run([str(executable), "-I", "-B", "-m", "pip", "--version"],
                               capture_output=True, env=runtime.child_env())
        self.assertEqual(check.returncode, 0)

    def test_missing_venv_configuration_is_repaired_before_any_dependency_install(self):
        _, folder, executable, identity = runtime.layout(self.home)
        folder.mkdir(parents=True)
        runtime.atomic_json(folder / "owner.json", identity)
        subprocess.run([sys.executable, "-I", "-B", "-m", "venv", "--without-pip", str(folder / "env")],
                       check=True, capture_output=True, env=runtime.child_env())
        (folder / "env/pyvenv.cfg").unlink()
        self.assertTrue(executable.is_file())
        self.assertEqual(runtime.check(self.home)["error"], "runtime_not_isolated")
        original_step = runtime.setup_step
        def stop_before_download(command, stage):
            if stage == "install declared dependencies":
                info = runtime.probe(executable)
                self.assertEqual(Path(info["prefix"]).resolve(), (folder / "env").resolve())
                raise runtime.RuntimeErrorInfo("runtime_setup_failed", "Stop after verified isolation")
            original_step(command, stage)
        with patch.object(runtime, "setup_step", side_effect=stop_before_download):
            with self.assertRaises(runtime.RuntimeErrorInfo):
                runtime.setup(self.home)
        self.assertTrue((folder / "env/pyvenv.cfg").is_file())
        self.assertEqual(Path(runtime.probe(executable)["prefix"]).resolve(), (folder / "env").resolve())

    def test_requirements_changes_select_a_different_environment(self):
        original = runtime.layout(self.home)
        requirements = self.case / "requirements.txt"
        requirements.write_bytes(runtime.REQUIREMENTS.read_bytes() + b"\n# revised dependency identity\n")
        with patch.object(runtime, "REQUIREMENTS", requirements):
            updated = runtime.layout(self.home)
        self.assertNotEqual(original[1], updated[1])
        self.assertNotEqual(original[3]["requirements_sha256"], updated[3]["requirements_sha256"])
        self.assertFalse(self.home.exists())

    def test_interruption_before_owner_publication_leaves_no_unrecoverable_runtime(self):
        _, folder, _, _ = runtime.layout(self.home)
        with patch.object(runtime, "atomic_json", side_effect=OSError("Interrupted owner publication")):
            with self.assertRaises(OSError):
                runtime.setup(self.home)
        self.assertFalse(folder.exists())
        failure = runtime.RuntimeErrorInfo("runtime_setup_failed", "Offline retry fixture")
        with patch.object(runtime, "setup_step", side_effect=failure) as prepare:
            with self.assertRaises(runtime.RuntimeErrorInfo) as caught:
                runtime.setup(self.home)
        self.assertEqual(caught.exception.code, "runtime_setup_failed")
        prepare.assert_called_once()
        self.assertTrue((folder / "owner.json").is_file())

    def test_pip_target_overrides_are_removed_from_real_setup_subprocess(self):
        inherited = {"PIP_TARGET": str(self.case / "wrong-target"), "PIP_PREFIX": str(self.case / "wrong-prefix"),
                     "PIP_USER": "true", "PIP_ROOT": str(self.case / "wrong-root"), "PIP_PYTHON": "wrong-python",
                     "PIP_CONFIG_FILE": str(self.case / "wrong-config"), "PIP_INDEX_URL": "https://example.invalid/simple"}
        completed = subprocess.CompletedProcess([], 0, "", "")
        with patch.dict(os.environ, inherited), patch.object(runtime.subprocess, "run", return_value=completed) as call:
            runtime.setup_step(["fixture"], "install")
        actual = call.call_args.kwargs["env"]
        for name in ("PIP_TARGET", "PIP_PREFIX", "PIP_USER", "PIP_ROOT", "PIP_PYTHON"):
            self.assertNotIn(name, actual)
        self.assertEqual(actual["PIP_CONFIG_FILE"], os.devnull)
        self.assertEqual(actual["PIP_REQUIRE_VIRTUALENV"], "true")
        self.assertEqual(actual["PIP_INDEX_URL"], inherited["PIP_INDEX_URL"])

    def test_pip_configuration_target_is_ignored_without_installing_anything(self):
        config = self.case / "pip.ini"
        config.write_text("[global]\ntarget = " + str(self.case / "wrong-target") + "\n", encoding="utf-8")
        with patch.dict(os.environ, {"PIP_CONFIG_FILE": str(config)}):
            process = subprocess.run([sys.executable, "-I", "-B", "-m", "pip", "config", "list"],
                                     capture_output=True, text=True, encoding="utf-8", env=runtime.pip_env())
        self.assertEqual(process.returncode, 0)
        self.assertNotIn("global.target", process.stdout)
        self.assertFalse((self.case / "wrong-target").exists())

    def test_selected_runtime_versions_must_meet_actual_requirements(self):
        declarations = runtime.declarations()
        declarations[0]["specifier"] = ">=99,<100"
        with patch.object(runtime, "declarations", return_value=declarations):
            result = runtime.probe(sys.executable)
        self.assertFalse(result["ready"])
        self.assertEqual(result["dependencies"][0]["error"], "version_mismatch")

    def test_preparation_preserves_stdin_and_redacts_credentials_in_errors(self):
        failure = subprocess.CompletedProcess([], 1, "", "Failed https://user:secret@example.invalid/simple")
        with patch.object(runtime.subprocess, "run", return_value=failure) as call:
            with self.assertRaises(runtime.RuntimeErrorInfo) as caught:
                runtime.setup_step(["fixture"], "install")
        self.assertIs(call.call_args.kwargs["stdin"], subprocess.DEVNULL)
        self.assertNotIn("user:secret", caught.exception.details["diagnostic"])
        self.assertIn("[redacted]@example.invalid", caught.exception.details["diagnostic"])

    def test_minimum_python_is_reported_before_preparation(self):
        with patch.object(runtime.sys, "version_info", (3, 11, 0)), patch.object(runtime, "setup") as setup:
            code, result, _ = self.direct(["setup", "--runtime-home", str(self.home)])
        self.assertEqual(code, 2)
        self.assertEqual(result["errors"][0]["code"], "python_version_unsupported")
        setup.assert_not_called()
        self.assertFalse(self.home.exists())

    def test_package_cache_cannot_be_a_runtime_home(self):
        with self.assertRaises(runtime.RuntimeErrorInfo) as caught:
            runtime.layout(BUNDLE / "runtime")
        self.assertEqual(caught.exception.code, "invalid_runtime_home")
        self.assertFalse((BUNDLE / "runtime").exists())

    def test_legacy_help_on_empty_python_returns_diagnostic_without_installing(self):
        env = dict(runtime.child_env(), GAMECADEN_RUNTIME_HOME=str(self.home))
        process = subprocess.run([str(self.empty_python), "-B", str(BUNDLE / "scripts/workflow_io.py"), "--help"],
                                 capture_output=True, text=True, encoding="utf-8", env=env)
        result = json.loads(process.stdout)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(result["status"], "not_ready")
        self.assertNotIn("ModuleNotFoundError", process.stderr)
        self.assertFalse(self.home.exists())

    def test_all_legacy_calls_without_bytecode_flags_preserve_package_bytes(self):
        package = self.case / "installed-package"
        shutil.copytree(BUNDLE, package, ignore=shutil.ignore_patterns("__pycache__"))
        before = snapshot(package)
        env = dict(runtime.child_env(), GAMECADEN_RUNTIME_HOME=str(self.home))
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        for script in runtime.TOOLS.values():
            with self.subTest(script=script):
                process = subprocess.run([str(self.empty_python), str(package / "scripts" / script), "--help"],
                                         capture_output=True, text=True, encoding="utf-8", env=env)
                self.assertEqual(process.returncode, 2)
                self.assertEqual(json.loads(process.stdout)["status"], "not_ready")
                self.assertNotIn("ModuleNotFoundError", process.stderr)
        self.assertEqual(snapshot(package), before)
        self.assertFalse(self.home.exists())

    def test_native_io_stdin_replay_and_exit_code_are_preserved(self):
        project = self.case / "game"
        shutil.copytree(BUNDLE / "examples/v1/project", project)
        request = {"protocol_version": 1, "request_id": "runtime-native-create", "operation": "record.create",
                   "context": {"project_root": str(project)}, "preconditions": [],
                   "payload": {"record_type": "task", "metadata": {"title": "Runtime fixture", "mode": "quick",
                               "kind": "bug", "status": "active", "epic": None}, "body": "Native original request."}}
        args = ("run", "--python", sys.executable, "io", "--project-root", project, "--request", "-")
        first_process, first = self.command(*args, input=json.dumps(request))
        self.assertEqual(first_process.returncode, 0)
        self.assertEqual(first["protocol_version"], 1)
        self.assertEqual(first["request_id"], request["request_id"])
        second_process, second = self.command(*args, input=json.dumps(request))
        self.assertEqual(second_process.returncode, 0)
        self.assertTrue(second["replayed"])
        self.assertEqual(first["receipt"]["allocations"], second["receipt"]["allocations"])
        before = snapshot(project)
        request["payload"]["metadata"]["title"] = "Conflict must preserve original"
        failed_process, failed = self.command(*args, input=json.dumps(request))
        self.assertEqual(failed_process.returncode, 2)
        self.assertEqual(failed["errors"][0]["code"], "request_id_conflict")
        self.assertEqual(snapshot(project), before)


if __name__ == "__main__":
    unittest.main()
