# 材料、约束与推进条件

本合同是面板、Skill 和工具共同使用的语义入口。定义放在其原拥有者：长期规则归 Spec，整体出口归 Epic/里程碑，执行前提归依赖方 Task。面板是带来源的派生视图，不维护第二份进度或批准账本。

## 准入与适用性

仅纳入承担目标、规格、工作、材料、证据或决定职责的来源与章节。登记表示能定位，不表示内容完整或已经采用。生效、候选、参考、历史、未知分别表达；停车场不成为当前承诺。角色、地图等材料的触发、等效形式和需要时机见[材料要求](material-requirements.md)。

缺失的必要材料仍可登记为需求条目，source ref 留空，显示 missing。applicability=unknown 表示适用性未核实；not_applicable 必须来自本次有依据的判断。工具不通过文件数或任务关闭数推断完整性。

声明 not_applicable 时用 applicability_reason 保存判断理由。materials.applies_to 可定位受影响工作，省略时继承本 Task/Epic 的作用对象；在其他文档中省略表示尚未限定对象。rules.layer 可区分 common/domain/engine/project 来源层，层级不是强制覆盖优先级。

## 同一来源中的可选结构

需要共享显示层级、材料和条件时，在原 Markdown 正文放一个标注块。无需给所有文件加标注，也无需把已有普通记录迁成新对象。一个来源记录最多一块，id 是本文件局部编号；跨引用使用原文件路径＋fragment。正文继续解释定义，机器块只维护需结构化复用的那部分定义，避免同时维护两份条件列表。

~~~~text
<!-- workflow:governance -->
```json
{
  "schema_version": 1,
  "materials": [{
    "id": "map-blueprint",
    "title": "可施工的空间蓝图",
    "domain": "map",
    "requirement": "required",
    "applicability": "applies",
    "for_actions": ["正式地图生产"],
    "purpose": "明确尺度、连接、入口与消费者"
  }],
  "conditions": [{
    "id": "production-ready",
    "title": "空间关系具备生产依据",
    "domain": "map",
    "scope": "关卡 A",
    "action": "正式地图生产",
    "strength": "required",
    "authority": "effective",
    "applies_to": [{"id":"T-004"}]
  }]
}
```
<!-- workflow:endgovernance -->
~~~~

此示例没有材料 ref 和检查依据，读取结果是材料缺失、条件未核实。它不会阻断其他对象的灰盒试验。

准确字段由 [schema](../schemas/governance-v1.schema.json) 拥有：
- outcomes：成果/里程碑及承接工作引用；不保存工作状态。
- rules：约束性质、领域、作用范围及适用对象。
- materials：所需信息、适用性、用途/动作和原材料引用。
- conditions：作用对象、限制动作、强度、采用性质与判断依据。
- 已有 Task.epic / depends_on / related 继续拥有原关系；引用、归属、需要结果不互相冒充。
- flows / relationships 按需声明动作前提组合与规范职责关系，见[关系表达](relation-views.md)；不另存工作状态或授权。

outcomes.work 是成果承接引用，不能因一个工作被引用就将它变成所有相关工作的执行前提。conditions.applies_to 明确列对象；不会仅凭 Epic 归属向全部 Task 扩散阻断。共用条件可由多个对象引用，不复制定义。

## 判断与来源

条件没有 check 时为 unknown，交给模型或指定判断者分析后在原 Evidence/Decision 保存依据。check 使用原格式 Subject，必须绑定 version；kind 为 evidence 或 decision，可限定 actor_kind。proofs 提供精确引用；省略时在已登记的相应记录中找严格匹配的依据。

- 对象、候选、版本、scope 与 use 均需匹配。提供 coverage 时，Evidence 还需覆盖指定项目。
- Evidence 的 passed/failed 只支持其声明覆盖；模型定性检查可由 agent Evidence 承载，不能伪装为实际运行测试。
- Decision 的 accept 支持其明确范围，reject/revise 表示该范围未满足；需要用户决定时用 actor_kind=user。
- Decision 事件整体 scope 默认也须匹配 Subject.scope；整体范围不同的多对象事件先作语义核对，再用 check.event_scope 显式绑定其原整体范围。
- 已被撤回或替代的事件失效；同一范围的有效依据矛盾时显示 unknown。
- 文件/manifest 当前摘要变化时显示 stale；无法验证的版本形式、缺少依据或引用损坏保留 unknown。
- 候选、参考、历史规则不成为生效硬门禁。只有 effective + required 才表示相应动作需要满足的前提。
- condition 状态为 satisfied/unsatisfied/unknown/stale/not_applicable；material 状态为 located/missing/unknown/not_applicable。它们不改变 Task planned/active/closed/cancelled。

工具核对来源、版本和记录声明。证据内容是否足够、用户授权、下一步是否适合执行，仍由相应 Skill 判断。satisfied 不自动授权生产、关闭 Task、提交 Git 或唤醒 Agent。

适用 Task 与检查 Subject 可以不同：Task 常消费一个资产、蓝图或上游结果。条件定义负责声明为何这个检查支持本动作，工具不会从二者 ID 相同或不同猜测业务关系。视图展示两者及原定义供复核。coverage 分开说明是否已有结构、是否识别材料/条件、记录扫描是否完整；任一部分存在都不代表全项目识别完成。

## 新旧项目

init 首先判断材料职责与采用范围，design 补齐当前动作需要的实际内容。原资料可以被引用；混合文档按章节处理；仅在需要关系展示时结构化相应部分。旧来源仍只读时，面板列已登记资料并明确“治理未识别”，不能猜测未知任务或从文字“通过”生成绿灯。

为旧项目补标注需先确认相应定义的维护归属；可以在获授权的当前 Task 中定义本次条件，引用旧资料，不复制它们的正文或旧任务状态。缺失、冲突和未知留下清楚的补齐路径，不一次生成全项目空模板。

## 使用

[面板与职责衔接](panel-workflow.md)说明时机、上下文与回读。`workflow_governance.py --project-root ... --focus T-004` 输出只读模型；`GET /api/projects/<id>/governance?focus=T-004` 为同一视图。节点与边只用于导航和解释，来源 revision 变化后重建，不保存可单独编辑的聚合状态。
