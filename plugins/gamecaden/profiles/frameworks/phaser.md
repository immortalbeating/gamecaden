# Phaser 框架 profile

## 触发与版本边界

实际游戏运行根加载 Phaser，或当前新项目设计已明确选用 Phaser 时使用。设计选择与实际安装事实分别表达。先确认项目实际安装/引用的精确版本与插件；本轮具体生命周期资料以 Phaser 3.x 官方文档核对。已有 Web 项目可能使用 4.x，不能把全部 Phaser 工程当成 3.x；2、4 或其他主版本的具体 API、生命周期和渲染行为须按安装版及其官方资料重核。浏览器目标同时读取[Web 平台 profile](../platforms/web.md)，但 Godot/Unity Web 导出不因此触发 Phaser。项目没有采用或选择 Phaser 时不套用本页。

## 需现场识别的工程事实

- Phaser 版本、启动配置、Scene 注册方式、全局与 Scene 级插件、实际运行入口。
- 命中变更的 Scene key、进入/停止/睡眠/唤醒关系，以及跨 Scene 状态由谁持有。
- 资产的 loader key、Texture Manager 条目、图集 frame 名、动画 key 与实际创建它们的消费者。
- 输入来自 Scene Input Plugin、全局 Game/DOM、UI 覆盖层或自定义总线；监听者由谁创建与释放。

## 条件规则

规则性质沿用 [rules](../../shared/rules.md)。下表中写出的 Scene 操作与清理机制是 3.x 核对基线；其他主版本先复核差异，再决定实现动作。个别项目的模拟/表现拆分、测试数量和资源尺寸保留原作用范围。

| ID | 性质与触发 | 要求或默认做法 | 可观察验证 |
|---|---|---|---|
| PHASER-ENTRY | 必要：识别 Phaser 根或改启动 | 用实际依赖、Game 配置与 Scene 注册确认运行根；同仓的 HTML 工具另识别。 | 从当前入口启动并进入目标 Scene，核对实际版本与资源请求。 |
| PHASER-SCENE-LIFE | 必要：Scene 切换、重进或销毁 | 明确使用版本的生命周期语义；3.x 中 `shutdown` 可再次启动、`destroy` 最终移除，`start/stop`、`sleep/wake`、`pause/resume` 决定状态保留或重置。 | 循环进入、离开、返回目标 Scene，状态及对象数量符合设计。 |
| PHASER-SUBSCRIBE | 必要：Scene 创建跨生命周期监听 | 区分 Scene 插件自身管理的监听与注册到 `game.events`、DOM、外部总线的监听；后者由创建者在合适生命周期解除，避免重复订阅。 | 重进 Scene 后一个事件只产生预期次数的效果；离场后无遗留回调。 |
| PHASER-STATE | 必要：多个 Scene 读写同一玩法状态 | 指定跨 Scene 状态所有者与重置时机；Registry、独立模型或其他既有模块均可，Scene 本地 Data 不自动成为全局真源。 | 切换、重启、刷新时每个消费者读到预期状态，无双写漂移。 |
| PHASER-KEYS | 必要：加载/替换贴图、图集或动画 | 保持 loader key、图集 frame、动画 key 与创建/播放消费者一致；全局缓存与 Texture Manager 的生命周期不同于单个 Scene 对象。 | 实际 Scene 的目标帧显示/播放正确；缺 key、错 frame 可定位。 |
| PHASER-COORD | 必要：碰撞、指针或视觉尺寸变化 | 以项目已定的坐标系、显示原点、相机与缩放规则连接逻辑目标和 Phaser 对象；浏览器尺寸/输入另按 Web profile。 | 目标分辨率下可见位置、交互命中和碰撞区域一致。 |
| PHASER-CLOCK | 默认：规则更新和表现时间互相影响 | 确认 `update(time, delta)`、Scene pause/sleep 及项目模拟时钟如何影响规则、动画和音效；仅在有风险时明确分工。 | 暂停、恢复、帧率变化或后台返回后结果符合规则。 |
| PHASER-ASSET-HANDOFF | 必要：正式资产接入 | 以当前候选、key/frame、实际 Scene 消费者和允许用途接线；图像加载成功只是接入链的一段。 | 在真实 Scene 的触发路径中观察展示、动画和相关输入/碰撞。 |

## 身份与目录机制

Phaser Scene 以 key 由 Scene Manager 寻址；纹理、缓存与动画管理器可跨 Scene 使用，Scene 对象和其插件则有各自生命周期。因此记录“谁持有 key/状态、谁创建监听、何时释放”，比规定 `src/scenes/` 等目录更重要。新系统或 Scene 组合、跨 Scene 状态、监听、UI/相机/DOM、资源消费者边界变化时读取 [Phaser 结构专题](../references/phaser-structure.md) 命中章节。具体结构沿用[项目结构](../project-structure.md)与项目有效约定；[共同边界](../common.md)负责通用责任，不在此重复。清理自己的外部监听时精确移除自己的回调，不无参清空共享 emitter。

## 与 Skill 阶段交接

- `flow/init`：确认依赖、运行根和项目生效规则；旧项目不因采用 profile 改造 Scene 架构。
- `design`：新系统、跨 Scene 状态、Scene 往返、UI/相机/DOM 或资源接线影响方案时读取 [Phaser 结构专题](../references/phaser-structure.md) 对应章节，明确所有者、key、重置与可观察路径。
- `develop/assets`：结构快改只读取 [Phaser 结构专题](../references/phaser-structure.md) 命中项，按实际 Scene 消费者接线；资产候选、接受、选用和接入见[资产交接](../../shared/asset-handoff.md)。
- `verify/close`：按[验证约定](../../shared/verification.md)复用原 Task/Evidence/Decision；仅补变更触及的 Scene 循环、资源或输入检查。

## 官网依据与未验证范围

- Phaser 官方：[Scenes](https://docs.phaser.io/phaser/concepts/scenes)（生命周期、Scene 与全局系统）、[Events](https://docs.phaser.io/phaser/concepts/events)（监听者所有权与精确移除）、[Data Manager](https://docs.phaser.io/phaser/concepts/data-manager)（Scene 与 Game 数据范围）。
- 既有项目曾在特定版本和调用路径发生 Text 首次渲染崩溃；类似经验只能作为调查线索，须在本项目复现，不能外推为所有主版本共有缺陷。
- 本页基于 Phaser 3.x 文档与既有 Web 工程经验；声明版本范围不等于已核对锁定安装版、插件或API行为；实际采用时须在本项目核验。目录和状态所有者是条件工作流判断，不是官方强制架构。

