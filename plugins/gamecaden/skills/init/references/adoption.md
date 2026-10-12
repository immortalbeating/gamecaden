<a id="旧项目接入修复与移交"></a>
# Adoption, repair and handover of old projects

Establish current scope and actual sources first. An old workflow in a directory does not mean migration is required; two systems in one directory do not require immediately stopping all work. What matters is whether this object has overlapping write responsibilities.

<a id="当前情况导航"></a>
## Navigation by current situation

Choose the entrypoint from the current request; read only matching parts.

| Current situation | Next action and grounds |
|---|---|
| Continue existing work or local repair | Restore from original work, checking current results, advancement constraints and relevant sources under [Continuation reference](../../flow/references/resume.md). |
| Target roots or authoritative sources remain unclear | First identify actual circumstances read-only through [init inspect](../SKILL.md). |
| Establishing Gamecaden adoption has been requested | Use [adopt](#adopt-organize-current-primary-documents-and-retain-original-sources) below to form current entrypoints, register maintenance responsibility and reuse valid content. |
| Registered entrypoints or mappings are invalid | Investigate and repair specific gaps under [repair](#repair-repair-according-to-actual-gaps) below. |
| Switching maintenance responsibility of records is authorized | Transfer specified objects under [migrate](#migrate-transfer-only-authorized-scope), retaining original identity and history. |
| Current design or production materials are insufficient | Locate affected actions under [Material responsibilities](../../../shared/material-requirements.md), completing relevant inputs in original work. |

<a id="识别已有来源"></a>
## Identify existing sources

Find relevant goals, specifications, routes, active work, ledgers, evidence and decisions from current guidance and actual entrypoints. Judge content from file bodies and actual consumers, not names, checked checkboxes or dates alone.

Concept art, character designs/models, level diagrams, gameplay and background materials can also fulfill material responsibilities. Check information required here under [Use reference](../../design/references/game-deliverables.md), retaining original sections, configuration and production sources. Reuse remains possible under different names or multiple purposes in one material; when future targets differ from current state, supplement only relevant differences. Handle independent candidates needing sustained tracking under original asset contracts, without forcing all design materials into asset registration.

Distinguish identically named Issues/Tasks through “source system + original identifier + original path”. Read old YAML in code blocks, nested Epic directories or other formats compatibly; do not force conversion before understanding content.

Before migration, original Task/Issue goals, lifecycle, continuation and approvals remain in original sources. A new entrypoint may link them, but cannot create another copy with identical goals and status.

<a id="adopt整理当前正文并保留原来源"></a>
## adopt: organize current primary documents and retain original sources

- Under [Material responsibilities](../../../shared/material-requirements.md), mark each item within scope reusable, missing, conflicting, unknown or inapplicable; understand mixed files through original responsibility, sections/fields, versions and applicable scope. Gaps may appear through [Governance derived views](../../../shared/governance.md).
- Organize Vision and necessary Spec overview from adopted requirements under [Current project primary documents](../../../shared/records.md#current-project-level-bodies); default to a Roadmap for project-level sustained development, retaining real outcomes and unresolved scope. Register Stage arrangements of large solutions independently or cite precisely under [PDP](../../../shared/phased-development.md). Original materials continue supplying detailed design/historical grounds; express current direction and target/actual capabilities separately.
- Register active work collections and maintenance responsibility by source system; create new Tasks only after their default source is clear.
- Original inputs retain locations and version references; detailed domain conventions, diagrams, data and ledgers may remain maintained by original sources, with overview explaining specific effective scope and consumers. Historical advice or candidates become effective requirements only after explicit adoption in the corresponding scope.
- Adoption guidance explains which objects remain managed by old processes. Without user authorization to switch old objects, retain original responsibility.

Adoption results must locate current vision, rules/baseline, necessary route and each subsequent writeback location, explaining what original materials still maintain. Adopted but unimplemented goals retain commitments; unadopted candidates do not become requirements through organization. Merely listing materials or moving all content into one Spec does not complete responsibility organization.

New entrypoints may coexist when old and new scopes are clearly separate. If two instruction sets or automatic entrypoints rewrite the same work, handle that specific overlap before switching the object; other independent work can continue.

Map only sources related to this delivery and confirmed project scope; choose primary documents/indexes and narrow collections under [Collection scope](../../../shared/workspace.md#2-portable-fields), and register report entrypoints under [Retention and indexing](../../../shared/records.md#retention-indexing-and-versions). scope does not filter out receipts or historical payloads. For panel-assisted location, read derived results under [Panel continuation](../../../shared/panel-workflow.md), then original text; views do not automatically adopt anything.

<a id="repair依据实际缺口修复"></a>
## repair: repair according to actual gaps

Distinguish empty collections at first use, moved files, genuinely lost records and old configuration. Locate using current references, content and available project history; do not treat disappearance of an originally active task directory as “there have never been tasks”.

Modify confirmed invalid mappings or links, preserving unrelated conventions. When permissions, tools or files are missing, identify affected actions; do not reset the entire project to repair one entrypoint.

When repairing primary document responsibilities has been requested, organize affected documents under adopt and align original sources; ordinary continuation does not automatically become full-project repair because a new entrypoint is absent. Package updates do not independently migrate projects or change original fact owners.

<a id="migrate只移交获授权范围"></a>
## migrate: transfer only authorized scope

Before handover, list current objects, original locations/IDs, original responsibility, new responsibility and entrypoints needing adjustment. Retain traceable execution records for actual conversion; simple ownership adjustment without content conversion can save the decision nearby.

During handover:

1. Preserve original content, status semantics, historical results and approval scope; explain old/new identity mappings.
2. Modify write sources and necessary guidance in this scope, handling genuinely overlapping automatic restoration/recording/archiving entrypoints.
3. Retain locatable historical identity or a reference to an effective entrypoint at the old location; move files only when genuinely needed and authorized.
4. Read back migrated objects and references, confirming each has one active status source. Unfinished work cannot become complete through migration.

Source code, resources, code branches, remotes and release state do not automatically change through record migration. Engineering actions allowed by original instructions still follow that actual delivery.

<a id="宿主项目指引与重复执行"></a>
## Host project guidance and repeated execution

First check project guidance, override and existing managed sections for the current host within target scope; Codex uses AGENTS.md and Claude Code uses CLAUDE.md. Effective locations may be root or nearer override files; merely adding an ignored root guide cannot establish completed adoption.

Update only this workflow's bounded sections; explicitly adjust conflicting rules within user-authorized scope, preserving other conventions. With incomplete boundary markers or conflicting candidate sections, investigate content first instead of guessing through broad replacement.

On a second execution, read existing registration and supplement relevant differences only. Retain established authorization and choices; identical paths or file existence do not prove content correctness. Still read back in proportion to current changes.
