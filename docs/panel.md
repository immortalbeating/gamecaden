<a id="本地面板"></a>

# Local Panel

The panel is an optional local tool shared by the eight responsibilities. It reads registered project sources and provides work entry points, original-text reading, governance relationships, asset previews, and review recovery. Read-only by default, the service listens only on `127.0.0.1`.

Panel reads do not require saving `views/` files first. See [derived outputs](../plugins/gamecaden/shared/derived-outputs.md) for on-demand JSON snapshots, current-summary refresh, and standalone handoff responsibilities; current JSON tools do not provide complete panel static HTML export. Roadmap/PDP original text can be read, while outcome or stage relationships enter relationship graphs only when actually declared structurally.

<a id="准备与启动"></a>

## Preparation and Startup

Requires Python 3.12+; see [local I/O](../plugins/gamecaden/shared/local-io.md#1-environment-and-invocation) for environment preparation. Run the following PowerShell example from the repository root:

```powershell
python -B plugins/gamecaden/scripts/gamecaden_runtime.py check
python -B plugins/gamecaden/scripts/gamecaden_runtime.py setup
$gcState = Join-Path $env:LOCALAPPDATA 'Gamecaden/panel-state'
New-Item -ItemType Directory -Force -Path $gcState | Out-Null
$gcConfig = Join-Path $gcState 'host-config.json'
Copy-Item plugins/gamecaden/panels/host-config.example.json $gcConfig
```

Edit your own configuration copy with actual project roots, workspace, or explicitly registered legacy sources, and remove unused example projects. Keep the example write permissions disabled; start after confirming sources are readable:

```powershell
python -B plugins/gamecaden/scripts/gamecaden_runtime.py run panel --config $gcConfig --state-dir $gcState --port 8875
```

On POSIX, choose independent configuration and state directories of your own. For installed copies, replace the relative paths above with the actual plugin root. See the [example](../plugins/gamecaden/panels/host-config.example.json) for configuration format.

Open the browser with the complete connection URL in the state directory's `private/connection.json`. Do not put connection secrets in public instructions, screenshots, or receipts; work deep links carry only project and object positioning information. Stop the service by stopping the launcher process. On restart, reuse the same trusted state directory and read new connection materials.

<a id="使用边界"></a>

## Usage Boundaries

state-dir sits outside business sources and belongs to the trusted launcher; it stores host state, signatures, and connection materials. Host configuration separately authorizes Task bodies, decisions, and designation of existing asset uses, and the launcher also binds identities. The page cannot choose recorders or change project roots.

Page data covers only registered scope; original record states are not inferred from Markdown bodies as completion percentages. Previews and media playback cannot replace engine effects or gameplay acceptance. Maintain technical checks, asset decisions, use designations, and runtime adoption separately.

<a id="冲突与恢复"></a>

## Conflicts and Recovery

Writes first obtain signed snapshots and submit stable request_id values; after network interruption, query original-request receipts before recovering original payloads. Receipts prove only results at that time; current facts still need rereading. On conflict, retain drafts and check current sources, then prepare new operations after explicit baseline comparison; pending frozen requests retain original payloads.

See the [bundled panel instructions](../plugins/gamecaden/panels/README.md), [panel continuation](../plugins/gamecaden/shared/panel-workflow.md), and [local I/O](../plugins/gamecaden/shared/local-io.md) for further operations and semantics.
