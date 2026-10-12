<a id="派生视图与交接快照"></a>
# Derived Views and Handoff Snapshots

Original Vision, Spec, Roadmap, PDP, Task/Epic, ledgers, and evidence own the facts. This page unifies the purposes, paths, and refresh responsibilities of derived outputs; read it when an overview, export, or standalone handoff is needed.

<a id="视图与-views"></a>
## Views and views/

A view presents and organizes sources; `views/` is the location for saving derived files on demand. Normally read actual sources through the panel or tools; save snapshots when the user needs sharing, offline materials, handoff, or comparison. Opening the panel does not require generating files first, and initialization or each Task closure does not export by default.

New outputs use JSON data and HTML presentation, without adding Markdown views. The existing `view.build` tool provides JSON read models for Progress/Timeline/Assets: without output_path it only returns data; it saves only when given a protected `.json` path. Progress Task/Epic summaries are not a complete Roadmap/PDP outcome tree; see [panel-workflow](panel-workflow.md) for reading and applicability of the panel governance model. Exports from different models identify their type and coverage rather than claiming equivalence to the whole panel.

HTML uses the existing live panel. Standalone static HTML export is a separate capability: an actually supported exporter must generate it from the corresponding snapshot data and verify its scope; current view.build does not provide complete panel HTML export. When JSON/HTML comparison is needed, use the same batch of data, source versions, and interpretation rules.

New JSON summaries may by default be saved as `views/<view>.json`; frozen results for comparison/handoff use `views/snapshots/<date-time>-<scope>-<view>.json`. Tools protect existing files within that directory; choose a different path for a new round. Actual existing views retain their original paths and generation methods; old Markdown summaries may still be read and are not migrated for the new output rules. Do not create empty directories or invalid links when no file has been produced.

Outputs identify the actual project/scope, model type, generation time, source revisions, diagnostics, and unconfirmed items. “Latest” means the most recent successfully read source versions; show limitations/lag when reads fail, sources are missing, or versions are inconsistent, rather than marking them current.

<a id="刷新与留存"></a>
## Refresh and Retention

The panel checks versions following [source updates](panel-workflow.md#reading-and-source-updates), reusing unchanged data and coalescing refreshes on changes. Rebuild persisted current summaries when related sources change and the summaries remain in actual use; frozen snapshots retain their versions at the time, with new rounds saved separately when a new comparison is needed. AI writes source facts and generators write derived files, without another manual synchronization task.

Closure refreshes only current views that actually exist and are affected. Mark a rebuildable view as lagging if its refresh fails; this does not overturn an already satisfied original delivery. If the view itself is a commitment for this work, assess it against that commitment. Snapshots, screenshots, and summary labels do not replace original requirements, Evidence/Decision, or actual consumer results.

<a id="独立-handoff"></a>
## Standalone handoff

For ordinary continuation, promptly update results, limitations, and next steps in the original Task/Epic. When the user explicitly needs standalone handoff material, or an effective project convention requires it, generate a Markdown snapshot from updated original records using the [handoff template](../templates/handoff.md.tpl). Markdown handoffs in this section serve a different purpose from view exports.

The default location is `handoffs/<date>-<safe-title-or-scope>-<time>[-sequence].md` under the workflow directory; tool-generated names use UTC, and the body states the actual snapshot time and timezone. Prefer an existing explicit location or user-specified location. Another generation on the same day for the same scope saves a separate time/sequence version rather than overwriting the old snapshot; operation replay with the same request_id still returns to the original file.

The tool stamps the actual UTC time in metadata.snapshot_time and returns that value. It preserves the caller's body without appending a fixed-language time label. Use a localized label or reference to that stamped value in the body rather than inventing another time; schema keys and ISO timestamps remain unchanged. Existing snapshots and frozen recovery bytes retain their original content.

Content includes the actual project/worktree and baseline, original work and sources, achieved/unachieved outcomes, evidence coverage and necessary acceptance, next actions, and effective limitations. A record.create handoff provides real source_refs and snapshot_scope; the tool checks those sources and binds their read versions. When related sources have unsettled writes, first recover/check the original operation rather than using old bytes as a new complete snapshot. Read back after saving to confirm paths and references; index only links snapshots that actually exist and truly need navigation.

handoff receives no new management ID and is neither a new Task nor a current-state ledger. Subsequent updates go to original records; recovery first checks original sources and the actual environment. A snapshot retains its identity at generation time. A directory name does not automatically turn historical handover JSON or other attachments into current handoff records.
