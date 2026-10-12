<a id="unity-结构对象职责状态与-ui"></a>
# Unity structure: object responsibilities, state and UI

<a id="何时读取"></a>
## When to read

When creating Unity systems, changing Scene/Prefab composition, shared definitions/instance state, cross-scene lifecycles, or selecting/adjusting uGUI or UI Toolkit wiring, read applicable sections. Quick changes load only affected entries and their acceptance checks. The [Unity profile](../engines/unity.md) still determines versions, resource identity and delivery; this page implements UNITY-STRUCTURE, UNITY-REFERENCE, UNITY-SHARED-DATA and UNITY-PLAY-LIFE without another set of Gates.

The [structure contract](structure-contract.md) owns common triggers, record ownership in existing design/Spec, adoption boundaries for new/existing projects and design/runtime acceptance. This page adds only relevant engine mechanisms and candidate approaches.

<a id="引擎事实与工作流选择"></a>
## Engine facts and workflow choices

Mechanism references use Unity 6 (6000.0); local Editor, Packages, Play Mode settings and selected UI systems take priority. Official facts: Scene saves scene content; GameObject provides behavior through components, MonoBehaviour receives engine callbacks; Prefab is reusable object configuration with possible instance overrides; ordinary C# objects have no automatic MonoBehaviour callbacks. ScriptableObject assets can share definitions, but that does not make assets a place to write runtime saves. Default responsibility arrangements are this workflow's approach; Unity does not mandate a particular game architecture.

| Required outcome and trigger | Workflow default / permitted alternatives | Common counterexamples | Observable acceptance |
|---|---|---|---|
| Entries, behavior and instance differences can be determined for new objects/reusable units | Scene composes levels/runtime scopes; Prefab represents repeated entities or UI units; components connect engine lifecycle, input, physics and presentation; ordinary C# classes may hold independent rules/data. Simple behavior may stay in one component; retain valid existing composition. | Creating a GameObject for every class; piling all rules and entity state into a Scene manager; copying instances without checking overrides. | Locate entries and required components from Scene/Prefab; two instances run independently; changes to definitions/instance overrides affect the designed scope. |
| Definitions and mutable runtime state have explicit ownership when shared across instances | ScriptableObject or serialized configuration holds definitions; each instance/current-session model holds mutable state such as health. Intentional shared runtime state or runtime ScriptableObject instances are allowed, with creation, owner, reset and release identified. | Multiple units directly modifying health in one configuration asset; treating static fields or Inspector defaults as automatic new-session reset. | Two consumers share parameters while instance state is independent; new sessions/re-entry restore designed values; intentional shared changes affect only specified consumers. |
| State and subscription lifetimes agree when lifecycle/cross-Scene behavior changes | Distinguish object enable/disable, Scene load/unload, current-session, application and save lifetimes; creators pair initialization and cleanup. Choose Awake/OnEnable/Start/OnDisable/OnDestroy by actual use; explicitly coordinate cross-object order dependencies. | Using Start to assume every dependency completes in some order; subscribing in every OnEnable but unsubscribing only on final destruction; persistent objects referencing unloaded Scene components. | Enable/disable, Scene round trips and repeated Play leave only expected instances/subscriptions; new-session reset and save restoration are separately correct. |
| Scene/Prefab wiring is editable and checkable | Prefer serializable fields and Inspector wiring for fixed local references; dynamic generation, dependency injection and runtime queries also work if failures and sources can be checked. Serialize ordinary classes under Unity's supported field rules, choosing inline values or SerializeReference according to shared identity needs. | Assuming arbitrary properties, dictionaries and ordinary class references serialize normally; global name searches hiding dependencies; inspecting only Prefab assets without instance overrides. | Check actual Scene/Prefab fields, overrides, UnityEvent or runtime binding sources; missing references provide locatable feedback; wiring and data survive save/reload. |
| Layout, input and state have definite boundaries when UI structure/system choices affect delivery | Identify existing UI systems first; uGUI uses Canvas/GameObject, RectTransform and layout components suited to the target; UI Toolkit uses UIDocument, VisualElement trees, UXML/USS and its layout/events. Choose according to local capabilities; mixing is allowed with hierarchy, focus/input and state interfaces specified. | Treating VisualElement as a Scene GameObject that accepts MonoBehaviour; treating ordinary Transform parent-child trees as automatic UI layout; buttons and gameplay models each holding writable copies of state. | Locate layout sources, bindings and callbacks in the actual system; target sizes, display changes, focus/input and data updates match established behavior; UI reconstruction does not duplicate callbacks. |

<a id="持久范围的选择"></a>
### Choosing persistent scope

For cross-Scene state, first ask whether it must survive one switch, a whole session or the application. By default, put authoritative state in an existing model/owner covering that lifetime, with Scene components as consumers. `DontDestroyOnLoad` root objects, persistent/additively loaded Scenes or existing application layers are allowed; these are methods requiring checks for duplicate creation, invalid references and new-session reset. `DontDestroyOnLoad` retains the target root object and children; one call alone does not prove the state contract correct. Domain Reload settings also affect static fields, and scene unloading does not equal clearing all static/external subscriptions.

<a id="序列化引用范围"></a>
### Serialized reference scope

`SerializeReference` identity and graph relationships for ordinary managed objects are saved within one serialization host; this does not guarantee the same instance across two MonoBehaviour/other UnityEngine.Object hosts. When persistent shared identity across hosts is needed, check suitable UnityEngine.Object/ScriptableObject references or the project's runtime model; separately validate that the same object was passed at runtime and that it remains the same object after save/reload. [SerializeReference](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SerializeReference.html).

<a id="ui-系统的版本判断"></a>
### Judging UI system versions

uGUI and UI Toolkit capabilities/support change by version; selection follows current world-space/screen UI, rendering, input, animation, binding and target-platform needs, checking local versions and package documentation. Official comparison pages provide capability comparisons without making recommendations mandatory migration for every project. UI Toolkit visual trees may be checked in corresponding tools such as UI Builder/Debugger, and uGUI in Hierarchy/Inspector; local conditions determine tool choice, and checks cannot be reported as performed without opening the editor.

<a id="候选例子"></a>
## Candidate examples

These are illustrative candidates for this approach, unrun and not official standard templates.

**Simple scene: one pickup.** Existing design awards score once per pickup. Scene contains player and pickup; repeated pickups use Prefab, with components handling contact/display and referencing read-only reward definitions; the current-session owner holds score. For one simple scene, a clear Scene component can manage score without first building a service layer. Acceptance follows actual input through one pickup, repeat triggering and level restart, checking reward counts, instance disappearance and score reset.

**Cross-scene: level end, results page, then new session.** Existing Spec retains session score on the results page and clears it for new sessions. Use `level component → current-session model ← results UI`; an owner spanning this switch holds the model, while level components and UI bind/unbind on entry/exit. Implementation may use a persistent root or persistent Scene; results use existing uGUI or UITK, with callbacks sending only "new session" intent. Acceptance runs level → results → new session twice, observing model, persistent owner count, score and callback counts; also check local settings for repeated Play entry.

<a id="输入来源与工作流交接"></a>
## Input sources and workflow handoff

When instance overrides, shared data, cross-Scene state or UI wiring changes, reference actual Scene/Prefab, Inspector bindings, ScriptableObject, selected UI resources and project/package settings to locate definition/instance differences, serialized references and state lifetimes; do not maintain another full GameObject, GUID or component inventory. Existing wiring expresses only current conditions: when future sharing, retention or UI relationships change, add target differences to original Task/design; where semantics are unclear, add necessary local relationship or lifecycle expression, selecting methods under [material references](../../skills/design/references/game-deliverables.md).

When Unity is selected but no project exists, form necessary initial design first and mark native sources as pending creation; planned bindings, settings and instance arrangements are not saved or running facts. develop implements actual sources; verify checks save/reload and runtime behavior according to current claims, with results remaining in original Evidence/Decision records.

<a id="官方事实来源与验证边界"></a>
## Official factual sources and validation boundaries

- [Scenes](https://docs.unity3d.com/6000.0/Documentation/Manual/CreatingScenes.html), [GameObjects](https://docs.unity3d.com/6000.0/Documentation/Manual/class-GameObject.html), [Prefabs](https://docs.unity3d.com/6000.0/Documentation/Manual/Prefabs.html): composition, component and reuse mechanisms.
- [ScriptableObject](https://docs.unity3d.com/6000.0/Documentation/Manual/class-ScriptableObject.html), [Serialization rules](https://docs.unity3d.com/6000.0/Documentation/Manual/script-serialization-rules.html): asset/ordinary-object and serialization boundaries.
- [Execution order](https://docs.unity3d.com/6000.0/Documentation/Manual/execution-order.html), [Domain Reloading](https://docs.unity3d.com/6000.0/Documentation/Manual/domain-reloading.html), [DontDestroyOnLoad](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Object.DontDestroyOnLoad.html): callbacks, Play Mode and persistence scope.
- [UI comparison](https://docs.unity3d.com/6000.0/Documentation/Manual/UI-system-compare.html), [UI Toolkit](https://docs.unity3d.com/6000.0/Documentation/Manual/UIElements.html), [Canvas](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Canvas.html): UI systems and inspection objects. Recheck page content and local versions before citing comparison-page capabilities; version paths alone do not establish every paragraph's applicability.

This round checked only documentation and links; it did not run Unity, Editor/Player or candidate examples. Validation records distinguish source/wiring checks, runtime results and human acceptance under [verification](../../shared/verification.md).
