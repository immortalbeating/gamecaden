"""Bounded panel-model reuse and concurrent probe regressions on private fixtures."""
import copy
import os
from pathlib import Path
import shutil
import tempfile
import threading
import unittest
from unittest.mock import patch
from workflow_formats import canonical, revision
from workflow_panel_data import PanelData, PanelDataError
from workflow_project import Project
from workflow_storage import Store
from workflow_governance import Governance
import test_workflow_panel_server as bridge

BUNDLE=Path(__file__).resolve().parents[1]/"plugins/gamecaden"
RUN=BUNDLE.parents[1]/"work/panel-scaling-eval/tests"

class ScalingTests(unittest.TestCase):
    def setUp(self):
        RUN.mkdir(parents=True,exist_ok=True)
        self.folder=Path(tempfile.mkdtemp(prefix="scaling-",dir=RUN))
        self.addCleanup(shutil.rmtree,self.folder)
        self.root=self.folder/"project"
        shutil.copytree(BUNDLE/"examples/v1/project",self.root)
        self.panel=PanelData(self.root)
    def test_pages_and_governance_share_one_scan(self):
        original=Project.scan;calls=[]
        def scan(project,**kwargs):
            calls.append(project)
            return original(project,**kwargs)
        with patch.object(Project,"scan",scan):
            page=self.panel.snapshot(limit=2)
            while page["next_cursor"]:
                page=self.panel.snapshot(page["next_cursor"],limit=2)
            batch=Governance(self.panel).build(include_records=True)
        self.assertEqual(len(calls),1)
        self.assertEqual(batch["records"],self.panel.snapshot_all()["records"])
        self.assertEqual(batch["records_complete"],batch["coverage"]["records_complete"])
        self.assertEqual(batch["record_diagnostics"],self.panel.snapshot_all()["diagnostics"])
    def test_off_page_content_membership_and_mapping_invalidate_cursor(self):
        for change in ("same_mtime","add","delete","mapping"):
            with self.subTest(change=change):
                panel=PanelData(self.root);page=panel.snapshot(limit=1)
                path=self.root/"game-workflow/vision.md"
                if change=="same_mtime":
                    stamp=path.stat();path.write_bytes(path.read_bytes()+b"\nchanged")
                    os.utime(path,ns=(stamp.st_atime_ns,stamp.st_mtime_ns))
                elif change=="add":(self.root/"game-workflow/spec/new.md").write_text("# New",encoding="utf-8")
                elif change=="delete":(self.root/"game-workflow/spec/new.md").unlink()
                else:
                    mapping=self.root/"game-workflow/workspace.yaml";mapping.write_bytes(mapping.read_bytes()+b"\n# changed")
                with self.assertRaises(PanelDataError) as error:panel.snapshot(page["next_cursor"],limit=1)
                self.assertEqual(error.exception.code,"stale_cursor")
    def test_pending_state_invalidates_cursor_and_refreshes_diagnostics(self):
        pending=[]
        with patch.object(Store,"pending",side_effect=lambda:copy.deepcopy(pending)):
            first=self.panel.snapshot(limit=1)
            pending.append({"receipt":{"request_id":"pending-fixture","phase":"prepared"}})
            with self.assertRaises(PanelDataError) as error:self.panel.snapshot(first["next_cursor"],limit=1)
            self.assertEqual(error.exception.code,"stale_cursor")
            self.assertTrue(any(d["code"]=="operation_pending" for d in self.panel.snapshot_all()["diagnostics"]))
            pending.clear()
            self.assertFalse(any(d["code"]=="operation_pending" for d in self.panel.snapshot_all()["diagnostics"]))
    def test_duplicate_identity_diagnostics_survive_model_reuse(self):
        source=self.root/"game-workflow/tasks/T-002-feedback.md"
        shutil.copyfile(source,source.with_name("duplicate.md"))
        first=self.panel.snapshot_all()
        self.assertTrue(any(d["code"]=="duplicate_id" for d in first["diagnostics"]))
        self.assertEqual(first,self.panel.snapshot_all())
    def test_record_and_output_limits_are_explicit(self):
        with patch("workflow_panel_data.MAX_RECORDS",1):
            with self.assertRaises(PanelDataError) as error:self.panel.snapshot_all()
            self.assertEqual((error.exception.code,error.exception.status),("too_many_records",413))
        with patch("workflow_panel_data.MAX_SNAPSHOT_BYTES",1):
            with self.assertRaises(PanelDataError) as error:self.panel.snapshot_all()
            self.assertEqual((error.exception.code,error.exception.status),("output_too_large",413))
    def test_initial_and_reused_output_recheck_after_assembly(self):
        original=Project.check_snapshot
        for cached in (False,True):
            with self.subTest(cached=cached):
                panel=PanelData(self.root)
                if cached:panel.snapshot(limit=1)
                calls=0
                def check(project):
                    nonlocal calls
                    calls+=1
                    if calls==(2 if cached else 1):
                        path=self.root/"game-workflow/vision.md";path.write_bytes(path.read_bytes()+b"\nrace")
                    return original(project)
                with patch.object(Project,"check_snapshot",check):
                    with self.assertRaises(PanelDataError) as error:panel.snapshot(limit=1)
                self.assertEqual(error.exception.code,"revision_conflict")
    def test_provenance_count_does_not_limit_governance_task_count(self):
        # In-memory source metadata avoids creating ten thousand disk documents.
        original_scan=Project.scan;original_check=Project.check_snapshot
        virtual={str(self.root/"virtual"/f"source-{i}.json"):"sha256:"+"0"*64 for i in range(10001)}
        def scan(project,**kwargs):
            result=original_scan(project,**kwargs)
            tasks=[r for r in result if r.kind=="task"]
            for i in range(26-len(tasks)):
                record=copy.deepcopy(tasks[0]);record.metadata["id"]=f"T-{100+i}"
                result.append(record)
            project.observed.update(virtual)
            return result
        def check(project):
            # Real fixture bytes and membership still get their normal final check.
            saved=project.observed
            project.observed={p:r for p,r in saved.items() if p not in virtual}
            try:return original_check(project)
            finally:project.observed=saved
        with patch.object(Project,"scan",scan),patch.object(Project,"check_snapshot",check):
            batch=Governance(self.panel).build(include_records=True)
        self.assertGreater(len(batch["source_revisions"]),10000)
        self.assertEqual(len([r for r in batch["records"] if r["record_type"]=="task"]),26)
        self.assertEqual(batch["coverage"]["records_complete"],self.panel._snapshot_guard.scan_complete)

class ProbeConcurrencyTests(unittest.TestCase):
    def setUp(self):
        self.host=bridge.BridgeTests("test_session_origin_csrf_and_endpoint_bounds")
        self.host.setUp();self.addCleanup(self.host.stop)
    def test_slow_probe_does_not_block_details_and_overlapping_probes_share_work(self):
        host=self.host;row=host.row("task");binding=host.server.host.project("lab")
        entered=threading.Event();release=threading.Event();results=[];calls=[]
        original=binding.data.revisions
        def slow():
            calls.append(True);entered.set();self.assertTrue(release.wait(5));return original()
        def probe():results.append(host.request("GET","/api/projects/lab/revisions"))
        with patch.object(binding.data,"revisions",side_effect=slow):
            first=threading.Thread(target=probe);first.start();self.assertTrue(entered.wait(2))
            # Synchronize the second request at Event.wait, after it has joined the flight.
            flight=binding.probe;waiting=threading.Event();original_wait=flight["event"].wait
            def wait(*args,**kwargs):waiting.set();return original_wait(*args,**kwargs)
            with patch.object(flight["event"],"wait",side_effect=wait):
                second=threading.Thread(target=probe);second.start();self.assertTrue(waiting.wait(2))
                try:
                    status,_,detail=host.request("GET","/api/projects/lab/records/"+row["key"])
                    self.assertEqual(status,200,detail)
                finally:release.set()
                first.join(5);second.join(5)
            self.assertEqual(len(calls),1)
            host.get("revisions");self.assertEqual(len(calls),2)
        self.assertEqual([r[0] for r in results],[200,200])
        self.assertEqual(results[0][2],results[1][2])
    def test_governance_optional_records_and_query_bounds(self):
        host=self.host
        standard=host.get("governance");self.assertNotIn("records",standard)
        batch=host.get("governance?include_records=1")
        self.assertEqual(batch["records"],host.get("snapshot?limit=1000")["records"])
        self.assertEqual(batch["records_complete"],batch["coverage"]["records_complete"])
        self.assertEqual(host.request("GET","/api/projects/lab/governance?include_records=0")[0],400)
        self.assertEqual(host.request("GET","/api/projects/lab/governance?include_records=")[0],400)
        self.assertEqual(host.request("GET","/api/projects/lab/governance?include_records=1&include_records=1")[0],400)
        self.assertEqual(host.request("GET","/api/projects/lab/governance?path=../other")[0],400)

if __name__=="__main__":unittest.main()
