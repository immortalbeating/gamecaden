"""HTTP-to-filesystem integration tests. Only disposable fixture copies are written."""
from __future__ import annotations
import copy
import hashlib
import http.client
import json
from pathlib import Path
import shutil
import tempfile
import threading
import unittest

from workflow_formats import yaml_load, yaml_dump
from workflow_panel_server import create_server

BUNDLE = (Path(__file__).resolve().parents[1] / "plugins" / "gamecaden")
RUNS = BUNDLE.parents[1] / "work/panel-bridge-eval/tests"
PNG = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000b49444154789c636000020000050001a5f645400000000049454e44ae426082")


class BridgeTests(unittest.TestCase):
    def setUp(self):
        RUNS.mkdir(parents=True, exist_ok=True)
        self.folder = Path(tempfile.mkdtemp(prefix=self._testMethodName[5:25] + "-", dir=RUNS))
        self.root = self.folder / "project"
        shutil.copytree(BUNDLE / "examples/v1/project", self.root)
        self.config = {"version": 1, "projects": [
            {"id": "lab", "root": str(self.root), "name": "隔离测试",
             "write": {"task_body": True, "decisions": True, "asset_selection": True},
             "reviewer": {"kind": "tool", "id": "bridge-tests"}, "identity_source": "test-fixture"},
            {"id": "old", "root": str(self.root), "name": "旧格式",
             "external_sources": [{"id": "vision", "label": "原文", "role": "vision", "path": "game-workflow/vision.md"}]}
        ]}
        self.server = None
        self.start()
        self.addCleanup(self.stop)

    def start(self):
        self.server = create_server(self.config, self.folder / "host", port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": .01}, daemon=True)
        self.thread.start()
        self.cookie = ""
        self.csrf = ""
        self.origin = self.server.host.origin
        self.connect()

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(2)
            self.server = None

    def request(self, method, path, body=None, *, headers=None, cookie=True, csrf=True):
        h = {"Origin": self.origin}
        if cookie:
            h["Cookie"] = self.cookie
        if csrf:
            h["X-CSRF-Token"] = self.csrf
        if body is not None:
            h["Content-Type"] = "application/json"
            raw = json.dumps(body, ensure_ascii=False).encode()
        else:
            raw = None
        h.update(headers or {})
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=8)
        conn.request(method, path, body=raw, headers=h)
        response = conn.getresponse()
        status, response_headers, data = response.status, dict(response.getheaders()), response.read()
        conn.close()
        if response_headers.get("Content-Type", "").startswith("application/json"):
            data = json.loads(data)
        return status, response_headers, data

    def connect(self):
        status, headers, data = self.request("POST", "/api/connect", {"token": self.server.host.bootstrap}, csrf=False, cookie=False)
        self.assertEqual(status, 200, data)
        self.cookie = headers["Set-Cookie"].split(";")[0]
        self.csrf = data["csrf_token"]
        return data

    def get(self, path):
        status, _, data = self.request("GET", "/api/projects/lab/" + path)
        self.assertEqual(status, 200, data)
        return data

    def post(self, path, body, expected=200, project="lab"):
        status, _, data = self.request("POST", "/api/projects/" + project + "/" + path, body)
        self.assertEqual(status, expected, data)
        return data

    def row(self, kind):
        return next(r for r in self.get("snapshot")["records"] if r["record_type"] == kind)

    def task(self):
        return self.get("records/" + self.row("task")["key"])

    def prepare_task(self):
        task = self.task()
        ticket = self.post("task/prepare", {"key": task["key"], "revision": task["revision"]})["ticket"]
        return task, ticket

    def review(self, rid="review-1", use="use-a", candidate="C-001"):
        asset = self.row("asset")
        detail = self.get("candidates/" + asset["key"] + "/" + candidate)
        payload = {"asset_key": asset["key"], "candidate_id": candidate,
                   "expected_revision": detail["ledger_revision"], "expected_version": detail["version"],
                   "scope": "隔离测试中的外观范围", "use_id": use}
        prepared = self.post("review/prepare", payload)
        return {"ticket": prepared["ticket"], "request_id": rid, "conclusion": "revise",
                "note": "自动化集成测试；不是游戏或用户的视觉验收。"}

    def add_candidate(self):
        manifest_path = self.root / "assets/flash/candidate-two.json"
        manifest = json.loads((self.root / "assets/flash/manifest.json").read_text())
        manifest["candidate_id"] = "C-002"
        (manifest_path.parent / "preview.png").write_bytes(PNG)
        manifest["files"].append({"path": "preview.png", "sha256": hashlib.sha256(PNG).hexdigest(), "role": "preview"})
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        ledger_path = self.root / "game-workflow/assets/ledger.yaml"
        ledger = yaml_load(ledger_path.read_text(encoding="utf-8"))
        ledger["assets"][0]["candidates"].append({"id": "C-002", "manifest": {"path": "../../assets/flash/candidate-two.json"},
                                                "version": {"kind": "sha256", "value": hashlib.sha256(manifest_path.read_bytes()).hexdigest()}})
        ledger_path.write_text(yaml_dump(ledger), encoding="utf-8")

    def test_session_origin_csrf_and_endpoint_bounds(self):
        self.assertEqual(self.request("GET", "/api/session", cookie=False)[0], 401)
        self.assertEqual(self.request("GET", "/api/session", headers={"Host": "evil.example"})[0], 403)
        self.assertEqual(self.request("GET", "/api/session", headers={"Origin": "https://evil.example"})[0], 403)
        self.assertEqual(self.request("POST", "/api/projects/lab/operation/status", {"request_id": "x"}, csrf=False)[0], 403)
        self.assertEqual(self.request("POST", "/api/connect", {"token": "reused-or-wrong"}, cookie=False, csrf=False)[0], 401)
        self.assertEqual(self.request("GET", "/api/projects/lab/records/../../.git/config")[0], 404)
        self.assertEqual(self.request("GET", "/api/projects/lab/media/unknown")[0], 404)
        self.assertEqual(self.request("GET", "/secret-config.json")[0], 404)
        self.post("execute", {"operation": "record.transition"}, expected=404)
        self.assertFalse((self.root / ".game-workflow-io").exists())

    def test_task_save_cas_replay_and_readback(self):
        task, ticket = self.prepare_task()
        request = {"ticket": ticket, "request_id": "save-1", "body": task["body"] + "\nBridge test append\n"}
        result = self.post("task/save", request)
        self.assertEqual(result["result"]["status"], "ok", result)
        self.assertEqual(result["record"]["body"], request["body"])
        replay = self.post("task/save", request)
        self.assertTrue(replay["result"]["replayed"])
        self.assertEqual(result["result"]["receipt"], replay["result"]["receipt"])
        altered = {**request, "body": request["body"] + "different"}
        self.assertEqual(self.post("task/save", altered)["result"]["status"], "conflict")
        old = {**request, "request_id": "save-stale", "body": task["body"]}
        self.assertEqual(self.post("task/save", old)["result"]["status"], "conflict")
        self.assertIn("Bridge test append", Path(task["path"]).read_text(encoding="utf-8"))

    def test_foreign_ticket_forged_actor_and_readonly(self):
        task, ticket = self.prepare_task()
        self.post("task/save", {"ticket": ticket[:-1] + ("0" if ticket[-1] != "0" else "1"),
                                "request_id": "tamper", "body": "bad"}, expected=403)
        self.post("task/save", {"ticket": ticket, "request_id": "actor", "body": "bad",
                                "actor": {"kind": "user", "id": "forged"}}, expected=400)
        self.post("task/save", {"ticket": ticket, "request_id": "root", "body": "bad",
                                "project_root": str(self.root.parent)}, expected=400)
        self.post("task/save", {"ticket": ticket, "request_id": "old", "body": "bad"}, expected=403, project="old")
        before = Path(task["path"]).read_bytes()
        self.server.host.projects["lab"].caps["task_body_write"] = False
        self.post("task/save", {"ticket": ticket, "request_id": "revoked", "body": "bad"}, expected=403)
        self.assertEqual(Path(task["path"]).read_bytes(), before)

    def test_exact_decision_scope_identity_idempotency_and_independent_failure(self):
        first = self.review()
        second = self.review("review-2", "use-b")
        success = self.post("review/commit", first)
        self.assertEqual(success["result"]["status"], "ok", success)
        event = success["record"]["metadata"]["events"][0]
        self.assertEqual(event["actor"], {"kind": "tool", "id": "bridge-tests"})
        self.assertEqual(event["subjects"][0]["use"]["consumer"], "battle-a")
        self.assertEqual(event["subjects"][0]["candidate_id"], "C-001")
        replay = self.post("review/commit", first)
        self.assertTrue(replay["result"]["replayed"])
        # One member succeeds; another now conflicts. No batch rollback or blanket success.
        ledger = self.root / "game-workflow/assets/ledger.yaml"
        ledger.write_bytes(ledger.read_bytes() + b"\n# concurrent edit\n")
        failure = self.post("review/commit", second)
        self.assertEqual(failure["result"]["status"], "conflict", failure)
        self.assertTrue(Path(success["record"]["path"]).is_file())
        self.assertEqual(len(list((self.root / "game-workflow/decisions").glob("*.md"))), 2)

    def test_recovery_preserves_request_id_and_ticket_across_restart(self):
        request = self.review("interrupted")
        def stop(stage, value):
            if stage == "prepared":
                raise OSError("isolated transport recovery fixture")
        self.server.host.projects["lab"].workflow.fault = stop
        interrupted = self.post("review/commit", request)["result"]
        self.assertEqual(interrupted["status"], "indeterminate", interrupted)
        self.assertNotEqual(interrupted["receipt"]["phase"], "settled")
        self.stop()
        self.start()
        observed = self.post("operation/status", {"request_id": "interrupted"})["result"]
        # Query status ok is not original success.
        self.assertEqual(observed["status"], "ok")
        self.assertNotEqual(observed["receipt"]["outcome"], "ok")
        replay = self.post("review/commit", request)["result"]
        self.assertEqual(replay["status"], "ok", replay)
        self.assertTrue(replay["replayed"])
        self.assertEqual(replay["receipt"]["allocations"], interrupted["receipt"]["allocations"])
        missing = self.post("operation/status", {"request_id": "missing"})["result"]
        self.assertEqual(missing["errors"][0]["code"], "not_found")

    def test_user_actor_requires_host_binding_and_exact_callback(self):
        # Synthetic fixture identity: this is not a real user acceptance.
        self.stop()
        self.config["projects"][0]["reviewer"] = {"kind": "user", "id": "synthetic-fixture-user"}
        self.start()
        request = self.review("host-bound-user")
        binding = self.server.host.projects["lab"]
        self.assertFalse(binding.authorize({"actor": binding.actor}, {}))
        response = self.post("review/commit", request)
        self.assertEqual(response["result"]["status"], "ok", response)
        self.assertEqual(response["record"]["metadata"]["events"][0]["actor"], binding.actor)

    def test_candidate_selection_and_private_media(self):
        self.add_candidate()
        asset = self.row("asset")
        candidate = self.get("candidates/" + asset["key"] + "/C-002")
        self.assertEqual(candidate["selected_uses"], [])
        self.assertEqual(candidate["check"]["status"], "verified")
        media = candidate["media"][0]
        url = "/api/projects/lab/media/" + media["key"]
        self.assertEqual(self.request("GET", url, cookie=False)[0], 401)
        self.assertEqual(self.request("GET", url)[2], PNG)
        status, headers, data = self.request("GET", url, headers={"Range": "bytes=0-7"})
        self.assertEqual((status, data), (206, PNG[:8]))
        prepared = self.post("selection/prepare", {"asset_key": asset["key"], "candidate_id": "C-002",
                  "expected_revision": candidate["ledger_revision"], "expected_version": candidate["version"], "use_id": "use-a"})
        selected = self.post("selection/commit", {"ticket": prepared["ticket"], "request_id": "select-1"})
        self.assertEqual(selected["result"]["status"], "ok", selected)
        uses = selected["record"]["metadata"]["selected_uses"]
        use_a, use_b = uses
        self.assertEqual(use_a["candidate_id"], "C-002")
        self.assertNotIn("decision_refs", use_a)
        self.assertNotIn("evidence_refs", use_a)
        self.assertIn("decision_refs", use_b)
        (self.root / "assets/flash/preview.png").write_bytes(PNG + b"changed")
        self.assertEqual(self.request("GET", url)[0], 409)

    def test_external_originals_readonly_without_initialization(self):
        before = {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob("*") if p.is_file()}
        status, _, page = self.request("GET", "/api/projects/old/snapshot")
        self.assertEqual(status, 200)
        row = page["records"][0]
        self.assertEqual(row["interpretation"], "raw")
        raw = self.request("GET", "/api/projects/old/records/" + row["key"])[2]
        self.assertIsNone(raw["metadata"])
        self.assertTrue(raw["body"])
        self.post("review/prepare", {}, project="old", expected=403)
        after = {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertFalse((self.root / ".game-workflow-io").exists())


if __name__ == "__main__":
    unittest.main()

