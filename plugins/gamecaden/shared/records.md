<a id="共同对象记录与交接"></a>
# Shared objects, records, and handoff

Workflow Skills read relevant sections when selecting, creating, restoring, or updating records. This page holds executable shared conventions; loading all content on every invocation is not required.

When creating/modifying new native records, read the corresponding sections of the [format contract](formats-v1.md) and blueprints in the [template catalog](../templates/catalog.md) as needed; do not load or copy everything at once. Before the first local I/O, check and prepare the isolated tool environment according to [local read/write tools](local-io.md#1-environment-and-invocation), then save, read back, and handle conflicts. Manually writing records does not establish validated tool invocation. Formats and interfaces refine this page's responsibilities without changing legacy sources or adding another copy of facts; operation names are not automatically installed host MCP commands.

<a id="1-文档职责"></a>
## 1. Document responsibilities

- Vision: complete product goals, core experience, design pillars, boundaries, and current key choices.
- Spec: effective rules and actual capabilities at a declared baseline, kept separate. Role diagrams/blueprints may constitute rules; unimplemented targets do not become current capabilities.
- Roadmap: outcomes, order, and necessary prerequisites, referencing carrying work and evidence of passing.
- PDP (Phased Development Plan): orchestrates a selected large solution into Epics, Stages, and carrying work; higher-level plans add no work lifecycle.
- Epic: bounded change, shared conventions, and overall acceptance. Its own management may be maintained directly; concrete implementation belongs to Tasks.
- Task: one concrete delivery; the main record explains goal, solution, acceptance, current results, and next steps, splitting details as needed.
- Parking lot: future ideas outside commitments. Committed later work stays in goals/routes; parking does not reduce scope.
- Notes: evidence-backed reusable understanding with applicability conditions; not automatically approval or project rules.

Organize user-provided design packages by responsibility and preserve sources. File formats and directory names do not automatically determine maturity, effectiveness, or runtime adoption.

<a id="项目级当前正文"></a>
### Current project-level bodies

At formal onboarding, establish definite current maintenance entry points in the selected workflow directory; if users explicitly specify another location, retain its unique entry point. Reuse existing content and specific references. Organize project-level bodies as below rather than substituting an entire mixed design package or development solution.

| Body | When to establish | Questions the body answers |
|---|---|---|
| vision.md | Establish the current vision at formal onboarding | Goals for the whole game, player experience and core loop, design pillars, boundaries, and important choices; express actual knowns and unresolved points when direction is unsettled |
| spec/index.md | Rules or implementation baselines already require ongoing maintenance | Which rules apply in which scope, which baseline actual capabilities belong to, current limitations, and maintenance entry points for detailed domain specifications/diagrams/data |
| roadmap.md | Established by default when formally adopting this workflow for ongoing project-level development | Committed outcomes, M milestones, order and necessary prerequisites, achievement conditions, and carrying work; current overall judgment references original facts |

Bodies should make their current conclusions independently understandable; references provide bases and detailed elaboration. Vision retains complete commitments, including unimplemented goals; unadopted branches belong in the parking lot, while unresolved points affecting direction are explained nearby. Spec separates effective rules, target solutions, and implemented capabilities. Roadmap owns product-outcome arrangements, PDP owns implementation Stage orchestration, and Task owns its steps and state. Retain unknowns when direction or implementation evidence is absent; file existence proves neither converged goals nor available capabilities.

Organizing effective rules requires identifying user adoption evidence or current authoritative maintenance scope. A single sentence, proposal, or expected check in original text alone does not prove adoption. When sources conflict without a clear priority basis, retain both and the unconfirmed scope while continuing independent work. Roadmap may contain only the current single confirmed outcome, explicitly stating unresolved future arrangements. If direction is entirely unsettled, retain actual knowns and unresolved scope. Engineering preparation, implementation, and test steps belong to original work/plans; do not manufacture extra outcomes to fill a route. Distinguish proposed from committed new outcomes.

Original north-star, GDD, development solutions, and other inputs retain original locations, versions, and specific section references; current bodies explain the adopted scope. Selected bodies own maintenance of their respective current direction/overview/route; original materials remain inputs, detailed designs, or history. If a legacy system genuinely maintains the same fact continuously, explicitly transfer or retain scope under onboarding authorization. Original sources may continue maintaining detailed domain rules, configuration, diagrams, and data; overviews explain effective scope and consumers without copying every parameter.

Subsequent changes update current bodies and genuinely affected original work according to [change handling](../skills/flow/references/change-work.md#4-synchronize-actually-affected-content). Daily continuation, read-only requests, and single local deliveries in legacy projects continue from existing sources. Apply this rule during formal onboarding or related onboarding repairs; package updates or missing new bodies do not block independent work. Task/Epic, asset ledgers, Manifest, Evidence, and Decision each retain their unique actual sources.

<a id="roadmap-的默认正文与推进"></a>
### Default Roadmap body and progression

The default four parts are: product/version scope and route basis; milestones and order; current overall judgment and outstanding items; sources and maintenance scope. The default outcome table uses these columns:

| Outcome/milestone identifier | Expected outcome | Achievement conditions or condition references | Necessary prerequisites | Carrying work and detailed materials |
|---|---|---|---|---|

New milestones default to M1, M2; continue referencing existing S/M/C and other identifiers. Precisely reference long conditions or overall exit criteria of Epics with the same scope. Roadmap defines only its own product-level conditions. Explicitly state unscheduled carrying work, unknown judgments, or pending necessary acceptance; complete table headings and all Tasks being closed do not prove outcome achievement.

When first arranging, expanding, or adjusting project/version routes, check the unique Roadmap and complete affected current bodies. Before the next stage, revisit its corresponding outcome and actual prerequisites. When valid results affect overall judgment, promptly update summaries and original Evidence/Decision references. Read detailed PDP Stage tables, Task steps/states, and original logs from their original sources; the route maintains only product-level conclusions. See the [Roadmap template](../templates/roadmap.md.tpl) for the default format.

<a id="大型方案到交付编排"></a>
### From large solutions to delivery orchestration

When users request phased implementation of a selected solution, or one/more large goals require continued batch implementation and combined checks, form a project/version-level plan under the [PDP contract](phased-development.md), clarifying current Epic/Stage divisions, inputs, and carrying destinations. Reuse sufficient existing orchestration directly; explicit quick fixes or simple Epics do not detour through PDP. Solutions are design content and choice outcomes, without new “solution states”; adopted scope and unsettled assumptions remain explained in original materials.

Generic Skills provide organization and gap judgment; effective, applicable project rules continue constraining work. When existing authorization or explicit new instructions change rules, save corresponding scope and basis. “As needed” cannot bypass still-effective requirements, and one project's rules cannot be imposed on other games.

<a id="2-选择和创建工作"></a>
## 2. Selecting and creating work

Task is the unified work object; quick is its lightweight mode and standard its regular mode. Both use the same identity, storage rules, and lifecycle.

<a id="选择管理模式"></a>
### Selecting the management mode

Mode describes the whole Task's organization and recording. For a specific step, choose depth according to current inputs, arrangements, and actual impact. Clear small fixes within standard may also be implemented, checked, and briefly recorded directly. Fixes, supplementary validation, and local adjustments within existing Tasks return to those Tasks; do not create same-goal work or change the original mode for one lightweight action.

| Mode | Suitable delivery form | Default handling |
|---|---|---|
| quick | A local delivery with clear goal and destination, sufficiently supported by existing methods/inputs for direct completion; a brief explanation supports execution and continuation | Execute after checking relevant conditions; save goals, necessary checks, actual results, and next steps |
| standard | Regular development requiring maintained solutions, implementation steps, interface relationships, batches, or ongoing follow-up; also applicable to key unknowns, risks, or collaboration requiring treatment | Save and maintain genuinely useful arrangements and intermediate judgments, directly reusing sufficient existing arrangements; suitable for low risk as well |

Whether dependencies affect mode depends on the need to coordinate other deliveries, confirm unavailable results, or maintain changing interface/version prerequisites. Reusing mature libraries, reading current specifications, or referencing available inputs may proceed directly. Ordinary session changes and saved next steps follow continuation rules. When handoffs genuinely require maintained responsibilities, input versions, or ongoing progression arrangements, choose mode based on those actual needs. Independent reports or handoff files do not themselves determine mode.

Test count, report count, code lines, Epic membership, step count, or one failure alone does not determine mode. Both follow applicable constraints, validation, and necessary acceptance; mode does not determine the quality floor or tool write protection. At the boundary, models choose according to actual maintenance needs, explaining related arrangements locally without separate mode-selection logs or asking users to choose labels; do not pursue a target quick-use ratio.

When scope or management needs substantively change, retain Task identity and reassess mode/arrangements. A simpler current step, body splitting, or report generation alone does not trigger reassessment. Use Epic + Tasks when multiple independent outcomes require shared progression. Split prose when only material volume increases; do not create Tasks because documents are long.

<a id="创建与保存"></a>
### Creation and saving

New workflows default to one directory per Task, with `tasks/T-<number>-<short-name>/task.md` as the main entry. At creation, safely derive the short name from title: retain Unicode word characters and hyphens, lowercase it, replace other character runs with hyphens, truncate to at most 64 characters, and trim leading/trailing hyphens/underscores. Use `work` if empty. Later title, quick/standard, or lifecycle changes do not relocate the main file; numbers remain stable and unreused within the project. Legacy flat `tasks/T-<number>-<short-name>.md` files remain readable/writable with default attachment directories `tasks/T-<number>/`; explicit original paths and Task identities do not change. Before creation, inspect actual numbering in mapped new-work sources and check for existing same-goal work. On concurrent conflicts, select a valid unused identity or coordinate rather than overwrite existing records.

When explicitly using flow to complete delivery in a project without legacy work sources, retain results in this project's default Task collection under [workspace conventions](workspace.md). Missing complete onboarding files is not a reason to leave results requiring retention only in chat. Do not establish this workflow for unrelated ordinary requests or when users explicitly request no records.

Minimal frontmatter for a new Task:

```yaml
---
id: T-001
title: Fix focus after returning from pause
mode: quick
kind: bug
status: active
epic: null
---
```

Fields illustrate the form rather than prescribe the actual title/state. Lifecycle states are planned, active, closed, cancelled; delivery acceptance, human acceptance, adoption, and release are judged separately. Quick may be briefly recorded after completion; on interruption, save necessary active/continuation information.

kind is an open label for the nature of work; neither it nor mode determines validation intensity. Optional depends_on expresses actually required results, while related expresses relationships only. The six required fields remain unchanged; body headings are not mandatory syntax.

Lifecycle alone does not permit execution. Explicit deferral may retain planned/active with user instructions and resumption conditions in the original record's current progression restrictions; read those restrictions when resuming. Specific routing for additions, changed goals, deferral, and cancellation is in [change handling](../skills/flow/references/change-work.md).

At quick start, briefly state goals, boundaries, and necessary checks/acceptance or original basis. As work progresses, answer what was done/changed, how it was validated, and impacts on specifications/ledgers; save unfinished items. standard maintains solutions, steps, dependencies, and important process details as needed. Both organize bodies around actual content; standard may also be brief, without empty sections. Task main records retain current understanding; split long designs, plans, and history into attachments with unique bodies as needed.

When splitting bodies in the new format, designs, the unique implementation checklist, and history may use `design.md`, `plan.md`, `history.md` in the Task directory. Source explanations, file inventories, and other Task-exclusive materials may use natural filenames in the same directory or purpose-specific subdirectories. Shared specifications, assets, and evidence retain original ownership and connect through references; Task creation does not duplicate materials or generate mandatory checklists. Continue using existing mappings and legacy flat-Task attachment paths; do not split mechanically by length thresholds.

When Quick is expected to wait, switch contexts, or run continuously, promptly save current goals and progress rather than waiting until completion for the first save. Unexpected interruptions cannot retroactively save content never retained; recovery uses the latest saved facts and actual scene.

<a id="实施安排与-planmd"></a>
### Implementation arrangements and plan.md

By default, keep sufficiently clear implementation arrangements in the Task. Judge the need for plan content separately from whether it needs its own file. Risks requiring order considerations do not automatically require new files.

Extract the unique implementation checklist when any of these actual needs occurs:

- The user/effective project conventions require a separate plan, or an existing separate implementation document is continuously used. In the latter case, retain its original path/name (such as implement.md) rather than create another plan.md.
- Branches, sequential dependencies, batches, or recovery/rollback arrangements within the same Task require repeated execution, handoff, or review as an independent checklist, which embedded content no longer clearly supports.
- An evolving plan noticeably crowds the main record, making goals, acceptance, current results, and next steps hard to locate; extraction clarifies both reading purposes.

Cross-session work, many modified files, many steps, many validation runs, or standard mode alone does not justify splitting. Models decide based on those purposes and briefly explain reasons; routine document organization requires no extra approval.

A Task's plan.md owns internal implementation steps and order, with results, prerequisites, checkpoints, waiting/rollback arrangements when needed, linking actual execution evidence. Existing Epic plans maintain orchestration of deliveries within that Epic and reference actual Tasks. Higher-level phased orchestration of large solutions uses [PDP](phased-development.md); Stage tables already maintained by PDP are not duplicated in Epics. Original Tasks/Epics retain overall goals, acceptance, and current results, referencing plans; design rationale remains in design bodies.

If multiple independently deliverable/acceptable outcomes actually emerge, split work through Task/Epic relationships rather than permanently hide them in a huge plan.md. File splitting alone does not change Task identity, mode, or lifecycle; reassess under shared rules when scope/risk substantively changes.

<a id="3-归属依赖和旧来源"></a>
## 3. Ownership, dependencies, and legacy sources

A Task belongs to at most one Epic; independent/cross-Epic shared work may use null. Dependent Tasks declare the results and states required for specific execution, without uniformly requiring upstream administrative closure. Overall exit conditions belong to Epics/milestones. PDP Stages maintain only their unique combined checks, precisely referencing other original conditions. Define identical conditions once; stage arrangements do not change Task Epic membership.

New Epics default to epics/E-<number>-<short-name>/epic.md, with id, title, status frontmatter. Bodies explain shared goals/boundaries, conventions, deliverable references, overall acceptance, and current unresolved items. Create only when multiple deliveries actually require coordination and save under the mapped default Epic source; do not establish a separate implementation path without Tasks inside Epics.

Operate legacy-system work first according to actual formats/conventions, preserving original identities and paths. These examples do not authorize forced rewriting of legacy YAML/states. Adopt new maintenance rules only after workspace declares the switch and objects have actually been transferred.

<a id="4-验证决定和记录形态"></a>
## 4. Validation, decisions, and record forms

Evidence preserves subjects/necessary versions, methods/environment, actual observations/conclusions, coverage, and sources. It is a responsibility for check facts; `EV-*` is a native record form, screenshots/logs are basis materials, and complete tool reports may fulfill the responsibility. Independent reports remain independent reports inside Task material directories; neither file suffix nor EV count determines evidence sufficiency.

<a id="留存索引与版本"></a>
### Retention, indexing, and versions

| Actual purpose | Default retention and escalation |
|---|---|
| Temporary debugging or exploratory trial runs not yet used for acceptance/decisions | Use project-permitted temporary outputs; briefly record useful continuation findings in the Task rather than permanently archive every trial. |
| Checks for simple local deliveries | Briefly record subject/baseline, method, results, and limitations in the Task, linking necessary materials; no separate report is needed for one sufficient small check. |
| Stage/Epic exits, independent review, formal asset review, or results requiring cross-task reuse/version comparison | Default to independently locatable evidence records/reports; original Tasks/Epics summarize current conclusions and stable references. One check batch may correspond to one record; do not assign EVs to every screenshot. |
| Existing complete tool reports | Adopt original reports directly, adding genuinely missing subject/scope explanations; when native queries/condition matching genuinely need it, use supported adaptation or create a short EV index referencing the report. |

New screenshots, logs, and reports exclusive to this Task default to `evidence/` inside its material directory. Separate multiple check rounds by check name and round. Native independent EVs default to the workspace Evidence source; existing reports, shared evidence, and legacy attachments are referenced at original locations. Main Tasks/Epics must directly reach current-round results. Independently discoverable reports use Evidence sources/indexes; index existing reports within Task collections rather than add overlapping collections. EV indexes own subject/version, conclusion/coverage, and report references; original reports still own methods and raw observations.

Once results are used for review, acceptance, or decisions, move necessary reports/basis into stable retention. Subsequent reruns, method changes, or substantive corrections use new rounds/records. Save minimal sufficient history and original conclusions explainable through old references; do not overwrite referenced old reports with same-name copies. Append explanatory errata. Update current Task summaries and genuinely affected decision/specification references. When synchronization is incomplete, state respective baselines and pending actions; do not combine unaligned results into a current overall pass.

Decision preserves who chose what for which subjects and scope. Single local choices/acceptances for this Task may record subjects, necessary versions, decision-makers, and scope nearby. When ledger/engineering adoption or multiple works need the same decision, batch review, or separate withdrawal/replacement by subject/aspect/use, default to an independently locatable decision record. Native records may be independent or embedded, retaining unique identities. Recording existing user decisions does not add approval requirements. Attribute model recommendations or authorized delegated judgments separately rather than record them as personal user acceptance.

Independent records may serve multiple works; original Tasks only reference them. When extracting embedded records, preserve identities and locatable references; do not maintain another complete body at the original location.

Reuse requires checking current subjects, scope, and necessary conditions. New sessions, older dates, or unrelated changes alone do not require revalidating everything.

Specific coverage, reuse/invalidation, independent verification, and check conclusions follow [validation conventions](verification.md); conclusions do not create another Task lifecycle.

<a id="5-游戏资产与采用"></a>
## 5. Game assets and adoption

Asset master ledgers preserve identity, sources, uses, candidates, and designated selection/replacement relationships. manifests preserve technical file facts; Decisions preserve acceptance/permitted scope; engineering consumers and their Evidence establish actual integration.

Judge adoption separately by candidate version, use, consumer, and baseline. If the same material is permitted for A/B and A succeeds while B fails, preserve the approved scope and truthfully record partial results. Approval does not establish complete integration; B's failure does not rewrite original approval as withdrawn.

Producing candidates, accepting appearance, formal adoption, and release are different commitments. Advance the user's original goal without reducing commitments through renaming or splitting later Tasks. Missing necessary acceptance pauses only actions dependent on it.

For actual production/integration, read [asset handoff and adoption](asset-handoff.md) rules for identity, ledger updates, batch decisions, panel write-back, and partial integration; the above ownership of facts stays unchanged.

<a id="6-当前事实关闭与汇总"></a>
## 6. Current facts, closure, and aggregation

Write back to original Tasks/Epics when important results arrive, blockers/pending reviews arise, or during handoff/closure. If results affect product outcomes/current overall judgment, synchronize Roadmap summaries and original bases; if they affect Stage orchestration, synchronize corresponding PDPs. Update Spec promptly after facts enter its declared baseline. For shared-rule changes, first align effective scope and decisions; the responsible Task may perform write-back, while Epic closure checks gaps and integrates.

Tasks close according to their own commitments and necessary conditions; Epics are judged by overall acceptance. All child Tasks being closed does not automatically establish overall completion. Handoff of remaining items only establishes their destinations, not fulfillment of commitments still in current scope.

If original closure was correct at the time, later requirements/regressions belong to work for the current change. If original closure is found to have been mistaken then, preserve historical explanation and reopen the same work as needed. On explicit goal changes, record affected objects' destinations and old/new relationships.

Progress/Timeline aggregate original records, stating sources and aggregation times; they do not prove original records passed. Saving, refreshing, and retention follow [derived outputs](derived-outputs.md). New views use JSON/HTML rather than another Markdown progress body. Ordinary events are not duplicated in a separate aggregate log; do not change dates in unchanged files merely to leave traces.

Actual closure is handled by [close](../skills/close/SKILL.md) according to current intent; its references cover scope adjustments, overall exits, historical misjudgments, and partial write-back. Daily quick fixes may directly fulfill the same information responsibilities without another ritual round.

<a id="7-续接与独立交接"></a>
## 7. Continuation and independent handoff

Pass on the following before the next action: the user's current request, actual project/runtime roots, original work identifiers and sources, current scope and next action, applicable records, and specific gaps.

This may be a brief explanation in current context; a new handoff file is not required. For writes, check original sources and actual roots before acting. Existing authorization remains valid. If missing information would substantively change goals or permissions, prepare specific questions while continuing independent available work.

When users genuinely need independent handoff or effective project conventions require it, export a snapshot from updated original records according to [independent handoff](derived-outputs.md#standalone-handoff), retaining actual scope, baselines, evidence, and next steps. The default location is handoffs/; regeneration saves a new version, while subsequent work still updates original records.

<a id="8-按实际问题整理"></a>
## 8. Organize according to actual problems

| Trigger | Organization action |
|---|---|
| Long process narratives obscure current goals, effective conclusions, or next steps | Retain current understanding in the main record; extract designs, the unique plan, or history needing repeated reading into original work attachments with precise references. |
| The same fact is updated repeatedly in multiple bodies, or original reports need sharing | Establish one maintenance source and replace other locations with summaries/references; escalate evidence/decisions according to the purposes above. |
| Broken entry points, mixed evidence rounds, or source lists overwhelmed by receipts/historical payloads | Repair specific references, version relationships, or source scopes; default locations and mappings follow [workspace](workspace.md), while original identities/history remain locatable. |

Do not periodically move files based on dates, word counts, or Task closure counts. Before deleting/overwriting, check still-valid references and project retention policies. Treat rebuildable caches separately from current evidence, candidate sources, and unsettled I/O receipts. Directory organization does not change acceptance, adoption, or work lifecycles.
