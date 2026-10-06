# 通用安装兼容与验证范围

Gamecaden的通用入口是包含SKILL.md、八个职责及共同文档/工具的完整包。Codex和Claude Code另有原生插件入口；支持标准Agent Skills的其他宿主可使用完整目录安装。

## 当前安装目标

| 宿主 | Skills CLI参数 | 本轮已观察的最低兼容依据 |
| --- | --- | --- |
| OpenCode | opencode | 项目级安装与完整资源通过；原生debug skill实际列出总入口及八职责，共九项 |
| Antigravity CLI（agy） | antigravity-cli | 项目级安装与完整资源通过；原生validator识别包内八职责。工作区自动发现全部入口未另行运行模型核验 |
| Cursor IDE／CLI | cursor | 项目级安装与完整资源通过；官方技能路径、元数据和本地CLI扫描实现已对照。未读取独立原生技能列表或运行模型核验 |
| Pi | pi | 项目级Copy安装与完整资源通过；原生目录加载器读取gamecaden总入口，零诊断；八职责另行解析通过 |
| oh my pi（OMP） | 完整目录复制 | 原生项目技能目录复制与完整资源通过；原生目录加载器读取gamecaden总入口，零警告；八职责另行解析通过 |

2026-10-07的检查使用不变的v0.1.1包，每份安装副本150资源且与原包摘要一致。宿主版本为OpenCode1.18.32、agy1.3.0、Cursor CLI2026.10.01-e373342；Cursor IDE3.20.21仅作为现有环境定位。表格说明安装/格式/解析范围，不声称三者都完成了游戏项目或模型工作流实跑。

`antigravity-cli`对应命令agy；`antigravity`另指Antigravity IDE。本轮增加的终端安装目标选择agy。

Pi与OMP的2026-10-07补测分别使用Pi1.0.4和已有OMP18.2.11，仍为同一v0.1.1完整包，每份150资源。检查调用宿主实际的离线目录加载器，不启动模型、登录或项目开发；未测试用户级真实安装或会话行为。

## 为什么不逐宿主跑完整项目

安装兼容只需核对目的目录、合法元数据、可观察的原生解析/发现、完整共同资源、安装范围和更新入口。相同工作流正文、记录合同和公共工具复用已通过的包级检查。

目录安装和离线格式检查不需要模型登录；实际调用模型时，再按宿主要求完成认证与配置。

遇到宿主实际差异时，再补对应的小检查，例如项目指引没有加载、文件操作被拒绝或会话恢复规则不同。模型是否正确路由、开发结果和跨会话续接属于下一层行为验证；本轮未将完整游戏开发流程设为各宿主安装的必经门槛。

## 安装

以OpenCode用户级安装为例：

```sh
npx skills add https://github.com/immortalbeating2/gamecaden/tree/main/plugins/gamecaden --skill gamecaden --agent opencode --global
```

agy改为`--agent antigravity-cli`，Cursor改为`--agent cursor`。省略global安装到当前项目；本轮实际安装检查采用项目级Copy模式，全局目的路径按安装器的当前配置解析。可添加`--copy`使用完整目录复制。

安装后用本宿主可用的Skill入口或文件阅读入口处理明确的Gamecaden请求，再按需要接入项目。项目指引在实际生效的位置合并：这三个宿主支持AGENTS.md，AGY也支持GEMINI.md。安装不自动改写已有项目记录。

独立安装更新使用`npx skills update gamecaden --global`，项目级换为`--project`。完整说明见[安装与更新](installation.md)。

<a id="pi-omp"></a>

## Pi与oh my pi

Pi可使用Skills CLI的`pi`目标：

```sh
npx skills add https://github.com/immortalbeating2/gamecaden/tree/main/plugins/gamecaden --skill gamecaden --agent pi --global
```

用户级目录为`~/.pi/agent/skills/gamecaden`；省略`--global`写入当前项目的`.pi/skills/gamecaden`。Pi也支持标准`.agents/skills`位置。项目技能加载遵循Pi自身的项目信任设置；不要同时安装多个相同入口副本。

OMP使用完整目录复制，用户级为`~/.omp/agent/skills/gamecaden`，项目级为`.omp/skills/gamecaden`。当前Skills CLI没有已确认的`oh-my-pi`目标，不使用猜测的agent参数。克隆本仓库后，在目标项目执行以下PowerShell示例，源路径换为实际克隆位置：

```powershell
$gcSource = Resolve-Path -LiteralPath 'C:\path\to\gamecaden\plugins\gamecaden'
$gcTarget = Join-Path $PWD '.omp/skills/gamecaden'
if (Test-Path -LiteralPath $gcTarget) { throw '先核对现有Gamecaden副本及更新范围' }
New-Item -ItemType Directory -Path (Split-Path -Parent $gcTarget) -Force | Out-Null
Copy-Item -LiteralPath $gcSource.Path -Destination $gcTarget -Recurse
```

OMP用户级安装将`$gcTarget`换为`Join-Path $env:USERPROFILE '.omp/agent/skills/gamecaden'`；启用profile或自定义agent目录时，使用其有效agent目录下的`skills/gamecaden`。该示例适用于Windows；其他系统将完整目录复制到上面的用户/项目路径即可。OMP也支持标准`.agents/skills`目录。手动副本更新沿用Git拉取后核对并替换自己维护的完整副本，不能用宿主自身升级命令替代Gamecaden更新。

两者使用总入口`gamecaden`；技能命令启用时可调用`/skill:gamecaden`，例如`/skill:gamecaden 使用init接入本项目`，也可直接明确要求以Gamecaden处理本次工作。此次原生加载均只注册总入口；内部八职责由入口按相对路径读取，不承诺出现Codex/Claude插件的八个命名空间命令。`AGENTS.md`仍承载项目采用指引，安装本身不接入或改写游戏项目。

依据：[Skills CLI目标列表](https://github.com/vercel-labs/skills#supported-agents)、[OpenCode Skills](https://opencode.ai/docs/skills/)、[AGY迁移和技能路径](https://antigravity.google/docs/cli/gcli-migration/)、[Cursor Skills](https://cursor.com/docs/skills)、[Pi Skills](https://pi.dev/docs/latest/skills)、[OMP Skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md)。
