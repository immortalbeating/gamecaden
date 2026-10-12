<a id="游戏工作材料按职责领域与动作判断"></a>
# Game Work Materials: Judge by Responsibility, Domain, and Action

Read this on demand for init adoption, brainstorm direction comparison, design planning, develop/assets execution, and verify/close condition judgments. Combine original Task/Epic commitments, current domains, actual consumers, and next actions to judge which information is needed; reuse clear items directly without traversing the entire catalog. Materials are responsibilities, not a set of files every project must copy; retain explicit requirements from users or effective project rules.

<a id="共通职责"></a>
## Common Responsibilities

| Responsibility | When needed | Available expressions |
|---|---|---|
| Direction and boundaries | When new-project direction, core experience, or scope affects tradeoffs | Current Vision and specific input references; formal adoption organizes north-star/design packages under [current bodies](records.md#current-project-level-bodies), while local legacy-project continuation may follow original Tasks and effective grounds |
| Gameplay rules | When adding/changing player input, states, outcomes, or failure recovery | Spec, existing configuration and consumer code, Task design, state diagrams; distinguish effective rules from target plans |
| Architecture and consumers | When new independent pages/levels, reusable entities, cross-scene/system states, resource wiring, or editing needs affect implementation | Composition/types, states and lifecycle, dependencies/interfaces, and editing/preview in original design; provide necessary diagrams for complex relationships, with depth under [structure conventions](../profiles/references/structure-contract.md); local changes may directly point to actual consumers |
| Verification and acceptance | When judging whether delivery holds | Original requirements, observable paths, applicable Evidence, and necessary Decision; test plans cannot serve as executed results |

One material may fulfill multiple responsibilities; one responsibility may also be jointly fulfilled by existing sources. References identify source, section/field, object or version, currently effective scope, and undecided parts. Filenames, diagram counts, and checkboxes do not automatically prove content sufficiency.

Judge multipurpose material reuse separately from maintaining project-level bodies: formal adoption establishes a defined Vision, necessary Spec overview/Roadmap, while detailed materials retain original responsibilities and references. A mixed file containing required information does not make the whole file a current vision, specification, or roadmap.

The workflow maintains navigation to candidate uses; original Task/design saves current inputs and gaps only when handoff or actual dependencies require them, and one sentence may suffice. Source code, configuration, models, and prototypes may fulfill responsibilities but must answer the current question; readable current state still needs to express differences from unimplemented goals. Actually produce or reference necessary spatial/form/timing expressions; gaps affect only dependent actions.

When retaining sources, judge purpose and applicability; when proposing new standalone material, judge the existing gap, why local supplementation is insufficient, and maintenance benefit. Treat information responsibilities, expression forms, specialized conditions, and facts after events separately; prototypes may express designs, while observations, production inventories, and acceptance remain owned by original sources.

For structured display, annotate only corresponding original sources under the [governance contract](governance.md): `materials` `located` means only that a reference can be located; `missing` means applicability is established but no locatable material exists; `unknown` preserves unclear applicability or source. Original requirements, consumers, and necessary evidence determine whether content is sufficient for execution. Only `effective` and `required` `conditions` may become effective prerequisites for corresponding actions; without bound check grounds, state remains `unknown`, never passed or failed.

<a id="领域触发"></a>
## Domain Triggers

Check only domains matched by current commitments or actual changes; see [game material references](../skills/design/references/game-deliverables.md) for concrete content and equivalent forms.

| Domain | Key questions when triggered | Purpose entry |
|---|---|---|
| Direction/gameplay | How changes to goals, loops, controls, combat, or behavior affect actions and outcomes | [Gameplay and mechanics](../skills/design/references/game-deliverables.md#gameplay-and-mechanics) |
| Economy/progression | How resource sources/sinks, rewards, ability acquisition, and unlock relationships change | [Economy and progression](../skills/design/references/game-deliverables.md#economy-and-progression) |
| Visuals/characters/reusable units | Structural proportions and visual identity in the target perspective, plus real production inputs such as actions, directions, anchors/skeletons, and display conditions | [Visual direction](../skills/design/references/game-deliverables.md#visual-direction), [character inputs](../skills/design/references/game-deliverables.md#characters-and-reusable-units) |
| Maps/levels | Entrances/exits, topology/scale, reachable paths, collision/navigation, interactions and state conditions; distinguish runtime data, build blueprints, and mood images | [Maps and space](../skills/design/references/game-deliverables.md#maps-and-spatial-levels) |
| Narrative/quests/dialogue | How current background, characters, event conditions, content, and camera shots must relate | [Narrative and content](../skills/design/references/game-deliverables.md#narrative-and-content) |
| UI/player journeys | Page/state relationships, input and focus, back/pause, occlusion, key feedback, and actual component ownership | [Interaction and adaptation](../skills/design/references/game-deliverables.md#ui-and-player-journeys) |
| Animation/effects/audio | Triggers, timing, repetition/cancellation, spatial attachment, priorities, and consumer references; expand dynamic music and similar topics only when adopted | [Motion and audiovisuals](../skills/design/references/game-deliverables.md#animation-effects-and-audio) |
| Architecture/saves/cross-level | Owners, dependencies, and lifetimes; save/restore/reset timing, compatibility, and failure recovery | [Architecture and data](../skills/design/references/game-deliverables.md#architecture-and-data), [persistence](../skills/design/references/game-deliverables.md#saves-and-cross-level-state) |
| Performance/networking/platforms | Only when goals or evidenced risks involve them: establish scale/budgets, authority and synchronization, target platform limits, and check environments | [Specialized conditions](../skills/design/references/game-deliverables.md#performance-networking-and-platforms) |

<a id="动作与成熟度"></a>
## Actions and Maturity

- **Exploration/design expression**: When sketches, reference boards, rule examples, or prototypes help compare directions or explain relationships, state purposes and produce/reference them under current authorization. Candidate references do not automatically take effect; a prototype may express a plan while runtime observations are separate evidence.
- **Graybox/bounded experiments**: Need rule, spatial, or interface substitutes sufficient to answer the experiment question and identify what they replace. Missing formal visual inputs do not block independent grayboxes; substitutes do not become formal assets or final acceptance.
- **Formal production**: Before actual production, check identity, structure, manufacturing parameters, and consumer conditions for matching domains. Adopted references/configuration may be inherited but versions and applicability must be locatable; gaps block only production actions depending on them.
- **Engineering integration**: Check current candidate version, use, permitted scope, actual consumers, and verification paths. Material completion, visible previews, technical validation, and user acceptance each have scopes; judge formal adoption under [asset handoff](asset-handoff.md).
- **Verification/closure**: Judge necessary conditions for current actions against original commitments and existing evidence. Derived views indicate gaps rather than adding uniform approval or whole-project gates; quick handles only related conditions for this work.

During legacy-project adoption, judge **reusable, missing, conflicting, unknown, and not applicable** individually. Reuse must point to original responsibilities and specific sections/fields and check versions and real consumers; gaps may enter derived views without creating empty documents first; conflicts list both sources and affected scope; unknowns retain facts awaiting investigation; not applicable explains why the current domain/action does not trigger it. Mapping only makes sources locatable; they become effective project requirements only after **explicit adoption and taking effect in the corresponding scope**. Historical proposals, candidates, and other-project experience do not automatically take effect. Register only sources relevant to current work and confirmed project scope rather than indiscriminately including the whole repository.

<a id="三种判断示例"></a>
### Three Judgment Examples

| Scenario | Expected judgment |
|---|---|
| Pure quick fix: change text on an already defined button | Read the original Task/interface and existing check paths; require no new Vision, character images, or complete UI blueprint. Verify actual impacts and record briefly. |
| Formal production of a new character | First check structural proportions, visual identity, actions/directions/anchors, and target consumers; combinations of adopted references and configuration may fulfill these. Authorized grayboxing may proceed without formal action inputs; formal production/integration cannot yet be claimed to pass conditions, derived materials may show `missing`, and conditions remain `unknown`. |
| Map gaps in a legacy project | Map existing map sections and check runtime data; flag missing routes/topology and affected construction or reachability checks. Independent work may continue; do not treat mood images as collision blueprints or migrate the whole repository because of gaps. |
