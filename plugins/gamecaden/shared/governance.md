<a id="材料约束与推进条件"></a>
# Materials, Constraints, and Progression Conditions

This contract is the shared semantic entry point for the panel, Skills, and tools. Definitions remain with their original owners: long-term rules belong to Spec, overall exits to Epics/milestones, and execution prerequisites to the dependent Task; [PDP](phased-development.md) Stages define only their distinctive combination checks. Conditions in the same scope reference their original definitions rather than being maintained repeatedly in Roadmap/PDP/Epic. The panel is a sourced derived view, not a second progress or approval ledger.

<a id="准入与适用性"></a>
## Admission and Applicability

Include only sources and sections responsible for goals, specifications, work, materials, evidence, or decisions. Registration means they can be located, not that their content is complete or adopted. Express effective, candidate, reference, historical, and unknown separately; parking lots do not become current commitments. See [material requirements](material-requirements.md) for triggers, equivalent forms, and timing for character, map, and other materials.

Missing necessary materials may still be registered as requirement entries, with source refs empty and missing displayed. applicability=unknown means applicability has not been verified; not_applicable must come from a reasoned judgment for this work. Tools do not infer completeness from file counts or closed-task counts.

When declaring not_applicable, save the rationale in applicability_reason. materials.applies_to can locate affected work; when omitted, it inherits this Task/Epic's affected objects; omission in other documents means objects have not yet been limited. rules.layer distinguishes common/domain/engine/project source layers; layers are not a mandatory precedence order.

<a id="同一来源中的可选结构"></a>
## Optional Structure Within the Same Source

When shared display of hierarchy, materials, and conditions is needed, put an annotation block in the original Markdown body. Not every file needs annotations, and existing ordinary records need not migrate to new objects. At most one block per source record; id is local to the file, and cross-references use the original file path plus fragment. The body continues explaining definitions; the machine block maintains only the portion needing structured reuse, avoiding two maintained condition lists.

~~~~text
<!-- workflow:governance -->
```json
{
  "schema_version": 1,
  "materials": [{
    "id": "map-blueprint",
    "title": "Buildable spatial blueprint",
    "domain": "map",
    "requirement": "required",
    "applicability": "applies",
    "for_actions": ["Formal map production"],
    "purpose": "Define scale, connections, entrances, and consumers"
  }],
  "conditions": [{
    "id": "production-ready",
    "title": "Spatial relationships have production grounds",
    "domain": "map",
    "scope": "Level A",
    "action": "Formal map production",
    "strength": "required",
    "authority": "effective",
    "applies_to": [{"id":"T-004"}]
  }]
}
```
<!-- workflow:endgovernance -->
~~~~

This example has no material ref or check grounds; its read result is missing materials and unverified conditions. It does not block graybox experiments on other objects.

Exact fields are owned by the [schema](../schemas/governance-v1.schema.json):
- outcomes: outcomes/milestones and references to work that delivers them; does not store work states.
- New milestones use M identifiers by default; PDP S identifiers are implementation segments within a document. Original anchors or existing flows can express necessary relationships, without expanding Stage into another managed object. Annotate original definitions only when structured display is actually needed.
- rules: constraint nature, domain, scope, and applicable objects.
- materials: required information, applicability, purposes/actions, and original material references.
- conditions: affected objects, restricted actions, strength, adoption nature, and judgment grounds.
- Existing Task.epic / depends_on / related retain ownership of their original relationships; reference, membership, and required results do not substitute for one another.
- flows / relationships declare action-prerequisite combinations and specification-responsibility relationships as needed; see [relationship expressions](relation-views.md). They do not separately store work state or authorization.

outcomes.work references work delivering an outcome; referencing one work item cannot make it an execution prerequisite for all related work. conditions.applies_to explicitly lists objects; Epic membership alone does not spread blocking to every Task. Multiple objects may reference a common condition without copying its definition.

<a id="判断与来源"></a>
## Judgment and Sources

A condition without check is unknown; the model or designated judge analyzes it and saves grounds in original Evidence/Decision. check uses the original Subject format and must bind a version; kind is evidence or decision, and actor_kind may be restricted. proofs provides precise references; when omitted, search registered corresponding records for strictly matching grounds.

- Object, candidate, version, scope, and use must all match. When coverage is supplied, Evidence must also cover the specified items.
- Evidence passed/failed supports only its declared coverage; qualitative model checks may be carried by agent Evidence but cannot masquerade as actual runtime tests.
- Decision accept supports its explicit scope; reject/revise means that scope is unmet; use actor_kind=user when a user decision is required.
- A Decision event's overall scope must also match Subject.scope by default; first semantically check multi-object events whose overall scope differs, then explicitly bind their original overall scope with check.event_scope.
- Withdrawn or superseded events are invalid; conflicting effective grounds within the same scope display unknown.
- Changes to current file/manifest digests display stale; unverifiable version forms, missing grounds, or broken references retain unknown.
- Candidate, reference, and historical rules do not become effective hard gates. Only effective + required indicates a prerequisite for the corresponding action.
- condition states are satisfied/unsatisfied/unknown/stale/not_applicable; material states are located/missing/unknown/not_applicable. They do not change Task planned/active/closed/cancelled.

Tools check sources, versions, and record declarations. The corresponding Skill still judges evidence sufficiency, user authorization, and whether the next step is appropriate. satisfied does not automatically authorize production, close a Task, commit Git, or wake an Agent.

The applicable Task and check Subject may differ: Tasks often consume an asset, blueprint, or upstream result. The condition definition declares why that check supports this action; tools do not guess business relationships from whether their IDs are equal or different. Views show both and the original definition for review. coverage separately explains whether structure exists, materials/conditions are recognized, and record scanning is complete; the presence of any one part does not mean the whole project is recognized.

<a id="新旧项目"></a>
## New and Legacy Projects

init first judges material responsibilities and adoption scope; design fills in actual content needed by current actions. Original materials can be referenced; handle mixed documents by section, and structure corresponding parts only when relationship display is needed. While legacy sources remain read-only, the panel lists registered materials and explicitly indicates “governance unrecognized”; it cannot guess unknown tasks or generate a green light from the word “passed.”

Before adding annotations to legacy projects, confirm who maintains the corresponding definitions. Current conditions may be defined in an authorized current Task referencing legacy materials, without copying their bodies or old task states. Leave clear paths to resolve missing, conflicting, and unknown items rather than generating empty templates for the entire project at once.

<a id="使用"></a>
## Usage

[Panel and responsibility coordination](panel-workflow.md) explains timing, context, and readback. `workflow_governance.py --project-root ... --focus T-004` outputs a read-only model; `GET /api/projects/<id>/governance?focus=T-004` provides the same view. Nodes and edges serve only navigation and explanation; rebuild them when source revisions change, without saving independently editable aggregate states.
