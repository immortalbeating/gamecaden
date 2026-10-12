<a id="cocos-creatorscenenodecomponent-与资源生命周期"></a>
# Cocos Creator: Scene, Node, Component and resource lifecycles

Read this when adding Scene/Prefab, independent pages, reusable units, cross-scene state, pooling/external subscriptions, resource ownership, or changing editing/UI methods. First use the [shared structure contract](structure-contract.md), then read applicable mechanisms here; the [Cocos Creator profile](../engines/cocos-creator.md) determines versions and platforms. This page reuses that profile's IDs without synonymous Gates.

<a id="对象与制作源"></a>
## Objects and production sources

**Engine facts (3.8 documentation baseline)**: Node organizes the transform tree and holds Components; components provide rendering, input, physics or script behavior. Distinguish saved `.scene`/scene resources from runtime `Scene` root nodes; instantiating a Prefab resource produces a Node tree. Ordinary TS objects may hold rules/state without automatically receiving component callbacks. `World`, `GameSession` and `LevelHost` are optional project responsibility names; Canvas, UITransform, Sprite, MeshRenderer, etc. are components, not Godot node classes with similar names. [Scene resources](https://docs.cocos.com/creator/3.8/manual/en/asset/scene.html), [Runtime Scene](https://docs.cocos.com/creator/3.8/api/en/class/Scene).

**Workflow default**: Independently edited or repeatedly instantiated content uses suitable Scene/Prefab/components. Clear code factories, data generators and previews may continue to be used; choices must support current editing and validation outcomes. Components connect the engine; business models supply state through explicit data/action interfaces; simple local behavior may remain in one component.

| Applicable scope | Default and permitted alternatives | Common counterexamples | Observable acceptance |
|---|---|---|---|
| New pages or reusable units (COCOS-COMPOSITION) | Identify Scene/Prefab sources, Node/components, instance entries and necessary dependencies in original design; retain existing composition when it serves the purpose | Turning every TS class into a node; Prefab implicitly searching a fixed host path; copying runtime nodes without production sources | Wiring survives production-source reload; with necessary dependencies supplied, two instances or another host remain valid |
| Cross-scene/shared state (COCOS-STATE) | Hold read-only definitions separately from instance/current-session state; for actual Scene switches, use persistent roots/components meeting engine requirements or models held by the existing application layer | Globalizing local selections; modifying the same shared Asset as each unit's health; each Scene creating another persistent session | Two instances' independence/sharing matches intent; target state survives scene changes, new sessions reset as designed, with no duplicate persistent owners |
| Enable/disable/pooling/asynchrony (COCOS-LIFE) | Pair connection/cancellation by active scope; distinguish engine-managed work from own external-bus, SDK or native-timer work; late results check whether original request/consumer still applies | Adding external callbacks every onEnable but cleaning only on final onDestroy; ordinary helpers assuming component callbacks; old loading results overwriting new pages | Only expected effects after disabling, re-enabling, pool return/retrieval and switching; results after exit handled according to ownership |
| Loading/retaining/releasing (COCOS-ASSETS) | Track static/dynamic references; pair long-term dynamic retention through actual addRef/decRef or equivalent project resource ownership; locate still-active consumers before releasing Bundle/Asset | Mistaking JS field assignment for engine reference counts; always using releaseAll on exit; treating preload callbacks as already-created UI/runtime Scene | One consumer's exit leaves another displaying/running; reload, failure and expired returns are correct; necessary releases are not missed and still-shared content is not released |
| Resource migration/copying (COCOS-IDENTITY) | Original assets retain identity/import settings; new independent copies receive independent UUIDs, checking SpriteFrame and other sub-assets and actual fields | Recognizing resources only by path; losing .meta during moves; keeping two copies with one UUID; rebuilding all identities in bulk to resolve missing ones | After Editor import, affected Scene/Prefab, component fields and Bundle-loading consumers still correspond to correct objects |
| UI and editing (COCOS-UI) | UI roots use suitable Canvas/RenderRoot2D; UITransform handles rectangles, Widget alignment, Layout layout; camera and layer/visibility determine display; adapt size/safe areas/touch to targets | Treating Canvas as automatic layout or sole visibility guarantee; control layout competing with handwritten coordinates; masks display correctly but input passes through/is swallowed | Check actual target sizes, cameras/dialogs and input paths; scenes/Prefabs or generators provide usable editing/preview entries |

<a id="生命周期和常驻范围"></a>
## Lifecycle and persistence scope

onLoad/start handle corresponding one-time initialization, onEnable/onDisable component/node enable/disable, and onDestroy destruction callbacks; actual versions determine order and execution conditions. Judge disabling, removing from parents, pooling retention and actual destruction separately. Distinguish `destroy()` requests from end-of-frame reclamation; asynchronous and SDK callbacks do not automatically end because of them; retain identities for precise external-callback removal.

In 3.8, `director.addPersistRootNode` requires a target at the scene's root level; persistent nodes survive Scene switching without guaranteeing business uniqueness or new-session clearing. `removePersistRootNode` removes persistence, without immediate destruction. Ordinary models already held by suitable application objects may continue there; do not promote every utility function/local view into persistent nodes. [Lifecycle](https://docs.cocos.com/creator/3.8/manual/zh/scripting/life-cycle-callbacks.html), [Scene management](https://docs.cocos.com/creator/3.8/manual/zh/scripting/scene-managing.html).

<a id="资源引用与目标平台"></a>
## Resource references and target platforms

Asset Manager can analyze serialized static dependencies; ordinary dynamic JS assignment does not automatically reflect dynamic ownership. Maintain references/releases under actual ownership mechanisms; direct release/releaseAsset/releaseAll can release target resources directly, so their safety cannot be summarized as "the engine checks references". When resources remain shared, first handle actual owners and dependencies. Releasing runtime nodes, releasing Assets, removing Bundle manager entries and cleaning download caches are different actions, distinguished according to current targets. [Resource release](https://docs.cocos.com/creator/3.8/manual/zh/asset/release-manager.html).

Explain authoritative game state separately from relevant external-adaptation lifetimes. Browser builds use applicable [Web](../platforms/web.md) entries; for other explicit targets, check actual build/runtime conditions, toolchains and official documentation nearby. Preview-supported behavior establishes only its environment; collect actual delivery evidence according to current targets.

<a id="候选例子"></a>
## Candidate examples

These are illustrative designs, without project creation or execution, not fixed official templates.

**Single-Scene pickup experiment**: Nodes in Scene hold player/pickup components; repeated pickups may use Prefab with shared reward definitions, while the current scene component holds session score. A simple experiment need not first build persistent sessions or Bundle systems. Check rewards/disappearance for two instances, one actual pickup and score after restart; design-only delivery saves these arrangements without marking runtime success.

**Level transitions, settlement and new sessions**: Original design requires the results page to retain session score. One candidate uses persistent `SessionHost (Node + custom Component)` to hold the session model, consumed by `Play.scene` and `Result.scene`; responsibilities and code sources of this custom component must be locatable. Gameplay may compose:

```text
Play (Scene)
├── World (Node + gameplay/physics/rendering root components needed here)
│   ├── CurrentLevel (Node, level/Prefab instance root)
│   └── Player (Node, outside the level if retention is required for this level change)
└── HUDRoot (Node + Canvas + UITransform)
    └── ScorePanel (Node + UITransform + required layout/display components)
```

If World uses Sprite or other 2D rendering components, provide suitable RenderRoot2D/Canvas ancestors and UITransform, etc., under official mechanisms; for 3D content, use actual rendering/physics components and camera/layer. The tree illustrates composition ownership only; `World` does not imply rendering capabilities.

Actual `director` Scene replacement and local level replacement inside Play release different scopes; design must identify actual paths. Placing players outside CurrentLevel addresses only local replacement, without guaranteeing survival across actual Scene switching. HUD uses actual camera/layer wiring; results send new-session intent, with the session owner resetting before gameplay entry. Dynamic assets are retained/released by each consumer; validate switching, re-entry, multiple instances, remaining shared consumers and target-host paths.

<a id="输入来源与工作流交接"></a>
## Input sources and workflow handoff

When Scene/Prefab saves, second instances, cross-scene retention, pooling, late loading or UI wiring changes, reference actual Scene/Prefab, component properties/scripts, Asset/.meta, Bundle configuration, loading/reference-management implementations and actual UI/camera wiring to locate production sources, instance entries, definition/state, active lifetimes and resource consumers; do not manually copy full node trees, UUIDs or resource ownership inventories. Use sufficient existing sources directly; when adding shared, independent, retained or exit relationships, add current-to-target differences to original Task/design even if source is readable. If semantics are unclear, add relevant relationship explanations or necessary local relationship/timing expressions, selecting methods under [material references](../../skills/design/references/game-deliverables.md).

When Creator is selected but no project exists, first form necessary initial design and mark native sources as pending creation; planned components, resources and wiring do not represent saved or running facts. Browser common conditions use [Web handoff](../platforms/web.md#handoff-to-skill-stages); other targets follow platform boundaries here. develop/assets implement actual production sources and consumers; verify checks saves, instances, enable/disable, resources and target entries according to current claims, with results in original Evidence/Decision records.

<a id="来源与交付边界"></a>
## Sources and delivery boundaries

Documentation checked: 2026-10-01. Technical facts refer to links above and official [nodes/components](https://docs.cocos.com/creator/3.8/manual/zh/concepts/scene/node-component.html), [project structure](https://docs.cocos.com/creator/3.8/manual/zh/getting-started/project-structure/index.html), [asset workflow](https://docs.cocos.com/creator/3.8/manual/zh/asset/asset-workflow.html), [Canvas](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/components/editor/canvas.html), [UITransform](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/components/editor/ui-transform.html), [Widget](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/components/editor/widget.html) and [Layout](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/components/editor/layout.html). Earlier examples retained in 3.8 documentation do not directly establish all-API compatibility with other versions.

Default approaches and observation methods are workflow choices. Design consistency, Editor save/wiring, runtime behavior, target builds and human acceptance remain separately reported under [shared evidence](../../shared/verification.md), within original Task/Evidence/Decision records. This round checked only documentation and did not run Creator or any candidates.
