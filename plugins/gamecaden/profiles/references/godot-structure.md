# Godot 场景、节点与状态组织

新增页面/关卡、可复用场景、跨场景状态，或修改节点、UI 空间、编辑/保存方式时读取。先应用 [结构共同约定](structure-contract.md)，只核对命中的专题；技术参考使用 Godot 4.6 文档，项目实际版本、语言和插件决定适用细节。

## 场景文件与运行树

**引擎事实**：场景具有一个根节点，可以保存、加载和实例化；多个场景实例进入运行时 SceneTree。主场景是项目入口，不规定所有代码和状态必须归其脚本，也不要求每个子模块都有单独文件。[节点与场景](https://docs.godotengine.org/en/4.6/getting_started/step_by_step/nodes_and_scenes.html)、[SceneTree](https://docs.godotengine.org/en/4.6/tutorials/scripting/scene_tree.html)。

**本工作流默认**：按独立编辑、生命周期和复用需求选择场景边界，职责清楚的脚本/数据模块也可承担非可视职责。一个运行树包含许多节点并不表示架构错误；只把文件拆开、运行时仍依赖未声明的上层细节，也不算满足模块边界。

需要保存的节点明确真实类型及对应脚本。`Main`、`CurrentScreen`、`GameSession`、`WorldRoot`、`Level`、`Actors`、`Systems` 都是可选职责名称；`Node`、`Node2D`、`Node3D`、`Control` 等才是引擎类型。自定义类型只有已有实现与注册方式时才引用。`Autoload` 是加载机制，`.tscn` 是场景格式，不能当节点类名。

## 触发与检查

| 命中问题 | 必须满足的结果 | 默认安排与可选方法 | 反例与验收 |
|---|---|---|---|
| 新页面/复用场景（GODOT-SCENE） | 根类型、编辑来源、实例化入口和必要依赖可定位 | 独立职责形成场景/组件，由拥有关系的上下文注入数据/引用；信号表达发生的动作，明确方法发起行为；按项目接口选择 | 分出 Menu.tscn 却依赖固定的 `../../Main/Inventory`。给定真实所需依赖后在另一个宿主或第二实例中核对行为，不以 F6 无依赖启动作为普遍门禁 |
| 关卡/页面替换（GODOT-LIFETIME） | 创建、释放、保留/重置关系与当前设计一致 | 根据父节点释放时子对象是否也应释放选归属；长期状态可由上层对象或合适模型持有 | 跨关卡玩家挂在待销毁关卡下；把全部状态移到 Main。实际替换关卡/返回页面，确认哪些节点消失、状态保留、监听不重复 |
| 角色/资源多实例（GODOT-RESOURCE） | 共享定义与实例可变状态有明确关系 | 按 [Godot profile](../engines/godot.md)的 Resource 条目选择共享/复制/实例数据；非节点状态可以由普通对象持有 | 两个角色改同一份配置的血量。创建两个实例并修改其中一个，核对设计要求的独立/共享结果 |
| UI、相机或坐标变化（GODOT-SPACE／GODOT-INPUT） | 世界对象、屏幕 HUD、世界内 UI 的空间/输入关系正确 | 按下节选择实际节点类型、变换、布局和焦点；目标设备决定检查范围 | 相机移动使 HUD 跟随地图；透明遮罩吞掉按钮或玩法输入。核对相机、尺寸变化、弹窗与暂停后的实际输入路径 |
| 编辑或保存场景（GODOT-SAVE-SCENE） | 保存范围、节点 owner、脚本/资源引用和承诺的编辑入口成立 | 稳定可视内容默认可在场景中调整；程序化内容保留生成入口与预览；修改实际制作源 | 内存里 `add_child()` 可见却未保存在目标 PackedScene；场景是空壳且无独立编辑/预览方法。保存后重新加载/实例化，核对关键节点、布局与引用 |

### 归属、依赖与保存

**官方最佳实践**以对象之间的关系选择树结构：场景尽可能自足，必要的外部依赖由拥有关系的上下文配置；是否随父对象结束，是父子关系的重要判断依据。这支持默认方案，不构成唯一节点树或固定命名要求。[Scene organization](https://docs.godotengine.org/en/4.6/tutorials/best_practices/scene_organization.html)。

**引擎事实**：释放父节点会释放其子节点；`owner` 则表达随哪个场景打包保存的关系，二者不能互换。编辑器工具或生成器创建需持久化的节点时，仅 `add_child()` 不足以证明目标 PackedScene 会包含它们；按目标保存范围设置并重新读回。普通运行时临时节点不因此全部加入持久场景。[Node.owner](https://docs.godotengine.org/en/4.6/classes/class_node.html#class-node-property-owner)、[PackedScene](https://docs.godotengine.org/en/4.6/classes/class_packedscene.html)。

### 信号接收者与退出范围

GDScript 的 Signal/Callable 连接在所关联的接收对象真正释放后会失效；不能仅凭信号来自常驻 EventBus，就认定释放页面后一定残留。先核对真实 Callable/接收者、连接次数和释放范围；`remove_child()` 只移出父子关系，不释放节点，排队释放也需确认实际完成。接收者仍常驻、被池化保留或逻辑订阅寿命短于对象寿命时，按真实退出边界解除自己的连接，或调整实际所有者。[Signal.connect](https://docs.godotengine.org/en/4.6/classes/class_signal.html#class-signal-method-connect)、[Node.remove_child](https://docs.godotengine.org/en/4.6/classes/class_node.html#class-node-method-remove-child)。

C# 的事件接入另核对实际方式：接收者释放时，捕获变量的 lambda 或使用 `+=` 接入自定义信号等情况不能套用上述自动断连判断。按语言 API 保留并配对解除自己的委托；不要以新建一个 lambda 代替原回调身份。[C# signals](https://docs.godotengine.org/en/4.6/tutorials/scripting/c_sharp/c_sharp_signals.html#disconnecting-automatically-when-the-receiver-is-freed)。实际重进后还需核对发出次数、连接与回调次数，避免把重复发出误判为残留订阅。

### 世界、HUD 与布局

| 本次用途 | 引擎机制与默认选择 | 实际核对 |
|---|---|---|
| 2D/3D 世界与角色 | 选择符合机制的 Node2D/Node3D 派生类型；需要物理能力时再用相应物理对象，不按 `Actor` 名称猜类型 | 相机、坐标、变换与碰撞/导航消费者符合项目设计 |
| 固定屏幕 HUD/菜单 | CanvasLayer 可提供独立二维绘制层；Control 承担 UI 矩形、锚点与 GUI 输入；层级与视口按设计选取 | 相机变换后 HUD 仍在要求的位置，焦点/鼠标过滤与暂停策略正确 |
| 世界内 UI | 明确其跟随对象、相机/视口和坐标转换；可在世界中组织，也可将目标投影到覆盖层 | 角色移动、遮挡或投影变化后位置与命中符合本次用途，不把一切 UI 自动固定到屏幕 |
| UI 自动布局 | 使用 VBoxContainer/HBoxContainer/GridContainer 等适合的 Container 子类，调整对应布局参数与子 Control 的尺寸策略 | 改变内容或窗口尺寸后布局成立；受容器管理的布局不与手写位置相互争抢 |

CanvasLayer 负责其二维绘制层，可用于 HUD 或背景，不负责自动布局；Control 与 Container 的职责和具体参数见官方 [CanvasLayer](https://docs.godotengine.org/en/4.6/classes/class_canvaslayer.html)、[Control](https://docs.godotengine.org/en/4.6/classes/class_control.html)、[Container](https://docs.godotengine.org/en/4.6/classes/class_container.html)。绘制顺序、层级、z_index 和输入过滤仍须按实际目标核对，职责拆分不能代替它们。

### 常驻与本局状态

**引擎事实**：Autoload 可使节点/脚本在普通场景切换间常驻，可保存共享状态或处理场景切换；它并不自动保证逻辑上的唯一实例。[Autoload](https://docs.godotengine.org/en/4.6/tutorials/scripting/singletons_autoload.html)。

**本工作流默认**：对需要跨场景常驻或全局访问的服务/状态说明理由与重置行为。已由适当上层对象持有的状态可以继续使用；工具函数不因可被多处调用就需要 Autoload。局部敌人、页面选中项和本关临时规则留在其合理存活范围。`GameSession` 可由 Node、Resource/其他对象组合实现，但始终区分定义与本局可变数据。

## 选择结构的例子

**有界单页试验**：只有一页、一个局部玩法循环，无跨页面状态或复用需求时，一个场景加相关脚本可以满足要求。若要给设计者调整静态 UI，就提供可编辑节点或已约定的代码编辑与预览途径；不能因是试验而忽略已经承诺的编辑能力。

**需要跨关卡保留玩家的 2D 游戏**：下面只画节点，是 Gamecaden 示例，不是官方固定模板；名称和节点类型按实际机制选择。另由 Main 或项目选定的装配者在局开始时创建 SessionState 普通对象，局结束按约定释放/重置；向玩法与 UI 提供其数据/动作接口。

```text
Main (Node，应用装配/切换)
└── ScreenHost (Node)
    └── PlayScreen.tscn (Node)
        ├── World (Node2D)
        │   ├── CurrentLevel (当前关卡场景)
        │   │   └── 本关敌人（随关卡结束）
        │   └── Player.tscn（当前设计要求跨关卡保留）
        └── UILayer (CanvasLayer)
            └── HUD.tscn (Control)
                └── 适合布局的 Container 子类
```

SessionState 的逻辑持有关系与节点树分别说明，避免将普通数据对象误当节点。关卡切换保留 Player，不代表返回主菜单或结束本局也要保留；各时机按本局约定处理。只有生命周期或可独立编辑的边界需要对应场景，不为图中每一行强制创建文件。

官方入门 [HUD 示例](https://docs.godotengine.org/en/4.6/getting_started/first_2d_game/06.heads_up_display.html)展示独立 HUD 场景，是可参考的组成方法；其节点名、UI 规格与教程规模不成为项目门禁。

## 与工作流交接

design 在原设计中说明命中的组成、生命周期与依赖，并定义验证观察点；develop/assets 落实真实场景、脚本和资源消费者；verify 对照保存后的组成与受影响的运行行为。跨实例、切关卡、页面退出/重进等检查按本次主张选择，记录仍归原 Evidence/Decision。

来源核对日期：2026-10-01。技术机制和官方最佳实践见上述链接；触发条件、默认编辑方式、示例与验收安排属于本工作流设计。此文件不是某个真实工程已完成结构验证的证据。
