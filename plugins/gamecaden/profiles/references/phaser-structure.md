# Phaser 结构：Scene、模块、状态与 UI

## 何时读取

新建 Phaser 系统、调整 Scene 组合/往返、状态持有、外部监听、UI/摄像机/DOM 边界或资源 key 消费者时，读取命中的章节。快改只加载受影响项及验收。沿用 [Phaser profile](../frameworks/phaser.md) 的 PHASER-SCENE-LIFE、PHASER-SUBSCRIBE、PHASER-STATE、PHASER-KEYS、PHASER-COORD；本页不增加同义 Gate。

通用触发、既有设计/Spec 的记录归属、新旧项目采用边界与设计/运行验收按 [结构合同](structure-contract.md)。本页只补充命中的引擎机制和候选方案。

## 引擎事实与工作流选择

机制以已核对的 Phaser 3.x（Context7 可用 3.90.0）为参考。先读实际 package、lockfile/安装版、插件与入口；4.x 或其他主版本须按锁定/现场版核对，再采用具体 API，声明范围不能替代安装事实。官方事实：Scene 是引擎运行范围，具备本地系统与生命周期；Game 有全局系统；普通 JS/TS 对象、类与模块可承载游戏规则，但不会自动获得 Scene 生命周期。下面默认方案属于本工作流，Phaser 未规定所有游戏的业务分层。

| 必要结果与触发 | 本工作流默认 / 允许替代 | 常见反例 | 可观察验收 |
|---|---|---|---|
| 新系统能明确进入、更新、离开和复用范围 | Scene 负责该运行范围的引擎接线、创建及协调；普通对象/类模块承载规则、数据或可复用行为。简单规则可留 Scene；独立模块有显式初始化/更新/释放接口。 | 把每个规则类都做成 Scene；所有业务状态放一个巨型 Scene；普通对象假定会随 Scene 自动清理。 | 能从 Scene 定位消费者和模块入口；独立单位可被创建/退出；变更只需触及相应责任。 |
| 跨 Scene 状态有一个权威来源 | 按局/应用/存档寿命选既有模型、Game Registry 或明确全局模块；Scene Data 用于 Scene 范围数据。允许有意共享或快照传入，但标清写者、重置与同步。 | HUD 与玩法 Scene 各自维护分数；认为 Scene Data 自动全局共享；认为 stop 后所有 JS 字段都恢复初值。 | Scene 往返、restart、新局及刷新后的值分别符合设计；所有消费者观察同一变化。 |
| Scene 重进或外部监听变化时能重复进入安全 | 区分 Scene 本地插件清理与 game.events、DOM、外部总线、原生计时器/异步回调；创建者在合适 shutdown/destroy 或自定义释放边界解除自己的回调，异步结果检查所属运行是否仍有效。 | 每次 create 增加外部监听，只在最终 destroy 清理；无参清空共享 emitter；离场 Promise 回来写入旧 UI。 | 进入→离开→返回，按风险继续必要重复；事件只触发预期次数，离场无旧对象回调，订阅/对象不累积。 |
| UI 或多 Scene 同时运行时，坐标、输入与暂停范围清楚 | 可用同 Scene 固定 UI、并行 UI Scene、独立摄像机或 DOM；按玩法/UI 生命周期和已定布局选最小方案。并行 Scene 明确叠放与输入归属，摄像机明确渲染对象和坐标转换，DOM 明确宿主/配置与焦点。 | 暂停玩法 Scene 后希望同 Scene UI 继续更新；多个 Scene 都响应同一意图；相机移动使 HUD 漂移；DOM 覆盖后画布仍误响应。 | 移动/缩放相机、暂停/恢复、尺寸变化和 UI 开关时，显示、命中、焦点与暂停范围符合设计。 |
| 层级或布局变化时，视觉变换与布局规则可区分 | Container 用于子对象组合变换；布局由明确计算、项目布局工具或合适 DOM/CSS 承担。允许直接定位少量固定控件。 | 把 Container 当 Godot Control 自动布局；加子对象就期待自动锚定/响应式；容器视觉位置与物理/输入坐标未经核对。 | 改容器变换及目标尺寸后检查子对象位置、命中/碰撞与布局；重新布局的触发与来源可定位。 |
| 资源替换或重进时 key 到消费者的链稳定 | 查 loader key、Texture/cache、atlas frame、Animation key 与实际创建/播放点；全局资源可复用，Scene 对象重建时重新接线。替换/删除共享条目前定位活跃消费者。 | 每次 create 重复建同名全局动画；同 key 覆盖别的 Scene 正在使用的纹理；只检查请求成功。 | 从目标入口和重进路径显示/播放正确 frame；共享消费者仍有效，无重复定义或缺 key 错误。 |

### Scene 生命周期与系统范围

3.x 中 Scene 的 start/stop、pause/resume、sleep/wake 和 remove/destroy 语义不同：shutdown 后可再次启动，destroy 是最终移除；暂停/睡眠也不能当成统一重置。具体组合先查现场版本。Game 的 Texture、Cache、Animation、Registry 等与 Scene 的显示列表、相机、输入、时钟等寿命不同；把对象从 Scene 移除不能证明全局资源或外部订阅已释放。每次进入需要重新绑定的对象和每局初始化的状态应显式处理，Scene 实例上的普通字段尤其不能依赖构造函数重新执行。

### UI 方案的约束

同 Scene 少量固定 HUD 可使用适当 scroll factor/相机安排，但需核对缩放和输入坐标。并行 UI Scene 可与玩法有不同暂停寿命；两者通过既有模型/消息接口交换意图和显示数据。多摄像机需明确哪些对象被哪台相机显示或忽略，以及指针采用哪台相机。DOM 方案先核对游戏 DOM 容器配置、CSS、焦点、缩放和官方限制；3.x 官方 DOM Element 说明要求所在 Scene 使用单相机，并指出跨 Scene 元素进入同一 DOM 容器；多相机需求可考虑并行 Scene，仍需核对现场版。Container 的层级变换不提供 Godot 式自动布局合同，布局来源必须在代码或所选工具中可定位。

## 候选例子

以下仅为本方案示意，未运行，不是官方标准模板。

**简单场景：点击目标增加分数。** 已有设计只有一局单屏玩法。一个 Scene 创建目标与固定计分文字，Scene 本地状态可承担本局分数；纯计分规则需要复用时再用普通模块。目标纹理 key 由 preload 到 create 的消费者链核对。验收真实点击一次、连续点击与 restart，观察计分次数、资源帧及重置；不为这项需求先建全局服务。

**跨场景：玩法、暂停 UI 与结果页。** 已有 Spec 规定暂停时 UI 可操作，结果页保留本局分数。采用 `玩法 Scene → 本局模型 ← 并行 UI Scene / 结果 Scene`；本局模型寿命覆盖结果页，UI 发暂停/继续意图，由协调者执行对应 Scene 操作。UI 本次退出清理自己的模型/DOM/全局监听，新局显式重置模型，重进玩法重建对象并复用已验证资源 keys。验收玩法→暂停→继续→结果→新局两轮，同时检查相机/指针、事件次数与共享动画/纹理消费者。

## 官方事实来源与验证边界

- [Scenes](https://docs.phaser.io/phaser/concepts/scenes)、[Scene events](https://docs.phaser.io/api-documentation/namespace/scenes-events)：Scene 与 Game 系统、并行运行及生命周期。
- [Data Manager](https://docs.phaser.io/phaser/concepts/data-manager)、[Events](https://docs.phaser.io/phaser/concepts/events)：数据范围、订阅与精确移除。
- [Container](https://docs.phaser.io/phaser/concepts/gameobjects/container)、[Cameras](https://docs.phaser.io/phaser/concepts/cameras)、[DOM Element](https://docs.phaser.io/phaser/concepts/gameobjects/dom-element)：组合变换、摄像机和 DOM 条件/限制。
- [Textures](https://docs.phaser.io/phaser/concepts/textures)、[Animations](https://docs.phaser.io/phaser/concepts/animations)：全局资源与 key 消费机制。官方概念站可能更新；API 采用前与现场主版本及锁定版核对。

本轮只核对文档与链接；没有启动 Phaser/浏览器游戏、核对任何真实工程锁定版或运行示例。验证记录沿用 [verification](../../shared/verification.md)，源码检查与实际运行/人工接受分别记录。


