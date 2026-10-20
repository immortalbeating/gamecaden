<a id="通用游戏工程规则"></a>
# Common game engineering rules

For work that actually changes game behavior, content integration or runtime delivery. Select entries using the triggers below; project size, file count and Task mode alone do not determine validation depth. Pure discussion first forms the corresponding design; when execution is authorized, continue to implement actual results.

[material-requirements](../shared/material-requirements.md) owns material requirements; see [records](../shared/records.md) and [verification](../shared/verification.md) for record and validation semantics. This page adds consumer, state and timing constraints easily missed in game engineering.

These entries turn transferable development experience and applicable mechanisms into a basis for judgment, helping design and implementation advance toward established gameplay/experience. Review inclusion, sources and current applicability under [profiles](README.md); keep required outcomes clear while projects and models choose methods. Complete formatting, scene separation or technical success supports only the corresponding scope; whether the target game meets expectations still requires its actual mechanisms, player paths and necessary acceptance.

<a id="工程与玩法"></a>
## Engineering and gameplay

| ID | Trigger | Requirement or default approach | Observable checks |
|---|---|---|---|
| GAME-OWNER | New mechanics, cross-interface/scene state or multiple consumers of the same data | **Required**: Player input can be traced to a single writing responsibility, state changes and display/save consumers. Presentation state may be locally owned; **default**: compose responsibilities through clear interfaces, without mandating ECS, MVC, event buses or a fixed scene count. | The changed entry actually triggers target state; other readers receive the same fact; destroying a local view does not incorrectly clear game data that should persist. |
| GAME-LIFETIME | Entry/exit, failure retry, pause, repeated loading or asynchronous return | **Required**: Current-session/scene/global object lifetimes are clear; creators manage the external subscriptions, asynchronous jobs and temporary state they add, following the engine's actual automatic cleanup semantics. | Re-entry, restart or cancellation does not cause duplicate triggers, leftover input or old callbacks overwriting new state; handle results that currently need retention on exit. |
| GAME-TIME | Movement, combat, timing, animation-driven events, pause or offline progression is affected | **Required**: Explain who owns rule time, how presentation and rules synchronize, and how pause/resume is handled. **Default**: use engine timing suitable for this gameplay; introduce fixed timesteps, deterministic replay or offline catch-up only when actually needed. | Under relevant frame-rate, pause, background or restart conditions, results follow the rules; validate audiovisual effects and hits through actual triggers, rather than treating animation existence as proof of event wiring. |
| GAME-SPACE | Maps, cameras, collision, navigation, character scale or input coordinates are affected | **Required**: Design space, runtime coordinates and display conversions correspond; asset appearance and collision/navigation each have checkable sources. | Follow the target route through actual entry, ability state and camera; local position injection may diagnose issues, but acceptance of natural reachability still needs actual player paths. |
| GAME-STRUCTURE | New independent pages/levels, reusable entities, cross-lifecycle state or editing changes | **Required**: Before relevant implementation, clarify actual types and composition, authoritative state sources, creation/end/reset, external dependencies and editing/observation methods; reuse valid existing designs. Expression follows the [structure contract](references/structure-contract.md), with engine mechanisms implemented by corresponding topics. | Compare actual saved/declared sources with runtime consumers; check multi-instance, switching, re-entry and editing capabilities within applicable scope; file counts or empty managers do not establish modularity. |

Repeated entry is not a gate requiring an arbitrary fixed N runs; repetition count, object count and observation points should suffice to expose relevant residual behavior and interference. Simple games without cross-scene state need not prebuild a global state service.

<a id="内容体验与持久化"></a>
## Content, experience and persistence

| ID | Trigger | Requirement or default approach | Observable checks |
|---|---|---|---|
| GAME-CONTENT | Replacing/generating runtime characters, maps, actions, effects, sounds or models; configuration only when it needs independent content identity, selection or review | **Required**: Link specific candidates, uses and consumers under [asset handoff](../shared/asset-handoff.md); check preview and actual runtime separately. Visual/audio replacement should not incidentally alter hit areas, resource keys, timing or gameplay values without authorization. | Actual consumers load the correct version; scale/direction/anchor/time or attachment positions match current design; old references and fallback behavior are explainable within affected scope. |
| GAME-DATA | Creating or expanding gameplay definitions needing repeated tuning, reuse or variants, or changing their editing/loading path | **Default**: Maintain these definitions in independently editable project resources/data files or existing typed-data/table pipelines, wired to actual gameplay consumers. Reuse sufficient current arrangements; choose format and grouping by engine and editing needs. | Trace the maintained definition through loading/assembly to its consumer; relevant parameter or compatible-variant changes affect gameplay. File creation or parsing alone does not establish adoption. |
| GAME-EXPERIENCE | Changes to player journey, UI hierarchy, controls or feedback | **Required**: Key actions can be discovered, performed and produce results; return/pause/cancel have consistent ownership; check actual target devices and display conditions. **Default**: cover these changes with the fewest sufficient paths. | Follow the user's actual entry through this operation to observable results; static images support only visual claims, without proving subsequent interaction. |
| GAME-PERSISTENCE | Saves, progression, rewards, equipment, economy or cross-level results are affected | **Required**: Clearly distinguish runtime state, persistent storage and reconstructed views; existing rules determine save/load/reset and repeated-operation semantics. Explain compatibility, migration or fallback when old data formats change. | Use isolated test data through change → save → reload → actual consumer, checking relevant interruption/repetition paths. Verify repeated requests when preventing duplicate claims; in-memory values or fake storage alone are insufficient. |
| GAME-SUPPLY | Third-party content, plugins, generation services or new production pipelines affect delivery | **Required**: Retain sources, applicable licenses/usage conditions and actual processing relationships; identify owners of inputs, generated outputs and runtime outputs. Costs, external writes and tool use follow existing authorization. | Files are traceable and usable by this project; generation logs/license text do not replace file and consumer checks. Purely self-made local fixes do not add procurement review. |

Consumers for concept exploration may be design discussion or style selection; require engine consumers only when the request includes runtime integration. Standalone concept-art work is not blocked by absence of runtime scenes and does not automatically become formal runtime assets.

### Data maintenance

Use the game's resource/data locations as maintenance entries. Existing types/schemas express field meaning, units, defaults and reference constraints where needed; original Task/design/Spec references those sources and their consumers instead of mirroring values in another management ledger. When a table generates runtime files, maintain the authoritative input and regenerate its derivatives.

Ordinary engineering definitions remain with these owners; a configuration file alone does not trigger asset registration. GAME-CONTENT applies when independent content identity, selection or review is actually needed.

Keep behavior rules and mutable instance state under [existing ownership conventions](references/structure-contract.md#express-it-in-the-original-design); compatible data variants use implemented mechanisms, while new mechanics may need code. Local serialized fields can remain with their scene/component; bounded experiments and stable implementation constants can retain their current form. Apply the default to affected content rather than migrating unrelated definitions.

<a id="规模与交付"></a>
## Scale and delivery

| ID | Trigger | Requirement or default approach | Observable checks |
|---|---|---|---|
| GAME-SCALE | Explicit performance targets, or added scale/loading/memory pressure affects commitments | **Required**: Target scale, scenario, platform and measurement conditions match the current claim; actual bottlenecks determine optimization. **Default**: first use local measurements that answer the question, then cover committed scale. | Small-scale smoke checks support only small scale; when target conditions cannot be executed, state the gap without treating reduced targets as successful optimization. Other projects' unit counts/GPU models are not this project's thresholds. |
| GAME-DELIVERY | The request concerns release packages, target devices, deployment or upgrade compatibility | **Required**: Check actual delivery outputs, resources and startup paths; retain evidence separately for development server/editor, export/build, external runtime and release. | Start affected paths from the delivery entry; identify outputs, platforms, dependencies and uncovered scope; routine development fixes do not thereby require all-platform packaging. Git actions follow [git-policy](../shared/git-policy.md). |

<a id="怎样成为本项目约束"></a>
## How these become project constraints

This table states the outcomes to preserve when triggers apply. Specific cameras, world scales, diagram counts, frame counts, devices, latency or performance values come from current design and engineering facts; write them into original Spec/rules when lasting constraints are needed, while short-term experimental assumptions remain in original Tasks.

When a check fails, first determine whether it expresses a currently valid requirement. For example, after adding assets, an old "total must equal exactly N" check should return to the required asset set and consumer checks; do not delete valid content to satisfy outdated counts. Check methods and tools may change, but current commitments and their required coverage still must be met.

Reference reusable existing materials and evidence directly, reviewing only genuinely affected parts. Missing formal character production materials do not block unrelated text fixes; exceptions and rule changes follow judgment and recording locations in [rules](../shared/rules.md).
