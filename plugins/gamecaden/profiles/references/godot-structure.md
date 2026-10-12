<a id="godot-场景节点与状态组织"></a>
# Godot scene, node and state organization

Read this when adding pages/levels, reusable scenes, cross-scene state, or modifying nodes, UI space or editing/save methods. First apply the [shared structure contract](structure-contract.md), checking only relevant topics; technical references use Godot 4.6 documentation, with the project's actual version, language and plugins determining applicable details.

<a id="场景文件与运行树"></a>
## Scene files and runtime tree

**Engine fact**: A scene has one root node and can be saved, loaded and instantiated; multiple scene instances enter the runtime SceneTree. The main scene is the project entry and does not require all code/state to belong to its script or every submodule to have a separate file. [Nodes and scenes](https://docs.godotengine.org/en/4.6/getting_started/step_by_step/nodes_and_scenes.html), [SceneTree](https://docs.godotengine.org/en/4.6/tutorials/scripting/scene_tree.html).

**Workflow default**: Choose scene boundaries by independent editing, lifecycle and reuse needs; script/data modules with clear responsibilities can serve nonvisual responsibilities. Many nodes in one runtime tree do not imply incorrect architecture; splitting files while still depending on undeclared parent details at runtime does not satisfy module boundaries either.

Specify actual types and corresponding scripts for nodes to save. `Main`, `CurrentScreen`, `GameSession`, `WorldRoot`, `Level`, `Actors` and `Systems` are optional responsibility names; `Node`, `Node2D`, `Node3D`, `Control`, etc. are engine types. Reference custom types only when implementation and registration methods exist. `Autoload` is a loading mechanism and `.tscn` a scene format; neither is a node class name.

<a id="触发与检查"></a>
## Triggers and checks

| Applicable issue | Required outcome | Default arrangement and alternatives | Counterexamples and acceptance |
|---|---|---|---|
| New pages/reusable scenes (GODOT-SCENE) | Root types, editing sources, instantiation entries and necessary dependencies are locatable | Independent responsibilities form scenes/components; the relationship-owning context injects data/references; signals express actions that occurred, explicit methods initiate behavior; choose according to project interfaces | Separating Menu.tscn while depending on fixed `../../Main/Inventory`. With actual necessary dependencies supplied, check behavior in another host or a second instance, without making dependency-free F6 startup a universal gate |
| Level/page replacement (GODOT-LIFETIME) | Creation, release and retention/reset match current design | Choose ownership by whether child objects should end when parents are freed; higher-level objects or suitable models may hold lasting state | Cross-level players under levels to be destroyed; moving all state into Main. Actually replace levels/return to pages and confirm which nodes disappear, state retention and absence of duplicate listeners |
| Multiple character/resource instances (GODOT-RESOURCE) | Shared definitions and mutable instance state have explicit relationships | Choose sharing/duplication/instance data under the Resource entry of the [Godot profile](../engines/godot.md); ordinary objects may hold non-node state | Two characters change health in the same configuration. Create two instances and modify one, checking required independent/shared outcomes |
| UI, camera or coordinate changes (GODOT-SPACE/GODOT-INPUT) | Spatial/input relationships among world objects, screen HUD and in-world UI are correct | Choose actual node types, transforms, layout and focus using the following section; target devices determine check scope | Camera movement makes HUD follow the map; transparent masks swallow button/gameplay input. Check actual input paths after camera/size changes, dialogs and pause |
| Editing or saving scenes (GODOT-SAVE-SCENE) | Save scope, node owner, script/resource references and promised editing entries are valid | Stable visual content is editable in scenes by default; procedural content retains generation entries and previews; modify actual production sources | In-memory `add_child()` is visible but absent from target PackedScene; shell scenes have no independent editing/preview method. Reload/instantiate after saving to check key nodes, layout and references |

<a id="归属依赖与保存"></a>
### Ownership, dependencies and saving

**Official best practice** chooses tree structure by relationships between objects: scenes are as self-contained as possible, with necessary external dependencies configured by the relationship-owning context; whether an object should end with its parent is an important basis for parent-child relationships. This supports the default arrangement without requiring one node tree or fixed naming. [Scene organization](https://docs.godotengine.org/en/4.6/tutorials/best_practices/scene_organization.html).

**Engine fact**: Freeing a parent frees its children; `owner` instead expresses which scene packages/saves a node, and the two are not interchangeable. When editor tools or generators create nodes needing persistence, `add_child()` alone does not prove target PackedScene inclusion; configure according to target save scope and read back. This does not require adding all ordinary temporary runtime nodes to persistent scenes. [Node.owner](https://docs.godotengine.org/en/4.6/classes/class_node.html#class-node-property-owner), [PackedScene](https://docs.godotengine.org/en/4.6/classes/class_packedscene.html).

<a id="信号接收者与退出范围"></a>
### Signal receivers and exit scope

GDScript Signal/Callable connections become invalid after their associated receiving objects are actually freed; a persistent EventBus signal alone does not establish leftovers after freeing a page. First check actual Callable/receivers, connection counts and freeing scope; `remove_child()` removes parent-child relationships without freeing nodes, and queued freeing also needs confirmation of completion. When receivers remain persistent or pooled, or logical subscription lifetimes are shorter than object lifetimes, disconnect own connections at actual exit boundaries or adjust actual ownership. [Signal.connect](https://docs.godotengine.org/en/4.6/classes/class_signal.html#class-signal-method-connect), [Node.remove_child](https://docs.godotengine.org/en/4.6/classes/class_node.html#class-node-method-remove-child).

Check actual C# event integration separately: cases such as lambdas capturing variables or custom signals connected with `+=` cannot use the automatic-disconnection judgment above when receivers are freed. Retain and pair removal of own delegates according to the language API; a new lambda does not substitute for original callback identity. [C# signals](https://docs.godotengine.org/en/4.6/tutorials/scripting/c_sharp/c_sharp_signals.html#disconnecting-automatically-when-the-receiver-is-freed). After actual re-entry, also check emission, connection and callback counts to avoid mistaking repeated emission for residual subscriptions.

<a id="世界hud-与布局"></a>
### World, HUD and layout

| Current use | Engine mechanisms and default choice | Actual checks |
|---|---|---|
| 2D/3D worlds and characters | Choose Node2D/Node3D derived types suited to the mechanism; use corresponding physics objects when physics is needed, without guessing types from the `Actor` name | Cameras, coordinates, transforms and collision/navigation consumers match project design |
| Fixed screen HUD/menus | CanvasLayer provides an independent 2D drawing layer; Control handles UI rectangles, anchors and GUI input; choose hierarchy and viewport according to design | HUD stays in required position after camera transforms, with correct focus/mouse filtering and pause strategy |
| In-world UI | Specify followed objects, camera/viewport and coordinate conversion; organize in-world or project targets to an overlay | Position and hit detection match current use after character movement, occlusion or projection changes; do not automatically fix all UI to the screen |
| Automatic UI layout | Use suitable Container subclasses such as VBoxContainer/HBoxContainer/GridContainer, adjusting corresponding layout parameters and child Control size policies | Layout works after content/window-size changes; container-managed layout does not compete with handwritten positioning |

CanvasLayer owns its 2D drawing layer and can serve HUD or backgrounds, without providing automatic layout; see official [CanvasLayer](https://docs.godotengine.org/en/4.6/classes/class_canvaslayer.html), [Control](https://docs.godotengine.org/en/4.6/classes/class_control.html) and [Container](https://docs.godotengine.org/en/4.6/classes/class_container.html) for responsibilities and specific parameters. Drawing order, hierarchy, z_index and input filtering still require checking against actual targets; responsibility separation cannot replace them.

<a id="常驻与本局状态"></a>
### Persistent and current-session state

**Engine fact**: Autoload can keep nodes/scripts alive across ordinary scene changes, retain shared state or manage scene switching; it does not automatically guarantee a logically unique instance. [Autoload](https://docs.godotengine.org/en/4.6/tutorials/scripting/singletons_autoload.html).

**Workflow default**: Explain reasons and reset behavior for services/state requiring cross-scene persistence or global access. State already held by a suitable higher-level object can continue there; utility functions do not require Autoload merely because multiple places call them. Local enemies, page selections and temporary level rules remain within appropriate lifetimes. `GameSession` may be composed from Node, Resource/other objects, but always distinguish definitions from mutable current-session data.

<a id="选择结构的例子"></a>
## Examples of structural choices

**Bounded single-page experiment**: With one page, one local gameplay loop and no cross-page state or reuse needs, one scene plus related scripts may satisfy requirements. If designers need to adjust static UI, supply editable nodes or agreed code-editing/preview methods; being an experiment does not excuse promised editing capabilities.

**2D game retaining a player across levels**: The following shows only nodes and is a Gamecaden example, not a fixed official template; choose names and node types according to actual mechanisms. Main or the project-selected assembler separately creates a SessionState ordinary object at session start, releases/resets it at session end as agreed, and supplies its data/action interfaces to gameplay and UI.

```text
Main (Node, application assembly/switching)
└── ScreenHost (Node)
    └── PlayScreen.tscn (Node)
        ├── World (Node2D)
        │   ├── CurrentLevel (current level scene)
        │   │   └── Level enemies (end with the level)
        │   └── Player.tscn (current design requires retention across levels)
        └── UILayer (CanvasLayer)
            └── HUD.tscn (Control)
                └── Suitable Container subclass for layout
```

Explain SessionState's logical ownership separately from the node tree to avoid treating ordinary data objects as nodes. Retaining Player across level changes does not imply retention when returning to the main menu or ending the session; handle each timing point under session agreements. Only lifecycle or independently editable boundaries need corresponding scenes; no file is mandatory for every line in the diagram.

The official introductory [HUD example](https://docs.godotengine.org/en/4.6/getting_started/first_2d_game/06.heads_up_display.html) shows a separate HUD scene as a composition approach to consider; its node names, UI specifications and tutorial scale are not project gates.

<a id="与工作流交接"></a>
## Workflow handoff

When saving scenes, adding second instances, retaining across levels or changing input/resource integration, first reference `project.godot`, actual scenes, Resource/animation resources, InputMap and script wiring to locate current type, source, parent-child/owner, definition/instance and consumer relationships; do not manually copy the full node tree or resource directory. Readable sources cannot replace future targets: when adding shared, independent, retained or editing relationships, supplement original design with current-to-target differences. Where semantics are insufficient, add relevant relationship explanations or necessary local diagrams/tables, selecting expression under [material references](../../skills/design/references/game-deliverables.md).

When Godot is selected but no project exists, first form necessary initial design and mark native sources as pending creation; planned types, resources and wiring are not saved scenes or runtime results.

design explains applicable composition, lifecycle and dependencies in original design and defines validation observation points; develop/assets implement actual scenes, scripts and resource consumers; verify compares saved composition with affected runtime behavior. Choose cross-instance, level-switching and page exit/re-entry checks according to current claims; original Evidence/Decision records still own results.

Sources checked: 2026-10-01. Technical mechanisms and official best practices are linked above; triggers, default editing methods, examples and acceptance arrangements are this workflow's design. This file is not evidence of completed structural validation in an actual project.
