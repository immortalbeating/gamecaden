---
name: flow
description: Use only when the user explicitly requests Gamecaden for this work, or effective guidance in the current project has adopted Gamecaden. Handle development requests, continuation, and additions, adjustments or cancellation of ongoing work; locate original records and choose the appropriate path. Unrelated ordinary projects are not automatically adopted or migrated.
---

# Flow

First check the applicability conditions above; when they are not met, follow the original project guidance. See [Workflow applicability](../../shared/workspace.md) for boundaries.

Advance the current request to the result it actually requires, retaining existing project goals, records and authorization. Use applicable development experience and conventions to help the model choose design, engineering, content and verification methods, reduce known detours, and maintain the intended game direction. Choose concrete execution according to the task and available capabilities; records support judgment and continuation.

Resolve relative links in this document from the directory containing this SKILL.md; ../../shared/ points to shared/ in the common skill package root, not from the target project or skills/.

<a id="1-确认本次意图和现场"></a>
## 1. Confirm this work's intent and current situation

- Combine the current request with unfinished original work to identify discussion/understanding, implementation, verification, closure or adoption intent. Answer status questions during ongoing execution first, then continue the original goal unless the user explicitly stops or changes it.
- Prefer the project, directory, Task/Issue or established context specified by the user. Check effective guidance, workflow entrypoints and relevant runtime identifiers under the current path; search further only when the locating scope needs to expand.
- Read workspace/index when present; otherwise use clear existing guidance and project facts, checking actual roots and sources under [Workspace conventions](../../shared/workspace.md). A project name, directory name, open port or old handoff alone cannot prove that the target is correct.
- For read-only questions, first read what the question needs. Advance local work directly when relevant paths and records suffice; missing a complete set of workflow documents is not a global gate.

At the start of a new session handling a project request, restore relevant context according to effective guidance as appropriate; execution still follows this request's intent such as “continue/implement” or an explicitly authorized continuing run. Opening a blank conversation, having an active Task, or only asking for status does not automatically authorize advancing arbitrary old work. See the continuation reference for Skill discovery and host entrypoint mechanisms and limits.

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

init need only return target roots, authoritative locations and relevant gaps; flow does not create its own state or log files. Read init only when initialization is needed; ordinary execution through an existing entrypoint does not load it.

<a id="3-定位已有工作或选择管理方式"></a>
## 3. Locate existing work or choose management mode

When creating, continuing or writing back work, read the relevant parts of [Common record rules](../../shared/records.md). When restoring existing work, also read the [Continuation reference](references/resume.md).

When locating an original Task, candidate or applicability condition through the panel, obtain the derived view under [Panel continuation](../../shared/panel-workflow.md) and read back original sources. Established explicit constraints still apply; ordinary quick work does not acquire unrelated gates through this.

When the user adds content, changes goals, requests deferral or abandonment of ongoing work, read [Change handling](references/change-work.md). Handle the relationship to the original delivery first, then decide on expansion, upgrade, splitting, replacement or cancellation; do not treat every new message as a new task.

- The request repairs, supplements verification or adjusts an existing Task: use the original work and choose execution depth according to the current action.
- A new independent delivery has a clear goal and destination and can be completed directly with existing methods and inputs: quick lightweight mode is usually suitable.
- Ordinary delivery needs maintained solutions, steps, interface relationships, batches or ongoing follow-up: standard mode may be used, not only for major-risk work.
- Multiple results can be delivered independently and need common scope and integration judgment: coordinate through an Epic, with Tasks handling each result.
- Pure discussion, a one-time current-state answer, or maintenance of a management object itself: handle it in the corresponding document; do not create a task before every read/edit.

The model chooses management mode under [Task modes](../../shared/records.md#selecting-the-management-mode); judge verification needs and record storage separately. Available dependencies, session changes and report count alone do not determine mode; handle the boundary according to real maintenance needs. Record work with existing external sources according to their conventions, without changing it to another lifecycle unilaterally.

<a id="4-选择本次动作并实际推进"></a>
## 4. Choose and actually advance the current action

When choosing the next action, use the object being changed, actual consumers and delivery stage to locate effective constraints and materials that affect this work. When relevant requirements are unclear, read matching parts of [Rule selection](../../shared/rules.md) and [Material responsibilities](../../shared/material-requirements.md). Inherit existing applicable grounds directly; gaps constrain only actions that depend on them. Concrete methods follow the task and actual capabilities. When saving or handing off a solution in this work, cite key grounds affecting judgment back into original records under existing authorization and rule conventions.

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

User-supplied design and an explicit choice to skip brainstorm take effect directly. Investigate ascertainable facts yourself; decide ordinary reversible choices within authorized scope yourself. Clarify only unresolved matters that materially affect scope, compatibility, permissions or necessary acceptance. For user acceptance, first prepare a reviewable object, version and relevant differences; ask only about real choices or unverifiable facts. The model handles record IDs, storage and writeback according to source conventions; do not require users to specify technical persistence details.

This package provides a main entrypoint and seven responsibility Skills, shared tools and [Engineering profiles](../../profiles/README.md) as rule candidates. Read [Installation instructions](../../INSTALL.md) when installing, updating or checking host discovery; daily delivery directly uses actually available entrypoints. Judge specialized execution capabilities from the current environment, reading matching specialized Skills/project rules when needed. When tools or key inputs are genuinely missing, record the specific gap and pause only dependent actions.

Having all responsibility modules does not mean calling each one every time. An explicit quick change with sufficient checks can complete lightweight closure in the current execution; load corresponding verify/close guidance when coverage checks, independent review, complex closure or an explicit user request requires it.

When the original request requires implementation and inputs/capabilities suffice, continue execution after routing; “develop selected” does not complete the original request. Routing itself does not require a new session or subagent; collaboration follows current authorization and actual benefit.

<a id="5-保存结果并留下可续接的位置"></a>
## 5. Save results and leave a continuation location

- Save meaningful results, actual verification and the current next step in original records; shared conclusions cite original sources.
- When current implementation enters its declared baseline, promptly align affected Spec; update goals, routes or ledgers only when actually affected.
- In external claims, distinguish what was done, how far verification reached and what is missing. Use real results; do not replace evidence with file existence, report titles or summary status.
- At closure, judge completion against this work's commitments; changing sessions, generating reports or handing over unfinished items does not automatically close work.

Briefly report actual results and necessary limits to the user, with the corresponding record entrypoint. Leave a specific question only when the next step truly needs user input; otherwise continue the original request within original authorization.
