<a id="原生文档格式-v1字段正文与引用"></a>
# Native document formats v1: fields, bodies, and references

Status: the v1 native document contract, used by the local read/write tools. Existing object/record responsibilities remain governed by shared rules such as records.md; this page defines the shape of new native records. This contract does not automatically convert existing projects. See the [local tool documentation](local-io.md) for actual capabilities.

Syntax source: [JSON Schema](../schemas/workflow-v1.schema.json); writing blueprints: [template catalog](../templates/catalog.md). JSON Schema checks structure; it cannot prove that a goal is implemented, a report is trustworthy, or the user has accepted it. Read/write actions are defined in the [interface contract](io-v1.md).

<a id="1-文件形态与加载范围"></a>
## 1. File forms and loading scope

| Object | New native form | Machine-readable content and body |
|---|---|---|
| workspace | workspace.yaml | Location, source, and rule mappings; no execution progress |
| Task (quick/standard) | Markdown + YAML frontmatter | The same six required fields; the body explains delivery, results, and continuation |
| Epic | Markdown + frontmatter | id/title/status; the body owns the shared goal and overall exit criteria |
| Vision, Spec, Roadmap, parking lot, Notes, Git rules | Markdown | Readable prose by default; add stable anchors to entries needing stable references |
| PDP (development-plan) | plans/<safe-title>.md | Project/version-level solution orchestration; no management ID, Task/Epic owner, or lifecycle; explicit sources and Stage scope |
| Ordinary task attachment (attachment) | Markdown/JSON/YAML, with natural filenames suited to their purpose | No independent management ID or lifecycle; attached to a real Task/Epic and read as needed |
| design/plan/detailed history/handoff snapshot | Markdown | Attached to the original work or source, without another lifecycle; a snapshot does not become the current source of truth |
| Independent Evidence | Markdown + frontmatter; existing tool reports retain their original format | Metadata binds subjects and check scope; methods/observations belong in the body |
| Independent Decision | Markdown + frontmatter; batch cases may use JSON with the same metadata shape | events store decisions and supplemental/withdrawal/replacement events; long reasons belong in the body |
| Asset Ledger | assets/ledger.yaml | Asset identity, candidate references, and designated uses; existing Markdown ledgers may remain in use |
| manifest | Prefer the specialist tool's native format; the v1 JSON fallback may be used when none exists | File identity and technical facts, without human-acceptance or runtime-adoption switches |
| Progress/Timeline/panel data | JSON read models and HTML display | Show sources, model scope, and generation time; new outputs do not generate MD views; saving and refreshing follow [derived outputs](derived-outputs.md) |

Ordinary attachments in subdirectories of native numbered collections do not require work-record frontmatter. Filenames or content declaring formal records are still validated against the corresponding schema; attachment types cannot conceal missing fields, malformed native blocks, or duplicate formal IDs. See the [local tool documentation](local-io.md#3-normal-writes) for supported attachment reading and creation.

Within these attachment locations, empty JSON outputs and files ending in `.stdout.json` or `.stderr.json` are read-only raw command/producer captures, not formal records. Preserve their original bytes, including failed or empty output; new stdout/stderr captures should use log filenames, with JSON result files reserved for actual serialized results. Explicit native file sources and reserved main-record filenames retain strict parsing; other malformed structured records still report errors.

Read the corresponding schema and template only when creating/modifying that native record type; do not load the entire format library for every Task. Template headings are writing prompts. Remove optional sections with no content; filling every section or generating an entire directory tree at once is not required.

YAML uses values expressible in JSON and prohibits executable tags. Quote ID, version, and date strings. When time is genuinely unknown, retain null and explain it rather than inventing dates. Preserve the original file's free prose, unrelated content, and extension data; formatting must not erase user material.

Native YAML/JSON rejects duplicate keys. Native YAML does not use aliases, anchors, or merge keys to hide overrides. Preserve external legacy formats verbatim and handle them through adapters; do not use native restrictions to clean their content without authorization.

<a id="2-身份路径与版本"></a>
## 2. Identity, paths, and versions

<a id="稳定身份"></a>
### Stable identity

New native Tasks/Epics default to T-001 and E-001; assign EV-001 and D-001 when tools need to locate Evidence/Decision independently; asset families use A-001. Display numbers with at least three digits, growing naturally beyond that. Existing valid shorter numbers are not renumbered during formatting. Native numeric IDs of the same type are unique within the project and never reused; include cancelled/historical entries in checks.

Do not rewrite existing external IDs, file locations, or managers. Native references usually use `{id: "T-001"}`; add project_id for cross-project references and source for external or source-qualified references. Resolve against the actual source; do not select another record merely because it has the same name or a newer date.

Ref has two mutually exclusive forms:

```yaml
{id: "T-001", fragment: "acceptance-focus"}
{path: "../checks/focus-report.json"}
```

id identifies a record; path identifies a located file; fragment identifies an explicit anchor or native record subitem (such as a Decision event_id), not a version. Nested objects are resolved by the declared format/adapter. References containing source/project_id only locate content; they do not expand read or write permissions.

New Tasks default to `tasks/T-<number>-<short-name>/task.md`. The short name is safely derived from title only at creation; later title changes do not relocate the path. Place designs, plans, history, and materials exclusive to this Task in the same directory or subdirectories as needed. Existing flat `tasks/T-<number>-<short-name>.md` files and their `tasks/T-<number>/` attachment directories remain readable/writable; explicit original paths and identities stay unchanged. Full naming rules are in the [record conventions](records.md#2-selecting-and-creating-work).

<a id="路径基准"></a>
### Path bases

- workspace root/path/marker values are relative to the directory containing workspace.yaml.
- Ref.path and relative Markdown links in persistent records are relative to the file carrying the reference.
- manifest.files[].path is relative to that manifest file.
- Business paths in requests are relative to context.base_dir; when omitted, use the confirmed project_root. Relative context.workspace/base_dir values themselves are based on project_root; Workspace document mappings remain based on the target YAML. Tools return actual locations; do not mistake the current shell directory for the reference base.
- External native reports retain the relative base defined by their producing tool, with explicit conversion by the adapter; return unresolved when unknown.

Writes must check the resolved real target, symbolic links/directory junctions, and the current authorized scope. Neither a string prefix nor a mapping owner alone permits crossing boundaries.

<a id="内容版本与源文件修订不同"></a>
### Content versions differ from source-file revisions

Version identifies the version of the subject checked/decided upon, containing kind/value and, when needed, proof referencing a manifest, build, or other verifiable source. kind may be sha256, git-commit, git-tree, build, or named. named is not a substitute for “latest”; it should have a locatable basis. Do not treat an overwritable path as a stable content identity.

The read/write interface revision is `sha256:<64-hex-digits>` of the carrier file's raw bytes, preventing an old page from overwriting newer writes. It is not persisted as a second Task version counter. Matching file revisions do not automatically establish matching media content; asset decisions must also check the content/manifest and file set they actually bind.

Version.kind=sha256 always means the raw-byte digest of one specific file, never a normalized JSON or file-set digest. With proof, the digest target is the file located by that proof; without proof, use the file directly located by Subject.ref or the candidate.manifest bound by an explicit candidate_id. The digest target of AssetCandidate.version is specifically the manifest file located by candidate.manifest. This digest binds only the manifest version; actual content still requires checking each file listed in manifest.files. Even if source revision and object version happen to match, check their respective subjects separately.

<a id="3-workspace-与来源"></a>
## 3. workspace and sources

The Workspace schema retains the established fields: schema_version=1, project, runtime_roots, sources, the two default work sources, and rule_sources.

Each sources entry contains id/role/kind/path/owner and may contain scope, format, adapter. In this native format, format explicitly means native-markdown-v1, native-yaml-v1, native-json-v1, or external. Existing mappings omitting it remain readable, but tools should report recognized formats and actual capabilities rather than assume they can be rewritten as v1.

role categorizes information; scope is a readable description of scope. Current tools do not slice sections according to scope or validate whether free prose adequately fulfills Vision/Spec/Roadmap responsibilities. At formal onboarding, organize current bodies and detailed references according to the [record conventions](records.md#current-project-level-bodies). Valid legacy mapping forms and read compatibility do not mean their content already meets new onboarding requirements.

owner is a maintenance convention, not permission. adapter is only an adaptation identifier, not a guarantee that an implementation exists. Tools return actual capabilities after checking. When an old management source has no write adapter, return its original text and limitations; continue its existing workflow or first complete an authorized transfer.

Each rule_sources entry locates effective rules through id/path/scope; owner is optional. Default Task/Epic sources must point to the correct role. Collections may not yet exist, but a missing record already referenced by specific work cannot be treated as an empty project.

<a id="4-task-与-epic"></a>
## 4. Task and Epic

The six required Task fields remain id/title/mode/kind/status/epic. mode is quick or standard; the lifecycle contains only planned/active/closed/cancelled; epic is one E-ID or null. kind is an open label describing the nature of work; feature, bug, asset, design, validation, maintenance, etc. are recommended. Do not use it to determine validation intensity.

Optional fields: depends_on, related, extensions. Each depends_on entry expresses the required result/condition through target and requires and may reference evidence_refs; it does not uniformly require upstream work to be closed. related only indicates a relationship and grants no permission to advance or close work. A Task's Epic membership and external dependencies remain defined once, in that Task.

Epic metadata contains only id/title/status and optional related/extensions; child membership is aggregated from Task.epic. The Epic body may reference deliverables and explain responsibilities, but adds no independently editable child-status table.

Pause/progression restrictions and resumption conditions remain in the Task's current continuation prose, without adding a paused lifecycle state. Tools return that original passage or the complete body for model judgment. If body headings cannot be recognized reliably, return the original text and a notice; active alone does not establish executability. The panel displays these restrictions; automatic execution must not bypass current user instructions.

The body answers the current goal/boundary, necessary checks, actual results, and continuation according to [modes and record purposes](records.md#selecting-the-management-mode). Maintain solutions and steps when needed; do not mechanically determine body depth from a label. A Task's plan.md owns its internal implementation checklist; existing Epic plans organize deliverable references for that Epic. Project/version-level orchestration uses [PDP](phased-development.md). Its S identifiers and Roadmap M identifiers are document-local anchors, without new management IDs. Keep detailed parameters and original reports at their original references.

## 5. Evidence

When a tool's native report already fulfills the record responsibility, reference it directly. Retention, indexing, and rounds follow [shared records](records.md#retention-indexing-and-versions); do not duplicate Evidence merely to conform to this page. Native independent records require id/title/observed_at/actor/subjects/result/coverage and may have report_refs, corrects, extensions.

observed_at expresses when the check actually occurred, as an explicit date or time; use null when unknown. actor may be null when unknown; do not invent a checker. subjects describe objects and applicable scope; versions must be bound precisely when they affect reuse, acceptance, or batch judgment.

result is passed/failed/inconclusive/not_run/not_applicable. coverage expresses the scope actually supported; it may be empty for not_run, but passing must state what is supported. Put methods, observations, limitations, and gaps in the body or reference the original report. Diagnose metadata/body contradictions rather than choosing whichever passing value is convenient.

Preserve each check result historically. Reruns or substantive corrections use new records; corrects may explicitly reference the original evidence. Native tools do not silently alter old results. For explanatory errata only, append the correction and its basis without rewriting the observations made at the time.

<a id="6-decision-与批量决定"></a>
## 6. Decision and batch decisions

Native Decision uses id/title/events and optional related/extensions. Each event includes:

- event_id: a stable subidentifier unique within that Decision.
- decided_at, recorded_at: the actual decision time (possibly unknown) and recording time; do not conflate them.
- actor: the actual decision-maker, distinguishing user/agent/tool; when recording a user choice, do not identify the recording model as the decision-maker.
- action: choose/accept/reject/revise/defer/waive/withdraw/supersede.
- subjects, scope, conclusion: specific objects/versions, applicable scope, and the actual conclusion.
- basis, replaces: references to the basis and replaced events as needed; native replacement references should locate specific event_id values.

Events already formally used cannot be overwritten or deleted in place. Append supplemental, withdrawal, and replacement events; they may stay in the same file, without creating a new document each time. Ordinary local choices may still be written directly in Task/Epic prose without events.

scope retains a readable explanation; subjects bind actual versions individually. Batch decisions do not imply unlisted members or uses. When an adapter cannot reliably interpret scope, return a need for judgment rather than automatically broadening it. Withdrawing acceptance for one use does not automatically withdraw other uses or roll back engineering work.

Tools must check event_id uniqueness and preserve effective events. replaces may reference another Decision but must resolve to a specific existing event. Replacing a multi-use event cannot directly be interpreted as invalidating every use. A partial withdrawal for a consumer/use must provide the corresponding Subject.use or another explicitly resolvable equivalent scope. Return invalid_scope when it cannot be determined; do not broaden it automatically. Full withdrawal also requires an explicit list of affected scope.

When locating by consumer is necessary, Subject may include use (runtime_id/consumer/purpose and, when needed, baseline), checked against readable scope. Items in the same batch may correspond to different uses; omitting use does not permit all consumers.

actor:user is only data, not proof that the user actually decided. decision.record must rely on actual user input, trusted panel identity/events, or an adopted automatic policy. The recorder and decision-maker should be distinguishable. A chat link alone cannot recover a decision's meaning; conclusion itself must be understandable.

<a id="7-内嵌记录与提取"></a>
## 7. Embedded records and extraction

Ordinary local checks may remain free Markdown, with stable anchors for occasional references; global IDs are not mandatory. For independent tool reading, batch processing, or ongoing references, the following explicit block may be used without requiring a separate file:

````markdown
<!-- workflow:record evidence EV-001 -->
```yaml
id: "EV-001"
# Remaining content matches Evidence frontmatter
```
Body describing methods, observations, and limitations.
<!-- workflow:endrecord EV-001 -->
````

Decision follows the same pattern: replace evidence with decision and use Decision metadata and prose inside the block. Blocks cannot nest; opening/closing IDs and metadata must match. Each native ID can have only one current body.

When extracting to an independent file, preserve the original ID and replace the old block with a forward. The original location no longer retains an editable complete body:

````markdown
<!-- workflow:forward EV-001 -->
```yaml
id: "EV-001"
to: {path: "../evidence/EV-001.md"}
```
<!-- workflow:endforward EV-001 -->
````

A forward is not a second evidence entity. Resolution must check matching target IDs, avoid cycles and multiple valid bodies, and report conflicts rather than choose by date. Old anchor references in ordinary prose retain a readable destination.

<a id="8-资产主台账与-manifest"></a>
## 8. Asset master ledger and manifest

A new native ledger contains schema_version=1 and assets. Each asset contains id/title/purpose, candidates, selected_uses, and optional sources, replacement relationships, and extensions.

A candidate contains its local id, manifest reference, and Version and may reference sources and Evidence. The same candidate ID is not used for another substantive content version. The manifest owns per-file parameters and content digests; the ledger references its identity without manually copying file attributes.

Existing candidate bindings remain immutable; new candidates validate their own manifests and members. For unreadable or mismatched historical payloads, preserve limitations and diagnostics according to [candidate recovery](asset-handoff.md#candidate-snapshots-and-legacy-recovery). Registering a new version does not correct old checks, transfer acceptance, or automatically change selection.

Each selected_uses entry contains use_id, purpose, runtime_id, consumer, candidate_id, with optional baseline and Decision/Evidence references. It expresses designated selection, without approved, adopted, official, or a unified current_version switch. Compare engineering and applicable Evidence to establish actual adoption; display unknown when unobserved, and do not infer success from the ledger.

The default manifest fallback contains asset_id/candidate_id/files; each file provides a relative path, sha256, role, and optional technical properties. When a specialist tool already provides an equivalent format, use an adapter directly rather than copy it. Content-version checks must verify the actual file set that needs proof, not just the approval JSON's own hash.

Candidates may be registered before selected_uses exist; do not create empty fictitious relationships when consumers or uses required for selection are unclear. Create ledger entries only when actual independent tracking is needed, not for every frame or temporary output.

<a id="9-格式验证与语义判断"></a>
## 9. Format validation and semantic judgment

JSON Schema checks types, required fields, and defined enums. Parsers/tools or the calling Skill must also check: ID uniqueness and non-reuse, reference resolution, matching default sources, dependency conditions, ownership of each fact, non-overwriting of decision events, candidate version identity, write scope, evidence validity, and closure commitments.

Place unknown native fields in extensions with an explicit purpose; retain unknown legacy/future-version content when reading. If reliable modification is impossible, report read-only/adaptation required; do not discard fields and claim a successful upgrade.

Passing schema only establishes valid form. Actual read/write/recovery is validated separately by local tools, with current support documented there. Neither schemas, templates, nor local tests prove panel bridging, engine adaptation, or host installation is complete.
