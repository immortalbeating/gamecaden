<a id="phaser-框架-profile"></a>
# Phaser framework profile

<a id="触发与版本边界"></a>
## Triggers and version boundaries

Use this when the actual game runtime root loads Phaser, or the current new-project design explicitly selects Phaser. Express design choices separately from actual installation facts. First confirm the project's exact installed/referenced version and plugins; specific lifecycle documentation in this round was checked against Phaser 3.x official documentation. Existing Web projects may use 4.x, so do not treat every Phaser project as 3.x; recheck specific APIs, lifecycles and rendering behavior for 2, 4 or other major versions against installed versions and official documentation. Browser targets also read the [Web platform profile](../platforms/web.md), but Godot/Unity Web exports do not trigger Phaser. Do not apply this page when the project has neither adopted nor selected Phaser.

<a id="需现场识别的工程事实"></a>
## Engineering facts to identify in the project

- Phaser version, startup configuration, Scene registration, global/Scene-level plugins and actual runtime entry.
- Affected Scene keys, enter/stop/sleep/wake relationships, and owners of cross-Scene state.
- Asset loader keys, Texture Manager entries, atlas frame names, animation keys and consumers that actually create them.
- Whether input comes from Scene Input Plugin, global Game/DOM, UI overlays or custom buses; who creates/releases listeners.

<a id="条件规则"></a>
## Conditional rules

Rule nature follows [rules](../../shared/rules.md). Scene operations and cleanup mechanisms in this table are the 3.x checking baseline; recheck differences for other major versions before choosing implementation actions. Individual projects' simulation/presentation separation, test counts and resource dimensions retain original scope.

| ID | Nature and trigger | Requirement or default approach | Observable validation |
|---|---|---|---|
| PHASER-ENTRY | Required: identifying a Phaser root or changing startup | Confirm runtime roots with actual dependencies, Game configuration and Scene registration; identify co-located HTML tools separately. | Start from current entry and enter target Scene, checking actual version and resource requests. |
| PHASER-SCENE-LIFE | Required: Scene switching, re-entry or destruction | Specify lifecycle semantics of the version used; in 3.x, `shutdown` permits restart, `destroy` finally removes, and `start/stop`, `sleep/wake`, `pause/resume` determine retention/reset. | Repeatedly enter, leave and return to target Scene; state and object counts match design. |
| PHASER-SUBSCRIBE | Required: Scene creates cross-lifecycle listeners | Distinguish Scene-plugin-managed listeners from those registered to `game.events`, DOM or external buses; creators remove the latter at appropriate lifecycle points to avoid duplicate subscriptions. | After Scene re-entry, one event produces expected effects only; no residual callbacks after exit. |
| PHASER-STATE | Required: multiple Scenes read/write the same gameplay state | Specify cross-Scene state owners and reset timing; Registry, independent models or other existing modules are valid, while local Scene Data does not automatically become a global source of truth. | Every consumer reads expected state on switching, restart and refresh, without divergent double writes. |
| PHASER-KEYS | Required: loading/replacing textures, atlases or animations | Keep loader keys, atlas frames and animation keys consistent with creation/playback consumers; global cache/Texture Manager lifecycles differ from individual Scene objects. | Target frames in actual Scenes display/play correctly; missing keys/wrong frames are locatable. |
| PHASER-COORD | Required: collision, pointer or visual-size changes | Connect logical targets and Phaser objects using established project coordinates, display origins, cameras and scaling; browser sizes/input also follow Web profile. | Visible positions, interaction hits and collision areas agree at target resolutions. |
| PHASER-CLOCK | Default: rule updates and presentation time interact | Confirm how `update(time, delta)`, Scene pause/sleep and project simulation clocks affect rules, animation and sound; specify division only when risk warrants it. | Results follow rules after pause, resume, frame-rate changes or background return. |
| PHASER-ASSET-HANDOFF | Required: formal asset integration | Wire current candidates, key/frame, actual Scene consumers and permitted uses; successful image loading is only one segment of integration. | Observe display, animation and related input/collision through trigger paths in actual Scenes. |

<a id="身份与目录机制"></a>
## Identity and directory mechanisms

Scene Manager addresses Phaser Scenes by keys; texture, cache and animation managers may serve multiple Scenes, while Scene objects/plugins have their own lifecycles. Recording "who holds keys/state, who creates listeners, when release occurs" matters more than prescribing directories such as `src/scenes/`. For new systems/Scene composition or changes to cross-Scene state, listeners, UI/camera/DOM or resource-consumer boundaries, read applicable sections of the [Phaser structure topic](../references/phaser-structure.md). Specific structure follows [project structure](../project-structure.md) and effective project agreements; [common boundaries](../common.md) owns common responsibilities, without repetition here. Remove own external callbacks precisely, without clearing shared emitters without arguments.

<a id="与-skill-阶段交接"></a>
## Handoff to Skill stages

- `flow/init`: Confirm dependencies, runtime roots and effective project rules; adopting a profile does not remodel existing Scene architecture.
- `design`: When new systems, cross-Scene state, Scene round trips, UI/camera/DOM or resource wiring affect plans, read corresponding sections of the [Phaser structure topic](../references/phaser-structure.md), specifying owners, keys, reset and observable paths.
- `develop/assets`: For structural quick changes, read only applicable [Phaser structure topic](../references/phaser-structure.md) entries and wire actual Scene consumers; see [asset handoff](../../shared/asset-handoff.md) for asset candidates, acceptance, selection and integration.
- `verify/close`: Reuse original Task/Evidence/Decision under the [verification contract](../../shared/verification.md); supplement only Scene cycles, resource or input checks touched by changes.

<a id="官网依据与未验证范围"></a>
## Official basis and unverified scope

- Phaser official: [Scenes](https://docs.phaser.io/phaser/concepts/scenes) (lifecycle, Scene/global systems), [Events](https://docs.phaser.io/phaser/concepts/events) (listener ownership and precise removal), [Data Manager](https://docs.phaser.io/phaser/concepts/data-manager) (Scene/Game data scopes).
- An existing project encountered a Text first-render crash under a specific version and call path; such experience is only an investigation lead requiring reproduction in this project, not a defect generalized to all major versions.
- This page uses Phaser 3.x documentation and existing Web project experience; declared version scope does not mean locked installed versions, plugins or API behavior were checked; actual adoption requires project-specific verification. Directory/state ownership are conditional workflow judgments, not official mandatory architecture.
