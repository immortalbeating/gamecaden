<a id="git-交付与收尾"></a>
# Git delivery and closure

Use for Git delivery in this work; see [Project Git policy](../../../shared/git-policy.md) for allowed scope and policy sources. Unadopted recommendations do not authorize operations.

<a id="1-核对本次终点与实际现场"></a>
## 1. Check current endpoints and actual situation

Establish delivery destinations from original Task, user instructions and adopted policy: local files, commits on specified branches, PR, target-branch integration, remote synchronization or explicit release. Each has its own result, without new Task status enums.

Check repository/worktree, branches, relevant differences, existing staged content, targets and remotes. Protect unrelated changes and permanent worktrees; operate from established actual sources rather than guessing directory/default branch names.

<a id="2-提交本次拥有的内容"></a>
## 2. Commit owned content

Organize commits by actual needs; one Task need not have exactly one commit, and each step need not commit. Retain valid develop checkpoints directly; close completes remaining content.

Confirm code, scenes, necessary assets/metadata and records in proposed commits belong to this work; generated outputs, large files and raw materials follow project storage/ignore rules. Stage owned differences only; do not directly include others' staged changes or mixed same-file edits. Clarify only ownership that cannot be established.

After commits, check actual included content and traceable grounds. Do not create empty commits without pending owned changes; use existing commits directly when they suffice.

<a id="3-集成推送与关联动作"></a>
## 3. Integration, pushing and related actions

| Action | When needed and how to check |
|---|---|
| Integration/merge | Execute when delivery to agreed target branches is required; check actual inclusion and necessary integration checks |
| PR | Create/update along adopted review routes, meeting conditions and host attachment/linking requirements; created PRs do not prove merges |
| Push | Execute necessary authorized synchronization; check correct remotes, branches and actual results. Pushed task branches do not prove target-branch integration |
| Tag/Release/deployment | Execute only for explicit corresponding goals/release policy, using corresponding verification/authorization |
| Branch/worktree cleanup | Execute authorized cleanup when results/necessary evidence are safely retained and no untransferred changes or active use remain |

When targets change or merging/conflict repair changes implementation, check new baselines and supplement relevant verification; retain other valid evidence. A new SHA from record-only commits does not require unchanged game checks rerun.

Handle ordinary conflicts resolvable under established semantics within integration authorization; for substantive product tradeoffs, overwriting others' results or unclear historical handling, prepare concrete differences/impacts then obtain missing decisions. Automatic delivery does not authorize force-push, overwriting others' commits or rewriting shared history, nor bypass protections.

Consider actual integration methods/content mappings, not only branch names, PR titles or old tracking status. Handle known external push effects under policy; address new uncovered impacts in corresponding scope first.

<a id="4-把结案写回真实权威位置"></a>
## 4. Write closure back to actual authoritative locations

Save tested-baseline facts and remaining Git actions, completing commits, integration, necessary checks and synchronization against current goals. Express corresponding Spec/conclusions as adopted in a baseline only when target branches/remotes actually receive results; candidate passes are stated as candidates first.

After integration, check which actual branch/worktree maintains closure records, avoiding updates only in old worktrees about to be cleaned. Original Task retains identity and clear sources; do not create same-goal records to replace merging/synchronization.

Necessary Git delivery and authoritative writeback jointly determine closure completion. When closure records themselves need version control/remote synchronization, complete record commits/synchronization under the same adopted policy; do not leave unexplained dirty changes.

Link existing implementation commits, target references, PRs or native receipts; records need not include their own containing commit SHA, avoiding endless commits updating self-SHAs. Read back final results without another parallel log per Git command.

Git actions and file writes are not inherently cross-system transactions. If closed was written while necessary delivery/synchronization remains, correct inconsistent records under [Closure and synchronization](closure-and-sync.md), retaining recoverable next steps; status fields do not prove complete delivery.

<a id="5-部分失败与恢复"></a>
## 5. Partial failure and recovery

State actual completed/unfinished commits, integration, pushing and release separately. Retain valid local commits/verification when pushing fails and continue remote deficits; do not roll back completed implementation or force-push around rejections.

For interrupted connections with unclear remote results, query actual results before deciding retries. Safe retries within original authorization need no repeated confirmation; address concrete divergence, conflicts or unmet protection checks.

Goals of specified-branch commits can close when satisfied. Target-branch integration or remote-delivery goals cannot call deficits merely subsequent work and claim completion. Record explicit user scope changes and handle new conditions accordingly.
