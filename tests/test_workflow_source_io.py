"""Source payload, long-path and bounded listing regressions on anonymous copies."""
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from workflow_formats import WorkflowError, revision, validate
from workflow_io import Workflow
from workflow_project import Project
from workflow_panel_data import PanelData, PanelDataError
from workflow_storage import filesystem_path


FIXTURE = Path(__file__).resolve().parents[1] / "plugins/gamecaden/examples/v1/project"


class SourceIO(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gc-source-")
        self.root = Path(self.temp.name) / "project"
        shutil.copytree(FIXTURE, self.root)
        self.context = {"project_root": str(self.root), "base_dir": str(self.root / "game-workflow")}

    def tearDown(self):
        # The same extended physical path is needed for disposable long-path cleanup.
        target = Path(self.temp.name).resolve()
        self.assertEqual(self.root.parent.resolve(), target)
        shutil.rmtree(filesystem_path(target))
        self.temp.cleanup()

    def call(self, operation, payload):
        response = Workflow(self.root).execute({"protocol_version": 1, "request_id": "source-test",
            "operation": operation, "context": self.context, "payload": payload})
        validate("Response", response)
        return response

    def assert_payload(self, path, data):
        physical = filesystem_path(path)
        physical.parent.mkdir(parents=True, exist_ok=True)
        physical.write_bytes(data)
        response = self.call("record.read", {"target": {"path": str(path)}})
        self.assertEqual(response["status"], "ok", response)
        record = response["data"]
        self.assertIsNone(record["body"])
        self.assertIsNone(record["metadata"])
        self.assertEqual(record["revision"], revision(data))
        self.assertEqual(record["capabilities"], ["record.read"])
        self.assertEqual(record["path"], str(path))
        project = Project(self.root, self.context)
        self.assertIsNone(project.resolve({"path": str(path)}).id)
        subject = {"ref": {"path": str(path)}, "version": {"kind": "sha256", "value": revision(data)[7:]}}
        project.check_subject(subject, project.base)
        subject["version"]["proof"] = {"path": str(path)}
        project.check_subject(subject, project.base)
        physical.write_bytes(data + b"changed")
        with self.assertRaises(WorkflowError) as error:
            Project(self.root, self.context).check_subject(subject, project.base)
        self.assertEqual(error.exception.code, "version_mismatch")

    def test_binary_payload_inside_and_outside_native_collections(self):
        for location in ("game-workflow/tasks/T-002/picture.png", "game-workflow/evidence/clip.bin", "outside/picture.png"):
            with self.subTest(location=location):
                self.assert_payload(self.root / location, b"\x89PNG\r\n\x1a\n\xff" * 100)
        self.assert_payload(self.root / "game-workflow/tasks/T-002/payload.bin", b"valid UTF-8 still opaque")

    def test_native_text_record_remains_strict(self):
        for suffix in (".md", ".json", ".yaml", ".yml"):
            with self.subTest(suffix=suffix):
                path = self.root / ("game-workflow/tasks/T-999-invalid" + suffix)
                path.write_bytes(b"\xff")
                response = self.call("record.read", {"target": {"path": str(path)}})
                self.assertEqual(response["status"], "rejected", response)
                self.assertEqual(response["errors"][0]["code"], "unsupported_format")

    def test_non_record_utf8_text_preserved_inside_and_outside_collections(self):
        text = "# Source text\nprint('原文')\n"
        for location in ("game-workflow/tasks/T-002", "outside"):
            directory = self.root / location
            directory.mkdir(parents=True, exist_ok=True)
            for suffix in (".py", ".gd", ".js", ".css", ".svg", ".unrecognized"):
                with self.subTest(location=location, suffix=suffix):
                    path = directory / ("source" + suffix)
                    path.write_bytes(text.encode("utf-8"))
                    result = self.call("record.read", {"target": {"path": str(path)}})["data"]
                    self.assertEqual(result["body"], text)
                    self.assertIsNone(result["metadata"])
                    self.assertEqual(result["capabilities"], ["record.read"])
                    self.assertEqual(result["revision"], revision(text.encode("utf-8")))
                    self.assertIsNone(Project(self.root, self.context).resolve({"path": str(path)}).id)
            self.assert_payload(directory / "nul.unrecognized", b"valid\x00binary")
            self.assert_payload(directory / "invalid.unrecognized", b"\xff")

    @unittest.skipUnless(os.name == "nt", "Windows extended physical paths")
    def test_windows_long_source_read_list_and_subject(self):
        directory = self.root / "game-workflow/tasks/T-002"
        while len(str(directory / "source.md")) < 305:
            directory /= "source-segment-0123456789"
        self.assert_payload(directory / "picture.png", b"\x89PNG\xff")
        path = directory / "source.md"
        filesystem_path(path).write_text("# Long source\n", encoding="utf-8")
        response = self.call("record.read", {"target": {"path": str(path)}})
        self.assertEqual(response["status"], "ok", response)
        self.assertEqual(response["data"]["body"], "# Long source\n")
        listing = self.call("record.list", {"limit": 1000})
        self.assertEqual(listing["status"], "ok", listing)
        self.assertIn(str(path), [item["path"] for item in listing["data"]["items"]])
        project = Project(self.root, self.context)
        project.check_subject({"ref": {"path": str(path)}, "version": {"kind": "sha256",
            "value": revision(filesystem_path(path).read_bytes())[7:]}}, project.base)

    def test_listing_bounds_every_stream_and_exposes_failures(self):
        directory = self.root / "game-workflow/tasks/T-002"
        directory.mkdir(exist_ok=True)
        for index in range(40):
            (directory / f"payload-{index}.json").write_text('{"producer": true}', encoding="utf-8")
        (self.root / "game-workflow/tasks/T-999-invalid.md").write_bytes(b"\xff")
        payload = {"limit": 3, "types": ["task"]}
        first = self.call("record.list", payload)["data"]
        self.assertIn("unsupported_format", first["summary"]["diagnostic_counts"])
        self.assertFalse(first["complete"])
        all_items, all_revisions, all_diagnostics = [], [], []
        page = first
        while True:
            for field in ("items", "source_revisions", "diagnostics"):
                self.assertLessEqual(len(page[field]), 3)
            all_items.extend(page["items"])
            all_revisions.extend(page["source_revisions"])
            all_diagnostics.extend(page["diagnostics"])
            if page["next_cursor"] is None:
                break
            page = self.call("record.list", {**payload, "cursor": page["next_cursor"]})["data"]
        self.assertEqual(len(all_items), first["summary"]["item_count"])
        self.assertEqual(len(all_revisions), first["summary"]["source_revision_count"])
        self.assertEqual(len(all_diagnostics), first["summary"]["diagnostic_count"])
        (directory / "payload-0.json").write_text('{"changed": true}', encoding="utf-8")
        stale = self.call("record.list", {**payload, "cursor": first["next_cursor"]})
        self.assertEqual(stale["errors"][0]["code"], "stale_cursor")

    def test_panel_snapshot_follows_all_pages_with_same_query(self):
        panel = PanelData(self.root)
        cursor, rows, revisions = None, [], []
        while True:
            page = panel.snapshot(cursor, limit=3)
            rows.extend(page["records"])
            revisions.extend(page["source_revisions"])
            cursor = page["next_cursor"]
            if cursor is None:
                break
        listed = self.call("record.list", {"limit": 1000})["data"]
        self.assertEqual(len(rows), listed["summary"]["item_count"])
        self.assertEqual(len(revisions), listed["summary"]["source_revision_count"])
        self.assertEqual(len({row["key"] for row in rows}), len(rows))

    def test_panel_snapshot_detects_change_outside_revision_page(self):
        panel = PanelData(self.root)
        original = panel._call
        list_calls = 0
        changed = self.root / "game-workflow/vision.md"

        def change_before_second_listing(operation, payload):
            nonlocal list_calls
            if operation == "record.list":
                list_calls += 1
                self.assertEqual(payload.get("limit"), 3)
                if list_calls == 2:
                    changed.write_bytes(changed.read_bytes() + b"\nchanged outside page\n")
            result = original(operation, payload)
            if operation == "record.list" and list_calls == 1:
                self.assertNotIn(str(changed), [row["ref"]["path"] for row in result["source_revisions"]])
            return result

        with patch.object(panel, "_call", side_effect=change_before_second_listing):
            with self.assertRaises(PanelDataError) as error:
                panel.snapshot(limit=3)
        self.assertEqual(error.exception.code, "revision_conflict")


if __name__ == "__main__":
    unittest.main()
