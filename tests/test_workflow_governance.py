"""Governance behavior tests; writes only owned fixture copies."""
import copy, hashlib, json
from pathlib import Path
import shutil, tempfile, unittest
from workflow_formats import yaml_dump, yaml_load, revision
from workflow_io import Workflow
from workflow_panel_data import PanelData
from workflow_governance import Governance
BUNDLE=(Path(__file__).resolve().parents[1] / "plugins" / "gamecaden")
RUN=BUNDLE.parents[1]/"work/governance-eval/tests"

def block(value):
    return "\n<!-- workflow:governance -->\n```json\n"+json.dumps(value,ensure_ascii=False,indent=2)+"\n```\n<!-- workflow:endgovernance -->\n"

def make_case(root, legacy=False):
    shutil.copytree(BUNDLE/"examples/v1/project",root)
    (root/"fixtures/blueprint.md").write_text("# 关卡 A 蓝图\n入口 A → 房间 B → 出口 C。\n",encoding="utf-8")
    subject={"ref":{"path":str(root/"fixtures/blueprint.md")},"version":{"kind":"sha256","value":hashlib.sha256((root/"fixtures/blueprint.md").read_bytes()).hexdigest()},"scope":"空间拓扑与尺度"}
    ledger=yaml_load((root/"game-workflow/assets/ledger.yaml").read_text(encoding="utf-8"))
    candidate=ledger["assets"][0]["candidates"][0]
    asset={"ref":{"id":"A-001"},"candidate_id":"C-001","version":candidate["version"],"scope":"面板演练选用"}
    model={"schema_version":1,
           "materials":[{"id":"blueprint","title":"关卡空间蓝图","domain":"map","requirement":"required","applicability":"applies","for_actions":["灰盒验证"],"purpose":"说明入口、连接与尺度","ref":{"path":"../../fixtures/blueprint.md"}},
                        {"id":"production-map","title":"正式地图制作说明","domain":"map","requirement":"required","applicability":"applies","for_actions":["正式地图生产"],"purpose":"当前尚缺正式生产参数"},
                        {"id":"network","title":"联网同步设计","domain":"network","requirement":"conditional","applicability":"not_applicable","applicability_reason":"本切片为单机内容","for_actions":["联网实现"],"purpose":"本切片没有联网范围"}],
           "conditions":[{"id":"map-ready","title":"关卡路线检查覆盖当前蓝图","domain":"map","scope":"关卡 A","action":"正式地图生产","strength":"required",
                          "authority":"unknown" if legacy else "effective","applies_to":[{"id":"T-004"}],
                          "check":{"kind":"evidence","subject":subject,"coverage":["路由连通"]}},
                         {"id":"asset-choice","title":"候选选用决定（工具演练）","domain":"animation","scope":"当前候选","action":"候选交接","strength":"required","authority":"effective",
                          "applies_to":[{"id":"T-002"}],"check":{"kind":"decision","subject":asset,"actor_kind":"tool"}}]}
    task={"id":"T-004","title":"关卡 A：从灰盒到正式生产","mode":"standard","kind":"map","status":"active","epic":None}
    (root/"game-workflow/tasks/T-004-map.md").write_text("---\n"+yaml_dump(task)+"---\n# 关卡 A\n\n## 当前安排\n灰盒可继续；正式地图尚需材料和当前蓝图检查。\n"+block(model),encoding="utf-8")
    roadmap={"schema_version":1,"outcomes":[{"id":"slice","title":"首个可玩战斗切片","kind":"milestone","scope":"当前切片","work":[{"id":"E-001"},{"id":"T-004"}]}]}
    (root/"game-workflow/roadmap.md").write_text("# 当前路线\n\n本工程仅用于工作流接入演练。\n"+block(roadmap),encoding="utf-8")
    rules={"schema_version":1,"rules":[{"id":"event-owner","title":"反馈由实际事件消费者触发","domain":"animation","scope":"战斗反馈","authority":"effective","applies_to":[{"id":"T-002"}]}]}
    p=root/"game-workflow/spec/combat.md"
    p.write_text(p.read_text(encoding="utf-8")+block(rules),encoding="utf-8")
    if legacy:
        p=root/"legacy/old-map-notes.md";p.parent.mkdir(exist_ok=True)
        p.write_text("# 旧草案\n地图大概是三个房间，尚未确认尺寸和版本。\n",encoding="utf-8")
        model["materials"][0]["ref"]={"path":"../../legacy/old-map-notes.md"}
        (root/"game-workflow/tasks/T-004-map.md").write_text("---\n"+yaml_dump(task)+"---\n# 接入中的关卡资料\n\n旧文件仅作为本次设计的来源，未迁移旧 Task。\n"+block(model),encoding="utf-8")
    return subject,asset

class GovernanceTests(unittest.TestCase):
    def setUp(self):
        RUN.mkdir(parents=True,exist_ok=True)
        self.folder=Path(tempfile.mkdtemp(prefix="gov-",dir=RUN))
        self.root=self.folder/"project"
        self.subject,self.asset=make_case(self.root)
        self.api=Workflow(self.root,actor={"kind":"tool","id":"gate-fixture"})
        self.seq=0

    def view(self):
        return Governance(PanelData(self.root)).build("T-004")

    def call(self,operation,payload):
        self.seq+=1
        request={"protocol_version":1,"request_id":f"governance-{self.seq}","operation":operation,
                 "context":{"project_root":str(self.root),"base_dir":str(self.root)},"payload":payload,"preconditions":[]}
        response=self.api.execute(request)
        self.assertEqual(response["status"],"ok",response)
        return response

    def evidence(self,result="passed",subject=None):
        return self.call("record.create",{"record_type":"evidence","metadata":{"title":"蓝图检查夹具","observed_at":"2026-09-27",
          "actor":{"kind":"tool","id":"gate-fixture"},"subjects":[subject or self.subject],"result":result,"coverage":["路由连通"]},
          "body":"隔离样例观察，不是实际游戏检查。"})
    def decision(self,action="accept",subject=None,replaces=None,scope="面板演练选用"):
        event={"event_id":"e"+str(self.seq+1),"actor":{"kind":"tool","id":"gate-fixture"},"action":action,
               "subjects":[subject or self.asset],"scope":scope,"conclusion":"隔离决定，不是用户验收。",
               "decided_at":None,"recorded_at":"2026-09-27T00:00:00Z"}
        if replaces:event["replaces"]=replaces
        return self.call("decision.record",{"title":"隔离候选选择","event":event})

    def test_tree_materials_and_unknown_do_not_write(self):
        before={str(p):revision(p.read_bytes()) for p in self.root.rglob("*") if p.is_file()}
        v=self.view()
        self.assertTrue(v["coverage"]["structured"])
        self.assertIsNotNone(v["focus"])
        self.assertEqual([m["state"] for m in v["materials"]],["located","missing","not_applicable"])
        self.assertTrue(all(c["state"]=="unknown" for c in v["conditions"]))
        kinds={e["relation"] for e in v["edges"]}
        self.assertTrue({"contains","supports","requires","governed_by"} <= kinds)
        self.assertEqual(before,{str(p):revision(p.read_bytes()) for p in self.root.rglob("*") if p.is_file()})

    def test_evidence_scope_version_and_contradiction(self):
        wrong=copy.deepcopy(self.subject);wrong["scope"]="另一个范围"
        self.evidence(subject=wrong)
        self.assertEqual(self.view()["conditions"][0]["state"],"unknown")
        self.evidence()
        self.assertEqual(self.view()["conditions"][0]["state"],"satisfied")
        self.evidence("failed")
        self.assertEqual(self.view()["conditions"][0]["state"],"unknown")

    def test_changed_blueprint_is_stale(self):
        self.evidence()
        (self.root/"fixtures/blueprint.md").write_bytes(b"changed")
        c=self.view()["conditions"][0]
        self.assertEqual(c["state"],"stale")

    def test_decision_revocation_and_actor_scope(self):
        accepted=self.decision()
        self.assertEqual(self.view()["conditions"][1]["state"],"satisfied")
        self.decision("withdraw",replaces=[accepted["data"]["ref"]])
        self.assertEqual(self.view()["conditions"][1]["state"],"unknown")

    def test_bad_block_fails_closed(self):
        p=self.root/"game-workflow/tasks/T-004-map.md"
        p.write_text(p.read_text(encoding="utf-8").replace('"schema_version": 1','"schema_version": 99'),encoding="utf-8")
        v=self.view()
        self.assertTrue(any(d["code"]=="invalid_governance" for d in v["diagnostics"]))
        self.assertFalse(v["conditions"])

    def test_outer_decision_scope_is_not_silently_widened(self):
        self.decision(scope="仅用于灰盒试验")
        self.assertEqual(self.view()["conditions"][1]["state"],"unknown")

    def test_examples_and_duplicate_ids_cannot_become_requirements(self):
        p=self.root/"game-workflow/spec/combat.md"
        p.write_text(p.read_text(encoding="utf-8")+"\n~~~~text\n"+block({"schema_version":1,"materials":[]})+"\n~~~~\n",encoding="utf-8")
        self.assertEqual(len(self.view()["conditions"]),2)
        p=self.root/"game-workflow/tasks/T-004-map.md"
        p.write_text(p.read_text(encoding="utf-8").replace('"id": "asset-choice"','"id": "map-ready"'),encoding="utf-8")
        v=self.view()
        self.assertFalse(v["conditions"])
        self.assertFalse(v["coverage"]["conditions_mapped"])
        self.assertTrue(any(d["code"]=="conditions_unmapped" for d in v["diagnostics"]))

    def test_not_applicable_requires_a_reason(self):
        p=self.root/"game-workflow/tasks/T-004-map.md"
        import re
        p.write_text(re.sub(r'"applicability_reason": "[^"]*",?','',p.read_text(encoding="utf-8")),encoding="utf-8")
        v=self.view()
        self.assertFalse(v["materials"])
        self.assertTrue(any(d["code"]=="invalid_governance" for d in v["diagnostics"]))

    def test_legacy_mapping_is_not_automatic_adoption(self):
        root=self.folder/"old-project";make_case(root,legacy=True)
        v=Governance(PanelData(root)).build()
        self.assertEqual(v["conditions"][0]["state"],"unknown")
        self.assertEqual(v["materials"][0]["state"],"located")
        legacy_nodes=[n for n in v["nodes"] if n.get("interpretation")=="raw"]
        self.assertTrue(legacy_nodes)
        self.assertTrue(all(n["kind"]=="document" and n.get("status") is None for n in legacy_nodes))
        self.assertFalse(any(e["relation"]=="contains" and e["to"] in {n["key"] for n in legacy_nodes} for e in v["edges"]))
        external=PanelData(root,external_sources=[{"id":"notes","label":"旧草案","role":"spec","path":"legacy/old-map-notes.md"}])
        v=Governance(external).build()
        self.assertFalse(v["coverage"]["structured"])
        self.assertTrue(any(d["code"]=="governance_unmapped" for d in v["diagnostics"]))

    def test_http_task_review_decision_and_resume_projection(self):
        from test_workflow_panel_server import BridgeTests
        host=BridgeTests("test_session_origin_csrf_and_endpoint_bounds")
        host.setUp()
        self.addCleanup(host.stop)
        # Copy only Task contract; rebase its fixture subject to the HTTP-owned project.
        text=(self.root/"game-workflow/tasks/T-004-map.md").read_text(encoding="utf-8")
        text=text.replace(str(self.root).replace("\\","\\\\"),str(host.root).replace("\\","\\\\"))
        (host.root/"game-workflow/tasks/T-004-map.md").write_text(text,encoding="utf-8")
        shutil.copyfile(self.root/"fixtures/blueprint.md",host.root/"fixtures/blueprint.md")
        before=host.get("governance")
        self.assertEqual(before["conditions"][1]["state"],"unknown")
        row=host.row("asset")
        c=host.get("candidates/"+row["key"]+"/C-001")
        prepared=host.post("review/prepare",{"asset_key":row["key"],"candidate_id":"C-001","expected_revision":c["ledger_revision"],
                                           "expected_version":c["version"],"scope":"面板演练选用"})
        body={"ticket":prepared["ticket"],"request_id":"governance-path","conclusion":"accept","note":"工具夹具路径；不是用户美术接受。"}
        first=host.post("review/commit",body)
        self.assertEqual(first["result"]["status"],"ok",first)
        second=host.post("review/commit",body)
        self.assertTrue(second["result"]["replayed"])
        after=host.get("governance")
        self.assertEqual(after["conditions"][1]["state"],"satisfied")
        self.assertEqual(after["conditions"][0]["state"],"unknown")
        self.assertEqual(first["record"]["metadata"]["events"][0]["actor"]["kind"],"tool")

if __name__=="__main__":
    unittest.main()

