"""Recover current asset registration without rewriting unavailable history."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from workflow_formats import plain, revision, validate, yaml_dump, yaml_load
from workflow_io import Workflow


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "plugins/gamecaden/examples/v1/project"


class CandidateRecovery(unittest.TestCase):
    def setUp(self):
        run_root = ROOT / "work/candidate-recovery-tests"
        run_root.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix="case-", dir=run_root)) / "project"
        shutil.copytree(FIXTURE, self.root)
        self.api = Workflow(self.root)
        self.sequence = 0
        self.ledger = self.root / "game-workflow/assets/ledger.yaml"

    def call(self, operation, payload, *, write=False):
        self.sequence += 1
        request = {"protocol_version": 1, "request_id": f"candidate-test-{self.sequence}",
                   "operation": operation, "context": {"project_root": str(self.root),
                   "base_dir": str(self.root / "game-workflow")}, "payload": payload}
        if write:
            request["preconditions"] = [{"target": {"path": "assets/ledger.yaml"},
                                         "expected_revision": revision(self.ledger.read_bytes())}]
        response = self.api.execute(request)
        validate("Response", response)
        (self.root.parent / f"response-{self.sequence}.json").write_text(
            json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")
        return response

    def asset(self):
        result = self.call("record.read", {"target": {"id": "A-001"}})
        self.assertEqual(result["status"], "ok", result)
        return plain(result["data"]["metadata"])

    def new_candidate(self):
        folder = self.root / "assets/flash/c-002"
        folder.mkdir(parents=True)
        media = folder / "flash.json"
        media.write_text('{"version": 2, "frames": 8}\n', encoding="utf-8")
        manifest = {"schema_version": 1, "asset_id": "A-001", "candidate_id": "C-002",
                    "files": [{"path": "flash.json", "sha256": revision(media.read_bytes())[7:],
                               "role": "runtime-input"}]}
        path = folder / "manifest.json"
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return {"id": "C-002", "manifest": {"path": "../../assets/flash/c-002/manifest.json"},
                "version": {"kind": "sha256", "value": revision(path.read_bytes())[7:]}}

    def update(self, asset):
        # Read metadata is relative to its ledger, so bind request references there.
        self.sequence += 1
        request = {"protocol_version": 1, "request_id": f"candidate-test-{self.sequence}",
                   "operation": "asset.upsert", "context": {"project_root": str(self.root),
                   "base_dir": str(self.ledger.parent)}, "payload": {"ledger": {"path": "ledger.yaml"},
                   "mode": "update", "asset": asset, "reason": "Register current version; retain historical bindings"},
                   "preconditions": [{"target": {"path": "ledger.yaml"},
                                      "expected_revision": revision(self.ledger.read_bytes())}]}
        result = self.api.execute(request)
        validate("Response", result)
        (self.root.parent / f"response-{self.sequence}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return result

    def test_overwritten_history_allows_new_candidate_but_not_old_selection(self):
        before = self.asset()
        original = copy.deepcopy(before["candidates"][0])
        engine = (self.root / "game/consumers.json").read_bytes()
        decision_path = self.root / "game-workflow/decisions/D-001.md"
        decision = decision_path.read_bytes()
        (self.root / "assets/flash/flash.json").write_text('{"overwritten": true}\n', encoding="utf-8")
        before["candidates"].append(self.new_candidate())
        result = self.update(before)
        self.assertEqual(result["status"], "ok", result)
        self.assertEqual(result["data"]["validated_candidate_ids"], ["C-002"])
        warning = result["data"]["historical_candidate_diagnostics"][0]
        self.assertEqual(warning["candidate_id"], "C-001")
        self.assertEqual(warning["error"]["code"], "version_mismatch")
        current = self.asset()
        self.assertEqual(current["candidates"][0], original)
        self.assertEqual(current["selected_uses"], before["selected_uses"])
        use = copy.deepcopy(current["selected_uses"][0])
        stale = self.call("asset.select", {"ledger": {"path": "assets/ledger.yaml"}, "asset_id": "A-001",
                          "action": "set", "use": use, "reason": "Verify the old version"}, write=True)
        self.assertEqual(stale["status"], "conflict", stale)
        use["candidate_id"] = "C-002"
        use.pop("decision_refs", None)
        use.pop("evidence_refs", None)
        selected = self.call("asset.select", {"ledger": {"path": "assets/ledger.yaml"}, "asset_id": "A-001",
                             "action": "set", "use": use, "reason": "Select the new version without inheriting old acceptance"}, write=True)
        self.assertEqual(selected["status"], "ok", selected)
        self.assertEqual(selected["data"]["validated_candidate_ids"], ["C-002"])
        self.assertEqual((self.root / "game/consumers.json").read_bytes(), engine)
        self.assertEqual(decision_path.read_bytes(), decision)

    def test_missing_manifest_history_does_not_block_current_registration(self):
        asset = self.asset()
        (self.root / "assets/flash/manifest.json").unlink()
        asset["candidates"].append(self.new_candidate())
        result = self.update(asset)
        self.assertEqual(result["status"], "ok", result)
        self.assertEqual(result["data"]["historical_candidate_diagnostics"][0]["error"]["code"], "not_found")

    def test_bad_new_payload_and_rewritten_history_are_rejected_without_write(self):
        asset = self.asset()
        asset["candidates"].append(self.new_candidate())
        (self.root / "assets/flash/c-002/flash.json").write_bytes(b"changed")
        ledger_before = self.ledger.read_bytes()
        result = self.update(asset)
        self.assertEqual(result["status"], "conflict", result)
        self.assertEqual(result["errors"][0]["code"], "version_mismatch")
        self.assertEqual(self.ledger.read_bytes(), ledger_before)
        rewritten = self.asset()
        rewritten["candidates"][0]["version"]["value"] = "0" * 64
        self.assertEqual(self.update(rewritten)["status"], "rejected")
        self.assertEqual(self.ledger.read_bytes(), ledger_before)
        removed = self.asset()
        removed["candidates"] = []
        self.assertEqual(self.update(removed)["status"], "rejected")
        self.assertEqual(self.ledger.read_bytes(), ledger_before)

    def test_new_references_on_retained_candidates_are_still_guarded(self):
        asset = self.asset()
        asset["candidates"][0]["evidence_refs"] = [{"path": "../../../outside.json"}]
        ledger_before = self.ledger.read_bytes()
        result = self.update(asset)
        self.assertEqual(result["status"], "rejected", result)
        self.assertEqual(result["errors"][0]["code"], "permission_denied")
        self.assertEqual(self.ledger.read_bytes(), ledger_before)

    def test_adding_references_preserves_unavailable_history_and_checks_new_refs(self):
        ledger = yaml_load(self.ledger.read_text(encoding="utf-8"))
        missing = {"path": "missing-history.md"}
        ledger["assets"][0]["source_refs"] = [copy.deepcopy(missing)]
        ledger["assets"][0]["candidates"][0]["evidence_refs"] = [copy.deepcopy(missing)]
        self.ledger.write_text(yaml_dump(ledger), encoding="utf-8")
        asset = self.asset()
        asset["source_refs"].append({"id": "T-002"})
        asset["candidates"][0]["evidence_refs"].append({"id": "EV-002"})
        result = self.update(asset)
        self.assertEqual(result["status"], "ok", result)
        saved = self.asset()
        self.assertEqual(saved["source_refs"], [missing, {"id": "T-002"}])
        self.assertEqual(saved["candidates"][0]["evidence_refs"], [missing, {"id": "EV-002"}])
        saved["candidates"][0]["evidence_refs"].append({"path": "another-missing.md"})
        before = self.ledger.read_bytes()
        rejected = self.update(saved)
        self.assertEqual(rejected["status"], "rejected", rejected)
        self.assertEqual(rejected["errors"][0]["code"], "not_found")
        self.assertEqual(self.ledger.read_bytes(), before)

    def test_historical_reference_cannot_be_promoted_into_new_candidate_or_field(self):
        ledger = yaml_load(self.ledger.read_text(encoding="utf-8"))
        missing = {"path": "missing-history.md"}
        ledger["assets"][0]["source_refs"] = [copy.deepcopy(missing)]
        ledger["assets"][0]["candidates"][0]["evidence_refs"] = [copy.deepcopy(missing)]
        self.ledger.write_text(yaml_dump(ledger), encoding="utf-8")
        baseline = self.asset()
        candidate = self.new_candidate()
        candidate["evidence_refs"] = [copy.deepcopy(missing)]
        variants = []
        new_candidate = copy.deepcopy(baseline)
        new_candidate["candidates"].append(candidate)
        variants.append(new_candidate)
        new_field = copy.deepcopy(baseline)
        new_field["candidates"][0]["source_refs"] = [copy.deepcopy(missing)]
        variants.append(new_field)
        for variant in variants:
            with self.subTest(candidates=len(variant["candidates"])):
                before = self.ledger.read_bytes()
                result = self.update(variant)
                self.assertEqual(result["status"], "rejected", result)
                self.assertEqual(result["errors"][0]["code"], "not_found")
                self.assertEqual(self.ledger.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
