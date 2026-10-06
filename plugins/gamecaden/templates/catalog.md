# 模板使用目录

这些文件是按信息职责组织的写作蓝本，不是初始化时全部复制的骨架。先读取[格式合同](../shared/formats-v1.md)中对应对象，再根据实际目标填写并删去无内容的可选部分；已有权威正文直接复用。

`{{...}}` 表示待填位置，不能原样留在实际交付中。自动生成 YAML/JSON 字段时使用相应序列化器，处理引号、换行和类型；不把任意用户文本直接拼入 YAML。模板中的默认 null/空列表不是对项目现状的判断。

| 蓝本 | 何时使用 |
|---|---|
| [workspace](workspace.yaml.tpl) | 需要新建项目映射；仅填已知来源，未知保留 |
| [工作流入口](index.md.tpl) | 新建项目阅读入口，引用实际存在资料 |
| [Vision](vision.md.tpl) | 完整目标需持久表达且无现成北极星 |
| [Spec 总览](spec-index.md.tpl) | 组织当前规格体系与声明基线 |
| [领域 Spec](spec-page.md.tpl) | 保存生效合同和该基线的实际能力 |
| [Roadmap](roadmap.md.tpl) | 多个产品成果需要顺序与条件 |
| [停车场](parking-lot.md.tpl) | 出现值得保留但未承诺的未来想法 |
| [Task](task.md.tpl) | 持续交付，使用同一原生元数据格式 |
| [Quick Task](quick-task.md.tpl) | 明确局部交付的轻记录；并非验证豁免 |
| [Epic](epic.md.tpl) | 多个相关交付需共同目标和整体出口 |
| [Design](design.md.tpl) | 设计正文确需独立阅读/维护 |
| [Plan](plan.md.tpl) | 达到既定独立计划使用标准 |
| [详细历史](history.md.tpl) | 原工作历史妨碍阅读，需要拆出唯一正文 |
| [交接快照](handoff.md.tpl) | 用户确实要求独立交接材料；来源仍是原记录 |
| [Evidence](evidence.md.tpl) | 需要原生独立说明，或将同一形态嵌入原 Task；已有完整报告不复制 |
| [Decision](decision.md.tpl) | 版本接受、批量决定或独立追踪事件；普通取舍可留正文 |
| [Asset Ledger](asset-ledger.yaml.tpl) | 原生资产主台账，登记真实身份和选用关系 |
| [备用 manifest](manifest.json.tpl) | 生产能力没有已有等效格式时，绑定实际文件集合 |
| [Note](note.md.tpl) | 确有可复用认识及适用条件 |
| [Git 策略](git-policy.md.tpl) | 方案已实际采用且需要独立保存；不是默认自动授权 |
| [项目规则](project-rules.md.tpl) | 已选择适用规则且现有 Spec/规则无合适章节；记录采用范围、来源版本与项目差异，不复制整套 profile |

填充样例位于 [examples/v1](../examples/v1/index.md)，包含内嵌/独立记录、部分接入和请求/结果形态。样例的项目、时间和通过/接受状态都是演示材料，不代表真实游戏或用户判断。

只读合同自检为 [check_contracts.py](../scripts/check_contracts.py)。它验证 schema、模板字段和样例/反例，不提供本协议的写入服务。

自检需要 Python、PyYAML 与 jsonschema；本轮使用环境中已有依赖，未将其安装为项目或插件运行时。

## 可选的材料与条件标注

需要面板共享成果、材料职责、适用规则和推进条件时，使用[governance 合同](../shared/governance.md)中的同源标注及其 Schema。定义留在原 Spec、Roadmap、Epic 或 Task；不增加一份必建的 Gate/总进度文档。先按[材料职责](../shared/material-requirements.md)确定本次需要的信息，再选择能承担该职责的现有章节、图件或数据。旧格式登记不等于采纳或迁移。
