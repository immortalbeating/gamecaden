# Architecture

Gamecaden separates task behavior, project facts, and host presentation. Eight responsibilities read authoritative project sources and select work for the request. Formal adoption organizes definite current Vision, necessary Spec overview, and Roadmap entries; detailed inputs and original work retain clear maintenance scope. Workspace mappings locate sources without duplicating changing state. See [record responsibilities](../plugins/gamecaden/shared/records.md#current-project-level-bodies) and [workspace adoption](../plugins/gamecaden/shared/workspace.md).

## Repository and distribution

| Location | Responsibility |
|---|---|
| `.agents/plugins/marketplace.json` | Installation entry pointing to public `plugins/gamecaden` |
| `plugins/gamecaden/` | Plugin manifests, Skills, contracts, schemas, templates, scripts, and panel |
| `tests/` | Maintenance tests and anonymous fixtures |
| `scripts/check.py` | Contract, Python, JavaScript, and build checks |
| `dist/` | Build artifacts, excluded from commits |

Installed package copies and project records are different objects. Upgrades do not automatically rewrite project designs, adopted rules, acceptance, or saves. Verify installed paths/version in a new session; discovery in an old session does not establish the installed version.

The standard-library `scripts/gamecaden_runtime.py` launcher checks/prepares an isolated cached environment, then forwards I/O, governance, panel, and contract tools. Resource installation and tool readiness are checked separately under [local I/O](../plugins/gamecaden/shared/local-io.md#1-environment-and-invocation).

## English development, user-language materials

English is the canonical maintenance language of interfaces, schemas, workflow rules, references, and templates. English and Chinese usage guides describe one package. Complete Chinese rule comparisons stay in ignored local review material rather than a second public rule set.

Material language follows the [workspace convention](../plugins/gamecaden/shared/workspace.md#6-language-preferences). Replies and new project materials default to the user's language; explicit communication/document preferences may differ. Adapt template headings, labels, table headers, prompts, and prose, preserving schema keys, IDs, enums, paths, and commands. Existing material language and identity are preserved during maintenance unless conversion is requested.

Native I/O retains caller-supplied UTF-8 bodies/titles and handles Unicode filenames. A document's headings are not native identity syntax. Governance displays an actual source section in any language, without inferring status or acceptance from its heading. Extraction adds language-neutral path-provenance data; legacy partial extraction recovery retains matching old target bytes. Technical diagnostics are English, while original user content remains unchanged. The current panel controls remain Chinese; panel localization is separate from document-language behavior.

## Sources and I/O

Mappings point to original records whose formats retain their maintenance ownership. Explain diagnostics together with scope completeness; located material does not imply semantic validity or satisfied conditions. Local I/O checks snapshots/revisions and saves stable operation identities/receipts. Query the original request before recovering unsettled operations. See [local I/O](../plugins/gamecaden/shared/local-io.md) and the [format contract](../plugins/gamecaden/shared/formats-v1.md).

Large settled operation receipts may use an internal lossless compressed envelope at the same JSON path; the storage reader restores the original value before scope, replay, allocation or recovery handling. Pending receipts and source files retain their original representation. Legacy plain receipts remain readable; old package readers do not understand the new envelope, so a project operation store needs a consistent supported reader.

Pending-operation queries retain a bounded process-local cache of verified settled-receipt metadata, bound to hashes of bytes read on each query. Cold starts and changed bytes require full validation; the cache stores no payloads or project facts, and does not rewrite history. Explicit receipt reads and replay retain full decoding.

New Tasks default to `tasks/T-<number>-<short-name>/task.md`, with dedicated materials in that directory or subdirectories as needed. Legacy flat Tasks and original attachment directories remain compatible. Ordinary attachments belong to their Task/Epic and have no separate work identity/lifecycle; shared specifications, assets, and evidence remain referenced from their original sources.

[Records](../plugins/gamecaden/shared/records.md#retention-indexing-and-versions) unify evidence retention, default paths, indexing, and organization triggers. Existing reports may fulfill Evidence responsibilities; reruns retain sufficient history. Path reading distinguishes native text from read-only binary data, and physical long-path handling retains logical Refs and boundaries. Records, diagnostics, and revisions share list pagination. The panel reuses one in-process model across pages and governance, rechecking actual bytes, registered membership and operational diagnostics; source changes invalidate its cursors. Large non-Markdown attachment payloads are not retained in that model; original-file reads remain complete. Source registration is narrowed to relevant bodies/indexes and bounded collections.

Main-document organization is a Skill's semantic judgment and write-back convention. role/scope do not automatically filter sections or prove adequate bodies. Old schemas/mappings remain readable, and responsibilities are organized within actual adoption/repair scope. Package updates do not migrate projects automatically.

Ongoing project adoption defaults to a Roadmap maintaining product outcomes/M milestones and condition references. An adopted large scheme needing phased implementation uses a project/version-level [PDP](../plugins/gamecaden/shared/phased-development.md), saved independently in plans/ and arranging Epics and local S Stages. Task ownership/lifecycle remain unchanged. PDP adds no management ID/lifecycle; design/plan/history attachments remain owned by real Tasks/Epics. Creation, registration, and content adequacy are verified separately; counts do not establish implementation.

## Panel

The local panel derives registered sources through the same library. Browser drafts recover input; original Task, Decision, and ledger records remain authoritative. Foreground events trigger source-version checks. Continuation summaries are location clues; reread original records and the actual environment before proceeding. The panel neither runs engines nor wakes agents. See [panel startup](../plugins/gamecaden/panels/README.md) and the [bridge contract](../plugins/gamecaden/shared/panel-bridge-v1.md).

[Derived outputs](../plugins/gamecaden/shared/derived-outputs.md) distinguish live HTML, rebuildable JSON summaries, and frozen snapshots. Saved views are not startup prerequisites; current view.build does not export complete static HTML. Independent handoffs derive from actual sources, retain new time/sequence rounds, and check source revisions; they are distinct from operation receipts and work lifecycles.

Engineering profiles are conditionally loaded references. Technical checks, model adherence, engine behavior, user acceptance, and release authorization each need corresponding evidence under the [validation tiers](validation.md).
