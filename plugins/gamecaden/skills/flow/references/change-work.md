<a id="执行中的范围变化暂缓与废弃"></a>
# Scope changes, deferral and abandonment during execution

Read when users add requirements, change goals, request a pause or abandonment of existing work. First understand this message's relationship to original delivery; discussing a possibility does not automatically change commitments. An explicit addition/modification request follows the new requirement, without asking again about the same decision.

First identify whether the changed object is a goal, scope, implementation solution or timing. When a solution is abandoned but the delivery goal retained, continue the original Task with another solution; seeing “abandon” alone does not cancel the entire work. Classify clear objects yourself; clarify only substantive ambiguity.

<a id="1-先处理正在发生的工作"></a>
## 1. Handle ongoing work first

Retain original goals that the user has not revoked. Stop advancing explicitly abandoned, paused or replaced actions at the next controllable safe point; for operations started by this task that are still running, check their identity, then interrupt according to tool capability or record returned results, without affecting other work.

When added scope is independent of the current action, currently authorized work can continue; when it makes current implementation meaningless, first save the situation and reorder the next action. Then write key changes back to original work before advancing affected new implementation.

<a id="2-同一-task-还是新-task"></a>
## 2. Same Task or a new Task

| Nature of change | Handling |
|---|---|
| Clarifying requirements, repairing, supplementing verification or changing implementation method while retaining the same deliverable result | Update the original Task; do not create another task with the same goal |
| Adding closely related necessary content still suitable for joint delivery and acceptance | Expand original Task scope/acceptance and retain its ID; reassess under common mode rules when management needs materially change |
| New content can be independently delivered, accepted or handed off | Create an independent Task; coordinate through an Epic when common scope and integration require it; do not mix it into the original task merely because it is “while you are at it” |
| One original work expands into multiple independent results | Split according to actual delivery; create an Epic if needed. The original Task may remain one explicit subdelivery; record the split mapping |
| Another work replaces the original delivery and retaining its ID would confuse its meaning | Record cancelled and the replacement destination in unfinished original Task, with an appropriate Task for the new goal; preserve historical completion of completed old tasks |
| User explicitly no longer wants the entire unfinished delivery | Cancel the original Task, retaining results already obtained, reasons and affected dependencies |
| Only part of the original Task is cancelled | Update original scope and remaining acceptance; retain work still required without automatically cancelling the entire Task |

Judge whether delivery remains the same, whether it can be independently accepted and what coordination requires; do not mechanically classify by file count, word count or development time. Major implementation changes may still be the same delivery; a single added requirement may introduce an independent system.

Express the same meaning through the actual lifecycle of work from old systems, without forcing new formats. Changing work ownership does not automatically expand authorization to modify other tasks or directories.

<a id="3-暂缓与取消分别保存"></a>
## 3. Save deferral and cancellation separately

Deferral means work remains, but currently must not continue under its original plan. Retain the existing planned/active lifecycle and state the user instruction, scope and resumption conditions in the original Task's “Current continuation/advancement constraints”; retain this decision in important history as needed. Do not create another set of paused tasks or disguise status as closed.

Deferred committed work still belongs to its original Task/Epic; do not put it into a parking lot and make it an optional idea.

Example: `Advancement constraint: The user deferred this task; do not continue its implementation until explicitly resumed. After resumption, first check the current candidate and integration situation.`

Resumption selection cannot rely on active alone. A general “continue the project” does not automatically lift explicit deferral of particular work; explicit continuation of that task can lift the user deferral, but originally applicable conditions such as verification and acceptance must still be judged.

Cancellation means the unfinished goal will no longer be fulfilled; retain the Task and history by default and use cancelled. Cancellation does not automatically delete code/materials, roll back adopted content, revoke approval in another scope or clean a dirty workspace. When users also explicitly request reversal of this task's changes, check actual differences and ownership before handling the specified scope, preserving other changes.

When users later explicitly resume the same cancelled delivery, reopen the original Task as appropriate and save reasons, current scope and original cancellation history; if the later work is a different delivery, use a new Task. Neither is inferred automatically from a general “continue the project”.

<a id="4-同步真正受影响的内容"></a>
## 4. Synchronize actually affected content

Briefly record key changes from original to new scope, grounds and destinations in the original Task; synchronize current goals, acceptance, plan and next step. Ordinary local changes do not need another Decision file; save decisions with independent applicability/traceability needs under common record rules.

- Solution changes in the current task: update this Task/design/sole plan.
- Changed Epic decomposition or Stage arrangement of a large solution: update original [PDP](../../../shared/phased-development.md) and affected work, retaining old/new destinations; implementation method changes do not automatically rewrite Vision or product milestones.
- Changed shared agreements across Tasks or long-term effective rules: align scope and decisions in relevant Epic/current Spec and domain sources, coordinating affected work; state target solutions and implementation baselines separately.
- Changed complete game goal, core experience, design pillars or boundaries: update current Vision designated by index and check actually affected Spec, Roadmap and work; original input solutions retain their version/historical identity.
- Changed committed outcomes, ordering or necessary prerequisites: update current Roadmap; implementation steps and task status still belong to original work. Local feature/character/level design updates these primary documents only when it actually changes upper-level direction or outcome arrangements.
- Valid check/adoption results change product outcomes or current overall judgment: synchronize Roadmap summaries and original Evidence/Decision references promptly, without waiting for every Epic to close; results within a Stage still belong to original work and corresponding PDP.
- Directions still under discussion: save as candidates or unresolved points in original work; update current conclusions only after adoption is determined. Explicitly committed but unimplemented goals remain in Vision/Roadmap.
- Changed version, input or acceptance: reassess applicability of relevant Evidence/Decision, retain historical results, and do not directly change an old pass into a new pass.
- Cancellation or splitting affects downstream work: specify which commitments are no longer supplied, which delivered results remain usable and which dependencies need new targets; cancelling one task does not erase all valid history.

Changes explicitly requested by the user go directly into corresponding records. Clarify only when key ambiguity affecting meaning, boundaries or permissions cannot be ascertained; the model handles ordinary maintenance such as filenames and record IDs.

Unspecified local presentation or implementation details do not automatically become a gate requiring user decisions. Investigate existing agreements first; directly select reasonable defaults that satisfy original results and explain necessary tradeoffs. Ask only when choices materially change user outcomes, compatibility or agreed costs. When users already request a replacement implementation, retain corresponding design/implementation authorization without requesting blanket “authorization for the model to choose for itself” again.

<a id="5-让下一次会话看见新要求"></a>
## 5. Make new requirements visible to the next session

Promptly save the original Task's current description at scope changes, explicit deferral or cancellation; saying “received” only in chat is insufficient. Save before advancing affected implementation; for an emergency stop, stop disallowed side effects first, then complete records.

Discussion or results unsaved before an unexpected interruption may not be fully recoverable. Next time, check against last saved records and actual changes; accessible original conversation supplements them. Mark unverifiable key facts honestly without guessing that users approved or cancelled anything.
