<a id="项目-git-策略选择保存与沿用"></a>
# Project Git Policy: Selection, Storage, and Reuse

init establishes conventions, develop uses authorized checkpoint commits, and close completes Git delivery required by the Task. Read this when a project uses or explicitly plans to adopt Git and policy must be determined; this workflow description itself chooses no policy for a specific repository and authorizes no remote writes.

<a id="1-先查事实和既有规则"></a>
## 1. Check Facts and Existing Rules First

Locate the actual repository/worktree, current branch or detached state, existing staged and uncommitted changes, remote/tracking relationships, integration-branch conventions, and applicable PR/protection rules. Users may determine goals; the model investigates facts available from the repository rather than handing users a series of technical questions to fill in.

Prioritize existing project rules and the user's current explicit instructions. inspect only reports current conditions and recommendations; adopt/repair/migrate saves or adjusts conventions under corresponding authorization. A remote, example configuration, or recommended option alone does not authorize commits, merges, or pushes.

| Situation | Handling |
|---|---|
| Clear, applicable existing policy | Reuse directly and state its source; do not ask all options again |
| User has already specified Git actions and scope for this work | Arrange directly under this round's authorization; do not rewrite project policy without a request for long-term change |
| This round needs Git, but relevant permissions or targets are unclear | Resolve only choices missing for the current action; leave other unselected parts undecided |
| A long-term Git policy actually needs establishment or change | Provide options and recommendations grounded in checked facts; save project-level conventions after an actual selection |
| New session, ordinary continuation, or repeated init | Read saved conventions and check changes in actual conditions; do not reset policy to defaults |
| Original policy conflicts, is invalid, or user requests changes | Handle only specific conflicts/changes, retaining unchanged portions and applicability |
| No current Git, or concept exploration only | Continue corresponding work; do not force repository creation or a Git questionnaire for init/close |

Even while long-term policy is undecided, currently authorized Git actions with clear targets may proceed; keep this round's arrangements in the original work record. Design, implementation, and verification continue within original scope. First establish permissions or targets actually needed and missing for the current Git action; clarify only what existing authorization cannot determine. Existing protection conditions still apply. Ordinary local work does not require rerunning init because complete project-adoption files are missing.

For formal binary assets or a missing large-file policy, use [Asset storage](asset-storage.md#versioning-storage-and-recovery) for the Git/LFS default, exact inclusion rules, actual object checks and recovery arrangements. That storage choice does not expand Git-action permissions or migrate existing history.

<a id="2-需要长期策略时提供方案"></a>
## 2. Provide Options When Long-term Policy Is Needed

When long-term delivery policy genuinely needs establishment or adjustment, the following options may explain choices; custom policies are also allowed. When only this round's commit, integration, or push arrangements need supplementation, resolve current missing choices without requiring a complete long-term policy. Base recommendations on the actual project; for a solo project with clear integration targets and remotes, automatic delivery is usually a reasonable recommendation. Recommendations or preselection do not mean the user has chosen.

| Option | Behavior when adopted long-term |
|---|---|
| Automatic delivery | Form meaningful commits by task, integrate into the target branch in the agreed manner, complete necessary verification, then synchronize the agreed remote |
| Automatic commits only | Form traceable commits; do not merge or push by default, and state the branch where results actually reside |
| Manual Git | Complete files, verification, and work records; provide Git status and recommendations, leaving Git writes to the user or their designated process |

Custom policies may specify “commit and push the task branch, then integrate after PR review,” for example. For automatic delivery, specify direct-merge/PR routes, target branches, push destinations, and temporary-worktree cleanup; do not assume main/origin or include cleanup and release merely through the option name.

First fill in discoverable facts and existing decisions, then ask the user to choose genuinely undecided parts. Continue satisfying existing PR review/protection conditions; if pushing triggers known deployment/release, explain linked effects and clarify policy scope. Automatic delivery does not bypass necessary acceptance or repository protections.

<a id="3-一处保存静态约定"></a>
## 3. Store Static Conventions in One Place

Prefer Git conventions in existing authoritative locations such as AGENTS/project standards; do not copy another active policy. When a new project needs a standalone body, default to rules/git.md within the workflow directory, referenced by workspace.rule_sources or the actual project entry. Existing short rules may remain in their original location when sufficient.

Project-level policy stores only explicitly adopted long-term scope, including option, permitted actions, integration/push destinations or determination rules, PR/protection conditions, cleanup scope, and adoption grounds. Put this round's Git arrangements in the existing original work record; for direct init without an original Task, explain them in the current adoption result without creating a Task or automatically promoting them to long-term conventions. Keep unknowns truthful rather than filling template examples as project facts. Leave machine schemas to actual tool protocols; this page requires no new Task frontmatter fields.

Read current branch, ahead/behind, uncommitted differences, execution progress, and operation results from Git/original Tasks rather than copying another dynamic Git ledger. AGENTS and index retain only necessary entry points and invariants, without repeating complete rules.

Facts found through one-time checks, such as deployment configuration, are only sourced adoption grounds; recheck on relevant later changes. Policy stores the scope of permitted external effects; “no deployment task found during adoption” cannot become a permanent guarantee that deployment will never occur.

When a new policy differs from old provisions in the same scope, identify the adopted change and update old bodies or their effective-state explanations within authorization to avoid conflicting active rules. Follow explicit new user instructions directly; if their meaning remains unclear, ask only about that disagreement. Do not expand one project's choices to other repositories or global rules.

<a id="4-每项工作怎样执行"></a>
## 4. Execution for Each Work Item

Combine project policy and Task goals to identify this delivery's destination. Current explicit user exceptions (such as “commit only this time; do not push”) apply to the current Task and are saved in original work; without a request for long-term change, do not rewrite project defaults.

Execute actions sufficiently covered by existing policy directly, without asking again for each action. Supplement choices only for missing specific targets or permissions, substantive conflicts, uncovered external effects, and similar gaps. All actual operations remain limited to changes owned by this work, protecting others' staged/uncommitted work.

Policy determines permitted Git-action scope; it cannot silently reduce business commitments. When the original task explicitly requires mainline integration or remote delivery beyond current policy coverage, explain the specific difference and resolve the missing decision; a branch commit alone cannot be claimed as fulfillment of the original goal.

Follow close's [Git delivery and closure](../skills/close/references/git-delivery.md) for operations and interrupted recovery.
