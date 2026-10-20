---
name: init
description: Use only when the user explicitly requests Gamecaden for this work, or effective guidance in the current project has adopted Gamecaden. Identify, adopt, complete or migrate projects; establish actual runtime roots, authoritative documents and task source mappings, and merge project guidance. Use for explicit adoption needs or relevant mapping gaps found by flow; reuse effective existing entrypoints for daily execution.
---

# Init

First check the applicability conditions above; when they are not met, follow original project guidance. See [Workflow applicability](../../shared/workspace.md) for boundaries.

Enable subsequent work to locate the correct project, applicable rules and sole write source. Ordinary initialization maintains adoption relationships; game features, asset production and engine setup still follow actual delivery.

Resolve relative links from this SKILL.md's directory; ../../shared/ points to shared/ in the common skill package root.

<a id="1-选择本次方式"></a>
## 1. Choose the current mode

| Mode | Conditions for use |
|---|---|
| inspect | Establish target roots, entrypoints or original record sources through read-only identification first |
| adopt | User requested using this workflow for the project or establishing a new project workflow |
| repair | Relevant mappings, entrypoints or guidance in existing adoption need repair |
| migrate | User authorized switching maintenance scope or management process of specified records |

Identification can happen automatically; writing retains existing adoption, repair or migration authorization for this work. Read-only questions and ordinary old-task repairs do not automatically become migration. When meanings conflict, prepare concrete scope, sources and impacts first, then clarify relevant choices.

<a id="2-识别实际现场"></a>
## 2. Identify the actual situation

Read [Workspace conventions](../../shared/workspace.md). Start from the user-specified location and actual current directory; check effective guidance, existing workflow entrypoints, relevant README/configuration, runtime identifiers and task sources.

- Distinguish project directory, actual runtime root, design material package and tools/panel. Identify purposes of multiple runtime entrypoints separately, selecting only targets needed here.
- With Git, check current repository/worktree and relevant differences; adoption remains possible without Git, without forcing repository initialization or a commit for registration.
- When a new directory has no runtime entrypoint, explicitly retain unknowns. Intended engines and future features are target materials, not verified runtime capabilities.
- Do not guess multiple candidate roots or conflicting authoritative sources from directory names/times. Continue useful read-only identification; clarify only when a write target needs deciding.

Read [Adoption and handover reference](references/adoption.md) for old projects, conflicts, repair or migrate branches; simple new projects do not load all migration details in advance.

When adoption involves game material responsibilities or viewing gaps through the panel, handle only relevant sources under [Material responsibilities](../../shared/material-requirements.md) and [Panel continuation](../../shared/panel-workflow.md); mapping does not equal adoption.

When establishing/confirming engineering conventions, use the [Profiles entrypoint](../../profiles/README.md) to match actual or explicitly selected engine, platform and current action; read corresponding structural items when creating/migrating directories. Selected but unestablished engineering is used for design arrangements; runtime facts remain unknown. Write adopted scope and project differences back to existing Spec/rules; package references do not become out-of-scope rule_sources paths.

For new projects needing page/level switching, reusable entities, state across lifecycles or explicit content editing capabilities, bring [Structural conventions](../../profiles/references/structure-contract.md) into design for corresponding solutions; init still handles adoption, without prebuilding an entire Main/Manager/directory set. Old-project registration records established current structure and present gaps; temporarily retained local single-scene arrangements do not become new-project defaults.

When the project already uses or explicitly intends Git and needs delivery conventions established/checked, read [Project Git policy](../../shared/git-policy.md). Investigate existing facts and rules first, retaining project conventions and explicit current instructions; directly arrange authorized Git actions with clear targets, clarifying only what is genuinely undecided for the current action. When long-term policy genuinely needs establishing or adjustment, offer automatic delivery, automatic commits only, manual Git and custom approaches, then save after an actual choice. Do not force a choice without Git or during conceptual exploration, or block authorized work because long-term policy is absent.

When adoption includes formal binary assets, repeated production outputs, or a missing large-file arrangement, read [Asset storage](../../shared/asset-storage.md). Reuse adequate existing rules; otherwise establish the needed versioning destinations, recovery and batch-retention arrangement in original project rules or current work, including the Git/LFS default and actual configuration checks where applicable.

<a id="3-决定真实需要的写入"></a>
## 3. Decide which writes are actually needed

inspect returns identification only, without automatically installing dependencies or writing project guidance. Before actual project adoption or first local I/O, check and prepare the environment under [Tool readiness and invocation](../../shared/local-io.md#1-environment-and-invocation), checking ready and actual invocation results. If unready, report reasons and unfinished scope; manual record writing cannot claim verified I/O. Other modes proceed incrementally within authorization:

1. Establish the workflow directory and sole entrypoint, preferring explicit existing locations; new projects default to game-workflow/, without overwriting conflicting occupied uses.
2. Read supplied requirements, design packages, rules and related work. Distinguish complete goals, effective rules, implementation arrangements, actual results, candidates and history; organize current Vision, necessary Spec overview and, by default for project-level sustained development, a Roadmap under [Current project primary documents](../../shared/records.md#current-project-level-bodies). Cite specific scopes and identify maintenance responsibility.
3. Register actual roots, current primary documents, original work collections and the default write source for new work; register applicable conventions under [Rule selection and loading](../../shared/rules.md), retaining detailed original materials in place. Inputs for multiple responsibilities are referenced by current primary documents, rather than replacing them wholesale.
4. Establish a readable index distinguishing current maintenance entrypoints from detailed/input/historical sources, explaining their purposes without duplicating progress.
5. Merge concise project guidance where it actually takes effect in the current host: AGENTS.md for Codex and CLAUDE.md for Claude Code; preserve existing user rules and unrelated content.

Save explicitly adopted long-term Git policy to original authoritative conventions; for new projects, use rules/git.md in the workflow directory when necessary and register its source. Current Git arrangements retain original work records; direct init without an original Task describes them in the current adoption result, without creating a Task or automatically rewriting project policy. Record only adopted solutions, targets/methods and applicable scope; recommendations are not decisions, and current branch/remote progress is not duplicated. Repeated adoption retains existing choices, handling actual changes or conflicts only.

Basic registration does not automatically create an initialization Task, empty Epic, asset ledger or entire directory set. Real batch conversion, engineering changes or migration deliveries needing tracking are handled by corresponding work under [Record conventions](../../shared/records.md).

When creating new native documents, choose only actually needed items from the [Template catalog](../../templates/catalog.md), validating corresponding structures under the [Format contract](../../shared/formats-v1.md). Remove empty optional sections, retain unknowns and do not copy sample facts. Reuse existing primary text such as pure vision to form a definite entrypoint; original materials and untransferred work retain identities. Templates guide only organization of current primary documents.

When [Local I/O tools](../../shared/local-io.md) create an unregistered new source, check returned source_registration_required/source_proposal and complete actual mapping through workspace.configure within this work's authorized adoption scope. Read back file creation and source registration separately; do not claim an ID resolves through existing entrypoints before registration.

Task records needed for an explicit flow delivery can be saved to the default collection when the target is unique and no old source exists, without full adopt first. Project-level long-term guidance, global documents and old-source switching still follow actual adoption/migration scope.

<a id="4-新项目引导"></a>
## 4. Guide new projects

Organize the next action from supplied materials: put complete goals of formal adoption in current Vision, maintained rules and ascertainable current state in Spec. Roadmap for project-level sustained development saves current real outcomes and unresolved arrangements; even one outcome can have a Roadmap, without inventing stages when direction is undecided. For phased delivery of a large existing solution, register original arrangements under [PDP](../../shared/phased-development.md) or hand to design for completion; PDP does not masquerade as primary documents or use fictitious Epics for storage. State candidates and commitments separately.

Use user requirements or executable designs directly, without requiring another brainstorm round. Clarify only when the next action truly depends on an unselected key direction; continue work supported by existing information.

Initialization only establishes correct entrypoints and factual boundaries. If the original request also requires making a game or implementing features, after registration return actual context to flow/the current executor to continue; creating a few documents does not complete the original request.

<a id="5-核对登记结果"></a>
## 5. Check registration results

Check current writes under [Workspace conventions](../../shared/workspace.md):

- Actual targets match declared roots; every file/runtime identifier declared existing can be located.
- Each file source has one current maintenance responsibility; scopes of multiple collections are clear, and the default source for new Tasks is unique or explicitly undecided.
- Current primary documents directly answer direction, grounds/baseline for rule adoption and product outcome arrangements; Roadmap in adopted project-level sustained development has an actual current entrypoint, conditions/ownership and unresolved scope. Detailed references resolve; original materials have no overlapping active maintenance responsibility; engineering preparation steps do not masquerade as product milestones. Conflicts remain unconfirmed; format passes do not replace content judgment.
- Project guidance is written in the current host's actually effective scope; existing override/nested rules and old manager entrypoints have no unhandled overlap.
- Repeated execution supplements only actual changes, without overwriting user text or creating a second entrypoint.
- Record actually saved, unfinished or unverifiable parts; failure of one write does not permit claiming entire adoption succeeded.

Writing project guidance and the host actually loading it next time are different facts. Check sources using current host observability; without actual loading evidence, report only that files were saved, not that automatic triggering was verified.

<a id="6-返回到原请求"></a>
## 6. Return to the original request

Briefly describe target roots, actual record sources, created/updated files, gaps still affecting the next action and recommended actions. Results may remain in current context; do not create another adoption state ledger.

When called by flow, return identified/registered facts; a direct initialization-only request ends here. If the original request includes implementation, continue its next action, avoiding repeated init→flow→init registration.
