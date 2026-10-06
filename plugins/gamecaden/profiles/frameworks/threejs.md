# Three.js 框架 profile

## 触发与现场边界

实际运行根使用 Three.js，或当前设计已明确选用时读取。先查 package、lockfile/安装版、入口、renderer 与 addons；设计选择不等于已安装。实际浏览器目标叠加 [Web](../platforms/web.md)，其它明确目标按真实运行环境、适配和官方资料核对，库名不证明目标支持。React / React Three Fiber（R3F）仅在现场采用时读取实际集成版本及其生命周期、资源策略，不默认引入。

需定位 renderer/canvas、camera、推进与渲染入口、页面装配/卸载者、业务状态、controls、加载器与 URL、共享资源消费者，以及 DOM/3D 输入边界。新系统、切页/重进或这些责任变化时按需读 [Three.js 结构专题](../references/threejs-structure.md)；快改只读命中项。

## 条件规则

性质按 [rules](../../shared/rules.md)。必要项约束结果；默认项可由满足同一结果的现有方案替代。

| ID | 性质与触发 | 要求或默认做法 | 可观察验证 |
|---|---|---|---|
| THREE-ENTRY | 必要：识别运行根或改宿主 | 确认版本、renderer/canvas、camera、实际入口和目标渲染能力；addons 与核心版本/导入方式按现场核对。 | 当前入口使用预期画布/相机，目标宿主能实际呈现。 |
| THREE-OWNER | 必要：新增页面/关卡或共享状态 | Scene/Object3D/Group 是渲染及变换树；指定页面生命周期、业务状态与物理/运行管理责任。 | 进入、离开、新局时预期状态保留/重置，消费者可定位。 |
| THREE-LOOP | 必要：推进、挂载或暂停变化 | 同一责任不得重复推进/渲染；明确时钟、暂停/恢复、挂载与撤销循环。多 pass/多视图允许由明确协调者安排。 | 重挂载、后台返回、暂停后更新次数和时间行为符合设计。 |
| THREE-ASYNC | 必要：异步加载或跨生命周期监听 | 离场撤销自己的外部监听/controls；异步结果按有效运行身份接纳或释放，取消能力以实际 loader 为准。 | 离场后加载返回不写旧页面，重进无重复事件。 |
| THREE-ASSET | 必要：加载/复用正式资源 | URL、部署基址、GLTFLoader 及命中扩展的 decoder 到真实消费者接通；实例状态与共享几何/材质/纹理分清。 | 真实入口显示/播放目标资产，多实例不串状态，共享消费者仍有效。 |
| THREE-DISPOSE | 必要：替换/卸载 GPU 资源 | 移出 Scene 不等于释放；按现场 API 显式释放不再使用的 geometry/material/texture 等资源，先查其他消费者及所有者。 | 往返后对象/资源使用趋势符合保留策略，存活消费者未被误释放。 |
| THREE-INPUT-SIZE | 必要：UI、相机、尺寸或输入变化 | 对齐 CSS 尺寸、绘制缓冲、相机投影和指针换算；明确 controls、3D picking、DOM 焦点与事件消费。 | 目标尺寸下显示与命中一致，UI 操作不意外驱动相机/玩法。 |
| THREE-MODEL | 默认：规则与显示开始互相牵制 | 普通 JS/TS 模型承载可复用规则，装配者连接渲染对象；简单局部规则可留当前模块，沿用有效现有架构。 | 模型所有者、显示消费者和释放入口可直接定位。 |

## 阶段交接与来源

`flow/init` 识别现场；`design` 在原 Task/design 或 Spec 写命中的所有者、寿命与方案；`develop/assets` 按消费者接线，资产状态沿用[资产交接](../../shared/asset-handoff.md)；`verify/close` 按[验证约定](../../shared/verification.md)补实际影响，Evidence 与 Decision 仍由原记录持有。

2026-10-01 资料核对：官方 [Object3D](https://threejs.org/docs/pages/Object3D.html)说明层级/移除及共享资源；[WebGLRenderer](https://threejs.org/docs/pages/WebGLRenderer.html)说明 canvas、循环、尺寸与释放；[GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html)说明 URL、addons/decoder；[OrbitControls](https://threejs.org/docs/pages/OrbitControls.html)说明相机控制。这些当前官网页面不是固定版兼容证明；采用 API 前核对现场版本。业务组织和生命周期所有者是工作流选择。本轮未安装/运行引擎或真实项目，未验证任何现场版本及 R3F 集成。
