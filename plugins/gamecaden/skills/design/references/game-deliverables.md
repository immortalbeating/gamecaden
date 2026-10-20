<a id="游戏材料按消费者选择必要信息"></a>
# Game materials: select necessary information by consumers

Locate matching entries by current actions, consumers and existing agreements; read [Material responsibilities](../../../shared/material-requirements.md) when applicability is unclear. Cite sufficient existing sources directly; supplement relevant content when target relationships change or semantics are insufficient. Names below are candidate materials and search aliases, not mandatory project files or a uniform approval checklist; effective project requirements still apply.

<a id="总体原则"></a>
## General principles

Materials should answer questions for actual users or subsequent actions. Structure, visual identity, production parameters, runtime integration and acceptance scope may mature separately; a pass in one cannot replace others.

Each material explains its purpose, applicable objects/versions, explicitly effective relationships and still-illustrative/unknown parts. Cite original authoritative sources directly when present; file counts, screenshot counts and titles do not prove complete information.

Cover information responsibilities by current consumers; select diagrams, tables, text, configuration, models and prototypes by the question. Expand economy, narrative, skeletons, dynamic music and other special topics by actual use. Original inventories/evidence own actual production/runtime facts. Candidate Spec/GDD do not take effect from names alone; prototypes can express design, but actual observations prove experimental results.

Before new independent materials, judge what existing sources lack, why references/local supplements are insufficient and the maintenance/handoff benefit. Actually produce or cite needed diagrams; important grounds inform original solutions, rather than merely listing “files read”. Merge aliases for common names as appropriate, judge functionally distinct materials separately, and do not create files by table-row count.

<a id="用途入口"></a>
## Use entrypoints

| Current question | Read as needed |
|---|---|
| Direction, loops, controls, combat or enemy behavior | [Gameplay and mechanics](#gameplay-and-mechanics) |
| Resource flows, rewards, growth or unlocking | [Economy and progression](#economy-and-progression) |
| Style comparison, character identity and production structure | [Visual direction](#visual-direction), [Characters and reusable units](#characters-and-reusable-units) |
| Routes, spatial construction, pacing or terrain modules | [Maps and spatial levels](#maps-and-spatial-levels) |
| Background, characters, quests, dialogue or shots | [Narrative and content](#narrative-and-content) |
| Pages, focus, layout or content adaptation | [UI and player journeys](#ui-and-player-journeys) |
| Poses/frames, attachment points, effects, sound or music | [Animation, effects and audio](#animation-effects-and-audio) |
| Composition, state, dependencies or persistence | [Architecture and data](#architecture-and-data), [Saves and cross-level state](#saves-and-cross-level-state) |
| Budgets, networking or delivery environments | [Performance, networking and platforms](#performance-networking-and-platforms) |
| Prototypes, inventories, evidence or acceptance records | [Experiment and delivery records](#experiment-and-delivery-records) |

<a id="玩法与机制"></a>
## Gameplay and mechanics

When adding/changing interaction rules, explain player inputs/triggers, state changes, results/feedback, failure/recovery and relationships to existing rules. Use state diagrams for complex transitions and brief text for simple rules.

Values affecting implementation need usable sources or explicit calibratable initial values. When configuration owns individual values, do not copy manual tables. With clear user outcomes and reasonably decidable ordinary initial values, choose them yourself, labeling purpose/calibration. Temporary values are not user-locked long-term standards.

Adjustable initial values need neither per-value user signatures nor Decisions. Parameter calibration, feature/appearance acceptance and long-term rule establishment are distinct responsibilities; existing commitments/project rules determine human decisions. Handle corresponding tradeoffs/acceptance only when numerical changes affect established boundaries.

For new games, focus on the core loop currently under verification; retain complete distant content in Vision/Roadmap, without requiring every chapter/value before current experiments.


| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| Project vision/design brief (Vision/Design Brief) | Target experience, audience/objects and scope | Project initiation or directional changes affect tradeoffs | Original Vision, requirements or Task sections |
| Design pillars (Design Pillars) | Explicit grounds for comparing alternatives | Direction or system goals conflict | Adopted principles and brief rationale |
| Reference comparison/difference explanation | Borrowed aspects and own outcomes | Reference projects influence choices | Original comparison sections and specific references |
| Core/meta loop diagram (Core/Meta Loop) | Action, results, feedback and repeated action | Verifying loops; expand long-term loops when actually adopted | Original rules, relationship diagrams or bounded prototypes |
| Control/camera specifications | Action mappings, observation and feedback | Changed input devices, controls or viewpoints | Input configuration, original design and camera sources |
| Combat specifications | Attack, defense, hit, cancellation and recovery | Changed combat outcomes/rules | Original state/event definitions and gameplay design |
| State diagram (State Diagram) | States and transition conditions | Ambiguous transition relationships | Existing state models or clear relationship explanations |
| Sequence diagram/event timing table | Participants, ordering and timing | Cross-object events/timing affect outcomes | Original event definitions or timing expression; state diagrams alone do not fulfill timing contracts |
| Enemy behavior/behavior tree/decision table | Perception, selection, action and exit | New behavior or changed multi-unit responses | Original behavior implementation/rules; behavior trees are not mandatory |

<a id="经济与成长"></a>
## Economy and progression

Judge resource relationships, gained abilities and saved state separately. Original configuration owns actual values; original design retains rule differences. Adjustable initial values/acceptance follow the preceding section.

| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| Economy flow diagram/resource income and expenditure explanation | Resource sources, consumption and conversion | Adding/changing economy relationships | Configuration plus necessary flow diagrams/text |
| Numerical/balance table | Costs, benefits and calibration assumptions | Values affect current gameplay results | Actual configuration or derived tables; do not duplicate manual sources of truth |
| Reward/drop rules | Acquisition conditions, counts and consumers | Changed rewards, drops or exchanges | Original definitions and player-outcome explanations |
| Progression curve/pacing explanation | Abilities, challenges and acquisition pace | Changed progression/difficulty advancement | Original configuration, rules and necessary curves |
| Skill tree/unlock relationship diagram | Ability dependencies and unlock consequences | Changed unlock conditions/ability relationships | Original definitions or local dependency diagrams; existing fields do not prove integrated abilities |

<a id="视觉方向"></a>
## Visual direction

Direction exploration materials support comparison; they guide corresponding production only after adopted scope is clear. Assets may share visual grounds, but each still needs structural/production input coverage.

Keep the adopted direction, its applicable scope and detailed visual grounds locatable from Vision. Existing visual sections and selected reference images may fulfill this; no separate art-bible file is required. Extract the features distinguishing the choice from plausible alternatives rather than only its medium, palette or theme. Later candidates do not revise the adopted selection; explicit changes follow the original decision and change conventions.

| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| Art bible/style guide (Art Bible/Style Guide) | Form, color, material and presentation rules | Style/cross-asset consistency affects production | Original visual sections, adopted samples and rules |
| Mood/reference board (Mood Board) | Compare atmosphere and visual language | Exploring actual directions | Reference sets with comparison explanations; do not prove individual structures settled |
| Concept art (Concept Art) | Form, environment or composition solutions | Comparing visual solutions | Existing concepts, local sketches or previs; explain adopted aspects |
| Key image/quality benchmark | Current presentation and quality aspects | Ambiguous quality goals | Adopted samples, target renders or previews; do not automatically accept new outputs |

<a id="角色与可复用单位"></a>
## Characters and reusable units

For formal character/action production, judge whether current materials cover these responsibilities:

| Responsibility | What consumers need to know |
|---|---|
| Structure and proportions | Silhouette, body/equipment relationships, obvious asymmetry and spatial extent in target viewpoints |
| Visual identity | Adopted references, style, identity features, colors/materials and details that must remain |
| Production and consumer adaptation | Required poses/directions, anchors/attachment points, timing/frame organization or skeleton requirements and target display conditions |

Three responsibilities do not mean three fixed documents or images. Adopted diagrams, text and existing production configuration may combine or be explicitly inherited; redesign affected parts only. Asymmetry, production risk and actual viewing angles determine view counts, without default six-direction/three-view requirements for all projects.

Identity/structural consistency in formal production of one character may be fulfilled by a shared master with individual differences, character-specific design, adopted models/assets and explicit constraints. Combine/select by coverage, without rebuilding all materials whenever “generate characters” appears; check current action/consumer inputs separately.

| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| Shared form master/body-type conventions | Shared proportions, silhouettes and variation range | Characters actually share structure or production chains | Used models, proportion diagrams and difference explanations; no uniform filename required |
| Character-specific design/model sheet (Character Model Sheet) | Individual structure, proportions and identity details | New identities or materials insufficient for production guidance | Original design, used models/assets and local explanations |
| Turnaround/model rotation (Turnaround/Model Rotation) | Form/equipment relationships at target angles | New viewpoints, asymmetry or unknown back/side structure | Necessary views or existing model screenshots; count follows purpose |
| Scale/proportion comparison (Scale Chart) | Relative scales between entities | Scale relationships affect production/readability | Original dimension configuration and inspectable comparisons |
| Equipment parts/structural breakdown diagram | Occlusion, connections and production parts | Ambiguous layers, assembly/disassembly or equipment structure | Original models/layers and local structural diagrams |
| Expression/pose sheet (Expression/Pose Sheet) | Performance range and identity features | Expressions, dialogue performance or pose production | Adopted samples, models or previews; not a universally mandatory package |
| Prop/weapon design and attachment explanation | Function, scale and connections | Independent objects or changed character-held relationships | Original models/configuration with necessary explanations |

Traceable proxies may be used for physical occupancy, spatial budgets or wiring experiments; proxies do not automatically become formal character identities/final assets. Continue formal delivery goals when requested, without ending at placeholders.

Accepting character references does not automatically accept all regenerated actions or runtime scales. Human-acceptance objects follow original project requirements and actual authorization, without uniform new approvals per design material.

<a id="地图与空间关卡"></a>
## Maps and spatial levels

For spatial movement, combat layouts or route requirements, establish entrances/exits, topology, scale, support/collision/navigation, main paths, camera readability, interaction positions and state conditions. Gameplay without spatial movement does not need terrain blueprints merely because it is a “game”.

Blueprints may be images, coordinate/topology data or readable layout explanations; choose forms that guide current actions and check results. Establish runtime fact ownership first:

- Data actually read by programs: corresponding runtime sources, from which charts may derive; do not create another independently changeable coordinate ledger.
- Blueprints guiding scene construction: design relationships belong to them, wiring/geometry to actual scenes/programs; design explains checking correspondence.
- Background/atmosphere images: only explicitly labeled and adopted design meanings become constraints; do not infer collision/exits directly from images.


| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| World/region connection diagram, level topology diagram | Connections, entrances/exits, paths and unlock conditions | Changed routes, region relationships or reachability | Original topology/quest data or local connection expression |
| Level layout/construction blueprint (Level Layout) | Spatial scale, positions and construction relationships | Construction, collision or interaction positions need clarity | Original layout data/scenes or diagrams; topology alone does not define geometry |
| Level scale/metrics explanation (Level Metrics) | Scales of movement, support and traversable space | Changed ability/spatial-scale relationships | Actual configuration and inspectable layouts; do not duplicate numerical tables |
| Pacing/encounter layout | Distribution of challenge, pauses, interaction and feedback | Changed experience pacing/encounter arrangements | Original design/layout and necessary pacing expression |
| Modular kit/terrain assembly specifications (Modular Kit/Tileset) | Combination boundaries, seams, scale and collision | Modular/terrain production reuse | Existing production sources and local assembly agreements |
| Greybox/blockout (Greybox/Blockout) | Operable spatial/rule proxies | Testing layout, scale or gameplay assumptions | Existing bounded prototypes; label substitution scope, observations belong to Evidence |
| Scene concept/light and color reference | Atmosphere, composition and spatial readability | Environment visual selection/production | Original scenes/diagrams; do not automatically define collision/exits |

Verify reachability through actual entrypoints, ability state and player inputs. Initialization can set starting points; teleporting/direct scene switching during path checks proves injected results only, not natural arrival. Concrete methods follow project capabilities.

<a id="叙事与内容"></a>
## Narrative and content

Expand actual narrative delivery, linking character visuals, quest rules and state sources. State story intent, execution conditions and actual content separately; completed settings do not prove implemented runtime content.

| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| World background/narrative settings | Consistent facts/boundaries for current content | Background affects current delivery | Original content sections; no complete world lore required first |
| Character settings/relationship diagrams | Motivations, relationships and narrative roles | Character relationships affect stories/dialogue | Original character/content sections; not replacements for visual structural design |
| Story/quest timelines, branch diagrams | Event ordering, conditions and consequences | Changed quests, chapters or branches | Original quest data and design differences |
| Dialogue scripts/conditional dialogue tables | Speakers, content, conditions and order | Actual dialogue/voice consumers exist | Original scripts/content tables; no duplicated dialogue source of truth |
| Storyboards (Storyboard)/shot explanations | Shot, action and narrative-presentation relationships | Ambiguous cutscene/shot arrangements | Necessary diagrams, existing shot sources or previs |
| Animatic/previs (Animatic/Previs) | Observable pacing/presentation solutions | Static expression insufficient for timing | Bounded previs; judge solution expression/runtime acceptance separately |

<a id="ui-与玩家旅程"></a>
## UI and player journeys

When layouts, hierarchy, page relationships or multiple states affect understanding, use wireframes or state/flow diagrams. Explain entry, return, pause/resume, focus, input devices, occlusion/clipping, key feedback and relevant abnormal states.

Map experience structure to actual scenes/components and state sources. Control lists are not interaction design; static screenshots do not prove dynamics. Pure copy changes or small changes without spatial ambiguity need no additional full-screen diagrams.

For coherent UI systems, reusable components or drift between related interfaces, use [UI families](../../../shared/ui-families.md) for proactive scope judgment, adaptable general/game component catalogues, family/variant selection and implementation ownership. Keep actual project definitions in their existing authoritative sources.

An array or placeholder field listed in materials does not prove users need only a corresponding simplified interface. For example, when maps lack position/connection information, investigate/design sources and offer suitable spatial/topological expression. If suggesting location lists instead, explicitly state changed feature meaning without treating them as already-adopted map outcomes yourself.


| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| Player journey/interaction flow (User Flow) | Entry, return and task paths | Changed page relationships/operation paths | Original flows, quest conditions or operable prototypes |
| Page/focus states and exceptional paths | Pause, resume, lost focus and failure relationships | Changed input, focus or recovery | Original state/input sources; screenshots do not prove behavior |
| Wireframe (Wireframe) | Content hierarchy, density and spatial layout | Ambiguous layouts/occlusion | Original UI sources, local sketches or prototypes |
| High-fidelity designs/component states | Visual rules and actual state presentation | UI visual/component production | Shared styles, actual components and necessary drafts |
| UI family/component arrangement | Shared grounds, contextual differences, supported variants and usage-to-implementation relationships | UI unification, reusable UI or evidenced inconsistency | Original UI design, component manifests, shared resources and representative samples |
| Interactive prototype | Operation feedback and dynamic relationships | Expressing/testing interaction solutions | Existing prototypes; actual observations alone are runtime evidence |
| Accessibility adaptation explanation | Inputs, readable feedback and relevant user paths | Effective commitments/current changes involve accessibility | Original rules and affected control/input sources |
| Localization/font and text adaptation | Language content, fonts, space and fallback | Changed language support/text presentation conditions | Actual content/font configuration; do not duplicate translation tables |

<a id="动画特效与音频"></a>
## Animation, effects and audio

When related to gameplay/characters, establish trigger events, cancellation/retriggering, temporal relationships, spatial/attachment positions, priorities and consumers. Cite original action/audio definition IDs instead of copying another timing table.

Distinguish raw materials, production parameters, runtime references and verification materials. Effects visible in isolated previews are not necessarily correctly integrated in actual player paths and target display conditions.


| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| Action list/action-state relationships | Action uses, entry, exit and transitions | New actions or changed consumers | Original action definitions/rules |
| Key poses/action sketches | Center of gravity, silhouette and action intent | Unclear pose meaning/production inputs | Existing actions, models or necessary pose diagrams |
| Frame/direction/timing/event specifications | Organization, timing and consumer contracts | Formal action production or changed formats | Original animation definitions/configuration; inherit valid frame counts/anchors without universal fixed values |
| Layer/skeleton/rigging/skinning explanation | Deformation, parts and connections | Production chains actually use the technology | Original model/layer/rigging sources; non-skeletal routes need no mandatory skeleton package |
| VFX references/effect trigger tables | Trigger, cancellation, attachment and readable feedback | Changed effect-event/spatial relationships | Original effect Cue/event definitions; do not duplicate hit timing |
| SFX/voice Cue tables | Playback conditions, repetition and consumers | Changed sound/dialogue playback rules | Original audio definitions/content sources |
| Mixing/spatial and priority relationships | Preemption, hierarchy, attachment and audible feedback | Concurrency, space or priorities affect presentation | Original mixing/audio configuration and necessary explanations |
| Music structure/loop explanation | Loops, sections and current use | Music production or changed loop conditions | Original music definitions and audible references |
| Dynamic music state/transition diagrams | Layers, switching conditions and transitions | State-driven music actually adopted | Original music state/Cue; static loops do not expand this branch |

<a id="架构与数据"></a>
## Architecture and data

Supplement matching technical mechanisms under [Structure contract](../../../profiles/references/structure-contract.md) and [Profile topics](../../../profiles/README.md#topic-entries-for-structural-changes). Source code explains current state; original design still expresses future relationship changes. New projects without engineering may establish arrangements first, labeling native sources not yet established.

| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| Composition/responsibility diagram | Assembly, types and consumer relationships | Changed independent pages, reusable entities or editing boundaries | Original design/production sources; see structure contract |
| State/lifecycle/dependency explanation | Writers, readers, creation, termination and reset | Changed shared-state, cross-system or async relationships | Original code/configuration with target differences; visible trees do not prove lifetimes |
| Data model/interface contract | Data meanings, references and failure behavior | Changed fields or cross-module inputs/outputs | Original schema/configuration/interfaces, supplemented with semantics/compatibility differences |

<a id="存档与跨关卡状态"></a>
## Saves and cross-level state

For actual persistent state, establish ownership, saving/loading/reset timing, changes retained across scenes and failure recovery; supplement compatibility/migration and rollback considerations when old data formats/meanings change.

Established character settings/chapter outlines do not prove implemented state transfer/runtime content. Verification covers actual consumers; configuration fields do not replace player-acquired abilities/rewards.


| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| Save/restore/reset explanation | State/save timing, cross-level retention and failure recovery | Actual persistence or changed state lifetime | Original data/runtime sources and design relationships |
| Compatibility/migration/rollback arrangements | Old data meanings, conversion and failure consequences | Changed formats/save semantics | Original version agreements and local change arrangements |

<a id="性能联网与平台"></a>
## Performance, networking and platforms

Supplement design only when current commitments/actual risks involve these conditions: target scale, state authority, synchronization/failure, resource budgets, platform inputs/limits and reproducible check environments.

Derive constraints from actual project requirements/evidence, without copying unit counts, GPU models, frame counts or fixed benchmarks from other projects. Investigate missing facts affecting solutions first; potentially needed future specifications do not become current level gates prematurely.


| Common name/alias | Function | When to use | Reusable or equivalent sources |
|---|---|---|---|
| Performance targets/resource budgets | Current scale, loading and resource constraints | Performance commitments or evidence-backed risks | Actual project requirements; measurements belong separately to evidence |
| Network authority/synchronization relationships | State decision owners, synchronization scope and consumers | Actual network behavior/support commitments | Original protocols, relationship explanations and necessary diagrams |
| Session/connection failure recovery | Entry, exit, failure and recovery | Connections/sessions affect current results | Original session models and failure paths |
| Platform/input/build conditions | Target environments, deployment and delivery limits | Actual targets affect design/integration | Project settings and matching profiles; no advance maintenance of all-platform certification tables |

<a id="试验与交付记录"></a>
## Experiment and delivery records

Maintain design inputs and subsequent facts separately; this directory only connects uses, while original contracts retain format/event semantics.

| Material/record | Function and ownership |
|---|---|
| Prototype/experiment arrangements and observations | Prototypes express design or support bounded experiments; allowed scope/questions belong to original work, actual observations to [Evidence](../../../shared/verification.md) |
| Test/acceptance arrangements | Match goals, objects, observable paths and necessary acceptance; plans are not executed evidence |
| Manifest/production inventories | Tools/files own actual files, versions, dimensions, frame counts, encoding and similar facts; cite inventories without manual mirrors |
| Asset master ledger and acceptance records | Track identity, uses, candidates, selection and integration grounds under [Asset handoff](../../../shared/asset-handoff.md); judge technical passes, acceptance and runtime separately |
| Build/release and change records | Original delivery sources own actual versions, delivery environments/results; still explain design-relevant limits in advance |

Concepts and design drafts may directly supply design inputs; independent identities/candidates needing sustained comparison, reuse or review may also be tracked under original ledger contracts. Temporary sketches need no individual entries, and references do not turn all design sections into assets.

<a id="缺项怎样影响下一动作"></a>
## How gaps affect the next action

Associate gaps with concrete actions: mandatory now, calibratable during authorized iteration, or needed only later. Brief text may explain classification, without new global readiness state files.

Without formal asset inputs, continue independent rule explanations/grayboxing; without key choices for current gameplay, do not write guesses as accepted requirements. Follow effective conventions that require specific materials; handle proposed changes through scope-change procedures.

<a id="名称与用途参考"></a>
## Name and use references

Names support search; teams may use other explicit aliases. For character model sheets and rotation views, see [Toon Institute original course](https://www.awn.com/tooninstitute/lessonplan/model.htm); for grayboxing as layout/scale and gameplay rough drafts, see [Epic grayboxing explanation](https://dev.epicgames.com/documentation/en-us/fortnite/greyboxing-in-unreal-editor-for-fortnite). Borrow only use distinctions, not fixed course view counts, engine operations or production order as cross-project requirements. Candidate navigation and trigger arrangements on this page are Gamecaden workflow choices.
