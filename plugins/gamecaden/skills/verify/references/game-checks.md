<a id="按游戏主张选择检查"></a>
# Choose checks by game claims

Current requirements and actual impact determine which parts to read. These are coverage directions, not full checklists for every task; engine commands and parameters come from current projects, applicable profiles and available specialized capabilities.

<a id="1-不同证据证明不同事情"></a>
## 1. Different evidence proves different things

| Result to judge | Corresponding evidence and common gaps |
|---|---|
| Documents, design or content packages fulfill their own delivery | Check committed information, files, references and consistency; do not automatically add future game-runtime obligations |
| Code/configuration parses/compiles and resources import | Actual command results and target versions; does not directly prove runtime scenes or player paths |
| State/rules are correct | Behavioral checks through real interfaces covering relevant order, failure and recovery; substitutes do not replace key boundaries this work proves |
| Gameplay configuration drives the claimed behavior | Follow the adopted [data-maintenance source](../../../profiles/common.md#data-maintenance) through actual loading and consumption; use relevant parameter/compatible-variant changes to distinguish old and new behavior. Select missing/invalid field or reference checks and shared-definition/instance-isolation observations by actual impact; reuse existing checks. Configuration existence or a successful parse establishes only those facts. |
| Engineering structure meets current agreements | Compare actual saved/declared sources, real types, assembly dependencies and authoritative state; check multiple instances, switching, exit/re-entry and editing/preview by impact. Design diagrams, parsing passes or scene counts do not directly prove correct runtime ownership |
| Levels/mechanics function normally | Enter target processes through normal inputs; check collision, navigation, events and return. Teleporting to endpoints does not prove natural reachability |
| UI operates and displays correctly | Actual pages and relevant focus, return, pause, expansion/occlusion, dimensions or input modes; use [family verification](../../../shared/ui-families.md#change-and-verify) for shared/variant claims and affected consumers. Static screenshots do not replace interaction paths |
| Assets are actually used | Specific consumers, resource identities/versions, triggering and visible/audible results; copying, loading or master-ledger selection alone does not prove actual presentation |
| Saves/migration are reliable | Old-version reading, changes, saving, reloading and relevant interruption/repetition with isolated data; memory values alone are insufficient |
| Performance meets targets | Specified scale, scenes, hardware/platforms, measurement methods and actual results; small smoke tests do not prove target scale |
| A target platform is deliverable | Corresponding builds, dependencies and necessary external runtime checks of that artifact; editor passes do not equal export/device passes |
| Experience/style receives required acceptance | Actual acceptance records for corresponding versions/aspects; retain technical passes and model impressions separately |

<a id="2-选择真实目标"></a>
## 2. Select actual targets

Use current-project check/runtime methods for each engine/framework and actual target separately. Check engineering targets, entry scenes/pages, builds and configuration; reachable bridges, old processes or existing screenshots do not replace instance confirmation. Report previews and actual delivery entrypoints separately; check mechanics, player paths and experience against commitments. Rendering or Scene names do not replace actual runtime roots.

When engineering/platform mechanisms affect conclusions, read matching verification items through [Profiles](../../../profiles/README.md), then adopted project rules/versions. Observable profile checks support method selection; they are not mandatory full test suites for every Task.

For structure changes, read [Common acceptance boundaries](../../../profiles/references/structure-contract.md), then select engine-topic observations exposing wrong ownership, leaked state, duplicate listeners, unsaved or uneditable content. Design-only deliveries check information/arrangements; implemented/runtime claims need actual engineering evidence. Independent modules may be verified in test hosts supplying real necessary dependencies; not every component must start alone without dependencies.

Verify games and tools in the same repository separately. For example, an HTML approval panel checks selection, version binding, writeback and withdrawal semantics; add game integration coverage only when it actually modifies game consumers.

Limit conclusions for missing devices/platforms/tools. Complete independent static/other-platform parts as appropriate, but do not treat them as replacement passes for missing platforms.

<a id="3-避免验证绕过要证明的行为"></a>
## 3. Avoid bypassing behavior under proof

State injection, skipping tutorials, calling internal functions directly or substitute services can locate local problems; claims involving actual inputs, persistence, consumer wiring or external boundaries still need corresponding actual paths.

Screenshots, recordings, videos and logs must correspond to current objects, runtime conditions and observation points. Reference images guide targets but are not current runtime evidence; screenshots cannot prove subsequent interactions absent from them.

Check precise properties for deterministic outputs; visual/audio quality uses suitable observation or explicit acceptance. Without established metrics, explain observation grounds and limits instead of inventing score thresholds as general gates.

<a id="4-处理测试与现行要求的冲突"></a>
## 4. Handle conflicts between tests and current requirements

For failures, distinguish implementation issues, environment faults and whether tests express effective requirements. An old validator requiring “exactly N files” with a current contract allowing extension should be reassessed by actual necessary items and consumers; do not delete valid content for old counts.

When updating outdated tests, save grounds and new coverage without silently weakening verified requirements. For substantive ambiguity in requirements themselves, hand concrete tradeoffs to corresponding design/users; validators cannot decide product scope.
