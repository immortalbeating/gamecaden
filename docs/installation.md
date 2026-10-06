# 安装、更新与独立使用

Gamecaden提供Codex插件、Claude Code插件和完整目录的Skill安装。插件提供八个命名空间职责；独立入口使用包根的`gamecaden` Skill，再读取同包职责。按宿主实际列表核对名称，安装后在新会话使用。

本轮Codex独立目录的新进程实际发现九个入口：`gamecaden:gamecaden`总入口及八个`gamecaden:flow`等职责，均为项目Skill而非marketplace安装。通用CLI报告的“一个Skill”是一个完整安装包，宿主还可能发现包内职责。Claude插件实际发现八职责；Claude独立目录已核对完整复制与相对资源，尚未运行模型确认其原生Skill列表。

## Codex插件

在支持插件命令的Codex CLI中执行：

```sh
codex plugin marketplace add immortalbeating2/gamecaden
codex plugin add gamecaden@gamecaden --json
```

未指定`--ref`时跟踪仓库默认分支，本仓库为`main`。这里的跟踪指更新时取该分支，不等于后台自动更新。后续更新使用相同命令，不需要填写新版本号：

```sh
codex plugin marketplace upgrade gamecaden
codex plugin add gamecaden@gamecaden --json
```

第一步刷新安装源，第二步安装该源当前提供的插件版本。新开会话回读真实版本，已有会话的列表不能证明新内容已加载。

### 固定版本及切换更新方式

复现或稳定固定场景可以指定tag，例如`codex plugin marketplace add immortalbeating2/gamecaden --ref v0.1.1`。固定tag后刷新仍读取该tag，不会自动跳到以后发布的tag；主动升级需改目标版本。

如果此前登记了`--ref v0.1.0`，改用默认分支前明确替换旧的marketplace登记：

```sh
codex plugin marketplace remove gamecaden
codex plugin marketplace add immortalbeating2/gamecaden
codex plugin add gamecaden@gamecaden --json
```

只对名为`gamecaden`的公开安装源使用上述切换。此前演练的其他本地来源独立处理，不能视为已自动迁移。

## Claude Code插件

在终端中执行，默认示例明确选择用户级：

```sh
claude plugin marketplace add immortalbeating2/gamecaden
claude plugin install gamecaden@gamecaden --scope user
```

在Claude Code交互会话内也可使用：

```text
/plugin marketplace add immortalbeating2/gamecaden
/plugin install gamecaden@gamecaden
/reload-plugins
```

交互安装时选择User、Project或Local范围；终端可用`--scope project`安装到当前项目。八个职责使用`/gamecaden:flow`、`/gamecaden:init`等命名空间。

后续刷新安装源并更新插件：

```sh
claude plugin marketplace update gamecaden
claude plugin update gamecaden@gamecaden --scope user
```

更新后开启新会话，或在交互会话执行`/reload-plugins`。Claude项目采用指引写入实际生效的CLAUDE.md；Codex使用AGENTS.md。两者都沿用项目已有记录，不因安装重建任务。

## 通用Skills CLI

需要Node.js/npm。这里的`skills`是Vercel维护的安装器，不是Gamecaden自己的npm注册表包。它可将完整包安装为宿主的本地Skill，无需登记marketplace。

```sh
# 用户级，供Codex使用
npx skills add https://github.com/immortalbeating2/gamecaden/tree/main/plugins/gamecaden --skill gamecaden --agent codex --global

# 用户级，供Claude Code使用
npx skills add https://github.com/immortalbeating2/gamecaden/tree/main/plugins/gamecaden --skill gamecaden --agent claude-code --global
```

省略`--global`即安装到当前项目；选择Copy模式可在不支持符号链接的环境中保存完整目录。需要时添加`--copy`。避免选择包内单个flow/init目录：这些职责依赖共同的shared、profiles、templates和scripts资源，拆开复制会失去相对链接。

更新独立用户级安装：

```sh
npx skills update gamecaden --global
```

项目级使用`npx skills update gamecaden --project`。以安装器的实际结果和宿主发现为准；其他宿主的目录选择由该CLI支持范围决定。本轮不宣称所有宿主都已实跑。

## 不需要npm的完整目录安装

克隆公开仓库，把`plugins/gamecaden`完整目录复制到当前宿主的Skill位置，保留所有共同资源。用户级示例位置：Codex为`~/.agents/skills/gamecaden`，Claude Code为`~/.claude/skills/gamecaden`；项目级使用项目下对应路径。

```sh
git clone https://github.com/immortalbeating2/gamecaden.git
```

目录已有内容时先核对归属与差异；更新由`git pull --ff-only`取得新源码，再更新自己维护的安装副本。可删除副本中的`.codex-plugin/`、`.claude-plugin/`、`plugin.json`和`.gamecaden-package.json`只保留独立Skill资源；此副本不再声称满足插件完整性manifest。正文及全部被引用资源仍需保留。支持标准SKILL.md的其他宿主可按其实际目录使用本入口。

## 安装、项目采用与运行工具

安装提供发现入口。项目采用通常通过明确请求`使用Gamecaden init接入本项目`完成；有效项目指引支持后续自然续接。插件方式与独立方式择一，避免同一宿主重复发现同包。

技能正文无需Python；可选本地I/O和面板需要Python 3.12+及独立运行环境，见[面板说明](panel.md)。这些依赖不会由插件安装或npx自动安装。本轮安装验证不等于模型行为、游戏运行或人工接受。

依据：[Codex插件文档](https://developers.openai.com/plugins/build/plugins)、[Claude市场与版本更新](https://code.claude.com/docs/en/plugin-marketplaces)、[Claude插件安装](https://code.claude.com/docs/en/discover-plugins)、[Vercel skills CLI](https://github.com/vercel-labs/skills)。
