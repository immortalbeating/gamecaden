<a id="面板定位读回与续接"></a>
# Panel Navigation, Readback, and Continuation

Use derived views for cross-record discovery, dependency overviews or batch review. Read known original sources directly when they suffice. This page explains the selected view path for flow/init/design/develop/assets/verify/close; [material responsibilities](material-requirements.md) and [governance](governance.md) own rule semantics. Launch the panel only when using it, under [panels/README.md](../panels/README.md); CLI views remain available. Views add no Skill or progress store.

<a id="取得本次范围的视图"></a>
## Obtain a View for the Current Scope

After confirming the actual project and registered sources, read the derived read-only graph, materials, and conditions from `GET /api/projects/<id>/governance?focus=T-003` in the panel; read according to the current Task/candidate and its relationships. `focus` locates an object without removing other sources from the graph. Without a panel, or when a command line is needed, use `scripts/workflow_governance.py --project-root ... [--workspace ...] --focus T-003` for the same derived model. The output reports applicable condition states; it does not automatically authorize execution, acceptance, closure, or changes to original records.

The panel does not require saving views files first. See [derived outputs](derived-outputs.md) for on-demand JSON snapshots, existing HTML display, model coverage, and historical retention. Free-form Roadmap/PDP bodies remain original text; only explicitly declared structural relationships enter outcome/progression graphs, without inferring achievement from S/M identifiers.

The panel supports positioning through `#project=<id>&view=overview|assets|review|documents&task=T-003&asset=A-002&candidate=C-001`; include only parameters currently needed. `connect=` remains exclusively for one-time connection authentication, not a copyable work deep link. Project IDs, Tasks, assets, and candidates must come from registered real objects; fragments cannot specify a new project root or extend permissions.

| Current responsibility | View use |
|---|---|
| flow / init | Find the original Task, authoritative sources, and related material gaps; map only the current scope in legacy projects and continue from original sources |
| design | Filter material responsibilities and conditions for the current action, follow links back to design/specification sections, and form the necessary plan |
| develop / assets | Locate candidates awaiting integration, uses, consumers, and current conditions; execute after reading back the original Task, ledger, Decision/manifest |
| verify / close | Follow conditions to original requirements and actual Evidence/Decision, then assess coverage, acceptance, and closure; view conclusions do not replace verification |

<a id="阅读与来源更新"></a>
## Reading and Source Updates

Within each domain, the document tree reader is the default: select documents on the left according to their actual inclusion relationships and read actual section bodies on the right. Switch to a focus relationship graph as needed and continue reading back by original headings, governance ids, and individual relationships. The tree organizes reading; it is not another task list or gate. See [reader and refresh design](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/panel.md) and [verification for that round](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md) for explanation and scope.

When the panel returns to the foreground (window focus / page visible), it calls `GET /api/projects/<id>/revisions` to check versions of registered physical sources. Compare only when complete is true and digest is nonempty; unchanged versions do not load full views, changes receive a coalesced refresh, and successful writes update affected records. If versions differ before and after a full read, sources are missing, or checks fail, retain the notice and do not claim the view is current. Defer automatic refresh while editing, in dialogs, or busy; keep original draft baselines and frozen requests unchanged. Isolate current-session reading selections, sections, expansion, and positions by project binding. There is no need to manually maintain panel facts after every progression step; save real changes according to original record responsibilities. Lightweight checks do not scan engine runtime roots or prove that the actual project, material bytes, or Git are synchronized; those still require explicit reads and corresponding evidence verification.

<a id="读回后继续"></a>
## Continue After Readback

Use [relationship views](relation-views.md) when multi-level prerequisites or specification responsibilities are needed. The progression graph reads declared flows and condition combinations; the source graph retains original relationship directions. Neither automatically executes, accepts, or closes anything. Without flow definitions, retain the unverified status and use existing conditions and source text.

After opening a panel record or CLI result, read back the referenced original Task, material sections, asset ledger, Decision, Evidence, and actual project state; check source versions and the current worktree. Derived results may be stale or cover only registered sources; retain diagnostics and unknowns. The panel does not run engines or automatically wake Agents.

When legacy-format sources are registered only as read-only and have no interpretable structured definitions, the panel may display source materials and indicate that governance is unrecognized. This does not imply that there are no materials or conditions, nor that gates have passed. Material `located` only means the source can be located; condition `satisfied` still requires checking its object, version, evidence coverage, and current authorization.

A copyable continuation summary should include project and original-record locations, sources/versions, current scope, observed conditions and gaps, next action, and a deep link. It is a handoff lead; the receiving Agent still rereads original records and the actual environment before continuing existing authorization, and does not write the summary or page state as a second authoritative progress record. If a view conflicts with source text, investigate from original sources and fix the mapping or derivation issue; do not infer a pass without an explicit result.

Identify explicit project constraints or user conditions and apply them to corresponding actions; ordinary quick work handles only matching conditions. Authorized work may continue after readback; panel state itself adds no approvals or stages.
