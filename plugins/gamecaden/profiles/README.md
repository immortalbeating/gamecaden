<a id="游戏工程-profiles选择采用与复核"></a>
# Game engineering profiles: selection, adoption and review

A Profile is a conditionally loaded engineering reference, not an extra Skill, task stage or automatically effective set of project-wide gates. [shared/rules](../shared/rules.md) owns rule nature and conflict handling; this page owns selection and integration of these references.

<a id="定位与规则纳入"></a>
## Purpose and rule inclusion

This workflow draws guidance from development practice across multiple channels, reliable materials and still-applicable industry approaches, helping AI choose game design, engineering and content approaches, identify common failures early, and check expected results along actual player paths. Records and checks support these judgments; document counts, rule counts or tool success do not replace game goals.

When adding or promoting rules/topics, judge whether the following are sufficient:

- **Which detour is avoided**: Identify transferable failure patterns or design tradeoffs and their effect on gameplay, content, implementation or delivery; background terms, market labels and possible future use are insufficient to establish a new topic.
- **Whether the basis is reliable and still applicable**: Express official mechanisms, actual project experience, industry approaches and workflow choices separately. Retain sources, versions/environments, applicability conditions and counterexamples; review historical approaches against current mechanisms, while single-project compromises retain original scope.
- **Whether it helps the next action**: Specify triggers, outcomes to preserve, reasons, defaults/alternatives and discriminating observations; checking intensity matches current claims.
- **Whether independent maintenance is worthwhile**: Shared rules own general principles and corresponding topics explain engine differences; supplement existing sections nearby when they can serve the content. Guidance benefits of new topics should cover loading, referencing and ongoing calibration costs.

Judge general value within this workflow's game-development scope; every lesson need not have occurred in the user's personal projects. Actual use still follows current goals; platform examples in materials do not automatically become project commitments or package support scope. Inferences lacking sufficient basis/scope remain investigations/recommendations, without being labeled industry-wide rules or required gates.

<a id="选择本次需要的部分"></a>
## Select what this work needs

First determine current objects, actual runtime roots, engine/framework versions, target platforms and actions. Read existing project configuration and effective agreements; retain unknowns where materials are insufficient. Existing design choices may guide plans without masquerading as installation/runtime facts.

| Profile ID | When to read | Body |
|---|---|---|
| game-common | Gameplay, shared state, content integration, lifecycle or runtime acceptance is affected | Applicable entries in [common game engineering](common.md) |
| project-structure | Creating project structure, adding modules/production pipelines, migrating paths or ambiguous directory responsibilities | [Directory and file responsibilities](project-structure.md) |
| godot | The runtime root designed/modified here actually uses Godot | [Godot](engines/godot.md) |
| unity | The runtime root designed/modified here actually uses Unity | [Unity](engines/unity.md) |
| cocos-creator | Current runtime roots or selected designs use Cocos Creator | [Cocos Creator](engines/cocos-creator.md), with platform rules selected separately by actual build target |
| web | Current objects run in browsers, including native pages, browser outputs of engines/frameworks and tool pages | [Web platform](platforms/web.md) |
| phaser | Actual dependencies of current runtime roots or selected designs use Phaser | [Phaser](frameworks/phaser.md), adding Web for browser targets |
| threejs | Actual dependencies of current runtime roots or selected designs use Three.js | [Three.js](frameworks/threejs.md), identifying target platforms and local integrations separately |

[Material responsibilities](../shared/material-requirements.md) and [game material references](../skills/design/references/game-deliverables.md) own game-domain diagrams/information; go directly to applicable parts for current uses. For changes to composition, state, lifetime or resource consumers, use [structure topics](#topic-entries-for-structural-changes) below; for browser paths, focus, background, audio or storage conditions, use [Web handoff](platforms/web.md#handoff-to-skill-stages). Untouched domains need not be loaded.

Selection is "applicable common entries + actual engine/library + target platform". Web is a browser platform, without restricting Phaser or 2D; handle scenes, runtime scopes and resource relationships using actual engine mechanisms. Other unlisted stacks may still use common entries and their actual official documentation; do not apply the nearest engine API merely because this table lacks a dedicated name.

<a id="组合示例"></a>
### Combination examples

- Godot desktop character integration: common content/state entries + Godot; read character materials according to actual integration.
- Godot Web export: Godot + Web; do not load Phaser.
- Fixing a co-located HTML asset panel: Web + panel contract; add game-engine scope only when game runtime input changes.
- Phaser game pause/restart: common lifecycle + Web + Phaser, checking actual major versions.
- Three.js browser game: applicable common entries + Three.js + Web; check actual React/R3F integration only when adopted.
- Cocos Creator Web outputs: applicable common entries + Creator + Web; for other explicit targets, check actual build/runtime conditions and official documentation nearby.
- Creator native game: applicable common entries + Creator + local native-build rules, with evidence tied to actual delivery entries.
- Pure static HTML small game: applicable common entries + Web, retaining existing startup methods.
- Only fixing a typo on an existing button: use quick directly when original Task, relevant display checks and effective rules suffice; no need to read every directory, character, map or release rule.

One repository may have multiple runtime roots; combinations target current objects without adding every technology name in the repository. Networking, performance, multiplayer collaboration and similar branches trigger only through actual commitments or risks.

<a id="规则怎样写"></a>
## How to write rules

Short IDs in files reference individual entries, retaining existing object, action, scope, basis and review semantics. They are not project Gate IDs and create no new business lifecycle.

Entries explain triggers, rule nature, expected behavior and observable checks. Required conditions constrain outcomes; defaults let models choose other methods meeting conditions. Even when labeled "required" in tables, rules depend on triggers applying; available documentation, existing materials and successful scripts do not automatically establish actual requirements being met.

Further distinguish the meaning of bases: **engine facts** are checked through version-specific official documentation/local results; **official best practices** provide optional organization methods; **workflow defaults** explain adoption reasons, permitted alternatives and counterexamples; **project experience** states premises, distinguishing effective practices, failure patterns and compromises at the time. Reference actual sources and acceptance near the same rule group, without asking users to fill another source ledger entry by entry.

<a id="结构变化的专题入口"></a>
## Topic entries for structural changes

When adding independent pages/levels, reusable entities, cross-lifecycle state, listeners or content-editing methods, first clarify current composition/responsibilities using the [shared structure contract](references/structure-contract.md), then take applicable engine topics:

| Current framework | Topic |
|---|---|
| Godot | [Scenes, nodes and state](references/godot-structure.md): actual node types, runtime trees/scene boundaries, parent/owner, World/UI, Autoload and editing/saving |
| Unity | [Scene, Prefab and state](references/unity-structure.md): serialized wiring, instances/definitions, lifecycle, UI systems and editable content |
| Cocos Creator | [Scene, node components and resources](references/cocos-structure.md): saved resources/runtime trees, Node/Component, enable/disable/persistence, asset references, UI editing and target platforms |
| Phaser | [Scene and display objects](references/phaser-structure.md): Scene runtime scopes, ordinary-object modules, global/local systems, UI and listener/resource consumers |
| Three.js | [Rendering trees, runtime and resources](references/threejs-structure.md): Scene/Object3D, renderer/loops, page lifetimes, shared resources/explicit release, DOM/3D input |

For new projects with selected stacks but no engineering project yet, form necessary initial design first, mark native sources as pending creation, and do not describe planned wiring as saved/runtime facts. Existing projects reuse sources according to actual effects; when target relationships change or source semantics are insufficient, supplement differences in original design/Spec under applicable topics. Local quick changes do not reread everything; topics add no Skills, core entities or default mandatory files.

<a id="在项目中采用"></a>
## Adoption in projects

1. Retain adopted project rules. When new projects/scopes need agreements, models select relevant profiles according to actual engines, goals and existing authorization, explaining effects; users need not fill profile IDs or approve routine engineering choices individually.
2. Save lasting adoption scope nearby in existing Spec/rule sections: referenced profiles/entries, source versions or content summaries, runtime roots/platforms, project differences and what needs review after changes. Use the [project rules template](../templates/project-rules.md.tpl) only when original text lacks suitable locations. Temporary arrangements for current Tasks remain in original Tasks, without automatic promotion to project-wide requirements.
3. `workspace.yaml.rule_sources` still locates only actual rule files within project roots. Skills read package references through relative links; do not register host installation directories as out-of-bound project paths. When offline use, distribution or fixed versions truly require full text retention, save local version snapshots of selected references within authorized adoption scope, registering sources, versions and unique maintenance locations, and checking referenced dependencies remain reachable; copying one page while leaving broken relative links is incomplete. Keep project differences separately in original rules, without manually editing snapshots and upstream simultaneously.
4. Package updates do not equal project-agreement updates. Compare actual differences in adopted entries, then handle affected objects; when older versions cannot be located, retain the gap and investigate first, without silently applying another version. Unrelated entry changes do not require project-wide revalidation.

Package profiles ship with the skill package; fixed-version project snapshots are saved only when actually needed under adoption agreements above. Installing/upgrading skill packages does not automatically update effective project rules or generate project snapshots. Runtime facts still come from original project configuration; do not manually maintain another engine-version/package-dependency ledger in profile tables.

<a id="进入面板的边界"></a>
## Boundaries for entering the panel

Only rules/prerequisites actually adopted here and needing shared tracking are expressed at original owners under [governance](../shared/governance.md). Lasting rules belong to Spec, overall exit criteria to Epic/milestones, execution prerequisites to dependent Tasks; registering the entire profile directory as required conditions for every task incorrectly expands scope.

AI selects entries by current goals and checks local facts/material content; original Evidence/Decision still owns necessary check results. Pages display sources and instantiated conditions, without automatically deriving every gate from arbitrary profile prose. Tool matching and semantic judgment have separate responsibilities.

<a id="完成界限"></a>
## Completion boundaries

These files provide candidate common, Godot, Unity, Cocos Creator, Phaser, Three.js and Web browser rules; they are not complete engine manuals or capability adapters. For specific APIs, importers, plugins, rendering pipelines or build platforms, read actual installed versions and official documentation, using available specialist Skills/tools. When explicit targets exceed built-in references, continue investigating actual conditions, without blocking work for a missing dedicated profile or applying another environment's APIs.

Documentation/reference checks for these profiles do not equal end-to-end engine validation. See [release validation records](https://github.com/immortalbeating/gamecaden/blob/v0.1.3/docs/validation.md) for installation, upgrade and bounded pilots in existing new/old projects; actual results for particular profiles in target versions, platforms and consumers still require corresponding local evidence.
