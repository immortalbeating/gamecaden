# Unity 引擎 profile

## 触发与版本边界

实际项目运行根是 Unity，或当前新项目设计已明确选用 Unity 时使用，以 Unity 6（6000.0）官方文档作为本轮核对基线；现场 Editor 版本、Packages、渲染管线、目标平台和项目设置决定具体行为。只有设计选择、尚无工程时，用本页形成安排，运行事实保持未知。尚未选定 Unity 时只把它作为候选比较；本页不假设 Editor、CLI、MCP 或构建模块已经可用。Web Player 目标另叠加[Web 平台 profile](../platforms/web.md)，不加载 Phaser 规则。

## 需现场识别的工程事实

- 项目根、`ProjectSettings/ProjectVersion.txt`、`Packages/manifest.json`、有效 Scene/Build Profile、目标 Player 平台与是否有可用 Editor/构建模块。
- 命中对象是 Scene 实例、Prefab asset/实例、ScriptableObject asset、导入资源或运行时生成对象；引用由谁持有。
- Play Mode 的 Domain Reload/Scene Reload 设定、静态字段、事件订阅和场景切换路径。
- 本次是否涉及物理时钟、Update 顺序、存档、Web 导出或资产迁移；未涉及则不强加相应系统。

## 条件规则

规则性质沿用 [rules](../../shared/rules.md)。Unity 官方机制支持核对；具体目录和游戏架构按本项目设计选择。

| ID | 性质与触发 | 要求或默认做法 | 可观察验证 |
|---|---|---|---|
| UNITY-ROOT | 必要：识别或接入 Unity 项目 | 以实际项目设置、Packages 和 Scene/构建配置确认运行根与版本；`Assets` 存在或文档提 Unity 不足以证明。 | 可定位当前工程身份、目标场景和目标平台；未运行 Editor 时标明未验证。 |
| UNITY-META | 必要：导入、移动/改名原资源或创建资源副本 | 原资源移动/改名保持 `.meta` 配对及 GUID 身份。创建同项目中的新独立副本时通过编辑器/可靠流程生成新的身份，避免两个有效资源复用同一 GUID；工程迁移则保留原身份和引用关系。 | 导入后检查受影响 Scene/Prefab/资源引用，无 Missing、意外身份替换或重复 GUID；验证副本与原件按设计独立。 |
| UNITY-REFERENCE | 必要：场景/Prefab/组件接线 | 区分 Prefab asset、Scene 中实例与序列化引用；改动目标层级和覆盖范围应与消费者一致。 | 实际 Scene/Prefab 实例上的组件字段、事件与运行行为相符。 |
| UNITY-SHARED-DATA | 必要：ScriptableObject 被多个对象共享且可变 | 明确它是共享配置 asset 还是运行实例状态；避免把一份共享 asset 的可变值误当每个单位独立状态。 | 多实例互相影响、退出重进与重新进入 Play Mode 的结果符合设计。 |
| UNITY-PLAY-LIFE | 必要：静态状态、事件或初始化依赖 Play Mode/场景生命周期 | 根据现场 Domain Reload、Scene Reload 和生命周期设定安排初始化/解绑；不要以一次 Play 成功推断反复进入安全。 | 连续进入/退出 Play Mode、重载 Scene 后订阅和状态仍正确。 |
| UNITY-UPDATE | 必要：物理与逐帧逻辑交互或顺序敏感 | 依据实际 `Update`、`FixedUpdate` 等时序安排输入采样、物理操作与表现；需固定顺序时确认项目已有设置与依赖。 | 在本次相关帧率/固定步长下，规则与碰撞符合项目约定；不把所有物理模拟默认为逐位确定性。 |
| UNITY-PLAYER | 必要：承诺可交付 Player | 明确目标 Build Profile、场景列表、平台模块与构建配置；Editor Play 结果只证明 Editor 条件。 | 实际目标 Player 构建并启动，走本次用户路径；失败区分构建、启动与行为。 |
| UNITY-ASSET-HANDOFF | 必要：正式资产接入 | 追踪源文件、导入设置、`.meta` 身份、Prefab/Scene 消费者与当前候选；导入成功不等于已接线或已被接受。 | 在实际消费者中验证引用、显示/动作及必要运行条件。 |
| UNITY-STRUCTURE | 默认：新系统、对象复用或结构边界变化 | 命中 Scene/Prefab 组合、共享定义与实例状态、生命周期或 UI 系统时，按 [Unity 结构专题](../references/unity-structure.md) 读取相应章节；选择组件、Prefab、ScriptableObject 或普通 C# 类依项目需求。 | 能定位状态所有者、序列化接线与消费者；相关实例和进入/退出行为符合已有设计。 |

## 资源身份与结构

`.meta` 内的 GUID 承担 Unity 资产引用身份；同一资源改路径时保持身份，新独立资源需要独立身份。Prefab asset 与其实例、ScriptableObject asset 与运行状态各有不同作用范围，设计时应写明本次修改落在哪一层。目录与命名由项目现状和[项目结构](../project-structure.md)决定；共同原则见[profiles 总览](../README.md)和[共同边界](../common.md)，不为采用本 profile 迁移已有工程。

## 与 Skill 阶段交接

- `flow/init`：登记实际版本、运行根和有效项目规则；工具可用性现场确认。
- `brainstorm/design`：命中新系统、Scene/Prefab 组合、共享数据、生命周期或 UI 结构时读取 [Unity 结构专题](../references/unity-structure.md) 对应章节，在已有设计/Spec 写清所有者、消费者与可观察结果；时序或构建风险按对应规则处理。
- `develop/assets`：结构快改只读取 [Unity 结构专题](../references/unity-structure.md) 命中项，按已授权范围修改对应资产与引用；候选、接受、选用、接入按[资产交接](../../shared/asset-handoff.md)继续同一工作身份。
- `verify/close`：用[验证约定](../../shared/verification.md)区分 Editor、目标 Player、人工接受与发布；复用原 Task/Evidence/Decision 的适用结果。

## 官网依据与未验证范围

- Unity 6 官方：[Asset Metadata](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html)、[ScriptableObject](https://docs.unity3d.com/6000.0/Documentation/Manual/class-ScriptableObject.html)、[Event function execution order](https://docs.unity3d.com/6000.0/Documentation/Manual/execution-order.html)、[Domain Reloading](https://docs.unity3d.com/6000.0/Documentation/Manual/domain-reloading.html)、[Build Profiles](https://docs.unity3d.com/6000.0/Documentation/Manual/create-build-profile.html)。
- 本轮未接入或运行真实 Unity 工程、Editor、Player、CLI/MCP；具体项目的版本差异、安装状态及构建结果仍待现场核验。

