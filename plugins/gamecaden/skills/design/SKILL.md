---
name: design
description: Use only when the user explicitly requests Gamecaden for this work, or effective guidance in the current project has adopted Gamecaden. Turn selected goals into game/engineering design, necessary diagrams, implementation arrangements and verification grounds, or organize large solutions into phased development plans. Use for missing practical solutions, solution review or design delivery; reuse explicit quick changes and existing executable designs directly.
---

# Design

Apply the [workflow applicability boundary](../../shared/workspace.md#workflow-applicability) before using this responsibility.

Establish sufficient design to guide the next action for current delivery. Fit design to actual consumers and project state, retaining complete goals; material depth follows current actions, risks and established agreements.

Resolve links from this Skill's directory; ../../shared/ is the package's shared/ directory.

<a id="1-确定这次要设计什么"></a>
## 1. Determine what to design here

Reuse user requirements, selected solutions, original Task/Epic and effective project specifications. Locate [original sources](../../shared/workspace.md#1-locations-and-resolution) without reinitializing established goals or roots.

- Users want design/plans only: deliver corresponding materials; code execution, asset integration and engine operations follow original authorization boundaries.
- Users only want existing solutions reviewed: deliver grounded problems and recommendations, preserving original files; save to corresponding sources when modifying/implementing design is requested.
- Users requested implementation/production: continue the original request after sufficient design, without requiring a fresh implementation request midway.
- Executable design exists: check relevant differences and reuse, entering the next action directly as needed.
- Selected large solutions need phased execution, or explicit upper-level phased development documents are requested: read [Phased Development Plan](../../shared/phased-development.md) and arrange current Epic/Stage and ownership destinations. PDP may be saved before real work exists, without fictitious Epics for plan storage.
- Core experience or commitments have genuine unresolved tradeoffs: handle that disagreement only, reading [brainstorm](../brainstorm/SKILL.md) as needed without reinterviewing all content.

Retain original work under [record conventions](../../shared/records.md#creation-and-saving); moving from discussion to design does not create a new Task. Independent design deliveries needing retention or handoff may use a design Task; pure planning or maintenance of a management object writes back to that object.

<a id="2-先核对现状与消费者"></a>
## 2. Check current state and consumers first

Follow relevant inputs or triggers to inspect state, data, scenes/modules, actual consumers and observable results. With no current implementation, explicitly describe new design without inventing existing interfaces, results or pass records.

Explain what must change, needs verification or remains under investigation. Read relevant project rules, existing design and failure experience, reusing still-applicable understanding; do not expand local changes into unrelated repository-wide audits.

Before solutions, select matching requirements under [rule selection](../../shared/rules.md#1-select-sources-for-current-work), respecting effective agreements, default recommendations and historical experience. Use actual runtime roots/versions and available specialized Skills within current design/execution scope.

Distinguish gaps: investigate project-accessible technical facts; offer explicit design recommendations for undefined interfaces/initial values that can reasonably be selected; ask users only about unresolved tradeoffs materially changing player outcomes or commitments. Materials omitting fields or input actions do not automatically require technical answers from users.

With insufficient current data, design paths for completing corresponding sources/interfaces rather than defaulting to reduced user outcomes. Simplifications changing feature meaning remain explicit recommendations; “easier to implement now” is not evidence users selected that replacement.

For cross-scene, shared-state, lifecycle or multi-system interface design, read corresponding parts of [Architecture and advancement conditions](references/architecture-and-readiness.md). Give necessary arrangements directly for simple local changes.

<a id="3-确定必要内容和表达"></a>
## 3. Determine necessary content and expression

For gameplay, character, map, UI, feedback, save or production-input changes, check [triggered responsibilities](../../shared/material-requirements.md#domain-triggers) and matching [material entries](references/game-deliverables.md#use-entrypoints). Use [derived views](../../shared/panel-workflow.md) when source discovery or an overview needs them, then read back originals.

For UI unification, reusable UI design or evidenced cross-interface drift, apply [UI families](../../shared/ui-families.md) within current scope, proactively organizing the arrangement when the requested outcome includes it.

Define responsibilities, inputs/outputs and key relationships, then choose text, diagrams or data. Cite explicit versions of existing materials that fulfill responsibilities; diagrams and text explain what is effective, illustrative or awaiting verification.

Design explanations or diagrams required by current commitments should actually be produced in delivery or cite materials already fulfilling responsibilities; merely listing “draw diagrams later” does not deliver design. When users request production arrangements only, deliver arrangements and necessary design expression; do not prematurely require later raw materials, animation previews or runtime results as this round's outputs.

Gaps constrain dependent actions only. For grayboxing or bounded experiments next, use purpose-fitting inputs; formal production/adoption rules and acceptance requirements still follow original agreements, without replacing final delivery with experimental results.

<a id="4-形成方案实施安排和验证路径"></a>
## 4. Form solutions, implementation arrangements and verification paths

Explain current changes and boundaries, relevant state, each part's responsibility, how data/state/resources reach consumers, failure/recovery and important tradeoffs.

Organize implementation around observable results and actual dependencies, prioritizing unknowns that block delivery. Investigate technical facts first; when experiments are necessary, explain the question, allowed change scope and observation grounds. For document-only requests, deliver experiment arrangements without running unauthorized prototypes.

Match verification to actual commitments: normal player paths, state transitions, consumer integration and necessary human acceptance. Explain evidence coverage without inventing commands, runtime results or adoption status.

The model handles ordinary reversible implementation and local presentation choices under existing agreements; clarify only disagreements materially changing outcomes, compatibility, permissions or agreed costs. For conflicting user requirements, explicitly recommend with reasons rather than silently dropping scope.

<a id="5-保存与一致性检查"></a>
## 5. Save and check consistency

Keep simple design in the original Task, using its design.md for extensive text or independent consumption. Split plan.md only under [implementation-arrangement rules](../../shared/records.md#implementation-arrangements-and-planmd); main records retain current explanation and references. Epic holds shared cross-Task design; Task holds this delivery's arrangements.

Long-term rules update current Spec overview and corresponding domain sources by scope, separately from implementation facts of declared baselines; choosing future implementation alone does not become current capability. When design changes complete direction or outcome arrangements, write back current Vision/Roadmap under [Change handling](../flow/references/change-work.md#4-synchronize-actually-affected-content); local design remains with original work. Future branches go to parking lots; valuable experience enters Notes as needed.

Check correspondence among goals, solutions, materials, plans and verification, and duplicated state or equivalent primary text. For changed, replaced or paused scope, save destinations under [Flow change rules](../flow/references/change-work.md), retaining valid history.

For PDP delivery, check commitment coverage of adopted solutions, Epic/Stage counts matching the sole table, ownership, clear real/proposed work distinctions and locatable necessary checks. Using PDP for complex implementation does not require precreating every distant Task. Product outcome arrangements belong to current Roadmap; stage orchestration belongs to PDP; precise references connect original design and work content.

<a id="6-明确现在可以推进什么"></a>
## 6. State what can advance now

Deliver current design and next action: original goal/work, roots/baseline, effective inputs, arrangements/acceptance and gaps still affecting that action. Use [original records for continuation](../../shared/records.md#7-continuation-and-independent-handoff), without another design state ledger.

Scope design conclusions, such as “room-connectivity grayboxing can begin” or “formal action production still lacks anchor conventions”; do not broadly declare “the entire project is ready”. With authorized subsequent work and sufficient key inputs, hand engineering implementation to [develop](../develop/SKILL.md) and content production to [assets](../assets/SKILL.md), continuing within original work; design-only requests end at design delivery.

State technical readiness and current execution authorization separately. For actions with unverified key facts, first investigate or perform authorized experiments; do not declare missing key inputs and formal implementation readiness simultaneously. Ending this design response does not automatically close the original Task: implementation/production commitments retain unfinished items; independent design Tasks alone judge closure by their own delivery conditions.

For closure, read actual Task delivery commitments, not just kind or “there are later steps”. For example, a goal only to deliver a hit-reaction production solution may close under rules after the solution fulfills agreements and is delivered/retained; missing generated animation is not an automatically added deficit. A Task completing formal action integration still needs corresponding production, acceptance and integration results. Design missing mandatory key conclusions remains unfinished because it fails design commitments, rather than because later implementation has not happened.
