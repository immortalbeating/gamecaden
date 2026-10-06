# 原生文档格式 v1：字段、正文与引用

状态：v1 原生文档合同，已用于本地读写工具。既有对象/记录职责继续由 records.md 等共享规则维护；本页定义新原生记录的形态。旧项目不因本合同出现就自动转换，实际能力见[本地工具说明](local-io.md)。

语法来源：[JSON Schema](../schemas/workflow-v1.schema.json)；写作蓝本：[模板目录](../templates/catalog.md)。JSON Schema 检查结构，不能证明目标已实现、报告可信或用户已接受。读写动作见[接口合同](io-v1.md)。

## 1. 文件形态与加载范围

| 对象 | 新原生形态 | 机读内容与正文 |
|---|---|---|
| workspace | workspace.yaml | 定位、来源与规则映射；无执行进度 |
| Task／Quick Task | Markdown＋YAML frontmatter | 同一套六个必需字段；正文说明交付、结果与续接 |
| Epic | Markdown＋frontmatter | id/title/status；正文拥有共同目标与整体出口 |
| Vision、Spec、Roadmap、停车场、Notes、Git 规则 | Markdown | 默认使用可读正文；需要稳定引用的条目加稳定锚点 |
| design/plan/详细历史/交接快照 | Markdown | 依附原工作或原始来源，不增加另一份生命周期；快照不成为当前真源 |
| 独立 Evidence | Markdown＋frontmatter；已有工具报告保留原格式 | 元数据绑定对象与检查范围，方法/观察等写正文 |
| 独立 Decision | Markdown＋frontmatter；批量场景可用同元数据形态的 JSON | events 保存决定及补充/撤回/替代事件，长理由写正文 |
| Asset Ledger | assets/ledger.yaml | 资产身份、候选引用与指定使用；已有 Markdown 台账可继续维护 |
| manifest | 专业工具原生格式优先；缺少时可使用 v1 JSON 备用格式 | 文件身份和技术事实，不含人工接受或运行采用开关 |
| Progress／Timeline／面板数据 | 派生 JSON/Markdown/HTML | 显示来源与生成时点，不成为第二写入源 |

只在需要创建/修改该类原生记录时读取相应 schema 和模板，不让每个 Task 全量加载格式库。模板中的标题是写作提示；没有内容的可选部分删去，不要求填满所有章节或一次生成整棵目录。

YAML 使用 JSON 可表达的值，禁止可执行标签。ID、版本和日期字符串加引号；时间确实未知时保留 null 并说明，不编造日期。原文件的自由正文、无关内容与扩展数据应保留，不能为了格式化清空用户资料。

原生 YAML/JSON 拒绝重复键；原生 YAML 不使用别名、锚点或合并键来隐藏覆盖。外部旧格式保留原文并按适配器处理，不用原生限制擅自清洗其内容。

## 2. 身份、路径与版本

### 稳定身份

新建原生 Task/Epic 默认分配 T-001、E-001；工具需要单独定位 Evidence/Decision 时分配 EV-001、D-001；资产族采用 A-001。编号至少三位显示，超过后自然增长；已存在且合法的较短编号不因格式整理重编号。原生同类数字编号项目内唯一、不复用，保留 cancelled/历史入口参与检查。

已有外部 ID、文件位置和管理者不改写。原生引用通常使用 `{id: "T-001"}`；跨项目增加 project_id，外部或需限定来源时增加 source。解析查实际来源，不能因同名或日期较新选中另一条记录。

Ref 有两种互斥写法：

```yaml
{id: "T-001", fragment: "acceptance-focus"}
{path: "../checks/focus-report.json"}
```

id 指记录身份；path 指已定位文件；fragment 指明确锚点或原生记录子项（如 Decision 的 event_id），不代替版本。对嵌套对象的解析由已声明格式/适配器完成。含 source/project_id 的引用只用于定位，不扩大读取或写入权限。

### 路径基准

- workspace 中的 root/path/marker 相对于 workspace.yaml 所在目录。
- 持久记录中的 Ref.path 与 Markdown 相对链接，相对于承载该引用的文件。
- manifest.files[].path 相对于该 manifest 文件。
- 请求的业务路径相对于 context.base_dir；省略时使用已确认 project_root。context.workspace/base_dir 自身的相对值基于 project_root；Workspace document 的映射值仍基于目标 YAML。工具回传实际位置，不能把当前 shell 目录误当引用基准。
- 外部原生报告沿用生产工具定义的相对基准，由适配器明确转换；未知时返回无法解析。

写入须核对解析后的真实目标、符号链接/目录联接及本次授权范围，不能仅凭字符串前缀或映射拥有者允许越界。

### 内容版本与源文件修订不同

Version 表示被检查/被决定的对象版本，包含 kind/value，必要时以 proof 引用 manifest、构建或其他可核对来源。kind 可为 sha256、git-commit、git-tree、build、named。named 不是“latest”的替代词；应有可定位依据，不把会被覆盖的路径当稳定内容身份。

读写接口的 revision 是承载文件原始字节的 `sha256:<64位hex>`，用于避免旧页面覆盖新写入，不持久存为 Task 的第二个版本计数。文件修订一致不自动说明素材内容一致；素材决定还要核对它实际绑定的内容/manifest 和文件集合。

Version.kind=sha256 固定表示一个具体文件的原始字节摘要，不混用规范化 JSON 或文件集合摘要。给出 proof 时摘要目标是该 proof 定位的文件；没有 proof 时使用 Subject.ref 直接定位的文件，或由明确 candidate_id 绑定的 candidate.manifest。AssetCandidate.version 的摘要目标明确是 candidate.manifest 定位的 manifest 文件本身；该摘要只绑定 manifest 版本，实际内容仍需逐项核对 manifest.files 列出的文件。source revision 和对象 version 即使恰好相同，也必须分别核对它们指的对象。

## 3. workspace 与来源

Workspace schema 保留既定字段：schema_version=1、project、runtime_roots、sources、两个默认工作来源及 rule_sources。

sources 每项包含 id/role/kind/path/owner，可有 scope、format、adapter。format 在本次原生格式中明确为 native-markdown-v1、native-yaml-v1、native-json-v1 或 external；省略的既有映射仍可读取，但工具应报告格式识别结果和实际能力，不默认为可按 v1 改写。

owner 是维护约定，不是权限。adapter 只是适配标识，不保证其已经存在；真正能力由工具检查后返回。旧管理来源无写适配器时返回原文及限制，继续使用其既有流程或先完成获授权移交。

rule_sources 每项用 id/path/scope 定位生效规则，owner 可选。默认任务/专题来源必须指向正确 role；集合可以尚未创建，但已被具体工作引用的缺失记录不能当作空项目。

## 4. Task 与 Epic

Task 必需字段保持 id/title/mode/kind/status/epic 六项。mode 为 quick 或 standard；生命周期只有 planned/active/closed/cancelled；epic 为单个 E-ID 或 null。kind 是开放的工作性质标签，推荐使用 feature、bug、asset、design、validation、maintenance 等，不用它决定验证强度。

可选字段：depends_on、related、extensions。depends_on 每项由 target 与 requires 表达需要哪个结果/条件，可引用 evidence_refs；不是统一要求上游 closed。related 只有关联意义，不赋予推进或关闭权限。Task 的 Epic 归属和外部依赖仍只在 Task 定义一次。

Epic 元数据只有 id/title/status 和可选 related/extensions；子 Task 归属从 Task.epic 汇总。Epic 正文可引用交付、说明分工，但不新增可独立编辑的子任务状态表。

暂停/推进限制和恢复条件继续在 Task 当前续接正文中保存，不增加 paused 生命周期。工具返回这段原文或完整正文供模型判断；正文标题无法可靠识别时返回原文和提示，不能据 active 就得出可执行。面板展示该限制，自动执行不得绕过当前用户指示。

正文仍回答目标/范围、现状/方案、必要安排、验收、实际结果、续接/收尾。Quick 用四答和必要续接即可；独立 plan.md 只拥有 Task 内部实施清单，详尽参数与原报告不复制进主记录。

## 5. Evidence

工具原生报告已经承担记录职责时直接引用，不为了符合本页重复造一份 Evidence。原生独立记录需要 id/title/observed_at/actor/subjects/result/coverage，可有 report_refs、corrects、extensions。

observed_at 表达检查实际发生时间，可用明确日期或时间；未知为 null。actor 不明可为 null，不能补造检查者。subjects 说明对象、适用范围，版本在影响复用、接受或批量判断时必须精确绑定。

result 为 passed/failed/inconclusive/not_run/not_applicable。coverage 表示实际支持的范围；not_run 可以为空，通过必须说明支持了什么。方法、观察、限制和缺口写正文或引用原报告。元数据/正文矛盾需诊断，不能任选一个通过值。

一次检查结果保留历史。重跑或实质纠正使用新记录，corrects 可明确指向原证据；原生工具不无痕改旧结果。仅需说明性勘误时追加更正与依据，不重写当时观察。

## 6. Decision 与批量决定

原生 Decision 使用 id/title/events 和可选 related/extensions。每个事件包括：

- event_id：该 Decision 内唯一的稳定子标识。
- decided_at、recorded_at：实际决定时间（可未知）与记录时间，不能混为同一件事。
- actor：实际决定者，区分 user/agent/tool；记录用户选择时不能把执行记录的模型当成决定者。
- action：choose/accept/reject/revise/defer/waive/withdraw/supersede。
- subjects、scope、conclusion：具体对象/版本、作用范围和真实结论。
- basis、replaces：按需引用依据与被替代事件；原生替代引用应定位到具体 event_id。

已正式使用的事件不可原地覆盖或删除，补充、撤回和替代追加事件；可继续保存在同一文件，不要求每次新建文档。普通局部取舍仍可直接写 Task/Epic 正文，无需套 events。

scope 保留可读说明，subjects 逐项绑定实际版本，批量决定不推定未列出的成员或用途。适配器无法可靠解释范围时返回需判断，不能自动放宽。撤回某用途的接受不自动撤回其他用途，也不自动回退工程。

工具须检查 event_id 唯一，并保留已经生效的事件。replaces 可以跨 Decision 引用，但必须解析到具体已有事件；不能将“替代一个多用途事件”直接理解为所有用途一起失效。针对消费者/用途的局部撤回必须给出对应 Subject.use 或其他可明确解析的相同范围；无法确定时返回 invalid_scope，不自动扩大。全撤回也需明确列出其影响范围。

需要按消费者定位时，Subject 可附 use（runtime_id/consumer/purpose，必要时 baseline），与可读 scope 对照。同一批可以逐项对应不同用途；省略 use 不表示已允许全部消费者。

actor:user 只是数据，不能证明用户真的决定过。decision.record 必须依据真实用户输入、可信面板身份/事件或已采用自动策略；保存者与决定者应能区分。只留一条聊天链接不足以恢复决定含义，conclusion 本身须可理解。

## 7. 内嵌记录与提取

普通局部检查可保持自由 Markdown，偶尔引用可用稳定锚点；不强制分配全局 ID。需要工具独立读取、批量处理或持续引用时，可使用以下显式块，仍不要求拆文件：

````markdown
<!-- workflow:record evidence EV-001 -->
```yaml
id: "EV-001"
# 其余内容与 Evidence frontmatter 相同
```
方法、观察和限制正文。
<!-- workflow:endrecord EV-001 -->
````

Decision 同理，将 evidence 改为 decision，块内使用 Decision 元数据与正文。块不可嵌套，起止 ID 与元数据一致；同一原生 ID 只能有一份当前正文。

提取到独立文件时保留原 ID，并将旧块改为转向，原位置不再保留可编辑完整正文：

````markdown
<!-- workflow:forward EV-001 -->
```yaml
id: "EV-001"
to: {path: "../evidence/EV-001.md"}
```
<!-- workflow:endforward EV-001 -->
````

转向不算第二个证据实体。解析须检查目标 ID 一致、避免循环及多个有效正文；出现冲突时报告，不能按日期挑一份。普通正文中的旧锚点引用仍保留可读去向。

## 8. 资产主台账与 manifest

新原生台账为 schema_version=1 与 assets。每个资产包含 id/title/purpose、candidates、selected_uses，可选来源、替换关系及扩展。

candidate 包含其局部 id、manifest 引用及 Version，可引用来源和 Evidence；同一候选 ID 不用于另一个实质内容版本。manifest 负责逐文件参数与内容摘要，台账只引用其身份，不手抄每文件属性。

selected_uses 每项包含 use_id、purpose、runtime_id、consumer、candidate_id，可加 baseline、Decision/Evidence 引用。它表达指定选用；没有 approved、adopted、official 或统一 current_version 开关。真实采用由工程和适用 Evidence 对照，未能观察时显示未知，不能从台账推断成功。

默认 manifest 备用格式包含 asset_id/candidate_id/files，每个文件给出相对 path、sha256、role，可有 technical 属性；专业工具已有等效格式时直接用适配器，不重抄。检查内容版本时必须核对需要证明的实际文件集合，不能仅检审批 JSON 自己的 hash。

候选可先登记而没有 selected_uses；选择依赖的消费者或用途未明确时不造空假关系。仅在有实际独立追踪需要时建立台账条目，不为每帧、每条临时输出都建身份。

## 9. 格式验证与语义判断

JSON Schema 能检查类型、必需字段和已定义枚举；以下还需解析器/工具或调用 Skill 核对：ID 唯一与不复用、引用是否解析、默认来源是否匹配、依赖条件、同一事实拥有者、决定事件不可覆盖、候选版本身份、写入范围、证据有效性及关闭承诺。

未知的原生字段放入有明确用途的 extensions；旧格式/未来版本的未知内容读取时保留。无法可靠修改时报告只读/需适配，不能丢弃字段后宣称升级成功。

通过 schema 只说明形态有效。实际读写/恢复由本地工具另行验证，当前支持范围见其说明；schema、模板或本地测试都不证明面板桥接、引擎适配和宿主安装已经完成。
