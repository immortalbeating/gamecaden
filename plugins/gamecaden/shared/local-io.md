# 本地读写工具：调用与恢复

当前实现提供 Python 库和命令行入口，使用 [v1 接口合同](io-v1.md)中的 14 个操作。[第十四步的本机 HTTP 宿主](../panels/README.md)已复用同一库，按独立启动配置提供受控面板接入；未自动修改 Codex 宿主配置，也未安装 MCP 服务。

材料、条件和关系的派生读取另由 [workflow_governance.py](../scripts/workflow_governance.py) 提供；它不是第十五个核心写入操作，不维护新的业务状态。字段、CLI 与面板用法见 [governance](governance.md) 和[面板衔接](panel-workflow.md)。

## 1. 环境与调用

入口为 [workflow_io.py](../scripts/workflow_io.py)，依赖见 [requirements.txt](../scripts/requirements.txt)。使用 Python 3.12+；本轮在 Windows、Python 3.14.5 上执行验证。依赖放在调用者选定的工具环境，沿用已有可用环境即可，不向游戏工程复制一个运行时。

```powershell
& $python -m pip install -r "$bundle/scripts/requirements.txt"
& $python "$bundle/scripts/workflow_io.py" --project-root $gameRoot --request $requestFile
```

这里 `$python` 是实际 Python 可执行文件，`$bundle` 是本包路径，`$gameRoot` 是已确认的项目根，`$requestFile` 是填写真实上下文的 UTF-8 JSON。可用 `--request -` 从 stdin 输入。成功退出码为 0；拒绝、冲突或未完成为 2，stdout 返回 JSON。

项目根由宿主参数绑定，请求里的 context 不能扩大它。context.project_root 使用绝对路径；context.workspace 与 base_dir 的相对值基于项目根解析。业务 payload/Ref 路径基于 base_dir；省略 base_dir 时使用项目根。Workspace document 本身的映射路径始终基于目标 workspace.yaml，正文/无结构元数据的相对路径由调用者按目标文档准备。

示例请求：

```json
{
  "protocol_version": 1,
  "request_id": "read-current-task",
  "operation": "record.read",
  "context": {"project_root": "C:/Games/MyGame"},
  "payload": {"target": {"id": "T-002"}}
}
```

示例中的根、ID 都应替换为已定位项目的真实值。examples/v1/io 中的 C:/ExampleGame 是格式样例，不是本机执行目标。JSON 语法错误、非对象顶层或无法识别的请求信封返回简短 invalid_request/error 结果，不伪装成某个合法操作的成功响应。

## 2. 实际能力

| 操作组 | 本地实现 |
|---|---|
| workspace.inspect/configure | 识别已有映射、原生默认位置、来源与缺口；条件保存映射，保留 YAML 注释 |
| record.list/read/resolve | 原生记录/内嵌记录/转向、原文读取、绝对位置与引用基准、分页及变化检测 |
| record.create/update/transition | 稳定编号、少量元数据/正文、附属文档、生命周期及理由记录；身份/正式记录保护 |
| record.extract | 目标先写入，源后转向；相对引用重定位、中断回读和明确冲突修复 |
| decision.record | 独立/内嵌创建、事件追加、真实来源校验入口、跨 Decision 替代和局部撤回范围检查 |
| asset.upsert/select | 身份/候选登记、set/clear 指定关系；校验备用 manifest 和实际成员字节 |
| view.build | Progress/Timeline/Assets 的 JSON 读模型，可保存至原有或指定位置；不推断通过百分比或运行采用 |
| operation.status | 读取原操作回执及可观察的恢复情况，不写原文档 |

原生 Markdown/YAML/JSON 及 UTF-8（包括 BOM、CRLF）已实现。修改保留未改动的正文和 YAML 注释；新增结构用序列化器处理。二进制对象可以按路径绑定摘要，正文为 null，不被误当文本解码。

旧格式无适配器时按原文只读。来源声明为原生但损坏时返回具体格式错误。既有 sources 的外部归属、重叠解释或限定来源不能被绕过；字段 `owner` 不是操作授权。

尚未建立 workspace 时，明确交付可以使用原生默认 Task 集合。已有映射后新增一类尚未登记的文档/资产台账时，工具可以在未被其他来源占用的新位置创建，并返回 `source_registration_required` 和可用的 `source_proposal`；init 随后用 workspace.configure 保存明确的映射。创建不会暗中改变默认来源；登记前不能假定新 ID 已进入已有来源列表。提取则要求目标已有可用原生来源，保持原 ID 可解析。

## 3. 正常写入

1. 从 record.read/resolve 取得真实承载路径、reference_base、源文件 revision 和当前正文。
2. 保留用户本次范围和不相关内容，准备指定操作。更新/显式创建目标分别提供匹配 revision 或 null（期望不存在）。
3. 需要当前对象一致性时附 expected_subjects。recorded_at 由实际写入准备过程生成；决策本身的发生时间未知仍可保留 null。
4. 同一次逻辑请求保持 request_id 和载荷。核对 response.status、逐文件 writes、receipt 和错误；按原 Skill 规则更新当前工作中的实际结果。

同一文件中的短记录、独立记录和 Quick/standard 都走相同保护边界。record.update 也检查所承载的正式内嵌块，不能借全量正文替换绕过专门动作。source_revision 与检查对象 Version 分别核对。

在原生Task/Epic集合内创建无frontmatter的design/plan/history附件时，当前读取器按文件stem识别类型。阶段名称放在目录，如 `tasks/T-002/m0/design.md`、`m0/plan.md`；`m0-design.md`这类未支持名称不能由record_type代替持久识别。创建会在写入前按实际来源的读取规则校验，无法回读时返回invalid_record且不写目标，不再留下阻断后续编号的文件。已有不支持附件需保留原字节后移到支持位置或明确登记合适来源，不把缺少frontmatter的真实Task当普通附件放行。

当前自动内容验证支持单文件 SHA-256，以及本包备用 manifest 中每个实际成员的 SHA-256；候选 Subject 可从其已绑定 candidate.manifest 得到隐含 proof。其他生产工具 manifest、git/build/named 的当前适用性需要对应适配器，当前请求会明确返回 unsupported_format，不把未解析的版本当作通过。已有历史记录仍可保存这些声明，不因此虚构当前验证。

## 4. 决定者与接受来源

CLI 的默认记录者为 agent/local-cli，`--actor-id` 可标识实际 Agent。它可以记录该 Agent 负责的决定；不能靠 payload 的 actor:user 冒充用户选择。

Python 调用方可用 `Workflow(project_root, actor=..., decision_authorizer=...)` 提供可信宿主身份与回调。回调接收完整事件和请求，必须核对实际用户输入/宿主事件及精确对象；回调不由请求 JSON 选择。已知用户决定无需再次请求同义批准。

本轮测试校验了拒绝伪造归因和明确宿主回调两条路径。后续面板提供了[本机启动会话绑定](panel-bridge-v1.md)，不会将它声称为 Codex 账号认证或真人证明。CLI 的身份界限保持不变。已有会话的决定仍可按原工作流规则保存。

## 5. 重试、中断与冲突

项目内 `.game-workflow-io/` 保存锁和操作回执，不保存第二份 Task 状态。回执中包含原请求和恢复材料，应留在本机操作环境；发行/项目接入时按项目约定排除打包和版本控制。工具本身不修改 .gitignore 或执行 Git。

- 请求结果未知：先 operation.status；需要继续且条件仍成立时重发原 request_id 和原载荷。
- 相同请求再次到达：复用原编号和结果。相同 ID 换载荷：request_id_conflict，原结果另查。
- 多文件仅完成一部分：回执逐项说明，恢复核对实际文件，不重新创建 Task 或清空已有结果。
- 原操作确认遇到外部修改：保留外部内容，结束该次冲突尝试；使用新 revision 和新请求表达已重新核对的修改。
- 提取在目标已写后遇到源文件外部修改：原回执为 settled/partial。新的 record.extract 提供 `recovery_of`、源路径/原内嵌 ID、原目标以及两者的新 revision；仅复用同一原操作、同一 ID、内容一致的目标，再切换源为 forward。

`written` 表示有本操作的已核实写入依据。崩溃后仅观察到目标字节、无法确认写入归属时，返回 unchanged 并用 note 说明；不会把外部恰好写出的相同内容算作本操作写入。已有 written 结果被外部恢复或改动时，未结算操作查询会标出冲突，重放保留该变化。

settled 回执说明原操作当时的结果；需要现在的内容时另读原文档。未结算操作会结合现场给出恢复观察。清理回执可能失去重试去重和编号保留依据，因此未决操作先恢复；普通清理/迁移需遵守已有范围和留存需要。

## 6. 验证范围与实用边界

项目级 OS 锁协调本工具的多个进程，退出后由 OS 释放。源文件采用写前修订比较、临时文件、替换和回读；恢复保留原分配及逐文件结果。Windows 目录联接和符号链接入口当前拒绝，需要实际受支持的适配方式。

这些保障针对本地协作调用。外部编辑器不参加项目锁；工具检测可观察的版本变化，不能把任意非合作编辑器纳入同一文件事务。本轮没有验证断电、网络盘或跨机器写入。

JSON views 保留来源、原文、时间和诊断。raw 源无法完整枚举结构化记录时 complete=false；重复 ID 和未结算操作是另外的诊断，不一概改变扫描完整性。分页是否还有内容看 next_cursor。Timeline 当前提供带来源的记录/事件材料，正文中的任意历史叙述不伪造为精确时间线。

工具不执行引擎、素材生成或 Git 交付，也不替代 verify/close 的实际判断。开发测试见维护仓库的 [test_workflow_io.py](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/tests/test_workflow_io.py)；包内纯合同检查为 [check_contracts.py](../scripts/check_contracts.py)。
