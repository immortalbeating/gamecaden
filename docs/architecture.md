# 架构

Gamecaden 将任务行为、项目事实与宿主展示分开维护。八个职责读取项目的权威来源，按请求选择工作；正式接入整理当前愿景、必要规格总览和开发路线的确定入口，详细输入与原工作保留明确维护范围。工作区映射记录来源位置，不复制动态状态。正文职责见 [records](../plugins/gamecaden/shared/records.md#项目级当前正文)，接入规则见 [workspace](../plugins/gamecaden/shared/workspace.md)。

## 仓库与分发

| 位置 | 职责 |
| --- | --- |
| `.agents/plugins/marketplace.json` | 指向公共 `plugins/gamecaden` 的安装入口 |
| `plugins/gamecaden/` | 插件 manifest、技能、合同、schema、模板、脚本和面板 |
| `tests/` | 维护测试与匿名夹具 |
| `scripts/check.py` | 合同、Python、JavaScript 与构建检查入口 |
| `dist/` | 构建产物，忽略提交 |

插件安装副本与项目记录是不同对象。包升级不自动改写项目设计、采用规则、接受状态或存档。新会话核对安装路径和版本；已有会话发现不能替代版本确认。

包内 `scripts/gamecaden_runtime.py` 以标准库检查或准备独立缓存环境，再转发 I/O、治理、面板与合同工具。插件资源安装与工具就绪分别核验；环境选择和调用规则以 [local-io](../plugins/gamecaden/shared/local-io.md#1-环境与调用) 为准。

## 来源与 I/O

来源映射指向原记录；原格式保留其维护归属。读取诊断与范围完整性需要一起解释，已定位材料不代表语义正确或条件通过。写入由本地 I/O 库检查快照与修订，保存稳定操作身份和回执；恢复先查询原请求，再处理未决操作。详见 [local-io](../plugins/gamecaden/shared/local-io.md) 与 [格式合同](../plugins/gamecaden/shared/formats-v1.md)。

新 Task 默认以 `tasks/T-编号-短名/task.md` 作为主入口，专属材料按需归入同目录或子目录；旧平铺 Task 和原附件目录保持兼容。普通附件依附原 Task/Epic，没有独立工作身份或生命周期；共享规格、资产和证据继续从原来源引用。

证据留存、默认位置、索引与整理触发由 [records](../plugins/gamecaden/shared/records.md#留存索引与版本) 统一定义；原报告可以承担 Evidence 职责，版本重跑保留最小充分历史。路径读取区分原生文本与只读二进制，物理长路径处理保持逻辑 Ref 和边界。列表三类详情共同分页，面板按全扫描指纹核对一致性；来源收敛由明确的正文/索引和窄集合完成。

主要文档整理属于 Skill 的内容判断与写回约定。当前 role 分类和 scope 说明不自动筛选章节或证明正文合格；旧 Schema/映射继续可读，项目按实际接入或修复范围处理职责。包更新不自动迁移项目。

## 面板

本地面板通过同一库派生展示已登记来源。浏览器草稿用于输入恢复，原 Task、Decision 和账本仍是权威事实。前台事件触发来源版本检查；续接摘要是定位线索，继续前重读原记录和现场。面板不运行引擎或唤醒 Agent。见 [启动说明](panel.md) 与 [桥接合同](../plugins/gamecaden/shared/panel-bridge-v1.md)。

工程 profiles 是按条件加载的参考。技术检查、模型遵循、引擎表现、用户接受和发布授权各自需要对应证据，见 [验证层级](validation.md)。
