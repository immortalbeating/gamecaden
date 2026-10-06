# Babylon.js 框架 profile

## 触发与现场边界

实际运行根使用 Babylon.js，或当前设计已明确选用时读取。查 package、lockfile/安装版、模块/全局构建、Engine 类型、入口及已用扩展；设计选择不等于安装事实。本页针对通常的 Babylon.js Engine/Scene，不能把 Babylon Lite API 混入。实际浏览器叠加 [Web](../platforms/web.md)，其它明确目标按真实 Engine、运行环境、适配和官方资料核对，库名不证明目标支持。

定位 Engine/canvas、Scene、camera、循环、页面卸载者、状态、observable/DOM 监听、资产容器与实例消费者。SDK、loader 注册、physics 插件、GUI 或 WebGPU 的具体资料只在当前请求命中时读取。结构变化按需读 [Babylon.js 结构专题](../references/babylonjs-structure.md)，快改只读受影响项。

## 条件规则

性质按 [rules](../../shared/rules.md)。必要项约束结果；默认项允许现有等效方案。

| ID | 性质与触发 | 要求或默认做法 | 可观察验证 |
|---|---|---|---|
| BABYLON-ENTRY | 必要：识别根或改平台 | 核对实际 Engine、画面输出入口、版本、模块与目标宿主能力；浏览器目标再查 canvas/WebGL/WebGPU，原生等目标查自己的 Engine/输出适配。 | 当前入口在目标宿主呈现，能力/失败路径符合约定。 |
| BABYLON-LIFE | 必要：页面/Scene 切换或共享状态 | 区分应用页面与引擎 Scene 的寿命；Engine、Scene、TransformNode/Mesh、普通模型各有明确所有者与重置边界。 | 页面往返与新局的 Scene/模型数量和状态符合设计。 |
| BABYLON-LOOP | 必要：挂载、更新、暂停或尺寸变化 | 明确 runRenderLoop 回调与 scene.render 的责任，退出使用现场 stopRenderLoop/释放方案，resize 与时钟策略有归属。 | 重挂载无重复推进，暂停/后台恢复与尺寸变化正常。 |
| BABYLON-SUBSCRIBE | 必要：observable、外部监听或异步变化 | 保存并解除自己的 observer/回调、DOM 监听与相机输入；异步返回检查目标 Scene/运行仍有效。 | 离场无旧回调，返回一次输入只生效预期次数。 |
| BABYLON-ASSET | 必要：导入/实例化正式资产 | 按现场 loader/注册与 URL 加载；明确 AssetContainer、实例根/骨骼/动画组及 material/texture 共享或克隆策略。 | 实际消费者显示/播放正确，多实例状态独立且共享策略生效。 |
| BABYLON-DISPOSE | 必要：卸载 Scene/实例或替换资源 | 核对对象 dispose 选项、递归与共享 material/texture 的消费者；容器、实例、Scene、Engine 分别按所有权释放。 | 退出/重进无累积，保留消费者仍有效，未误销毁共享 Engine。 |
| BABYLON-COORD-INPUT | 必要：模型、物理、GUI/DOM 或输入变化 | 明确 handedness、相机/picking、输入消费与屏幕尺寸；物理按现场版本/插件核对，GUI/DOM 与相机控制分工。 | 可见位置、交互/碰撞和目标尺寸一致，UI 不重复触发玩法。 |
| BABYLON-MODEL | 默认：跨 Scene 规则或复用行为 | 普通 TS 模型/组件与装配者承担规则和寿命；可用有效现有组织，组件不会仅因命名自动获得 Scene 生命周期。 | 状态真源、依赖接口和释放入口可定位。 |

## 阶段交接与来源

`flow/init` 确认现场；`design` 在原 Task/design 或 Spec 记录命中关系；`develop/assets` 按实际实例接线并沿用[资产交接](../../shared/asset-handoff.md)；`verify/close` 按[验证约定](../../shared/verification.md)复用原 Evidence/Decision，只补本次影响。

2026-10-01 资料核对：官方 [Engine](https://doc.babylonjs.com/typedoc/classes/BABYLON.Engine)、[Scene](https://doc.babylonjs.com/typedoc/classes/BABYLON.Scene)、[TransformNode](https://doc.babylonjs.com/typedoc/classes/BABYLON.TransformNode)、[AbstractMesh](https://doc.babylonjs.com/typedoc/classes/BABYLON.AbstractMesh) API；官方文档仓库的 [AssetContainer](https://github.com/BabylonJS/Documentation/blob/master/content/features/featuresDeepDive/importers/assetContainers.md)与 [Observables](https://github.com/BabylonJS/Documentation/blob/master/content/features/featuresDeepDive/events/observables.md)。当前官网/master 非现场兼容证明，API 采用前核对锁定版；组织默认是工作流选择。本轮未安装/启动引擎、真实项目或插件，也未测试目标浏览器能力。
