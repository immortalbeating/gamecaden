<a id="验证范围与方法"></a>
# Validation Scope and Methods

Program checks, host discovery, model behavior, game runtime, user acceptance, and release delivery need separate evidence. Passing one layer does not replace another. Historical development/installation results below remain in their original Chinese wording and retain their original source versions; they are not silently relabeled as new release checks.

<a id="仓库检查"></a>
## Repository checks

Run from the repository root using Python 3.12+ and Node.js. For panel/I/O dependencies, prepare an isolated environment under the [panel guide](../plugins/gamecaden/panels/README.md), then run with its interpreter:

```sh
python scripts/check.py --suite all
```

`all` covers contracts, Python, JavaScript, and build integrity. Select smaller checks according to impact:

```sh
python scripts/check.py --suite core
python scripts/check.py --suite distribution
```

The entry point and `--help` define actual suites. Contract checks verify interfaces/file relationships; core regression checks I/O, governance, and panel models; distribution checks builds, integrity, installation, and recovery. Before release, run the complete suite and retain the environment, commands, actual results, and uncovered scope. Material-language behavior requires inspecting actual generated documents, including headings/labels, not only response language or tool exit codes.

## v0.2.1 icon patch validation

The 2026-10-14 patch adds the selected orange G and charcoal play icon to the Codex listing and composer. All three plugin manifests use 0.2.1. Independent byte comparisons against the 0.2.0 release found no changes in the 103 Skill, shared-contract, schema, template, profile, script, and panel files.

Local validation ran the complete required check entry with Python 3.14.5 and Node.js 24.16.0:

```sh
python -B -X utf8 scripts/check.py --suite all
git -c core.whitespace=cr-at-eol diff --check
```

All 153 core tests passed. Distribution completed 45 tests: 44 passed and one file-symlink capability test was skipped on Windows. All 13 JavaScript tests passed. The complete entry also verified contracts, source inventory, and identical inventories and ZIP bytes from two fresh builds.

The PNG is a decoded square 1254 by 1254 RGB image, 1,392,298 bytes, with valid chunk CRCs and compressed image data. Both branding references resolve to this packaged file. The verified package contains 153 inventoried resources plus its inventory manifest. Image provenance was inspected for accidental private paths or user material; none was found in the inspected metadata. Raw prompts and local release records remain outside the public package.

These checks establish package and program integrity; they do not rerun game projects, model behavior, human gameplay acceptance, or the host's rendered plugin UI.

## v0.2.0 release validation

The 2026-10-12 release makes English the canonical development and maintenance language for all Skills, shared contracts, material references, profiles, and templates. The public repository has English and Chinese usage guides; complete Chinese rule comparisons and raw evaluation artifacts stay outside public history. Existing multilingual example fixtures and earlier validation observations retain their original source versions.

Local program validation used Python 3.14.5 and Node.js 24.16.0:

```sh
python -B -X utf8 scripts/check.py --suite all
python -B -X utf8 plugins/gamecaden/scripts/check_contracts.py
git -c core.whitespace=cr-at-eol diff --check
```

The final runtime implementation passed 153 core tests, 44 distribution tests with one file-symlink capability skip on Windows, and 13 JavaScript tests. Coverage includes native language-preserving writes, extraction provenance and exact legacy recovery, multilingual source excerpts, and handoff metadata time/replay without a forced-language body footer. Contracts, 536 local links/anchors, and 75 canonical rule/reference/template bodies were checked separately after the final language wording changes. Two fresh builds had identical package inventories and identical ZIP bytes, with 152 inventoried resources, 153 archive files, and retained MIT/EPL licenses and notices.

Fresh isolated Codex installations discovered all eight Skills with verified cache paths and digests. Actual Codex CLI sessions used gpt-6.1-sol/high and natural requests, without inheriting this maintenance discussion or scoring instructions. Inspection covered written documents, original input hashes, commands/results, source revisions, Task scope/status, and responses; process exit codes alone were not treated as behavior evidence.

| Natural request | Observed behavior |
|---|---|
| English formal adoption from an existing product package | English current Vision/Spec/Roadmap and entry points; original input retained; adopted goals separated from unimplemented capabilities |
| Chinese adoption with English product inputs | Readable Chinese current documents and explanations; English input retained; no invented runtime or acceptance result |
| English continuation of an existing Chinese quick Task | Existing Chinese README/Task language and quick identity retained; requested copy repair and real check completed within the original promise |
| Spanish design with existing English project inputs | New design/Task prose in Spanish; existing English Roadmap maintained in its language; design completion not presented as implementation or visual acceptance |
| Chinese independent verification and handoff for an English active Task | Real two-input kernel check, independently readable report and EV entry, source-bound handoff, retained English Task language and active/standard identity; no implementation or Git changes |

Language suitability is assessed from readable prose and explanations for the user, stable technical identifiers, and established professional terminology. It is not a zero-English test or a gate on isolated English labels. Exact inherited scope/coverage bindings retain their actual values. The final narrowed wording was tested in a fresh installation on the affected verification/handoff request and independently reviewed.

The first capacity-limited continuation attempt changed no project files; its failure was retained and a fresh session with identical inputs completed. An early navigation candidate incorrectly treated YAML comments as Markdown headings; contract checks caught it before model execution, and it was corrected. Initial handoff observations exposed an automatic English timestamp footer, which was removed while preserving actual UTC metadata and replay behavior. A free-text English metadata value also prompted clarification; the final user-approved policy then explicitly retained conventional terms and labels without creating language acceptance gates. Earlier observations were not rewritten as final-byte reruns. The affected path was retested after the code and policy corrections, while still-applicable observations on other paths were retained.

The program suite covers the final runtime code. The final release differs from its last model-test package only in an installation-guide sentence identifying English maintenance as canonical; the shared language policy and runtime code are unchanged. Final contracts, integrity, navigation, and deterministic builds cover the release source. These observations do not guarantee every future host/model/session, nor prove a cost reduction without a before/after comparison.

The first release CI run passed on Ubuntu but exposed a Windows test-fixture setup error: TEMP used an 8.3 path alias while the tool bound its canonical root. The source-I/O fixture now resolves its existing root before constructing context and targets. An actual Windows short-path experiment reproduced the old refusal; all seven affected tests then passed with the corrected fixture. Production path-boundary, reserved-location, symlink/junction, and revision protections were not changed. The complete Windows/Ubuntu CI matrix is rerun on this fixture correction before publication; the initial failed run remains recorded.

No real game-engine execution, GPU/raster acceptance, physical-device behavior, user playtest approval, macOS execution, or new Claude model behavior was verified in this batch. Daily installed copies and external game projects were not changed. Transient evaluation authentication was removed; anonymous raw evidence remains local. Historical sections below describe earlier development snapshots, including their then-unpublished status, rather than a new release certificate.

## 未发布变更：Task 管理模式与执行深度

2026-10-12，Task 统一使用 quick 轻量、standard 常规两种管理模式，按整个交付的组织与维护需要选择。standard 覆盖普通开发中的方案、步骤、接口、批次和持续跟进，低风险同样适用；其中明确的局部步骤也可直接执行与简记。已有 Task 内的修复、补验和调整保留原身份/模式，仅在范围或管理需要实质改变时重判。已可用输入、成熟库、Epic 归属、普通换会话、报告/测试数量及一次失败均不单独决定模式，边界由模型按实际需要判断。

共同合同、flow/develop 和变更处理引用同一规则；通用 Task 模板填写实际 mode，轻量模板补开工目标、必要检查与真实未开始/执行结果，面板同步模式名称。验证与必要接受继续按真实承诺处理，模式字段及 I/O 写入保护沿用既有结构。

使用已准备的独立 Python 3.14.5 执行：

```sh
python -B -X utf8 scripts/check.py --suite all
git -c core.whitespace=cr-at-eol diff --check
```

flow、develop、close 三个入口另用 skill-creator 的 `quick_validate.py` 检查元数据。

核心 143 项通过；分发 45 项完成，44 通过、1 因本机文件符号链接能力跳过；JavaScript 13 项通过。合同核对通用 Task 模板的 quick/standard 两种实际绑定及原生元数据，三个入口元数据与空白检查通过；完整检查另核对包完整性与确定性双构建。公共资源仍为152项（含库存共153个文件），版本仍0.1.3。

模型行为在与当前来源字节一致的独立安装中，以真实 Codex CLI、gpt-6.1-sol/high 执行六类自然请求，共七个新会话；不继承维护讨论或评分条件。保存原始提示、完整会话、工具返回、读写回执、前后来源摘要、产物及最终答复，逐项核对实际行为，并经独立只读复核。六类最终交付均符合本次范围，未发现实质遗漏或错误完成声明。

| 自然场景 | 本批最终观察 |
|---|---|
| 新独立按钮文案修复 | 新建 quick，原检查实际通过；保存目标、结果、覆盖与续接，其他文案和原检查保持不变 |
| 原 standard 的局部文案修复 | 保留原 ID、路径、standard；直接修改、检查及收尾，没有另建同目标工作或设计计划 |
| 已可用输入与本地模块接入 | 新 Task 采用 quick，实际调用原 formatter 并通过两项输入/调用观察；原输入与生产 Task 不变，Epic 按真实整体出口收尾；独立检查报告未迫使模式升级 |
| 旧存档兼容设计，经验规则未定 | 采用 standard，保存条件化方案、备份/回退和待执行验证；未把样本 7→27 当作转换规则，原规范及样本不变；只按设计承诺关闭，没有迁移实现或运行通过声明 |
| quick 换会话且上一轮命令失败 | 保留原 ID、位置、quick 与失败历史，修正后运行原检查并保存实际结果，没有因会话切换/一次失败升级 |
| 低风险、输入与方法已定的分步功能 | 一个 standard Task 内维护两次实施、接口及整体检查；仅实现并验证本次内核，原消费者文件不变；完整交付仍 active，没有额外 Epic、PDP 或独立计划 |

旧存档设计首轮因服务返回模型容量不足而退出，项目字节不变，不算行为通过；用相同提示与初始文件摘要另开新会话补测，原失败保留。五个完成案例曾出现错误列表字段、依赖缺 target 或更新缺 reason 等 I/O 请求拒绝，writes 为空；另有猜错材料路径。模型纠正后完成，失败轨迹继续保留，不宣称首次请求全部成功。判断看有效结果、实际恢复和当前承诺，不用进程退出码或 mode 标签单独判分，也不把简单交付选 standard 本身算失败。

来源与测试安装包最终摘要同为 `10b0efaf3e070a15f26bcbd12850164c66a55112045e882db5cad94eecf28dc9`。本批没有变更前对照，不证明成本下降、所有模型/后续会话必然遵循或某种模式应占固定比例。未验证 Claude Code 新行为、真实游戏/引擎或用户视觉/玩法接受；日常安装副本及三个外部游戏项目未同步，未推送或发布。匿名原始资料与本机路径留在公共包外，临时认证已移除。

## 未发布变更：Roadmap、分阶段计划与派生输出

2026-10-12，正式采用项目级持续开发时默认建立当前 Roadmap，正文包含产品/版本范围、M 里程碑表、当前整体判断及来源维护范围；仅有一个已知成果也可建立，未知未来保持未定。已采用大型方案需要分阶段落实时，经独立 Phased Development Plan（PDP）编排 Epic 与局部 S Stage，承接 Task 仍归对应 Epic，已有被引用工作保留原归属。PDP、Roadmap 与原设计/工作各维护自己的事实，结果影响组合判断时及时同步原依据。

新增 development-plan 来源角色与独立创建/登记，默认 plans/<安全标题>.md，无工作 ID 或生命周期；保留原 Task 内 plan 和旧附件规则。PDP 目标属于其他来源角色时拒绝静默混入。视图按需保存 JSON，现有 HTML 面板直接读取来源；默认冻结目录禁止新请求覆盖，原中断请求仍按 before/after 精确恢复。独立 handoff 使用实际来源、UTC 默认名称和重复轮次；明确引用有未结算写入的来源时先恢复原操作。

使用已准备的独立 Python 3.14.5 执行：

```sh
python -B -X utf8 scripts/check.py --suite core
python -B -X utf8 scripts/check.py --suite distribution
node --test tests/test_panel_refresh.mjs
python -B -X utf8 plugins/gamecaden/scripts/check_contracts.py
git -c core.whitespace=cr-at-eol diff --check
```

核心最终 143 项通过；分发 45 项完成，44 通过、1 因本机文件符号链接能力跳过；JavaScript 13 项通过。新增回归覆盖 PDP 独立创建、登记/回读、标题更新、角色/owner 边界，handoff 来源变化、未结算来源、重复/同秒/长路径名称，以及冻结视图新建保护、写后中断恢复和外部修改留存。独立只读复核发现的类型丢失、冻结覆盖、交接旧字节及冻结恢复问题均修正并补有针对性的回归。设计 Skill 元数据检查、最终合同与包完整性通过，最终来源及确定性双构建摘要相同；152 项公共资源（含库存共153个文件），版本仍0.1.3。

模型行为使用独立安装的真实 Codex CLI，在匿名项目执行七类自然请求，共八个新会话，配置为 gpt-6.1-sol/high；不继承维护讨论或评分条件。保存原始提示、会话调用、工具返回/回执、源修订、文件变化及最终答复，逐项对照实际产物并经独立只读复核。

| 自然场景 | 本批实际行为 |
|---|---|
| 已有设计包，正式持续接入，仅一个成果已定 | 建立固定 Vision/Spec/Roadmap/M1 及入口；原包保留，不编造后续成果或创建空工作 |
| 已采用大型方案，先交付上位编排 | 独立 PDP 与 Roadmap 创建、登记/回读；最终复测两个拟建目标、七个 Stage，承接归属明确，原方案未改，没有新 E/T 记录 |
| 已有充分安排的简单 Epic | 实际修改两处字符串并检查，原 Epic 与承接 Task 收尾，不生成 PDP |
| 原 Task 的局部按钮纠错 | 现有检查通过后原 Task 收尾，未来 Roadmap/PDP 字节保持不变，没有另起版本工作 |
| 子 Task 已关闭，但组合消费者缺结果 | 实测首胜返回0而要求10，S1/M1未达成；保留局部 Task closed、Epic active，原 Epic/PDP/Roadmap引用同一失败依据 |
| 两份不同续接用途的独立交接 | 生成两份默认 Markdown 快照，scope、来源修订、UTC 时点及限制可回读；原 Task/资料字节不变 |
| 保存进展用于离线比较 | 仅生成冻结 Progress JSON，原来源及 active 状态不变；说明实时面板无需先保存文件，不冒称完整路线/阶段模型或静态 HTML 导出 |

初批大型方案案例曾将一个归属成长目标的组合 Stage 安排为未来 epic:null 的共享 Task，判定仅部分符合。随后澄清“新 Stage 承接 Task 归对应 Epic，引用的既有独立工作保留原属”，以完全相同的自然请求和初始资料，在新的冻结安装中复测；实际表、归属及33处链接核对通过。复测的初次链接检查因项目根规范化断言失败，修正检查器后通过；不将其说成首轮检查全过。原失败产物和会话保留，没有改写初轮结论。其余六案复用仍有效的观察；不宣称八个回合均在最终全部字节上重跑。

程序回归覆盖最终工具实现，最后的 PDP 归属文字补修另核对合同、元数据、完整性与确定性双构建。模型观察没有变更前对照，不能证明所有宿主/后续会话必然遵循。未验证 Claude Code 新行为、真实游戏/引擎运行或用户视觉/玩法接受；未提供完整面板静态 HTML 导出。日常安装副本及三个外部游戏项目未同步，未推送或发布；匿名日志与本机路径留在公共包外，临时认证已移除。

## 未发布变更：证据留存、来源读取与判断边界

2026-10-11，证据按用途选择 Task 简记或可定位报告；正式出口、独立复核、资产审阅和跨任务/版本使用明确留存与索引，新轮次保留最小充分历史。Task 专属材料默认归其 evidence 子目录，旧报告和旧平铺附件不迁移；已有完整报告不复制。目录整理、当前文档入口、来源范围和局部接受/独立决定统一引用 shared 合同；本轮明确例外不自动改成长期规则。

实现补齐原生集合内二进制的只读/SHA 绑定及 Windows 长源路径。非记录代码、SVG 和未知 UTF-8 文本继续返回原文，二进制保持 body=null、无正式 ID/写能力。列表三类详情共同分页，保留全扫描计数/诊断计数和指纹；面板同查询核对完整指纹。仍全扫描以保护一致性，实际范围靠相关正文/索引及窄集合，不声称扫描耗时已经消除。新候选和同对象/字段新增引用严格核验，旧身份/版本/选用保留；历史载荷失配给诊断，不阻止登记有效新候选，所选候选仍检查实际成员。

最终程序与合同验证使用已准备的独立 Python：

```sh
python -B -X utf8 scripts/check.py --suite core
python -B -X utf8 scripts/check.py --suite distribution
node --test tests/test_panel_refresh.mjs
python -B -X utf8 plugins/gamecaden/scripts/check_contracts.py
git -c core.whitespace=cr-at-eol diff --check
```

核心最终 133 项通过；分发 45 项完成，44 通过、1 因本机文件符号链接能力跳过；JavaScript 13 项通过。独立复核另验证长路径中的 junction/越界仍拒绝，新候选成员在检查后改变导致冲突且不写台账。面板分页比较回归、旧失效 Ref 的新增/跨位置边界以及代码正文兼容均按实际失败补回归，保留初轮失败结果。分发和 JavaScript 结果复用其后未改变的安装/接口分支；最后的局部决定文字澄清与非记录文本恢复另以核心、合同、包完整性及确定性双构建核对。

模型行为在独立安装和匿名工程中，以真实 Codex CLI 的九个新会话执行自然请求，不继承维护讨论或评分标准；指定 gpt-6.1-sol/high。保存原始输入、工具返回、会话、逐文件修订/回读并复核实际产物，进程退出 0 不等同被测交付通过。

| 自然场景 | 实际判断与行为 |
|---|---|
| 配置检查通过，消费者未实现规则 | 实跑接口发现结果不符，保存失败和欠项，未改实现或关闭 |
| 方向已选，展示输入未对应 | 查实际读取及输出，保留未交付；检查只覆盖语义输出，没有栅格或视觉接受 |
| 帧槽齐全，源姿态重复 | 区分槽数/频率通过与不同姿态未生产，独立报告回写原 Task，未宣称实播接受 |
| 测法变化，旧结果已用于复核 | 新轮次报告、输入及 stdout 保存，旧报告字节保留；当前引用同步，不改旧失败为通过 |
| 充分的小文案修复 | 实际修改/检查并在原 Task 简记关闭，无额外全量验收或报告包 |
| 充分的规则演示 | 核验通过且说明覆盖，验证请求未自动关闭 Task 或改实现 |
| 保留检出转向生产根续接 | 在目标根执行 I/O/修改/检查和收尾；原保留检出字节不变 |
| 本轮明确授权代判接受 | 依本轮对象/范围执行并记录 agent 归因，关闭该 Task，长期规则字节不变 |
| 同类工作没有本轮例外 | 完成修改/技术检查，准备真实接受材料；按项目原接受条件保留 active |

前七案使用冻结候选，后两案使用随后补齐的授权规则候选。后续候选引用分组、局部决定文字及非记录文本恢复未改变这些输入分支的要求或动作；相应工具分支另用最终源码回归，不宣称九案全部在最终字节重跑。最终源/双构建摘要一致，149 项资源（含库存共150个文件），版本仍0.1.3。匿名原始证据和本机路径留在公共包外，临时认证已移除。

本轮未更新日常安装副本、迁移三个游戏项目或验证真实引擎/GPU画面、人工视觉/试玩接受；未推送或发布。文档与匿名模型回归不保证所有后续会话必然遵循，正式项目按实际版本与承诺继续验收。

## 未发布变更：Task 目录与普通附件

2026-10-11，新 Task 默认采用 `tasks/T-编号-短名/task.md`，专属材料按需同目录或子目录保存；旧平铺 Task、原身份、显式路径及原附件位置继续兼容，改标题不迁移。原生编号集合子目录中的普通 Markdown/JSON/YAML 材料不再按 Task 校验；生产者局部 ID、状态和关系字段不成为工作身份、生命周期或依赖。正式主文件、正式 ID、坏原生块和重复身份仍严格检查，普通附件不能通过创建或更新转成新工作记录。合同、Schema、默认创建器、面板索引与导航同步。

最终源码使用已准备的独立 Python 环境执行：

```sh
python -B -X utf8 scripts/check.py --suite core
python -B -X utf8 scripts/check.py --suite distribution
node --test tests/test_panel_refresh.mjs
git -c core.whitespace=cr-at-eol diff --check
```

核心 120 项全部通过；分发 45 项完成，44 通过、1 项因本机文件符号链接能力跳过；JavaScript 13 项通过。覆盖自然附件名称、生产者数据与编码保留、正式身份保护、后续编号分配、新旧布局、显式路径、标题修改、回执重放、并发、面板关系和导航。早期匿名测试修正了既有外部来源的完整性预期与已保留 Evidence 编号；独立源码复核发现的局部 ID、非对象 frontmatter、字段更新和消费者隔离边界均补回归后通过。

模型行为由一个不继承维护讨论的独立代理，在冻结完整包与匿名项目中执行两项自然请求：新增候选预览说明维护交付，并将设计和实施安排独立保存；沿原 T-002 整理来源和文件清单。实际 I/O 创建了新目录内的 `task.md`、`design.md`、`plan.md`；原平铺 Task 和附件原位置保留，生产者编号及来源正文不变，局部状态更新成功，原 Task 仍 active。新维护 Task 按其文档承诺关闭，没有把来源审阅记录为视觉接受。保留请求、原始响应、逐文件修订、回执、回读与实际文件；一次错误列表参数被拒绝且未写入，修正后成功。

该回合显式提供冻结 Skill 路径，角色配置为 gpt-6.1-sol/low，不验证原生宿主自动发现或 Claude/Codex Desktop 新会话。冻结包之后补充的真实 owner、非字符串标题和集合根显式 `task.md` 边界不影响这两个输入分支；最终包另以本地 CLI 回读新 Task 和原来源附件，均成功。普通项目说明文件仍由原位置维护，不把无写适配器的原文读取冒称为原生记录写入。

最终源包与构建包完整性一致：149 项资源（含库存共 150 个文件），摘要 `0c547285dd7a5f2c608fed67b16a4f5ce6a69e509f247c92e9b5640b5c03e9e8`，版本仍为 0.1.3。忽略的编译缓存保存在公共包外；匿名输入、原始日志和本机路径不进入公共资源。未更新日常安装副本或迁移外部项目，未验证真实游戏/引擎、视觉/玩法接受，也未推送或发布。

## 未发布变更：项目级当前正文与接入行为

2026-10-11，正式接入从已给材料整理固定的当前 Vision、必要 Spec 总览和 Roadmap，正文可独立表达结论，详细输入保留具体引用及明确维护范围。纯愿景也复用内容形成确定入口；当前方向、生效规则、目标方案、实现基线、候选与历史结果分别处理。后续变化按影响写回当前正文和原工作，旧映射、单次交付及局部续接保留兼容。公共程序、Schema、核心回归输入和九个入口的 frontmatter 未改，不增加全局门禁、审批或每日全量加载。

使用已准备的独立 Python 环境执行 `python -B -X utf8 scripts/check.py --suite distribution`：初候选及最终候选均退出 0，每次 45 项完成，44 通过、1 项因本机文件符号链接能力跳过。包内合同/链接、修改的 init/brainstorm/design 的 `quick_validate.py`、包完整性与 `git diff --check` 通过。最终公共包为 149 项资源（含库存共 150 个文件），源码摘要为 `ae9f777f706fb92e30ee72b7d5123bb980ea57a2ba70ab1d7eaea4883170536f`，版本仍为 0.1.3。程序及核心回归输入不变，未重跑核心或 JavaScript 回归。

模型行为使用真实 Codex CLI 0.162.1、gpt-6.1-sol/high，在独立配置与匿名项目中执行自然请求，每个回合是新会话，不继承维护讨论或评分标准。安装包经新 app-server 发现八个职责，缓存字节与相应候选一致；独立 Python 工具检查就绪。保留原始输入、会话、成功/失败工具返回、写入修订与回读、文件摘要及独立语义复核；判分依据职责和实际结果，不以文件名、标题或命令退出 0 代替内容判断。

| 自然场景 | 最终观察与结论 | 证据批次 |
|---|---|---|
| 混合产品材料正式接入 | 固定愿景、规格、路线和候选分流；三个原承诺成果及历史检查范围保留；原始输入字节不变；映射不复制动态检查结果 | 最终候选重测 |
| 已采用纯愿景正式接入 | 复用已采用内容形成固定 Vision；旧正文仅有边界的转向；单一成果不因工程准备生成 Roadmap；两方暂停来源冲突保持未确认 | 最终候选重测 |
| 明确改变核心体验 | 同步 Vision/Spec/Roadmap 与受影响工作；取消已不适用的旧交付并保留历史，新工作仅承接设计，没有游戏实现 | 复用未受细化影响的初轮 |
| 局部功能设计 | 保存可执行的设计/图件和安排；其他主要正文、原 Task 及候选摘要不变 | 同上 |
| 候选只读讨论 | 分析备选，保持未采用；全部项目文件摘要不变，无实施 | 同上 |
| 自然继续原 Task | 修正真实 README 消费者，已有检查实际通过；保存并回读原身份/位置，未推进其他工作 | 同上 |
| 单次显式 GC 局部交付 | 修复、检查并保存必要 Task；未建立 workspace/index/AGENTS 或全套正文 | 同上 |
| 旧混合映射续接 | 沿原 records 来源与 Task 身份修复、检查并回写；未迁移主文档或新建重复入口 | 同上 |
| 无工程但已有明确完整目标 | 直接整理固定正文与三项承诺成果，建议依赖区别于已定承诺；不重复访谈或虚构引擎、工程、实现与接受 | 同上 |

本批共 11 个原生回合，覆盖九种场景。初轮九回合均正常退出，但独立内容复核将混合接入判为 limited（scope 存了当前检查结果）、纯愿景接入判为 fail（把无采用依据且相互冲突的暂停表述提升为生效规则）；后者另有把单一成果的准备步骤展开为 Roadmap 的不充分触发。根据实际观察，合同补清采用依据、冲突未确认、Roadmap 成果粒度与 scope 的事实边界，最终候选以另一独立安装/配置重测两案，通过语义验收。初轮结果保留，其他七案未受这些接入细化影响，复用其有效结果；不声称九案全部在最终字节重跑。

纯愿景场景没有冻结旧正文的指示，允许保留原采用段的职责转向与导航标注；混合场景明确要求原始材料不动，继续按字节核验。两者的采纳依据、唯一维护责任和路线必要性标准相同。原 README 文本检查的失败在接入场景中如实保留为未确认暂停冲突，不外推为游戏行为失败，也不冒记通过。

证据限定于上述匿名 CLI 场景，不证明所有后续会话必然遵循或遗漏率下降。成功运行采用 danger-full-access/never；未新增 Windows 受限沙箱、Codex Desktop/Claude 行为、真实游戏/引擎运行或用户接受验证。日常安装副本、外部项目记录、历史发行与版本未更新，本轮未推送或发布。凭据仅临时用于两个独立配置并已移除，原始私有证据与本机路径留在公共包外。

## 未发布变更：项目指引入口与续接操作根

2026-10-10，默认宿主段落明确项目采用 Gamecaden，并以实际可发现的 flow 名称定位入口与原记录；示例的技能名按宿主回读改写。移除其中重复的 init 路由句，修复职责仍由 flow 按需选择。续接参考补充恢复或切换工作树时核对实际命令目录和本地 I/O 的 project_root。不增加实验转正式条款、每轮初始化或全量规则加载要求；init/adoption 正文、九个 Skill 正文和 frontmatter、程序/schema 均保持原字节。

使用已有独立 Python 环境执行 `python -B -X utf8 scripts/check.py --suite distribution`，退出 0：45 项完成，44 通过，1 项因本机符号链接能力不足跳过。源包完整性与合同检查通过，公共包含 149 项资源（含库存共 150 个文件），当前源码摘要为 `2b6f65e26d0fe11b08f15fcbe603e1f1f1f10dc4f857f5fa7fffb451acc70c76`。程序与核心回归输入未变，未重跑核心回归。

从该源码构建并校验包，安装到独立 Codex 配置实例；新 app-server 的 skills/list 实测八个启用入口，安装字节与源码一致。模型行为使用 Codex CLI 0.162.1 的独立新会话，配置和会话元数据为 gpt-6.1-sol/high，不继承维护会话。匿名项目的指引从更新后的默认示例生成；提示只提供自然请求或显式职责，不提供评分条件。保留原生指引注入、成功的正文读取、工具调用与回执、文件变化及最终答复。

| 最终完整夹具请求 | 原生观察 |
|---|---|
| 自然“继续之前的工作” | 自动注入项目指引，实际读取当前 flow 与续接参考；完成原计时修复，四项已有断言通过，以匹配修订的原生 I/O 更新并回读原 Task |
| 从历史检出显式调用 flow | 自动注入历史检出的路由指引，读取当前开发根；功能检查、记录更新和回读显式使用当前根，历史检出字节保持不变 |
| 只读状态 | 实际恢复原 Task，识别未完成修复和用户暂缓项；项目文件字节不变，没有执行功能检查或推进任务 |

三个最终回合均保留原 Task 身份、active 状态及暂停项，未新增同目标工作或改写 workspace，未读取 init 正文。两执行回合的源码和原 Task 变化与原生写入回执对应，检查脚本、其他输入及历史检出保持原样；不把 I/O 的操作回执和锁文件当作第二工作记录。独立只读复核确认上述原生调用、回读和文件变化，也区分旧根指引的自动注入与当前根指引的后续读取。

本批共八个原生回合：两次早期状态回合被宿主受限执行环境阻止读取，不算恢复通过；最初三个可执行回合的匿名映射由维护者遗漏 default_epic_source，其中两个执行回合在工具拒绝后按 flow 选择 init、补 null 并回写原 Task，状态回合保持零修改。维护者修正夹具并用原生 record.read 预检后，重新执行上表三类回合，原受阻与修复证据均保留。执行成功的回合使用 danger-full-access/never；Windows 受限沙箱隔离未验证。

这些结果限定于该 CLI、配置、源码和匿名计时任务；没有变更前对照，不能证明遗漏率下降或所有后续会话必然遵循。未验证 Codex Desktop 新聊天、Claude Code 行为、真实游戏/引擎运行或人工接受。日常安装副本、外部项目采用记录、版本及发行内容未在本轮更新；原始日志和本地路径保留在公共包外。

## 未发布变更：材料用途导航与 Creator 恢复

2026-10-10，材料参考补充常用名称/别名、功能、触发场景与等效来源，区分转面/角色设定、拓扑/施工、状态/时序等用途。共同合同提供领域直达入口；brainstorm 补探索材料指针；旧项目保留原来源与维护责任。五个结构专题与 Web 补原生输入复用、目标差异和无工程初始设计边界。按用户后续要求恢复 Cocos Creator profile、专题及入口，Babylon.js 继续暂停；不增加统一材料包、审批、schema 或规则加载日志。

使用已准备的独立 Python 环境执行 `python -B -X utf8 scripts/check.py --suite distribution`，退出 0，45 项完成：44 通过，1 项因本机文件符号链接不可用跳过。源包完整性、43 个包内章节引用、brainstorm 的 `quick_validate.py` 和 `git diff --check` 通过；公共包含 149 项资源（含库存共 150 个文件）。九个 Skill 的 frontmatter 未变，程序/schema 与核心回归输入未改，未重跑核心回归。独立只读源码复核未发现阻断问题。

从最终源码冻结参考副本，以 15 组匿名资料进行四个新模型前向回合，每回合包含 3–4 个独立任务；同回合任务共用会话。各回合不继承父聊天，仅提供自然请求、项目目录和显式参考包路径，不提供期望答案或评分条件。使用 reviewer 角色，配置为 `gpt-6.1-sol/high`；实际服务端模型未另行回报。维护者对照原资料、有效合同及完整答复逐项核对。

| 情境 | 本批观察 |
|---|---|
| 按钮文案／返回与失焦 | 文案局部处理；行为变化实际形成状态/输入关系，不套完整 UI 材料包 |
| 新角色／既有受击／灰盒 | 继承参考的有效方面和消费者参数；结构缺项提出方案；已有身份与动作帧约定复用；代理范围可继续 |
| 经济成长／对白与动态音乐 | 资源流、解锁、重复支付、句子状态及音乐过渡进入设计，原配置继续拥有事实 |
| Phaser／Three.js | 区分监听与资源消费者、渲染树与业务寿命；处理共享消费者与迟到加载 |
| Godot／Unity | 区分保存 owner 与父子、定义与实例状态；沿现有 UI 系统及实际制作源，设计不冒充 Editor 结果 |
| 旧项目／方向比较 | 原 ID、位置与维护责任保留；只给比较意见和轻量材料，无额外访谈或正式生产包 |
| 地图／Cocos Creator | 实际形成拓扑、施工与门禁表达；Creator 形成 Scene/Node/Component、常驻、实例、暂停 UI 与加载关系，并叠加 Web |

本批十五份答复符合各自只读范围，未发现需要增加公共规则的遗漏或过度材料要求。79 个匿名输入文件、冻结参考副本与当前源包摘要前后保持一致。完整代理答复在本地协作会话留存，维护核对摘录及匿名资料留在公共包外；模型报告的来源列表不是完整工具轨迹，也不验证原生宿主自动发现。没有变更前对照，不能据此宣称遗漏率下降、成本降低或以后必然触发。

本轮未生成/接入真实游戏资产，未运行各引擎、浏览器游戏或目标构建，也未取得用户视觉/玩法接受。修改只在本地源码，安装副本、历史 tag/发行和外部项目采用记录未更新；设计选择、模型行为、运行采用与用户接受分别保留范围。

## 未发布变更：暂停两个专属 profiles

2026-10-10，按维护范围选择暂移除 Babylon.js 与 Cocos Creator 的两个 profile 和两个结构专题，并清理其选择入口、组合示例及 Web/共享引用。当前包保留 Godot、Unity、Phaser、Three.js、Web 和共同规则；通用与专属材料导航的合并精简方案仍待用户审阅，本轮没有实施。

执行 `python -B -X utf8 scripts/check.py --suite distribution`，退出 0，45 项完成：44 通过，1 项因本机文件符号链接不可用跳过；合同与源包完整性检查通过。公共包含 147 项资源（含库存文件共 148 个文件），暂停条目与其活动引用均已移出。另对照变更前源码核对 49 个 Skill、代码/schema、共同材料及保留专题文件字节未变，`git diff --check` 通过；独立复核未发现阻断性问题。

原文件及入口可从变更前提交 `0340c43480a3fea6c1e8127823655051b3bfe779` 获取；已在内存中重建变更前 151 项资源清单，与该提交的包摘要一致，没有恢复或改写当前工作树。后续启用需保留当时的新导航与其他修改，恢复相应入口并刷新库存，再按目标版本核对机制及实际采用；可恢复不等于适配已验证。

本轮未新增模型行为、原生宿主发现、游戏/引擎运行或用户接受验证；代码与相应核心回归输入未改，复用原有效核心结果。修改只在本地源包，安装副本、历史 tag/发行和外部项目已采用规则未变。

## 未发布变更：适用条件简化

2026-10-10，相对 `de7570c` 简化八个职责及独立入口的 description 开头条件，正文保留短检查并引用统一的工作流适用边界。职责描述剩余部分和其他正文未变，共享合同及宿主隐式调用配置未变；没有新增询问、审批或采用步骤。

执行 `python -B -X utf8 scripts/check.py --suite core`，退出 0，108 项通过；九个入口的 `quick_validate.py`、源包完整性、元数据与源码一致性、其余正文保持检查及 `git diff --check` 通过。

以五组匿名项目资料进行独立只读前向回合，只提供自然请求、项目目录和由当前源码提取的 Skill 元数据目录，不提供预期答案。使用不继承父聊天的 reviewer 角色，其配置为 `gpt-6.1-sol/high`；实际服务端模型未另行回报。元数据目录由维护者显式提供，不能当作原生宿主自动发现或选取验证。

| 情境 | 本轮观察 |
|---|---|
| 普通未采用项目 | 沿用原任务与设计，不启用 Gamecaden 或要求接入 |
| 仅提到以前读过介绍 | 未把名称或历史阅读当作当前授权 |
| 显式单次调用 | 按本次范围安排，保留原任务，不扩为全项目接入 |
| 已采用项目自然续接 | 沿用有效指引和原记录，不重复确认采用 |
| 尚未结束的单次授权 | 沿用当前授权，不要求再次点名，也不长期化或迁移 |

独立复核判定五份回复均符合各自只读准备范围。19 个输入文件及 152 个公共参考文件与快照一致；留存的是回复正文及模型报告的来源，不是完整工具轨迹。没有变更前对照、正文有无检查的消融或实际误加载回合，不能证明短检查必需、误调用率降低或未来必然遵循；也未验证实际实施、游戏运行或用户接受。本次仍为本地未发布变更，安装副本、历史 tag 和发行内容未更新，原始证据保留在公共包外。

## 未发布变更：讨论表达与 Git 选择

2026-10-10，brainstorm 将固定文字模板改为可选示例，保留默认逐轮提问、真实备选、推荐依据与等待实际选择。init 与共享 Git 策略区分本轮明确安排和长期项目约定：仅补当前动作所缺选择，确需建立或调整长期策略时再比较完整方案；直接 init 没有原 Task 时在当前接入结果中说明，不为保存 Git 安排新建 Task。

使用已准备的独立 Python 环境执行 `python -B -X utf8 scripts/check.py --suite core`，退出 0，108 项通过；brainstorm 与 init 的 `quick_validate.py`、源包完整性和 `git diff --check` 通过。对照变更前源码确认八个 Skill 的 description 与正文入口检查未变。

以匿名资料进行六个独立前向回合，只提供自然请求、夹具位置和明确的 Skill 入口，不继承父聊天，也不提供预期答案。使用只读 reviewer 角色，其配置为 `gpt-6.1-sol/high`；实际服务端模型未另行回报。

| 情境 | 本轮观察 |
|---|---|
| 要求简短自然对话 | 使用短对话说明两个真实方向、取舍和推荐，等待选择 |
| 要求逐轮讨论 | 先解决上游选择，保留后续依赖问题并等待回答 |
| 已有长期策略，本轮仅本地提交 | 按本轮例外安排，保留原长期策略，不重问完整套餐 |
| 尚未决定是否提交 | 保持未定，不强迫采用长期策略或制造提交授权 |
| 明确要建立长期策略 | 比较实际方案并推荐，未把推荐或现有远端写成用户决定 |
| 无 Task 的直接接入，本轮允许本地提交 | 在接入结果说明一次安排，不为此建立 Task 或长期 Git 规则 |

独立复核对照原资料与合同，判定六份回复符合各自只读准备范围。输入资料与公共参考包的字节摘要保持一致；留存的是回复正文和模型报告的来源，不是完整原生工具轨迹。Git 现状来自匿名假设资料，未创建实际案例仓库或执行案例提交、集成、推送、策略保存；明确指定 Skill 入口也不验证宿主自动发现。本轮只有候选回合，没有变更前对照，不能据此宣称改进率、成本下降或以后必然遵守。

临时 Git 仓库夹具创建命令在执行前被自动批准审查拦截，仅返回 `blocked by policy`，未计为 Git 执行证据；随后使用上述只读资料完成决策演练。未验证游戏运行或用户视觉/玩法接受。本次为本地未发布变更，安装副本、历史 tag 和发行内容未更新；原始证据保留在公共包外。

## 未发布变更：阶段说明修正

2026-10-10，修正工作区、规则、profiles 与 flow/init 中的草稿及未来发行措辞，指向 0.1.3 固定版本验证记录，并保留安装、宿主加载、引擎适配和真实项目结果的各自范围。包内 profiles 的分发与项目内规则/快照维护分别说明，不新增自动更新能力。

使用已准备的独立 Python 环境执行 `python -B -X utf8 scripts/check.py --suite core`，退出 0，108 项通过；源包完整性与包内相对链接检查通过。另对照变更前源码确认八个 Skill 的 description 与正文入口检查未变，brainstorm 及 Git 策略正文未变；`git diff --check` 通过。新增的固定版本验证引用已对照该 tag 的原文。

本轮不改变职责触发、访谈节奏、授权或 Git 行为，未新增模型、宿主发现、游戏运行或用户视觉接受验证；既有结果仍保留原基线与范围。本地源包摘要随正文更新，版本标识仍为 0.1.3；安装副本、历史 tag 和发行内容未更新。

## 未发布变更：约束定位与旧项目导航

2026-10-09，flow 在选择动作处增加按变更对象、消费者和交付阶段定位相关要求的提示；已有依据继续继承，缺项只约束依赖动作，方案回写沿用已有授权。旧项目接入参考增加六种情境导航，详细规则保留在原合同。

使用已准备的独立 Python 环境执行 `python -B -X utf8 scripts/check.py --suite core`，退出 0，108 项通过；flow 的 `quick_validate.py`、当前源包完整性、导航链接与章节锚点、`git diff --check` 均通过。规则正文最后的只读边界措辞调整后，重新核对格式和包摘要；程序及核心回归输入未改变，复用该次核心结果。

以匿名原任务、设计和配置进行七对独立前向回合。每回合不继承父聊天，只提供自然请求、夹具位置和对应工作流入口，未提供预期答案或评分标准。基线与候选的资料一致，仅 flow 提示不同；该对照不单独检验两版共有的导航改动。使用只读 reviewer 角色，其配置为 `gpt-6.1-sol/high`；实际服务端模型未另行回报。

| 情境 | 基线 / 候选 | 本轮核验的结果 |
|---|---|---|
| 文案快改 | 通过 / 通过 | 保留原任务、文案源和局部检查，不扩大工作范围 |
| UI 返回与暂停变化 | 通过 / 通过 | 识别状态及时间关系的变化，限定受影响设计与验证路径 |
| 已有角色新增受击 | 通过 / 通过 | 继承角色与动作配置，区分已接受身份和新动作的未验部分 |
| 新角色正式生产缺输入 | 通过 / 通过 | 继承概念的适用部分，定位身份、结构与制作输入缺项 |
| 获准移动灰盒 | 通过 / 通过 | 正式视觉缺项不阻断已授权代理试验 |
| 目标未变的旧任务续接 | 通过 / 通过 | 保留原身份、设计和剩余动作，不重新初始化或设计 |
| 同素材更换消费者 | 通过 / 通过 | 保留原接受范围，对新显示条件安排局部核验 |

独立复核对照原资料与合同判定十四份回复均符合只读准备范围。匿名夹具、参考包和已登记维护文件的前后字节摘要一致；候选 flow 与当前源码摘要一致。结果留存的是回复正文及模型报告的来源，不是完整工具轨迹，不能据来源列表证明每次读取或宿主自动发现。

基线和候选均为 7/7；本轮支持该批样本未观察到边界回归，不能宣称遗漏率下降、优于基线、成本降低或未来必然触发。未生成或接入真实资产、运行游戏、执行方案回写或取得用户视觉接受；六种旧项目导航的完整行为也未逐项实跑。

前期另有七次原生 CLI 尝试，分别遇到模型支持、上下文污染和工具访问阻碍，未取得有效行为回合；即使退出 0 或产生回复也未计为通过。它们与前向验证分开记录，不将后者转述为 CLI 集成通过。原始私有证据保留在公共包外。本次为本地未发布变更，安装副本与历史发行内容未更新。

## v0.1.3 首次使用与发行检查

2026-10-08，0.1.3 增加包内标准库运行入口，解决插件资源已安装而工具依赖尚未准备的首用缺口。以下分别保留发行前首用验证与当前发行检查，不改记旧版本的安装结果。

Windows 使用官方 Codex 与 Claude CLI 在独立用户目录从候选本地 catalog 实际安装；通用 Skills CLI 1.7.0 将同包复制到独立项目。三种安装目录均保留 151 项公共资源且与候选逐字节一致。另建不含 pip 或任何工作流依赖的 Python 3.14.5 环境，从各安装目录调用统一入口：首次准备后原 stdin 请求成功创建匿名 Task，重放复用原编号，重复 setup 不安装或改变缓存字节，冲突保留原状态并返回原生退出码 2。旧式不带 `-B` 的 CLI 调用保持包字节；Codex 新 app-server 发现八职责，没有发送模型请求。

Linux / WSL 使用 Python 3.12.3 的空依赖环境，实际通过自动准备、创建、重放、重复 setup 和合同检查。POSIX 虚拟环境解释器的符号链接路径保留，避免复用时误选系统 Python。最终工具代码在 Windows 与 Linux 各通过 19 项定向回归，覆盖缺依赖、只读检查、禁止安装、外部环境保护、安装目标配置隔离、半建 venv / pip 恢复、owner 发布中断、业务 stdin / 退出码和包字节保持。

候选开发过程的完整集合通过：108 核心、45 分发与运行入口检查（44 通过、1 文件 symlink 不可用跳过）、13 JavaScript、合同与重复构建。随后 POSIX 路径修正按影响补跑上述两平台定向回归和实际首用；最终封包重复构建字节一致。原生核心与面板逻辑未改变，复用已有有效检查。

正式 0.1.3 源在独立用户缓存环境重新执行 `python -B -X utf8 scripts/check.py --suite all`，退出 0：108 核心、45 分发与运行入口检查（44 通过、1 文件 symlink 跳过）、13 JavaScript，以及合同和重复构建全部完成。发行包与三个宿主 manifest 统一为 0.1.3，公共资源为 151 项。

本轮验证的是宿主安装与公共工具首用，不证明模型已执行完整游戏项目或用户已接受游戏。macOS 未实机验证；系统仍需可调用的 Python 3.12+ 与 venv 支持，首次依赖准备需要可用下载源和用户缓存写权限。未就绪时保留明确结果，不记为工具或项目已可用。

## v0.1.1安装兼容检查

2026-10-07，Windows公开布局完整执行 `python -B -X utf8 scripts/check.py --suite all`，退出0：108核心通过，26分发/恢复完成（25通过、1文件symlink不可用跳过），13JavaScript通过；合同检查与重复构建通过。新增回归覆盖三manifest与两catalog同源、独立完整资源、错误身份拒绝及历史包构建/校验/安装/回滚。

在新隔离环境中，Codex插件安装并由新app-server发现八职责；Claude Code 2.1.288官方validator、安装、list和details确认0.1.1及八职责。两种插件缓存与150资源的候选逐字节一致。Skills CLI 1.7.0复制到两个宿主的项目目录，也与候选一致；Codex独立目录实际发现总入口及八职责共九入口，均为repo scope、pluginId为空。安装器显示的一个包不能当成宿主一个入口，初次探针的数量假设失败已保留并按实际结果修正。

Claude独立目录通过文件/相对依赖核对；`plugin details gamecaden@skills-dir`不是普通Skill发现接口，其未找到结果保留，未据此声称原生Skill列表已验证。本轮没有发送模型请求、复制登录或改写真实游戏/用户安装；真实试点继续rc.8。远端发布消费及提交级CI结果以GitHub对应版本/运行记录为准。

## v0.1.0发行检查

2026-10-06，在Windows的独立公开仓库布局中，使用Python 3.14.5和Node.js执行 `python -B -X utf8 scripts/check.py --suite all`，最终退出码0：

| 检查 | 实际结果 |
| --- | --- |
| 合同、schema、模板与样例 | 通过 |
| 核心I/O/治理/面板 | 108项通过 |
| 分发与中断恢复 | 22项完成，21通过，1项本机文件symlink不可用而跳过；Windows目录junction拒绝与深路径用例实际通过 |
| JavaScript状态/阅读恢复 | 13项通过 |
| 同源重复构建 | 包摘要和ZIP字节一致，MIT及第三方许可在封包中保留 |
| 最终本地marketplace原生安装 | 隔离Codex home安装0.1.0，148公共文件与候选一致，新进程发现八个职责；未发送模型请求 |

公开布局的首轮检查曾出现27项深目录回执写入失败。发行版修复了Windows存储的物理长路径处理，逻辑路径、scope、guard与CAS保留；新增大于260字符回执的真实创建、幂等重放和读取回归。测试模拟外部写入时的物理回执读取也同步修正，原行为断言保留。旧失败按失败保存，最终结果来自修复后完整检查。

上述结果不把发布前候选的模型/游戏行为改记为0.1.0重新执行。GitHub CI另外显示各次提交的当前仓库检查，仍不等于原生宿主模型或游戏验收。

## 发布前功能基线

截至 2026-10-06，公开版之前的 Windows/Codex 候选已有以下基线：

- 107 项核心回归，以及分发、升级回滚与宿主发现检查。
- 面板浏览器交互与恢复检查；最近实际安装包只读 HTTP 补查为 9 项。
- 原生宿主的未采用项目自然负例、显式职责链和只读状态场景。
- 独立上下文继续原任务的演练，原有 4 项行为检查复跑通过。
- 新、旧两个有界游戏试点的接入、原记录回读和续接。

这些是发布前候选的匿名覆盖摘要，保留其原运行范围，不声称是本轮 v0.1.0 重新执行，也不公开私人项目日志。当前发行检查由实际仓库状态另行完成。

## 适用限制

上述基线不证明所有模型、宿主、操作系统、引擎或旧格式适配都已覆盖；旧会话热加载也未获保证。浏览器与 HTTP 检查不替代用户视觉接受，游戏试点不等于全部项目或长期运行通过。

修改职责触发时补相应自然请求场景；修改面板交互时补浏览器操作证据；修改公共接口或分发时补消费者与安装恢复检查。复用同一代码状态下仍有效的结果，针对实际变更和缺口补查。经验增强未采用，不计入现有功能完成范围。
