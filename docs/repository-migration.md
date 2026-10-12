<a id="统一维护与发行仓库"></a>

# Unified Maintenance and Release Repository

Gamecaden is now maintained and publicly released at [immortalbeating/gamecaden](https://github.com/immortalbeating/gamecaden). Ownership of the former immortalbeating2/gamecaden has transferred; GitHub may redirect the old address, which is no longer an independent maintenance source.

0.1.2 updated public installation sources, repository metadata, and publisher names; Skills, record protocols, and runtime logic retained the validated 0.1.1 implementation. First-party content remains MIT, with third-party licenses and original copyright notices retained. Tags and release assets for 0.1.0 and 0.1.1 are not overwritten.

<a id="更新"></a>

## Updates

When an existing public Codex source is named gamecaden, first replace source registration, then install:

```sh
codex plugin marketplace remove gamecaden
codex plugin marketplace add immortalbeating/gamecaden
codex plugin add gamecaden@gamecaden --json
```

For existing Claude Code sources, likewise use marketplace remove/add to switch to immortalbeating/gamecaden, then repeat plugin install under the original scope (for example, user scope: `claude plugin install gamecaden@gamecaden --scope user`). Install or update standalone Skills from the [current repository's complete package](https://github.com/immortalbeating/gamecaden/tree/main/plugins/gamecaden). See [installation instructions](installation.md) for specific steps.

Locally adopted projects with pinned versions, digests, or tool-cache paths need incremental synchronization of those fields; retain original tasks, acceptance, and historical records. After updates, open a new session to check actual entry points rather than reinitializing projects or rerunning complete games.

Internal maintenance history has a separate protected read-only archive; the current public repository uses the original public ancestry without internal records or local receipts.
