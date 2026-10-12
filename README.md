# Gamecaden

[中文说明](README.zh-CN.md)

A local-first game development workflow for Codex, Claude Code, and compatible Skill hosts. Continue from existing goals and project records, connecting design, implementation, assets, verification, and closure to their actual sources.

The maintained public repository is [immortalbeating/gamecaden](https://github.com/immortalbeating/gamecaden). The current version is **0.2.0**; previously published 0.1.x tags and releases retain their original contents. The former address remains a GitHub compatibility redirect.

0.2.0 brings together current project documents, material navigation, evidence retention, phased development planning, derived outputs, Task mode guidance, attachment reading, and Windows long source paths. All Skill bodies, shared contracts, material references, and templates are available in English, with English and Chinese usage guides in the same repository.

## Install and update

In a Codex CLI with plugin support:

```sh
codex plugin marketplace add immortalbeating/gamecaden
codex plugin add gamecaden@gamecaden --json
```

For Claude Code:

```sh
claude plugin marketplace add immortalbeating/gamecaden
claude plugin install gamecaden@gamecaden --scope user
```

Ordinary installation tracks the default branch when updated. Codex updates use `marketplace upgrade` followed by `plugin add`; Claude uses `marketplace update` followed by `plugin update`. Open a new session afterwards to check actual paths and version. Pinning a tag is optional.

Install the complete package through `npx skills` or copy it as a standalone Skill. Commands, scopes, updates, and tag switching are in the [installation guide](docs/installation.md). OpenCode, Antigravity CLI (agy), Cursor, Pi, and oh my pi (OMP) are additional standalone targets. Installation, native discovery, and complete project behavior have separate coverage, recorded in the [compatibility report](docs/compatibility.md).

## Language

There is **one plugin identity and one installation**, rather than separate English and Chinese plugins. English is the published workflow text. Chinese users can read the [Chinese usage guide](README.zh-CN.md) and retain Chinese communication and project documents.

By default, **replies and newly created material documents use the user's current language**. English Skills, templates, or input references do not make the outputs English. The user or effective project guidance may explicitly specify communication and document languages separately; current explicit instructions take precedence over earlier preferences. Maintain an existing document in its language unless conversion is requested. Prose and explanations use the selected language, template labels adapt to reading needs, and professional terms follow established usage. Schema keys, IDs, enums, paths, and commands remain unchanged; isolated English labels are not an acceptance gate. See [language preferences](plugins/gamecaden/shared/workspace.md#6-language-preferences).

## Start using Gamecaden

Describe the goal in the current project, for example:

- New project: `Use Gamecaden init to adopt this new project, then help me choose an achievable small-game goal.`
- Existing project: `Use Gamecaden init to adopt this project. Preserve existing design, task, and asset maintenance locations, and check the actual runtime entry first.`
- One delivery: `Use Gamecaden flow to fix the timer jump after resuming from pause and verify this change.`
- Continue an adopted project: `Continue the existing work toward the saved project goals and preserve actual check results.`

Effective guidance in an adopted project supports natural continuation in later sessions. A single explicit invocation stays within that work's scope and does not require whole-project migration. Formal adoption organizes current `vision.md` and necessary `spec/index.md`; ongoing project-wide development defaults to `roadmap.md`, usually under `game-workflow/`. State a single current outcome or unresolved direction honestly.

For an adopted large scheme needing phased implementation, design uses a [Phased Development Plan](plugins/gamecaden/shared/phased-development.md) to arrange Epics, S Stages, and Tasks; Roadmap maintains M milestones. Original materials and work retain clear maintenance ownership. Local continuation using legacy mappings remains compatible.

## Eight responsibilities

| Skill | Purpose |
|---|---|
| flow | Locate the request and original work, then select the next responsibility |
| init | Identify project/runtime roots and authoritative sources; adopt or migrate |
| brainstorm | Clarify ideas, alternatives, and key tradeoffs through successive questions |
| design | Turn known requirements into design and implementation arrangements |
| develop | Implement, repair, and verify the actual runtime path |
| assets | Produce, revise, and deliver traceable assets |
| verify | Check requirement coverage, evidence, and necessary acceptance |
| close | Save delivery conclusions and remaining ownership, then close work |

Responsibilities are selected for the request, not eight mandatory steps. Read the [Skills](plugins/gamecaden/skills), [standalone entry](plugins/gamecaden/SKILL.md), and [source conventions](plugins/gamecaden/shared/workspace.md). Notes provide basic project-local records; enhanced experience memory is not adopted. This package provides no background memory, automatic scheduler, or dedicated MCP server.

quick and standard are lightweight and regular management modes of the same Task, selected by actual delivery organization and maintenance needs. Standard can directly handle a clear small step; mode never lowers verification or acceptance requirements. See [Task modes](plugins/gamecaden/shared/records.md#selecting-the-management-mode).

Views and independent handoffs add no Skill commands. The panel reads original sources; save JSON snapshots and handoffs when actually needed. Paths, refresh, and version retention follow [derived outputs](plugins/gamecaden/shared/derived-outputs.md). The current tool does not export the complete panel as static HTML or create new Markdown progress views.

## Optional panel and maintenance

Reading Skill bodies requires no Python environment. Before actual project adoption, the first local I/O, or panel startup, check and prepare the isolated environment under [tool readiness](plugins/gamecaden/shared/local-io.md#1-environment-and-invocation). The launcher requires Python 3.12+. Read the [panel guide](plugins/gamecaden/panels/README.md). Registered sources are read-only by default; technical checks, user acceptance, and runtime adoption remain distinct. The current panel interface is Chinese; this release supplies English workflow documentation rather than translated panel controls.

Maintenance checks require Python 3.12+ and Node.js:

```sh
python scripts/check.py --suite all
```

[Validation](docs/validation.md) · [Architecture](docs/architecture.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)

## License

Gamecaden's own code and documentation use [MIT](LICENSE). Bundled ELK.js 0.12.0 retains EPL-2.0; third-party notices and licenses remain with their files.
