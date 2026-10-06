"""Executable integration checks; all mutations use disposable project copies.

Run with this task's Python environment. Artifacts stay under work/io-runtime-eval
for inspection; the suite never deletes a user project or invokes engine/Git work.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from workflow_formats import Document, json_load, plain, revision, validate, yaml_dump, yaml_load
from workflow_io import Workflow
from workflow_storage import Store, filesystem_path


BUNDLE = (Path(__file__).resolve().parents[1] / "plugins" / "gamecaden")
FIXTURE = BUNDLE / "examples/v1/project"
RUN_ROOT = BUNDLE.parents[1] / "work/io-runtime-eval"
RUN_ROOT.mkdir(parents=True, exist_ok=True)
CLI = BUNDLE / "scripts/workflow_io.py"


class Integration(unittest.TestCase):
    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(prefix=self._testMethodName + "-", dir=RUN_ROOT))
        self.root = self.folder / "project"
        self.assertTrue(self.root.resolve().is_relative_to(RUN_ROOT.resolve()))
        shutil.copytree(FIXTURE, self.root)
        self.api = Workflow(self.root)
        self.seq = 0

    def request(self, operation, payload, conditions=None, **extra):
        self.seq += 1
        request = {"protocol_version": 1, "request_id": f"test-{self.seq}", "operation": operation,
                   "context": {"project_root": str(self.root), "base_dir": str(self.root / "game-workflow")}, "payload": payload}
        if conditions is not None:
            request["preconditions"] = conditions
        request.update(extra)
        return request

    def condition(self, path):
        absolute = self.root / "game-workflow" / path
        return {"target": {"path": path}, "expected_revision": revision(absolute.read_bytes()) if absolute.exists() else None}

    def run_request(self, request, status="ok", api=None):
        response = (api or self.api).execute(request)
        (self.folder / f"response-{request['request_id']}.json").write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")
        self.assertEqual(status, response["status"], response)
        validate("Response", response)
        return response

    def read(self, target):
        return self.run_request(self.request("record.read", {"target": target}))["data"]

    def task_create(self, **metadata):
        data = {"title": "New task", "mode": "quick", "kind": "bug", "status": "active", "epic": None}
        data.update(metadata)
        return self.request("record.create", {"record_type": "task", "metadata": data, "body": "Keep this goal and next action.\n"}, [])

    @unittest.skipUnless(os.name == "nt", "Windows long receipt path")
    def test_windows_long_receipt_roundtrip(self):
        root = self.folder / "long-project"
        while len(str(root / ".game-workflow-io/operations" / ("x" * 64 + ".json"))) < 290:
            root /= "segment-0123456789"
        shutil.copytree(FIXTURE, root)
        api = Workflow(root)
        context = {"project_root": str(root), "base_dir": str(root / "game-workflow")}
        request = self.task_create()
        request["context"] = context
        first = self.run_request(request, api=api)
        self.assertEqual(first["receipt"]["phase"], "settled")
        replay = self.run_request(request, api=api)
        self.assertTrue(replay["replayed"])
        identity = first["receipt"]["allocations"][0]["ref"]["id"]
        read = self.request("record.read", {"target": {"id": identity}}, context=context)
        self.assertEqual(self.run_request(read, api=api)["data"]["metadata"]["id"], identity)
        receipts = list((root / ".game-workflow-io/operations").glob("*.json"))
        self.assertEqual(len(receipts), 1)
        self.assertGreater(len(str(receipts[0])), 260)

    def test_read_inspect_raw_and_no_read_side_effects(self):
        self.run_request(self.request("workspace.inspect", {}))
        task = self.read({"id": "T-002"})
        self.assertEqual(task["metadata"]["id"], "T-002")
        self.assertEqual(Path(task["reference_base"]), self.root / "game-workflow/tasks")
        legacy = self.read({"path": "../legacy/.trellis/tasks/04-21-old/task.json"})
        self.assertEqual(legacy["interpretation"], "raw")
        self.assertEqual(legacy["capabilities"], ["record.read"])
        self.assertFalse((self.root / ".game-workflow-io").exists())

    def test_create_replay_and_request_id_conflict(self):
        request = self.task_create()
        first = self.run_request(request)
        second = self.run_request(request)
        self.assertTrue(second["replayed"])
        self.assertEqual(first["receipt"]["allocations"], second["receipt"]["allocations"])
        self.assertEqual(len(list((self.root / "game-workflow/tasks").glob("*.md"))), 3)
        request["payload"]["metadata"]["title"] = "Different work"
        conflict = self.run_request(request, "conflict")
        self.assertEqual(conflict["errors"][0]["code"], "request_id_conflict")
        self.assertNotIn("receipt", conflict)

    def test_stale_source_and_null_does_not_skip(self):
        path = self.root / "game-workflow/tasks/T-002-feedback.md"
        condition = self.condition("tasks/T-002-feedback.md")
        path.write_bytes(path.read_bytes() + b"\nExternal edit\n")
        actual = path.read_bytes()
        req = self.request("record.update", {"target": {"id": "T-002"}, "set_fields": {"title": "Changed"}, "reason": "Rename"}, [condition])
        self.run_request(req, "conflict")
        self.assertEqual(path.read_bytes(), actual)
        req["request_id"] = "null-precondition"; req["preconditions"][0]["expected_revision"] = None
        self.run_request(req, "conflict")
        self.assertEqual(path.read_bytes(), actual)

    def test_update_preserves_bom_crlf_comments_and_body(self):
        path = self.root / "game-workflow/tasks/T-002-feedback.md"
        text = path.read_text(encoding="utf-8").replace('title:', '# Important original comment\ntitle:', 1)
        path.write_bytes(b"\xef\xbb\xbf" + text.replace("\n", "\r\n").encode("utf-8"))
        before_body = self.read({"id": "T-002"})["body"]
        req = self.request("record.update", {"target": {"id": "T-002"}, "set_fields": {"title": "中文：带引号 ' 与 #"}, "reason": "Rename"}, [self.condition("tasks/T-002-feedback.md")])
        self.run_request(req)
        data = path.read_bytes()
        self.assertTrue(data.startswith(b"\xef\xbb\xbf"))
        self.assertIn(b"# Important original comment\r\n", data)
        self.assertNotIn(b"\n", data.replace(b"\r\n", b""))
        self.assertEqual(before_body, self.read({"id": "T-002"})["body"])

    def test_lifecycle_owner_and_transition_reason(self):
        bad = self.request("record.update", {"target": {"id": "T-002"}, "set_fields": {"status": "closed"}, "reason": "Bypass"}, [self.condition("tasks/T-002-feedback.md")])
        self.run_request(bad, "rejected")
        req = self.request("record.transition", {"target": {"id": "T-002"}, "to": "closed", "reason": "Fixture-only caller judgment; not real game acceptance."}, [self.condition("tasks/T-002-feedback.md")])
        self.run_request(req)
        task = self.read({"id": "T-002"})
        self.assertEqual(task["metadata"]["status"], "closed")
        self.assertIn("Fixture-only caller judgment", task["body"])
        self.assertEqual(self.read({"id": "E-001"})["metadata"]["status"], "active")

    def test_raw_write_rejected_and_preserved(self):
        path = self.root / "legacy/.trellis/tasks/04-21-old/task.json"
        before = path.read_bytes()
        req = self.request("record.update", {"target": {"path": str(path)}, "set_fields": {"status": "closed"}, "reason": "No adapter"}, [{"target": {"path": str(path)}, "expected_revision": revision(before)}])
        result = self.run_request(req, "rejected")
        self.assertEqual(result["errors"][0]["code"], "unsupported_write")
        self.assertTrue(all(w["status"] == "not_attempted" for w in result["writes"]))
        self.assertEqual(before, path.read_bytes())

    def test_scope_and_reserved_paths(self):
        req = self.task_create()
        req["context"]["project_root"] = str(self.folder)
        self.run_request(req, "rejected")
        req = self.request("record.read", {"target": {"path": "../../outside.txt"}})
        self.run_request(req, "rejected")
        req = self.request("record.read", {"target": {"path": "../.git/config"}})
        self.run_request(req, "rejected")

    def test_list_cursor_staleness_and_no_false_complete(self):
        query = self.request("record.list", {"types": ["task"], "limit": 1})
        first = self.run_request(query)["data"]
        self.assertFalse(first["complete"])
        self.assertIsNotNone(first["next_cursor"])
        self.run_request(self.task_create())
        query["request_id"] = "next-page"; query["payload"]["cursor"] = first["next_cursor"]
        response = self.run_request(query, "conflict")
        self.assertEqual(response["errors"][0]["code"], "stale_cursor")

    def extraction(self):
        return self.request("record.extract", {"target": {"id": "EV-001"}, "destination": "evidence/EV-001.md"},
                            [self.condition("tasks/T-001-copy.md"), self.condition("evidence/EV-001.md")])

    def test_extract_preserves_identity_and_rebases_refs(self):
        req = self.extraction()
        req["payload"]["destination"] = "evidence/extracted/EV-001.md"
        req["preconditions"][1] = self.condition("evidence/extracted/EV-001.md")
        self.run_request(req)
        record = self.read({"id": "EV-001"})
        self.assertEqual(Path(record["path"]), self.root / "game-workflow/evidence/extracted/EV-001.md")
        self.assertIn("workflow:forward EV-001", self.read({"id": "T-001"})["body"])
        resolved = self.run_request(self.request("record.resolve", {"target": {"path": "tasks/T-001-copy.md", "fragment": "EV-001"}}))["data"]
        self.assertEqual(resolved["ref"], {"id": "EV-001"})
        proof = record["metadata"]["subjects"][0]["ref"]["path"]
        self.assertEqual(proof, "../../../fixtures/copy.json")
        self.assertTrue((Path(record["reference_base"]) / proof).is_file())

    def test_extract_missing_actual_source_condition(self):
        req = self.extraction()
        req["preconditions"][0] = self.condition("tasks/T-002-feedback.md")
        self.run_request(req, "rejected")
        self.assertFalse((self.root / "game-workflow/evidence/EV-001.md").exists())

    def test_crash_after_replace_then_query_and_resume(self):
        req = self.extraction()
        code = """import json,os,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from workflow_io import Workflow
def crash(stage,value):
 if stage=='after_replace:0': os._exit(73)
Workflow(sys.argv[2],fault=crash).execute(json.loads(Path(sys.argv[3]).read_text(encoding='utf-8')))
"""
        request_path = self.folder / "crash.request.json"
        request_path.write_text(json.dumps(req), encoding="utf-8")
        proc = subprocess.run([sys.executable, "-c", code, str(CLI.parent), str(self.root), str(request_path)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 73, proc.stderr)
        status = self.run_request(self.request("operation.status", {"request_id": req["request_id"]}))
        self.assertEqual(status["receipt"]["outcome"], "partial")
        self.assertEqual(status["writes"][0]["status"], "unchanged")
        self.assertIn("does not prove", status["writes"][0]["note"])
        self.assertEqual(status["writes"][1]["status"], "not_attempted")
        self.run_request(req)
        self.assertIn("workflow:forward EV-001", self.read({"id": "T-001"})["body"])

    def test_create_crash_reserves_id_across_restart(self):
        req = self.task_create()
        def fault(stage, value):
            if stage == "prepared":
                raise OSError("Simulated unavailable writer")
        interrupted = self.run_request(req, "indeterminate", Workflow(self.root, fault=fault))
        allocated = interrupted["receipt"]["allocations"][0]["ref"]["id"]
        recovered = self.run_request(req, api=Workflow(self.root))
        self.assertEqual(recovered["receipt"]["allocations"][0]["ref"]["id"], allocated)
        self.assertEqual(self.read({"id": allocated})["metadata"]["title"], "New task")

    def test_concurrent_process_creation_and_same_request(self):
        request_paths = []
        for index in range(6):
            req = self.task_create(title=f"Concurrent {index}")
            path = self.folder / f"request-{index}.json"
            path.write_text(json.dumps(req), encoding="utf-8")
            request_paths.append(path)
        def launch(path):
            return subprocess.Popen([sys.executable, str(CLI), "--project-root", str(self.root), "--request", str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        processes = [launch(path) for path in request_paths]
        results = []
        for process in processes:
            output, error = process.communicate(timeout=30)
            self.assertEqual(process.returncode, 0, output + error)
            results.append(json_load(output))
        ids = [r["receipt"]["allocations"][0]["ref"]["id"] for r in results]
        self.assertEqual(len(set(ids)), 6)
        duplicate = [launch(request_paths[0]) for _ in range(3)]
        for process in duplicate:
            output, error = process.communicate(timeout=30)
            self.assertEqual(process.returncode, 0, output + error)
            self.assertTrue(json_load(output)["replayed"])

    def decision_request(self, actor=None, target=True):
        event = {"event_id": "e2", "decided_at": None, "recorded_at": "2026-09-22T00:00:00Z",
                 "actor": actor or {"kind": "agent", "id": "local-cli"}, "action": "withdraw",
                 "subjects": copy.deepcopy(self.read({"id": "D-001"})["metadata"]["events"][0]["subjects"][-1:]),
                 "scope": "Only battle-b", "conclusion": "Fixture-only B withdrawal", "replaces": [{"id": "D-001", "fragment": "e1"}]}
        payload = {"event": event, "target": {"id": "D-001"}} if target else {"event": event, "title": "New decision"}
        req = self.request("decision.record", payload, [self.condition("decisions/D-001-flash.json.md")])
        path = Path(self.read({"id": "D-001"})["path"])
        req["context"]["base_dir"] = str(path.parent)
        req["preconditions"] = [{"target": {"path": str(path)}, "expected_revision": revision(path.read_bytes())}] if target else []
        return req

    def test_decision_actor_binding_append_only_and_partial_scope(self):
        request = self.decision_request({"kind": "user", "id": "fixture-user"})
        self.run_request(request, "rejected")
        trusted = Workflow(self.root, decision_authorizer=lambda event, req: event["actor"] == {"kind": "user", "id": "fixture-user"})
        result = self.run_request(request, api=trusted)
        data = self.read({"id": "D-001"})
        self.assertEqual(len(data["metadata"]["events"]), 2)
        self.assertNotEqual(data["metadata"]["events"][1]["recorded_at"], "2026-09-22T00:00:00Z")
        path = Path(data["path"])
        overwrite = self.request("record.update", {"target": {"id": "D-001"}, "set_fields": {"events": []}, "reason": "Erase"}, [{"target": {"path": str(path)}, "expected_revision": revision(path.read_bytes())}])
        self.run_request(overwrite, "rejected")
        self.assertEqual(len(self.read({"id": "D-001"})["metadata"]["events"]), 2)

    def test_decision_bad_event_and_unknown_scope(self):
        request = self.decision_request()
        request["payload"]["event"]["replaces"][0]["fragment"] = "missing"
        self.run_request(request, "rejected")
        request = self.decision_request()
        request["payload"]["event"]["subjects"][0].pop("use")
        self.run_request(request, "rejected")

    def test_asset_clear_keeps_candidate_decision_and_engine(self):
        engine = (self.root / "game/consumers.json").read_bytes()
        decision = Path(self.read({"id": "D-001"})["path"]).read_bytes()
        req = self.request("asset.select", {"ledger": {"path": "assets/ledger.yaml"}, "asset_id": "A-001", "action": "clear", "use_id": "use-b", "reason": "Clear only B"}, [self.condition("assets/ledger.yaml")])
        self.run_request(req)
        asset = self.read({"id": "A-001"})["metadata"]
        self.assertEqual([u["use_id"] for u in asset["selected_uses"]], ["use-a"])
        self.assertEqual(len(asset["candidates"]), 1)
        self.assertEqual((self.root / "game/consumers.json").read_bytes(), engine)
        self.assertEqual(Path(self.read({"id": "D-001"})["path"]).read_bytes(), decision)

    def test_asset_set_checks_member_bytes_not_only_manifest(self):
        asset = self.read({"id": "A-001"})["metadata"]
        req = self.request("asset.select", {"ledger": {"path": "assets/ledger.yaml"}, "asset_id": "A-001", "action": "set", "use": asset["selected_uses"][0], "reason": "Select A"}, [self.condition("assets/ledger.yaml")])
        self.run_request(req)
        media = self.root / "assets/flash/flash.json"
        media.write_bytes(media.read_bytes() + b" ")
        req["request_id"] = "new-media-check"; req["preconditions"] = [self.condition("assets/ledger.yaml")]
        response = self.run_request(req, "conflict")
        self.assertEqual(response["errors"][0]["code"], "version_mismatch")

    def test_asset_create_update_ownership(self):
        req = self.request("asset.upsert", {"ledger": {"path": "assets/ledger.yaml"}, "mode": "create", "asset": {"title": "Unproduced asset", "purpose": "Future actual tracked output", "candidates": [], "selected_uses": []}, "reason": "Register"}, [self.condition("assets/ledger.yaml")])
        made = self.run_request(req)
        rid = made["data"]["ref"]["id"]
        metadata = self.read({"id": rid})["metadata"]
        metadata["title"] = "Renamed"
        req = self.request("asset.upsert", {"ledger": {"path": "assets/ledger.yaml"}, "mode": "update", "asset": metadata, "reason": "Rename"}, [self.condition("assets/ledger.yaml")])
        self.run_request(req)
        self.assertEqual(self.read({"id": rid})["metadata"]["title"], "Renamed")

    def test_evidence_and_container_cannot_rewrite_facts(self):
        record = self.read({"id": "EV-001"})
        task = self.read({"id": "T-001"})
        body = task["body"].replace("result: passed", "result: failed")
        self.assertNotEqual(body, task["body"])
        req = self.request("record.update", {"target": {"id": "T-001"}, "body": body, "reason": "Rewrite evidence"}, [self.condition("tasks/T-001-copy.md")])
        self.run_request(req, "rejected")
        self.assertEqual(self.read({"id": "EV-001"})["metadata"]["result"], "passed")

    def test_derived_views_do_not_close_epic_or_claim_adoption(self):
        result = self.run_request(self.request("view.build", {"view": "assets"}, []))
        self.assertNotIn("receipt", result)
        self.assertEqual(result["data"]["entries"][0]["runtime_adoption"], "unknown")
        req = self.request("view.build", {"view": "progress", "output_path": "views/progress.json"}, [self.condition("views/progress.json")])
        self.run_request(req)
        data = json_load((self.root / "game-workflow/views/progress.json").read_text(encoding="utf-8"))
        self.assertNotIn("completion_percent", data)
        self.assertEqual(self.read({"id": "E-001"})["metadata"]["status"], "active")

    def test_workspace_configure_and_attachment(self):
        path = self.root / "game-workflow/workspace.yaml"
        mapping = yaml_load(path.read_text(encoding="utf-8"))
        mapping["project"]["name"] = "New display name"
        req = self.request("workspace.configure", {"document": plain(mapping)}, [self.condition("workspace.yaml")])
        self.run_request(req)
        req = self.request("record.create", {"record_type": "design", "owner": {"id": "T-002"}, "body": "# Design\nOriginal work: T-002\n"}, [])
        self.run_request(req)
        self.assertTrue((self.root / "game-workflow/tasks/T-002/design.md").is_file())
        self.assertEqual(self.read({"id": "T-002"})["metadata"]["status"], "active")

    def test_attachment_creation_uses_registered_reader_before_write(self):
        for kind in ("design", "plan", "history"):
            with self.subTest(kind=kind):
                path = f"tasks/T-002/m0-{kind}.md"
                req = self.request("record.create", {"record_type": kind, "owner": {"id": "T-002"},
                                   "path": path, "body": "# Stage attachment\n"}, [self.condition(path)])
                result = self.run_request(req, "rejected")
                self.assertEqual(result["errors"][0]["code"], "invalid_record")
                self.assertFalse((self.root / "game-workflow" / path).exists())
                self.assertNotIn("receipt", result)
        listing = self.run_request(self.request("record.list", {"limit": 100}))
        self.assertFalse(any(x["code"] == "invalid_record" for x in listing["data"]["diagnostics"]))
        created = self.run_request(self.task_create())
        self.assertEqual(created["data"]["ref"]["id"], "T-003")

    def test_stage_attachment_roundtrip_and_later_allocation(self):
        for kind in ("design", "plan", "history"):
            path = f"tasks/T-002/m0/{kind}.md"
            body = f"# M0 {kind}\nOriginal work remains T-002.\n"
            req = self.request("record.create", {"record_type": kind, "owner": {"id": "T-002"},
                               "path": path, "body": body}, [self.condition(path)])
            self.run_request(req)
            first = self.read({"path": path})
            self.assertEqual(first["body"], body)
            self.assertIsNone(first["metadata"])
            req = self.request("record.update", {"target": {"path": path}, "body": body + "Updated.\n",
                               "reason": "Update only the stage attachment."}, [self.condition(path)])
            self.run_request(req)
            self.assertEqual(self.read({"path": path})["body"], body + "Updated.\n")
        listing = self.run_request(self.request("record.list", {"limit": 100}))
        self.assertFalse(any(x["code"] == "invalid_record" for x in listing["data"]["diagnostics"]))
        self.assertEqual(self.read({"id": "T-002"})["metadata"]["status"], "active")
        self.assertEqual(self.run_request(self.task_create())["data"]["ref"]["id"], "T-003")

    def test_binary_version_subject(self):
        path = self.root / "fixtures/picture.png"
        path.write_bytes(b"\x89PNG\r\n\x1a\n\xff\x00")
        req = self.task_create()
        req["expected_subjects"] = [{"ref": {"path": "../fixtures/picture.png"}, "scope": "fixture bytes", "version": {"kind": "sha256", "value": revision(path.read_bytes())[7:]}}]
        self.run_request(req)

    def test_partial_extract_external_edit_and_explicit_repair(self):
        req = self.extraction()
        def stop(stage, value):
            if stage == "after_write:0":
                raise OSError("Simulated pause after first file")
        self.run_request(req, "partial", Workflow(self.root, fault=stop))
        source = self.root / "game-workflow/tasks/T-001-copy.md"
        source.write_bytes(source.read_bytes() + b"\nUser-added context must survive.\n")
        result = self.run_request(req, "partial")
        self.assertEqual(result["receipt"]["phase"], "settled")
        repair = self.request("record.extract", {"target": {"path": "tasks/T-001-copy.md", "fragment": "EV-001"},
                    "destination": "evidence/EV-001.md", "recovery_of": req["request_id"]},
                    [self.condition("tasks/T-001-copy.md"), self.condition("evidence/EV-001.md")])
        self.run_request(repair)
        self.assertIn(b"User-added context must survive.", source.read_bytes())
        self.assertEqual(Path(self.read({"id": "EV-001"})["path"]), self.root / "game-workflow/evidence/EV-001.md")

    def test_document_rebase_leaves_code_examples_and_moves_real_links(self):
        source = self.root / "game-workflow/tasks/T-001-copy.md"
        text = source.read_text(encoding="utf-8")
        added = '\n[real](../../fixtures/copy.json)\n```md\n[example](../../fixtures/copy.json)\n```\n'
        text = text.replace('<!-- workflow:endrecord EV-001 -->', added + '<!-- workflow:endrecord EV-001 -->')
        source.write_text(text, encoding="utf-8")
        req = self.extraction(); req["payload"]["destination"] = "evidence/deep/EV-001.md"
        req["preconditions"][1] = self.condition("evidence/deep/EV-001.md")
        self.run_request(req)
        body = self.read({"id": "EV-001"})["body"]
        self.assertIn('[real](../../../fixtures/copy.json)', body)
        self.assertIn('[example](../../fixtures/copy.json)', body)

    def test_duplicate_identity_in_creation_body_is_rejected(self):
        request = self.task_create()
        task = self.read({"id": "T-001"})
        request["payload"]["body"] = task["body"]
        self.run_request(request, "rejected")
        self.assertEqual(self.read({"id": "EV-001"})["metadata"]["result"], "passed")

    def test_custom_view_location_and_authority_protection(self):
        req = self.request("view.build", {"view": "progress", "output_path": "../views/progress.json"}, [self.condition("../views/progress.json")])
        self.run_request(req)
        self.assertTrue((self.root / "views/progress.json").exists())
        req = self.request("view.build", {"view": "progress", "output_path": "../legacy/.trellis/tasks/04-21-old/task.json"}, [self.condition("../legacy/.trellis/tasks/04-21-old/task.json")])
        self.run_request(req, "rejected")

    def test_new_project_inspect_then_create_and_map(self):
        fresh = self.folder / "new-project"
        fresh.mkdir()
        api = Workflow(fresh)
        req = self.request("workspace.inspect", {})
        req["context"] = {"project_root": str(fresh)}
        result = self.run_request(req, api=api)
        self.assertFalse(result["data"]["configured"])
        self.assertEqual(list(fresh.iterdir()), [])
        req = self.task_create()
        req["context"] = {"project_root": str(fresh)}
        result = self.run_request(req, api=api)
        self.assertEqual(result["data"]["ref"]["id"], "T-001")
        req = self.request("workspace.configure", {"document": {"schema_version":1,"project":{"id":"fresh","name":"Fresh","root":".."},"runtime_roots":[],
             "sources":[{"id":"tasks","role":"task","kind":"collection","path":"tasks","owner":"flow","format":"native-markdown-v1"}],
             "default_task_source":"tasks","default_epic_source":None,"rule_sources":[]}},
             [{"target":{"path":"game-workflow/workspace.yaml"},"expected_revision":None}])
        req["context"] = {"project_root": str(fresh)}
        self.run_request(req, api=api)

    def test_local_junction_is_rejected(self):
        target = self.folder / "outside"
        target.mkdir(); (target / "secret.txt").write_text("outside fixture", encoding="utf-8")
        link = self.root / "linked"
        if os.name == "nt":
            import _winapi
            _winapi.CreateJunction(str(target), str(link))
        else:
            link.symlink_to(target, target_is_directory=True)
        req = self.request("record.read", {"target": {"path": "../linked/secret.txt"}})
        result = self.run_request(req, "rejected")
        self.assertEqual(result["errors"][0]["code"], "invalid_scope")

    def test_embedded_evidence_creation_and_cross_decision_replacement(self):
        evidence = copy.deepcopy(self.read({"id": "EV-001"})["metadata"])
        evidence.pop("id")
        request = self.request("record.create", {"record_type":"evidence","metadata":evidence,"body":"New fixture observation.",
            "storage":"embedded","container":{"id":"T-002"}}, [self.condition("tasks/T-002-feedback.md")])
        request["context"]["base_dir"] = str(self.root / "game-workflow/tasks")
        request["preconditions"] = [{"target":{"path":"T-002-feedback.md"},"expected_revision":revision((self.root/'game-workflow/tasks/T-002-feedback.md').read_bytes())}]
        created = self.run_request(request)
        self.assertEqual(Path(self.read(created["data"]["ref"])["path"]), self.root/'game-workflow/tasks/T-002-feedback.md')
        request = self.decision_request(target=False)
        created = self.run_request(request)
        self.assertNotEqual(created["data"]["ref"]["id"], "D-001")
        self.assertEqual(len(self.read({"id":"D-001"})["metadata"]["events"]),1)

    def test_capabilities_and_required_metadata(self):
        asset = self.read({"id":"A-001"})
        self.assertNotIn("record.update",asset["capabilities"])
        self.assertIn("asset.select",asset["capabilities"])
        path = self.root/'game-workflow/tasks/T-900-broken.md'
        path.write_text('# Missing metadata\n',encoding='utf-8')
        result = self.run_request(self.request('record.read',{'target':{'path':'tasks/T-900-broken.md'}}),'rejected')
        self.assertEqual(result['errors'][0]['code'],'invalid_record')

    def test_optional_marker_and_extension_payload_are_preserved(self):
        path=self.root/'game-workflow/workspace.yaml'
        workspace=yaml_load(path.read_text(encoding='utf-8'));workspace['runtime_roots'][0].pop('marker')
        self.run_request(self.request('workspace.configure',{'document':plain(workspace)},[self.condition('workspace.yaml')]))
        request=self.task_create(extensions={'custom':{'path':'this-is-domain-data-not-a-file'},'another':{'id':'business-identifier'}})
        created=self.run_request(request)
        self.assertEqual(self.read(created['data']['ref'])['metadata']['extensions'],request['payload']['metadata']['extensions'])

    def test_candidate_subject_uses_its_bound_manifest(self):
        candidate=self.read({'id':'A-001'})['metadata']['candidates'][0]
        req=self.task_create()
        req['expected_subjects']=[{'ref':{'id':'A-001'},'candidate_id':'C-001','version':candidate['version'],'scope':'Content checks'}]
        self.run_request(req)

    def test_source_qualifier_cannot_point_into_another_source(self):
        req=self.request('record.read',{'target':{'path':'tasks/T-002-feedback.md','source':'legacy-trellis'}})
        result=self.run_request(req,'rejected')
        self.assertEqual(result['errors'][0]['code'],'invalid_scope')

    def test_complete_is_separate_from_identity_diagnostics(self):
        path=self.root/'game-workflow/workspace.yaml'
        workspace=yaml_load(path.read_text(encoding='utf-8'))
        workspace['sources']=[s for s in workspace['sources'] if s['id']!='legacy-trellis']
        path.write_text(yaml_dump(workspace),encoding='utf-8')
        source=self.root/'game-workflow/tasks/T-002-feedback.md'
        (source.parent/'T-002-duplicate.md').write_bytes(source.read_bytes())
        result=self.run_request(self.request('record.list',{}))['data']
        self.assertTrue(result['complete'])
        self.assertIn('duplicate_id',{d['code'] for d in result['diagnostics']})

    def test_receipt_save_failure_reports_actual_partial_write(self):
        req=self.task_create()
        original=Store.save; counter=0
        def failing(store,value):
            nonlocal counter
            counter+=1
            if counter>=3:
                raise OSError('Simulated receipt storage failure')
            return original(store,value)
        with patch.object(Store,'save',failing):
            result=self.run_request(req,'partial')
        self.assertEqual(result['writes'][0]['status'],'written')
        self.assertTrue(Path(result['writes'][0]['target']['path']).exists())
        self.assertIn('indeterminate',{e['code'] for e in result['errors']})
        self.run_request(req)

    def test_saved_write_reverted_is_not_overwritten_on_recovery(self):
        source=self.root/'game-workflow/tasks/T-002-feedback.md'
        before=source.read_bytes()
        req=self.request('record.update',{'target':{'id':'T-002'},'set_fields':{'title':'Changed'},'reason':'Fixture change'},[self.condition('tasks/T-002-feedback.md')])
        def stop(stage,value):
            if stage=='after_write:0': raise OSError('Stop after durable written marker')
        self.run_request(req,'partial',Workflow(self.root,fault=stop))
        source.write_bytes(before)
        queried=self.run_request(self.request('operation.status',{'request_id':req['request_id']}))
        self.assertEqual(queried['writes'][0]['status'],'failed')
        self.run_request(req,'conflict')
        self.assertEqual(source.read_bytes(),before)

    def test_matching_external_content_does_not_claim_write_authorship(self):
        req=self.task_create()
        def stop(stage,value):
            if stage=='prepared': raise OSError('Stop before replacing files')
        result=self.run_request(req,'indeterminate',Workflow(self.root,fault=stop))
        receipt_path=next((self.root/'.game-workflow-io/operations').glob('*.json'))
        data=json_load(filesystem_path(receipt_path).read_text(encoding='utf-8'))
        import base64
        target=Path(data['plans'][0]['path']);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(base64.b64decode(data['plans'][0]['content']))
        queried=self.run_request(self.request('operation.status',{'request_id':req['request_id']}))
        self.assertEqual(queried['writes'][0]['status'],'unchanged')
        self.assertIn('does not prove',queried['writes'][0]['note'])
        replayed=self.run_request(req)
        self.assertEqual(replayed['writes'][0]['status'],'unchanged')

    def test_withdrawal_cannot_change_the_accepted_version(self):
        req=self.decision_request()
        req['payload']['event']['subjects'][0]['version']['value']='a'*64
        response=self.run_request(req,'rejected')
        self.assertEqual(response['errors'][0]['code'],'invalid_scope')

    def test_current_decision_subjects_match_current_review_preconditions(self):
        req=self.decision_request()
        req['expected_subjects']=copy.deepcopy(req['payload']['event']['subjects'])
        req['expected_subjects'][0]['scope']='Some other review scope'
        response=self.run_request(req,'rejected')
        self.assertEqual(response['errors'][0]['code'],'invalid_scope')

    def test_malformed_cli_input_is_a_controlled_error(self):
        for content in ('[]','{"request_id":"x","operation":"unknown"}','{"request_id":"x","operation":[]}','{"a":1,"a":2}'):
            process=subprocess.run([sys.executable,str(CLI),'--project-root',str(self.root)],input=content,
                                   capture_output=True,text=True,encoding='utf-8',timeout=20)
            self.assertEqual(process.returncode,2,process.stderr)
            self.assertEqual(json_load(process.stdout)['status'],'rejected')
            self.assertNotIn('Traceback',process.stderr)

    def test_pending_operation_is_separate_from_scan_completeness(self):
        path=self.root/'game-workflow/workspace.yaml'
        mapping=yaml_load(path.read_text(encoding='utf-8'))
        mapping['sources']=[s for s in mapping['sources'] if s['id']!='legacy-trellis']
        path.write_text(yaml_dump(mapping),encoding='utf-8')
        request=self.task_create()
        def stop(stage,value):
            if stage=='prepared': raise OSError('Pause before source creation')
        self.run_request(request,'indeterminate',Workflow(self.root,fault=stop))
        data=self.run_request(self.request('record.list',{}))['data']
        self.assertTrue(data['complete'])
        self.assertIn('operation_pending',{d['code'] for d in data['diagnostics']})

    def test_add_first_ledger_to_an_already_mapped_project(self):
        fresh=self.folder/'mapped-project';home=fresh/'game-workflow';home.mkdir(parents=True)
        mapping={'schema_version':1,'project':{'id':'mapped','name':'Mapped','root':'..'},'runtime_roots':[],
                 'sources':[{'id':'tasks','role':'task','kind':'collection','path':'tasks','owner':'flow','format':'native-markdown-v1'}],
                 'default_task_source':'tasks','default_epic_source':None,'rule_sources':[]}
        workspace=home/'workspace.yaml';workspace.write_text(yaml_dump(mapping),encoding='utf-8')
        api=Workflow(fresh)
        req=self.request('asset.upsert',{'ledger':{'path':'assets/ledger.yaml'},'mode':'create',
            'asset':{'title':'First tracked asset','purpose':'Actual output','candidates':[],'selected_uses':[]},'reason':'Register first asset'},
            [{'target':{'path':'assets/ledger.yaml'},'expected_revision':None}])
        req['context']={'project_root':str(fresh),'base_dir':str(home)}
        created=self.run_request(req,api=api)
        self.assertTrue(created['data']['source_registration_required'])
        self.assertEqual(yaml_load(workspace.read_text(encoding='utf-8'))['sources'],mapping['sources'])
        mapping['sources'].append(created['data']['source_proposal'])
        configure=self.request('workspace.configure',{'document':mapping},[{'target':{'path':'workspace.yaml'},'expected_revision':revision(workspace.read_bytes())}])
        configure['context']=req['context']
        self.run_request(configure,api=api)
        read=self.request('record.read',{'target':created['data']['ref']});read['context']=req['context']
        self.assertEqual(self.run_request(read,api=api)['data']['metadata']['title'],'First tracked asset')

    def test_overlapping_external_source_cannot_reuse_cached_native_writer(self):
        path=self.root/'game-workflow/workspace.yaml';mapping=yaml_load(path.read_text(encoding='utf-8'))
        mapping['sources'].append({'id':'overlap-external','role':'task','kind':'file','path':'tasks/T-002-feedback.md','owner':'legacy','format':'external'})
        path.write_text(yaml_dump(mapping),encoding='utf-8')
        target=self.root/'game-workflow/tasks/T-002-feedback.md';before=target.read_bytes()
        req=self.request('record.update',{'target':{'path':'tasks/T-002-feedback.md','source':'overlap-external'},
            'set_fields':{'title':'Wrong owner'},'reason':'Must not borrow native capability'},[self.condition('tasks/T-002-feedback.md')])
        self.run_request(req,'rejected')
        self.assertEqual(target.read_bytes(),before)


if __name__ == "__main__":
    import importlib.metadata
    import platform
    from datetime import datetime, timezone
    class ArtifactResult(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.cases = []
        def stopTest(self, test):
            failed = any(item[0] is test for item in self.failures + self.errors)
            self.cases.append({"test":test.id(), "status":"failed" if failed else "passed", "artifacts":str(getattr(test,"folder",""))})
            super().stopTest(test)
    program=unittest.main(verbosity=2,exit=False,testRunner=unittest.TextTestRunner(verbosity=2,resultclass=ArtifactResult))
    result=program.result
    report={"time":datetime.now(timezone.utc).isoformat(),"python":sys.version,"platform":platform.platform(),
            "dependencies":{name:importlib.metadata.version(name) for name in ('PyYAML','jsonschema','ruamel.yaml')},
            "ran":result.testsRun,"failures":len(result.failures),"errors":len(result.errors),"skipped":len(result.skipped),"cases":result.cases}
    stamp=datetime.fromisoformat(report['time']).strftime('%Y%m%dT%H%M%S.%fZ')
    target=RUN_ROOT/f'run-{stamp}-{os.getpid()}.json'
    with target.open('x',encoding='utf-8') as handle:
        handle.write(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (RUN_ROOT/'latest-run.json').write_text(json.dumps({'report':target.name})+'\n',encoding='utf-8')
    print(f'Report: {target}')
    raise SystemExit(0 if result.wasSuccessful() else 1)
