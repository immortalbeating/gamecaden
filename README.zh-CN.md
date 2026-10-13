# Gamecaden

[English](README.md)

维护与公开发行已统一到 [immortalbeating/gamecaden](https://github.com/immortalbeating/gamecaden)。当前版本为0.2.1；已发布的0.1.x版本保持原内容。原账号地址仅保留GitHub兼容跳转。

0.2.0 整合项目当前正文、材料导航、证据留存、分阶段开发计划与派生输出，并补齐 Task 模式判断、附件读取及 Windows 长源路径支持。Codex、Claude 和完整通用包继续共用环境检查、独立依赖准备与调用入口。

Gamecaden 是面向 Codex、Claude Code及兼容Skill宿主的游戏开发工作流：从已有目标和项目记录继续工作，把设计、实现、资产、验证和收尾接回真实来源。

A local-first game development workflow for Codex and Claude Code, with eight focused skills, a standalone skill entry and an optional local panel.

0.2.1 为 Codex 插件列表与输入框加入已确定的橙色 G＋深灰黑播放图标；工作流合同与运行行为沿用 0.2.0 基线。

## 安装与更新

在支持插件的 Codex CLI 中执行：

```sh
codex plugin marketplace add immortalbeating/gamecaden
codex plugin add gamecaden@gamecaden --json
```

Claude Code终端安装：

```sh
claude plugin marketplace add immortalbeating/gamecaden
claude plugin install gamecaden@gamecaden --scope user
```

普通安装跟踪默认分支，更新时无需修改版本号。固定tag可选；Codex更新使用`marketplace upgrade`后`plugin add`，Claude使用`marketplace update`后`plugin update`。安装后开启新会话核对实际路径和版本。

还可通过`npx skills`安装完整包或手动复制为独立Skill；具体命令、范围、更新及固定tag切换见[安装说明](docs/installation.md)。

通用安装目标还包括OpenCode、Antigravity CLI（agy）、Cursor、Pi和oh my pi（OMP）。安装、原生解析/发现与完整项目行为的覆盖分别记录，见[兼容范围](docs/compatibility.md)。

## 语言

安装保持一个 Gamecaden 插件身份，不需要选择两个语言包。发布包的全部 Skill、共享合同、材料参考与模板采用英文正文，公开仓库提供中英文使用说明，完整规则正文统一为英文。

**回复和新建材料文档默认使用用户当前语言**，英文 Skill、模板或输入资料不会使产出自动改为英文。用户或有效项目指引可以分别明确沟通与文档语言，本次明确要求优先于旧偏好。维护已有文档默认保留原语言，用户要求转换时再调整。schema 字段、ID、枚举、路径和命令保持原样。详见[语言约定](plugins/gamecaden/shared/workspace.md#6-language-preferences)。当前面板控件仍为中文，本次英文覆盖工作流文档。

语言适配以可读和可维护为目标：正文与说明默认采用用户语言，技术标识保持稳定，专业术语沿用既有惯例。无需消除所有英文，也不将零散英文标签设为验收门禁。

## 开始使用

直接在当前项目向 Codex 描述目标即可，例如：

- 新项目：`使用 Gamecaden init 接入这个新项目，然后帮我确定一个可实现的小型游戏目标。`
- 旧项目：`使用 Gamecaden init 接入这个项目，保留现有设计、任务和资产记录的位置，先核对实际运行入口。`
- 单次工作：`使用 Gamecaden flow 修复暂停后计时跳变的问题，并验证本轮改动。`
- 已采用项目续接：`继续之前的工作，按项目已保存的目标完成当前任务，并保存真实检查结果。`

项目明确采用后的有效指引可支持后续自然续接；单次显式调用按本次范围执行，不要求全项目迁移。正式接入整理当前 `vision.md`、必要的 `spec/index.md`；项目级持续开发默认建立 `roadmap.md`，默认在 `game-workflow/`，只有当前一个成果或方向未定也如实表达。已有大型方案需要分阶段落实时，design 使用 [Phased Development Plan](plugins/gamecaden/shared/phased-development.md) 编排 Epic、S 阶段与 Task；Roadmap 维护 M 里程碑。原材料与工作保留明确维护范围，旧映射的局部续接保持兼容。

## 八个职责

| 职责 | 用途 |
| --- | --- |
| flow | 定位请求与原工作，选择后续职责 |
| init | 确认项目根、运行根与权威来源，接入或迁移 |
| brainstorm | 逐轮澄清想法、备选与关键取舍 |
| design | 将明确需求转为设计和实施安排 |
| develop | 实现、修复并验证真实运行路径 |
| assets | 制作、修订和交付可追溯资产 |
| verify | 核验要求覆盖、证据与必要接受 |
| close | 保存交付结论和遗留归属，收尾工作 |

职责按请求选择，不是八步必经流程。详细规则见 [技能目录](plugins/gamecaden/skills) 和 [来源约定](plugins/gamecaden/shared/workspace.md)。Notes 提供项目内的基础记录能力；经验增强尚未采用。当前包没有后台记忆、自动调度或专用 MCP 服务。

quick 和 standard 是同一 Task 的轻量与常规管理模式；按交付的实际组织与维护需要选择。常规模式也能直接处理明确小步骤，模式不降低验证或接受要求。选用与模板见 [Task 模式](plugins/gamecaden/shared/records.md#selecting-the-management-mode)。

视图与独立交接不增加 Skill 命令：面板直接读原来源，JSON 快照和 handoff 按真实需求保存，默认路径、刷新与版本留存见[派生输出](plugins/gamecaden/shared/derived-outputs.md)。当前工具不提供完整面板静态 HTML 导出，不生成新的 Markdown 进度视图。

## 可选面板与开发工具

读取技能正文无需 Python 环境。真正采用项目、首个本地 I/O 或启动面板前，按 [工具就绪与调用](plugins/gamecaden/shared/local-io.md#1-environment-and-invocation) 检查并准备独立环境；启动入口需要 Python 3.12+。面板操作见 [面板说明](docs/panel.md)。面板读取已登记来源，默认只读；技术检查、用户接受与运行采用分别记录。

维护测试使用 Python 3.12+ 和 Node.js：

```sh
python scripts/check.py --suite all
```

[验证范围](docs/validation.md) · [架构](docs/architecture.md) · [贡献指南](CONTRIBUTING.md) · [变更记录](CHANGELOG.md)

## 许可

本项目采用 [MIT](LICENSE)。随包保留的 ELK.js 0.12.0 使用原 EPL-2.0 许可；第三方声明与许可随对应文件保留。仓库：https://github.com/immortalbeating/gamecaden
