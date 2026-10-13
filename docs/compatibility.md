<a id="通用安装兼容与验证范围"></a>

# General Installation Compatibility and Validation Scope

Maintenance and public releases are unified at [immortalbeating/gamecaden](https://github.com/immortalbeating/gamecaden). The current version is 0.2.1; published 0.1.x versions retain their original content. The former account address remains only as a GitHub compatibility redirect.

Gamecaden's general entry point is a complete package containing SKILL.md, eight responsibilities, and common documents/tools. Codex and Claude Code also have native plugin entry points; other hosts supporting standard Agent Skills can use complete-directory installation.

<a id="当前安装目标"></a>

## Current Installation Targets

| Host | Skills CLI parameter | Minimum compatibility grounds observed in that round |
| --- | --- | --- |
| OpenCode | opencode | Project-level installation and complete resources passed; native debug skill actually listed the main entry and eight responsibilities, nine entries total |
| Antigravity CLI (agy) | antigravity-cli | Project-level installation and complete resources passed; native validator recognized the eight bundled responsibilities. Automatic workspace discovery of all entries was not separately verified by running a model |
| Cursor IDE / CLI | cursor | Project-level installation and complete resources passed; official Skill paths, metadata, and local CLI scanning implementation were compared. No separate native Skill list was read and no model verification was run |
| Pi | pi | Project-level Copy installation and complete resources passed; native directory loader read the gamecaden main entry with zero diagnostics; the eight responsibilities separately passed parsing |
| oh my pi (OMP) | Complete-directory copy | Native project Skill-directory copying and complete resources passed; native directory loader read the gamecaden main entry with zero warnings; the eight responsibilities separately passed parsing |

Checks on 2026-10-07 used the unchanged v0.1.1 package, with 150 resources in each installation copy and digests matching the original package. Host versions were OpenCode 1.18.32, agy 1.3.0, and Cursor CLI 2026.10.01-e373342; Cursor IDE 3.20.21 served only to locate the existing environment. The table describes installation/format/parsing coverage and does not claim all three completed actual game-project or model-workflow runs.

`antigravity-cli` corresponds to the agy command; `antigravity` separately refers to Antigravity IDE. The terminal installation target added in that round selects agy.

Pi and OMP supplementary checks on 2026-10-07 used Pi 1.0.4 and existing OMP 18.2.11 respectively, still with the same complete v0.1.1 package and 150 resources per copy. Checks called the hosts' actual offline directory loaders without starting models, login, or project development; actual user-level installation or session behavior was not tested.

<a id="为什么不逐宿主跑完整项目"></a>

## Why Complete Projects Are Not Run in Every Host

Installation compatibility needs only checks of destination directories, valid metadata, observable native parsing/discovery, complete common resources, installation scope, and update entry points. The same workflow bodies, record contracts, and public tools reuse passed package-level checks.

Directory installation and offline format checks need no model login; authenticate and configure under host requirements when actually calling a model.

When actual host differences arise, supplement with corresponding small checks, such as project guidance not loading, rejected file operations, or different session-recovery rules. Correct model routing, development outcomes, and cross-session continuation belong to the next layer of behavioral verification; that round did not make complete game development a mandatory installation threshold for every host.

<a id="安装"></a>

## Installation

Example user-level OpenCode installation:

```sh
npx skills add https://github.com/immortalbeating/gamecaden/tree/main/plugins/gamecaden --skill gamecaden --agent opencode --global
```

Change to `--agent antigravity-cli` for agy or `--agent cursor` for Cursor. Omit global to install into the current project; actual installation checks in that round used project-level Copy mode, while the installer's current configuration resolves global destination paths. Add `--copy` for complete-directory copying.

After installation, use available host Skill or file-reading entry points for explicit Gamecaden requests, then adopt projects as needed. Merge project guidance at actually effective locations: these three hosts support AGENTS.md, and AGY also supports GEMINI.md. Installation does not automatically rewrite existing project records.

Update standalone installations with `npx skills update gamecaden --global`, replacing it with `--project` for project-level scope. See [installation and updates](installation.md) for complete instructions.

<a id="pi-omp"></a>

<a id="pi与oh-my-pi"></a>

## Pi and oh my pi

Pi can use the Skills CLI `pi` target:

```sh
npx skills add https://github.com/immortalbeating/gamecaden/tree/main/plugins/gamecaden --skill gamecaden --agent pi --global
```

The user-level directory is `~/.pi/agent/skills/gamecaden`; omit `--global` to write to the current project's `.pi/skills/gamecaden`. Pi also supports standard `.agents/skills` locations. Project Skill loading follows Pi's own project-trust settings; do not install multiple copies of the same entry at once.

OMP uses complete-directory copying, with `~/.omp/agent/skills/gamecaden` for user scope and `.omp/skills/gamecaden` for project scope. The current Skills CLI has no confirmed `oh-my-pi` target; do not guess agent parameters. After cloning this repository, run the following PowerShell example in the target project, replacing the source path with the actual clone location:

```powershell
$gcSource = Resolve-Path -LiteralPath 'C:\path\to\gamecaden\plugins\gamecaden'
$gcTarget = Join-Path $PWD '.omp/skills/gamecaden'
if (Test-Path -LiteralPath $gcTarget) { throw '先核对现有Gamecaden副本及更新范围' }
New-Item -ItemType Directory -Path (Split-Path -Parent $gcTarget) -Force | Out-Null
Copy-Item -LiteralPath $gcSource.Path -Destination $gcTarget -Recurse
```

For user-level OMP installation, replace `$gcTarget` with `Join-Path $env:USERPROFILE '.omp/agent/skills/gamecaden'`; with profiles or custom agent directories enabled, use `skills/gamecaden` under the effective agent directory. This example is for Windows; on other systems, copy the complete directory into user/project paths above. OMP also supports the standard `.agents/skills` directory. To update manual copies, pull through Git, then check and replace the complete copy you maintain; host self-upgrade commands do not replace Gamecaden updates.

Both use the `gamecaden` main entry. When Skill commands are enabled, call `/skill:gamecaden`, for example `/skill:gamecaden 使用init接入本项目`, or explicitly request Gamecaden for current work. Native loading in those checks registered only the main entry; it reads the eight internal responsibilities by relative paths, without promising eight Codex/Claude-plugin-style namespaced commands. `AGENTS.md` still carries project-adoption guidance; installation itself does not adopt or rewrite game projects.

Sources: [Skills CLI target list](https://github.com/vercel-labs/skills#supported-agents), [OpenCode Skills](https://opencode.ai/docs/skills/), [AGY migration and Skill paths](https://antigravity.google/docs/cli/gcli-migration/), [Cursor Skills](https://cursor.com/docs/skills), [Pi Skills](https://pi.dev/docs/latest/skills), [OMP Skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md).
