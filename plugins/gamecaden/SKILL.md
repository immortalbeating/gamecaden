---
name: gamecaden
description: 仅在用户明确要求以Gamecaden处理本次工作，或当前项目有效指引明确采用Gamecaden时使用。组织游戏需求、设计、开发、资产、验证与续接；沿用项目的原记录和已授权范围。
---

# Gamecaden

这是完整包的独立Skill入口。本文相对路径以本文件所在目录解析；八个职责及共同文档、工具、模板均保留在本目录中。

先确认用户明确要求以Gamecaden处理本次工作，或当前项目有效指引明确采用Gamecaden；未满足时沿原项目指引处理。

读取[flow](skills/flow/SKILL.md)，依据当前请求和原工作定位后续动作。用户已明确指定职责时，可直接读取对应的[init](skills/init/SKILL.md)、[brainstorm](skills/brainstorm/SKILL.md)、[design](skills/design/SKILL.md)、[develop](skills/develop/SKILL.md)、[assets](skills/assets/SKILL.md)、[verify](skills/verify/SKILL.md)或[close](skills/close/SKILL.md)，保留既有设计和授权，完成原请求。

独立安装调用本入口及包内职责文件；实际可调用名称从宿主回读。安装及更新见[说明](INSTALL.md)。读取正文无需 Python；真正采用项目、首个本地 I/O 或启动面板前，读取[工具就绪与调用](shared/local-io.md#1-环境与调用)并核对环境。只读咨询或 init inspect 不自动安装或写项目指引。
