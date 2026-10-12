<a id="godot-工程-profile"></a>
# Godot engineering profile

Trigger: The actual runtime root for this work uses Godot, or a new project design explicitly selects Godot. A selected but not yet established project can use this to form a plan; runtime capabilities remain to be confirmed. First locate existing `project.godot`, entry scene, actual editor version, rendering mode, script language, plugins and target platform; reuse existing mappings. If Godot files merely coexist in the repository while this change affects only a standalone tool, select rules for that tool.

The official documentation baseline checked in this round is Godot 4.6; this does not require projects to upgrade to it. Verify specific 4.x patches, 3.x, C#/.NET and export-platform capabilities against this project's configuration and corresponding official documentation; do not claim compatibility for unchecked areas.

<a id="场景与状态"></a>
## Scenes and state

| ID | Trigger | Requirement or default approach | Observable checks |
|---|---|---|---|
| GODOT-SCENE | Changes to page/level switching, reusable units or independent lifecycles | **Required**: State ownership, entries, external dependencies and communication interfaces are identifiable; **default**: compose scenes/sub-scenes and scripts with clear responsibilities, with dependencies configured by the party that owns the relationship. A separate View does not prove all state has been reasonably separated. | Repeated instances/re-entry work; sub-scenes do not depend on undeclared ancestor paths; this routing and local state each have clear maintainers. |
| GODOT-RESOURCE | Multiple instances reference and modify the same Resource | **Required**: Distinguish shared definitions from mutable instance state; choose sharing, instance data or applicable duplication/scene localization according to intent. | After changing one instance, others behave according to the sharing agreement; check nested resource references rather than assuming top-level duplication isolates all data. |
| GODOT-SAVE-SCENE | Generating/modifying nodes and resources that must be saved as a PackedScene | **Required**: Save scope, node owner and persistent references match the actual target. Do not default to writing every temporary runtime node into the scene. | After saving, read/instantiate the target scene again: key nodes, scripts and resources remain; correct in-memory display does not mean persistence is complete. |
| GODOT-LIFETIME | Changes to scene switching, pause, node freeing, pooling or asynchronous callbacks | **Required**: Distinguish tree lifetime, rule state, global services and this work's external subscriptions; use enter/exit/process semantics of the actual version. | Restart/exit does not cause duplicate processing, references to invalid objects or leftover input; data that must persist remains correct across switches. |

Scene separation follows responsibilities and dependencies; a simple bounded experiment can start in one scene. When adding independent pages, reusable units or complex persistent state, design appropriate boundaries before expanding further. A text-only quick change does not trigger comprehensive refactoring. [Scene organization basis](https://docs.godotengine.org/en/4.6/tutorials/best_practices/scene_organization.html)

For these changes, and changes to how nodes/UI are edited and saved, read the [scenes, nodes and state topic](../references/godot-structure.md). It turns GODOT-SCENE, GODOT-LIFETIME, GODOT-SAVE-SCENE and GODOT-SPACE/INPUT requirements into composition, actual types, ownership, interfaces and observable acceptance, distinguishing custom responsibility names, engine types, Autoload and scene formats.

Resource `resource_local_to_scene` applies during scene instantiation; changing the flag at runtime does not retroactively isolate existing instances. Check specific duplication semantics against the actual resource type and version. [Resource basis](https://docs.godotengine.org/en/4.6/classes/class_resource.html); see [PackedScene](https://docs.godotengine.org/en/4.6/classes/class_packedscene.html) for persistent scene save scope.

<a id="输入空间与运行"></a>
## Input, space and runtime

| ID | Trigger | Requirement or default approach | Observable checks |
|---|---|---|---|
| GODOT-SPACE | Changes to character scale, collision/navigation, maps, cameras or projection | **Required**: Coordinate relationships, transform inheritance and spatial data of Node2D/Node3D/Control match the current design. Choose physics and display processing according to actual mechanisms. | Actual input follows the entry/path/interaction, is readable through the target camera, and has correct collision/navigation; after changing sprite scale, check related anchors and spatial bounds. |
| GODOT-INPUT | Changes to input routing, UI focus, pause or input devices | **Required**: Retain/adjust the actual InputMap and event consumers; explain GUI/gameplay input relationships and which objects continue processing during pause. | Follow start, return, pause/resume and key operations covered by this commitment; UI does not unexpectedly swallow or duplicate gameplay actions. |
| GODOT-IMPORT | Changes to new resources, import settings, plugins, script types or project structure | **Required**: Check the current project, engine/plugin versions and first root error; confirm resources, paths/UIDs, case and loading relationships through the actual import flow. | Record import/parsing/startup results separately; trace cascading errors to their root cause; an old process, port response or existing screenshot does not prove this project has run. |
| GODOT-EXPORT | Target-platform delivery, export settings or version compatibility is part of this commitment | **Required**: Check actual export configuration, required templates and toolchain; validate outputs using matching-version capabilities. | State coverage separately for import, editor/headless checks, export and external launch; local editor success does not automatically establish target-platform delivery. |

[SceneTree](https://docs.godotengine.org/en/4.6/tutorials/scripting/scene_tree.html) provides the technical basis for nodes entering/leaving the tree and processing scope; this project owns specific restart, save and pause rules. Runtime checks use applicable [common](../common.md) entries and [verification](../../shared/verification.md), without another Godot task-state ledger.

<a id="目录身份与工具"></a>
## Directories, identity and tools

Godot organizes content through the actual filesystem; scenes, scripts and resources may be grouped by feature. Default folder-name suggestions are not grounds for repository-wide renaming. Before excluding production sources or workflow materials from import, confirm they have no runtime consumers, then use `.gdignore` supported by the actual version. Do not exclude resource directories still read by the project. [Project organization](https://docs.godotengine.org/en/4.6/tutorials/best_practices/project_organization.html)

Distinguish source assets and identity/import configuration that carries reference meaning from rebuildable `.godot/` caches; maintain existing UIDs and resource references according to the actual engine version. Follow project conventions for Git file policy; this profile does not authorize deleting caches/history or replacing version-control configuration. [Version-control reference](https://docs.godotengine.org/en/4.6/tutorials/best_practices/version_control_systems.html)

design forms responsibility/input arrangements; develop/assets implement scenes, resources and consumers; verify/close read corresponding results. Use the actually available editor, CLI or MCP, following specialist Skills for connections and operations; when a tool is unavailable, state which operation it affects and continue independent analysis or editing. MCP callability alone does not establish connection to the correct project.

<a id="来源与范围"></a>
## Sources and scope

Technical constraints refer to the Godot 4.6 official pages above and [export documentation](https://docs.godotengine.org/en/4.6/tutorials/export/exporting_projects.html), checked on 2026-09-27. Directory arrangements, responsibility boundaries and validation intensity are selection rules of this workflow; official documentation does not require one structure for every project. This round did not run Godot or validate actual project exports.
