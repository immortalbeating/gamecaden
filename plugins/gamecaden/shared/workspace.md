# 工作区与来源约定

供 flow 定位和 init 登记，并由本工作流其他 Skill 读取来源。新原生映射的 v1 候选字段已由[格式合同](formats-v1.md)与[可校验 schema](../schemas/workflow-v1.schema.json)细化；本页维护接入职责与用法，不代表已发行或完成宿主安装验证。

## 工作流适用条件

使用Gamecaden职责前确认本次依据，满足以下任一条件即可：

- 用户明确要求以Gamecaden或其命名职责处理本次工作，或明确要求项目接入Gamecaden。同一尚未结束的授权工作及flow按该授权选择的后续职责沿用这个依据，无需用户逐一点名。
- 当前项目有效指引明确采用Gamecaden。按指引的实际作用范围恢复原入口与原记录，并根据本次请求选择职责。

普通未采用项目沿用其有效指引、原记录与专业工具完成请求。技能可见、目录元数据介绍、仅提及名称、任务属于游戏开发、历史讨论或发现同名目录，都不构成使用或采用依据；历史归档、其他项目及仅作参考的材料也不替代当前指引。没有上述依据时不自动选择本工作流，也不以要求接入代替用户原任务。

仅阅读、解释或评审技能本身时，可把正文作为待分析材料，不因此执行其项目职责。单次显式调用按本次范围沿用已有资料，完整接入/迁移仍遵循init的独立授权与来源约定。适用条件不扩大写入、实施或发布权限；只读和进行中工作的授权边界照常生效。

## 1. 位置与解析

优先使用用户指定或有效项目指引明确引用的工作流入口。新项目草稿默认 game-workflow/，其中 workspace.yaml 记录映射、index.md 负责阅读导航。品牌确定后再统一发行默认值；已接入项目保留自己的映射路径。

workspace.yaml 中所有 path、root、marker 均相对于该 YAML 所在目录解析。写入前结合本次明确目标解析实际路径，核对项目、工作树与作用范围。相对路径使同一项目可以在不同 checkout 中使用；实际运行结果仍记录本次具体基线。

同名项目、目录或分支不是写入目标证明。映射指向范围外的资料可以作为相关引用；它不会扩展本次对其他目录的修改授权。

用户明确调用 flow 完成具体交付，实际目标已唯一确定，且核实没有既有工作来源时，可在该项目 game-workflow/tasks/ 保存必要 Task 记录；这是本次交付的留存，不等于全项目接入或旧流程迁移。无真实需要时无需为此先生成 workspace/index/AGENTS。下次没有映射但存在该默认集合时，核对其 Task 格式、目标和项目现场后读取；遇到已被其他用途占用或互相冲突的入口再解决具体冲突。

## 2. 便携字段

| 字段 | 含义 |
|---|---|
| schema_version | 本稿格式版本，当前为 1 |
| project.id | 稳定项目身份；沿用已有明确标识或首次登记时分配，不随分支/显示名称改变 |
| project.name | 人可读名称 |
| project.root | 本项目实际根的相对位置 |
| runtime_roots | 已确认的运行根列表；没有运行入口时允许为空 |
| runtime_roots[].id/path/engine/marker | 运行用途标识、目录、已识别引擎和实际标识文件；engine 不代表运行已验证 |
| sources | 原始文档或记录集合；每项有 id、role、kind、path、owner，必要时 scope/format/adapter |
| default_task_source | 新 Task 的唯一默认来源 id；尚未决定时可为空，现有任务仍按原来源操作 |
| default_epic_source | 新 Epic 的默认来源；无需要或尚未决定时可为空 |
| rule_sources | 真正生效的项目规范/profile 来源及适用范围；仅登记可定位的材料，使用时按[规则选择与加载](rules.md)判断 |

sources 的 role 使用 vision、spec、roadmap、task、epic、asset-ledger、evidence、decision、notes、parking-lot。kind 为 file 或 collection。owner 表示维护约定，例如 flow、codestable、trellis、project；它不是操作系统权限，也不强制必须存在同名工具。

format/adapter 说明实际形态与适配线索，省略时先识别；声明适配器不等于已有写入能力。新建时按需使用[workspace 模板](../templates/workspace.yaml.tpl)，旧来源不会因为登记映射而自动转换。

首次登记的管理 ID 和常规存放位置可以由模型按约定选择并保存，无需让用户逐个命名。新 Task/Epic 集合默认 owner 为 flow，其他新项目文档默认 project；已有系统或生成器的来源沿用真实维护约定。分配管理标识与推断产品事实不同，不能因此编造目标、引擎入口或批准。

同一作用范围的同一事实只能有一个维护来源。多个 task 集合可以并存，但各自的实际对象/范围应明确。有 workspace 映射时，新任务使用明确的 default_task_source；无映射的单次 flow 交付按第一节约定留存。默认来源尚未确定且确需新建工作时，先依据用户要求、现有管理范围和默认位置补齐；只有仍有实质冲突才澄清。已有任务依据其原来源继续，不能被默认新来源重新收编。

文件来源应指向实际存在且可解释其职责的正文。collection 可以表示按需创建的新记录位置；未产生内容时不必建空目录。若已有任务引用却找不到集合，按缺失记录处理，不能直接当空项目初始化。

采用包内工程 profiles 时使用 [profile 接入约定](../profiles/README.md)：规则选择及项目差异保存到原 Spec/规则，rule_sources 只登记本项目根内的实际文件；需要可移植的固定正文才保存有来源版本的本地快照。包更新不自动改写项目已生效规则。新建/迁移目录职责见 [project-structure](../profiles/project-structure.md)。

## 3. 新项目示例

这是一个已有 Godot 标识及规格的新项目登记示例，不得照抄为其他项目的事实。

```yaml
schema_version: 1
project:
  id: aurora-game
  name: Aurora
  root: ..
runtime_roots:
  - id: game
    path: ..
    engine: godot
    marker: ../project.godot
sources:
  - id: current-spec
    role: spec
    kind: file
    path: spec/index.md
    owner: project
  - id: tasks
    role: task
    kind: collection
    path: tasks
    owner: flow
  - id: epics
    role: epic
    kind: collection
    path: epics
    owner: flow
default_task_source: tasks
default_epic_source: epics
rule_sources: []
```

尚无工程的新项目可使用 runtime_roots: []；预定引擎记录在目标材料中。旧项目可将 task 来源映射到 .trellis/tasks 或 codestable 的实际集合，owner 保留原系统；复杂嵌套来源以真实入口和 scope 说明，不假定全都采用本稿 Task frontmatter。

workspace 不存当前 Task 状态、完成百分比、进程/端口、临时登录信息、批准副本或 package 命令副本。实际命令读项目配置，历史与续接读原记录。

项目 Git 策略作为适用规则由 rule_sources/实际入口引用，选择与保存见[Git 策略约定](git-policy.md)。沿用已有权威位置；新项目必要时使用 rules/git.md。仓库当前分支、远端差异和执行进度从 Git/原 Task 获取，不加一份动态镜像。

## 4. index 和宿主指引

### 新建资料的默认位置

在没有既有权威路径或用户指定位置时，新建正文放在当前工作流目录：vision.md、spec/index.md、roadmap.md、parking-lot.md、notes/、assets/ledger.yaml，以及按需的 evidence/、decisions/、views/。这一约定只决定需要新建时放哪里，不要求全部生成。

已有文档能承担职责时直接映射；同一输入文件包含多个职责时说明章节和当前维护范围。未来候选需要持续留存时由独立 parking-lot.md 维护，保留输入来源引用，Vision 只指向该停车场；原需求输入可以保留历史内容，不再把其中的候选段作为第二个活动停车场。默认集合中的新 Task/Epic 位置沿用共同记录规则。

### 入口正文与宿主段落

index 应简述本项目及工作流入口，指明目标/规格/路线/工作记录各从哪里读，说明旧系统保留的范围。只链接已经存在的文件；尚未创建的集合可以说明用途，不把不存在的正文写成有效链接。

在实际生效的项目指引中合并本流程的短段落，路径按项目实际位置改写。默认示意：

```markdown
<!-- game-workflow:begin -->
## 游戏工作流
- 本项目工作流入口为 game-workflow/index.md，根与来源映射为 game-workflow/workspace.yaml。
- 新会话处理本项目的开发、续接、验收或收尾请求时，先按实际可用的 flow Skill 读取相关入口和原工作记录；接入缺口按需交给 init。
- 用户要求继续时，依据原 Task 当前结果、推进限制和实际工作区定位下一动作；多项工作无法按目标/前提确定时再澄清。
- 沿用各记录的维护来源；执行进展与续接写回原工作，汇总视图读取原事实。
<!-- game-workflow:end -->
```

只在实际提供本流程 Skill 的环境中写入相应技能指针，使用其真实可发现名称。未安装时可先提供文件阅读入口，并说明技能发现尚未验证，不能留下一个声称可调用的虚构命令。

保留已有规则。检查 override、嵌套作用域和当前宿主来源，避免新增被覆盖的无效入口。文件写入与后续会话实际加载分别报告；不为本项目接入修改全局用户指引或宿主配置。

安装与项目接入后，需要在正确项目的新会话中分别检验自然语言“继续”、显式 Skill 调用和只读状态请求，观察实际加载来源、所选原工作与写入行为。没有做过这类宿主验证时，只能声明指引和文件已准备，不能声称每次必然自动调用或自动执行。

## 5. 接入结果与复用

init 返回：本次实际根、运行根、来源/规则引用、实际写入、仍相关的缺口和下一动作。它们构成当前上下文，不另存第二份动态 context/state 文件。

回读相关文件和路径；重复接入优先复用已确定的来源与授权。任何一步只部分完成时说明已发生与未完成内容，下一次从这些实际结果恢复，不无条件从零重建。
