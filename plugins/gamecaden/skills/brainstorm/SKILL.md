---
name: brainstorm
description: Use only when the user explicitly requests Gamecaden for this work, or effective guidance in the current project has adopted Gamecaden. Clarify game ideas, requirement boundaries and key tradeoffs through successive questions, feasible alternatives and recommendations until the current discussion scope converges. Use for requirement exploration, solution selection or in-depth examination; do not repeat interviews for clear requirements or executable designs, and answer within scope when users explicitly want opinions only.
---

# Brainstorm

First check the applicability conditions above; when they are not met, follow original project guidance. See [Workflow applicability](../../shared/workspace.md) for boundaries.

Clarify requirements and key tradeoffs within current discussion through successive questions and grounded comparisons. Form conclusions after key tradeoffs are clear; do not replace requirement exploration with lengthy advice. Retain complete goals without manufacturing convergence through fixed questionnaires or reduced goals.

Resolve relative links from this SKILL.md's directory; ../../shared/ is in the common skill package root.

<a id="1-识别本轮讨论的范围"></a>
## 1. Identify this discussion's scope

Judge scope from user requests, supplied materials and existing work: the whole game, disagreements within an Epic/Task or a local tradeoff. Retain established scope, decisions and authorization.

When users invoke brainstorm for undecided game ideas, gameplay or solutions, advance by successive questions by default. Briefly state current understanding first, then ask one unresolved question with the greatest influence on subsequent direction, giving feasible alternatives and a recommendation; do not decide these requests want a one-time opinion only.

When users explicitly want opinions or comparisons without interviews, answer within that scope. “Discuss only, do not write files or implement” limits writing and implementation, without cancelling questions.

Read relevant facts and established conventions first. With a project, find current sources under [Workspace conventions](../../shared/workspace.md); without a project or when users only want to chat, discuss directly without initializing directories first. Do not ask users to repeat supplied design or ascertainable project facts.

When users explicitly skip brainstorm and goals are sufficiently clear, reuse inputs and enter required design/execution. Retain choices with clear existing answers; with only one unresolved key tradeoff, handle that tradeoff alone. Without unresolved matters requiring user choice in current scope, explain settled conclusions and the next action without manufacturing questions.

<a id="按未决项选择提问深度"></a>
### Choose question depth from unresolved matters

Judge depth from established goals and unresolved matters: what requirements remain unknown, whether decisions depend on each other, whether consequences affect compatibility, existing investment or irreversible results, and whether this round covers a local tradeoff, system or complete solution. Do not classify directly by question length, file count, lines of code or estimated hours.

| Current situation | Judgment grounds | Question depth |
|---|---|---|
| Requirements clear | No key user tradeoff in current scope; existing facts and decisions suffice for the next action | Retain decisions without manufacturing interview questions |
| Local tradeoff | One bounded, relatively independent unresolved choice | Focus on it; examine normal, failure and consequence boundaries when needed |
| Linked tradeoffs | Choices affect each other; upstream answers change later questions | Ask upstream first, unfolding relevant branches from actual answers |
| Open solution or comprehensive examination | Goals, main experience or scope unclear, or users request a thorough examination | Cover key branches within current scope; recheck omissions and conflicts before convergence |

Cover user-requested comprehensive examination within their scope; use existing answers for consistency checks without asking again. Check major consequences even for a single tradeoff; a local label does not skip boundaries.

These situations determine starting points and branch coverage, without question quotas or difficulty scores, and without binding to quick / standard / Epic. Judge implementation workload separately from interview unknowns: complex implementation with settled requirements goes to investigation or design; a one-line change affecting benefits, saves or lifespan still needs corresponding tradeoffs clarified.

When new facts or answers expose links, omissions or conflicts, deepen affected branches; directly retain resolved branches. Depth adjustment does not expand request scope; exit still follows [Convergence and pausing](references/decision-exploration.md#convergence-and-pausing).

<a id="2-找到有影响的分歧"></a>
## 2. Find consequential disagreements

- Understand desired experience through player actions, outcomes and feedback, distinguishing goals, means and current assumptions.
- Establish constraints, existing capabilities or production conditions touched here, avoiding solutions based on invented current state.
- Identify conflicts between goals, omitted consumers, costs and dependencies; recommend omitting content as appropriate, but recommendation does not mean users cancelled the goal.
- For open gameplay/solution selection, explicit continuous questioning or comprehensive examination, or interdependent substantive choices, read [Tradeoff exploration](references/decision-exploration.md) and cover key branches within current scope; a single local tradeoff handles relevant branches only.

Express complete goals, this round's outcomes and unadopted branches separately. Without a user request for reduction, staged arrangements retain complete commitments; give reasons for scope tradeoffs and keep them recommendations.

When visual, gameplay or experience expression helps compare actual directions, select relevant sketches, reference boards, rule examples or prototypes under [Material responsibilities](../../shared/material-requirements.md) and [Material use reference](../design/references/game-deliverables.md), explaining the disagreement resolved and cost. Reuse existing materials; exploration does not require a formal production package first. Report recommended experiments and actual runs separately; producing materials still follows this discussion's authorization.

<a id="3-提出推荐与真正必要的问题"></a>
## 3. Give recommendations and truly necessary questions

Investigate ascertainable technical facts first; directly handle implementation/presentation choices achievable through existing conventions and reasonable defaults. Ask users only about uninferable tradeoffs materially affecting experience, commitments, compatibility, cost or permissions.

Ask one key question at a time by default. With user-requested batch answers, or a few independent, brief and easy questions, ask multiple in a round as appropriate; questions dependent on unanswered content wait until the next round. Retain user-specified cadence.

For user tradeoffs, explain this question, necessary context, major benefits/costs of real alternatives and recommendation grounds. Use short conversation, tables or the textual example below according to question and user cadence. Default to 2–3 genuinely feasible options, recommended first; give two when only two real directions exist. Check recommendation/reason consistency before asking, and number correspondence when numbering. Include only background needed to answer, expanding detailed grounds as needed.

```markdown
**Question: <One key tradeoff to settle this round>**

<Necessary background: why this tradeoff affects the current goal>

1. **<Direction A> (Recommended)** — <Approach, main benefits and costs>
2. **<Direction B>** — <Approach, main benefits and costs>
3. **<Direction C>** — <Approach, main benefits and costs; include only if a real third direction exists>

**Recommendation grounds:** <Why the first choice fits current goals and constraints better>

You can reply with a number or describe another direction, or ask further questions without choosing yet.
```

When user intent is insufficient for real alternatives, or the question needs ideas that cannot reasonably be enumerated, ask an open question; the following text is an optional example. Compare directions after clarification; do not invent options to meet a count.

```markdown
**Question: <One key intention or preference the user needs to express>**

<Necessary context and known constraints>

**Suggested starting point:** <A direction and reasons for consideration, not an already-made user decision>

You can describe your ideas directly or ask further questions first.
```

Wait for an actual answer before advancing the next round dependent on that decision. For questions about option meanings, free discussion or no choice yet, explain/discuss first; the tradeoff remains unresolved. Do not treat follow-up questions, missing answers or recommendations as user choices. If explanation reveals options need changing, explicitly relist them and wait for an answer.

After answers, update settled conclusions and unresolved branches, test boundaries through concrete situations, counterexamples, failure/retry paths or resource conflicts, then ask the next currently decidable question. Continue questioning while key branches remain unresolved; a list of pending matters does not replace resolution. No fixed round count applies; convergence conditions appear in [Tradeoff exploration](references/decision-exploration.md#convergence-and-pausing). Use explicit user choices directly; revisit affected parts only when positions change.

<a id="4-保存到原本应负责的位置"></a>
## 4. Save where responsibility originally belongs

For persistent retention, locate under [Common record rules](../../shared/records.md):

Write direction conclusions in adopted projects back to current primary documents designated by index; at first formal adoption, form definite entrypoints under [Current project primary documents](../../shared/records.md#current-project-level-bodies). Cite specific original-material scopes for grounds and organize clear existing goals directly; unselected directions are not adopted conclusions.

| Conclusion | Destination |
|---|---|
| Complete experience, boundaries, key directions | Vision |
| Common agreements for bounded changes | Epic |
| Requirements, solution judgments or unresolved matters of current delivery | Original Task |
| Explicitly effective long-term rules | Corresponding Spec, distinguishing actual implementation state |
| Branches outside commitments worth revisiting later | Independent parking lot |

Save valuable interim conclusions in work within adopted projects, distinguishing settled, recommended and assumptions needing verification. Open exploration can start in conversation; explicit chat-only requests do not persist files. No talk file per round or automatic Task/Epic creation merely for discussion is needed.

For additions, replacements or deferral of current work, use flow's [Change rules](../flow/references/change-work.md), retaining valid history. Do not split ordinary records for file count.

<a id="5-收住当前分支并继续正确的动作"></a>
## 5. Close the current branch and continue the correct action

Close the branch under [Tradeoff exploration](references/decision-exploration.md#convergence-and-pausing)'s convergence/pausing conditions, explaining settled conclusions, consequential unknowns and their ownership, and the next action. Keep asking while key user tradeoffs remain unresolved; stop within scope for requests to stop, retain candidates or give opinions only. Unresolved candidates do not constitute completed implementation preparation.

With clear goals but missing practical arrangements, read [design](../design/SKILL.md). With an executable solution and requested implementation, continue corresponding actions; discussion/design-only requests deliver those results without unilaterally performing production or engineering changes.

For phased delivery of a selected large solution, design organizes upper-level arrangements under [PDP](../../shared/phased-development.md), retaining original design and settled conclusions. Whether solutions update Vision depends on directional impact; ordinary tradeoffs or sufficiently established work do not automatically add PDP.

A single issue needing correction does not reopen a full interview; technical unknowns can be handled by investigation or authorized bounded experiments rather than perpetual questions replacing evidence gathering.
