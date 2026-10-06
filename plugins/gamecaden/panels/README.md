# Gamecaden 面板与本地宿主

工作流名称为 **Gamecaden**，当前界面采用用户选择的“墨夜放映室”方向。它是共享面板，不是第九个职责 Skill；插件入口为 `gamecaden:flow` 等八个职责，安装与版本恢复见 [安装说明](../INSTALL.md)。维护背景见[项目 README](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/README.md)。

## 启动

使用已有 Python 3.12+ 环境，安装 scripts/requirements.txt 中的依赖。先为宿主准备项目清单，格式见 [host-config.example.json](host-config.example.json)。

```powershell
& $python "$bundle/scripts/workflow_panel_server.py" --config $hostConfig --state-dir $hostState --port 8875
```

- $hostState 是该启动方专用的本机操作目录，放在游戏业务文档之外。
- 新连接保存在 $hostState/private/connection.json。用其中完整 URL 打开浏览器；一次性口令会立即从地址栏移除。已连接浏览器可直接刷新。
- 默认只读。写入分别开启 Task 正文、决定记录、既有资产用途指定；启动方绑定 actor，页面不能填写身份。
- 当前实验配置只对隔离工程开放写入。旧格式项目的已登记来源保持原格式只读。
- 服务只监听 127.0.0.1；关闭启动进程即可停止。重启使用相同 state-dir 保留快照签名能力，重新获取连接。
- 默认端口 8875；启动失败时选择明确的新端口。跨端口浏览器草稿不共享，恢复优先复用原端口。

启动配置中的 root、workspace、external_sources 和写能力均由可信宿主设置。它们不是页面 API，也不能通过 URL 任意改项目根。示例配置默认无写权限，绝不把示例 root 当真实目录。

## 页面提供什么

| 页面 | 内容与操作 |
|---|---|
| 项目总览 | 成果/里程碑/Epic/Task 树、当前 Task 与候选、材料矩阵和条件表；关系区可切换推进条件／规范来源，显示声明前提组合、职责、状态与证明，支持流程选择、范围、折叠、缩放及原文回链；可复制带来源版本的续接摘要 |
| 资料与原文 | 独立的来源列表、筛选、原文/元数据和 revision；可按已登记清单阅读旧格式，获准时条件保存原生 Task 正文 |
| 资产管理 | 资产族图库、候选大图、并排比较、manifest 和文件校验、用途、图片/音频/视频预览；可为既有用途指定候选 |
| 批量审阅与恢复 | 当前候选大图与方面/用途/意见表单、底部成员队列和提交托盘；逐项决定写入与回执，保留失败草稿、核对新版、恢复原请求 |

Task/Epic 的状态来自原记录。任意 Markdown 正文不被推断成完成百分比。部分来源扫描有诊断；页面记录数只表示当前登记范围。

关系区使用原来源的可选 flows / relationships 定义，语义见[关系视图](../shared/relation-views.md)。规范来源默认打开“项目领域”：先看折叠的领域概览，展开领域和文档收录内容后阅读真实来源。“来源与影响”沿用同一批原节点与关系，两种来源视角均可切换横纵排版。进入领域默认打开文档树阅读器（用户所说的领域内部工作树）：左侧是真实文档收录树，右侧是所选文档实际章节正文，可切换焦点关系图查看所选来源的直接关系。原文、治理 id 与原始关系逐项跳转继续保留。点击领域可聚焦，保留直接相连的一跳外部端点；返回恢复该项目同一页面会话的视角、展开、缩放与画布位置。侧栏展示职责、章节目录、原治理条目及原始关系逐项，原文按钮定位正文标题或治理 id；同名多处或当前版本缺失时提示核对。

没有 navigation 时仍保留已读来源、未分类资料和孤立文档，不强制补满标注；没有声明流程时明确提示缺口。原文入口只使用已登记来源，窄屏改为领域/文档/步骤列表并保留完整详情。登记范围不代表全部项目完整性。当前阅读器与刷新范围见[设计](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/panel.md)与[核验](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/validation.md)；[领域概览设计](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/panel.md)与[领域核验](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/validation.md)、早前[关系设计](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/panel.md)与[验证](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/validation.md)保留历史范围。

总览的 `GET /api/projects/<id>/governance?focus=T-003` 是只读派生视图；命令行可用 `scripts/workflow_governance.py --project-root ... [--workspace ...] --focus T-003` 读取同一模型。材料 `located` 只表示已定位来源；条件状态和证明不能替代语义核验或授权。旧来源未识别治理定义时明确显示缺口，不推断全部通过。详情见[治理合同](../shared/governance.md)、[材料职责](../shared/material-requirements.md)与[面板续接](../shared/panel-workflow.md)。

已连接页面可用 `#project=<id>&view=overview|assets|review|documents&task=T-003&asset=A-002&candidate=C-001` 定位当前对象；只带实际需要的参数。关系视图参数可加 `diagram=sources|progress`、`lens=domains|impact` 和 `layout=DOWN|RIGHT`，分别选择规范来源/推进条件、项目领域/来源与影响、纵向/横向；例如 `#project=<id>&view=overview&diagram=sources&lens=domains&layout=RIGHT`。选择、章节、展开、缩放、阅读和画布位置在当前会话按项目 binding 隔离，面板刷新与项目切回保留仍有效的对象；来源删除或身份变化时需重新定位。不承诺浏览器整页重载恢复这些阅读设置。`connect=` 仍是一次连接口令，不放入工作深链接。复制的续接摘要包含来源/版本线索，Agent 继续前须重读原记录和现场；面板不运行引擎或自动唤醒 Agent。

资产的技术检查、决定、用途指定和实际运行采用仍各有归属。换候选时，旧用途的决定/证据引用不自动沿用。预览是静态参考或媒体播放，不能代替引擎内效果和玩法验收。当前没有帧编辑、地图生成器或模型编辑器。

总览先提供当前工作入口，资料页可进入同一来源的章节阅读器。候选比较可选择任一已登记备选；预览读取失败提供就地重试。审阅的完整候选版本与账本 Revision 收在“版本依据”中，队列缩略图仅复用两者均与草稿相符的已读缓存；选择成员仍重新读取当前候选，来源变化不自动升级草稿基准。延期只保留本地草稿，不准备写回；窄屏“填写意见”直接定位表单。本轮范围与验证见[Gemini 评估及修复](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/validation.md)。

## 来源更新与阅读恢复

`GET /api/projects/<id>/revisions` 只检查已登记物理来源及映射的内容版本，返回稳定 digest、source_revisions、mapping_revision、complete 和 diagnostics；不解析逐条记录或派生治理。只有 `complete === true` 且 digest 非空才比较。未登记文件及 runtime roots 不纳入检查，digest 不是批准、记录语义有效性或工程运行的证明。缺失、读取失败或检查期间变化保留诊断，不视为没有更新。

窗口重新获得焦点或页面变为可见时检查版本；未变化不读取完整数据，变化与成功写回的受影响记录合并刷新，保留阅读位置。全量读取前后核对版本，不把读取中变化标记为最新。编辑输入、打开对话框或 busy 时延后自动刷新，待可用时继续；不自动改草稿 base_revision 或冻结请求。当前采用前台事件触发，不增加定时轮询、文件监听或第二份事实源。

## 写入与恢复

正文、决定和用途指定都先取得签名快照，再提交稳定 request_id。宿主调用同一 Workflow 库，不另造面板业务数据库。只在原库已结算且 outcome=ok、逐文件结果支持时确认成功。

草稿和未决冻结请求按项目 binding_id 保存在当前浏览器 localStorage。它们用于输入恢复，不是 Task/Decision 的权威记录。重载或网络失败后先查询原 request_id，再按原载荷恢复；查询不到回执不代表从未执行。已经结算的回执只证明当时结果，当前事实另读源文件。

已确认冲突时保留输入。Task 和审阅成员均提供“核对当前来源/候选”，明确比较旧新基准后才允许准备新操作；已冻结的未决请求保持不变。

目前 Task 正文编辑不会自动改变状态，也不关闭 Epic。独立的设计/验证、引擎执行和 Git 交付仍由职责 Skill 负责。

## 身份与部署范围

这里的 user/agent/tool 是可信本机启动方绑定的记录者，不是 Codex/ChatGPT 账号登录，也不检测操作者是否真人。自动化测试使用 tool。运行用户操作时，启动方须有真实用户行为来源，不可让 Agent 借用户会话伪造接受。

state-dir/private 的新目录在 Windows 限当前账户、SYSTEM 与管理员访问；POSIX 使用 0700。连接文件由私有临时文件替换，口令不写日志。仍要求 state-dir 属于可信启动方，不能复用他人预置的签名密钥或共享状态目录。该宿主是本机工具，没有远程多人账号系统。

详情：[桥接合同](../shared/panel-bridge-v1.md) · [本地 I/O 与恢复](../shared/local-io.md) · [第十四步桥接验证](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/validation.md) · [第十五步衔接](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/panel.md) · [治理验证](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/docs/validation.md)。第十四步的历史结果只覆盖当时的桥接读写，不代表完整治理界面已通过浏览器验收。
