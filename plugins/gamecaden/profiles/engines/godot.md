# Godot 工程 profile

触发：本次实际运行根采用 Godot，或新项目设计已明确选用 Godot。已选但未建立的工程可据此形成方案，运行能力仍待确认。先定位已有的 `project.godot`、入口场景、实际编辑器版本、渲染方式、脚本语言、插件及目标平台；已有映射可复用。仅同仓存在 Godot 文件而本次只改独立工具时，按该工具选择规则。

本轮官方资料核对基线为 Godot 4.6；它不要求项目升级到此版本。4.x 具体补丁、3.x、C#/.NET 和导出平台能力应按本项目配置及对应官方文档核实，未核对部分不声称兼容。

## 场景与状态

| ID | 触发 | 要求或默认做法 | 可观察核对 |
|---|---|---|---|
| GODOT-SCENE | 页面/关卡切换、可复用单位或独立生命周期变化 | **必要**：状态归属、入口、外部依赖和通信接口能辨认；**默认**用职责清楚的场景/子场景和脚本组合，由拥有关系的一方配置依赖。独立 View 的存在不证明所有状态已经合理拆分。 | 重复实例/再次进入可工作；子场景不依赖未声明的上层路径；本次路由及局部状态各有明确维护者。 |
| GODOT-RESOURCE | 多个实例引用并修改同一 Resource | **必要**：区分共享定义与实例可变状态；按意图选择共享、实例数据或适用的复制/场景本地化。 | 改变一个实例后，其他实例的表现符合共享约定；检查嵌套资源引用，不能假定顶层复制已隔离全部数据。 |
| GODOT-SAVE-SCENE | 生成/修改需要保存为 PackedScene 的节点与资源 | **必要**：保存范围、节点 owner 和持久引用符合实际目标。临时运行节点不默认全部写进场景。 | 保存后重新读取/实例化目标场景，关键节点、脚本和资源仍存在；内存中显示正确不等于已持久化。 |
| GODOT-LIFETIME | 换场景、暂停、节点释放、池化或异步回调变化 | **必要**：将树内存活、规则状态、全局服务及本次外部订阅分清；使用实际版本的进入/退出/处理语义。 | 重开/退出后不重复处理、引用失效对象或遗留输入；需保留的数据跨切换仍正确。 |

场景拆分遵循责任和依赖，简单有界试验可先在单一场景完成；当加入独立页面、可复用单位或复杂持久状态时，设计相应边界再继续扩展。纯文案快改不因此触发全面重构。[场景组织依据](https://docs.godotengine.org/en/4.6/tutorials/best_practices/scene_organization.html)

这些变化及节点/UI 编辑保存方式变化时，读取[场景、节点与状态专题](../references/godot-structure.md)。专题把 GODOT-SCENE、GODOT-LIFETIME、GODOT-SAVE-SCENE、GODOT-SPACE／INPUT 的要求落实为组成、真实类型、归属、接口和可观察验收，并区分自定义职责名、引擎类型、Autoload 与场景格式。

Resource 的 `resource_local_to_scene` 作用于场景实例化；运行时修改该标志不会追溯隔离已经存在的实例。具体复制语义按实际资源类型与版本检查。[Resource 依据](https://docs.godotengine.org/en/4.6/classes/class_resource.html)；持久场景的保存范围见 [PackedScene](https://docs.godotengine.org/en/4.6/classes/class_packedscene.html)。

## 输入、空间与运行

| ID | 触发 | 要求或默认做法 | 可观察核对 |
|---|---|---|---|
| GODOT-SPACE | 角色尺度、碰撞/导航、地图、相机或投影变化 | **必要**：Node2D/Node3D/Control 的坐标关系、变换继承和空间数据对得上当前设计。物理处理与显示处理按实际机制选择。 | 实际输入经过入口/路径/交互，在目标相机中可读且碰撞/导航正确；修改精灵比例后检查相关锚点和空间范围。 |
| GODOT-INPUT | 输入路由、UI 焦点、暂停或输入设备变化 | **必要**：沿用/调整真实 InputMap 和事件消费者，说明 GUI 与玩法输入的关系、暂停时哪些对象继续处理。 | 按本次承诺走开始、返回、暂停/恢复和关键操作；界面不意外吞掉或重复发出玩法动作。 |
| GODOT-IMPORT | 新资源、导入设置、插件、脚本类型或工程结构变化 | **必要**：核对当前项目、引擎/插件版本与首次根错误；沿真实导入流程确认资源、路径/UID、大小写与加载关系。 | import/解析/启动结果分别记录；级联报错先追根因；旧进程、端口响应或已有截图不证明本次工程已运行。 |
| GODOT-EXPORT | 目标平台交付、导出设置或版本兼容性属于本次承诺 | **必要**：检查实际导出配置、所需模板及工具链，使用匹配版本的能力验证产物。 | 导入、编辑器/headless 检查、导出和外部启动各说明覆盖；本地编辑器通过不自动表示目标平台可交付。 |

节点的进入/离开树及处理范围以 [SceneTree](https://docs.godotengine.org/en/4.6/tutorials/scripting/scene_tree.html) 为技术依据，具体重开、保存和暂停规则由本项目拥有。运行核验取 [common](../common.md) 中命中的条目及 [verification](../../shared/verification.md)，不再维护另一份 Godot 任务状态。

## 目录、身份与工具

Godot 按实际文件系统组织内容，可按功能将场景、脚本及资源放在一起；文件夹名称的默认建议不成为全仓重命名理由。准备屏蔽制作源或工作流资料的导入时，先确认没有运行消费者，再使用实际版本支持的 `.gdignore`。不要屏蔽仍由项目读取的资源目录。[工程组织](https://docs.godotengine.org/en/4.6/tutorials/best_practices/project_organization.html)

将源资产及有引用意义的身份/导入配置与 `.godot/` 可重建缓存区分；既有 UID 和资源引用按实际引擎版本维护。Git 文件策略沿用项目约定，本 profile 不授权删除缓存、历史或替换版本控制配置。[版本控制参考](https://docs.godotengine.org/en/4.6/tutorials/best_practices/version_control_systems.html)

设计由 design 形成责任/输入安排；develop/assets 落实场景、资源和消费者；verify/close 读取对应结果。使用实际可用的编辑器、CLI 或 MCP，依专业 Skill 处理连接和操作；工具缺失时说明它影响哪项操作，可独立的分析或编辑继续。不要仅凭 MCP 可调用就假定连接到正确工程。

## 来源与范围

技术约束参照上述 Godot 4.6 官方页面及[导出说明](https://docs.godotengine.org/en/4.6/tutorials/export/exporting_projects.html)，核对日期 2026-09-27。目录方案、责任边界和验证强度是本工作流的选择规则；官方资料不要求所有项目采用同一结构。本轮没有运行 Godot 或验证实际项目导出。
