# 贡献指南

先通过 Issue 说明具体问题、复现步骤和期望行为。小修复可直接提交 Pull Request；涉及记录格式、公共接口或职责边界的改动，先说明消费者、兼容方案及验证条件。

## 本地检查

需要 Python 3.12+ 和 Node.js。面板与 I/O 的额外依赖使用独立虚拟环境：

```sh
python -m venv .venv
```

Windows 使用 `.venv/Scripts/python.exe`，POSIX 使用 `.venv/bin/python`；用该解释器安装 `plugins/gamecaden/scripts/requirements.txt`。从仓库根运行：

```sh
python scripts/check.py --suite all
```

按改动影响选择较小检查集见 [验证说明](docs/validation.md)。保存命令、环境与结果，说明无法执行的检查；发行前仍需完整检查。

## 提交内容

- 保持公共插件与维护测试分离：插件在 `plugins/gamecaden/`，测试在 `tests/`，维护入口在 `scripts/`。
- 变更说明写清问题、最终行为、兼容影响和实际验证；有关合同随实现同步。
- 使用匿名夹具，不提交连接资料、真实项目记录或机器专属路径。
- 保留第三方许可和出处。不要将测试通过写成用户接受或运行采用。

项目采用 [MIT](LICENSE)。贡献应具有可用于该许可的权利；第三方材料保留自己的许可说明。
