"""Black-box distribution contract tests; all fixtures stay under work/.

Run with: python scripts/check.py --suite distribution from the repository root.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


BUNDLE = (Path(__file__).resolve().parents[1] / "plugins" / "gamecaden")
REPO = BUNDLE.parents[1]
CLI = BUNDLE / "scripts" / "gamecaden.py"
WORK = REPO / "work" / "distribution-tests"


def snapshot(root):
    if os.name == "nt" and not str(root).startswith("\\\\?\\"):
        root = Path("\\\\?\\" + str(Path(root).absolute()))
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file()}


class DistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        WORK.mkdir(parents=True, exist_ok=True)
        cls.suite = Path(tempfile.mkdtemp(prefix="suite-", dir=WORK))
        cls.source = cls.suite / "source"
        shutil.copytree(BUNDLE, cls.source, ignore=shutil.ignore_patterns("__pycache__"))
        cls.release1 = cls.build(cls.source, cls.suite / "rc1", "0.1.0-rc.1")
        with (cls.source / "INSTALL.md").open("a", encoding="utf-8") as stream:
            stream.write("\nDistribution test fixture revision.\n")
        cls.release2 = cls.build(cls.source, cls.suite / "rc2", "0.1.0-rc.2")
        cls.same_version = cls.build(cls.source, cls.suite / "conflict", "0.1.0-rc.1")

    @classmethod
    def command(cls, *args, ok=True):
        result = subprocess.run([sys.executable, str(CLI), *map(str, args)],
                                capture_output=True, text=True, encoding="utf-8")
        try:
            data = json.loads(result.stdout)
        except ValueError as error:
            raise AssertionError(f"CLI did not return JSON: {result.stdout!r}; {result.stderr!r}") from error
        expected = (0, "ok") if ok else (2, "rejected")
        if (result.returncode, data.get("status")) != expected:
            raise AssertionError(f"Expected {expected}, got {result.returncode}: {data}; {result.stderr}")
        return data

    @classmethod
    def build(cls, source, output, version):
        data = cls.command("build", "--source", source, "--output", output, "--version", version)
        for key in ("digest", "version", "plugin_root", "archive"):
            if key not in data:
                raise AssertionError(f"Missing build field {key}: {data}")
        if len(data["digest"]) != 64 or any(c not in "0123456789abcdef" for c in data["digest"]):
            raise AssertionError(f"Invalid content digest: {data}")
        return data

    def setUp(self):
        self.case = Path(tempfile.mkdtemp(prefix="c-", dir=self.suite))
        self.target = self.case / "t"

    def stage(self, release=None, ok=True):
        return self.command("stage", "--package", (release or self.release1)["plugin_root"],
                            "--target-root", self.target, ok=ok)

    def current(self):
        return self.command("status", "--target-root", self.target)["current"]

    def test_deterministic_build_and_verify(self):
        repeat = self.build(self.source, self.case / "repeat", "0.1.0-rc.2")
        self.assertEqual(repeat["digest"], self.release2["digest"])
        self.assertEqual(Path(repeat["archive"]).read_bytes(), Path(self.release2["archive"]).read_bytes())
        self.assertEqual(snapshot(Path(repeat["plugin_root"])), snapshot(Path(self.release2["plugin_root"])))
        self.command("verify", "--package", repeat["plugin_root"])
        self.assertTrue((Path(repeat["plugin_root"]) / ".gamecaden-package.json").is_file())
        self.assertTrue((self.case / "repeat/.agents/plugins/marketplace.json").is_file())

    def test_public_license_is_retained_in_archive(self):
        expected = (BUNDLE / "LICENSE").read_bytes()
        package = Path(self.release1["plugin_root"])
        self.assertEqual((package / "LICENSE").read_bytes(), expected)
        with zipfile.ZipFile(self.release1["archive"]) as archive:
            self.assertEqual(archive.read("gamecaden/LICENSE"), expected)
            self.assertIn("gamecaden/panels/night/vendor/ELK-LICENSE.md", archive.namelist())
        self.command("verify", "--package", package)

    def test_three_host_manifests_and_catalogs_share_package(self):
        package = Path(self.release1["plugin_root"])
        for rel in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            manifest = json.loads((package / rel).read_text(encoding="utf-8"))
            self.assertEqual(manifest["name"], "gamecaden")
            self.assertEqual(manifest["version"], self.release1["version"])
        self.assertNotIn("skills", json.loads((package / ".claude-plugin/plugin.json").read_text(encoding="utf-8")))
        output = self.suite / "rc1"
        codex = json.loads((output / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        claude = json.loads((output / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(claude["name"], "gamecaden-local")
        self.assertEqual(claude["owner"]["name"], "immortalbeating")
        self.assertEqual(claude["plugins"], [{"name": "gamecaden", "source": "./plugins/gamecaden"}])
        self.assertEqual(codex["plugins"][0]["source"]["path"], claude["plugins"][0]["source"])
        self.assertEqual((output / claude["plugins"][0]["source"]).resolve(), package.resolve())

    def test_standalone_and_shared_dependencies_retained_in_archive(self):
        package = Path(self.release1["plugin_root"])
        required = ["SKILL.md", ".claude-plugin/plugin.json", "INSTALL.md",
                    "scripts/gamecaden_runtime.py", "scripts/requirements.txt"]
        required += [p.relative_to(BUNDLE).as_posix() for p in (BUNDLE / "shared").rglob("*") if p.is_file()]
        self.assertGreater(len(required), 2)
        with zipfile.ZipFile(self.release1["archive"]) as archive:
            for rel in required:
                if rel != ".claude-plugin/plugin.json":
                    self.assertEqual((package / rel).read_bytes(), (BUNDLE / rel).read_bytes())
                self.assertEqual(archive.read("gamecaden/" + rel), (package / rel).read_bytes())

    def test_legacy_package_build_verify_stage_and_rollback(self):
        source = self.case / "legacy"
        shutil.copytree(self.source, source)
        (source / ".claude-plugin/plugin.json").unlink()
        (source / ".claude-plugin").rmdir()
        (source / "SKILL.md").unlink()
        (source / "INSTALL.md").write_text("# Legacy installation fixture\n", encoding="utf-8")
        legacy = self.build(source, self.case / "legacy-output", "0.1.0")
        self.assertFalse((self.case / "legacy-output/.claude-plugin/marketplace.json").exists())
        self.command("verify", "--package", legacy["plugin_root"])
        self.assertEqual(self.stage(legacy)["current"]["digest"], legacy["digest"])
        self.stage(self.release2)
        restored = self.command("rollback", "--target-root", self.target)
        self.assertEqual(restored["current"]["digest"], legacy["digest"])

    def test_invalid_claude_or_standalone_identity_rejected(self):
        for kind in ("name", "version", "skills", "standalone"):
            with self.subTest(kind=kind):
                source = self.case / kind
                shutil.copytree(self.source, source)
                if kind == "standalone":
                    path = source / "SKILL.md"
                    path.write_text(path.read_text(encoding="utf-8").replace("name: gamecaden", "name: other"), encoding="utf-8")
                else:
                    path = source / ".claude-plugin/plugin.json"
                    manifest = json.loads(path.read_text(encoding="utf-8"))
                    manifest[kind] = {"name": "other", "version": "9.0.0", "skills": "./other-skills/"}[kind]
                    path.write_text(json.dumps(manifest), encoding="utf-8")
                result = self.command("build", "--source", source, "--output", self.case / (kind + "-output"), ok=False)
                self.assertEqual(result["errors"][0]["code"], "invalid_skills" if kind == "standalone" else "invalid_identity")

    def test_tampered_and_extra_files_rejected(self):
        for kind in ("tampered", "extra"):
            package = self.case / kind
            shutil.copytree(self.release1["plugin_root"], package)
            file = package / ("INSTALL.md" if kind == "tampered" else "unexpected.txt")
            file.write_text("unexpected bytes", encoding="utf-8")
            self.command("verify", "--package", package, ok=False)
            self.command("stage", "--package", package, "--target-root", self.target, ok=False)

    def test_upgrade_idempotence_and_rollback(self):
        first = self.stage()
        self.assertEqual(first["current"]["digest"], self.release1["digest"])
        owned = self.target / "plugins/gamecaden" / self.release1["digest"]
        self.assertTrue(owned.is_dir())
        before = snapshot(self.target)
        self.stage()
        self.assertEqual(snapshot(self.target), before)
        upgraded = self.stage(self.release2)
        self.assertEqual(upgraded["current"]["version"], "0.1.0-rc.2")
        rolled = self.command("rollback", "--target-root", self.target)
        self.assertEqual(rolled["current"]["digest"], self.release1["digest"])
        self.assertEqual(snapshot(owned), snapshot(Path(self.release1["plugin_root"])))

    def test_first_install_rollback(self):
        self.stage()
        result = self.command("rollback", "--target-root", self.target)
        self.assertIsNone(result["current"])
        self.assertIsNone(self.current())
        self.assertTrue((self.target / "plugins/gamecaden" / self.release1["digest"]).is_dir())

    def test_same_version_different_digest_rejected(self):
        self.stage()
        before = snapshot(self.target)
        self.stage(self.same_version, ok=False)
        self.assertEqual(snapshot(self.target), before)

    def test_historical_version_different_digest_rejected_after_upgrade(self):
        self.stage()
        self.stage(self.release2)
        before = snapshot(self.target)
        self.stage(self.same_version, ok=False)
        self.assertEqual(snapshot(self.target), before)
        self.assertEqual(self.current()["digest"], self.release2["digest"])
        rolled = self.command("rollback", "--target-root", self.target)
        self.assertEqual(rolled["current"]["digest"], self.release1["digest"])

    def test_historical_version_different_digest_rejected_after_uninstall(self):
        self.stage()
        self.assertIsNone(self.command("rollback", "--target-root", self.target)["current"])
        before = snapshot(self.target)
        self.stage(self.same_version, ok=False)
        self.assertEqual(snapshot(self.target), before)
        self.assertIsNone(self.current())
        restored = self.stage()
        self.assertEqual(restored["current"]["digest"], self.release1["digest"])

    def test_marketplace_other_entries_and_fields_preserved(self):
        catalog = json.loads((self.suite / "rc1/.agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        catalog["plugins"] = [{"name": "other-plugin", "source": {"source": "local", "path": "./other"}, "custom": [1, 2]}]
        catalog["custom_metadata"] = {"keep": "exact"}
        path = self.target / ".agents/plugins/marketplace.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(catalog), encoding="utf-8")
        self.stage()
        self.stage(self.release2)
        self.command("rollback", "--target-root", self.target)
        actual = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(actual["custom_metadata"], catalog["custom_metadata"])
        self.assertIn(catalog["plugins"][0], actual["plugins"])

    def test_unknown_same_name_catalog_rejected(self):
        path = self.target / ".agents/plugins/marketplace.json"
        path.parent.mkdir(parents=True)
        catalog = json.loads((self.suite / "rc1/.agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        path.write_text(json.dumps(catalog), encoding="utf-8")
        before = path.read_bytes()
        self.stage(ok=False)
        self.assertEqual(path.read_bytes(), before)

    def test_unknown_package_directory_rejected(self):
        foreign = self.target / "plugins/gamecaden" / self.release1["digest"]
        foreign.mkdir(parents=True)
        (foreign / "foreign.txt").write_text("owned by someone else", encoding="utf-8")
        before = snapshot(foreign)
        self.stage(ok=False)
        self.assertEqual(snapshot(foreign), before)
        self.assertFalse((self.target / ".agents/plugins/marketplace.json").exists())

    def test_changed_active_package_rejected(self):
        installed = self.stage()["current"]
        root = self.target / installed["source_path"]
        (root / "INSTALL.md").write_text("external modification", encoding="utf-8")
        before = snapshot(self.target)
        self.stage(self.release2, ok=False)
        self.command("status", "--target-root", self.target, ok=False)
        self.command("rollback", "--target-root", self.target, ok=False)
        self.assertEqual(snapshot(self.target), before)

    def test_project_records_unchanged(self):
        project = self.target / "game-workflow/tasks/task-1"
        project.mkdir(parents=True)
        (project / "task.json").write_text('{"status":"active","human_approved":false}', encoding="utf-8")
        before = snapshot(self.target / "game-workflow")
        self.stage()
        self.stage(self.release2)
        self.command("rollback", "--target-root", self.target)
        self.assertEqual(snapshot(self.target / "game-workflow"), before)

    def test_overlapping_paths_rejected(self):
        package = Path(self.release1["plugin_root"])
        before = snapshot(package)
        self.command("stage", "--package", package, "--target-root", package / "nested", ok=False)
        self.assertEqual(snapshot(package), before)
        self.command("build", "--source", self.source, "--output", self.source / "nested", ok=False)

    def test_existing_build_output_is_not_overwritten(self):
        output = self.case / "existing"
        output.mkdir()
        (output / "sentinel.txt").write_text("existing user data", encoding="utf-8")
        before = snapshot(output)
        self.command("build", "--source", self.source, "--output", output, ok=False)
        self.assertEqual(snapshot(output), before)

    def test_windows_long_install_path(self):
        if os.name != "nt":
            self.skipTest("Windows extended-path contract")
        self.target = self.case / ("long-target-" + "x" * 70) / ("y" * 70)
        result = self.stage()
        self.assertEqual(result["current"]["digest"], self.release1["digest"])
        self.assertEqual(self.current()["digest"], self.release1["digest"])
        owned = self.target / result["current"]["source_path"]
        self.assertEqual(snapshot(owned), snapshot(Path(self.release1["plugin_root"])))
        self.assertIsNone(self.command("rollback", "--target-root", self.target)["current"])

    def test_package_symlink_rejected(self):
        package = self.case / "linked-package"
        shutil.copytree(self.release1["plugin_root"], package)
        linked = package / "INSTALL.md"
        linked.unlink()
        try:
            linked.symlink_to(Path(self.release1["plugin_root"]) / "INSTALL.md")
        except OSError:
            self.skipTest("File symlinks unavailable")
        self.command("verify", "--package", package, ok=False)
        self.command("stage", "--package", package, "--target-root", self.target, ok=False)

    def test_symlink_or_junction_target_rejected(self):
        outside = self.case / "outside"
        outside.mkdir()
        (outside / "sentinel.txt").write_text("do not alter", encoding="utf-8")
        try:
            self.target.symlink_to(outside, target_is_directory=True)
        except OSError:
            if os.name != "nt":
                self.skipTest("Directory symlinks unavailable")
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.target), str(outside)], capture_output=True)
            if result.returncode:
                self.skipTest("Directory symlinks and junctions unavailable")
        before = snapshot(outside)
        self.stage(ok=False)
        self.assertEqual(snapshot(outside), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
