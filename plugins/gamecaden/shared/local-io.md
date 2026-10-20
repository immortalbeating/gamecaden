<a id="本地读写工具调用与恢复"></a>
# Local read/write tools: invocation and recovery

The current implementation provides a Python library and command-line entry point, using the 14 operations in the [v1 interface contract](io-v1.md). [Step 14's local HTTP host](../panels/README.md) reuses the same library and provides controlled panel access through separate startup configuration; it does not automatically modify Codex host configuration or install an MCP service.

Derived reading of materials, conditions, and relationships is provided separately by [workflow_governance.py](../scripts/workflow_governance.py). It is not a fifteenth core write operation and maintains no new business state. Fields, CLI, and panel usage are documented in [governance](governance.md) and [panel integration](panel-workflow.md).

<a id="1-环境与调用"></a>
## 1. Environment and invocation

This section governs tool readiness and invocation. Reading Skill prose, read-only consultation, or init's on-site inspect does not require preparing Python dependencies. Before actually adopting the workflow for a project, performing the first local I/O, or starting the panel, confirm the actual installed bundle root and check the tool environment. If inspect itself invokes local tools, follow this section as well, without automatically installing or writing project guidance as a consequence.

[gamecaden_runtime.py](../scripts/gamecaden_runtime.py) is a standard-library launcher requiring an existing system Python 3.12+. It prepares an isolated environment for [requirements.txt](../scripts/requirements.txt), without modifying global Python or placing a venv in plugin caches or game projects. Missing/outdated Python first requires the host to prepare Python 3.12+. Retain explicit errors for network, download-source, or directory-permission failures; do not promise unconditional success.

```powershell
& $python -B "$bundle/scripts/gamecaden_runtime.py" check
& $python -B "$bundle/scripts/gamecaden_runtime.py" setup
& $python -B "$bundle/scripts/gamecaden_runtime.py" run io --project-root $gameRoot --request $requestFile
```

`check` is read-only; `setup` prepares idempotently. Both return JSON. Check `status`, `ready`, `python_executable`, and `dependencies`; `ready=true` confirms the tool environment. `run` automatically prepares missing dependencies before continuing the original invocation. Preparation logs go to stderr; normal business stdout returns only the original tool output. Preparation failure returns an explicit not-ready error without calling the business tool.

Default caches are Windows `%LOCALAPPDATA%/Gamecaden/runtimes`, macOS `~/Library/Caches/Gamecaden/runtimes`, and Linux `${XDG_CACHE_HOME:-~/.cache}/Gamecaden/runtimes`. Set `GAMECADEN_RUNTIME_HOME` or `--runtime-home DIR` to specify a cache directory. Environments are isolated by requirements bytes, Python implementation and major/minor version, platform, and architecture; dependency-file changes select a new environment.

Managed installation ignores pip configuration files and target, prefix, and user-install overrides, first confirming that the interpreter belongs to the isolated environment. Download sources, proxies, and certificates may be provided through corresponding environment parameters such as `PIP_INDEX_URL`, `PIP_PROXY`, and `PIP_CERT`. Existing direct legacy CLI calls also route through this launcher when dependencies are missing; importing the library does not automatically prepare them. Requesting only `--help` with missing dependencies returns readiness diagnostics without downloading dependencies.

Reuse an already-ready Python through `check --python PATH` or `run --python PATH io ...`. Missing dependencies in an external Python return an explicit error; pip installation into it is not automatic. To prohibit automatic download/preparation, use:

```powershell
& $python -B "$bundle/scripts/gamecaden_runtime.py" run --no-install io --project-root $gameRoot --request $requestFile
```

`--runtime-home` applies to check/setup/run. Place run launcher options before the tool name. Supported tools are `io`, `governance`, `panel`, `contracts`; arguments after the tool name pass unchanged to that entry point. Examples: `run governance --project-root ... --focus T-003`, `run panel --config ... --state-dir ... --port 8875`, `run contracts`.

Here `$python` is a Python 3.12+ launcher, `$bundle` is the actual complete installed bundle root, `$gameRoot` is the confirmed project root, and `$requestFile` is UTF-8 JSON containing actual context. I/O arguments, exit codes, and stdin/stdout retain the [workflow_io.py](../scripts/workflow_io.py) interface: `--request` accepts a UTF-8 JSON request file or `-` (stdin); success exits with 0, rejection/conflict/incompletion with 2, and stdout returns JSON.

After readiness succeeds, still check actual I/O responses and read-back results. Manually saving records is not evidence of validated I/O. If the environment is not ready, report the reason and unfinished scope, preserving the project's original state.

Host arguments bind the project root; request context cannot expand it. context.project_root uses an absolute path; relative context.workspace and base_dir values resolve against that root. Business payload/Ref paths use base_dir, or the project root when omitted. Mapping paths in the Workspace document itself always use the target workspace.yaml as their base. Callers prepare relative paths in bodies/unstructured metadata against the target document.

Example request:

```json
{
  "protocol_version": 1,
  "request_id": "read-located-task",
  "operation": "record.read",
  "context": {"project_root": "C:/Games/MyGame"},
  "payload": {"target": {"path": "game-workflow/tasks/T-002-example/task.md"}}
}
```

Replace example roots and paths with actual values from the located project. C:/ExampleGame in examples/v1/io is a format example, not a local execution target. Invalid JSON syntax, non-object top levels, or unrecognized request envelopes return concise invalid_request/error results rather than masquerading as successful responses from valid operations.

Use the known carrier path for a located read; ID-only lookup and full discovery have different scan scopes under the [read contract](io-v1.md#1-one-source-different-reading-surfaces).

<a id="2-实际能力"></a>
## 2. Actual capabilities

| Operation group | Local implementation |
|---|---|
| workspace.inspect/configure | Recognize existing mappings, native default locations, sources, and gaps; conditionally save mappings, preserving YAML comments |
| record.list/read/resolve | Native/embedded records/forwards, raw-text reading, absolute locations and reference bases, pagination and change detection |
| record.create/update/transition | Stable numbering, small metadata/bodies, attached documents, lifecycles and recorded reasons; identity/formal-record protection |
| record.extract | Write targets before forwarding sources; relocate relative references, read back interruptions, and explicitly repair conflicts |
| decision.record | Independent/embedded creation, event appends, actual-source validation entry point, cross-Decision replacement and partial-withdrawal scope checks |
| asset.upsert/select | Identity/candidate registration and set/clear designated relationships; validate fallback manifests and actual member bytes |
| view.build | JSON read models for Progress/Timeline/Assets, saveable at existing or specified locations; no inferred pass percentages or runtime adoption |
| operation.status | Read original operation receipts and observable recovery conditions without writing original documents |

Native Markdown/YAML/JSON and UTF-8 (including BOM, CRLF) are implemented. Edits preserve unchanged bodies and YAML comments; serializers handle new structure. Binary objects inside/outside native collections support read-only access by path and digest binding, with null bodies and no formal record identity or write capability. Physical reads/enumeration of long Windows source paths use extended paths; returned logical paths, project boundaries, and link restrictions remain consistent.

Material titles, headings, prose, and readable values may use the user's language; native reading/writing does not translate them or require English headings. Governance excerpts retain the first nonempty actual H2 section in its original language, without deriving status or acceptance from its label. Extracted records retain unrebased code/free-text path provenance as `unrebased_relative_reference_base` data rather than inserting prose in the toolkit's language. Explicit recovery still recognizes the previous Chinese provenance note and preserves an already-written matching target.

Legacy formats without adapters are read-only as raw text. Sources declared native but damaged return specific format errors. Existing sources' external ownership, overlapping interpretations, and source qualifications cannot be bypassed; `owner` is not operation authorization.

Before a workspace exists, explicit deliveries may use native default Task collections. After mappings exist, when adding an unregistered document type/asset ledger, tools may create at new locations not occupied by other sources, returning `source_registration_required` and an available `source_proposal`. init then saves explicit mappings through workspace.configure. Creation does not silently change defaults; before registration, do not assume new IDs belong to existing source lists. Extraction requires an available native target source so the original ID remains resolvable.

<a id="3-正常写入"></a>
## 3. Normal writes

1. Obtain the actual carrier path, reference_base, source-file revision, and current body from record.read/resolve.
2. Preserve the user's current scope and unrelated content while preparing the specified operation. Provide matching revisions for updates or null (expecting absence) for explicit creation targets.
3. Attach expected_subjects when current subject consistency is needed. recorded_at is generated during actual write preparation; unknown decision occurrence time may remain null.
4. Keep request_id and payload unchanged for the same logical request. Check response.status, per-file writes, receipt, and errors; update actual results in current work according to the original Skill rules.

Short records within files, independent records, and Quick/standard share the same protection boundary. record.update also checks formal embedded blocks in its carrier; whole-body replacement cannot bypass dedicated actions. Check source_revision and checked-subject Version separately.

Subdirectories of native numbered collections support ordinary `.md`, `.json`, `.yaml`, `.yml` attachments with natural filenames such as `SOURCE.md`, `FILES.md`. Collection roots retain compatibility with design/plan/history/readme/index names; arbitrary root files are not all attachments. Main task/epic/evidence/decision/asset filenames, filenames beginning with T-/E-/EV-/D-/A- plus digits, and content declaring formal management IDs are still validated as formal records. Task metadata without id but with quick/standard mode and epic cannot be downgraded either. Malformed native blocks and duplicate formal IDs still produce errors.

Object frontmatter in ordinary Markdown attachments retains metadata/body. Producer-local id/status/events may be updated through set_fields; they do not become work identities, lifecycles, or formal events and do not reserve numbered references. Non-object frontmatter retains complete text with null metadata. JSON/YAML attachments without formal identities likewise return full text as body; whole-text updates must remain syntactically valid. Every update still requires reading back the original source; ordinary attachments cannot be converted into formal work records. No `.txt` scanning is added.

`record.create` attachment requires an actual Task/Epic owner and an explicit `.md` path within its actual attachment directory or subdirectories. New Task material directories are the main file's `tasks/T-<number>-<short-name>/`; legacy flat Tasks retain `tasks/T-<number>/`. Later title changes do not move files. Attachments receive no work ID or lifecycle. Before writing, creation validates against the actual source's reading rules; inability to read back returns invalid_record without writing the target. Existing materials retain original bytes and ownership, without automatic migration to impose the new layout.

Project/version-level PDP uses `record.create` with `record_type: development-plan`, without Task/Epic owner, management ID, or transition. Supply `metadata.title` when omitting path; the default is `plans/<safe-title>.md`. Explicit original paths and updates after title changes remain stable. Creation returns a development-plan source proposal; register with `workspace.configure`, then read back/list. Current count and orchestration meaning are still checked against the [PDP contract](phased-development.md).

handoff provides `source_refs` and `snapshot_scope`; tools read actual sources for revision checks and save tool snapshot time. When path is omitted, default names under handoffs/ use UTC date/safe title/time; same-second collisions append a sequence number. Replaying the same request_id returns the original location; new requests retain new snapshots. Scope, prose, and old paths follow [derived outputs](derived-outputs.md); handoffs are not new work entities.

Current automatic content validation supports single-file SHA-256 and SHA-256 for every actual member of this bundle's fallback manifest. Candidate Subjects may obtain implicit proof from their bound candidate.manifest. Current applicability of other producing tools' manifests and git/build/named versions requires corresponding adapters; current requests explicitly return unsupported_format rather than treating unresolved versions as passing. Existing historical records may still preserve these declarations without inventing current validation.

`asset.upsert` creation validates all new candidates; updates protect existing candidate ID/manifest/version and selection relationships, strictly checking new candidates and added references. Results return `validated_candidate_ids` and `historical_candidate_diagnostics`. The latter explains mismatches/unreadability of retained old payloads without converting them to passing. `asset.select set` still checks selected candidates individually. Recovery registration, selection updates, and engineering adoption remain separate; see [candidate snapshots and legacy recovery](asset-handoff.md#candidate-snapshots-and-legacy-recovery).

<a id="4-决定者与接受来源"></a>
## 4. Decision-maker and acceptance sources

The CLI's default recorder is agent/local-cli; `--actor-id` may identify the actual Agent. It may record decisions that Agent owns; payload actor:user cannot impersonate a user choice.

Python callers may provide trusted host identity and a callback through `Workflow(project_root, actor=..., decision_authorizer=...)`. The callback receives the complete event and request and must check actual user input/host events and exact subjects. Request JSON cannot choose the callback. Known user decisions do not require equivalent approval again.

This round's tests validated both rejection of fabricated attribution and explicit host callbacks. The subsequent panel provides [local startup-session binding](panel-bridge-v1.md), without claiming Codex account authentication or proof of a human. CLI identity boundaries remain unchanged. Existing-session decisions may still be saved under original workflow rules.

<a id="5-重试中断与冲突"></a>
## 5. Retries, interruptions, and conflicts

Project-local `.game-workflow-io/` stores locks and operation receipts, not a second Task state. Receipts contain original requests and recovery materials and should remain in the local operating environment. Exclude them from packaging/version control according to project conventions during distribution/onboarding. Tools themselves do not modify .gitignore or execute Git.

Large settled receipts use a lossless, integrity-checked gzip/base64 JSON storage envelope when it is smaller. `Store.load/all` transparently recover the complete original request, guards, plans, results and allocations; operation responses and replay semantics are unchanged. Prepared/applying receipts keep their full original JSON representation. Existing plain receipts remain readable and are not rewritten by reads. The internal envelope requires a reader supporting `gamecaden.operation.gzip-base64.v1`; older package readers cannot consume it, so do not alternate old and new writers on the same operation store. This is storage compression, not deletion or automatic migration of project receipts.

- Unknown request outcome: first operation.status; if continuation is needed and conditions still hold, resend the original request_id and payload.
- Identical request arrives again: reuse original numbers and results. Same ID with changed payload: request_id_conflict; query original results separately.
- Multi-file operation only partly completed: receipts explain each item; recovery checks actual files without recreating Tasks or clearing existing results.
- Original operation confirmed to encounter external edits: preserve external content and end that conflict attempt; use new revisions and a new request for rechecked changes.
- Extraction encounters external source edits after writing the target: original receipt is settled/partial. A new record.extract supplies `recovery_of`, source path/original embedded ID, original target, and new revisions for both. Reuse only the same original operation, same ID, and matching target content, then switch the source to a forward.

`written` means verified evidence of a write by this operation exists. After a crash, when only target bytes are observable and attribution is unconfirmed, return unchanged with an explanatory note; identical content coincidentally written externally is not counted as this operation's write. When existing written results are externally restored/changed, queries for unsettled operations identify conflicts and replay preserves the changes.

settled receipts describe original outcomes at the time; read original documents separately for current content. Unsettled operations report recovery observations from the actual scene. Clearing receipts may lose retry deduplication and ID reservation bases, so restore pending operations first. Ordinary cleanup/migration follows existing scope and retention needs.

<a id="6-验证范围与实用边界"></a>
## 6. Validation scope and practical boundaries

Project-level OS locks coordinate this tool's multiple processes and are released by the OS on exit. Source files use pre-write revision comparisons, temporary files, replacement, and read-back; recovery preserves original allocations and per-file outcomes. Windows directory-junction and symbolic-link entry points are currently rejected; an actually supported adaptation is required.

These guarantees cover local cooperative calls. External editors do not participate in project locks. Tools detect observable version changes but cannot include arbitrary non-cooperative editors in the same file transaction. This round did not validate power loss, network drives, or cross-machine writes.

JSON views retain sources, original prose, timestamps, and diagnostics. complete=false when raw sources cannot fully enumerate structured records. Duplicate IDs and unsettled operations are separate diagnostics and do not uniformly change scan completeness. next_cursor indicates remaining pages. Timeline currently provides records/event materials with sources; arbitrary historical narratives in prose are not fabricated into precise timelines.

New view outputs use only JSON/HTML. Current view.build saves only `.json`; existing panels produce HTML by reading actual sources, while static HTML export depends on actual exporter capabilities. Saving is not a panel-startup prerequisite. Progress Task/Epic summaries do not replace full Roadmap/PDP outcome/stage judgments; refreshing and frozen retention follow [derived outputs](derived-outputs.md).

`record.list` items, source_revisions, and diagnostics are each paginated with the same offset/limit. Revision/diagnostic pages may remain after records are exhausted; continue until next_cursor ends. summary provides the full-scan fingerprint, totals for all three categories, and diagnostic counts by code; detail scope is page. Paginated detail is not complete acceptance. Cursors and panel before/after checks use the full-scan fingerprint for the same query; source/query changes invalidate cursors. Full scanning is still needed for consistency; narrow actual scanning through [source registration](workspace.md#2-portable-fields), not silent exclusion based on scope text.

Tools do not run engines, generate assets, or perform Git delivery, and do not replace verify/close judgments. Development tests are in the maintenance repository's [test_workflow_io.py](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/tests/test_workflow_io.py); bundle-local pure contract checks are in [check_contracts.py](../scripts/check_contracts.py).
