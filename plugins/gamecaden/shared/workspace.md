<a id="工作区与来源约定"></a>
# Workspace and Source Conventions

Used by flow for location and init for registration, and by other Skills in this workflow to read sources. The [format contract](formats-v1.md) and [validatable schema](../schemas/workflow-v1.schema.json) define native mapping v1 fields; this page maintains adoption responsibilities and usage. Source registration, package installation, and later host loading are verified separately, with actual coverage determined by corresponding validation records. Project communication and document languages follow [language preferences](#6-language-preferences).

<a id="工作流适用条件"></a>
## Workflow Applicability

Before using Gamecaden responsibilities, confirm the grounds for this work; either condition is sufficient:

- The user explicitly requests Gamecaden or one of its named responsibilities for this work, or explicitly requests project adoption of Gamecaden. The same unfinished authorized work and subsequent responsibilities selected by flow under that authorization retain these grounds without the user naming each one.
- Effective guidance in the current project explicitly adopts Gamecaden. Restore original entry points and records within the guidance's actual scope, then select responsibilities for the current request.

Ordinary projects without adoption complete requests under effective guidance, original records, and professional tools. Skill visibility, directory metadata descriptions, name mentions alone, game-development tasks, historical discussion, or a same-named directory do not constitute grounds for use or adoption; historical archives, other projects, and reference-only materials do not replace current guidance. Without the grounds above, do not automatically select this workflow or replace the user's original task with an adoption requirement.

When only reading, explaining, or reviewing the Skills themselves, treat their bodies as material for analysis without executing project responsibilities. A single explicit invocation reuses existing materials within current scope; complete adoption/migration still follows init's separate authorization and source conventions. Applicability does not expand write, implementation, or release permissions; read-only boundaries and authorization for ongoing work remain effective.

<a id="1-位置与解析"></a>
## 1. Locations and Resolution

Prioritize workflow entry points specified by the user or explicitly referenced by effective project guidance. New projects default to game-workflow/, with workspace.yaml recording mappings and index.md providing reading navigation. Adopted projects retain their mapping paths.

All path, root, and marker values in workspace.yaml resolve relative to the YAML directory. Before writing, resolve actual paths against explicit current goals and check project, worktree, and affected scope. Relative paths let the same project work across checkouts; actual runtime results still record this round's specific baseline.

Matching project, directory, or branch names do not prove write targets. Mappings pointing to materials outside scope may provide related references but do not extend authorization to modify other directories.

When the user explicitly calls flow for a concrete delivery, the actual target is uniquely determined, and no existing work sources are found after verification, necessary Task records may be saved in that project's game-workflow/tasks/. This retains current delivery and does not mean whole-project adoption or migration of old workflows. Without actual need, do not first generate workspace/index/AGENTS. On later occasions without mappings but with this default collection, check Task format, goals, and actual project conditions before reading it; resolve specific conflicts if entry points are occupied by other uses or conflict with one another.

<a id="2-便携字段"></a>
## 2. Portable Fields

| Field | Meaning |
|---|---|
| schema_version | Format version of this specification, currently 1 |
| project.id | Stable project identity; reuse an existing explicit identifier or assign on first registration, without changes for branch/display-name changes |
| project.name | Human-readable name |
| project.root | Relative location of the project's actual root |
| runtime_roots | Confirmed runtime roots; may be empty when no runtime entry exists |
| runtime_roots[].id/path/engine/marker | Runtime-purpose identifier, directory, identified engine, and actual marker file; engine does not mean runtime has been verified |
| sources | Original documents or record collections; each has id, role, kind, path, owner, and scope/format/adapter when needed |
| default_task_source | Sole default source id for new Tasks; may be empty when undecided, while existing tasks still operate through original sources |
| default_epic_source | Default source for new Epics; may be empty when unnecessary or undecided |
| rule_sources | Actually effective project standard/profile sources and applicability; register only locatable materials, then judge usage under [rule selection and loading](rules.md) |

sources role uses vision, spec, roadmap, development-plan, task, epic, asset-ledger, evidence, decision, notes, parking-lot. kind is file or collection. role indicates information category and does not automatically prove sufficient body responsibilities or effective requirements. scope describes applicability and is not a tool section filter. owner indicates maintenance conventions, such as flow, codestable, trellis, project; it is not operating-system permission and does not require a tool of the same name.

format/adapter describes actual form and adaptation leads; identify first when omitted. Declaring an adapter does not imply write capability exists. Use the [workspace template](../templates/workspace.yaml.tpl) as needed for creation; registering mappings does not automatically convert legacy sources.

collection recursively enumerates supported record suffixes, and scope does not filter files. During registration, prioritize bodies/index files needing navigation and narrow collections with clear boundaries; related reports precisely reference raw measurements, receipts, frozen payloads, and historical attachments rather than registering whole output trees as Notes to obtain indexing. Use existing entry points or a few file sources for mixed-purpose directories, selecting roles by actual information responsibility. See [record conventions](records.md#retention-indexing-and-versions) for evidence retention and upgrades; do not overlay conflicting collection interpretations on the same path.

The model may choose and save first-registration management IDs and regular storage locations under conventions without asking the user to name each one. New Task/Epic collections default to owner flow, and other new-project documents to project; sources owned by existing systems/generators retain actual maintenance conventions. Assigning management identifiers differs from inferring product facts and cannot justify inventing goals, engine entry points, or approvals.

The same fact in the same affected scope must have only one maintenance source. Multiple task collections may coexist, but actual objects/scopes must be clear. With workspace mappings, new tasks use explicit default_task_source; single flow deliveries without mappings retain records under Section 1. When default sources are undecided and new work is truly needed, first fill in gaps from user requirements, existing management scope, and default locations; clarify only remaining substantive conflicts. Continue existing tasks through original sources rather than reassigning them to new defaults.

File sources point to existing bodies whose responsibilities can be explained. collection may represent an on-demand new-record location; no empty directory is needed before content exists. If existing tasks reference a missing collection, treat it as missing records rather than initializing an empty project.

When adopting bundled engineering profiles, use the [profile adoption convention](../profiles/README.md): save rule selections and project differences in original Spec/rules, while rule_sources registers only actual files inside this project's root; save sourced-version local snapshots only when portable fixed bodies are needed. Package updates do not automatically rewrite effective project rules. See [project-structure](../profiles/project-structure.md) for new/migrated directory responsibilities.

<a id="3-新项目示例"></a>
## 3. New Project Example

This registers a new project with existing Godot markers and specifications; do not copy it as facts about other projects.

```yaml
schema_version: 1
project:
  id: aurora-game
  name: Aurora
  root: ..
runtime_roots:
  - id: game
    path: ..
    engine: godot
    marker: ../project.godot
sources:
  - id: current-vision
    role: vision
    kind: file
    path: vision.md
    owner: project
    format: native-markdown-v1
  - id: current-spec
    role: spec
    kind: file
    path: spec/index.md
    owner: project
  - id: current-roadmap
    role: roadmap
    kind: file
    path: roadmap.md
    owner: project
    format: native-markdown-v1
  - id: tasks
    role: task
    kind: collection
    path: tasks
    owner: flow
  - id: epics
    role: epic
    kind: collection
    path: epics
    owner: flow
default_task_source: tasks
default_epic_source: epics
rule_sources: []
```

New projects without an actual project yet may use runtime_roots: []; record intended engines in goal materials. Legacy projects may map task sources to .trellis/tasks or codestable's actual collections, retaining original-system owners; describe complex nested sources with actual entry points and scope, without assuming all use this specification's Task frontmatter.

workspace does not store current Task states, completion percentages, processes/ports, temporary login information, approval copies, or package command copies. scope describes only responsibilities and applicability; current check results and completion judgments return to original bodies/evidence, not source descriptions. Read actual commands from project configuration and history/continuation from original records.

Project Git policy is referenced as applicable rules through rule_sources/actual entry points; see [Git policy conventions](git-policy.md) for selection and storage. Reuse existing authoritative locations; use rules/git.md for new projects when needed. Obtain current branches, remote differences, and execution progress from Git/original Tasks rather than adding dynamic mirrors.

<a id="4-index-和宿主指引"></a>
## 4. index and Host Guidance

<a id="新建资料的默认位置"></a>
### Default Locations for New Materials

During formal adoption, create vision.md and necessary spec/index.md in the current workflow directory under [project-level current bodies](records.md#current-project-level-bodies); default to creating roadmap.md when adopting sustained project-level development. Follow explicit user locations and register sole entry points. Repeated adoption retains determined locations and fills only current differences; reading and local continuation of legacy mappings remain compatible, with responsibilities organized only during relevant repairs.

vision sources point to current vision bodies, and Spec overview/Roadmap to corresponding current entry points; detailed domain specifications may still register independent sources. Register development-plan sources under [PDP](phased-development.md) for phased implementation of large plans, defaulting to narrow plans/ collections or actual file entry points with owner project; they may be created independently of Epic/Task. Reference mixed inputs by sections/fields, versions, and adopted scope rather than registering whole files as current primary documents because they contain goals, rules, or stage tables. Historical/candidate registration serves only location and does not become another effective body.

Other new materials default to parking-lot.md, notes/, assets/ledger.yaml, and on-demand plans/, evidence/, decisions/, views/, handoffs/, created when actual responsibilities exist. PDP defaults to plans/<safe-title>.md; see [derived outputs](derived-outputs.md) for generation, naming, refresh, and version retention for views and standalone handoffs. Task/Epic, ledgers, checks/decisions retain original identities and maintenance sources. Independent parking-lot.md maintains future candidates and is referenced by Vision. New Tasks default to `tasks/T-<number>-<short-name>/task.md`, with dedicated materials saved in the same directory or subdirectories as needed; Epic locations follow common record rules. Continue reusing old flat Tasks and explicit original paths.

<a id="入口正文与宿主段落"></a>
### Entry-point Bodies and Host Sections

index briefly describes the project and workflow entry points, separately identifying current project-level bodies, maintenance entry points for original work/rules, and purposes/scopes of detailed/input/historical materials. First understand direction and effective scope from current bodies, then read detailed sources for the current question; do not rewrite dynamic progress. Link only existing files; describe purposes of not-yet-created collections without making nonexistent bodies active links.

Merge a short workflow section into actually effective project guidance, adapting paths to actual project locations. Codex defaults to AGENTS.md, Claude Code uses CLAUDE.md, and other hosts use actual guidance entry points. Default illustration (Skill names use the Codex plugin as an example; reread and adapt for the actual host):

```markdown
<!-- game-workflow:begin -->
## Game Workflow (Gamecaden)
- This project adopts Gamecaden. The workflow entry point is game-workflow/index.md, and project root, runtime roots, and source mappings are in game-workflow/workspace.yaml.
- When a new session handles development, continuation, acceptance, or closure requests for this project, first use the actually installed gamecaden:flow to locate relevant entry points and original work records.
- When the user asks to continue, locate the next action from current original Task results, progression restrictions, and the actual workspace; handle read-only status requests as read-only, and clarify multiple work items only when goals/prerequisites cannot determine the choice.
- Read relevant rules, designs, and implementation arrangements according to current goals, changed objects, and actual consumers; directly reuse effective existing grounds.
- Retain each record's maintenance source; write execution results, scope changes, progression restrictions, and next steps back to original work, while aggregate views read original facts.
- Follow explicit current language instructions and effective project preferences; otherwise use the user's language for replies and new material documents. Preserve existing documents' language when maintaining them unless conversion is requested.
<!-- game-workflow:end -->
```

Write corresponding Skill pointers only in environments actually providing these workflow Skills, using genuinely discoverable names. Before installation, provide file-reading entry points and state that Skill discovery is unverified; do not leave fictitious commands claimed to be callable.

Preserve existing rules. Check overrides, nested scopes, and current host sources to avoid ineffective new entry points that are overridden. Report file writes separately from actual loading in later sessions; do not modify global user guidance or host configuration for project adoption.

After installation and project adoption, separately test natural-language “continue,” explicit Skill invocation, and read-only status requests in a new session in the correct project, observing actual loaded sources, selected original work, and write behavior. Without such host validation, claim only prepared guidance and files, not guaranteed automatic invocation or execution every time.

<a id="5-接入结果与复用"></a>
## 5. Adoption Results and Reuse

init returns actual roots, runtime roots, source/rule references, actual writes, still-relevant gaps, and next actions for this work. These form current context without a second dynamic context/state file.

Read back related files and paths; repeated adoption prioritizes reuse of determined sources and authorization. When any step is only partially complete, explain what occurred and what remains unfinished; next time recover from actual results rather than unconditionally rebuilding from scratch.

## 6. Language Preferences

Gamecaden has one plugin identity and one set of workflow rules. The package's English authoring language does not select the project's communication or output language.

Communication language and document language may be specified separately by the user or effective project guidance. Explicit instructions for this work take precedence over earlier preferences. Without an explicit preference, use the user's current language both for replies and newly created material documents, including Vision, Spec, Roadmap, PDP, designs, Tasks, Evidence, and handoffs. English Skills/templates, English input references, and the language of other project files do not establish an English output preference. Maintain an existing document in its language unless conversion is requested. Apply the same scope, verification, and acceptance requirements in every language.

Treat English templates as structural guidance, not text to copy verbatim. Prose and explanations default to the selected document language; adapt headings, section labels, table headers, placeholder prompts, and notes as needed for the user's reading and maintenance. Preserve schema keys, identifiers, enums, API names, paths, and executable commands. Follow established usage for professional terms and familiar labels, adding a local-language explanation when helpful. Translate human-readable values where their meaning permits; retain existing scope/coverage/version values when used as exact-match binding qualifiers, explaining them in the selected language rather than silently rewriting the binding. No new locale field or mandatory language interview is needed.

Apply the same default to newly authored human-readable metadata, including titles, purpose, snapshot_scope, reasons, and conclusions. Storage in YAML/JSON does not by itself select English; a new scope description is not an exact-match binding merely because its key contains "scope". On read-back, assess whether the actual document's prose, explanations, structure, and new readable values suit the selected language, rather than judging from reply language alone. Do not pursue documents with no English, mechanically translate established terms or every label, or make isolated English labels a verification or acceptance gate. Language preferences do not add a separate approval requirement.

When an ongoing language preference is actually selected during adoption or configuration, save it in the existing effective AGENTS.md/CLAUDE.md or agreed project guidance. Keep communication and document preferences distinguishable, and preserve unrelated guidance. An English package update does not translate existing project materials or change their maintenance sources.
