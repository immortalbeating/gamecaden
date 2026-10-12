<a id="cocos-creator-工程-profile"></a>
# Cocos Creator engineering profile

<a id="触发与版本边界"></a>
## Triggers and version boundaries

Read this when the actual runtime root uses Cocos Creator, or the current design has selected it. First check the actual Creator/engine version, entry scene, modules, rendering/physics settings, plugins and target platform. Mechanism documentation in this round uses 3.8 LTS; check corresponding mechanisms first for 2.x, 4.x or other local versions, without requiring an upgrade.

Confirm target platform and engine separately. Browser targets add [Web](../platforms/web.md); for other explicit targets, check local build/runtime conditions and corresponding official documentation, retaining separate evidence for preview and actual outputs. Do not merge Cocos2d-x and Creator into one project type based on their names.

<a id="需现场识别的事实"></a>
## Facts to identify in the project

- Current project configuration, actual editor and runtime engine versions, startup Scene, build target and output; when delivering only a design without a project, retain these runtime facts as unknown.
- Whether the current object is a Scene/Prefab resource, Node/Component instance, shared Asset, ordinary TS model or build adaptation code; its editing source and actual consumer.
- Actual relationships among node/component enable/disable, scene switching, pooling, external events, platform foreground/background behavior, dynamic loading and resource ownership.
- Affected resources' `.meta`, UUID/sub-assets, property wiring, Bundle/path/type, remote resources and platform cache sources.

<a id="条件规则"></a>
## Conditional rules

Rule nature follows [shared/rules](../../shared/rules.md). Required outcomes apply when triggered; default organization permits alternatives serving the same purpose.

| ID | Nature and trigger | Requirement or default approach | Observable checks |
|---|---|---|---|
| COCOS-ROOT | Required: adopting or confirming an actual project | Identify version and runtime root from actual configuration/Editor, entry and target; a planned engine or installation directory cannot substitute for project facts. | Current sources and target outputs can be located; without a project, report only the selected design target. |
| COCOS-COMPOSITION | Required: new Scene/Prefab, reusable objects or structural changes | Distinguish saved resources, Node, Component and ordinary models according to the [structure topic](../references/cocos-structure.md); clarify assembly, dependencies, editing and actual types. | Save/reload, Prefab instance wiring and necessary independent instances match the design; directory/node counts do not prove compliance. |
| COCOS-STATE | Required: shared configuration, cross-scene or multi-instance state | Distinguish shared Asset/definitions from per-instance/current-session mutable state; persistent nodes or existing session models hold it according to actual lifetime, with explicit new-session reset. | Modifying one instance does not unintentionally change others; retention/clearing on switching and new sessions follows the original design. |
| COCOS-LIFE | Required: enable/disable, pooling, scene switching, listener or asynchronous changes | Distinguish onLoad/start, onEnable/onDisable, onDestroy and ordinary objects/platform jobs; manage own external callbacks and late results according to actual active scope. | After disable/restart, pool return/retrieval and switching, call counts and old results match the design; confirm destruction requests and actual reclamation separately. |
| COCOS-IDENTITY | Required: moving, renaming, copying or importing resources | Preserve the original asset's `.meta`/UUID and actual sub-asset references; new independent asset copies receive independent identity. Investigate missing/conflicting identities, then use a reliable editing/recovery process. | Affected Scene/Prefab/component fields and dynamic loading still point to correct resources, without unexpected missing resources or duplicate identities. |
| COCOS-ASSETS | Required: dynamic loading, Bundle or releasing shared assets | Locate path/type/Bundle/consumers; distinguish preloading, loading, instantiation and integration. Choose retention/release based on static/dynamic references and shared lifetime; direct release methods are not safe reference checks. | Late/failed/re-entry results do not write back to old consumers; other consumers remain valid after one exits, and objects/resources that require release do not accumulate. |
| COCOS-UI | Required: UI layout, camera, input or adaptation changes | Organize by actual responsibilities of Canvas/RenderRoot2D, UITransform, Widget/Layout, Camera/layer, etc.; layout, display and input each have clear sources. | Position and hit detection are correct at target sizes, safe areas, masks/dialogs, cameras and touch conditions; merely attaching Canvas does not prove visibility or operability. |
| COCOS-TARGET | Required: this commitment includes target outputs or platform integration | Check builds, modules, resources and relevant capabilities against the local version and actual target; retain separate evidence for Editor/Web previews, target builds and delivery entry. | Observe this user path from the actual delivery entry, with evidence identifying version, environment and actual coverage. |

<a id="与现有职责交接"></a>
## Handoff to existing responsibilities

init locates the actual or planned engine and platform; design writes relevant composition/lifetime/editing/observation into the original design and reads the [structure topic](../references/cocos-structure.md). develop/assets modify actual production sources and consumers, preserving the scope of candidate, acceptance, selection and runtime integration under [asset handoff](../../shared/asset-handoff.md). verify/close reuse original Task/Evidence/Decision records and add evidence for saves, instances, enable/disable, switching and target outputs affected by actual changes.

Reuse existing projects and editing methods when they can deliver this work; when a defect comes from incorrect state or lifetime boundaries, address the necessary scope locally. Text-only quick changes take only display and original closeout requirements, without rebuilding the entire scene/Bundle/platform chain.

<a id="官方来源与本轮范围"></a>
## Official sources and scope of this round

- [Nodes and components](https://docs.cocos.com/creator/3.8/manual/zh/concepts/scene/node-component.html), [Project structure](https://docs.cocos.com/creator/3.8/manual/zh/getting-started/project-structure/index.html), [Asset workflow](https://docs.cocos.com/creator/3.8/manual/zh/asset/asset-workflow.html): objects, production sources and asset identity.
- [Lifecycle](https://docs.cocos.com/creator/3.8/manual/zh/scripting/life-cycle-callbacks.html), [Scene switching](https://docs.cocos.com/creator/3.8/manual/zh/scripting/scene-managing.html), [Resource release](https://docs.cocos.com/creator/3.8/manual/zh/asset/release-manager.html): callbacks, persistence scope and resource reference mechanisms.
- [Canvas](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/components/editor/canvas.html): UI/camera boundaries; check version-specific documentation for a particular build target once it becomes an actual commitment.

Documentation checked: 2026-10-01. Factual sources are listed above; organizational defaults and acceptance choices belong to Gamecaden. This round did not run Creator/games, build target packages or validate platform SDKs, and does not establish market usage rankings.
