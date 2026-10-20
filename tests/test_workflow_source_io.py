"""Source payload, long-path and bounded listing regressions on anonymous copies."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from workflow_formats import WorkflowError, revision, validate, yaml_dump, yaml_load
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
        # Windows TEMP may use an 8.3 alias; bind the existing fixture's canonical root.
        self.root = self.root.resolve(strict=True)
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

    def test_located_reads_do_not_scan_unrelated_collections(self):
        target = self.root / "game-workflow/tasks/T-002-feedback.md"
        unrelated = self.root / "game-workflow/tasks/T-002/raw/large-report.json"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text('{"frames": [' + '"producer-data",' * 10000 + 'null]}', encoding="utf-8")
        for operation in ("record.read", "record.resolve"):
            with self.subTest(operation=operation), patch.object(Project, "scan", side_effect=AssertionError("Unrelated full scan")):
                response = self.call(operation, {"target": {"path": str(target)}})
                self.assertEqual(response["status"], "ok", response)
                self.assertEqual(response["data"]["metadata"]["id"], "T-002")
                self.assertEqual(response["data"]["revision"], revision(target.read_bytes()))

    def independent_update(self):
        target = self.root / "game-workflow/tasks/T-900-independent.md"
        target.write_text("---\nid: T-900\ntitle: Independent update\nmode: quick\nkind: engineering\nstatus: active\nepic: null\n---\n\nOriginal body.\n", encoding="utf-8")
        request = {"protocol_version": 1, "request_id": "source-write-test", "operation": "record.update",
                   "context": self.context, "payload": {"target": {"path": str(target)},
                   "body": "Updated body.", "reason": "Check actual dependency scope"},
                   "preconditions": [{"target": {"path": str(target)}, "expected_revision": revision(target.read_bytes())}]}
        return target, request

    def test_located_independent_update_keeps_only_actual_guards(self):
        target, request = self.independent_update()
        api = Workflow(self.root)
        with patch.object(Project, "scan", side_effect=AssertionError("Independent update scanned unrelated sources")):
            response = api.execute(request)
        self.assertEqual(response["status"], "ok", response)
        self.assertIn("Updated body.", target.read_text(encoding="utf-8"))
        receipt = api.store.load(request["request_id"])
        self.assertEqual(set(receipt["guards"]), {str(target), str(self.root / "game-workflow/workspace.yaml")})

    def test_unrelated_producer_change_does_not_conflict_with_located_update(self):
        target, request = self.independent_update()
        unrelated = self.root / "game-workflow/tasks/T-002/raw/report.json"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text('{"producer": "old"}', encoding="utf-8")
        original = Workflow.write_operation

        def change_after_planning(api, operation, payload):
            result = original(api, operation, payload)
            unrelated.write_text('{"producer": "new"}', encoding="utf-8")
            return result

        with patch.object(Workflow, "write_operation", change_after_planning):
            response = Workflow(self.root).execute(request)
        self.assertEqual(response["status"], "ok", response)
        self.assertIn("Updated body.", target.read_text(encoding="utf-8"))
        self.assertEqual(unrelated.read_text(encoding="utf-8"), '{"producer": "new"}')

    def test_located_update_preserves_explicit_non_target_dependency(self):
        target, request = self.independent_update()
        dependency = self.root / "game-workflow/spec/combat.md"
        original_bytes = dependency.read_bytes()
        request["preconditions"].append({"target": {"path": str(dependency)}, "expected_revision": revision(original_bytes)})
        original = Workflow.write_operation

        def change_dependency(api, operation, payload):
            result = original(api, operation, payload)
            dependency.write_bytes(original_bytes + b"\nConcurrent dependency edit\n")
            return result

        with patch.object(Workflow, "write_operation", change_dependency):
            response = Workflow(self.root).execute(request)
        self.assertEqual(response["status"], "conflict", response)
        self.assertEqual(response["errors"][0]["code"], "revision_conflict")
        self.assertIn("Original body.", target.read_text(encoding="utf-8"))

    def test_list_detects_new_member_after_identity_discovery(self):
        added = self.root / "game-workflow/tasks/T-002/new-output.json"
        original = Project.read_record

        def add_after_discovery(project, record, include_body=True):
            data = original(project, record, include_body)
            if not added.exists():
                added.parent.mkdir(parents=True, exist_ok=True)
                added.write_text('{"producer": true}', encoding="utf-8")
            return data

        with patch.object(Project, "read_record", add_after_discovery):
            response = self.call("record.list", {"limit": 3})
        self.assertEqual(response["status"], "conflict", response)
        self.assertEqual(response["errors"][0]["code"], "revision_conflict")

    def test_located_update_still_rejects_ambiguous_parent_identity(self):
        target = self.root / "game-workflow/tasks/T-002-feedback.md"
        before = target.read_bytes()
        parent = Project(self.root, self.context).resolve({"id": "E-001"}).path
        duplicate = parent.with_name("E-900-duplicate" + parent.suffix)
        duplicate.write_bytes(parent.read_bytes())
        response = Workflow(self.root).execute({"protocol_version": 1, "request_id": "ambiguous-parent",
            "operation": "record.update", "context": self.context,
            "payload": {"target": {"path": str(target)}, "body": "New body", "reason": "Parent identity check"},
            "preconditions": [{"target": {"path": str(target)}, "expected_revision": revision(before)}]})
        self.assertEqual(response["status"], "rejected", response)
        self.assertEqual(response["errors"][0]["code"], "ambiguous_ref")
        self.assertEqual(target.read_bytes(), before)

    def test_new_collection_is_optional_but_existing_file_is_not_a_collection(self):
        workspace = self.root / "game-workflow/workspace.yaml"
        mapping = yaml_load(workspace.read_text(encoding="utf-8"))
        mapping["sources"].append({"id": "future-notes", "role": "notes", "kind": "collection",
                                   "path": "future-notes", "owner": "project", "format": "native-markdown-v1"})
        workspace.write_text(yaml_dump(mapping), encoding="utf-8")
        before = Project(self.root, self.context)
        before.scan()
        self.assertFalse(any(row["code"] in ("not_found", "invalid_scope") for row in before.diagnostics))
        (self.root / "game-workflow/future-notes").write_text("Wrong object type", encoding="utf-8")
        after = Project(self.root, self.context)
        after.scan()
        self.assertFalse(after.scan_complete)
        self.assertTrue(any(row["code"] == "invalid_scope" for row in after.diagnostics))

    def test_panel_recovers_unreadable_source_without_membership_change(self):
        panel = PanelData(self.root)
        failed = self.root / "game-workflow/spec/combat.md"
        original = Project.read_bytes

        def unreadable(project, path):
            if Path(path) == failed:
                raise WorkflowError("not_found", "Transient source failure", {"path": str(path)})
            return original(project, path)

        with patch.object(Project, "read_bytes", unreadable):
            first = panel.snapshot(limit=1)
            self.assertIsNotNone(first["next_cursor"])
            # Stable failed-source diagnostics remain pageable.
            panel.snapshot(first["next_cursor"], limit=1)
            self.assertFalse(any(row["path"] == str(failed) for row in panel.snapshot_all()["records"]))
        with self.assertRaises(PanelDataError) as error:
            panel.snapshot(first["next_cursor"], limit=1)
        self.assertEqual(error.exception.code, "stale_cursor")
        restored = panel.snapshot_all()
        self.assertTrue(any(row["path"] == str(failed) for row in restored["records"]))
        self.assertFalse(any(row["code"] == "not_found" for row in restored["diagnostics"]))

    def test_panel_detects_workspace_appearing_after_unconfigured_read(self):
        workspace = self.root / "game-workflow/workspace.yaml"
        original = workspace.read_bytes()
        workspace.unlink()
        panel = PanelData(self.root)
        first = panel.snapshot(limit=1)
        self.assertFalse(first["project"]["configured"])
        workspace.write_bytes(original)
        with self.assertRaises(PanelDataError) as error:
            panel.snapshot(first["next_cursor"], limit=1)
        self.assertEqual(error.exception.code, "stale_cursor")
        self.assertTrue(panel.snapshot_all()["project"]["configured"])

    def test_partial_collection_scan_failure_remains_readable_and_recovers(self):
        panel = PanelData(self.root)
        original = Project.source_inventory
        failed = self.root / "game-workflow/spec/combat.md"

        def partial_failure(project):
            inventory = original(project)
            for entry in inventory:
                if str(failed) in entry["files"]:
                    entry["error"] = {"code": "read_failed", "message": "Collection traversal interrupted"}
            return inventory

        with patch.object(Project, "source_inventory", partial_failure):
            page = panel.snapshot(limit=1)
            self.assertIsNotNone(page["next_cursor"])
            panel.snapshot(page["next_cursor"], limit=1)
            self.assertTrue(any(row["code"] == "read_failed" for row in panel.snapshot_all()["diagnostics"]))
        restored = panel.snapshot_all()
        self.assertTrue(any(row["path"] == str(failed) for row in restored["records"]))
        self.assertFalse(any(row["code"] == "read_failed" for row in restored["diagnostics"]))

    @unittest.skipUnless(os.name == "nt", "Windows junction guard")
    def test_warm_source_location_does_not_authorize_replaced_ancestor(self):
        folder = self.root / "extra"
        outside = self.root.parent / "outside"
        folder.mkdir()
        outside.mkdir()
        path = folder / "input.md"
        path.write_text("Original", encoding="utf-8")
        (outside / "input.md").write_text("Outside", encoding="utf-8")
        workspace = self.root / "game-workflow/workspace.yaml"
        mapping = yaml_load(workspace.read_text(encoding="utf-8"))
        mapping["sources"].append({"id": "extra-input", "role": "notes", "kind": "file",
                                   "path": "../extra/input.md", "owner": "project", "format": "external"})
        workspace.write_text(yaml_dump(mapping), encoding="utf-8")
        project = Project(self.root, self.context)
        project.resolve({"path": str(path)})
        self.assertTrue(project._source_locations)
        path.unlink()
        folder.rmdir()
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(folder), str(outside)],
                                capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode:
            self.skipTest("Windows junction creation unavailable")
        try:
            with self.assertRaises(WorkflowError) as error:
                project.resolve({"path": str(path)})
            self.assertEqual(error.exception.code, "invalid_scope")
        finally:
            # Remove only the junction itself before disposable-tree cleanup.
            if folder.is_junction():
                folder.rmdir()

    def test_located_read_retains_revision_and_pending_checks(self):
        target = self.root / "game-workflow/tasks/T-002-feedback.md"
        workspace = self.root / "game-workflow/workspace.yaml"
        original = Project.read_record
        for changed in (target, workspace):
            before = changed.read_bytes()

            def change_after_read(project, record, include_body=True):
                result = original(project, record, include_body)
                changed.write_bytes(before + b"\n# Concurrent edit\n")
                return result

            with self.subTest(changed=changed.name), patch.object(Project, "read_record", change_after_read):
                response = self.call("record.read", {"target": {"path": str(target)}})
                self.assertEqual(response["status"], "conflict", response)
                self.assertEqual(response["errors"][0]["code"], "revision_conflict")
            changed.write_bytes(before)
        with patch("workflow_io.Store.pending", return_value=[{"plans": [{"path": str(target)}]}]):
            response = self.call("record.read", {"target": {"path": str(target)}})
            self.assertEqual(response["errors"][0]["code"], "operation_pending")

    def test_id_reads_still_detect_ambiguous_formal_identity(self):
        target = self.root / "game-workflow/tasks/T-002-feedback.md"
        duplicate = target.with_name("T-999-duplicate.md")
        duplicate.write_bytes(target.read_bytes())
        response = self.call("record.read", {"target": {"id": "T-002"}})
        self.assertEqual(response["status"], "rejected", response)
        self.assertEqual(response["errors"][0]["code"], "ambiguous_ref")
        located = self.call("record.read", {"target": {"path": str(target)}})
        self.assertEqual(located["status"], "ok", located)
        listing = self.call("record.list", {"limit": 1000})
        self.assertIn("duplicate_id", {row["code"] for row in listing["data"]["diagnostics"]})

    def test_raw_command_captures_and_empty_json_are_read_only_attachments(self):
        folder = self.root / "game-workflow/tasks/T-002/evidence"
        folder.mkdir(parents=True)
        samples = {"failed.stdout.json": b"", "failed.stderr.json": b"Traceback: producer failed\n",
                   "empty-report.json": b"\xef\xbb\xbf\r\n \t",
                   "captured.stdout.json": b'{"id":"T-901","mode":"quick","epic":null}\n'}
        for name, body in samples.items():
            with self.subTest(name=name):
                path = folder / name
                path.write_bytes(body)
                response = self.call("record.read", {"target": {"path": str(path)}})
                self.assertEqual(response["status"], "ok", response)
                data = response["data"]
                self.assertEqual(data["interpretation"], "raw")
                self.assertEqual(data["capabilities"], ["record.read"])
                self.assertNotIn("id", data["ref"])
                self.assertEqual(data["revision"], revision(body))
                self.assertEqual(data["body"], body.decode("utf-8-sig").replace("\r\n", "\n"))
                self.assertEqual(path.read_bytes(), body)
        listing = self.call("record.list", {"types": ["task"], "limit": 1000})
        self.assertNotIn("T-901", {(row.get("metadata") or {}).get("id") for row in listing["data"]["items"]})
        self.assertFalse(any(row["code"] == "invalid_record" for row in listing["data"]["diagnostics"]))

    def test_raw_attachment_handling_does_not_hide_broken_formal_records(self):
        folder = self.root / "game-workflow/tasks/T-002/evidence"
        folder.mkdir(parents=True)
        for name, body in {"task.json": b"", "T-901.stdout.json": b"not JSON",
                           "broken.json": b'{"id":"T-901","title":"Missing lifecycle"}'}.items():
            with self.subTest(name=name):
                path = folder / name
                path.write_bytes(body)
                response = self.call("record.read", {"target": {"path": str(path)}})
                self.assertEqual(response["status"], "rejected", response)
        declared = self.root / "declared/index.json"
        declared.parent.mkdir()
        declared.write_bytes(b"")
        workspace = self.root / "game-workflow/workspace.yaml"
        mapping = yaml_load(workspace.read_text(encoding="utf-8"))
        mapping["sources"].append({"id": "explicit-task", "role": "task", "kind": "file",
                                  "path": "../declared/index.json", "owner": "flow", "format": "native-json-v1"})
        workspace.write_text(yaml_dump(mapping), encoding="utf-8")
        response = self.call("record.read", {"target": {"path": str(declared)}})
        self.assertEqual(response["status"], "rejected", response)
        listing = self.call("record.list", {"limit": 1000})
        self.assertEqual(sum(row["code"] == "invalid_record" for row in listing["data"]["diagnostics"]), 4)

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
        original = Project.check_snapshot
        checked = False
        changed = self.root / "game-workflow/vision.md"

        def change_before_final_check(project):
            nonlocal checked
            if not checked:
                checked = True
                self.assertIn(str(changed), project.observed)
                changed.write_bytes(changed.read_bytes() + b"\nchanged outside page\n")
            return original(project)

        with patch.object(Project, "check_snapshot", change_before_final_check):
            with self.assertRaises(PanelDataError) as error:
                panel.snapshot(limit=3)
        self.assertEqual(error.exception.code, "revision_conflict")


if __name__ == "__main__":
    unittest.main()
