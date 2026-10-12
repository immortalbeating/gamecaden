# Gamecaden Panel and Local Host

The workflow is named **Gamecaden**, and the current interface follows the user-selected “Ink-night Screening Room” direction. It is a shared panel, not a ninth responsibility Skill; plugin entry points are the eight responsibilities such as `gamecaden:flow`. See [installation instructions](../INSTALL.md) for installation and version recovery. See the [project README](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/README.md) for maintenance background.

This release translates workflow text; panel controls currently remain Chinese. English descriptions below explain their functions without claiming an English panel UI.

## Startup

First check and prepare the independent environment under [tool readiness and invocation](../shared/local-io.md#1-environment-and-invocation); the launcher requires Python 3.12+. Prepare the host's project list first, using the format in [host-config.example.json](host-config.example.json).

```powershell
& $python -B "$bundle/scripts/gamecaden_runtime.py" run panel --config $hostConfig --state-dir $hostState --port 8875
```

- $hostState is the launcher's dedicated local operations directory, outside game business documents.
- New connections are saved in $hostState/private/connection.json. Open its complete URL in a browser; the one-time secret is immediately removed from the address bar. Connected browsers can refresh directly.
- Read-only by default. Enable Task-body writes, decision recording, and designation of existing asset uses separately; the launcher binds actor, and the page cannot enter identities.
- Current experimental configuration enables writes only for isolated projects. Registered sources in legacy-format projects retain their original formats as read-only.
- The service listens only on 127.0.0.1; stop it by closing the launcher process. Restarting with the same state-dir preserves snapshot-signing capability; obtain a new connection.
- Default port is 8875; select an explicit new port if startup fails. Browser drafts are not shared across ports; prefer the original port for recovery.

A trusted host sets root, workspace, external_sources, and write capabilities in startup configuration. These are not page APIs, and URLs cannot arbitrarily change project roots. Example configuration has no write permissions by default; never treat its example root as a real directory.

## What the Pages Provide

| Page | Content and operations |
|---|---|
| Project overview | Outcome/milestone/Epic/Task tree, current Tasks and candidates, material matrix and condition table; relationship area switches between progression conditions/specification sources, showing declared prerequisite combinations, responsibilities, states and proof, with flow selection, scope, collapse, zoom and source backlinks; copy continuation summaries with source versions |
| Materials and original text | Separate source lists, filters, original text/metadata and revision; read legacy formats through registered lists and conditionally save native Task bodies when authorized |
| Asset management | Asset-family galleries, large candidate images, side-by-side comparison, manifest and file checks, uses, image/audio/video previews; designate candidates for existing uses |
| Batch review and recovery | Large current candidate images and aspect/use/comment forms, bottom member queues and submission trays; individual decision writes and receipts, retained failed drafts, new-version checks, and original-request recovery |

Task/Epic states come from original records. Arbitrary Markdown bodies are not inferred as completion percentages. Partial source scans carry diagnostics; page record counts indicate only current registered scope.

The relationship area uses optional flows / relationships definitions in original sources; see [relationship views](../shared/relation-views.md) for semantics. Specification sources default to “Project domains”: start with a collapsed domain overview, expand domains and included documents, then read actual sources. “Sources and impact” reuses the same original nodes and relationships; both source perspectives support horizontal/vertical layout. Entering a domain defaults to the document tree reader (the user's domain-internal worktree): the left is the actual document inclusion tree, and the right shows actual sections of the selected document. Switch to a focus relationship graph to inspect direct relationships of selected sources. Item-by-item navigation to original text, governance ids, and original relationships remains available. Clicking domains focuses them while retaining directly connected one-hop external endpoints; back navigation restores perspective, expansion, zoom, and canvas position for the same project/page session. The sidebar displays responsibilities, section contents, original governance entries and individual original relationships; original-text buttons locate body headings or governance ids, with check notices for duplicate names or missing current-version targets.

Without navigation, read sources, unclassified materials, and isolated documents remain available rather than requiring complete annotations; missing declared flows show explicit gaps. Original-text entry points use only registered sources; narrow screens switch to domain/document/step lists with full details retained. Registered scope does not mean whole-project completeness. See [design](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/panel.md) and [verification](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md) for the reader and refresh scope; [domain overview design](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/panel.md), [domain verification](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md), and earlier [relationship design](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/panel.md) and [validation](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md) retain their historical scopes.

Overview `GET /api/projects/<id>/governance?focus=T-003` is a read-only derived view; the command line can read the same model through `python -B <bundle>/scripts/gamecaden_runtime.py run governance --project-root ... [--workspace ...] --focus T-003`. Material `located` only means sources were located; condition states and proof do not replace semantic verification or authorization. Explicitly display gaps when governance definitions in legacy sources are unrecognized rather than inferring everything passed. See the [governance contract](../shared/governance.md), [material responsibilities](../shared/material-requirements.md), and [panel continuation](../shared/panel-workflow.md).

Connected pages can use `#project=<id>&view=overview|assets|review|documents&task=T-003&asset=A-002&candidate=C-001` to locate current objects; include only needed parameters. Relationship views may add `diagram=sources|progress`, `lens=domains|impact`, and `layout=DOWN|RIGHT` to choose specification sources/progression conditions, project domains/sources and impact, and vertical/horizontal layout respectively; for example, `#project=<id>&view=overview&diagram=sources&lens=domains&layout=RIGHT`. Selections, sections, expansion, zoom, reading, and canvas positions are isolated by project binding in the current session; panel refresh and project switching retain still-valid objects, while source deletion or identity changes require repositioning. Recovery of these reading settings after a full browser-page reload is not promised. `connect=` remains a one-time connection secret and is excluded from work deep links. Copied continuation summaries include source/version leads; Agents must reread original records and actual conditions before continuing. The panel does not run engines or automatically wake Agents.

Asset technical checks, decisions, use designations, and actual runtime adoption retain separate ownership. Switching candidates does not automatically retain old-use decision/evidence references. Previews are static references or media playback and cannot replace in-engine effects or gameplay acceptance. There is currently no frame editor, map generator, or model editor.

The overview first provides current-work entry points; the materials page opens section readers for the same sources. Candidate comparison can select any registered alternative; preview read failures offer local retry. Full reviewed candidate versions and ledger Revision appear under “Version grounds”; queue thumbnails reuse read caches only when both match the draft. Selecting members still rereads current candidates, and source changes do not automatically upgrade draft baselines. Deferral retains local drafts only without preparing writeback; narrow-screen “Enter comments” directly locates the form. See [Gemini assessment and repairs](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md) for that round's scope and validation.

## Source Updates and Reading Recovery

`GET /api/projects/<id>/revisions` checks only content versions of registered physical sources and mappings, returning stable digest, source_revisions, mapping_revision, complete and diagnostics; it does not parse individual records or derive governance. Compare only when `complete === true` and digest is nonempty. Unregistered files and runtime roots are excluded; digest proves neither approval, record-semantic validity, nor engineering execution. Missing sources, read failures, or changes during checks retain diagnostics rather than being treated as no updates.

Check versions when the window regains focus or the page becomes visible; unchanged versions do not read full data, while changes and affected records from successful writes receive coalesced refreshes retaining reading positions. Check versions before and after full reads rather than marking data changed during reads as latest. Defer automatic refresh while editing inputs, in open dialogs, or busy, resuming when available; do not automatically change draft base_revision or frozen requests. Current behavior is foreground-event triggered, without periodic polling, file watchers, or a second fact source.

## Writes and Recovery

Bodies, decisions, and use designations all obtain signed snapshots before submitting stable request_id values. The host calls the same Workflow library rather than creating a separate panel business database. Confirm success only after the original library settles with outcome=ok and supporting per-file results.

Drafts and pending frozen requests are stored in the current browser's localStorage by project binding_id. They recover inputs and are not authoritative Task/Decision records. After reloads or network failures, first query original request_id, then recover with original payloads; finding no receipt does not mean execution never occurred. Settled receipts prove only results at that time; read source files separately for current facts.

Retain inputs on confirmed conflicts. Tasks and review members both provide “Check current source/candidate”; allow preparation of new operations only after explicit old/new baseline comparison. Already frozen pending requests remain unchanged.

Currently Task-body editing does not automatically change state or close Epics. Responsibility Skills still handle independent design/verification, engine execution, and Git delivery.

## Identity and Deployment Scope

Here user/agent/tool are recorders bound by a trusted local launcher, not Codex/ChatGPT account login, and do not detect whether operators are human. Automated tests use tool. For actual user operations, the launcher must have real user-action provenance; Agents may not use user sessions to fabricate acceptance.

New state-dir/private directories restrict access on Windows to the current account, SYSTEM, and administrators; POSIX uses 0700. Connection files replace private temporary files, and secrets are not logged. state-dir must still belong to the trusted launcher; do not reuse others' preconfigured signing keys or shared state directories. This host is a local tool without remote multiuser accounts.

Details: [bridge contract](../shared/panel-bridge-v1.md) · [local I/O and recovery](../shared/local-io.md) · [step fourteen bridge validation](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md) · [step fifteen coordination](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/panel.md) · [governance validation](https://github.com/immortalbeating/gamecaden/blob/v0.1.0/docs/validation.md). Historical step-fourteen results cover only bridge reads/writes at that time, not browser acceptance of the complete governance interface.
