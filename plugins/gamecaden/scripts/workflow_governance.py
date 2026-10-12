"""Source-backed governance projection. It never writes project facts or authorizes actions."""
from __future__ import annotations

if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from gamecaden_runtime import bootstrap_cli
    bootstrap_cli("governance")

import argparse, hashlib, json, re
from pathlib import Path
from datetime import datetime, timezone
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from workflow_formats import SCHEMA, WorkflowError, canonical, json_load, revision
from workflow_panel_data import PanelData, PanelDataError

BUNDLE = Path(__file__).resolve().parents[1]
GOV_SCHEMA = json_load((BUNDLE/"schemas/governance-v1.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(GOV_SCHEMA, registry=Registry().with_resource(SCHEMA["$id"], Resource.from_contents(SCHEMA)))
BLOCK = re.compile(r"<!-- workflow:governance -->\s*```json\s*\n(.*?)\n```\s*<!-- workflow:endgovernance -->", re.S)

def annotation_blocks(body):
    """Only standalone markers outside ordinary fenced examples are active."""
    lines=body.splitlines(); result=[]; i=0; fence=None
    while i<len(lines):
        line=lines[i].strip()
        if fence:
            if re.fullmatch(re.escape(fence[0])+"{"+str(fence[1])+",}",line): fence=None
        elif line=="<!-- workflow:governance -->":
            end=i+1
            while end<len(lines) and lines[end].strip()!="<!-- workflow:endgovernance -->": end+=1
            chunk="\n".join(lines[i:end+1])
            match=BLOCK.fullmatch(chunk)
            if not match: raise PanelDataError("invalid_governance","Governance block is not properly closed")
            result.append(match[1]); i=end
        else:
            opening=re.match(r"^(`{3,}|~{3,})",line)
            if opening:fence=(opening[1][0],len(opening[1]))
        i+=1
    return result

def source_excerpt(body):
    """Return the first nonempty H2 section without interpreting its language.

    Fenced examples cannot supply headings or workflow boundaries. Preserve
    section content verbatim (apart from outer whitespace) for source display.
    Actual embedded records have already been masked by the native parser.
    """
    heading = None
    content = []
    fence = None
    for line in body.splitlines(keepends=True):
        stripped = line.strip()
        if fence:
            if heading is not None:
                content.append(line)
            if re.fullmatch(re.escape(fence[0])+"{"+str(fence[1])+",}", stripped):
                fence = None
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if opening:
            fence = (opening[1][0], len(opening[1]))
            if heading is not None:
                content.append(line)
            continue
        boundary = stripped.startswith("<!-- workflow:")
        match = re.match(r"^ {0,3}##[ \t]+(.+?)[ \t]*(?:\r?\n)?$", line)
        if boundary or match:
            if heading is not None and "".join(content).strip():
                return {"text": "".join(content).strip(), "heading": heading,
                        "kind": "source_excerpt"}
            if boundary:
                break
            heading = match[1]
            content = []
        elif heading is not None:
            content.append(line)
    if heading is not None and "".join(content).strip():
        return {"text": "".join(content).strip(), "heading": heading,
                "kind": "source_excerpt"}
    return None


class Governance:
    def __init__(self, panel):
        self.panel = panel
        self.guard = panel._project()
        self.nodes, self.edges, self.conditions, self.materials, self.diagnostics = {}, [], [], [], []
        self.by_ref, self.locals, self.bodies, self.entries = {}, {}, {}, []
        self.rows = []
        self.extensions = []
        self.local_ids = set()
        self.complete = True
        self.invalid_paths=set()

    def diagnostic(self, code, message, source=None):
        self.diagnostics.append({"code":code,"message":message,"source_key":source})

    def add(self, node):
        self.nodes[node["key"]] = node
        return node["key"]

    def edge(self, a, b, kind):
        edge = {"from":a,"to":b,"relation":kind}
        if a in self.nodes and b in self.nodes and edge not in self.edges:
            self.edges.append(edge)

    def from_record(self, row):
        key = "record:" + row["key"]
        metadata = row.get("metadata") or {}
        native=row.get("interpretation")=="native"
        self.add({"key":key,"kind":row["record_type"] if native and row["record_type"] in ("task","epic","asset") else "document",
                  "title":row["title"],"ref":row["ref"],"path":row["path"],"revision":row["revision"],
                  "record_key":row["key"],"metadata":metadata,"role":row.get("role",row["record_type"]),
                  "interpretation":row.get("interpretation"),"authority":"unknown",
                  "status":metadata.get("status") if native and row["record_type"]!="attachment" else None})
        self.by_ref[(row["path"],row["ref"].get("id"))] = key
        return key

    def resolve(self, ref, base):
        # Validate the original record qualifiers before interpreting a governance
        # fragment. Only that fragment is removed; source/project/id stay intact.
        owner_ref={k:v for k,v in ref.items() if k!="fragment"}
        record=self.guard.resolve(owner_ref,base)
        local=self.locals.get((str(record.path),ref.get("fragment")))
        if local:
            return local
        if ref.get("fragment"):
            record=self.guard.resolve(ref,base)
        key = self.by_ref.get((str(record.path),record.id))
        if key:
            return key
        data = self.guard.read_record(record,False)
        row = self.panel._row(data,record.kind)
        return self.from_record(row)

    def link_ref(self, start, ref, base, relation):
        try:
            key = self.resolve(ref,base)
            self.edge(start,key,relation)
            return key
        except (WorkflowError,PanelDataError) as exc:
            self.diagnostic("unresolved_relation",str(exc),start)
            return None

    def subject_key(self, subject, base):
        record = self.guard.resolve(subject["ref"],base)
        version = subject.get("version") or {}
        return canonical([str(record.path),record.id,subject.get("candidate_id"),
                          version.get("kind"),version.get("value"),subject["scope"],subject.get("use")])

    def proof_rows(self, check, base):
        if check.get("proofs"):
            result=[]
            for ref in check["proofs"]:
                record = self.guard.resolve(ref,base)
                data=self.guard.read_record(record)
                result.append((record.kind,data,ref.get("fragment")))
            return result
        return [(row["record_type"],{"metadata":row["metadata"],"path":row["path"],"revision":row["revision"]},None)
                for row in self.rows if row["record_type"] in ("evidence","decision")]

    def evaluate(self, definition, base):
        if definition.get("applicability","applies") == "not_applicable":
            return "not_applicable",definition["applicability_reason"],[]
        if definition.get("authority","unknown") != "effective":
            return "unknown","Constraint is not effective; retain it for verification or reference",[]
        if definition.get("applicability","applies") == "unknown":
            return "unknown","Applicability has not been verified",[]
        check=definition.get("check")
        if not check:
            return "unknown","Semantic judgment is required; no corresponding evidence or decision is bound",[]
        subject=check["subject"]
        try:
            self.guard.check_subject(subject,base)
            wanted=self.subject_key(subject,base)
        except WorkflowError as exc:
            state="stale" if exc.code in ("version_mismatch","revision_conflict") else "unknown"
            return state,"Subject version could not be verified against the current source: "+str(exc),[]
        try:
            proofs=self.proof_rows(check,base)
        except WorkflowError as exc:
            return "unknown","Declared grounds could not be resolved: "+str(exc),[]
        values,used=[],[]
        for kind,data,fragment in proofs:
            meta=data.get("metadata") or {}
            origin=Path(data["path"]).parent
            if check["kind"]=="evidence" and kind=="evidence":
                candidates=[{"subjects":meta.get("subjects",[]),"actor":meta.get("actor"),"result":meta.get("result"),
                             "coverage":meta.get("coverage",[])}]
            elif check["kind"]=="decision" and kind=="decision":
                candidates=[e for e in meta.get("events",[]) if fragment is None or e["event_id"]==fragment]
            else:
                continue
            for event in candidates:
                if check.get("actor_kind") and (event.get("actor") or {}).get("kind")!=check["actor_kind"]:
                    continue
                if kind=="decision" and (data["path"],event["event_id"]) in self.retired:
                    continue
                if kind=="decision" and event.get("scope")!=check.get("event_scope",subject["scope"]):
                    continue
                try:
                    matches=any(self.subject_key(s,origin)==wanted for s in event.get("subjects",[]))
                except WorkflowError:
                    matches=False
                if not matches:
                    continue
                if kind=="evidence":
                    if not set(check.get("coverage",[])) <= set(event.get("coverage",[])):
                        continue
                    value = "satisfied" if event["result"]=="passed" else "unsatisfied" if event["result"]=="failed" else "unknown"
                    ref={"id":meta["id"]}
                else:
                    action=event["action"]
                    value="satisfied" if action=="accept" else "unsatisfied" if action in ("reject","revise") else "unknown"
                    ref={"id":meta["id"],"fragment":event["event_id"]}
                values.append(value)
                used.append({"ref":ref,"path":data["path"],"revision":data["revision"],"title":meta.get("title",meta.get("id")),
                             "actor":event.get("actor"),"event_scope":event.get("scope"),"conclusion":event.get("conclusion",event.get("result"))})
        if not values:
            return "unknown","No effective grounds match the subject, version, coverage, and use",[]
        if len(set(values))>1:
            return "unknown","Grounds for the same scope conflict; verify them or declare a replacement",used
        state=values[0]
        return state,{"satisfied":"Original records match the declared check scope; execution still requires checking all applicable agreements","unsatisfied":"Original records for the matching scope report failure or require revision","unknown":"Existing grounds do not establish satisfaction"}[state],used

    def build(self, focus=None):
        cursor=None
        for _ in range(100):
            page=self.panel.snapshot(cursor=cursor)
            self.rows.extend(page["records"])
            self.complete=self.complete and page["complete"]
            self.diagnostics.extend(page["diagnostics"])
            cursor=page["next_cursor"]
            if cursor is None:
                break
        else:
            raise PanelDataError("too_many_records","Sources exceed the read limit for this request",413)
        root_key="project:"+page["project"]["id"]
        self.add({"key":root_key,"kind":"project","title":page["project"]["name"],"ref":None,
                  "path":str(self.panel.root),"revision":None})
        for row in self.rows:
            key=self.from_record(row)
            if row["interpretation"]=="native" and row["record_type"] in ("task","epic"):
                self.edge(root_key,key,"contains")
            if row["interpretation"]!="native":
                continue
            try:
                record=self.guard.resolve(row["ref"])
                body=record.body or ""
                # Native parser spans are relative to the main body. Mask only actual
                # embedded records, preserving newlines and surrounding example fences.
                if record.span is None:
                    document=self.guard.documents[record.path]
                    spans=sorted((r.span for r in document.records if r.span is not None),reverse=True)
                    for start,end in spans:
                        body=body[:start]+"\n"*body[start:end].count("\n")+body[end:]
                self.bodies[key]=body
                excerpt=source_excerpt(body)
                if excerpt:
                    self.nodes[key]["excerpt"]=excerpt
                blocks=annotation_blocks(body)
                # Embedded EV/Decision bodies are parsed only in their own record.
                if len(blocks)>1:
                    raise PanelDataError("invalid_governance","Each source record may contain at most one governance block")
                if blocks:
                    model=json_load(blocks[0])
                    errors=list(VALIDATOR.iter_errors({k:v for k,v in model.items() if k!="navigation"}))
                    if errors:
                        raise PanelDataError("invalid_governance",errors[0].message)
                    ids=[e["id"] for group in ("outcomes","rules","materials","conditions","flows","relationships") for e in model.get(group,[])]
                    if len(ids)!=len(set(ids)) or any((row["path"],local_id) in self.local_ids for local_id in ids):
                        raise PanelDataError("invalid_governance","Duplicate local governance IDs in the same file")
                    for flow in model.get("flows",[]):
                        step_ids=[step["id"] for step in flow["steps"]]
                        if len(step_ids)!=len(set(step_ids)):
                            raise PanelDataError("invalid_governance","Duplicate step IDs within a flow")
                    self.local_ids.update((row["path"],local_id) for local_id in ids)
                    self.extensions.append((model,row))
                    for group,kind in (("outcomes","outcome"),("rules","rule"),("materials","material"),("conditions","condition")):
                        for entry in model.get(group,[]):
                            local=(row["path"],entry["id"])
                            if local in self.locals:
                                raise PanelDataError("invalid_governance","Duplicate local governance IDs in the same file")
                            node_key="local:"+hashlib.sha256(canonical(local).encode()).hexdigest()
                            self.locals[local]=node_key
                            node={"key":node_key,"kind":entry.get("kind",kind) if group=="outcomes" else kind,
                                  "title":entry["title"],"ref":{"path":row["path"],"fragment":entry["id"]},
                                  "path":row["path"],"revision":row["revision"],"source_key":key,**{k:v for k,v in entry.items() if k not in ("id","title","kind","check")}}
                            self.add(node)
                            self.edge(node_key,key,"defined_in")
                            self.entries.append((group,node_key,entry,row))
            except (WorkflowError,PanelDataError,ValueError,TypeError) as exc:
                self.invalid_paths.add(row["path"])
                self.diagnostic("invalid_governance",str(exc),key)
        for row in self.rows:
            if row["interpretation"]!="native" or row["record_type"]=="attachment":
                continue
            key="record:"+row["key"]
            meta=row.get("metadata") or {}
            base=Path(row["reference_base"] or row["path"]).parent if not row["reference_base"] else Path(row["reference_base"])
            if row["record_type"]=="task" and meta.get("epic"):
                parent=self.link_ref(key,{"id":meta["epic"]},base,"references")
                if parent:
                    self.edges=[e for e in self.edges if not(e["from"]==root_key and e["to"]==key and e["relation"]=="contains")]
                    self.edge(parent,key,"contains")
            for dep in meta.get("depends_on",[]):
                target=self.link_ref(key,dep["target"],base,"requires")
                if target:
                    edge=next(e for e in self.edges if e["from"]==key and e["to"]==target and e["relation"]=="requires")
                    edge.update(requirement=dep["requires"],assessment="unknown",evidence_refs=dep.get("evidence_refs",[]))
            for ref in meta.get("related",[]):
                self.link_ref(key,ref,base,"references")
        self.retired=set()
        for row in self.rows:
            if row["record_type"]!="decision":
                continue
            for event in (row.get("metadata") or {}).get("events",[]):
                for ref in event.get("replaces",[]):
                    try:
                        target=self.guard.resolve(ref,Path(row["reference_base"]))
                        self.retired.add((str(target.path),ref.get("fragment")))
                    except WorkflowError:
                        self.diagnostic("invalid_replacement","Decision replacement relation could not be resolved","record:"+row["key"])
        for group,key,entry,row in self.entries:
            base=Path(row["reference_base"])
            source="record:"+row["key"]
            if group=="outcomes":
                self.edge(root_key,key,"contains")
                for ref in entry.get("work",[]):
                    self.link_ref(key,ref,base,"supports")
            elif group=="rules":
                for ref in entry.get("applies_to",[]):
                    target=self.link_ref(key,ref,base,"references")
                    if target:self.edge(target,key,"governed_by")
            elif group=="materials":
                state="not_applicable" if entry["applicability"]=="not_applicable" else "unknown"
                reason=entry["applicability_reason"] if state=="not_applicable" else "Applicability must be determined or materials provided"
                target=None
                if entry["applicability"]=="applies":
                    if entry.get("ref"):
                        try:
                            target=self.resolve(entry["ref"],base)
                            self.edge(key,target,"references")
                            state,reason="located","Material is located; related conditions and grounds determine content sufficiency"
                        except WorkflowError as exc:
                            state,reason="missing",str(exc)
                    else: state,reason="missing","Materials required for this action have not been provided"
                item={**entry,"key":key,"source_key":source,"state":state,"reason":reason}
                refs=entry.get("applies_to",[row["ref"]] if row["record_type"] in ("task","epic") else [])
                item["applies_to"]=[k for ref in refs if (k:=self.link_ref(key,ref,base,"references"))]
                if target:item["record_key"]=self.nodes[target].get("record_key")
                self.materials.append(item)
                self.nodes[key].update(status=state,reason=reason)
            else:
                state,reason,proofs=self.evaluate(entry,base)
                if row["path"] in self.invalid_paths:
                    state,reason="unknown","Definition source contains invalid or conflicting annotations"
                targets=[]
                for ref in entry["applies_to"]:
                    target=self.link_ref(key,ref,base,"references")
                    if target:targets.append(target);self.edge(target,key,"requires")
                # Broken scope must never be shown as a current satisfied prerequisite.
                if len(targets)!=len(entry["applies_to"]) or not any(self.nodes[t].get("kind") in ("task","epic","asset") for t in targets):
                    state,reason="unknown","Some applicable subjects could not be resolved"
                item={**{k:v for k,v in entry.items() if k not in ("check","applies_to")},
                      "key":key,"source_key":source,"state":state,"reason":reason,"applies_to":targets,
                      "expected_check":{k:entry.get("check",{}).get(k) for k in ("kind","actor_kind")},
                      "proofs":proofs,"subject":entry.get("check",{}).get("subject")}
                self.conditions.append(item)
                self.nodes[key].update(status=state,reason=reason)
                for proof in proofs:
                    proof_key=self.link_ref(key,proof["ref"],base,"verified_by" if entry["check"]["kind"]=="evidence" else "accepted_by")
                    if proof_key:proof["record_key"]=self.nodes[proof_key].get("record_key")
        from workflow_relations import build_relations
        flows,relationships=build_relations(self)
        from workflow_navigation import build_navigation
        build_navigation(self)
        if not self.materials:
            self.diagnostic("materials_unmapped","Material responsibilities are unmapped; determine requirements for the current action",root_key)
        if not self.conditions:
            self.diagnostic("conditions_unmapped","Progression conditions are unmapped; this does not establish that all conditions are satisfied",root_key)
        if not self.entries and not flows and not relationships:
            self.diagnostic("governance_unmapped","Material responsibilities and progression conditions are unmapped; readable sources do not establish specification completeness",root_key)
        # Caller sees snapshot provenance, never a mutable gate status ledger.
        for path,expected in self.guard.observed.items():
            if revision(self.guard.path(path).read_bytes())!=expected:
                raise PanelDataError("revision_conflict","Sources changed during the governance read; refresh the view",409)
        focused=next((n["key"] for n in self.nodes.values() if n.get("ref",{}) and n["ref"].get("id")==focus),None) if focus else None
        return {"generated_at":datetime.now(timezone.utc).isoformat(),"project":page["project"],
                "nodes":list(self.nodes.values()),"edges":self.edges,"materials":self.materials,"conditions":self.conditions,
                "flows":flows,"relationships":relationships,
                "diagnostics":self.diagnostics,"coverage":{"structured":bool(self.entries or flows or relationships),"records_complete":self.complete,
                    "materials_mapped":bool(self.materials),"conditions_mapped":bool(self.conditions)},
                "source_revisions":[{"ref":{"path":p},"revision":r} for p,r in sorted(self.guard.observed.items())],
                "focus":focused}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root",required=True)
    parser.add_argument("--workspace")
    parser.add_argument("--focus")
    args=parser.parse_args()
    try:
        print(json.dumps(Governance(PanelData(args.project_root,workspace=args.workspace)).build(args.focus),ensure_ascii=False,indent=2))
    except (WorkflowError,PanelDataError,OSError) as exc:
        print(json.dumps({"error":{"code":getattr(exc,"code","read_failed"),"message":str(exc)}},ensure_ascii=False))
        return 2
    return 0
if __name__=="__main__":
    raise SystemExit(main())
