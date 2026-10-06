# Gamecaden

Gamecaden 是面向 Codex、Claude Code及兼容Skill宿主的游戏开发工作流：从已有目标和项目记录继续工作，把设计、实现、资产、验证和收尾接回真实来源。

A local-first game development workflow for Codex and Claude Code, with eight focused skills, a standalone skill entry and an optional local panel.

## 安装与更新

在支持插件的 Codex CLI 中执行：

```sh
codex plugin marketplace add immortalbeating2/gamecaden
codex plugin add gamecaden@gamecaden --json
```

Claude Code终端安装：

```sh
claude plugin marketplace add immortalbeating2/gamecaden
claude plugin install gamecaden@gamecaden --scope user
```

普通安装跟踪默认分支，更新时无需修改版本号。固定tag可选；Codex更新使用`marketplace upgrade`后`plugin add`，Claude使用`marketplace update`后`plugin update`。安装后开启新会话核对实际路径和版本。

还可通过`npx skills`安装完整包或手动复制为独立Skill；具体命令、范围、更新及固定tag切换见[安装说明](docs/installation.md)。

通用安装目标还包括OpenCode、Antigravity CLI（agy）和Cursor。安装、原生解析/发现与完整项目行为的覆盖分别记录，见[兼容范围](docs/compatibility.md)。

## 开始使用

直接在当前项目向 Codex 描述目标即可，例如：

- 新项目：`使用 Gamecaden init 接入这个新项目，然后帮我确定一个可实现的小型游戏目标。`
- 旧项目：`使用 Gamecaden init 接入这个项目，保留现有设计、任务和资产记录的位置，先核对实际运行入口。`
- 单次工作：`使用 Gamecaden flow 修复暂停后计时跳变的问题，并验证本轮改动。`
- 已采用项目续接：`继续之前的工作，按项目已保存的目标完成当前任务，并保存真实检查结果。`

项目明确采用后的有效指引可支持后续自然续接；单次显式调用按本次范围执行，不要求全项目迁移。普通未采用项目继续沿用原工作方式。接入时先读取已有目标和记录，只补实际需要的材料；新记录默认在 `game-workflow/`，已有来源保留原位置。

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

## 可选面板与开发工具

读取技能正文无需 Python 环境。面板和本地 I/O 使用 Python 3.12+，按 [面板说明](docs/panel.md) 安装独立环境。面板读取已登记来源，默认只读；技术检查、用户接受与运行采用分别记录。

维护测试使用 Python 3.12+ 和 Node.js：

```sh
python scripts/check.py --suite all
```

[验证范围](docs/validation.md) · [架构](docs/architecture.md) · [贡献指南](CONTRIBUTING.md) · [变更记录](CHANGELOG.md)

## 许可

本项目采用 [MIT](LICENSE)。随包保留的 ELK.js 0.12.0 使用原 EPL-2.0 许可；第三方声明与许可随对应文件保留。仓库：https://github.com/immortalbeating2/gamecaden
