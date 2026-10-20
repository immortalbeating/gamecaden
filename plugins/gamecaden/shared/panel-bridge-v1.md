<a id="本地面板桥接-v1"></a>
# Local Panel Bridge v1

This layer connects the browser to the existing Workflow library. Original files still own source records; HTTP sessions, signed snapshots, and recovery requests are only operational materials.

<a id="启动与身份"></a>
## Startup and Identity

The launcher registers the project root, native workspace or explicit list of legacy-format files, permitted write actions, and recorder identity. The browser cannot submit another root, actor, or authorization scope.

Read-only by default. When writes are enabled, Task bodies, decisions, and selection of existing asset uses remain separately controlled. Recorders may be agent/tool; user identities require a trusted host callback in the bridge. This implements **local startup session binding**: it is not Codex/ChatGPT account authentication and does not determine whether the operator is human. Automated validation uses a tool identity; automated clicks must not be attributed to actual user acceptance.

Bind only to 127.0.0.1. A one-time startup secret is passed to the page in the URL fragment; the page immediately removes the fragment and exchanges it for an HttpOnly / SameSite cookie and CSRF token. HTTP validates the exact Host / Origin; private data and media require a session, and write requests also require CSRF validation. Arbitrary files and general command execution are not exposed.

<a id="只读接口"></a>
## Read-only Interfaces

- GET /api/session: current session, host-bound identity, projects, and capabilities.
- GET /api/projects/<id>/snapshot: pagination of native records or an explicit list of legacy-format sources.
- GET /api/projects/<id>/revisions: two content-based observations of registered sources and mappings; returns completeness and diagnostics without parsing records. Physical Windows operations use extended paths while returned references remain logical paths. A not-yet-created collection is an observed empty location; creation/removal changes its fingerprint. Missing registered files, wrong source types and failed reads retain diagnostics; this probe does not assess referenced-record validity.
- GET /api/projects/<id>/governance?focus=T-003: derive read-only outcome relationships, material responsibilities, and conditions from registered sources; focus only locates the current object and does not reduce the original graph. See the [governance contract](governance.md) for semantics.
- GET /api/projects/<id>/records/<key>: original text, metadata, revision, format, and capabilities.
- GET /api/projects/<id>/candidates/<key>/<candidate>: manifest technical validation, candidate-level uses, and previewable media.
- GET /api/projects/<id>/media/<key>: registered safe media, checked against current bytes and the registered digest.

key is a server-derived identifier for known records/files, not an arbitrary browser path. Legacy formats are read-only; this does not create a copy of Task state. Free-form bodies are displayed as written, without inferring acceptance or overall progress from the word “passed.”

Snapshot pages and governance reuse one reconstructible in-process model for the current source version. Reuse rechecks actual content, registered membership and pending operations; changed sources invalidate old cursors. Governance consumes the complete model directly, without a page-count limit on provenance. Add `include_records=1` to the governance query to receive `records`, `record_diagnostics` and `records_complete` from that same checked model; omitting it retains the ordinary response. The browser uses this batch instead of separately enumerating all pages. Current limits are 50,000 record rows and 64 MiB of serialized snapshot metadata or governance output; exceeding a limit returns 413 with a diagnostic. These are reader resource bounds, not Task, asset-production or retention quotas.

Version probes use independent read guards and share only simultaneously running observations for the same binding. They do not hold the record/media state lock; later probes read actual bytes again. Source checks retain content and race detection rather than treating unchanged timestamps as proof.

The same derived model can also be obtained read-only through `scripts/workflow_governance.py --project-root ... [--workspace ...] --focus T-003`. The overview displays the current Task, outcome tree, [material responsibilities](material-requirements.md), condition nature/status/proof, and one-hop relationships; source documents remain on separate pages. See [panel coordination](panel-workflow.md) for deep-link positioning and copying continuation summaries. These do not save new authoritative state or wake an Agent.

<a id="写入协议"></a>
## Write Protocol

Preparing an operation returns a signed snapshot ticket. It binds the project, identity, source revision, and exact object/version/use; preparation does not write business files. Submission must carry the ticket and a stable request_id.

- POST .../task/prepare {key, revision} → ticket; .../task/save {ticket, request_id, body} → record.update.
- POST .../review/prepare {asset_key, candidate_id, expected_revision, expected_version, scope, use_id} → ticket; .../review/commit {ticket, request_id, conclusion, note} → decision.record.
- POST .../selection/prepare: likewise binds the candidate and existing use_id; .../selection/commit → asset.select.
- POST .../operation/status {request_id} → original library operation.status.

Decisions are saved independently per member, each with its own request_id and exact scope. The browser aggregates individual receipts rather than inventing a new core batch operation. Only accept/revise/reject are allowed conclusions; defer stays in the draft. The host assigns the actor to events, and expected_subjects and file preconditions are checked together. Selecting a new candidate for an existing use does not carry over the old candidate's acceptance/evidence references.

Frozen tickets, payloads, and request_id values may be saved in browser drafts for the same project to recover transport; they do not represent business success. Retries must resend them unchanged; if the result is unknown, first query the original request. If the source has changed, retain the draft, reread it, and explicitly prepare a new operation; do not automatically replace expected_revision or upgrade to latest.

<a id="返回与限制"></a>
## Responses and Limits

Actual writes return the original Workflow response (including status/writes/errors/receipt) and, where possible, separately retrieve the current source record. Only actual writes/readback support a success conclusion; technical validation, acceptance, designated use, and runtime adoption remain separately displayed.

This layer does not close tasks, run engines, automatically continue Agents, or change Git policy. Specialized media editors and account-level host login belong to later adapters.

<a id="宿主来源核对"></a>
## Host Source Verification

The [official Codex App Server documentation](https://learn.chatgpt.com/docs/app-server) and [plugin authentication documentation](https://developers.openai.com/plugins/build/auth) have been checked. App Server account authentication, transport authentication, and command/file approvals serve distinct purposes; we have not treated account login or command approval as acceptance decisions for these game assets. This phase uses the local trusted launcher model above; an actual host may replace that binding later.
