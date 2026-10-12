<a id="phaser-结构scene模块状态与-ui"></a>
# Phaser structure: Scene, modules, state and UI

<a id="何时读取"></a>
## When to read

When creating Phaser systems, adjusting Scene composition/round trips, state ownership, external listeners, UI/camera/DOM boundaries or resource-key consumers, read applicable sections. Quick changes load only affected entries and acceptance checks. Follow PHASER-SCENE-LIFE, PHASER-SUBSCRIBE, PHASER-STATE, PHASER-KEYS and PHASER-COORD in the [Phaser profile](../frameworks/phaser.md); this page adds no synonymous Gates.

The [structure contract](structure-contract.md) owns common triggers, record ownership in existing design/Spec, adoption boundaries for new/existing projects and design/runtime acceptance. This page adds only relevant engine mechanisms and candidate approaches.

<a id="引擎事实与工作流选择"></a>
## Engine facts and workflow choices

Mechanisms reference checked Phaser 3.x (3.90.0 available through Context7). First read actual package, lockfile/installed version, plugins and entry; check 4.x or other major versions against locked/local versions before adopting specific APIs; declared scope does not replace installation facts. Official facts: Scene is an engine runtime scope with local systems and lifecycle; Game has global systems; ordinary JS/TS objects, classes and modules may hold game rules without automatically receiving Scene lifecycle. Defaults below belong to this workflow; Phaser does not mandate business layering for every game.

| Required outcome and trigger | Workflow default / permitted alternatives | Common counterexamples | Observable acceptance |
|---|---|---|---|
| New systems have explicit entry, update, exit and reuse scopes | Scene handles engine wiring, creation and coordination for its runtime scope; ordinary object/class modules hold rules, data or reusable behavior. Simple rules may stay in Scene; independent modules have explicit initialization/update/release interfaces. | Every rule class made into a Scene; all business state in a giant Scene; ordinary objects assumed to clean up automatically with Scene. | Consumers and module entries can be located from Scene; independent units can be created/exited; changes affect corresponding responsibilities only. |
| Cross-Scene state has one authoritative source | Choose existing models, Game Registry or explicit global modules by session/application/save lifetimes; Scene Data serves Scene-scoped data. Intentional sharing or passed snapshots are allowed, with writers, reset and synchronization specified. | HUD and gameplay Scenes each maintaining score; assuming Scene Data is automatically globally shared; assuming stop restores every JS field to initial values. | Values after Scene round trips, restart, new sessions and refresh each match design; all consumers observe the same change. |
| Scene re-entry or external-listener changes remain safe for repeated entry | Distinguish local Scene plugin cleanup from game.events, DOM, external buses, native timers/asynchronous callbacks; creators remove own callbacks at appropriate shutdown/destroy or custom release boundaries, with asynchronous results checking whether their runtime remains valid. | Adding external listeners every create but cleaning only at final destroy; clearing shared emitters without arguments; departed Promises writing old UI. | Enter → leave → return, repeating as necessary by risk; events trigger only expected counts, old-object callbacks do not remain after exit, subscriptions/objects do not accumulate. |
| Coordinates, input and pause scopes are clear for UI or concurrently running Scenes | Use fixed UI in the same Scene, parallel UI Scenes, separate cameras or DOM; choose the smallest arrangement by gameplay/UI lifetimes and established layout. Parallel Scenes specify stacking/input ownership, cameras specify rendered objects/coordinate conversion, DOM specifies host/configuration/focus. | Expecting same-Scene UI to keep updating after gameplay Scene pause; multiple Scenes responding to one intent; camera movement drifting HUD; canvas responding incorrectly beneath DOM overlays. | Display, hits, focus and pause scope match design during camera movement/zoom, pause/resume, resizing and UI toggling. |
| Visual transforms and layout rules remain distinguishable after hierarchy/layout changes | Container composes child-object transforms; explicit calculations, project layout tools or suitable DOM/CSS provide layout. Direct positioning of a few fixed controls is allowed. | Treating Container as Godot Control automatic layout; expecting automatic anchors/responsiveness after adding children; container visual positions not checked against physics/input coordinates. | After container transforms and target-size changes, check child positions, hits/collisions and layout; relayout triggers and sources can be located. |
| Key-to-consumer chains remain stable after resource replacement/re-entry | Check loader keys, Texture/cache, atlas frames, Animation keys and actual creation/playback points; reuse global resources and reconnect rebuilt Scene objects. Locate active consumers before replacing/deleting shared entries. | Recreating same-name global animations every create; overwriting textures used by another Scene with the same key; checking only successful requests. | Correct frames display/play from target entries and re-entry paths; shared consumers remain valid, without duplicate definitions or missing-key errors. |

<a id="scene-生命周期与系统范围"></a>
### Scene lifecycle and system scopes

In 3.x, Scene start/stop, pause/resume, sleep/wake and remove/destroy have different semantics: Scenes can restart after shutdown, while destroy is final removal; pause/sleep are not uniform resets either. Check combinations against local versions first. Game Texture, Cache, Animation, Registry, etc. have different lifetimes from Scene display lists, cameras, input and clocks; removing objects from Scene does not establish release of global resources or external subscriptions. Explicitly handle objects needing rebinding on each entry and state initialized each session; ordinary Scene-instance fields especially cannot rely on constructors running again.

<a id="ui-方案的约束"></a>
### Constraints on UI approaches

A small fixed HUD in the same Scene can use suitable scroll factors/camera arrangements, checking zoom and input coordinates. Parallel UI Scenes may have different pause lifetimes from gameplay; they exchange intent/display data through existing model/message interfaces. Multiple cameras must specify which objects each displays/ignores and which camera pointers use. DOM approaches first check game DOM container configuration, CSS, focus, scaling and official limits; official 3.x DOM Element documentation requires its Scene to use one camera and notes that elements across Scenes enter the same DOM container; parallel Scenes may address multi-camera needs, still subject to local-version checks. Container hierarchy transforms do not provide Godot-style automatic layout contracts; layout sources must be locatable in code or chosen tools.

<a id="候选例子"></a>
## Candidate examples

The following illustrate this approach only, are unrun, and are not official standard templates.

**Simple scene: clicking a target adds score.** Existing design is one single-screen session. One Scene creates targets and fixed score text; Scene-local state can hold session score, with an ordinary module added when pure scoring rules need reuse. Check the target texture key through preload-to-create consumer chains. Acceptance uses one actual click, consecutive clicks and restart, observing score counts, resource frames and reset; do not first create global services for this requirement.

**Cross-scene: gameplay, pause UI and results.** Existing Spec requires operable UI during pause and results retaining session score. Use `gameplay Scene → current-session model ← parallel UI Scene / results Scene`; model lifetime covers results, UI sends pause/resume intents and a coordinator performs corresponding Scene operations. UI exit cleans its own model/DOM/global listeners; new sessions explicitly reset the model; gameplay re-entry rebuilds objects and reuses validated resource keys. Acceptance follows gameplay → pause → resume → results → new session for two rounds, also checking camera/pointer, event counts and shared animation/texture consumers.

<a id="输入来源与工作流交接"></a>
## Input sources and workflow handoff

When Scene re-entry, pause UI, external listeners or atlas replacement changes, reference Scene registration/code, existing state models, loader/atlas/animation configuration and actual creation/playback points to locate composition, state/input lifetimes, listener ownership and key/frame-to-consumer relationships; do not maintain complete Scene-object catalogs or manually mirrored key tables. Use existing sources directly when they answer current questions; add differences to original design for future composition, sharing or exit changes even when source is readable. If semantics are insufficient, form necessary local state/timing or consumer-relationship expressions, selecting methods under [material references](../../skills/design/references/game-deliverables.md).

When Phaser is selected but no project exists, first form necessary initial design and mark registration/resource sources as pending creation; planned configuration does not represent loading/runtime success. Browser common inputs use [Web handoff](../platforms/web.md#handoff-to-skill-stages). develop implements wiring from sources; verify checks current entry/exit and resource consumers, with results in original Evidence/Decision records.

<a id="官方事实来源与验证边界"></a>
## Official factual sources and validation boundaries

- [Scenes](https://docs.phaser.io/phaser/concepts/scenes), [Scene events](https://docs.phaser.io/api-documentation/namespace/scenes-events): Scene/Game systems, parallel operation and lifecycle.
- [Data Manager](https://docs.phaser.io/phaser/concepts/data-manager), [Events](https://docs.phaser.io/phaser/concepts/events): data scopes, subscriptions and precise removal.
- [Container](https://docs.phaser.io/phaser/concepts/gameobjects/container), [Cameras](https://docs.phaser.io/phaser/concepts/cameras), [DOM Element](https://docs.phaser.io/phaser/concepts/gameobjects/dom-element): composition transforms, cameras and DOM conditions/limits.
- [Textures](https://docs.phaser.io/phaser/concepts/textures), [Animations](https://docs.phaser.io/phaser/concepts/animations): global resources and key consumption. Official concept sites may change; check local major/locked versions before API adoption.

This round checked only documentation and links; it did not start Phaser/browser games, check any actual project's locked version or run examples. Validation records follow [verification](../../shared/verification.md), recording source checks separately from actual runtime/human acceptance.
