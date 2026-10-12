---
name: verify
description: Use only when the user explicitly requests Gamecaden for this work, or effective guidance in the current project has adopted Gamecaden. Verify explicit deliveries, changes, assets or milestones; judge requirement coverage, evidence applicability, actual runtime results and necessary acceptance. Use to check fulfilled commitments, independently review or supplement acceptance evidence; reuse valid results within current scope without automatically expanding into full-project audits or release.
---

# Verify

First check the applicability conditions above; when they are not met, follow original project guidance. See [Workflow applicability](../../shared/workspace.md) for boundaries.

Answer which commitments of the current object hold, which failed or remain unproven, and the grounds. Share [Verification conventions](../../shared/verification.md) with implementation and closure; check results return to original records.

Resolve relative links from this SKILL.md's directory; ../../shared/ is in the common skill package root.

<a id="1-确定核验目标和允许动作"></a>
## 1. Establish verification goals and allowed actions

Locate actual project/runtime roots, original Task/Epic, requirements and existing evidence under [Workspace conventions](../../shared/workspace.md). Distinguish local checks, complete-delivery verification, independent review, experience-acceptance preparation and release judgment.

For status-only or explicit read-only requests, read/report within scope; when actual verification is allowed, run corresponding checks and produce necessary evidence. Verification permission does not automatically include production implementation changes, clearing player saves, publishing or operations on other projects.

Read matching effective conditions through [Rule selection](../../shared/rules.md). Retain explicit scope and acceptance decisions directly; “reacceptance” does not justify another general approval round or reduced goals.

<a id="2-对照要求审查现有证据"></a>
## 2. Review existing evidence against requirements

Read original requirements and actual objects first, then development checks, content reports and conclusions. Brief work states correspondence directly; complex deliveries organize necessary coverage in original records/existing reports, without parallel acceptance ledgers.

Judge reusable, invalid or missing conclusions under common verification conventions. Check versions, consumers, environments, inputs and coverage; report titles, completion percentages, material counts or subtask status alone do not prove goals.

Choose sufficient checks for uncovered/doubtful parts. For game inputs, scenes, assets, saves, performance or target platforms, read [Game check scope](references/game-checks.md) as needed. Do not expand unrelated domains.

Associate material gaps with actual actions under [Material responsibilities](../../shared/material-requirements.md); locate conditions through the panel under [Panel continuation](../../shared/panel-workflow.md) and read back original requirements/evidence, without treating derived status as verification results.

<a id="3-完成必要检查或独立核验"></a>
## 3. Complete necessary checks or independent verification

Use actual available project commands, tools, scenes and user paths; call applicable specialized Skills when needed, retaining task/evidence ownership. Confirm target instances and test data before runs, protecting existing changes and player data.

Verification may produce reports, caches or isolated test materials; use applicable locations and explain relevant side effects. Strict read-only requirements prohibit file-writing checks. Production implementation retains the tested baseline; do not modify outcomes while calling the same observation verified. Hand actual repairs back to corresponding execution responsibility, then reverify.

Judge need for independent executors under common conventions; ordinary use of verify does not necessarily delegate another agent. When independent verification is genuinely required, retain executor, baseline and coverage grounds; absent capabilities mean missing conditions, not fabricated independent conclusions.

After passes, expand/repeat only for new changes, failures or specific uncovered requirements. For unavailable checks, record reasons and alternative-evidence coverage; a pending checklist cannot masquerade as results.

<a id="4-给出范围准确的判断"></a>
## 4. Give accurately scoped judgments

For current necessary requirements, state passes, failures, undecidable or unchecked facts; distinguish existing failures and current regressions, explaining blockers to current delivery.

State technical results and necessary human judgment separately. Prepare reviewable objects, versions and aspects for user acceptance; cite applicable existing decisions directly. When users change acceptance arrangements, retain actual untested parts and adjustment grounds without rewriting old evidence.

Overall conclusions cover verified scope only. Local, machine or model-review passes cannot be restated as completion of the entire game, all experience or release.

<a id="5-保存结论并继续原工作"></a>
## 5. Save conclusions and continue original work

Save current conclusions and Evidence/Decision references under [Retention, indexing and versions](../../shared/records.md#retention-indexing-and-versions), writing back original Task/Epic. Synchronize Roadmap for product outcome/overall judgment impacts and original [PDP](../../shared/phased-development.md) for Stage orchestration impacts; summaries cite actual grounds. Deliver in conversation for read-only or explicit no-persistence requests. Formal exits, independent reviews or version comparisons use locatable reports; cite complete existing reports directly.

For Stage/milestone verification, recheck actual conditions and necessary combined results within scope. Shared conditions cite original Task/Epic; unique conditions are judged in corresponding PDP/Roadmap. Counts and created records do not prove passes. Stage/PDP do not call record.transition or add human acceptance per item.

For implementation-inclusive requests, return failures by cause to [develop](../develop/SKILL.md) or [assets](../assets/SKILL.md), repairing and supplementing verification in original work; check-only requests report problems/recommendations. Return locally to corresponding responsibility for necessary design/scope changes, continuing independent work.

After all necessary conditions are met, continue under [close](../close/SKILL.md) when closure is explicitly requested or complete delivery authorized. For verification-only or explicitly no-closure requests, report conclusions and retain scope without automatic lifecycle changes. A verify pass does not itself close a Task, Epic or release version.
