---
name: develop
description: Use only when the user explicitly requests Gamecaden for this work, or effective guidance in the current project has adopted Gamecaden. Implement or repair defined deliveries, connect code, scenes, data and resources to actual runtime paths and verify them. Support explicit quick changes and sustained Tasks; reuse existing design directly and coordinate content production with assets as needed.
---

# Develop

Apply the [workflow applicability boundary](../../shared/workspace.md#workflow-applicability) before using this responsibility.

Advance authorized goals to observable engineering results, verify according to actual impact and write back to original work. The model judges methods, step granularity and necessary collaboration; goals, fact sources and delivery commitments remain traceable.

Resolve links from this Skill's directory; ../../shared/ is the package's shared/ directory.

<a id="1-接住原交付并核对现场"></a>
## 1. Take over original delivery and check the situation

Retain original work, goals, design, acceptance, advancement constraints and authorization from current context or [flow](../flow/SKILL.md). Check actual [source/runtime locations](../../shared/workspace.md#1-locations-and-resolution) and applicable [rules](../../shared/rules.md#1-select-sources-for-current-work), reusing valid context.

Check related code, scenes, resource references and existing changes. Distinguish current changes from others before writing; when using editors, bridges or external runtime processes, check connected projects and worktrees. Use separate worktrees only for actual isolation/parallel needs, not every quick change.

For Git delivery, follow the existing [policy and explicit exceptions](../../shared/git-policy.md), checking actual destinations and including only owned changes. Unselected recommendations do not authorize Git actions.

Establish whether users request implementation, repair, integration or investigation only. Return read-only diagnosis/design within scope, without expanding into runtime changes because tools exist; continue complete implementation requests through original commitments.

<a id="2-选择执行深度"></a>
## 2. Choose execution depth

Keep original work. Use [Task modes](../../shared/records.md#selecting-the-management-mode) only when organization needs judgment; follow [record structure](../../shared/records.md#creation-and-saving) when saving. Entering implementation creates no new Task.

When original work belongs to a [PDP](../../shared/phased-development.md) Stage, read necessary current inputs/actual prerequisites and original Task/Epic, advancing actual executable delivery. Stages are orchestration only; Task ownership and lifecycle remain. Reuse sufficient local arrangements directly without a full upper-level plan for engineering quick changes.

Use sufficient executable design directly. Return to relevant [design](../design/SKILL.md) parts for missing implementation arrangements; clarify locally only when actual product tradeoffs are unclear. Investigate ascertainable facts and decide ordinary reversible choices yourself.

For formal production inputs, cross-system relationships or integration conditions, check matching [material responsibilities](../../shared/material-requirements.md#domain-triggers). Read known original sources directly; use [derived views](../../shared/panel-workflow.md) when cross-record discovery or an overview is needed, then read back sources. Local changes check related conditions only.

For bugs, key unknowns, repeated failures, parallel/isolation needs or interruption recovery, read corresponding [Execution and recovery](references/execution-and-recovery.md) parts.

<a id="3-实现完整的可观察路径"></a>
## 3. Implement complete observable paths

Connect inputs, state, content/data, consumers and results along actual triggers. Follow established responsibility boundaries and lifecycles; necessary structure changes serve correct implementation, avoiding more new behavior in wrong owners.

For new pages/levels, reusable objects, cross-lifecycle state or editing changes, apply [structural ownership](../../profiles/references/structure-contract.md) and matching engine/platform topics. Establish real types, composition, dependencies, authoritative state and production/editing entrypoints; fill local gaps affecting implementation. Empty files or managers do not establish structure.

For reusable UI components or shared UI style/interaction changes, apply [UI families](../../shared/ui-families.md#production-and-implementation) to actual resources, behavior and consumers, inspecting existing implementations first.

With integration risks, first connect real paths that verify them, then expand remaining commitments; a successful small segment does not reduce complete goals. Complete ordinary explicit changes directly without unrelated abstractions, repository-wide refactoring or fixed-granularity steps in advance.

For generated outputs, check actual sources and generation methods first, maintain correct sources and regenerate. For editor-managed resources, imported files or stable reference identities, use applicable project methods to prevent code and scene/resource inconsistency.

For mid-work additions, replacements, deferral or cancellation, adjust original work and affected arrangements under flow's [Change handling](../flow/references/change-work.md). Retain established results; stop only actions dependent on unresolved information.

<a id="4-与内容生产协作"></a>
## 4. Collaborate with content production

Use [assets](../assets/SKILL.md) for new materials, content variants or source revisions; qualified existing materials integrate directly without regeneration.

Check specific version, use, consumer and corresponding allowed scope under [Asset handoff and adoption](../../shared/asset-handoff.md), then import resources, wire configuration/scenes and check runtime. Continue to formal integration when committed; for candidate-preview requests, preview as agreed without registering temporary wiring as formal adoption.

Locate integration failures first: return content/format problems to production, repair engineering reference/state/lifecycle problems in implementation, and return contract conflicts to relevant design. Collaboration remains within the same delivery without new Tasks per Skill switch.

<a id="5-以实际影响完成验证"></a>
## 5. Complete verification by actual impact

Judge verification from user requirements and effective rules, using real project commands, tools and player/user entrypoints. Select checks covering impact, adding discriminating tests when needed; quick/standard labels do not mechanically dictate test counts or full regression.

State coverage of file existence, compilation, static checks, resource import and runtime paths separately. For movement, page switching, input focus, save restoration or resource switching, verify actual corresponding paths; injections/screenshots skipping key links cannot replace them.

Reuse evidence after checking object, inputs, baseline and coverage under [Verification conventions](../../shared/verification.md); when changes invalidate it, supplement relevant checks only. End verification on grounded passes; handle actual causes of failure. Record not run, interrupted, timed out or unavailable environments honestly without recasting as passes.

Complete human acceptance or independent verification when original delivery/project rules require it; distinguish tool PASS, model checks and user acceptance by actual source. Continue with [verify](../verify/SKILL.md) for complete coverage judgment or independent verification; use results directly for explicit small changes with sufficient checks.

<a id="6-同步事实与交接"></a>
## 6. Synchronize facts and hand off

Save engineering changes, actual checks, remaining requirements and next actions under [common writeback rules](../../shared/records.md#6-current-facts-closure-and-aggregation), citing detailed reports at their original locations.

Update affected Spec when current behavior enters declared baseline; for assets, synchronize selections/references and integration evidence. Refresh only existing affected current views under [derived outputs](../../shared/derived-outputs.md#refresh-and-retention).

Judge closure from Task commitments and [Common closure rules](../../shared/records.md). Retain actual unfinished items when necessary acceptance/checks are incomplete. After delivery conditions are met, continue corresponding closure when explicitly requested or complete delivery is authorized; use [close](../close/SKILL.md) for complex closure. Retain explicit partial-implementation or no-closure limits. Git commits, merges, packaging and publishing each retain actual authorization and requirements.
