# Unity 结构：对象职责、状态与 UI

## 何时读取

新建 Unity 系统、改变 Scene/Prefab 组合、共享定义与实例状态、跨场景生命周期，或选择/调整 uGUI、UI Toolkit 接线时，读取命中的章节。快改仅加载受影响项及其验收。版本、资源身份和交付仍由 [Unity profile](../engines/unity.md) 决定；本页承接 UNITY-STRUCTURE、UNITY-REFERENCE、UNITY-SHARED-DATA、UNITY-PLAY-LIFE，不增加另一组 Gate。

通用触发、既有设计/Spec 的记录归属、新旧项目采用边界与设计/运行验收按 [结构合同](structure-contract.md)。本页只补充命中的引擎机制和候选方案。

## 引擎事实与工作流选择

本页机制参考 Unity 6（6000.0），现场 Editor、Packages、Play Mode 设置和已选 UI 系统优先。官方事实：Scene 保存场景内容；GameObject 通过组件提供行为，MonoBehaviour 接收引擎回调；Prefab 是可复用对象配置，其实例可有覆盖；普通 C# 对象没有自动的 MonoBehaviour 回调。ScriptableObject asset 可共享定义，但不能据此把运行存档当成 asset 写入。默认职责安排是本工作流方案，Unity 未强制某种游戏架构。

| 必要结果与触发 | 本工作流默认 / 允许替代 | 常见反例 | 可观察验收 |
|---|---|---|---|
| 新对象或复用单位能确定入口、行为与实例差异 | Scene 组合关卡/运行范围；Prefab 表达重复实体或 UI 单位；组件连接引擎生命周期、输入、物理和表现；独立规则/数据可用普通 C# 类。简单行为可留在一个组件，已有有效组合继续用。 | 为每个类建立 GameObject；把所有规则与所有实体状态堆进 Scene 管理器；只复制实例而不检查覆盖。 | 从 Scene/Prefab 定位入口和必要组件，创建两个实例能独立运行；修改定义与实例覆盖的影响范围符合设计。 |
| 多实例共享定义时，定义和可变运行状态有明确归属 | ScriptableObject 或序列化配置承担定义；每个实例/本局模型持有生命值等可变状态。允许有意共享运行状态或运行时 ScriptableObject 实例，但标清创建、所有者、重置与释放。 | 多个单位直接修改同一配置 asset 的生命值；把静态字段或 Inspector 默认值当自动新局重置。 | 两个消费者共享参数而实例状态独立；新局/重进恢复设计值；有意共享变化只影响指定消费者。 |
| 生命周期或跨 Scene 变化时，状态寿命与订阅寿命相符 | 区分对象启停、Scene 装卸、本局、应用及存档寿命；创建者配对初始化和清理。Awake/OnEnable/Start/OnDisable/OnDestroy 按实际用途选择，跨对象顺序依赖显式协调。 | 用 Start 假设所有依赖已按某种顺序完成；OnEnable 每次订阅而只在最终销毁解绑；持久对象引用已卸载 Scene 组件。 | 启停、Scene 往返和重复 Play 后仅有预期实例/订阅；新局重置与存档恢复分别正确。 |
| 场景/Prefab 接线可编辑且可检查 | 固定本地引用优先使用可序列化字段与 Inspector 接线；动态生成、依赖注入、运行查询也可，只要能检查失败与来源。普通类序列化按 Unity 支持的字段规则处理，按共享身份需要选择内联值或 SerializeReference。 | 认为任意属性、字典、普通类引用都会照常序列化；全局名称搜索隐藏依赖；只看 Prefab asset 未看实例覆盖。 | 检查实际 Scene/Prefab 字段、覆盖、UnityEvent 或运行绑定来源；缺引用有可定位反馈；保存/重载后接线与数据保持。 |
| UI 结构或系统选择影响交付时，布局、输入与状态有确定边界 | 先识别已有 UI 系统；uGUI 使用 Canvas/GameObject、RectTransform 与适合目标的布局组件；UI Toolkit 使用 UIDocument、VisualElement 树、UXML/USS 与其布局/事件。按现场功能选择，可混用但写清层级、焦点/输入与状态接口。 | 把 VisualElement 当 Scene 中可挂 MonoBehaviour 的 GameObject；把普通 Transform 父子层级当 UI 自动布局；按钮与玩法模型各存一份可写状态。 | 在实际系统中定位布局源、绑定与回调；目标尺寸、显示切换、焦点/输入和数据更新符合已定行为；重建 UI 后回调不重复。 |

### 持久范围的选择

跨 Scene 状态先问它需要跨一次切换、整局还是应用。默认将权威状态放在能覆盖该寿命的既有模型/所有者，Scene 组件只是消费者。允许 `DontDestroyOnLoad` 根对象、常驻/加法加载 Scene 或已有应用层；这些都是手段，须检查重复创建、引用失效和新局重置。`DontDestroyOnLoad` 会保留目标根对象及其子对象，不能只凭一个调用证明状态合同正确。静态字段还受 Domain Reload 设置影响，场景卸载也不等同于清空所有静态/外部订阅。

### 序列化引用范围

普通托管对象的 `SerializeReference` 身份与图关系保存在同一序列化宿主范围内，不保证跨两个 MonoBehaviour/其他 UnityEngine.Object 宿主保持同一实例。跨宿主需要持久共享身份时，核对合适的 UnityEngine.Object/ScriptableObject 引用或项目自己的运行模型；运行时已经传入同一对象与保存后重载仍是同一对象，分别验证。[SerializeReference](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SerializeReference.html)。

### UI 系统的版本判断

uGUI 与 UI Toolkit 的功能和支持随版本变化；选型依据本次需要的世界空间/屏幕 UI、渲染、输入、动画、绑定及目标平台功能，查现场版本与 package 文档。官方比较页提供能力比较，不把其推荐升级成所有项目强制迁移。UI Toolkit 的视觉树可在 UI Builder/Debugger 等对应工具检查，uGUI 在 Hierarchy/Inspector 检查；使用哪种工具由现场条件决定，未打开编辑器不得写成已检查。

## 候选例子

以下是本方案的说明性候选，未运行，也不是官方标准模板。

**简单场景：一个可拾取物。** 已有设计规定拾取一次增加分数。Scene 放玩家与拾取物；可重复拾取物用 Prefab，其组件处理接触与显示，引用只读奖励定义；本局分数由当前局所有者持有。若只有一个简单场景，分数可以由一个清楚的 Scene 组件管理，无需先建服务层。验收沿真实输入触发一次拾取、重复触发和重开关卡，核对奖励次数、实例消失和分数重置。

**跨场景：关卡结束进入结果页再开新局。** 已有 Spec 规定结果页保留本局得分，新局清零。采用 `关卡组件 → 本局模型 ← 结果页 UI`；模型由覆盖这次切换的所有者持有，关卡组件和 UI 分别按进入/离开绑定解绑。实现可用持久根或常驻 Scene；结果页选择现有 uGUI 或 UITK，其回调只发送“新局”意图。验收两次关卡→结果→新局，观察模型、持久所有者数量、分数与回调次数；同时检查重复进入 Play 的现场设置。

## 官方事实来源与验证边界

- [Scenes](https://docs.unity3d.com/6000.0/Documentation/Manual/CreatingScenes.html)、[GameObjects](https://docs.unity3d.com/6000.0/Documentation/Manual/class-GameObject.html)、[Prefabs](https://docs.unity3d.com/6000.0/Documentation/Manual/Prefabs.html)：组合、组件与复用机制。
- [ScriptableObject](https://docs.unity3d.com/6000.0/Documentation/Manual/class-ScriptableObject.html)、[Serialization rules](https://docs.unity3d.com/6000.0/Documentation/Manual/script-serialization-rules.html)：asset/普通对象与序列化边界。
- [Execution order](https://docs.unity3d.com/6000.0/Documentation/Manual/execution-order.html)、[Domain Reloading](https://docs.unity3d.com/6000.0/Documentation/Manual/domain-reloading.html)、[DontDestroyOnLoad](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Object.DontDestroyOnLoad.html)：回调、Play Mode 与持久范围。
- [UI comparison](https://docs.unity3d.com/6000.0/Documentation/Manual/UI-system-compare.html)、[UI Toolkit](https://docs.unity3d.com/6000.0/Documentation/Manual/UIElements.html)、[Canvas](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Canvas.html)：UI 系统及检查对象。引用比较页的能力前复核页面内容与现场版本；版本路径不能单独证明所有段落适用。

本轮只核对文档与链接；没有运行 Unity、Editor/Player 或候选例子。验证记录按 [verification](../../shared/verification.md) 区分源码/接线检查、运行结果及人工接受。


