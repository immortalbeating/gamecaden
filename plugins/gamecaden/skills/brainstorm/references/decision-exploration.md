<a id="关键取舍与有依据的追问"></a>
# Key tradeoffs and evidence-based follow-up questions

Read for open gameplay or solution selection, explicit requests for continuous in-depth questioning or comprehensive examination, or interdependent substantive choices in the current solution. This reference specifies branch coverage, follow-up and exit within the current discussion scope; local requirements cover relevant branches only.

<a id="看清当前分歧"></a>
## Understand the current disagreement

First explain the result users want, then examine whether the proposed solution actually achieves it. For example, highly automated gameplay still needs to explain where players make meaningful choices; compact experiences and large-scale long-term content also need explicit respective scopes, rather than being listed as parallel features alone.

Confirm facts from relevant sources: adopted rules, actual code/content, target platforms and consumers. Treat judgments lacking evidence as assumptions; avoid disguising unknowns as infeasibility or claiming there are no costs to accommodate users.

<a id="用具体反例检查"></a>
## Check with concrete counterexamples

Select angles that change the current solution, rather than asking every item:

- When players see results on normal paths, and what happens on failure or retry.
- Whether two goals compete for the same input, screen space, state owner or production resources.
- Whether new content needs consumers, data or sustained maintenance absent from the original solution.
- Whether current design depends on an unselected direction or treats illustrations/candidates as established contracts.
- Whether one bounded investigation/experiment can verify key assumptions instead of continued guessing.

Describe discovered impacts within actual scope; do not turn every future risk into a current gate.

<a id="给出意见"></a>
## Give an opinion

Explain how each feasible direction meets user outcomes, what it gives up or adds, then recommend the direction best fitting current constraints. When opposing an idea, give concrete reasons and value that can be retained; before the user chooses, recommendations remain recommendations.

The model handles ascertainable facts, established decisions and ordinary reversible implementation/presentation choices within authorization. For user tradeoffs changing current requirements, product commitments or material preferences, ask under the main Skill; an apparently better recommendation does not replace user choice. Do not ask users to decide ascertainable APIs, file paths, ordinary control positions or internal implementation details.

<a id="问题组织与退出"></a>
## Organizing questions and exit

Ordinary clarification resolves the current concrete disagreement; in-depth follow-up continues through decision branches within current scope that change outcomes. When users explicitly request comprehensive examination, cover key branches of the entire solution; do not end early merely because one main path can be implemented.

<a id="连续深入追问"></a>
### Continuous in-depth follow-up

1. List key unresolved branches and dependencies from existing goals and materials, using the main Skill's [Depth judgment table](../SKILL.md#choose-question-depth-from-unresolved-matters) for current coverage. Distinguish ascertainable facts, user tradeoffs and experience assumptions requiring experiments; the list supports current reasoning and, when retained, goes into unresolved items in original records.
2. Handle upstream choices that alter subsequent questions first. Follow the main Skill's question cadence to explain this question, relevant alternatives and recommendation grounds, choosing suitable expression; present only the current question and necessary context, each question focused on one decision. Leave details dependent on unanswered content to the next round instead of dumping the entire design tree.
3. Wait for an actual answer. For explanation requests, free discussion or deferral of choice, clarify first; the original tradeoff remains unresolved. After a decision, check consistency with existing agreements and test boundaries through concrete player situations, counterexamples, failure/retry paths or resource conflicts. When users say “both”, establish respective scopes and conflict priority without deleting one yourself.
4. Promptly update established conclusions under brainstorm record ownership, retaining precise boundaries, numbers, exceptions and negative requirements; recommendations and experimental assumptions retain original identities. For explicit chat-only requests, organize within the session only. No new document or Decision is needed per round.
5. Reassess unresolved branches; while tradeoffs affecting current discussion remain, ask the next currently decidable question. New facts or answers revealing relationships, omissions or conflicts deepen affected branches; do not end early because initial classification was light. Revisit only affected parts when users change goals; reuse existing answers and let the model judge ordinary reversible implementation details.

<a id="收敛与暂停"></a>
### Convergence and pausing

Before entering design or implementation preparation, current goals, affected objects, commitment boundaries, key tradeoffs and observable acceptance results should be clear; user tradeoffs affecting current results must be resolved. Keep asking when blocking decisions remain; merely registering “awaiting tradeoff” cannot establish convergence.

Handle technical facts through investigation and experience/performance assumptions through bounded experiments. Unknowns in later batches can be deferred only with clear ownership and no actual blockage of current delivery; deferral does not cancel complete goals or turn unverified assumptions into facts.

For comprehensive examination requests, recheck key branches and commitments in original materials for omissions, weakening or conflicts with new conclusions; do not end because one main path is implementable.

When users request stopping questions, pausing or retaining multiple candidates, stop within that scope and explain settled and unresolved matters. Open candidates or user pauses do not complete implementation preparation; question count or many rounds do not justify exit.

There is no fixed number of question-and-answer rounds or new uniform final approval step; retain actual project rules and existing authorization. Intensive questioning can expose requirement contradictions; performance, feasibility and “is it fun” still require corresponding evidence or experience experiments.

For experiments, explain question, scope, inputs and observation method. Implement only within original authorization; a discussion-only request may receive experiment recommendations, without engineering changes or claims that experiments passed.
