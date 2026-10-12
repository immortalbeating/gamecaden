<a id="安装升级与回滚"></a>
# Installation, Upgrades, and Rollback

This is Gamecaden 0.2.0, including current project bodies, material navigation, evidence retention, phased planning, and a unified tool-environment entry point. First-party code and documentation are provided under [MIT](LICENSE); see [notices](THIRD_PARTY_NOTICES.md) for third-party licenses. The plugin provides eight responsibilities: flow / init / brainstorm / design / develop / assets / verify / close. The standalone Skill reads these through the package-root [gamecaden entry point](SKILL.md). Read actual names back from the host. Workflow records retain adopted projects' own locations, defaulting to `game-workflow/`, schema v1.

The same complete Gamecaden plugin/package serves English and Chinese users; there is no separate locale installer. English workflow text is complete, with a [Chinese usage guide](https://github.com/immortalbeating/gamecaden/blob/main/README.zh-CN.md). New material documents default to the user's current language, regardless of the language of Skills, templates, input references, or other project files; only an explicit current/user or effective project document-language preference selects another language, and current explicit instructions override older preferences. Existing documents retain their language unless conversion is requested. Set project communication and document preferences separately under [language preferences](shared/workspace.md#6-language-preferences). English is the canonical workflow development and maintenance language; panel controls currently remain Chinese.

<a id="codex插件安装与更新"></a>
## Codex Plugin Installation and Updates

```powershell
codex plugin marketplace add immortalbeating/gamecaden
codex plugin add "gamecaden@gamecaden" --json
```

Ordinary installation tracks the repository's default main branch. To update, run `codex plugin marketplace upgrade gamecaden`, then `codex plugin add gamecaden@gamecaden --json`; no new version number is needed, and this does not mean background automatic updates.

Optionally use `--ref v0.2.0` to pin a version; updates to a pinned tag still read that tag. To switch an existing pinned source to the default branch, explicitly remove the old gamecaden marketplace registration before adding it with the commands above; handle other local trial sources separately. See [public installation instructions](https://github.com/immortalbeating/gamecaden/blob/main/docs/installation.md) for complete steps.

<a id="claude-code插件"></a>
## Claude Code Plugin

```sh
claude plugin marketplace add immortalbeating/gamecaden
claude plugin install gamecaden@gamecaden --scope user
```

Update with `claude plugin marketplace update gamecaden`, then `claude plugin update gamecaden@gamecaden --scope user`. Interactive sessions also support `/plugin marketplace add` and `/plugin install`; open a new session or use `/reload-plugins` after installation. Use `--scope project` when project-level installation is selected.

<a id="独立skill与完整目录"></a>
## Standalone Skill and Complete Directory

Install the complete package with Vercel's general Skills CLI. The following example uses user-level Codex; change agent to claude-code for Claude Code, and omit global for the current project:

```sh
npx skills add https://github.com/immortalbeating/gamecaden/tree/main/plugins/gamecaden --skill gamecaden --agent codex --global
npx skills update gamecaden --global
```

This is an npm-provided installer, not Gamecaden's own npm registry package. Alternatively, clone with Git and copy this entire directory to the host's Skill directory; copying only the eight responsibility directories loses shared documents and tools. See [public installation instructions](https://github.com/immortalbeating/gamecaden/blob/main/docs/installation.md) for installation scope, copy mode, and manual updates.

After installation, open a new session to check entry points and actual versions. Projects adopt through explicit Gamecaden invocation or effective project guidance, usually completing adoption with init; a single responsibility invocation stays within current scope. Codex project guidance uses AGENTS.md, and Claude Code uses CLAUDE.md. Reading Skills needs no Python; before actual project adoption, the first local I/O, or panel startup, separately check and prepare the environment under [tool readiness and invocation](shared/local-io.md#1-environment-and-invocation).

<a id="构建与准备安装源"></a>
## Build and Prepare Installation Sources

Requires Python 3.12+. Distribution tools use the standard library; see [local I/O](shared/local-io.md#1-environment-and-invocation) for I/O and panel environment preparation. Fill `$python`, `$bundle`, `$releaseRoot`, and `$installRoot` with confirmed absolute paths; the output directory must not yet exist, and the caller must explicitly specify the installation root.

```powershell
& $python "$bundle/scripts/gamecaden.py" build --source $bundle --output $releaseRoot
& $python "$bundle/scripts/gamecaden.py" verify --package "$releaseRoot/plugins/gamecaden"
& $python "$bundle/scripts/gamecaden.py" stage --package "$releaseRoot/plugins/gamecaden" --target-root $installRoot
```

build generates Codex and Claude catalogs; stage returns marketplace_name and current.source_path, managing only Codex installation sources without performing host-cache installation. Directories use `plugins/gamecaden/<content-digest>`; the same version permits only identical content. Runtime state does not reside inside the plugin.

<a id="宿主安装与发现"></a>
## Host Installation and Discovery

```powershell
codex plugin marketplace add $installRoot
codex plugin add "gamecaden@<marketplace_name-returned-by-stage>" --json
```

Codex installs its own cache copy. Check actual paths and versions of all eight Skills in a new session; an existing session's list does not prove the new package loaded. Candidate validation uses an independent `CODEX_HOME`; ordinary user installation uses the actual user environment. Check source preparation, cache installation, session discovery, and behavioral continuation separately. See [plugin packaging and installation](https://developers.openai.com/plugins/build/plugins) for the official entry point.

[check_codex_discovery.py](scripts/check_codex_discovery.py) can start a new app-server for explicit codex-home / project-root paths and verify the eight actual cache entry points and file digests. It checks only host discovery, sends no model requests, and does not prove natural-language continuation executed.

Bodies and templates can be read directly. Tools/panels use the bundled standard-library launcher; first check the actual installed package root:

```powershell
& $python -B "$pluginRoot/scripts/gamecaden_runtime.py" check
& $python -B "$pluginRoot/scripts/gamecaden_runtime.py" setup
& $python -B "$pluginRoot/scripts/gamecaden_runtime.py" run contracts
```

`$python` is Python 3.12+, and `$pluginRoot` is the actual complete installed package root. See [local I/O](shared/local-io.md#1-environment-and-invocation) for environment caching, existing-Python reuse, disabling automatic installation, and failure handling. Verify resource installation, session discovery, and tool readiness separately. Panel configuration and connection materials reside in an independent host state directory under the [panel contract](panels/README.md); this package does not automatically install an MCP service.

<a id="升级与恢复"></a>
## Upgrades and Recovery

After source revisions, increment the manifest version or generate a candidate using `--version <new-version>` during build. After verify passes, stage to the same installation root, then run the native Codex installation commands above and check the cache and a new session.

```powershell
& $python "$bundle/scripts/gamecaden.py" status --target-root $installRoot
& $python "$bundle/scripts/gamecaden.py" rollback --target-root $installRoot
& $python "$bundle/scripts/gamecaden.py" recover --target-root $installRoot
```

rollback switches to the previous package; rolling back the first deployment returns to undeployed state, retaining old packages. Refresh host installation after rollback; first-deployment withdrawal also requires `codex plugin remove` according to the actual host. status is read-only; recover completes original operations only when pending transactions' before/after bytes still match. With external changes, retain materials and report conflicts rather than forcing overwrites.

OS locks coordinate this tool's processes; external editors do not participate. Tools check observable revision changes, but a race window remains between the final comparison and file replacement; no multi-file transaction guarantees are made for network drives, power loss, or arbitrary noncooperating editors.

`.gamecaden-install/` stores installation locks, history, and recovery receipts, not game progress. Public package upgrades do not rewrite project designs, records, adopted rules, acceptance states, or saves. Handle project adoption and legacy-workflow migration within [init](skills/init/SKILL.md)'s separate scope.
