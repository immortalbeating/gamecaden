# 本地面板桥接 v1

本层把浏览器接到现有 Workflow 库。源记录仍由原文件拥有；HTTP 会话、签名快照和恢复请求只是操作材料。

## 启动与身份

启动方注册项目根、原生 workspace 或明确的旧格式文件清单、允许的写动作和记录者身份。浏览器不能提交另一个根、actor 或授权范围。

默认只读。开启写入时仍分别控制 Task 正文、决定、既有资产用途选择。记录者可为 agent/tool；user 类型必须通过桥接中的可信宿主回调。这里实现的是**本机启动会话绑定**：它不等于 Codex/ChatGPT 账号认证，也不识别操作者是否真人。自动化验证使用 tool 身份；不得把自动化点击归因为真实用户接受。

仅绑定 127.0.0.1。一次启动口令在 URL fragment 中交给页面，页面立即移除 fragment 并换取 HttpOnly / SameSite cookie 与 CSRF 令牌。HTTP 校验精确 Host / Origin，私有数据与媒体均要求会话，写请求另验 CSRF。不开放任意文件或通用命令执行。

## 只读接口

- GET /api/session：当前会话、宿主绑定的身份、项目与能力。
- GET /api/projects/<id>/snapshot：原生记录分页或明确旧格式来源清单。
- GET /api/projects/<id>/governance?focus=T-003：从已登记来源派生只读成果关系、材料职责和条件；focus 仅定位当前对象，不缩减原图。语义见[治理合同](governance.md)。
- GET /api/projects/<id>/records/<key>：原文、元数据、revision、格式和能力。
- GET /api/projects/<id>/candidates/<key>/<candidate>：manifest 技术校验、候选级用途与可预览媒体。
- GET /api/projects/<id>/media/<key>：注册过的安全媒体，按当前字节与已登记摘要核对。

key 是服务端由已知记录/文件推导的标识，不是浏览器任意路径。旧格式只读，并不因此复制一个新的 Task 状态。自由正文按原文展示，不从“通过”一词猜测验收或整体进度。

同一派生模型也可由 `scripts/workflow_governance.py --project-root ... [--workspace ...] --focus T-003` 只读取得。总览展示当前 Task、成果树、[材料职责](material-requirements.md)、条件性质/状态/证明与一跳关系；资料原文仍在独立页面。深链接定位和复制续接摘要见[面板衔接](panel-workflow.md)，它们不保存新的权威状态或唤醒 Agent。

## 写入协议

准备操作返回带签名的快照 ticket。它绑定项目、身份、来源 revision、精确对象/版本/用途；准备不写业务文件。提交必须携带 ticket 与稳定 request_id。

- POST .../task/prepare {key, revision} → ticket；.../task/save {ticket, request_id, body} → record.update。
- POST .../review/prepare {asset_key, candidate_id, expected_revision, expected_version, scope, use_id} → ticket；.../review/commit {ticket, request_id, conclusion, note} → decision.record。
- POST .../selection/prepare：同样绑定候选与既有 use_id；.../selection/commit → asset.select。
- POST .../operation/status {request_id} → 原库 operation.status。

决定按成员独立保存，每项有自己的 request_id 和精确范围。浏览器汇总逐项回执，不发明新的核心 batch operation。结论仅允许 accept/revise/reject；defer 留在草稿。事件由宿主赋 actor，expected_subjects 与文件前置条件同时核对。指定新候选到已有用途时，不沿用旧候选的接受/证据引用。

请求冻结后的 ticket、载荷和 request_id 可以在同项目浏览器草稿中保存以恢复传输；这些数据不代表业务成功。重试必须原样发送，结果未知先查原请求。若源已变化，保留草稿，重新读取并明确准备新操作；不自动替换 expected_revision 或升级为 latest。

## 返回与限制

实际写入返回原 Workflow response（含 status/writes/errors/receipt），并尽可能另取当前原记录。只有实际写入/回读支持成功结论；技术校验、接受、指定用途、运行采用继续分别显示。

本层不关闭任务、不执行引擎、不自动继续 Agent，不改变 Git 策略。专业媒体编辑器和账号级宿主登录属于后续适配。

## 宿主来源核对

已核对 [Codex App Server 官方文档](https://learn.chatgpt.com/docs/app-server) 和 [插件认证文档](https://developers.openai.com/plugins/build/auth)。App Server 的账号认证、传输认证与命令/文件审批有各自用途；我们没有将账号登录或命令批准当作本游戏资产的接受决定。本阶段采用上述本机可信启动方模型，后续可由实际宿主替换该绑定。
