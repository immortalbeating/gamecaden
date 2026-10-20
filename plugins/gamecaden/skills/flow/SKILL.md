---
name: flow
description: Use only when the user explicitly requests Gamecaden for this work, or effective guidance in the current project has adopted Gamecaden. Handle development requests, continuation, and additions, adjustments or cancellation of ongoing work; locate original records and choose the appropriate path. Unrelated ordinary projects are not automatically adopted or migrated.
---

# Flow

Apply the [workflow applicability boundary](../../shared/workspace.md#workflow-applicability) before using this responsibility.

Advance the requested result while retaining adopted game direction, original records and authorization. Choose methods from current goals, applicable guidance and available capabilities.

Resolve links from this Skill's directory; ../../shared/ is the package's shared/ directory.

<a id="1-确认本次意图和现场"></a>
## 1. Confirm this work's intent and current situation

- Combine the current request with unfinished original work to identify discussion/understanding, implementation, verification, closure or adoption intent. Answer status questions during ongoing execution first, then continue the original goal unless the user explicitly stops or changes it.
- Start from the specified project, Task/Issue or established context. Check effective guidance, workspace/index when present and actual runtime identifiers; expand searches only for unresolved location questions. [Source locations](../../shared/workspace.md#1-locations-and-resolution) apply; names, open ports or old handoffs alone do not identify the current target.
- For read-only questions, first read what the question needs. Advance local work directly when relevant paths and records suffice; missing a complete set of workflow documents is not a global gate.

Restore relevant context for a new project session under the continuation reference. Execution still needs the current continuation/implementation request or an existing authorized run; a blank chat, active Task or status question alone does not authorize advancing old work.

At the end of this judgment, be able to explain the current goal, actual operation scope, who maintains the original records, and which missing information would affect the next action.

<a id="2-按需建立接入关系"></a>
## 2. Establish adoption relationships as needed

| Situation | Handling |
|---|---|
| An effective entrypoint exists | Reuse it; do not initialize again because the session is new |
| Roots or sources are unclear | Read [init](../init/SKILL.md)'s inspect mode to establish them first |
| Explicit request to adopt/complete the workflow | Use init adopt/repair, then continue the original request |
| The specified scope switches maintenance responsibility for old records | Use init migrate; retain old identities and history |
| Only reading an old project or repairing its existing work | Continue from old sources; do not expand the request into migration |
| Explicit flow invocation for delivery, with a unique target and genuinely no old work source | Save this Task under common conventions as appropriate; handle complete project adoption separately according to actual need |

Read init only for these adoption/location needs; it returns roots, original sources and relevant gaps. Flow keeps no separate state or log.

<a id="3-定位已有工作或选择管理方式"></a>
## 3. Locate existing work or choose management mode

Reuse the original Task for repairs, supplementary checks and local adjustments. For creation, splitting or changed organization, use [Task modes](../../shared/records.md#selecting-the-management-mode); for restoration, use the [continuation reference](references/resume.md).

Read known sources directly. Use [derived views](../../shared/panel-workflow.md) for cross-record discovery or overviews when needed, then read back original sources and matching constraints.

When the user adds content, changes goals, requests deferral or abandonment of ongoing work, read [Change handling](references/change-work.md). Handle the relationship to the original delivery first, then decide on expansion, upgrade, splitting, replacement or cancellation; do not treat every new message as a new task.

Coordinate independently deliverable results through an Epic when shared scope/integration needs it. Discussion, one-off status answers and maintenance of management objects do not create Tasks automatically. The model chooses mode by real maintenance needs; verification is a separate judgment. Retain external systems' original conventions and lifecycle.

<a id="4-选择本次动作并实际推进"></a>
## 4. Choose and actually advance the current action

Use changed objects, actual consumers and delivery stage to select effective grounds. For unclear applicability, consult [rule selection](../../shared/rules.md#1-select-sources-for-current-work) or [material domains](../../shared/material-requirements.md#domain-triggers). Reuse valid grounds; gaps constrain dependent actions only. Cite key grounds when saving the solution.

| Request and materials | Current action |
|---|---|
| Only asking about or reviewing current state | Read relevant facts and answer/review |
| Core direction still needs comparison | Read [brainstorm](../brainstorm/SKILL.md), resolve relevant differences and save to the corresponding location |
| Requirements exist but a necessary solution is missing; or explicit design/solution review request | Read [design](../design/SKILL.md), form or review this arrangement |
| A selected large solution needs phased delivery, or an explicit phased development plan request | Read design and [PDP](../../shared/phased-development.md), reuse the original solution and arrange Epic/Stage/Task; pure planning does not automatically implement |
| Executable design exists or an explicit engineering quick change | Read [develop](../develop/SKILL.md), implement and perform necessary verification directly; do not load brainstorm/design merely to complete a sequence |
| Content production, reuse, revision, or delivery after review | Read [assets](../assets/SKILL.md), produce and retain for the specific use; coordinate with develop when integration is included |
| Engineering integration or reference repair of existing materials | Use develop and check asset handoff and allowed scope; no need to produce again |
| Verification, review, or checking whether delivery is possible | Read [verify](../verify/SKILL.md), judge coverage and results for the specified target; do not automatically expand into release |
| Closing a Task/Epic or handling closure conditions | Read [close](../close/SKILL.md), retain actual commitments, valid evidence and existing authorization |

Before first performing a responsibility selected above, load its guidance, including when switching responsibilities within one long session. Use an available host Skill invocation or read the linked SKILL.md and applicable references; naming a route or loading flow/resume alone does not load those bodies. Reuse guidance already in context and still applicable; after context loss, restore what the next action needs. The quick execution exception below remains applicable.

Reuse supplied design and explicit choices to skip brainstorm. Investigate facts and decide ordinary reversible choices within scope. Clarify unresolved scope, compatibility, permission or acceptance tradeoffs only; prepare concrete objects/versions/differences before acceptance questions. Handle record IDs and persistence under source conventions.

Use actually available host entrypoints and specialized capabilities. Read [installation guidance](../../INSTALL.md) for installation/discovery questions only; missing tools or inputs pause dependent actions, not unrelated work.

Having all responsibility modules does not mean calling each one every time. An explicit quick change with sufficient checks can complete lightweight closure in the current execution; load corresponding verify/close guidance when coverage checks, independent review, complex closure or an explicit user request requires it.

When the original request requires implementation and inputs/capabilities suffice, continue execution after routing; “develop selected” does not complete the original request. Routing itself does not require a new session or subagent; collaboration follows current authorization and actual benefit.

<a id="5-保存结果并留下可续接的位置"></a>
## 5. Save results and leave a continuation location

Save results, verification and next actions under [common writeback rules](../../shared/records.md#6-current-facts-closure-and-aggregation). Align affected Spec when behavior enters its declared baseline; update other goals/ledgers only when affected. Completion follows original commitments, not report or handoff creation.

Report actual results, limits and the original record entrypoint. Ask only for needed user input; otherwise continue authorized work.
