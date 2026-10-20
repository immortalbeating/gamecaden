# UI families: design and implementation

Use this reference for UI unification, reusable UI design, family-based production/integration, or evidenced drift between related interfaces. Retain project vocabulary, authoritative design, real components and existing work records under [material responsibilities](material-requirements.md). Read only the parts needed by the current action.

## When to apply

- A request to unify UI appearance/interaction or design a coherent UI system includes organizing suitable families; proactively establish the arrangement within that request without waiting for the user to name this method.
- Existing applicable families are the default inputs for related UI work. Reuse their definitions, components and supported variants.
- When actual duplication, style drift or inconsistent behavior suggests family organization, explain the concrete conflict and propose the smallest useful correction. Establish local reusable arrangements within authorized work; changes to accepted direction or unrelated interfaces retain original scope and change rules.
- A local edit with sufficient existing design continues directly. Simple interfaces can use existing themes/components; family organization grows with actual consumers rather than becoming a prerequisite for every UI change.

Unselected directions remain candidates. Reuse the [adopted visual grounds](../skills/design/references/game-deliverables.md#visual-direction), decisions and applicability of existing sources; arranging candidates does not grant them production authority or require a new universal approval round.

## Distinguish responsibilities and appearance

| Concept | Responsibility |
|---|---|
| Common foundation | Adopted typography, shapes, materials, spacing, emphasis and shared interaction/feedback meanings |
| Component | A functional unit with defined data, states and behavior, such as a command button, tab, item slot or health display |
| Visual family/theme | Related appearance rules and members, with explicit scope, shared grounds and independent differences |
| Variant | A supported difference within a component/family, such as size, density, emphasis, intent or placement |
| Page/HUD pattern | A composition of components, navigation and layout for a player activity |

A project may have multiple component families, multiple independent visual systems, or both. Explain inheritance/composition and selection by scene, object, faction, device or other actual context. A decorative menu and an in-world terminal may have different visual roots while sharing suitable component behavior and learned input meanings. A single global visual root is optional.

Functional categories locate suitable components; they do not prescribe visual families. Screen-fixed, world-following or scene-embedded presentation, real-time or paused use, and input devices are contextual dimensions. Organize responsibilities without requiring a matching class hierarchy or directory tree.

## Recommended component catalogues

These are adaptable Gamecaden recommendations, not an industry-wide naming standard or a completeness checklist. Select existing needs from the game's actual mechanics; retain equivalent engine/project names. A game component may combine primitives, custom drawing or scene objects and owns its gameplay-specific presentation rules.

| General UI category | Example components |
|---|---|
| Commands | Button, IconButton, MenuButton |
| Navigation | Tabs, NavigationList |
| Selection and adjustment | Checkbox, RadioGroup, Switch, Select, Slider |
| Text input | Input, TextArea, SearchField |
| Containers and layout | Panel, Dialog, Drawer, List, Grid |
| Information | Label, Icon, Badge, Meter |
| Feedback and explanation | Tooltip, Toast, ProgressIndicator |

| Game UI category | Example components |
|---|---|
| Actor and target status | Health/shield/resource displays, status effects, target information, cast bars |
| Actions and combat operation | Ability slots, cooldowns, weapon/ammunition indicators, reticles, input prompts, hit feedback |
| Items and builds | Item/equipment slots, card views, attribute rows, upgrade nodes |
| Objectives and spatial guidance | Quest entries, objective markers, map nodes, navigation and area indicators |
| Narrative and decisions | Dialogue panels, speaker information, dialogue/event choices |
| Trade and rewards | Offers, prices, purchase conditions, reward options, acquisition notices |
| Match and progression | Turn/phase indicators, timers, scores, result entries |
| Social and multiplayer | Party members, chat messages, room members, matchmaking status, leaderboard entries |
| System and assistance | Save slots, settings rows, input bindings, device prompts, tutorial hints |

Extend by mechanism when needed, such as production queues, tactical initiative or rhythm judgments. Cross-reference components used in several categories while retaining one maintenance owner. Main menus, inventory screens and combat HUDs are compositions; category counts do not determine family counts or require separate assets.

## Establish and select families

Inspect existing UI sources first. Use representative components and actual contexts to establish the arrangement, then expand supported needs. A small project may express it in its existing design section; extensive independent use may justify a dedicated reference under the normal [material rules](material-requirements.md). Retain existing Task/Spec, component manifests, sample scenes and runtime resources as their respective authorities.

| Information needed for affected work | What it should answer |
|---|---|
| Grounds and scope | Which selected sources/versions apply, to which members and uses, and which directions remain undecided? |
| Members and roles | What does each component do, and which foundation or family does it inherit or compose? |
| Shared constraints | Which visual features and interaction meanings remain stable? Reference actual parameters/resources and representative appearance. |
| Variants and usage | Which differences may callers select, under what conditions, and which contexts need a different component/family? |
| Implementation and production entrypoints | Where are the shared component, style/data, editable/generation source and real consumers maintained or planned? |
| Examples and verification | Which states and contexts demonstrate the arrangement, and what existing or missing evidence supports the current claim? |

This information can be distributed across existing sources with precise references. Actual style resources own their values; design explains intent and boundaries rather than copying another manually maintained parameter table. Proposed entrypoints remain plans until implemented.

Select by observable behavior first: executing a command, switching a persistent tab, choosing an exclusive option and toggling a setting have different responsibilities even when their shapes resemble buttons. Then select the applicable family and supported variant. Keep size, emphasis and semantic intent distinguishable; current hover/focus/pressed/selected/disabled states follow behavior rather than becoming manually assigned themes. Document meaningful combined states where applicable.

Reuse a sufficient component, then a supported variant; extend only when necessary differences remain. Size, color or ornament changes usually fit a variant. New content structure, behavior or independently necessary constraints may justify a component or family; explain the difference and allowed uses. Build only combinations needed by current consumers. Candidate examples and authorized experiments may refine the arrangement before wider production.

## Production and implementation

For UI content production, carry the applicable family, variant, baseline and state requirements into real tool inputs and editable/export sources. Match geometry, text/icon safe areas, scaling and required state assets to consumers. Follow [production review](../skills/assets/references/production-and-review.md) for representative baseline comparison before expansion and [asset handoff](asset-handoff.md) for versions and permitted uses; one family need not mean one image, atlas or generation job.

Map shared appearance to actual themes, style resources, tokens or equivalent sources and shared behavior to components/navigation mechanisms appropriate to the stack. Pages supply content, business actions, layout and supported options. Keep caller overrides within defined variation boundaries; repeated necessary exceptions should update the responsible definition. Inspect current implementation before introducing another shared layer, and follow [structural ownership](../profiles/references/structure-contract.md) for real state/lifecycle boundaries.

Cross-interface interaction covers applicable confirm/back, focus entry/restoration, modal input, pause/resume, device changes and feedback conventions. Components own their relevant activation, selection, disabled, drag/drop or other behavior. Gameplay state remains with its actual owner; shared style/definition resources must not accidentally share mutable per-instance focus, selection or animation state. Preserve visible focus alongside selected states when both apply.

Use existing component samples or a small runnable showcase when it helps independent reuse and review. Cover relevant states, content lengths, scales and backgrounds using the actual shared implementation; a showcase is an aid, not another mandatory tool project. Representative success establishes its tested scope while full delivery still follows the original commitments.

## Change and verify

When shared grounds, variants or behavior change, use [original change handling](../skills/flow/references/change-work.md) to identify affected members, consumers and evidence. Correct the responsible design, resource or generation source, propagate the intended change, retain valid history and recheck affected uses. Selecting another family or rejecting one member does not invalidate every other family automatically.

Match checks to the claim under [verification conventions](verification.md):

- Design delivery: check usable family selection, shared/different responsibilities, scope, representative expression and locatable planned/current entrypoints. A category list alone does not establish a usable family arrangement.
- Content production: compare relevant outputs/states with the applicable baseline at target display conditions; internal pack consistency or correct export alone does not establish style conformity.
- Implementation: follow actual resource/component references into affected pages, HUDs or world-space consumers. Observe applicable interaction paths, compound states, instance isolation, input modes, text adaptation and context changes; declarations or static screenshots alone do not prove these behaviors.
- Shared changes: check affected consumers and distinguish intended contextual differences from accidental overrides, duplicate behavior or stale sources. Reuse unchanged evidence; do not impose a fixed screenshot count or full-project regression on a local change.

Record technical checks, model observations, required human acceptance and actual runtime adoption in their existing sources with their actual scope. Family names, sample approval and component reuse do not automatically establish every page's acceptance.
