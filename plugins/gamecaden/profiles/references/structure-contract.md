<a id="工程结构组成状态生命周期与验收"></a>
# Engineering structure: composition, state, lifecycle and acceptance

Read this when adding independent pages/levels, cross-interface state, reusable entities, cross-lifecycle listeners, or changing how content is edited. It implements [GAME-OWNER, GAME-LIFETIME](../common.md) and [LAYOUT-BOUNDARY](../project-structure.md); choose engine/framework mechanisms from [profiles topic entries](../README.md). Routine typos, local value adjustments and fixes within already clear boundaries review only actual effects.

<a id="何时先确定结构"></a>
## When to establish structure first

The following changes need composition and responsibilities explained before their relevant implementation; valid existing designs can be reused directly:

- First introducing pages, levels or game modes that can be entered/exited independently.
- Instantiating the same unit/interface in different locations, or reusing configuration while keeping state independent.
- Retaining character, inventory, current-session progress or other state across pages/levels, or adding restart/settlement/load-save entries.
- External subscriptions, asynchronous returns or background jobs may outlast the objects that created them.
- Adjusting stable content through an editor/panel has been promised, or original editing/preview methods cannot support this change.

New projects establish boundaries in their first playable slice involving these relationships. A bounded experiment with one page and local state can stay simple; when it expands to the scope above, complete the corresponding design before continuing. File line counts, scene counts and quick/standard labels alone do not determine structural compliance.

For existing projects, first check actual owners, readers and effective rules. Reuse structure when it can support this delivery; if this defect or added behavior comes from confused lifecycles, shared state or hidden dependencies, relevant boundary adjustment belongs to this implementation. Carrying an existing project's temporary single-scene arrangement into a new project delays necessary design; such arrangements retain only their original scope. Handle rule conflicts under the [rules contract](../../shared/rules.md).

<a id="表达在原设计里"></a>
## Express it in the original design

Simple relationships can go directly in Task/existing design sections. For multi-object relationships, use a composition diagram and necessary lifecycle table, or existing materials serving the same responsibilities. Lasting agreements belong in original Spec/rules, current arrangements in original Task/design; do not create synonymous architecture ledgers or additional Tasks for every submodule.

| Question that needs an answer | What to express | Easily missed counterexample |
|---|---|---|
| Which parts compose the current feature? | Editing/declaration sources, instantiation/assembly entries, actual types and external interfaces; distinguish source modules, saved resources and runtime instances | Mistaking custom names for engine types; listing only directories without showing actual consumers |
| Which state is authoritative? | Who updates/reads configuration, instance state, session state, saves and presentation state respectively | UI reconstruction resets inventory; instances modify shared definitions; global objects duplicate a local view's source of truth |
| Who creates, who ends, and when is reset performed? | Lifetimes for entry, exit, replacement, retry, pooling or asynchronous completion; actually relevant branches | Destroying a cross-level player with a level; registering external callbacks again on every entry |
| How do external dependencies reach consumers? | Explicit references, input data, events and assemblers; identify required dependencies and behavior when unmet | Submodules implicitly search an ancestor path and fail under a different host or second instance |
| How is content edited and observed? | Maintenance entries and available previews for editor resources, code components/factories or data generators | Delivering shell scenes for visual editing while hiding every stable page in one branching script without independent preview |
| What confirms conformance? | Objects and baselines, corresponding observation points for save/instantiation/entry-exit/consumer checks | Calling scene counts proof of modularity; claiming lifecycle correctness from type parsing alone |

Write only applicable information; existing configuration/code can be explicit references without manually copying a second dependency table. Identify which action an unknown affects, and continue investigating facts the model can investigate. Complex diagrams are not required deliverables for every task.

<a id="默认组织与允许替代"></a>
## Default organization and permitted alternatives

This workflow defaults to organizing modules by independent responsibility, editing/reuse needs and lifecycle, so interfaces and state ownership are directly locatable. Projects may use components, pure data models, ECS, code generation or other structures; choices must still meet editing, integration and validation outcomes needed now.

For stable pages, characters or independently adjustable content, prefer suitable engine scene/Prefab/component editing methods. Procedural content supplies locatable generators, inputs and previews/checks appropriate to this use; when code-driven UI is already selected, keep page/component responsibilities, input interfaces and observable paths clear. Do not manufacture empty directories, empty managers or formalistic separation to match default examples.

A single authoritative source for state does not mean putting all state in Main or allowing only one update function in the system. Each state has clear update responsibilities and consistent consumers; presentation state such as temporary selection may be locally owned.

<a id="从设计到实际验收"></a>
## From design to actual acceptance

| Current delivery | Checks needed | Reportable results |
|---|---|---|
| Design only | Composition/lifecycle/dependencies correspond; actual engine facts are checked or explicitly assumptions; required expression and validation arrangements exist | Design complete for this scope, or which design needs investigation; do not report saved scenes or runtime success |
| Implementing/integrating structure | Actual saved/declared sources correspond to runtime objects; necessary dependencies and editing entries are available | Actual file/reference check results and areas still requiring runtime checks |
| Claiming runtime structure conforms | Validate multi-instance, switching, exit/re-entry, pause/input and state retention/reset within applicable scope | Evidence tied to current objects, versions and observation conditions; static success covers only static claims |

Independent modules may be validated in test hosts with explicitly supplied dependencies; every module need not start alone without dependencies. Shared-configuration checks establish intended sharing; instance-isolation checks establish absence of state interference. Visual/gameplay acceptance still uses actual Decisions and is not replaced by structural checks.

Reuse same-baseline evidence; add only affected coverage for new content. When an engine cannot run, retain unverified scope while independently completing design and static checks. Unresolved incorrect ownership blocks implementation/acceptance actions depending on it, without blocking unrelated quick changes.

<a id="来源与采用"></a>
## Sources and adoption

These triggers and expression arrangements are Gamecaden workflow choices based on existing project experience and delivery requirements; official sources in corresponding topics check specific engine facts. When adopting project experience, distinguish effective approaches, failure counterexamples and cost compromises at the time, retaining conditions; a structure's presence in source code does not prove it merits broader adoption.

Project adoption scope, source versions and differences follow the [profiles contract](../README.md). Concrete structural prerequisites needing shared tracking are expressed by their original owners nearby; the panel consumes only defined conditions. This reference does not automatically generate project-wide Gates or another completion-state system.
