<a id="unity-引擎-profile"></a>
# Unity engine profile

<a id="触发与版本边界"></a>
## Triggers and version boundaries

Use this when the actual project runtime root is Unity, or the current new-project design explicitly selects Unity. Unity 6 (6000.0) official documentation is this round's checking baseline; the local Editor version, Packages, rendering pipeline, target platform and project settings determine specific behavior. With only a design choice and no project, use this page to form arrangements while keeping runtime facts unknown. Before Unity is selected, treat it only as a candidate for comparison; this page does not assume Editor, CLI, MCP or build modules are available. Web Player targets additionally load the [Web platform profile](../platforms/web.md), without Phaser rules.

<a id="需现场识别的工程事实"></a>
## Engineering facts to identify in the project

- Project root, `ProjectSettings/ProjectVersion.txt`, `Packages/manifest.json`, effective Scene/Build Profile, target Player platform, and availability of Editor/build modules.
- Whether the affected object is a Scene instance, Prefab asset/instance, ScriptableObject asset, imported resource or runtime-generated object; who holds references.
- Play Mode Domain Reload/Scene Reload settings, static fields, event subscriptions and scene-switching paths.
- Whether this work concerns the physics clock, Update order, saves, Web export or asset migration; do not impose corresponding systems when unaffected.

<a id="条件规则"></a>
## Conditional rules

Rule nature follows [rules](../../shared/rules.md). Official Unity mechanisms support checks; choose specific directories and game architecture according to this project's design.

| ID | Nature and trigger | Requirement or default approach | Observable validation |
|---|---|---|---|
| UNITY-ROOT | Required: identifying or adopting a Unity project | Confirm runtime root and version using actual project settings, Packages and Scene/build configuration; presence of `Assets` or a document mentioning Unity is insufficient proof. | Current project identity, target scene and platform can be located; mark unverified when Editor has not run. |
| UNITY-META | Required: importing, moving/renaming original resources or creating resource copies | Preserve `.meta` pairing and GUID identity when moving/renaming originals. For new independent copies in the same project, generate new identities through the editor/a reliable process, avoiding two valid resources sharing one GUID; project migration preserves original identities and reference relationships. | After import, check affected Scene/Prefab/resource references for Missing, unexpected identity replacement or duplicate GUIDs; verify copies and originals are independent as designed. |
| UNITY-REFERENCE | Required: scene/Prefab/component wiring | Distinguish Prefab assets, Scene instances and serialized references; the target layer and override scope of changes must match consumers. | Component fields, events and runtime behavior on actual Scene/Prefab instances agree. |
| UNITY-SHARED-DATA | Required: a mutable ScriptableObject shared by multiple objects | Clarify whether it is a shared configuration asset or runtime instance state; do not mistake mutable values in one shared asset for each unit's independent state. | Cross-instance effects, exit/re-entry and re-entering Play Mode match the design. |
| UNITY-PLAY-LIFE | Required: static state, events or initialization depend on Play Mode/scene lifecycle | Arrange initialization/unsubscription according to local Domain Reload, Scene Reload and lifecycle settings; one successful Play does not establish safe repeated entry. | Subscriptions and state remain correct after consecutive Play Mode entries/exits and Scene reloads. |
| UNITY-UPDATE | Required: physics and per-frame logic interact or order is sensitive | Arrange input sampling, physics operations and presentation according to actual `Update`, `FixedUpdate`, etc.; when a fixed order is needed, confirm existing project settings and dependencies. | Rules and collisions follow project agreements at relevant frame rates/fixed timesteps; do not assume all physics simulation is bitwise deterministic. |
| UNITY-PLAYER | Required: a deliverable Player is promised | Specify target Build Profile, scene list, platform modules and build configuration; Editor Play results establish only Editor conditions. | Build and launch the actual target Player and follow this user path; distinguish build, startup and behavior failures. |
| UNITY-ASSET-HANDOFF | Required: formal asset integration | Trace source files, import settings, `.meta` identity, Prefab/Scene consumers and current candidate; successful import does not establish wiring or acceptance. | Validate references, display/actions and necessary runtime conditions in the actual consumer. |
| UNITY-STRUCTURE | Default: new systems, object reuse or structural boundary changes | For affected Scene/Prefab composition, shared definitions/instance state, lifecycle or UI systems, read corresponding sections of the [Unity structure topic](../references/unity-structure.md); choose components, Prefab, ScriptableObject or ordinary C# classes according to project needs. | State owners, serialized wiring and consumers can be located; relevant instances and entry/exit behavior follow the existing design. |

<a id="资源身份与结构"></a>
## Resource identity and structure

GUIDs in `.meta` carry Unity asset reference identity; preserve identity when changing a resource's path, while new independent resources need independent identities. Prefab assets and their instances, ScriptableObject assets and runtime state have different scopes; specify which layer this change affects during design. Directories and naming follow project conditions and [project structure](../project-structure.md); shared principles are in the [profiles overview](../README.md) and [common boundaries](../common.md). Do not migrate an existing project simply to adopt this profile.

<a id="与-skill-阶段交接"></a>
## Handoff to Skill stages

- `flow/init`: Register actual version, runtime root and effective project rules; confirm tool availability in the project environment.
- `brainstorm/design`: For affected new systems, Scene/Prefab composition, shared data, lifecycle or UI structure, read corresponding sections of the [Unity structure topic](../references/unity-structure.md) and specify owners, consumers and observable results in existing design/Spec; handle timing or build risks under corresponding rules.
- `develop/assets`: For structural quick changes, read only applicable [Unity structure topic](../references/unity-structure.md) entries, modifying corresponding assets and references within authorized scope; continue the same work identity for candidate, acceptance, selection and integration under [asset handoff](../../shared/asset-handoff.md).
- `verify/close`: Use the [verification contract](../../shared/verification.md) to distinguish Editor, target Player, human acceptance and release; reuse applicable results from original Task/Evidence/Decision records.

<a id="官网依据与未验证范围"></a>
## Official basis and unverified scope

- Unity 6 official: [Asset Metadata](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html), [ScriptableObject](https://docs.unity3d.com/6000.0/Documentation/Manual/class-ScriptableObject.html), [Event function execution order](https://docs.unity3d.com/6000.0/Documentation/Manual/execution-order.html), [Domain Reloading](https://docs.unity3d.com/6000.0/Documentation/Manual/domain-reloading.html), [Build Profiles](https://docs.unity3d.com/6000.0/Documentation/Manual/create-build-profile.html).
- This round did not adopt or run actual Unity projects, Editor, Player or CLI/MCP; version differences, installation state and build results for specific projects still require checks in their actual environments.
