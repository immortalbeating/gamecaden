# Cocos Creator：Scene、Node、Component 与资源生命周期

新增 Scene/Prefab、独立页面、复用单位、跨场景状态、池化/外部订阅、资源持有或编辑/UI 方式变化时读取。先用[共同结构合同](structure-contract.md)，再读取本页命中的机制；版本和平台由 [Cocos Creator profile](../engines/cocos-creator.md)决定。本页复用该 profile 的 ID，不新增同义 Gate。

## 对象与制作源

**引擎事实（3.8 资料基线）**：Node 组织变换树并承载 Component，组件提供渲染、输入、物理或脚本行为；保存的 `.scene`/场景资源与运行 `Scene` 根节点分别说明，Prefab 资源实例化产生 Node 树。普通 TS 对象可承载规则和状态，不自动收到组件回调。`World`、`GameSession`、`LevelHost` 是项目可选职责名；Canvas、UITransform、Sprite、MeshRenderer 等是组件，不能当成 Godot 的同名节点类。[场景资源](https://docs.cocos.com/creator/3.8/manual/en/asset/scene.html)、[运行 Scene](https://docs.cocos.com/creator/3.8/api/en/class/Scene)。

**本工作流默认**：独立编辑或重复实例的内容使用合适 Scene/Prefab/组件。清楚的代码工厂、数据生成器与预览也可继续用；选择须支持本次编辑和验证结果。组件连接引擎，业务模型通过显式数据/动作接口提供状态；简单局部行为可以保留在一个组件。

| 命中范围 | 默认与允许替代 | 常见反例 | 可观察验收 |
|---|---|---|---|
| 新页面或复用单位（COCOS-COMPOSITION） | 在原设计标明 Scene/Prefab 来源、Node/组件、实例入口与必要依赖；既有组合能承担用途时继续使用 | 把每个 TS 类都做成节点；Prefab 中隐式查一个固定宿主路径；只复制运行节点却没有制作源 | 重载制作源后接线保持；提供必要依赖后两个实例或另一个宿主仍有效 |
| 跨场景/共享状态（COCOS-STATE） | 只读定义与实例/本局状态分别持有；需要跨真正 Scene 切换时，可用符合引擎要求的常驻根与组件，或现有应用层持有的模型 | 局部选中项全局化；修改同一共享 Asset 当每单位血量；每个 Scene 又创建一份常驻会话 | 两实例状态独立/共享符合意图；切场景保留目标状态，新局按设计重置，没有重复常驻所有者 |
| 启停/池化/异步（COCOS-LIFE） | 按活动范围配对连接/取消，先区分引擎自身管理与自己加到外部总线、SDK、原生计时器的工作；晚到结果检查原请求/消费者是否仍适用 | 每次 onEnable 增加外部回调而只在最终 onDestroy 清理；普通 helper 假定也有组件回调；旧加载结果覆盖新页 | 停用、再次启用、入池/取出和切换后只有预期效果；离场结果按归属处理 |
| 加载/持有/释放（COCOS-ASSETS） | 跟踪静态与动态引用；动态长期持有按实际 addRef/decRef 或项目等效资源拥有机制配对；Bundle/Asset 释放前定位仍在使用的消费者 | JS 字段赋值被误当引擎引用计数；离场一律 releaseAll；预加载回调被当成已经创建 UI/运行 Scene | 一个消费者退出后另一个仍能显示/运行；重新加载、失败和过期返回正确；必要释放没有漏掉，也不释放仍需共享的内容 |
| 资源迁移/复制（COCOS-IDENTITY） | 原资产保留身份与导入设置；新独立副本取得独立 UUID，并核对 SpriteFrame 等子资源及实际字段 | 只按路径认资源；移动时丢 .meta；同时保留两份相同 UUID；为解决缺失批量重建全部身份 | Editor 导入后受影响 Scene/Prefab、组件字段、Bundle 加载消费者仍对应正确对象 |
| UI 与编辑（COCOS-UI） | UI 根使用适当 Canvas/RenderRoot2D；UITransform 管矩形，Widget 做对齐，Layout 做布局；相机与 layer/visibility 决定显示；按目标适配尺寸/安全区/触摸 | 将 Canvas 当自动布局或唯一 UI 可见性保证；控件布局与手写坐标争抢；遮罩显示正确但输入穿透/吞掉 | 在实际目标尺寸、相机/弹窗与输入路径中检查；场景/Prefab 或生成器提供可用编辑与预览入口 |

## 生命周期和常驻范围

onLoad/start 用于对应的一次初始化，onEnable/onDisable 对应组件或节点的启停，onDestroy 对应销毁回调；具体顺序与执行条件按现场版本。禁用、移出父节点、池化保留和真正销毁分别判断。`destroy()` 的销毁请求与帧末回收区分，异步与 SDK 回调不因此自动结束；对外部回调保留可精确解除的身份。

3.8 的 `director.addPersistRootNode` 要求目标处于场景的根层级；常驻节点跨 Scene 切换保留，但不自动保证业务唯一或新局清零。`removePersistRootNode` 取消常驻属性，不是立即销毁。仍由合适应用对象持有的普通模型可以继续使用，不把所有工具函数/局部视图提升为常驻节点。[生命周期](https://docs.cocos.com/creator/3.8/manual/zh/scripting/life-cycle-callbacks.html)、[场景管理](https://docs.cocos.com/creator/3.8/manual/zh/scripting/scene-managing.html)。

## 资源引用与目标平台

Asset Manager 可分析序列化中的静态依赖，普通 JS 动态赋值不自动体现动态持有关系。按实际拥有机制维护引用与释放；直接 release/releaseAsset/releaseAll 可直接释放目标资源，其安全性不能用“引擎会做引用检查”概括。资源仍共享时，先处理真正持有者和依赖。释放运行节点、释放 Asset、移除 Bundle 管理项与清理下载缓存是不同动作，按本次目标区分。[资源释放](https://docs.cocos.com/creator/3.8/manual/zh/asset/release-manager.html)。

游戏权威状态与命中的外部适配寿命分别说明。浏览器构建采用 [Web](../platforms/web.md) 命中项，其它明确目标就近核对真实构建/运行条件、工具链与官方资料。预览支持的行为只证明其环境，实际交付按本次目标取证。

## 候选例子

以下是说明性设计，未建工程或运行，不是官方固定模板。

**单 Scene 拾取试验**：Scene 中 Node 挂玩家/拾取物组件；重复拾取物可用 Prefab，共享奖励定义，当前场景组件持有本局分数。一个简单试验无需先做常驻会话或 Bundle 系统。检查两个实例的奖励与消失、真实拾取一次、重开后的分数；只交设计时保存这些安排，不填运行通过。

**跨关、结算、新局**：原设计要求结果页保留本局分数。候选采用常驻 `SessionHost (Node + 自定义 Component)` 持有本局模型，`Play.scene` 和 `Result.scene` 消费模型；本次自定义组件的职责和代码来源要能定位。玩法内可组合：

```text
Play (Scene)
├── World (Node + 本次所需玩法/物理/渲染根组件)
│   ├── CurrentLevel (Node，关卡/Prefab 实例根)
│   └── Player (Node，若本次换关要求保留则置于关卡外)
└── HUDRoot (Node + Canvas + UITransform)
    └── ScorePanel (Node + UITransform + 所需布局/显示组件)
```

本例 World 若使用 Sprite 等 2D 渲染组件，按官方机制提供合适的 RenderRoot2D/Canvas 祖先与 UITransform 等组件；若使用 3D 内容，取其实际渲染/物理组件和 camera/layer。树只示意组合归属，不能用 `World` 名称推断渲染能力。

真实 `director` Scene 替换与 Play 内局部关卡替换的释放范围不同，设计须指出实际路径；玩家置于 CurrentLevel 外只解决局部替换，不保证跨真正 Scene 切换保留。HUD 使用实际 camera/layer 接线，结果页发新局意图，由会话拥有者重置后进入玩法。动态资产按各消费者持有/释放，验证切换、重进、多实例、剩余共享消费者和目标宿主路径。

## 来源与交付边界

资料核对日期：2026-10-01，技术事实参照上述链接及官方[节点/组件](https://docs.cocos.com/creator/3.8/manual/zh/concepts/scene/node-component.html)、[项目结构](https://docs.cocos.com/creator/3.8/manual/zh/getting-started/project-structure/index.html)、[资源工作流](https://docs.cocos.com/creator/3.8/manual/zh/asset/asset-workflow.html)、[Canvas](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/components/editor/canvas.html)、[UITransform](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/components/editor/ui-transform.html)、[Widget](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/components/editor/widget.html)、[Layout](https://docs.cocos.com/creator/3.8/manual/zh/ui-system/components/editor/layout.html)。3.8 文档中保留的早期示例不直接证明其他版本所有 API 兼容。

默认方案与观察方法属于本工作流选择。设计一致性、Editor 保存/接线、运行行为、目标构建及人工接受仍按[共同证据](../../shared/verification.md)分别报告，归原 Task/Evidence/Decision。本轮仅核对文档，未运行 Creator 或任何候选。
