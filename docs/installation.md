# Installation, Updates, and Standalone Use

Maintenance and public releases are unified at [immortalbeating/gamecaden](https://github.com/immortalbeating/gamecaden). The current version is 0.3.0; published versions retain their original content. The former account address remains only as a GitHub compatibility redirect. See [repository migration](repository-migration.md) for switching existing installations.

0.3.0 includes asset storage/retention, gameplay-data and UI family conventions, scoped continuation, and the unified environment entry point. Pinned older tags retain their corresponding contracts. The system needs Python 3.12+ with venv support; the first local-tool invocation automatically prepares independent dependencies.

Upgrade tools used by all clients sharing a project's operation store together. Version 0.3.0 reads legacy receipts and may write losslessly compressed large settled receipts; older tools cannot read that format, and package rollback does not convert it. Project documents and schema v1 retain their existing identities and locations.

Gamecaden provides Codex plugins, Claude Code plugins, and complete-directory Skill installation. Plugins provide eight namespaced responsibilities; the standalone entry point uses the package-root `gamecaden` Skill, then reads responsibilities from the same package. Check names against the host's actual list and use a new session after installation.

The same complete Gamecaden plugin/package serves English and Chinese users; there is no separate locale installer. English workflow text is complete, with a [Chinese usage guide](https://github.com/immortalbeating/gamecaden/blob/main/README.zh-CN.md). New material documents default to the user's current language, regardless of the language of Skills, templates, input references, or other project files; only an explicit current/user or effective project document-language preference selects another language, and current explicit instructions override older preferences. Existing documents retain their language unless conversion is requested. See [language preferences](../plugins/gamecaden/shared/workspace.md#6-language-preferences) for separate project communication and document preferences. Workflow text is English; panel controls currently remain Chinese.

In the installation evidence for the earlier round, a new process for the standalone Codex directory actually discovered nine entry points: the `gamecaden:gamecaden` main entry and eight responsibilities such as `gamecaden:flow`, all as project Skills rather than marketplace installations. The general CLI's “one Skill” refers to one complete installation package; hosts may also discover responsibilities within it. The Claude plugin actually discovered eight responsibilities; complete copying and relative resources were checked for the Claude standalone directory, but no model run confirmed its native Skill list.

## Codex Plugin

Run in a Codex CLI supporting plugin commands:

```sh
codex plugin marketplace add immortalbeating/gamecaden
codex plugin add gamecaden@gamecaden --json
```

Without `--ref`, installation tracks the repository's default branch, `main` here. Tracking means taking that branch during updates, not automatic background updates. Later updates use the same commands without a new version number:

```sh
codex plugin marketplace upgrade gamecaden
codex plugin add gamecaden@gamecaden --json
```

The first step refreshes the installation source, and the second installs the plugin version currently supplied by that source. Read back the actual version in a new session; existing session lists cannot prove new content loaded.

### Pinned Versions and Switching Update Methods

For reproducibility or stable pinned use, specify a tag, for example `codex plugin marketplace add immortalbeating/gamecaden --ref v0.3.0`. Refreshing a pinned tag still reads that tag rather than automatically moving to later released tags; deliberate upgrades require changing the target version.

If previously registered with `--ref v0.1.0`, explicitly replace the old marketplace registration before switching to the default branch:

```sh
codex plugin marketplace remove gamecaden
codex plugin marketplace add immortalbeating/gamecaden
codex plugin add gamecaden@gamecaden --json
```

Use this switch only for the public installation source named `gamecaden`. Other local sources from earlier trials are handled independently and cannot be considered automatically migrated.

## Claude Code Plugin

Run in a terminal; the default example explicitly selects user-level scope:

```sh
claude plugin marketplace add immortalbeating/gamecaden
claude plugin install gamecaden@gamecaden --scope user
```

Within an interactive Claude Code session, you can also use:

```text
/plugin marketplace add immortalbeating/gamecaden
/plugin install gamecaden@gamecaden
/reload-plugins
```

Choose User, Project, or Local during interactive installation; terminal installations can use `--scope project` for the current project. The eight responsibilities use namespaces such as `/gamecaden:flow` and `/gamecaden:init`.

Refresh the installation source and update the plugin later:

```sh
claude plugin marketplace update gamecaden
claude plugin update gamecaden@gamecaden --scope user
```

After updates, open a new session or run `/reload-plugins` interactively. Claude project-adoption guidance goes in the actually effective CLAUDE.md; Codex uses AGENTS.md. Both retain existing project records rather than rebuilding tasks on installation.

## General Skills CLI

Requires Node.js/npm. Here `skills` is the installer maintained by Vercel, not Gamecaden's own npm registry package. It installs the complete package as a host-local Skill without marketplace registration.

```sh
# User-level, for Codex
npx skills add https://github.com/immortalbeating/gamecaden/tree/main/plugins/gamecaden --skill gamecaden --agent codex --global

# User-level, for Claude Code
npx skills add https://github.com/immortalbeating/gamecaden/tree/main/plugins/gamecaden --skill gamecaden --agent claude-code --global
```

Omit `--global` to install into the current project; choose Copy mode to retain the complete directory in environments without symbolic-link support. Add `--copy` when needed. Avoid individual flow/init directories inside the package: these responsibilities depend on common shared, profiles, templates, and scripts resources, and separated copies lose relative links.

Update standalone user-level installations:

```sh
npx skills update gamecaden --global
```

For project-level installations, use `npx skills update gamecaden --project`. Actual installer results and host discovery govern; the CLI's supported scope determines directory choices for other hosts. The earlier installation round does not claim actual runs for all hosts.

### Pi and oh my pi (OMP)

Pi uses the same complete package with the agent parameter changed to `--agent pi`: user-level installs go to `~/.pi/agent/skills/gamecaden`, and project-level to `.pi/skills/gamecaden`. OMP uses complete-directory copying to `~/.omp/agent/skills/gamecaden` or project `.omp/skills/gamecaden`; no `oh-my-pi` installer parameter has been confirmed.

Both read eight responsibilities and common resources through the main entry; when Skill commands are enabled, use `/skill:gamecaden`. In the earlier round, native directory loaders registered only the main entry, without running a model or complete project. See [general installation compatibility](compatibility.md#pi-omp) for installation commands, OMP PowerShell copying examples, updates, and project trust.

## Complete-directory Installation Without npm

OpenCode, Antigravity CLI (agy), and Cursor can also use the complete-package approach above, selecting `--agent opencode`, `--agent antigravity-cli`, and `--agent cursor` respectively. See [general installation compatibility](compatibility.md) for minimum compatibility checks and behavioral verification not performed; installation compatibility does not require running complete game projects in every host.

Clone the public repository and copy the complete `plugins/gamecaden` directory into the current host's Skill location, preserving all common resources. Example user-level locations are `~/.agents/skills/gamecaden` for Codex and `~/.claude/skills/gamecaden` for Claude Code; use corresponding paths under the project for project-level installation.

```sh
git clone https://github.com/immortalbeating/gamecaden.git
```

When directories already contain files, check ownership and differences first; obtain updated source through `git pull --ff-only`, then update the installation copy you maintain. You may delete `.codex-plugin/`, `.claude-plugin/`, `plugin.json`, and `.gamecaden-package.json` from the copy to retain standalone Skill resources only; that copy no longer claims plugin-integrity manifest compliance. Bodies and every referenced resource must remain. Other hosts supporting standard SKILL.md can use this entry in their actual directories.

## Installation, Project Adoption, and Runtime Tools

Installation provides discovery entry points. Project adoption is usually completed by an explicit request such as `Use Gamecaden init to adopt this project`; effective project guidance supports later natural continuation. Choose either plugin or standalone installation to avoid duplicate discovery of the same package in one host.

Skill bodies require no Python. Plugin or npx installation supplies resources and discovery entry points; before actual project adoption, first local I/O, or panel startup, separately check and prepare an independent environment under [tool readiness and invocation](../plugins/gamecaden/shared/local-io.md#1-environment-and-invocation). The bundled launcher requires Python 3.12+, and the first tool invocation may automatically prepare dependencies; read-only consultation or init inspect does not automatically install or write project guidance. See [panel instructions](panel.md) for startup. Installation validation from the earlier round is not model behavior, game execution, or human acceptance.

Sources: [Codex plugin documentation](https://developers.openai.com/plugins/build/plugins), [Claude marketplaces and version updates](https://code.claude.com/docs/en/plugin-marketplaces), [Claude plugin installation](https://code.claude.com/docs/en/discover-plugins), [Vercel skills CLI](https://github.com/vercel-labs/skills).
