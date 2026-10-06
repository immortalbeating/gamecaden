"""Focused integration checks for the panel's read-only adapter."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from workflow_panel_data import PanelData, PanelDataError
from workflow_formats import revision
from workflow_project import Project


FIXTURE = (Path(__file__).resolve().parents[1] / "plugins" / "gamecaden") / "examples/v1/project"
PNG = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000b49444154789c636000020000050001a5f645400000000049454e44ae426082")


class PanelDataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        shutil.copytree(FIXTURE, self.root)
        self.panel = PanelData(self.root)

    def asset(self):
        cursor = None
        while True:
            page = self.panel.snapshot(cursor, limit=2)
            for row in page["records"]:
                if row["record_type"] == "asset":
                    return row
            cursor = page["next_cursor"]
            if cursor is None:
                self.fail("Fixture asset was not listed")

    def test_native_pagination_read_and_stale_cursor(self):
        first = self.panel.snapshot(limit=1)
        self.assertEqual(first["project"]["kind"], "native")
        self.assertIsNotNone(first["next_cursor"])
        second = self.panel.snapshot(first["next_cursor"], limit=1)
        self.assertNotEqual(first["records"][0]["key"], second["records"][0]["key"])
        row = first["records"][0]
        self.assertIn("body", self.panel.read(row["key"]))
        (self.root / "game-workflow/vision.md").write_bytes((self.root / "game-workflow/vision.md").read_bytes() + b"\n")
        with self.assertRaises(PanelDataError) as error:
            self.panel.snapshot(first["next_cursor"], limit=1)
        self.assertEqual(error.exception.code, "stale_cursor")
        self.assertFalse((self.root / ".game-workflow-io").exists())

    def test_candidate_and_media_revision(self):
        row = self.asset()
        original = self.panel.candidate(row["key"], "C-001")
        self.assertEqual(original["check"]["status"], "verified")
        self.assertEqual(len(original["selected_uses"]), 2)
        self.assertEqual(original["all_uses"], original["selected_uses"])
        folder = self.root / "assets/flash"
        (folder / "preview.png").write_bytes(PNG)
        manifest_path = folder / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"].append({"path": "preview.png", "sha256": hashlib.sha256(PNG).hexdigest(), "role": "preview"})
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        ledger = self.root / "game-workflow/assets/ledger.yaml"
        ledger.write_text(ledger.read_text(encoding="utf-8").replace(original["version"]["value"], revision(manifest_path.read_bytes())[7:]), encoding="utf-8")
        asset = self.asset()
        result = self.panel.candidate(asset["key"], "C-001")
        self.assertEqual(result["check"]["status"], "verified")
        media = result["media"]
        self.assertEqual(len(media), 1)
        self.assertEqual(self.panel.media(media[0]["key"])["data"], PNG)
        (folder / "preview.png").write_bytes(PNG + b"changed")
        with self.assertRaises(PanelDataError) as error:
            self.panel.media(media[0]["key"])
        self.assertEqual(error.exception.code, "revision_conflict")
        self.assertEqual(self.panel.candidate(asset["key"], "C-001")["check"]["status"], "invalid")

    def test_external_raw_only_and_path_guard(self):
        source = self.root / "legacy/task.json"
        source.parent.mkdir(exist_ok=True)
        source.write_text('{"title":"legacy", "status":"done"}', encoding="utf-8")
        before = source.read_bytes()
        panel = PanelData(self.root, external_sources=[{"id": "legacy", "label": "Legacy task", "role": "task", "path": "legacy/task.json"}])
        page = panel.snapshot()
        self.assertEqual(page["project"]["kind"], "external")
        self.assertEqual(len(page["records"]), 1)
        row = page["records"][0]
        self.assertEqual(row["record_type"], "external")
        self.assertEqual(row["interpretation"], "raw")
        self.assertIsNone(row["metadata"])
        self.assertEqual(row["capabilities"], ["record.read"])
        self.assertIn("legacy", panel.read(row["key"])["body"])
        self.assertEqual(source.read_bytes(), before)
        self.assertFalse((self.root / ".game-workflow-io").exists())
        binary = self.root / "legacy/raw.bin"
        original_task = self.root / "game-workflow/tasks/T-002-feedback.md"
        raw_task = PanelData(self.root, external_sources=[{"id": "task", "label": "Task original", "role": "task", "path": "game-workflow/tasks/T-002-feedback.md"}])
        task_row = raw_task.snapshot()["records"][0]
        self.assertEqual(raw_task.read(task_row["key"])["body"], original_task.read_bytes().decode("utf-8-sig"))
        binary.write_bytes(b"\xff\x00")
        binary_panel = PanelData(self.root, external_sources=[{"id": "binary", "label": "Binary", "role": "file", "path": "legacy/raw.bin"}])
        binary_row = binary_panel.snapshot()["records"][0]
        self.assertIsNone(binary_panel.read(binary_row["key"])["body"])
        with self.assertRaises(PanelDataError) as unknown:
            binary_panel.read("unknown")
        self.assertEqual(unknown.exception.code, "not_found")
        escaped = PanelData(self.root, external_sources=[{"id": "out", "label": "Out", "role": "file", "path": "../out.txt"}])
        self.assertEqual(escaped.snapshot()["diagnostics"][0]["code"], "permission_denied")
        link = self.root / "legacy/linked.json"
        try:
            link.symlink_to(source)
        except (OSError, NotImplementedError):
            return
        linked = PanelData(self.root, external_sources=[{"id": "link", "label": "Link", "role": "file", "path": "legacy/linked.json"}])
        self.assertEqual(linked.snapshot()["diagnostics"][0]["code"], "invalid_scope")

    def test_manifest_changed_after_verification_is_not_registered(self):
        row = self.asset()
        original = Project.check_candidate
        def change_after_check(project, *args, **kwargs):
            original(project, *args, **kwargs)
            path = self.root / "assets/flash/manifest.json"
            path.write_bytes(path.read_bytes() + b"\n")
        with patch.object(Project, "check_candidate", change_after_check):
            with self.assertRaises(PanelDataError) as error:
                self.panel.candidate(row["key"], "C-001")
        self.assertEqual(error.exception.code, "revision_conflict")
        self.assertFalse(self.panel._media)


if __name__ == "__main__":
    unittest.main()
