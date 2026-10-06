# Cocos Creator 工程 profile

## 触发与版本边界

实际运行根采用 Cocos Creator，或当前设计已经选定它时读取。先查实际 Creator/engine 版本、入口场景、模块、渲染/物理设置、插件和目标平台。本轮机制资料使用 3.8 LTS；2.x、4.x 或其他现场版本先核对对应机制，不要求升级。

目标平台与引擎分别确认。浏览器目标叠加 [Web](../platforms/web.md)，其它明确目标核对现场构建/运行条件和对应官方资料，预览与实际产物分别留证。Cocos2d-x 与 Creator 也不凭名称合并为同一种工程。

## 需现场识别的事实

- 当前项目配置、实际编辑器与运行引擎版本、启动 Scene、构建目标和输出；只交设计且尚无工程时保留这些运行事实未知。
- 当前对象是 Scene/Prefab 资源、Node/Component 实例、共享 Asset、普通 TS 模型还是构建适配代码；编辑来源与真实消费者是什么。
- 节点/组件启停、场景切换、池化、外部事件、平台前后台、动态加载和资源持有的实际关系。
- 命中资源的 `.meta`、UUID/子资源、属性接线、Bundle/路径/类型、远程资源与平台缓存来源。

## 条件规则

规则性质按 [shared/rules](../../shared/rules.md)。必要结果在命中时成立；默认组织允许满足同一用途的替代方法。

| ID | 性质与触发 | 要求或默认做法 | 可观察核对 |
|---|---|---|---|
| COCOS-ROOT | 必要：接入或确认实际工程 | 从真实配置/Editor、入口与目标识别版本和运行根；不能用预定引擎或安装目录替代工程事实。 | 可定位当前来源和目标产物；没有工程时只报告选定的设计目标。 |
| COCOS-COMPOSITION | 必要：新 Scene/Prefab、复用对象或结构变化 | 按[结构专题](../references/cocos-structure.md)区分保存资源、Node、Component 与普通模型；明确装配、依赖、编辑和实际类型。 | 保存/重新加载、Prefab 实例接线与必要独立实例符合设计；目录/节点数量不作为合格证明。 |
| COCOS-STATE | 必要：共享配置、跨场景或多实例状态 | 区分共享 Asset/定义与每实例/本局可变状态；常驻节点或已有局模型按实际寿命持有，明确新局重置。 | 修改一实例不会误改其他实例；切换和新局保留/清零符合原设计。 |
| COCOS-LIFE | 必要：启停、池化、切场景、监听或异步变化 | 区分 onLoad/start、onEnable/onDisable、onDestroy 与普通对象/平台作业；按真实活动范围管理自己的外部回调和晚到结果。 | 禁用/重启、入池/取出、切换后调用次数及旧结果符合设计；销毁请求与实际回收分别确认。 |
| COCOS-IDENTITY | 必要：资源移动、改名、复制或导入 | 保持原资产的 `.meta`/UUID 与实际子资源引用；新独立资产副本取得独立身份。查明缺失/冲突后按可靠编辑/恢复流程处理。 | 受影响 Scene/Prefab/组件字段和动态加载仍指向正确资源，无意外缺失或重复身份。 |
| COCOS-ASSETS | 必要：动态加载、Bundle 或释放共享资产 | 定位 path/type/Bundle/消费者，区分预加载、加载、实例化与接入。按静态/动态引用和共享寿命选择持有与释放；直接 release 系列不能当安全引用检查。 | 晚到/失败/重进不回写旧消费者；退出一方后其他消费者仍有效，需要释放的对象/资源不累积。 |
| COCOS-UI | 必要：UI 布局、相机、输入或适配变化 | 按 Canvas/RenderRoot2D、UITransform、Widget/Layout、Camera/layer 等实际职责组织；布局、显示和输入各有清楚来源。 | 目标尺寸、安全区域、遮罩/弹窗、相机和触摸下位置及命中正确；仅挂 Canvas 不证明可见或可操作。 |
| COCOS-TARGET | 必要：本次承诺目标产物或平台接入 | 对照现场版本与实际目标核对构建、模块、资源和命中能力，Editor/Web 预览、目标构建与交付入口分别留证。 | 从真实交付入口观察本次用户路径，证据标明版本、环境与实际覆盖。 |

## 与现有职责交接

init 定位真实或预定引擎及平台；design 把命中的组成/寿命/编辑与观察写入原设计，读取[结构专题](../references/cocos-structure.md)。develop/assets 修改真实制作源与消费者，按[资产交接](../../shared/asset-handoff.md)保留候选、接受、选用与运行接入的范围。verify/close 复用原 Task/Evidence/Decision，补实际变更涉及的保存、实例、启停、切换及目标产物证据。

已有工程与编辑方法能完成本次交付时复用；缺陷来自错误状态或寿命边界时，就近处理必要范围。纯文字快改只取显示与原收尾要求，不全量重建场景/Bundle/平台链。

## 官方来源与本轮范围

- [节点和组件](https://docs.cocos.com/creator/3.8/manual/zh/concepts/scene/node-component.html)、[项目结构](https://docs.cocos.com/creator/3.8/manual/zh/getting-started/project-structure/index.html)、[资源工作流](https://docs.cocos.com/creator/3.8/manual/zh/asset/asset-workflow.html)：对象、制作来源与资产身份。
- [生命周期](https://docs.cocos.com/creator/3.8/manual/zh/scripting/life-cycle-callbacks.html)、[场景切换](https://docs.cocos.com/creator/3.8/manual/zh/scripting/scene-managing.html)、[资源释放](https://docs.cocos.com/creator/3.8/manual/zh/asset/release-manager.html)：回调、常驻范围与资源引用机制。
- [Canvas](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/components/editor/canvas.html)：UI/相机边界；具体构建目标在其实际承诺成立后核对对应版本资料。

资料核对日期：2026-10-01。事实来源如上，组织默认和验收选择属于 Gamecaden；本轮没有运行 Creator/游戏、构建目标包或验证平台 SDK，也不证明市场使用排名。
