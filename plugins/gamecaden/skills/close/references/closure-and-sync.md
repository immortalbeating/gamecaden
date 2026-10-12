<a id="关闭范围调整与事实同步"></a>
# Closure, scope adjustment and fact synchronization

Read corresponding parts for unfinished items, parent/child work, multiple baselines, historical closure or interrupted writeback.

<a id="1-依据自己的交付承诺"></a>
## 1. Follow the work's own delivery commitments

| Situation | Closure judgment |
|---|---|
| Quick implemented with necessary checks complete | Briefly record and close under conditions; no mandatory independent review or lengthy closure report |
| Design Task delivered qualified design | Close against design conditions; unimplemented future code is not automatically its deficit |
| Content package meets its own checks/acceptance | Close against package scope; actual adoption belongs to work committing that result |
| Actual runtime integration committed, with only files/import results | Corresponding runtime obligations remain unmet |
| Agreed human acceptance/independent verification missing | Retain deficits; do not waive unless users explicitly adjusted arrangements |
| Original goal incomplete, merely allocated to subsequent Task | Clear destination does not fulfill current commitments; original work stays unfinished |
| Users explicitly narrow work to completed parts and defer another delivery | Save scope change/later owners and close against revised conditions; retain later/milestone requirements |
| Users explicitly no longer need unfinished delivery | Record cancellation/replacement, not successful completion |

When human judgment is deferred, record its actual absence and owner; do not write “accepted by the user”. For delivery permitted with known limits, retain limits and allowed scope; verification facts still follow actual results.

<a id="2-epic-与里程碑"></a>
## 2. Epics and milestones

Read overall exits first, then Task deliveries. Shared inputs, version compatibility, end-to-end integration and overall experience may not belong to any child's independent acceptance; they need corresponding evidence/decisions.

Roadmap M and PDP S each follow original scope; identical conditions precisely cite original Epic/Task exits. Combined conditions of different scope cannot merely concatenate local passes. Synchronize route/plan summaries and original grounds when valid results affect overall judgment; stages have no other closable state. See [Phased development](../../../shared/phased-development.md) for PDP details.

All child Tasks closed does not automatically close Epic; administrative nonclosure of a shared Task does not necessarily block independent work with satisfied prerequisites. Owners define dependency on actual results/status; do not infer from counts/labels alone.

When transferred necessary items remain current Epic commitments, keep Epic unfinished. Only explicit scope changes alter exits; separately judge other milestones/Epics referencing the same result instead of automatically allowing all.

Correctly closed child Tasks retain history. Actual responsible scopes handle new integration defects; do not reopen all children to make status tidy.

<a id="3-过去正确与过去误判分别处理"></a>
## 3. Distinguish correct historical closure and past misjudgment

When old tasks genuinely met commitments at original baseline but later new requirements/regressions invalidate results, retain old closure facts; appropriate current work owns changes and links history.

When investigation confirms missing mandatory deliveries, misused evidence or false acceptance at original closure, save correction reasons and original records, reopening original tasks as needed. Do not rewrite old reports to make mistakes appear never to have occurred.

Unclear scope, age or temporarily unfindable evidence alone cannot establish erroneous historical closure. Investigate past commitments and available materials first; explain remaining uncertainty, supplementing current required verification as appropriate.

<a id="4-同步范围与写入顺序"></a>
## 4. Synchronization scope and write order

1. Read current sources and list facts, declared baselines and owners actually requiring writeback; preserve content updated by other work.
2. Write still-valid current behavior/limits back to corresponding Spec, distinguishing target rules and actual implementation; candidate results unmerged to mainline are not mainline capabilities.
3. Synchronize asset references, affected Epic/Roadmap, experience or later ownership as needed, without copying execution streams.
4. Check delivery destinations, save original Task/Epic closure grounds and update lifecycle, reading back to confirm; for Git, complete necessary actions and version-control/synchronization of closure records under [Git delivery reference](git-delivery.md). This process does not move main entrypoints by default.
5. Refresh actually existing affected current views under [Derived outputs](../../../shared/derived-outputs.md), retaining sources, scope and time; frozen snapshots save separate rounds. Retain actual paths/generation methods; ordinary closure does not generate empty view packages, and defaults apply only to genuine new creation.

This is logical order, not a claim that cross-file transaction tools exist. When others change sources in between, recheck and merge current scope instead of overwriting new text with old snapshots; use effective atomic-write/version-check protocols when tools offer them.

For failed necessary authoritative writeback, explain how far delivery facts reached and the missing closure step, retaining recoverable state. If closed was written before necessary synchronization completed, correct inconsistent closure records and save reasons; status fields do not prove successful full closure.

When authoritative records and necessary synchronization are complete but reconstructable Progress/Timeline refresh alone fails, usually retain actual closure conclusions and mark views lagging, repairing projection only; if updating the view itself is mandatory Task delivery, judge against that commitment.

<a id="5-收尾不隐含清理或发布"></a>
## 5. Closure does not imply cleanup or release

Closing records does not delete candidates, evidence, adopted files or dirty worktrees; retain referenced materials and others' changes. For needed cleanup, check actual sources/references and execute user-authorized scope.

Code completion, committed, merged, packaged and published each have facts. Do not add release gates when original goals stop at code delivery; when goals include release, Task closed alone cannot establish completed release.
