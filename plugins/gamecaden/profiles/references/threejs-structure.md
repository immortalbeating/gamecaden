# Three.js 结构：渲染树、运行寿命与资源

## 何时读取

新系统、页面/关卡往返、状态/循环所有权、异步加载、实例复用或 DOM/3D UI 边界变化时读取命中章节；局部快改只读受影响项和验收。沿用 [Three.js profile](../frameworks/threejs.md) 的规则 ID，不增加同义 Gate。通用触发、采用边界与记录归属按[结构合同](structure-contract.md)：长期约定归原 Spec，本次方案归原 Task/design，运行事实归 Evidence，接受归 Decision。

## 真实类型与责任

Scene 是渲染场景，Object3D 提供层级和变换，Group 组合对象，Mesh 连接几何与材质；这些类型不自动提供游戏页面/关卡生命周期、权威玩法状态、物理或运行管理。渲染树不能代替业务寿命图。普通 JS/TS 模型、装配函数或现场框架组件可承担规则和页面协调，不固定文件数、目录和命名。官方依据：[Scene](https://threejs.org/docs/pages/Scene.html)、[Object3D](https://threejs.org/docs/pages/Object3D.html)、[Mesh](https://threejs.org/docs/pages/Mesh.html)。

| 必要结果与触发 | 工作流默认 / 允许替代 | 典型反例 | 可观察验收 |
|---|---|---|---|
| 页面进入、退出与跨页状态可定位 | 页面装配者创建场景对象、接模型与释放；跨页模型寿命按已有设计。单页局部状态可留当前模块，既有 ECS/组件也可承担同一责任。 | 把 Group 当关卡管理器；移除 Mesh 后认为分数自动重置；UI 自建另一份库存。 | 进入/离开/新局各状态符合保留和重置规则，写者及消费者一致。 |
| renderer/canvas、camera 与推进责任明确 | 默认一个宿主协调循环、活动页面和渲染；多视图/pass 或按需渲染允许明确分工。时钟按暂停、后台恢复及模拟需求选现场 API。 | 每次挂载新增 RAF；两个模块都更新同一模型；暂停只隐藏 Scene。 | 重挂载不增加推进次数，暂停/恢复不跳变，画布及相机正确。 |
| controls、监听和异步结果不会越过寿命 | 创建者解除自己的监听/controls；采用运行身份或有效性检查处理迟到结果，实际支持取消才用取消。 | 离场加载回来加到旧 Scene；撤销自己的监听时清空共享总线。 | 加载中离开再返回，旧结果不污染当前页，输入无重复。 |
| 内容来源到多实例消费者可追踪 | 代码工厂/实际资产导出与 URL 可定位；GLTFLoader 结果按需要实例化，骨骼模型按现场合适工具处理；可共享几何/材质/纹理，需独立修改时明确复制。 | 一个 Object3D 同时 add 到两个父节点；把 clone 当所有资源深复制；路径只在开发根可用。 | 部署路径能加载，两份实例变换/动画独立，共享修改符合约定。 |
| 卸载释放资源且不破坏存活消费者 | 资源所有者在最后使用结束后按现场 API dispose；对象移出树与资源释放分别处理，可用现有缓存/引用策略。 | scene.remove 后宣称 GPU 已释放；遍历页面直接 dispose 仍被另一页使用的纹理。 | 往返后资源趋势符合缓存策略，另一消费者仍正确呈现；不要求所有计数归零。 |
| 屏幕尺寸、UI 与输入映射一致 | 明确 canvas CSS/缓冲尺寸、相机投影和 picking 换算；DOM UI、3D UI 或现场组件方案按寿命/可访问性需求选。 | canvas 放大但相机投影未更新；DOM 按钮同时触发 raycast 和 controls。 | 调整目标尺寸、开关 UI、切换焦点时显示和命中正确。 |

循环/尺寸事实见 [WebGLRenderer](https://threejs.org/docs/pages/WebGLRenderer.html)；controls 及其更新条件见 [OrbitControls](https://threejs.org/docs/pages/OrbitControls.html)。API 不能从当前网页直接推定现场版本。需要的时间 API 以安装版为准，不强制旧 Clock 或新 Timer。

### 资源与框架条件

[GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html)是显式导入的 addon；命中压缩/扩展时核对对应 decoder、路径和运行能力，不为每项资产加载全套工具。几何、材质和纹理各有释放机制：[BufferGeometry](https://threejs.org/docs/pages/BufferGeometry.html)、[Material](https://threejs.org/docs/pages/Material.html)、[Texture](https://threejs.org/docs/pages/Texture.html)。当前 Object3D 文档也有自身 dispose，不能假定所有旧版都有同一接口；即使对象支持 dispose，共享几何/材质/纹理仍需分别按所有权处理。GLTFLoader 使用的 image bitmap 另需核对处理方式。

React/R3F 若已选用，先读取实际集成版本的挂载、帧循环、缓存和自动/手动资源处置策略；本页 imperative 默认不能直接套为所有 renderer 框架的统一清理做法。实际浏览器按 [Web](../platforms/web.md)，其它明确目标查真实运行环境、renderer/适配和对应官方资料，按本次实际条件形成安排。

## 候选例子

以下仅为设计示意，未运行。

**简单单页：点击旋转方块。** 一个宿主拥有 renderer/canvas、camera、循环与 Mesh；本地角度可留页面模块，指针经当前 canvas 坐标做 picking。退出撤销输入和循环，最后消费者结束后释放自有资源。验收点击次数、尺寸变化及卸载/重挂载；不为单页先建全局服务。

**跨页面：选角→玩法→结果→新局。** 会话模型保留选角及本局结果；宿主协调活动页面，页面装配者持有渲染树和输入。资产缓存共享几何/纹理，角色实例拥有独立变换与动画状态；加载迟到时检查当前运行身份。退出玩法移除对象并释放实例专属资源，共享资产按消费者寿命处理。验收两轮往返、加载中切页、暂停返回、两份角色不串状态及 UI/controls 输入。

## 核对与验证边界

2026-10-01 核对以上官方资料；当前官网为变化中的参考，实施前查 package/lock/现场版及相应源码/文档。表中的组织、有效运行身份和缓存策略是工作流默认/候选，非引擎强制业务架构。本轮只核对文档与链接，未运行真实项目或例子、核对现场依赖/框架及目标设备。验证按[verification](../../shared/verification.md)记录实际范围，静态检查不等于运行或人工接受。
