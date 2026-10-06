# 读写接口 v1：来源、预期版本与回读

状态：与 formats-v1 配套的本地接口合同。14 个操作已由 Python 库/CLI 实现，调用方法、能力范围和恢复方式见[本地读写工具](local-io.md)。这些名称是 JSON operation，不代表当前宿主已安装同名 MCP 工具；面板/宿主接入分别验证。

## 1. 同一来源，不同读取表面

持久文档形态见[格式合同](formats-v1.md)。接口读取源文件并返回可读正文、必要结构、引用和源文件 revision；前端/模型消费同一结果。规范化读模型是派生数据，不反写成另一个 task.json、审批状态表或当前 Git 数据库。

读取结果应说明实际位置、记录 ID/来源、识别格式、可用能力、revision 与限制。未知旧格式可返回原文与诊断；没有写适配器时明确不支持写入。owner 标签和 adapter 名称不自动授予权限或证明能力存在。

record.read/resolve 的成功数据为 ref/path/reference_base/format/interpretation/revision/metadata/body/capabilities/diagnostics；interpretation 区分原生、适配和仅原文读取。ref 返回规范身份；没有可解析 ID 的外部原文使用已解析绝对 path，不回显一个基准不明的相对路径。path 是真实承载文件，reference_base 是返回元数据/正文中结构化引用的基准，外部格式无法确定时为 null。capabilities 表示实际实现支持的操作，不代表本次授权。列表项的 metadata 也声明 reference_base。列表返回 items、next_cursor、complete、source_revisions 与诊断；complete 表示来源扫描是否完整，仍有 next_cursor 时尚未读完结果。翻页遇到来源变化返回 stale_cursor 或明确的新快照，不能悄悄漏掉记录。

调用对象总是已有来源或获准创建的位置。先核对上下文的 project_root/workspace/base_dir 与当前真实授权目标，再解析引用；用户提交的路径、source 或 actor 字段不会扩大权限。

请求中结构化 Ref.path 按 context.base_dir 解析；写入目标文件时，工具需转换为相对于目标文件的持久引用。读取的元数据若原样回传，调用者可把 base_dir 设为原记录目录。正文 Markdown/原生块由调用者按目标文件基准准备并校验，不能将另一文件的相对链接盲目粘贴。路径转换不改变指向对象，也不放宽越界限制。

context.project_root 为绝对根；context.workspace/base_dir 的相对值以该根解析。Workspace document 自身的 root/path/marker 仍以目标 workspace.yaml 目录为基准。未定义结构的正文/扩展数据不凭 {path: ...} 的外形猜作 Ref。

complete 表示声明来源中的记录是否已完成结构枚举；raw 源缺少结构适配时不能证明这一点。重复身份或未结算操作等诊断单独返回，不一概代表扫描没有完成。读取者仍需处理这些诊断，不能仅凭 complete 推进或关闭。

## 2. 请求与结果信封

Request schema 包含 protocol_version=1、request_id、operation、context、payload；写操作还必须明确 preconditions，需要时附 expected_subjects。

request_id 对同一次逻辑写入同时作为重试键。重试相同请求使用相同 ID；同一 ID 对不同内容返回冲突，不能覆盖原操作。已确定失败后有意修改请求，应使用新 ID；结果未知时先查询原操作，不直接换 ID 重做。

request_id_conflict 响应不附 receipt，避免将旧请求成功回执误认作本次不同内容已生效；只返回冲突与本次未写入事实。需要了解旧请求时显式调用 operation.status，它返回原摘要与原结果。

幂等索引按实际授权项目/写入范围的 scope_id 与 request_id 定位，scope_id 由服务端解析真实绑定，不接受客户端自封权限。保存规范化请求的 SHA-256：排除 request_id，对解析后的 JSON 使用 UTF-8、对象 key 排序、紧凑分隔、保留数组顺序、拒绝 NaN/Infinity；v1 自检用 json.dumps(ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) 作为固定计算方式。摘要包含 operation、context、preconditions、expected_subjects 和 payload；客户端无需自算授权摘要。请求内容改变不能沿用旧 ID。

preconditions 绑定即将读改写的实际源文件 revision。expected_revision:null 只表示期望该目标不存在，不能当作跳过检查。更新既有源必须提供对应 revision；多文件操作须覆盖各个会变化的来源。新 ID/路径由工具分配时，工具在锁定范围内检查最终目标不存在，客户端不能凭空预先声称创建成功。

expected_subjects 额外绑定当前审阅/选择的对象版本与范围，解决“源记录没变但媒体变了”的问题。记录真实历史决定时保留其原对象；它不自动获得当前候选适用性。不能满足指定版本时返回 version_mismatch，不能偷偷改为 latest。

Response 保留 request_id/operation，status 为 ok/conflict/rejected/partial/indeterminate，并返回实际 data、writes、errors，必要时标明 replayed。这些是操作结果，不是 Task 生命周期或产品验收结果。

每项 writes 指明对象、written/unchanged/failed/not_attempted 与可确认的前后 revision。返回 ok 前要完成实际写入和回读；仅生成提案或在浏览器保存草稿不得返回权威写入成功。

WriteResult 可用 note 说明恢复观察。仅看到当前字节与目标相同而缺少已核实的写入记录时，使用 unchanged，不声称知道写入者；原 written 结果被外部改回/改成其他内容时，未结算操作报告冲突并保留该变化。

响应中用于操作定位的 path（含 writes、errors、source_revisions、allocations 和 recovery_actions 的路径引用）返回已解析绝对路径，不依赖接收者当前目录或 operation.status 查询时的新 base_dir。读取结果内的原文/元数据仍沿用声明的 reference_base；两者不可混用。

写操作的 ok/partial 结果及 operation.status 的成功查询还须返回 receipt：原 request_id/operation、scope_id、request_digest、prepared/applying/settled 阶段、outcome、已分配对象和 recovery_actions。它描述一次文件操作，不成为业务流程状态。operation.status 的 writes 表示被查询原操作的写入结果，不表示查询本身写了文件；receipt 中的原 request_id 与查询请求 ID 分开。

allocations 只列分配稳定管理 ID 的 Task/Epic/Evidence/Decision/Asset。无独立管理 ID 的 design/plan/history/handoff 等文件创建由 writes 指明实际位置，不借回执增设管理实体。

## 3. 操作目录

| 操作 | 输入与责任 | 成功能说明什么 |
|---|---|---|
| workspace.inspect | 检查指定根、入口、来源、格式和能力；不要求已存在 workspace | 返回定位和缺口，不初始化或迁移 |
| workspace.configure | 保存获授权映射，引用已有正文；核对默认源/重复源/规则范围 | 映射已写回，不证明游戏已就绪 |
| record.list/read/resolve | 按范围读取原记录或明确转向；返回正文、元数据、revision | 真实来源可读取，未知处有说明 |
| record.create | 按对象格式在合法位置创建，分配或核对身份；支持原生内嵌 Evidence | 新记录确已存在，不证明其业务结论成立 |
| record.update | 编辑允许的元数据/正文，保留身份和无关内容 | 指定变更已保存，不默认转换状态或旧格式 |
| record.transition | 只处理 Task/Epic 的生命周期，含具体理由及相关记录引用 | 状态按该次请求保存，不自证验收或父项完成 |
| record.extract | 将可机读内嵌记录提取到独立文件，保留 ID 与旧位置转向 | 已完成指定迁出；部分失败单独返回 |
| decision.record | 新建 Decision 或向同一记录追加正式事件；可独立或内嵌 | 真实决定被记录，不能据此推断工程采用 |
| asset.upsert | 明确 create/update，维护资产身份、来源与候选索引，保留既有选用关系 | 登记真实变化，不生成素材或批量接受 |
| asset.select | set 指定或替换某 use_id 的关系；clear 撤销该指定；保存理由与依据 | 指定关系已保存，不改接受或消费者引用 |
| view.build | 根据实际源构建进度/历史/资产读模型；可选保存视图 | 返回或保存派生结果，不产生新事实 |
| operation.status | 按原 request_id 查已发生写入、部分结果和恢复条件 | 说明操作结果，不将回执当 Task 真源 |

record.update 不改原生 ID，不绕过 record.transition 修改 Task/Epic 状态，也不覆盖已使用的 Decision 事件或 Evidence 结果。草稿正文可以修改；正式事件的更正/替代遵守对应记录规则。明确格式移交仍属于 init/migrate，不藏在 update 中。

改写承载文件正文（含 record.update/transition）时，同样核对其中的原生内嵌块，不能借整段替换删除正式事件、改变 Evidence 的实质对象/结果或重新分配身份。格式/基准转换属于保持含义的搬移；实质证据纠正另建记录并引用原记录。record.create 分配缺省 ID 后仍须按目标记录格式校验完整元数据，Request 信封通过本身不足以证明可保存。

record.create 也可以创建 design/plan/history/handoff 文档；前几类必须定位 owner，handoff 明确原始来源与快照范围。它们是附属文档类型，不新增管理实体或生命周期。正文拆分可组合受保护的 create/update，遵循先准备目标、再切换原正文为说明/引用、逐项回读的同一恢复原则；不能仅创建一份副本就宣称迁出完成。

所有写操作在任何权威源文件改动前，重新解析实际目标与来源并核对当前写能力、格式与授权。不能信任请求自行声称 capabilities；raw/缺少对应写适配器时返回 unsupported_write，各目标为 not_attempted。读取之后来源发生迁移/变化时，需要重新核对真实位置和写入前提，不把旧正文盲写到另一个来源。操作锁/回执属于本地恢复材料，不等于已写入权威源。

新建未被既有来源占用的文档/台账后，若还未登记其来源，结果标明 source_registration_required，必要时返回 source_proposal；init 再以 workspace.configure 保存映射。创建不隐式改默认来源，登记前也不宣称新 ID 已在现有来源中可解析。

decision.record 的 targets/subjects 必须对应本次真实决定，记录时间由写入事实确定，实际决定时间未知则保留未知。面板身份与用户输入需由实际宿主核对，客户端填写 actor:user 不等于人工批准。已有决定直接记录时也不额外要求用户再批准同一个选择。

asset.upsert 的 create 可以省略 id，由工具分配并回传；提供的 ID 必须未占用，新建 selected_uses 必须为空。update 必须指定既有 id，selected_uses 须与已有值一致；指定关系只由 asset.select 在其范围内维护。候选 ID 不复用为不同实质内容，旧版本保留其引用。实际生成、加工、引擎接线与 Git 操作使用其专门能力，并将结果写回这些已有来源，不通过本接口假装执行。

asset.select 明确 action=set/clear。set 提供完整 use（含 use_id）；clear 只提供已存在的 use_id，并移除当前指定关系。两者均需 reason，必要时附 basis 引用真实决定/工作；原工作保存影响与历史去向。clear 不删除资产/候选，不撤销原接受，也不回退已经发生的工程接入。

Task 转换前，调用 Skill 核对原范围、有效证据、必要接受与 Git 落点。工具核对结构、引用和操作允许范围；它不能仅凭 status 字段或 JSON Schema 通过，代替 close 的交付判断。

view.build 只返回数据时 preconditions 可为空；保存时需保护实际输出目标。没有可靠的正文解析/引擎观察时保留原文或 unknown/needs_review，不能从 closed 数量推导 Epic 完成或从素材数量推导质量。

## 4. 编号、并发和写入顺序

创建原生 ID 时在实际项目的同类 ID 空间中检查活动、取消及保留历史记录；生成时默认至少三位。编号分配与新文件创建需要协同保护，单靠不同文件名的 create-exclusive 不能防止两个 T-001。同一请求重试不得再分配第二个 ID。

正式写入之前先将请求摘要、绑定范围、分配结果和将写目标保存为 prepared 回执；只有回执可恢复后才应用文件写入。回执更新为 applying/settled 时保留每个目标的实际结果。相同请求查到已有分配时复用它，不能再取下一个编号。没有持久分配/恢复保证的实现不得宣称提供了幂等创建。

写前检查源 revision 与目标语义，写后回读；同文件冲突返回 conflict 及当前定位信息，保留用户原提交内容供重新比较。不能自动把旧页面值套到新版并当作同一次批准。

单文件可以使用同目录暂存与适用的原子替换方式；保留有效编码/换行、元数据及无关正文。原子替换不等于版本检查，读取与提交间仍需适当锁定/一致性保护。

多文件不宣称天然原子事务。record.extract 等操作应先准备可恢复内容，按真实写入逐项回读，再完成转向；中断时报告已完成、未完成与下一步。读到正在提交或冲突的记录时，返回明确限制，不能用时间较新的一份猜“真源”。

record.extract 必须保护源承载文件和目标文件（新目标为期望不存在），并在 prepared 回执中绑定两者。先准备同 ID 的目标内容及正确的新相对引用，目标写入并回读后，才将原块替换为 forward，再核对唯一正文/转向。禁止先删源正文再尝试写目标。中断时 receipt.recovery_actions 应指明 read_back、finish_extract 或冲突检查及具体对象；发现临时双正文时读取器报 operation_pending/歧义，不将两份都计为有效记录。

外部修改使原尝试明确无法按旧前提继续时，保留其逐项结果并结算为 conflict/partial。提取恢复可用新请求的 payload.recovery_of 引用已结算的 partial 提取，提供源和既有目标的新 revision；仅同一来源/目标/ID且目标内容一致时复用，不覆盖目标差异。这样保留用户新增正文，也不要求删除已生成的合法目标。

提取时重定位结构化 Ref 和可识别 Markdown 相对链接；无法可靠转换的正文引用须保留其原基准或交由调用者准备，不能只搬文件让同一链接改指其他内容。

实现可以保留锁、暂存和 request_id 回执等操作元数据；它们只用于并发和恢复，不拥有 Task 状态、人工接受或运行采用。清理未决操作材料前必须解决其结果；权威事实仍从原文档读。

自动重试仅在原授权内且源/对象条件仍成立时进行。发生冲突先读新状态和差异，决定是否重新提交；不能用无条件覆盖、重新编号或删除他人改动绕过。

## 5. 模型如何使用自由正文

模板提供推荐结构，但格式不要求所有 Task 使用相同章节标题。读取器可以返回已识别段落；无法稳定定位时返回完整正文。更新请求应保留不属于本次改动的段落和可选扩展，不按标题猜测并删掉其他内容。

需要独立寻址的条目用明确锚点或原生记录块。普通 Task 的推进限制、下一步和已发生结果可以保持文字；工具不能在未理解这些条件时仅依据 active 自动执行。

与语义有关的缺口由模型依据原始资料判断，必要时澄清；结构错误由工具返回具体字段/引用问题。不要把所有风险或模糊文字都升级为新全局字段、额外审批或一个总状态文件。

## 6. 错误与恢复输出

至少区分：not_found、ambiguous_ref、duplicate_id、unsupported_format、unsupported_write、invalid_record、invalid_transition、invalid_scope、precondition_required、revision_conflict、version_mismatch、permission_denied、request_id_conflict、stale_cursor、operation_pending、write_failed、partial_write、indeterminate。

错误说明受影响对象、已发生部分、当前可核实状态和下一步。缺少工具、缺少记录和原记录格式不同是不同情况；不能统一显示成“项目未初始化”。

操作结果不明时用 operation.status/实际源核对。回执不可用不代表没写过；若无法确定是否重放安全，先保留现场和明确缺口。已经完成且仍有效的其他结果继续使用，不重做整项工作。

## 7. 实现与验证边界

本地实现和可执行检查已提供，支持范围以[工具说明](local-io.md)为准。实际测试与纯 schema 检查分开记录；本地 CLI 验证不证明引擎消费者、浏览器/宿主用户身份、网络服务或插件安装已经完成。
