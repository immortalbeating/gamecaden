# 维护入口

本仓库维护 Gamecaden 工具包。先读取 [README](README.md) 和当前任务范围，保留已有工作树修改，仅修改本次负责的文件。

- 修改职责或触发规则时，读取对应 `plugins/gamecaden/skills/*/SKILL.md` 和其引用的 `shared/` 合同；详细行为以包内合同为准。
- 修改来源、I/O 或面板时，读取 [架构](docs/architecture.md) 与对应共享合同，保持原来源权威、修订检查和恢复语义。
- 根 `tests/`、`scripts/` 是维护入口；`plugins/gamecaden/` 是公共插件，`dist/` 是构建产物。
- 按影响运行 `python scripts/check.py --suite core` 或 `--suite distribution`；发行前运行 `--suite all`。检查方式见 [验证说明](docs/validation.md)。
- 报告实际执行命令、结果及未验证部分。程序检查、模型行为、运行采用和用户接受分别说明。
- 公共材料仅使用匿名示例；连接凭据、本机路径、私有日志和业务项目资料留在公共包外。

维护本工具包不自动授权运行游戏、修改外部项目、提交、推送或发布。
