<a id="规则来源适用范围与加载时机"></a>
# Rule Sources, Applicability, and Loading Times

Read this when adopting a project, forming a design, or when implementation/verification identifies new engine or domain impacts. Use a shared rule-selection mechanism rather than copying rule bodies into every Skill.

Rules help AI make better game-design, engineering, content, and verification judgments from effective development experience and standards. Following the [profile inclusion principles](../profiles/README.md), distinguish reliable grounds, current applicability, and candidate inferences. General guidance can prevent known detours early, while specific requirements are still triggered by the current goal and real objects. Market context or platform examples cannot expand the support scope on their own.

<a id="1-按当前工作选择来源"></a>
## 1. Select Sources for Current Work

First identify the objects affected using effective project guidance, the [workspace mapping](workspace.md), the current goal, and the actual project. Use rule_sources to locate sources when present; without a mapping, directly read existing effective standards rather than ignoring them because registration files are missing.

Select portions matching the current scope from the following sources rather than prereading everything:

- Common rules: basic conventions for goals, factual sources, state ownership, records, and evidence.
- Game domains: contracts actually involved in current gameplay, characters, maps, UI, animation/audio, saves, and other domains. When direction, production, or handoff inputs are missing, go directly from [material responsibilities](material-requirements.md) to relevant purposes and equivalent sources; do not turn the entire candidate catalog into requirements.
- Engines/frameworks/platforms: select by actual runtime root, confirmed version, and target; browser targets may combine Phaser, Three.js, or browser outputs of engines such as Godot/Unity/Cocos Creator. For other targets, check actual runtime/build conditions and reliable sources; collect preview and actual-delivery evidence separately.
- Project standards: currently effective specific conventions, adopted references, and applicable rules derived from historical issues.

When a Godot game includes an HTML approval panel, select rules separately for the game and panel; do not identify a side tool as the main game engine. If a new project has no selected engine yet, use only common and confirmed domain requirements to compare options; do not record future options as adopted profiles.

When common engineering, directory, or engine/platform rules are needed, read the current branch from the [profile selection entry](../profiles/README.md#select-what-this-work-needs). Reuse existing versions and scopes while they remain applicable; reassess matching items when the engine, target platform, consumer, or delivery action changes, without loading everything for every quick task.

<a id="2-明确规则的性质"></a>
## 2. Identify the Nature of Rules

Be able to explain the source, applicable objects/version, and whether cited content is an effective requirement, default recommendation, or conditional experience.

| Rule nature | Usage |
|---|---|
| Necessary condition | Once triggered, a result or technical mechanism necessary to fulfill the current effective goal; choose methods according to the project. A local gap affects only actions that depend on it. |
| Default practice | Use when no more suitable effective convention exists; the model may choose an equivalent method and explain material tradeoffs nearby, without exception approval. |
| Experience awaiting adoption | Suggests investigation directions or conditional candidates; historical issues, project numbers, and specialized production sequences do not automatically become gates in other projects. |

Rule nature and adoption state are separate: a proposed necessary condition is not yet an effective gate, and default methods cannot lower effective result requirements. Use authority/strength from [governance](governance.md) only when actually defining conditions for this project; do not automatically convert every profile item into a required condition.

- The user's current explicit requirements and effective host guidance constrain this work; existing authorization carries forward.
- When the user explicitly changes project requirements or grants an exception, act within their specified object/action scope for this round and record it in the original work; change long-term rules only when long-term adjustment is explicitly requested. Clarify only if scope remains unclear and would change actual actions; do not seek repeated approval for an explicit exception. Higher-priority host constraints still apply.
- Effective specific project conventions implement this project's requirements, with default recommendations in common profiles adjusted accordingly.
- Historical Notes, candidate plans, and other-project experience inform judgments; they become project requirements only after explicit adoption.
- Verify actual engine capabilities, version limits, and data facts. When documents conflict with facts, investigate the difference rather than assuming technical facts change because one document has “higher priority.”

When effective requirements conflict within the same scope, check sources and prior decisions; resolve directly when existing authorization suffices, and clarify only when actual product tradeoffs cannot be inferred. If rules are missing or versions do not apply, investigate actual local evidence and official sources; propose or save new standards within scope when needed, without claiming a nonexistent profile was loaded.

When changing effective project requirements, save old/new scopes and reasons in the original Spec/rule or Task; follow [records](records.md) when an independent decision is needed. After changing rules, consumers, or technical versions, review actually affected designs, materials, and supporting grounds; rereading the same unchanged version, changing sessions, or unrelated file updates does not trigger full revalidation. Changing acceptance scope does not turn unexecuted or failed evidence into passes.

<a id="3-何时读取与如何交接"></a>
## 3. When to Read and How to Hand Off

| Action | Rule use |
|---|---|
| flow / init | Locate sources and applicable runtime roots; register existing rules and selections during adoption, without copying entire bodies |
| brainstorm | Read relevant content when constraints affect goals, scope, or options |
| design | Before forming a plan, read requirements affecting structure, content production, compatibility, and acceptance outcomes; use them in the plan and verification arrangements |
| develop / assets | Before actual operations, read matching specific execution rules; load additional rules and review when inputs, engines, or scope change |
| verify / close | Assess coverage, actual results, and synchronization against commitments and effective rules for the same scope; do not temporarily add another set of gates |

design may call professional Skills actually available in the target environment as needed to obtain design judgments for this work. A design-only request still stays within design scope; available professional tools do not authorize production. Map specialized Skill record outputs back to original workflow records to avoid introducing a second Task/log system.

In the grounds or constraints section of the original Task/design, cite sources affecting this judgment and explain key results, for example, “Character proportions inherit the adopted reference; the new hit reaction follows the existing anchor convention.” There is no need to copy all standards or create a separate dynamic rule-loading log. Reuse already read materials that remain unchanged and applicable.

<a id="4-提供范围与验证边界"></a>
## 4. Provided Scope and Verification Boundaries

Existing shared contracts and design references provide record and material responsibilities; [profiles](../profiles/README.md) centrally maintain candidates and version boundaries for common engineering, project structure, engines/frameworks, and browsers. Specialized execution still uses currently available Skills/tools; verify specific APIs against actual versions.

Rules, calling guidance, and document-consistency checks are not actual engine-adaptation runs. See [release validation records](https://github.com/immortalbeating/gamecaden/blob/v0.1.3/docs/validation.md) for installation, upgrades, host discovery, and bounded pilots with existing new and old projects; each result retains its original version and scope, without extrapolation to all engines, hosts, or projects. Current execution still collects evidence for real consumers, environments, and delivery commitments.
