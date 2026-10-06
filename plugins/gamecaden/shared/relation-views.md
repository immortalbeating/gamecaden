# 推进条件与规范来源视图

需要解释跨动作前提或多层规范职责时读取。它们复用[治理合同](governance.md)和原记录，不新增任务、批准或进度库。

## 选择表达

| 需要回答 | 定义与视图 |
|---|---|
| 本动作需要什么结果、欠项影响哪些后续 | 原来源的 flows；推进条件图 |
| 谁定义规则、委托职责、生产或消费成果 | 原来源的 relationships；规范来源图 |
| 只查直接关联或处理局部快改 | 沿用已有 Task 依赖、条件和原文；无需补整套标注 |

所有定义按项目真实范围提供。分组便于阅读，不表示先后；前置结果由表达式明确引用。项目专用的阶段、编号和批准方式不成为其他项目的默认要求。

## flows：原动作的前提定义

在原 workflow:governance 块中按需增加 flows。每个流程提供 id、title、scope、authority 与非空 steps；每步提供 id、title、target、action，可加 group 和 requires。target 定位原作用对象，action 对应实际动作。步骤不是另一个 Task，状态也不另行保存。

requires 是单键表达式，可递归组合：

```json
{"all": [{"step": "candidate"}, {"condition": {"path": "./production.md", "fragment": "visual-choice"}}]}
```

- condition 引用原 conditions；path/fragment 及 source/project 限定继续校验。
- step 引用同一流程的步骤 id，表示需要其声明前提的结果。
- all 表示全部适用项须满足，any 表示任一适用分支满足即可；组合至少有一项。
- 没有 requires 时保留 unknown；Task closed、材料 located、文件存在不填补判断缺口。

条件叶项只有在 effective、required、作用对象匹配且 action 相同的情况下，才支持本步判断。参考、提议、建议、错误对象或动作保留 unknown。证明仍由原条件的 Subject、版本、范围、用途、coverage 与 actor 要求核对。用户决定条件使用相符的 user Decision；机器 Evidence 不替代它。

| 组合 | 判断 |
|---|---|
| all | 排除明确不适用项；任一未满足为 unsatisfied，余项全满足为 satisfied，否则 unknown 优先于 stale |
| any | 任一适用项满足为 satisfied；否则 unknown 优先于 stale；其余适用项全未满足为 unsatisfied |
| 全部不适用 | not_applicable，不记为通过 |
| 循环引用 | 全部成环成员固定 unknown；布局或声明顺序不改变结论 |
| 非生效流程、坏引用或错误定义 | 保留未核实及诊断，不生成就绪结论 |

这些结果只解释已声明前提。satisfied 不授权实施、接受、关闭或发布。后续关系由来源重新派生，每个后续动作仍按自己的表达式判断。

## relationships：职责与来源

每项提供 id、from、to、kind、authority，可加 label。两端使用原 Ref；边保留声明来源与版本。

| kind | 关系含义 |
|---|---|
| delegates_to | 定义者委托部分职责 |
| defines | 来源定义对应规则或对象 |
| provides_policy | 来源提供该工作的判断政策 |
| produces | 工作或生产职责产出成果 |
| consumes | 工作或消费职责读取输入 |

它们用于导航和责任解释，不参与前提计算。原 contains、supports、references、requires、governed_by、verified_by、accepted_by 保留原意。规范定义与任务、资产、Evidence、Decision 的实例事实分别显示。

## 使用和回读

面板总览提供“推进条件 / 规范来源”切换。规范来源默认以折叠的项目领域概览组织已读来源，展开领域和文档可阅读真实文档及其收录内容；“来源与影响”复用同一批原节点与原关系。进入领域默认使用文档树阅读器：左侧为实际收录树，右侧为所选文档的实际章节正文；可切换焦点关系图，不把文档树当执行树。两种来源图视角支持纵向/横向排版，聚焦领域保留直接相连的一跳外部端点；返回、面板刷新及项目切回保留当前会话中仍有效的阅读选择、章节、展开、缩放和位置，记忆按项目 binding 隔离，不承诺浏览器整页重载恢复。当前关联是局部范围，已登记范围也不表示全部项目规范已识别。流程选择、折叠和缩放是显示设置，不改来源。

节点详情显示职责、归属、章节、前提、证明、定义及引用此结果的后续动作；汇总关系可逐项回读每条原始关系。原文按钮仅用于已登记可读来源，按正文 heading 或治理 id 精确定位，未登记、缺失或同名多处时保留位置与核对提示。窄屏使用领域/文档/步骤列表及完整详情。没有 navigation 的已读来源、未分类资料与孤立文档仍保留，不要求项目为界面补齐标注。

回到前台时使用 `GET /api/projects/<id>/revisions` 检查已登记物理来源版本；未变化不加载完整数据，变化时合并刷新，成功写回按受影响记录更新。编辑、对话框或 busy 时延后，不改草稿基准和冻结请求；缺失或读取期间变化不判为未变化。轻量检查不是门禁或工程同步，具体边界见[面板衔接](panel-workflow.md)。当前范围见[阅读器与刷新设计](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/panel.md)及[核验](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/validation.md)。

GET governance 与命令行继续使用同一只读模型，兼容增加 flows、relationships，条件增加 expected_check 说明判断类型。步骤的 condition_keys、predecessor_keys、affected_keys 是本轮引用结果；affected_keys 不表示那些动作必定受阻。

嵌入 EV/Decision 的定义由实际嵌入记录拥有，外层不重复解释。局部 ID 冲突、读取期间来源变化和无效限定继续报错或保留未知，不靠读取顺序覆盖。

字段由 [schema](../schemas/governance-v1.schema.json)拥有，实现见[派生模块](../scripts/workflow_relations.py)。本轮范围与结果见[设计](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/panel.md)及[核验](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/validation.md)。

## 只读文档导航合同

原文 `workflow:governance` 块可选 `navigation` 对象，允许 `domain: string`、`responsibility: string`、`parent: Ref`，至少一项，拒绝其他字段。此对象描述来源记录的阅读归属，不增加依赖、门禁或状态，也不改变 rules、flows、conditions、authority 的计算。

记录节点派生 `navigation_domain`、`navigation_responsibility`、`navigation_parent_key`、`navigation_source_key`；无声明时为 null，不推测领域。声明来源指向本记录节点，来源版本沿用节点 `revision`。父子两端必须是已读取的 `document` 节点；原 Ref 的 source、project_id、id 限定仍须校验，不读取未登记来源来补全导航。自引用、循环、坏引用、非文档父对象保留 `invalid_navigation`、`invalid_navigation_parent` 或 `navigation_cycle` 诊断，不生成相应父子关系或通过结论。导航关系只用 `navigation_parent_key` 表达，不加入 `edges`。

已读取记录同时派生 `headings: [{text, level, fragment}]`，忽略 fenced code、治理 JSON 与嵌入记录示例；嵌入原生记录的标题归该记录所有。fragment 是原正文标题文本，供阅读器定位，不声称存在另外的文件或批准事实。标题和导航元数据只在读取时派生，原文仍由原记录提供。


可在原正文已有的治理块中合并可选导航字段；例如子文档声明阅读领域及已读取的父文档：

````markdown
<!-- workflow:governance -->
```json
{
  "schema_version": 1,
  "navigation": {
    "domain": "地图与关卡",
    "responsibility": "说明房间连接与路线",
    "parent": {"path": "./level-design.md"}
  }
}
```
<!-- workflow:endgovernance -->
````

上例只表达阅读收录关系。正文标题由 headings 派生；原治理条目可用 `{"path":"./level-design.md","fragment":"route-check"}` 回读 id 为 route-check 的定义，fragment 不作为第二份状态。parent 须解析到 document，本例不把规则条目当作父文档。已存在的 rules、conditions、flows 等继续保留在同一块中，不另建重复治理块或状态记录。当前入口见[领域设计](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/panel.md)与[本轮核验](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/validation.md)。
