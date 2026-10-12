<a id="分阶段开发计划phased-development-planpdp"></a>
# Phased Development Plan (PDP)

Use this to turn a selected large plan into delivery orchestration: plan → PDP → Epic → Stage → Task. PDP is a project- or version-level document, and Stage is an implementation segment within it; neither has a new work lifecycle. Formal Task ownership remains in `Task.epic`.

<a id="何时使用"></a>
## When to Use

design organizes or reuses a PDP when the user asks to implement an existing plan in stages, or when one or more large goals need sustained implementation, checks, or handoff by batches, dependencies, risks, and development capacity. Reuse existing executable orchestration directly; local fixes, sufficient Tasks, and simple Epics can execute directly. Plan length or session count alone does not trigger a PDP.

Plans may come from multi-round conversations, brainstorm, design deliverables, or existing design packages. First distinguish adopted content, recommendations, and undecided assumptions; generating a plan does not change original implementation authorization. Update Vision only when overall direction changes, and Roadmap only when product outcome arrangements change.

<a id="信息归属"></a>
## Information Ownership

| Source | Owned information |
|---|---|
| Original plan/design materials | Detailed design, rationale, inputs, and explicit adopted scope |
| Roadmap | Product outcomes, M milestones, necessary order, and current overall judgment |
| PDP | Plan decomposition into Epics, each Epic's Stage arrangements, and stage-specific combination checks |
| Epic | Established bounded goals, shared conventions, and overall exits |
| Task | Its own delivery, concrete steps, actual results, evidence, and lifecycle |

After actual Epics are created, PDP retains goal summaries and references; Epics directly reference their corresponding PDP orchestration without mirroring Stage tables. New Tasks created to deliver the PDP belong to their Stage's Epic; for cross-goal collaboration, identify the delivering Epic and reference other goals' inputs, without clearing ownership because work is “shared.” Existing independent or shared work may be referenced by Stages while retaining actual ownership, without reassignment. Planned work states only its intended goal ownership and does not misuse formal E identifiers.

Precisely reference design, stage arrangements, or conditions maintained elsewhere first; switch maintenance sources only after explicit transfer. Task-internal plans continue under [records](records.md#implementation-arrangements-and-planmd); PDP does not copy each Task's execution lists and states.

<a id="默认内容"></a>
## Default Content

1. **Plan scope and grounds**: corresponding product/version, paths and versions/sections of adopted plans, full commitments, and undecided parts.
2. **Epic and Stage orchestration**: how many Epics are currently planned, their Stages, the current total Stage count, and undecided portions; derive counts from the same orchestration table without another statistics ledger.
3. **Current progression and gaps**: currently executable work, necessary inputs or unresolved items, related fact/evidence references, and next actions.

Default orchestration table:

| Epic or planned goal | Stage | Expected output | Inputs and necessary prerequisites | Delivering work | Stage check or exit |
|---|---|---|---|---|---|

Divide Epics by bounded goals and overall exits; arrange Stages by actual dependencies, risks, verifiable outputs, and capacity. Refine near-term work into actual Tasks; retain outcomes and arrangements awaiting detail for distant work. Staging does not reduce full commitments. Planned Epics/Tasks state goals and awaiting-creation status; reference real E/T identifiers after actual creation. Planned counts do not mean records exist or outcomes are complete.

<a id="stage-与里程碑"></a>
## Stages and Milestones

Stages in new PDPs default to unique local identifiers S1, S2, etc.; each identifies its Epic or planned goal. Use subidentifiers such as S1.1 when independent outcome subdivisions are needed. Decide whether design, implementation, and testing need segmentation by actual inputs/outputs rather than adding hierarchy to fit names.

New Roadmap milestones default to M1, M2; retain existing S/M/C and other identifiers. S/M are stable anchors within documents, not new global management IDs. To locate table items across documents, supply actual Markdown anchors (such as `<a id="s1"></a>S1`) or corresponding headings and reference original paths plus fragments; do not assume table text automatically becomes an anchor. Do not renumber after reordering; preserve dispositions after cancellation/merging.

Stages express how to implement; milestones express which outcomes hold within which scope/baseline. A stage exit can support a milestone, and a milestone can combine multiple Epics/Stages. Directly reference Task/Epic conditions in the same scope; PDP defines only stage-specific combination checks, and Roadmap only unique product-level conditions. Whether downstream actions are restricted depends on actual dependencies; necessary acceptance follows original commitments, without adding uniform approval per segment.

<a id="执行变化与验证"></a>
## Execution, Changes, and Verification

On entering the current Stage, read back necessary inputs, original work, and applicable conditions; before later segments, check genuinely needed results rather than uniformly waiting for administrative closure of all earlier Tasks. Update original Task/Epic after results arrive; synchronize summaries and original grounds in corresponding PDP/Roadmap when Stage orchestration or product outcome judgments are affected. The current Stage is only a continuation explanation, not another state field system.

When plans/scope/dependencies change, reassess affected Epics, Stages, Tasks, and evidence, retaining unchanged portions and old/new dispositions. Even temporary segments preserve referenced history rather than erasing old commitments in place. Stage counts, file existence, or Task closed counts cannot prove combination results hold.

Before delivering a PDP, check that all adopted-plan commitments have Epic/Stage delivery or explicit destinations awaiting refinement; counts match tables; existing work is reused and planned work does not misuse formal IDs; necessary prerequisites and combination checks are locatable and unknowns explicit; responsibilities are not maintained redundantly with Roadmap/Epic/Task.

<a id="保存与工具"></a>
## Storage and Tools

New PDPs default to `plans/<safe-title>.md` under the workflow directory, with role/record_type `development-plan` and source owner defined by project maintenance conventions; retain existing explicit locations. They may be saved independently before Epic creation; creation payloads supply no Task/Epic owner, do not invent Epics to satisfy attachment rules, and do not impersonate Vision/Spec/Roadmap. When a target already belongs to another source role, first choose an unoccupied location or explicitly adjust registration rather than silently saving under another type.

For record.create, omitting path requires `metadata.title`; explicit path may retain existing locations. After creation, register sources using returned source_proposal and read back; renaming titles does not move files, and actual maintenance uses original path references. PDP has no management ID or record.transition; tools can confirm only storage/reference facts, while content completeness is judged above. See the [PDP template](../templates/development-plan.md.tpl).
