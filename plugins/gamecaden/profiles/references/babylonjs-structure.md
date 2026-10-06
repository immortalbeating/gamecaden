# Babylon.js 结构：Scene、页面、实例与资源

## 何时读取

新系统、页面/Scene 往返、跨页状态、循环/observable、资产实例复用、GUI/DOM 或物理边界变化时读取命中章节。快改只读受影响项及验收，沿用 [Babylon.js profile](../frameworks/babylonjs.md) 的规则 ID，不新增同义 Gate。通用采用、设计/运行边界与 Task/Spec/Evidence/Decision 归属按[结构合同](structure-contract.md)。

## 真实类型与责任

Engine 管理渲染基础与循环；Scene 是引擎对象、摄像机、渲染等运行范围；TransformNode 提供变换层级，Mesh 承担几何表现。应用页面的进入/退出与 Scene 创建/释放可相同，也可不同，必须按项目关系明确。普通 TS 模型、自定义组件不会仅因命名自动获得引擎生命周期；AssetContainer 是资产容器，不等同 Unity Prefab 的编辑/行为合同。官方 API：[Engine](https://doc.babylonjs.com/typedoc/classes/BABYLON.Engine)、[Scene](https://doc.babylonjs.com/typedoc/classes/BABYLON.Scene)、[TransformNode](https://doc.babylonjs.com/typedoc/classes/BABYLON.TransformNode)。

| 必要结果与触发 | 工作流默认 / 允许替代 | 典型反例 | 可观察验收 |
|---|---|---|---|
| 页面、Scene、状态寿命能对应 | 装配者协调页面/Scene 与普通模型，跨页状态由既有会话模型持有；单页可局部持有，现有组件/ECS 可替代。 | 结果页重建 Scene 时丢本局分数；把每个规则对象都变成 Scene。 | 页面往返、新局时状态及 Scene 数量符合设计，消费者可定位。 |
| Engine、canvas、camera、循环与 resize 有归属 | 默认宿主拥有 Engine 与循环，活动 Scene 由协调者渲染；允许多 Scene/多相机但明确各自推进责任。 | 每次进入 runRenderLoop 注册另一回调；卸载一页 dispose 共享 Engine。 | 重挂载无重复更新，退出不再 render 已释放 Scene，尺寸/相机正确。 |
| observable、输入和迟到加载安全退出 | 创建者保存 observer/回调引用并精确解除；外部 DOM/总线独立清理，异步结果检查有效 Scene/运行身份。 | 以 scene.dispose 推断所有 DOM 监听都移除；旧 Promise 回来绑定新页面。 | 加载中离开、返回后事件次数正确，旧回调不写当前模型。 |
| 来源、容器与实例消费者清晰 | 查实际资产 URL/导出及 loader；AssetContainer 可加载后实例化，明确返回的 roots/skeletons/animationGroups、共享或克隆材质。也可用现有工厂/直接导入。 | 所有角色共享本应独立的动画状态；容器模板与实例一并无差别释放。 | 两份实例变换/动画独立，修改共享材质符合意图，实际入口资源完整。 |
| 释放契约保持共享消费者 | 按现场 Mesh/节点 dispose 的递归、材质/纹理选项和容器/Scene/Engine 所有权清理；缓存允许明确保留。 | 把 dispose 当 Three.js remove；强制 disposeMaterialAndTextures 破坏别的 Mesh；认为单 Mesh 默认释放所有共享纹理。 | 实例退出、Scene 替换后资源不无意累积，仍活跃消费者正常。 |
| 坐标、物理和 UI 输入一致 | 核对 Scene handedness、导入转换、camera/picking、物理插件坐标/版本；GUI 或 DOM 按内容/寿命选择，明确 attach/detach 输入与焦点。 | 只翻转模型显示而未核对碰撞；DOM 按钮和 camera 同时消费拖动；凭库名声称目标渲染或平台能力。 | 目标尺寸下显示/命中/碰撞一致，UI、camera、玩法只执行预期意图，目标能力实测。 |

### 循环、订阅与资源机制

`runRenderLoop`、`stopRenderLoop` 与 `resize` 按现场 Engine API 使用，记录自己注册的回调，避免解除不属于本页的循环。Scene observable 的 token/回调与外部监听各按实际注册方式清理；官方 [Observables](https://github.com/BabylonJS/Documentation/blob/master/content/features/featuresDeepDive/events/observables.md)展示保存 observer 并 remove 的用法。页面退出是否释放 Scene/Engine 是所有权选择，不是所有页面统一销毁。

官方 [AssetContainer 文档](https://github.com/BabylonJS/Documentation/blob/master/content/features/featuresDeepDive/importers/assetContainers.md)说明 `instantiateModelsToScene`、实例结果及其 dispose；[容器源码](https://github.com/BabylonJS/Babylon.js/blob/master/packages/dev/core/src/assetContainer.ts)可核对现场对应版的复制/共享选项。Mesh 的 dispose 选项见 [AbstractMesh API](https://doc.babylonjs.com/typedoc/classes/BABYLON.AbstractMesh)，不要把节点删除、实例释放、容器释放和 Scene 卸载合成一个无条件步骤。共享 material/texture、动画与骨骼的具体寿命须查所用方法/选项和消费者。

AssetContainer 与所加载/创建的 Scene 关联，资产即使暂未加入活动列表也仍属于该运行关系；不能把它当不依赖 Scene 的全局模板。在同一保留 Scene 中切页面，可按设计复用该容器；若 Scene 实际释放后创建另一 Scene，默认为新 Scene 重新加载/建立容器。确需迁移时核对现场 API 与对象依赖，下载源/字节缓存与 Scene 内模型模板分别记录，不能凭 JS 还保留变量就认定旧资产可跨新 Scene 使用。

handedness 按现场 Scene 配置与 importer 行为核对，不把默认值当所有工程事实。物理 SDK/插件、loader 注册/扩展、GUI、WebGPU 只在当前请求命中时查安装版资料与能力。实际浏览器叠加 [Web](../platforms/web.md)，其它明确目标查真实 Engine、运行环境、适配与对应官方资料。本页不固定业务架构、文件数或命名。

## 候选例子

以下仅为设计示意，未运行。

**简单单页：点击球体计分。** 一个宿主拥有 Engine/canvas 与循环，一个 Scene 创建 camera、球体和输入，本局计分可留页面模块。退出移除自己的 observer/DOM 监听，按实际所有权释放 Scene 与 Engine。验收点击一次、重进及尺寸变化，不先引入全局服务。

**跨页/重进：选角→战斗→结算→新局。** 会话模型保留角色选择和本局结果，宿主复用 Engine 并协调当前 Scene。每个战斗 Scene 建立自己的 AssetContainer 模板，装配者持有本次实例根、骨骼/动画组与订阅；同 Scene 中材料共享或克隆按编辑需求选。退出撤销本次输入/observer，按所有权释放本次实例、容器及 Scene，迟到加载不写旧运行；新战斗在新 Scene 中建立对应对象，可复用已定义的源数据/下载缓存。若改为保留同一 Scene 切换页面，另明确模板与活动实例寿命。验收两轮往返、加载中切页、共享材质与独立动画、暂停/GUI 输入以及新局重置。

## 核对与验证边界

2026-10-01 核对官方文档仓库与 API 入口；Context7 首次结果混入 Babylon Lite，未采用其 API。当前官网/master 不能单凭 URL 证明现场兼容，先查 package、lockfile/安装版及对应源码。业务模型、宿主和缓存是工作流默认/候选。本轮未安装/启动引擎、真实项目、物理/loader 插件或验证 browser/WebGL/WebGPU 能力。验证沿用[verification](../../shared/verification.md)，静态结果与运行/人工接受分别记录。
