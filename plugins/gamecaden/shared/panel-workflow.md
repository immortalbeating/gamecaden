# 面板定位、读回与续接

供 flow/init/design/develop/assets/verify/close 在需要跨记录定位 Task、候选或条件时使用。规则语义见 [材料职责](material-requirements.md) 与 [governance 合同](governance.md)；本页只说明如何把派生视图用于当前工作。面板仍按 [panels/README.md](../panels/README.md) 启动，是现有职责 Skill 的入口，不是第九个 Skill 或新进度库。

## 取得本次范围的视图

确认实际项目及已注册的来源后，从面板 `GET /api/projects/<id>/governance?focus=T-003` 读取派生只读图、材料和条件；按当前 Task/候选及其关系阅读。`focus` 定位对象，不删去图中其他来源。无面板或需命令行时使用 `scripts/workflow_governance.py --project-root ... [--workspace ...] --focus T-003` 取得同一派生模型。输出报告适用条件状态，不自动授权执行、接受、关闭或改变原记录。

面板可定位到 `#project=<id>&view=overview|assets|review|documents&task=T-003&asset=A-002&candidate=C-001`；只带当前需要的参数。`connect=` 仍只用于一次连接认证，不作为可复制的工作深链接。项目 ID、Task、资产和候选均应来自已登记真实对象；片段不能指定新项目根或扩展权限。

| 当前职责 | 视图用法 |
|---|---|
| flow / init | 找到原 Task、权威来源和相关材料缺口；旧项目只映射本次范围，按原来源继续 |
| design | 对当前动作筛选材料职责和条件，点回设计/规格章节，形成必要方案 |
| develop / assets | 定位待接入候选、用途、消费者和当前条件；读回原 Task、台账、Decision/manifest 后执行 |
| verify / close | 由条件定位原要求与实际 Evidence/Decision，判断覆盖、接受和关闭；视图结论不代替核验 |

## 阅读与来源更新

领域内部默认使用文档树阅读器，左侧按实际收录关系选择文档，右侧读取实际章节正文；可切换焦点关系图，继续按原文标题、治理 id 与逐项关系回读。树是阅读组织，不是另一份任务清单或门禁。说明与范围见[阅读器与刷新设计](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/panel.md)和[本轮核验](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md)。

面板回到前台（窗口 focus / 页面 visible）时调用 `GET /api/projects/<id>/revisions` 检查已登记物理来源版本。只有 complete 为 true、digest 非空才比较；未变化不加载完整视图，变化时合并刷新，成功写回更新受影响记录。全量读取前后版本不一致、来源缺失或检查失败时保留提示，不认定已是最新。编辑、对话框和 busy 时延后自动刷新，原草稿基准及冻结请求不改；当前会话阅读选择、章节、展开和位置按项目 binding 隔离。无需每推进一次就手工维护面板事实，仍按原记录职责保存真正变化。轻量检查不扫描引擎运行根，也不证明实际工程、素材字节或 Git 已同步；这些仍须显式读取和对应证据核验。

## 读回后继续

需要多层前提或规范职责时，使用[关系视图](relation-views.md)。推进图读取已声明的流程与条件组合，来源图保持原关系方向；它们均不自动执行、接受或关闭。没有流程定义时保留未核实，沿用现有条件与原文。

打开面板记录或 CLI 结果后，回读所引用的原 Task、材料章节、资产台账、Decision、Evidence 与实际工程状态；核对来源版本和本次工作树。派生结果可能过时或只覆盖登记来源，诊断和未知项应保留。面板不运行引擎，也不自动唤醒 Agent。

旧格式来源仅登记为只读且没有可解释的结构化定义时，面板可显示原资料并提示治理未识别；不能由此推断没有材料或条件，也不能声称门禁通过。材料 `located` 只说明来源可定位，条件 `satisfied` 也须核对其对象、版本、证据覆盖和当前授权。

可复制续接摘要应带项目与原记录定位、来源/版本、当前范围、观察到的条件与缺口、下一动作及深链接。它是交接线索；接手 Agent 仍从原记录和现场重读后继续已有授权，不把摘要或页面状态写成第二个权威进度。若视图与原文冲突，以原始来源调查并修正映射或派生问题；没有明确结果时不推断通过。

有明确项目约束或用户条件时必须识别并用于对应动作；普通 quick 只处理命中的条件。用户已授权的工作可在读回后继续，面板状态本身不新增审批或阶段。
