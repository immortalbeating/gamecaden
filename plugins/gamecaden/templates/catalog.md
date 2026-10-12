<a id="模板使用目录"></a>
# Template catalog

These files are writing guides organized by information responsibility, not a skeleton to copy in full during initialization. Read the corresponding object in the [format contract](../shared/formats-v1.md), then fill it for the actual goal and remove empty optional sections. The main documents created during formal adoption have definite entries under [current project documents](../shared/records.md#current-project-level-bodies), reusing original content and specific references; other objects follow their actual maintenance sources.

`{{...}}` marks content to fill in and must not remain unchanged in an actual delivery. Use the appropriate serializer when generating YAML/JSON fields, handling quotes, newlines, and types; do not concatenate arbitrary user text directly into YAML. Default nulls/empty lists in templates are not judgments about the project's state.

Before filling a template, apply the project's [document-language convention](../shared/workspace.md#6-language-preferences) to its headings, labels, table headers, prompts, and prose. The English blueprint is not the output-language choice.

| Template | When to use |
|---|---|
| [Workspace](workspace.yaml.tpl) | Create a project mapping; fill only known sources and leave unknowns unknown |
| [Workflow entry](index.md.tpl) | Create a project reading entry that references materials that actually exist |
| [Vision](vision.md.tpl) | Organize the current vision during formal adoption; reuse content from an existing focused vision and state unresolved direction honestly |
| [Spec overview](spec-index.md.tpl) | Maintain rules/baselines through a definite overview and domain entries |
| [Domain Spec](spec-page.md.tpl) | Save the effective contract and actual capabilities at its baseline |
| [Roadmap](roadmap.md.tpl) | Create by default when formally adopting project-wide ongoing development; retain real current outcomes and unresolved scope without inventing commitments to fill stages |
| [Phased Development Plan](development-plan.md.tpl) | Arrange delivery across one or more Epics when an adopted large scheme needs phased implementation; save separately from work records under the [PDP contract](../shared/phased-development.md) |
| [Parking lot](parking-lot.md.tpl) | Retain worthwhile future ideas that have not been committed |
| [General Task](task.md.tpl) | Select quick/standard from actual needs first; retain useful body sections, and keep standard concise when appropriate |
| [Lightweight Task](quick-task.md.tpl) | Use after selecting quick; record the goal and required checks at the start, then save results as work actually progresses |
| [Epic](epic.md.tpl) | Related deliveries need a shared goal and overall exit conditions |
| [Design](design.md.tpl) | Design content needs independent reading/maintenance |
| [Plan](plan.md.tpl) | The original Task's sole internal checklist or arrangements within an existing Epic; an overarching PDP uses its separate template |
| [Detailed history](history.md.tpl) | Original work history obstructs reading and needs a separate sole body |
| [Handoff snapshot](handoff.md.tpl) | The user or effective project convention needs an independent handoff; derive it from original records, with paths/version retention under [derived outputs](../shared/derived-outputs.md#standalone-handoff) |
| [Evidence](evidence.md.tpl) | Use an independent native explanation or embed the same form in the original Task; do not copy an existing complete report |
| [Decision](decision.md.tpl) | Version acceptance, batch decisions, or independently tracked events; ordinary choices may remain in the body |
| [Asset Ledger](asset-ledger.yaml.tpl) | A native asset ledger registers actual identities and selected uses |
| [Fallback manifest](manifest.json.tpl) | Bind an actual file set when production has no equivalent existing format |
| [Note](note.md.tpl) | A reusable lesson and its applicability actually exist |
| [Git policy](git-policy.md.tpl) | A policy has actually been adopted and needs separate storage; the template grants no default authorization |
| [Project rules](project-rules.md.tpl) | Applicable rules have been selected and the existing Spec/rules have no suitable section; record adoption scope, source version, and project differences without copying an entire profile |

Filled [examples/v1](../examples/v1/index.md) cover embedded/independent records, partial adoption, and request/result forms. Their projects, times, and pass/acceptance states are demonstration data, not facts about a real game or user judgment.

The read-only contract check is [check_contracts.py](../scripts/check_contracts.py). It validates schemas, template fields, and positive/negative examples; it does not provide this protocol's write service.

The check requires Python, PyYAML, and jsonschema; the original validation used dependencies already present in the environment rather than installing them as a project or plugin runtime.

<a id="可选的材料与条件标注"></a>
## Optional material and condition annotations

When the panel needs shared outcomes, material responsibilities, applicable rules, and progression conditions, use annotations on the same source and their Schema under the [governance contract](../shared/governance.md). Definitions remain in the original Spec, Roadmap, PDP, Epic, or Task; this adds no mandatory Gate/overall-progress document. Reading views, optional JSON storage, and HTML capabilities are described in [derived outputs](../shared/derived-outputs.md). Registering an old format does not constitute its adoption or migration.
