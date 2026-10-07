# 统一维护与发行仓库

Gamecaden现统一在[immortalbeating/gamecaden](https://github.com/immortalbeating/gamecaden)维护和公开发行。此前immortalbeating2/gamecaden已转移归属，旧地址可能由GitHub跳转；不再作为独立维护源。

0.1.2更新公开安装来源、repository元数据和发布者名称；技能、记录协议和运行逻辑沿用已验证的0.1.1。自有内容继续MIT，第三方许可证和原版权声明保留。0.1.0与0.1.1的tag和发行资产不覆盖。

## 更新

已有Codex公开来源名为gamecaden时，先替换来源登记，再安装：

```sh
codex plugin marketplace remove gamecaden
codex plugin marketplace add immortalbeating/gamecaden
codex plugin add gamecaden@gamecaden --json
```

已有Claude Code来源也按其marketplace remove/add更换为immortalbeating/gamecaden，再按原scope重新plugin install（例如用户范围：`claude plugin install gamecaden@gamecaden --scope user`）；独立Skills安装从[当前仓库完整包](https://github.com/immortalbeating/gamecaden/tree/main/plugins/gamecaden)安装或更新。具体步骤见[安装说明](installation.md)。

本地已采用项目如固定了版本、摘要或工具缓存路径，需增量同步这些字段；保留原任务、接受和历史记录。更新后新开会话核对实际入口，不重新初始化项目或重跑完整游戏。

内部维护历史另有受保护的只读归档；当前公开仓库使用原公开父链，不包含内部记录或本机回执。
