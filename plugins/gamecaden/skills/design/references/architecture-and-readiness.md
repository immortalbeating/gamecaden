<a id="架构边界计划与可推进条件"></a>
# Architecture boundaries, plans and advancement conditions

Read when current design involves shared state, scene/page separation, lifecycle, cross-system wiring or key unknowns. Ordinary local changes do not thereby become full-repository architecture audits.

<a id="1-沿真实路径明确责任"></a>
## 1. Establish responsibility along actual paths

From current player inputs/events, locate who owns, modifies and consumes state, and how it displays/saves. Explain entry, exit, re-entry and cancellation/failure behavior, avoiding duplicate registration, old-state writeback or multiple independent sources of truth.

Distinguish runtime data, presentation state and derived views. Determine actual consumer inputs among diagrams, configuration, scenes and models from engineering reading relationships; not every project needs the same layering.

A single state source does not centralize all state in Main. Game data such as inventory or exploration progress each have sole write responsibility; local presentation state such as focus, selection and scroll position may belong to corresponding views. Existing page-route state also needs explicit modification/synchronization ownership, without two independent current-page copies in different components. Concrete boundaries still follow effective project agreements.

For new independent pages/levels, reusable entities, state across lifecycles or editing approaches, write actual composition, types, authoritative state, survival/reset, external dependencies and editing/preview into original design under [Common structural conventions](../../../profiles/references/structure-contract.md). Use text for simple relationships, composition diagrams and lifecycle tables for complex ones. Cite sufficient existing materials directly; establish boundaries before related implementation rather than waiting for oversized files.

<a id="2-映射到引擎和现有工程"></a>
## 2. Map to engines and existing engineering

Select current engine/library and actual target separately through [Profiles entrypoint](../../../profiles/README.md): saved scenes/runtime trees, components/render objects, page/session lifetimes, shared resources and input each use corresponding mechanisms. Preview, design arrangements and actual delivery each have scope; platform background cannot expand commitments. Read structure references for directory creation/adjustment without copying another set of engine rules.

When organization of actual scenes/nodes, Prefabs/components or Scenes/display objects changes, enter corresponding structural topics through profiles; distinguish engine mechanisms, default examples and project adoption. For design-only delivery, check composition consistency and verification arrangements; implementation/runtime results require their own evidence.

Reuse still-applicable components and interfaces first. Include structural adjustments necessary for correctly implementing/verifying current goals; exclude unrelated cleanup. Without engineering yet, give explicit design choices rather than claiming these modules exist.

<a id="3-图数据与工程之间的关系"></a>
## 3. Relationships among diagrams, data and engineering

Design tells implementers which versions/relationships are adopted, which are illustrative, where generation/editing happens and where consistency is checked. One location owns each runtime fact; other expressions reference or derive from it.

When blueprints are design contracts, define correspondence checks against actual scenes; when blueprint data is runtime input, maintain data directly and generate needed presentations. Resolve substantive diagram/text conflicts first, without assuming a file extension is more authoritative.

<a id="4-组织实施与试验"></a>
## 4. Organize implementation and experiments

Organize plans around observable results and actual dependencies; steps do not automatically become Tasks. Keep one internal checklist across main records and plan.md; upper-level [PDP](../../../shared/phased-development.md) owns Stage arrangements and references real work. Cross-Task execution dependencies remain with dependent work; overall exits belong to Epic/milestone; Stage maintains only its unique combination checks, referencing original definitions for other conditions.

For unknowns, first determine whether existing code/configuration/evidence can establish them. When experiments are necessary, explain the question, current assumption, permitted operation scope, needed inputs and observations sufficient to change subsequent choices.

For solution-only requests, deliver experiment arrangements; with authorized implementation, run relevant bounded experiments before expanding as appropriate. Experimental scope does not reduce final product commitments automatically, and results do not automatically lock in long-term contracts.

<a id="5-对下一动作作出明确判断"></a>
## 5. Make explicit judgments for the next action

When an action can advance, explain its goal, key inputs, concrete arrangements and expected verification; for gaps, identify blocked actions, causes and parts that can continue.

For example, topology grayboxing readiness does not imply batch production readiness for formal backgrounds; a textual character description may suffice for discussion but not reusable actions. Conversely, undesigned expressions/voice for future chapters should not block established movement mechanics now.

Design completion means providing usable solutions/arrangements or explicit investigation results for this commitment. Runtime passes, human acceptance, formal adoption and release each need actual records; document completeness cannot replace them.

Distinguish “what should be established first”, “which step has sufficient inputs” and “what this round allows”. Without collider, trigger or actual consumer materials, offer candidate solutions with assumptions and checking arrangements; geometry inference does not establish player reachability. If acceptance requires verified final design, relevant gaps still need completion; investigation lists cannot replace committed conclusions.
