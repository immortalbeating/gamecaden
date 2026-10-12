<a id="推进条件与规范来源视图"></a>
# Progression Conditions and Specification Source Views

Read this when cross-action prerequisites or multi-level specification responsibilities need explanation. These views reuse the [governance contract](governance.md) and original records without adding tasks, approvals, or progress stores.

<a id="选择表达"></a>
## Select an Expression

| Question to answer | Definition and view |
|---|---|
| What results this action needs, and which downstream actions gaps affect | flows in original sources; progression condition graph |
| Who defines rules, delegates responsibilities, produces or consumes outcomes | relationships in original sources; specification source graph |
| Only direct relationships or a local quick fix | Use existing Task dependencies, conditions, and original text; no need for a full set of annotations |

Provide all definitions according to actual project scope. Grouping aids reading and does not imply order; expressions explicitly reference prerequisite results. Project-specific stages, numbering, and approval methods do not become default requirements in other projects.

<a id="flows原动作的前提定义"></a>
## flows: Prerequisite Definitions for Original Actions

Add flows to original workflow:governance blocks as needed. Each flow supplies id, title, scope, authority, and nonempty steps; each step supplies id, title, target, action, and optionally group and requires. target locates original affected objects and action corresponds to actual actions. Steps are not another Task and do not separately store state.

requires is a single-key expression that supports recursive combinations:

```json
{"all": [{"step": "candidate"}, {"condition": {"path": "./production.md", "fragment": "visual-choice"}}]}
```

- condition references original conditions; path/fragment and source/project qualifiers remain validated.
- step references a step id in the same flow, requiring results of its declared prerequisites.
- all requires all applicable items to be satisfied; any requires one applicable branch to be satisfied; combinations contain at least one item.
- Without requires, retain unknown; Task closed, material located, and file existence cannot fill judgment gaps.

Condition leaves support step judgments only when effective, required, matching affected objects, and the same action. References, proposals, recommendations, wrong objects, or wrong actions remain unknown. Proof still checks the original condition's Subject, version, scope, use, coverage, and actor requirements. User-decision conditions use matching user Decisions; machine Evidence does not replace them.

| Combination | Judgment |
|---|---|
| all | Exclude explicitly inapplicable items; any unmet item means unsatisfied, all remaining items satisfied means satisfied, otherwise unknown takes precedence over stale |
| any | Any applicable item satisfied means satisfied; otherwise unknown takes precedence over stale; all remaining applicable items unmet means unsatisfied |
| All inapplicable | not_applicable, not recorded as a pass |
| Cyclic references | All cycle members remain fixed at unknown; layout or declaration order does not change conclusions |
| Ineffective flow, broken reference, or invalid definition | Retain unverified status and diagnostics, without generating readiness conclusions |

These results explain only declared prerequisites. satisfied does not authorize implementation, acceptance, closure, or release. Downstream relationships are rederived from sources, and each downstream action is still judged by its own expression.

<a id="relationships职责与来源"></a>
## relationships: Responsibilities and Sources

Each item supplies id, from, to, kind, authority, and optional label. Both endpoints use original Refs; edges retain declaration source and version.

| kind | Relationship meaning |
|---|---|
| delegates_to | Definer delegates part of its responsibilities |
| defines | Source defines corresponding rules or objects |
| provides_policy | Source provides judgment policy for the work |
| produces | Work or production responsibility produces outcomes |
| consumes | Work or consumer responsibility reads inputs |

These serve navigation and responsibility explanation, not prerequisite calculation. Existing contains, supports, references, requires, governed_by, verified_by, accepted_by retain their meanings. Specification definitions and instance facts in Tasks, assets, Evidence, and Decisions are displayed separately.

<a id="使用和回读"></a>
## Usage and Readback

The panel overview offers a “Progression conditions / Specification sources” switch. Specification sources default to a collapsed project-domain overview organizing read sources; expand domains and documents to read actual documents and included content. “Sources and impact” reuses the same original nodes and relationships. Entering a domain defaults to the document tree reader: the left is the actual inclusion tree and the right shows actual section bodies of the selected document; switch to a focus relationship graph as needed without treating the document tree as an execution tree. Both source-graph perspectives support vertical/horizontal layouts; focusing a domain retains directly connected one-hop external endpoints. Back navigation, panel refresh, and switching back to projects retain still-valid reading selections, sections, expansion, zoom, and positions in the current session; memory is isolated by project binding and does not promise recovery after a full browser-page reload. Current relationships are local, and registered scope does not mean all project standards have been recognized. Flow selection, collapse, and zoom are display settings and do not change sources.

Node details display responsibilities, ownership, sections, prerequisites, proof, definitions, and downstream actions referencing the result; aggregate relationships can be read back individually to each original relationship. Original-text buttons apply only to registered readable sources and locate precisely by body heading or governance id; retain location and check notices for unregistered, missing, or multiply named targets. Narrow screens use domain/document/step lists and full details. Read sources without navigation, unclassified materials, and isolated documents remain available; projects need not add annotations for the interface.

When returning to the foreground, use `GET /api/projects/<id>/revisions` to check registered physical source versions; unchanged versions do not load full data, changes trigger coalesced refresh, and successful writes update affected records. Defer during editing, dialogs, or busy states without changing draft baselines or frozen requests; missing sources or changes during reading are not treated as unchanged. Lightweight checks are neither gates nor engineering synchronization; see [panel coordination](panel-workflow.md) for boundaries. See [reader and refresh design](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/panel.md) and [verification](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md) for current scope.

GET governance and the command line continue using the same read-only model, compatibly adding flows and relationships, with expected_check on conditions explaining judgment types. Step condition_keys, predecessor_keys, affected_keys are reference results for this round; affected_keys does not mean those actions are necessarily blocked.

Definitions embedded in EV/Decision belong to the actual embedded record and are not reinterpreted by the outer layer. Local ID conflicts, source changes during reads, and invalid qualifiers continue raising errors or retaining unknowns rather than being overwritten by read order.

Fields are owned by the [schema](../schemas/governance-v1.schema.json); see the [derived module](../scripts/workflow_relations.py) for implementation. See [design](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/panel.md) and [verification](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md) for this round's scope and results.

<a id="只读文档导航合同"></a>
## Read-only Document Navigation Contract

The original `workflow:governance` block may include a `navigation` object permitting `domain: string`, `responsibility: string`, and `parent: Ref`, with at least one field and all others rejected. It describes reading ownership of source records, adding no dependencies, gates, or states and changing no rules, flows, conditions, or authority calculation.

Record nodes derive `navigation_domain`, `navigation_responsibility`, `navigation_parent_key`, and `navigation_source_key`; without declarations these are null, with no inferred domains. Declaration sources point to the current record node, with source versions inherited from node `revision`. Parent and child endpoints must both be read `document` nodes; original Ref source, project_id, and id qualifiers remain validated, and unregistered sources are not read to complete navigation. Self-references, cycles, broken references, and non-document parents retain `invalid_navigation`, `invalid_navigation_parent`, or `navigation_cycle` diagnostics rather than generating corresponding parent-child relationships or passing conclusions. Navigation relationships are expressed only by `navigation_parent_key`, not added to `edges`.

Read records also derive `headings: [{text, level, fragment}]`, ignoring fenced code, governance JSON, and embedded record examples; headings of embedded native records belong to those records. fragment is original body heading text for reader positioning and claims no separate file or approval fact. Headings and navigation metadata are derived only during reads; original text still comes from original records.


Optional navigation fields can be merged into an existing governance block in the original body; for example, a child document declares its reading domain and an already read parent document:

````markdown
<!-- workflow:governance -->
```json
{
  "schema_version": 1,
  "navigation": {
    "domain": "Maps and levels",
    "responsibility": "Explain room connections and routes",
    "parent": {"path": "./level-design.md"}
  }
}
```
<!-- workflow:endgovernance -->
````

The example expresses only reading inclusion relationships. Body headings derive from headings; original governance entries can use `{"path":"./level-design.md","fragment":"route-check"}` to read back the definition whose id is route-check, without treating fragment as a second state. parent must resolve to document; the example does not treat rule entries as parent documents. Existing rules, conditions, flows, and other fields remain in the same block rather than creating duplicate governance blocks or state records. See [domain design](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/panel.md) and [verification for this round](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md) for current entry points.
