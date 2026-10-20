<a id="读写接口-v1来源预期版本与回读"></a>
# Read/write interface v1: sources, expected versions, and read-back

Status: the local interface contract accompanying formats-v1. All 14 operations are implemented by the Python library/CLI. See the [local read/write tools](local-io.md) for invocation, capabilities, and recovery. These names are JSON operations, not evidence that the current host has installed MCP tools of the same names; panel/host integration is validated separately.

<a id="1-同一来源不同读取表面"></a>
## 1. One source, different reading surfaces

Persistent document forms are defined in the [format contract](formats-v1.md). The interface reads source files and returns readable bodies, necessary structure, references, and source-file revisions; frontends/models consume the same result. Normalized read models are derived data, not written back as another task.json, approval-status table, or current Git database.

Read results should state actual location, record ID/source, recognized format, available capabilities, revision, and limitations. Unknown legacy formats may return original text and diagnostics; explicitly report unsupported writes when no write adapter exists. owner labels and adapter names neither grant permission nor prove capabilities exist.

Successful record.read/resolve data contains ref/path/reference_base/format/interpretation/revision/metadata/body/capabilities/diagnostics. interpretation distinguishes native, adapted, and raw-text-only reading. ref returns canonical identity; external raw text without a resolvable ID uses the resolved absolute path rather than echoing a relative path of unclear base. path is the actual carrier file; reference_base is the base for structured references in returned metadata/body, or null when it cannot be determined for external formats. capabilities describes operations actually implemented, not current authorization. List-item metadata also declares reference_base. Lists return items, next_cursor, complete, source_revisions, and diagnostics. complete indicates whether source scanning is complete; a next_cursor means results are still unread. Source changes during pagination return stale_cursor or an explicit new snapshot rather than silently omitting records.

When the carrier is known, a path-based read/resolve checks that file, its mapped source, followed references and pending writes without scanning unrelated collections. Its revision checks cover the workspace and files actually read, not a project-wide audit. ID-only lookup still enumerates the identity set to detect ambiguous bodies/forwards; record.list, workspace.inspect and numbering checks retain full discovery. A located read does not establish that other records are valid.

Located record.update/transition operations bind the workspace, target, supplied preconditions and actual semantic dependencies. Parent-Epic or other ID references may still require complete identity discovery. Unrelated producer files do not become dependencies merely because they are registered. Complete discovery also checks source membership as well as bytes, so an added or removed source during reading cannot silently preserve the old snapshot.

Invocation targets are always existing sources or locations authorized for creation. Check context project_root/workspace/base_dir against the actual current authorized target before resolving references. User-supplied path, source, or actor fields do not expand permissions.

Structured Ref.path values in requests resolve against context.base_dir. When writing a target file, tools must convert them to persistent references relative to that file. When returning read metadata unchanged, callers may set base_dir to the original record directory. Callers prepare and validate body Markdown/native blocks against the target file's base; do not blindly paste relative links from another file. Path conversion neither changes referenced objects nor relaxes boundary restrictions.

context.project_root is an absolute root; relative context.workspace/base_dir values resolve against it. The Workspace document's own root/path/marker values remain based on the target workspace.yaml directory. Do not guess that unstructured body/extension data is a Ref merely because it resembles {path: ...}.

complete indicates whether structural enumeration of records in declared sources is finished; raw sources without structural adaptation cannot establish this. Diagnostics such as duplicate identities or unsettled operations are returned separately and do not uniformly mean scanning is incomplete. Readers must still handle them; complete alone does not permit progression or closure.

<a id="2-请求与结果信封"></a>
## 2. Request and response envelopes

The Request schema contains protocol_version=1, request_id, operation, context, payload. Writes must also explicitly provide preconditions and, when needed, expected_subjects.

request_id also serves as the retry key for the same logical write. Retry the same request with the same ID; different content using the same ID returns a conflict rather than overwriting the original operation. After a confirmed failure, use a new ID for an intentional request change. When the outcome is unknown, query the original operation before retrying under another ID.

request_id_conflict responses omit receipt to prevent mistaking an old successful receipt for application of the current different content. They return only the conflict and the fact that this request did not write. To inspect the old request, explicitly call operation.status, which returns its original digest and result.

The idempotency index uses scope_id for the actual authorized project/write scope together with request_id. The server resolves the real binding for scope_id; it does not accept client-proclaimed permission. Store the SHA-256 of the normalized request: exclude request_id, use UTF-8 for resolved JSON, sort object keys, use compact separators, preserve array order, and reject NaN/Infinity. The fixed v1 self-check calculation is json.dumps(ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False). The digest includes operation, context, preconditions, expected_subjects, and payload; clients need not calculate an authorization digest themselves. Changed request content cannot reuse an old ID.

preconditions bind revisions of actual source files about to be read/modified/written. expected_revision:null only expects the target not to exist; it does not skip checks. Updating an existing source requires its corresponding revision; multi-file operations must cover every source that will change. When tools allocate new IDs/paths, they check final-target absence within the locked scope; clients cannot claim creation succeeded in advance.

expected_subjects additionally binds the versions and scope of subjects currently reviewed/selected, addressing unchanged source records with changed media. Recording genuine historical decisions preserves their original subjects; it does not automatically establish applicability to current candidates. If specified versions cannot be satisfied, return version_mismatch rather than silently switching to latest.

Responses retain request_id/operation, use status ok/conflict/rejected/partial/indeterminate, and return actual data, writes, errors, marking replayed when needed. These describe operation outcomes, not Task lifecycles or product acceptance.

Each writes entry identifies its object, written/unchanged/failed/not_attempted, and verifiable before/after revisions. Complete actual writes and read-back before returning ok; merely generating a proposal or saving a browser draft cannot return authoritative write success.

WriteResult may explain recovery observations through note. If current bytes match the target but no verified write record exists, use unchanged without claiming knowledge of who wrote them. If an original written result was externally restored/changed, unsettled operations report a conflict and preserve that change.

Paths used for operation location in responses (including path references in writes, errors, source_revisions, allocations, and recovery_actions) are resolved absolute paths. They do not depend on the recipient's current directory or a new base_dir used when querying operation.status. Raw text/metadata in read results still follows declared reference_base; do not conflate the two.

Write ok/partial results and successful operation.status queries must also return receipt: original request_id/operation, scope_id, request_digest, prepared/applying/settled phase, outcome, allocated objects, and recovery_actions. It describes one file operation, not a business-workflow state. operation.status writes describes write results of the queried original operation, not files written by the query itself. The original request_id in receipt is separate from the query request ID.

allocations lists only Task/Epic/Evidence/Decision/Asset allocations of stable management IDs. Creation of development-plan/attachment/design/plan/history/handoff files without independent management IDs reports actual locations through writes, without adding management entities through receipts.

<a id="3-操作目录"></a>
## 3. Operation catalog

| Operation | Input and responsibility | What success establishes |
|---|---|---|
| workspace.inspect | Inspect the specified root, entry points, sources, formats, and capabilities; an existing workspace is not required | Returns locations and gaps; does not initialize or migrate |
| workspace.configure | Save authorized mappings referencing existing bodies; check default/duplicate sources and rule scope | Mappings were written back; does not prove the game is ready |
| record.list/read/resolve | Read original records or explicit forwards within scope; return body, metadata, revision | Actual sources are readable, with unknowns explained |
| record.create | Create at a valid location according to object format, allocating or checking identity; supports native embedded Evidence | New record actually exists; does not prove its business conclusion |
| record.update | Edit permitted metadata/body, preserving identity and unrelated content | Specified changes were saved; does not implicitly convert states or legacy formats |
| record.transition | Handle only Task/Epic lifecycles, with specific reasons and related-record references | State was saved according to that request; does not prove acceptance or parent completion |
| record.extract | Extract machine-readable embedded records into independent files, preserving IDs and forwarding old locations | Specified extraction completed; partial failures are returned separately |
| decision.record | Create a Decision or append formal events to the same record, independently or embedded | Actual decisions were recorded; does not imply engineering adoption |
| asset.upsert | Explicit create/update; maintain asset identity, sources, and candidate indexes, preserving existing selection relationships | Registers real changes; does not generate assets or batch-accept them |
| asset.select | set designates/replaces a relationship for a use_id; clear removes that designation; save reasons and basis | Designated relationship was saved; does not change acceptance or consumer references |
| view.build | Build progress/history/asset read models from actual sources, optionally saving views | Returns/saves derived results without creating facts |
| operation.status | Query writes, partial results, and recovery conditions by original request_id | Explains operation results; receipts are not Task sources of truth |

record.update does not change native IDs, bypass record.transition to alter Task/Epic states, or overwrite used Decision events or Evidence results. Draft prose may be edited; formal-event corrections/replacements follow their record rules. Explicit format transfer remains init/migrate rather than being hidden in update.

Rewriting carrier-file bodies (including record.update/transition) also checks native embedded blocks. Whole-body replacement cannot delete formal events, change substantive Evidence subjects/results, or reassign identities. Format/base conversion is relocation preserving meaning; substantive evidence corrections use new records referencing originals. After allocating default IDs, record.create must still validate complete metadata against the target record format; passing the Request envelope alone does not establish that saving is valid.

record.create development-plan creates a project/version-level [PDP](phased-development.md), without a Task/Epic owner, ID allocation, or lifecycle. When path is omitted, provide metadata.title; the default location is plans/<safe-title>.md. Return an actual source-registration proposal; registration and creation are read back separately. Title changes do not relocate files; subsequent operations use the original path.

attachment/design/plan/history remain attached to real Task/Epic objects: attachment provides owner and an explicit `.md` path inside that work's attachment directory or subdirectories; design/plan/history must also locate owner. Higher-level PDPs do not expand the scope of these existing attachment types. handoff provides real source_refs and snapshot_scope; sources participate in current read checks. Default paths and retention for regeneration follow [independent handoff](derived-outputs.md#standalone-handoff). None of these documents adds management entities or lifecycles. Body splitting follows the recovery principle of preparing the target first, then switching original prose to explanation/references, with per-item read-back; creating a copy does not establish completed extraction.

Before modifying any authoritative source file, all writes re-resolve actual targets/sources and check current write capabilities, formats, and authorization. Do not trust capabilities asserted by requests. raw sources or missing write adapters return unsupported_write with not_attempted for each target. If sources migrate/change after reading, recheck actual locations and write preconditions instead of blindly writing old prose into another source. Operation locks/receipts are local recovery materials, not proof of authoritative writes.

After creating documents/ledgers at new locations not occupied by existing sources, mark source_registration_required if their sources remain unregistered, returning source_proposal when needed. init then saves mappings through workspace.configure. Creation does not implicitly change default sources; do not claim new IDs resolve in existing sources before registration.

decision.record targets/subjects must match the actual current decision. Recording time follows write facts; retain unknown actual decision time as unknown. Actual hosts must verify panel identity and user input; client actor:user does not establish human approval. Directly recording an existing decision does not require the user to approve the same choice again.

asset.upsert create may omit id, which tools allocate and return; supplied IDs must be unused and new selected_uses must be empty. update must specify an existing id, and selected_uses must match existing values; only asset.select maintains designated relationships within its scope. Candidate IDs are not reused for different substantive content; old versions retain their references. Actual generation, processing, engine wiring, and Git actions use dedicated capabilities, writing results back to these existing sources rather than pretending to execute them through this interface.

asset.select explicitly uses action=set/clear. set provides a complete use (including use_id); clear provides only an existing use_id and removes the current designated relationship. Both require reason and, when needed, basis referencing actual decisions/work; original work preserves impacts and historical disposition. clear does not delete assets/candidates, withdraw original acceptance, or roll back engineering integration already performed.

Before Task transitions, the calling Skill checks original scope, valid evidence, necessary acceptance, and Git destination. Tools check structure, references, and permitted operation scope; status fields or JSON Schema passing alone cannot replace close's delivery judgment.

view.build may use empty preconditions when only returning data; saving must protect the actual output target. Without reliable body parsing/engine observation, retain original text or unknown/needs_review. Do not infer Epic completion from closed counts or quality from asset counts.

Actual read-model coverage and saving follow [derived outputs](derived-outputs.md#views-and-views): current progress summarizes only Task/Epic; timeline summarizes Task/Epic/Decision/Evidence; assets summarizes asset identity. The panel reads sources live; saving JSON is not a startup prerequisite. Full milestone/Stage judgment returns to the original Roadmap/PDP and basis. Current view.build generates neither Markdown nor complete static panel HTML.

New Tasks without specified original paths default to `tasks/T-<number>-<short-name>/task.md`. The safe short name comes from title at creation; see [record conventions](records.md#2-selecting-and-creating-work). Later title changes do not relocate files. Original main files and `tasks/T-<number>/` attachment directories for legacy flat Tasks remain in use; explicit paths are not automatically migrated.

<a id="4-编号并发和写入顺序"></a>
## 4. Numbering, concurrency, and write order

When creating native IDs, check active, cancelled, and retained historical records in the actual project's ID space for the same type. Generated numbers default to at least three digits. ID allocation and new-file creation require coordinated protection; create-exclusive on different filenames alone cannot prevent two T-001 IDs. Retrying the same request must not allocate a second ID.

Before formal writes, save the request digest, bound scope, allocations, and intended targets as a prepared receipt. Apply file writes only after the receipt is recoverable. Updates to applying/settled preserve actual results for every target. Reuse existing allocations found for the same request rather than taking the next number. Implementations without durable allocation/recovery guarantees must not claim idempotent creation.

Check source revisions and target semantics before writing, then read back. Same-file conflicts return conflict and current location information, preserving the user's submitted content for renewed comparison. Do not automatically apply old-page values to a new version and treat them as the same approval.

Single-file writes may use same-directory staging and applicable atomic replacement, preserving valid encoding/line endings, metadata, and unrelated prose. Atomic replacement is not a version check; appropriate locking/consistency protection is still required between reading and committing.

Do not claim multi-file writes are inherently atomic transactions. Operations such as record.extract should prepare recoverable content, read back each actual write, then complete forwarding. On interruption, report completed/uncompleted parts and next steps. Reads of committing/conflicting records return explicit limitations; do not guess the source of truth from the newest timestamp.

record.extract must protect the source carrier and target files (expect absence for a new target), binding both in the prepared receipt. First prepare target content with the same ID and correct new relative references. Only after writing and reading back the target may the original block become a forward; then check the unique body/forward. Deleting source prose before attempting the target write is prohibited. On interruption, receipt.recovery_actions should identify read_back, finish_extract, or conflict checks and specific objects. When temporary duplicate bodies are found, readers report operation_pending/ambiguity rather than count both as valid records.

When external edits clearly prevent the original attempt from continuing under old preconditions, preserve per-item results and settle as conflict/partial. Extraction recovery may reference a settled partial extraction through payload.recovery_of in a new request, supplying new revisions for source and existing target. Reuse only with the same source/target/ID and matching target content; do not overwrite target differences. This preserves user-added prose without requiring deletion of a valid generated target.

Extraction relocates structured Refs and recognizable relative Markdown links. Body references that cannot be reliably converted must retain their original base or be prepared by the caller; do not merely move files and let identical links point elsewhere.

Implementations may retain locks, staging, request_id receipts, and other operation metadata. These support only concurrency/recovery and do not own Task states, human acceptance, or runtime adoption. Resolve pending outcomes before clearing operation materials; authoritative facts still come from original documents.

Automatic retries occur only within original authorization while source/object conditions still hold. On conflict, first read the new state and differences, then decide whether to resubmit. Do not bypass conflicts through unconditional overwrites, renumbering, or deleting others' changes.

<a id="5-模型如何使用自由正文"></a>
## 5. How models use free prose

Templates provide recommended structure, but formats do not require identical section headings for every Task. Readers may return recognized passages; when reliable location is impossible, return the complete body. Updates should preserve passages and optional extensions outside the current change rather than guess from headings and delete other content.

Use explicit anchors or native record blocks for independently addressable entries. Ordinary Task progression restrictions, next steps, and actual results may remain prose; tools cannot automatically execute solely from active without understanding these conditions.

Models judge semantic gaps from original materials, clarifying when necessary; tools report specific field/reference problems for structural errors. Do not elevate every risk or ambiguous phrase into a new global field, extra approval, or aggregate state file.

<a id="6-错误与恢复输出"></a>
## 6. Errors and recovery output

Distinguish at least: not_found, ambiguous_ref, duplicate_id, unsupported_format, unsupported_write, invalid_record, invalid_transition, invalid_scope, precondition_required, revision_conflict, version_mismatch, permission_denied, request_id_conflict, stale_cursor, operation_pending, write_failed, partial_write, indeterminate.

Errors explain affected objects, portions already performed, currently verifiable state, and next steps. Missing tools, missing records, and different original formats are distinct situations; do not display all as “project not initialized.”

When operation outcomes are unclear, check operation.status/actual sources. An unavailable receipt does not mean no write occurred. If safe replay cannot be determined, preserve the scene and specify the gap first. Continue using other completed, still-valid results without redoing all work.

<a id="7-实现与验证边界"></a>
## 7. Implementation and validation boundaries

Local implementation and executable checks are provided; supported scope follows the [tool documentation](local-io.md). Record actual tests separately from pure schema checks. Local CLI validation does not prove completion of engine consumers, browser/host user identity, network services, or plugin installation.
