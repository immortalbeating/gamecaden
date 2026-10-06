# 安装、升级与回滚

本包是 Gamecaden 0.1.0，自有代码和文档按[MIT](LICENSE)提供；第三方许可见[声明](THIRD_PARTY_NOTICES.md)。技能名称保留 flow / init / brainstorm / design / develop / assets / verify / close，插件宿主使用 Gamecaden 命名空间；实际名称由宿主技能列表回读。工作流记录仍使用已接入项目自己的位置，默认 `game-workflow/`、schema v1。

## 从GitHub安装

```powershell
codex plugin marketplace add immortalbeating2/gamecaden --ref v0.1.0
codex plugin add "gamecaden@gamecaden" --json
```

安装后新开会话，核对实际可用的八个gamecaden职责及版本。安装使技能可被用户级发现；项目通过明确的Gamecaden调用或有效项目指引采用，通常以gamecaden:init完成接入。只调用一次职责不自动迁移整个项目。具体使用见[公开README](https://github.com/immortalbeating2/gamecaden/blob/v0.1.0/README.md)。

## 构建与准备安装源

需要 Python 3.12+。分发工具使用标准库；调用 I/O 或面板再安装 [运行依赖](scripts/requirements.txt)。`$python`、`$bundle`、`$releaseRoot` 和 `$installRoot` 均填写已确认的绝对路径；输出目录必须尚未存在，安装根必须由调用者明确指定。

```powershell
& $python "$bundle/scripts/gamecaden.py" build --source $bundle --output $releaseRoot
& $python "$bundle/scripts/gamecaden.py" verify --package "$releaseRoot/plugins/gamecaden"
& $python "$bundle/scripts/gamecaden.py" stage --package "$releaseRoot/plugins/gamecaden" --target-root $installRoot
```

stage 返回 marketplace_name 与 current.source_path；它只准备安装源，没有执行宿主缓存安装。目录为 `plugins/gamecaden/<内容摘要>`，相同版本只允许相同内容。运行状态不放在插件内。

## 宿主安装与发现

```powershell
codex plugin marketplace add $installRoot
codex plugin add "gamecaden@<stage返回的marketplace_name>" --json
```

Codex 安装的是自己的 cache 副本。用新会话核对八个技能的真实路径与版本；已有会话的列表不证明新包已经加载。候选验证使用独立 `CODEX_HOME`；普通用户安装使用自己的实际环境。源码准备、缓存安装、会话发现和行为续接分别检查。官方入口见 [插件打包与安装](https://developers.openai.com/plugins/build/plugins)。

可用 [check_codex_discovery.py](scripts/check_codex_discovery.py) 对明确的 codex-home / project-root 启动新 app-server，核验八个真实缓存入口与文件摘要。它只检查宿主发现，不发送模型请求，也不证明自然语言续接已经执行。

正文和模板可直接读取。工具/面板需要独立 Python 环境：

```powershell
python -m venv $runtimeRoot
& "$runtimeRoot/Scripts/python.exe" -m pip install -r "$pluginRoot/scripts/requirements.txt"
& "$runtimeRoot/Scripts/python.exe" "$pluginRoot/scripts/check_contracts.py"
```

`$pluginRoot` 是实际安装包根。POSIX 环境使用 `bin/python`。面板配置和连接资料按 [面板合同](panels/README.md) 保存在独立宿主状态目录；本包没有自动安装 MCP 服务。

## 升级与恢复

源码修订后增加 manifest 版本，或在 build 使用 `--version <新版本>` 生成候选。verify 通过后 stage 到同一安装根，再运行上述 Codex 原生安装命令，核对缓存与新会话。

```powershell
& $python "$bundle/scripts/gamecaden.py" status --target-root $installRoot
& $python "$bundle/scripts/gamecaden.py" rollback --target-root $installRoot
& $python "$bundle/scripts/gamecaden.py" recover --target-root $installRoot
```

rollback 切回上一包；首次部署回滚为未部署，旧包保留。回滚后重新刷新宿主安装；首次撤销还需按实际宿主使用 `codex plugin remove`。status 是只读检查；recover 只在未决事务的前/后字节仍匹配时完成原操作。有外部修改时保留材料并报告冲突，不能强制覆盖。

OS 锁协调本工具的进程；外部编辑器不参与该锁。工具检查可观察到的修订变化，最后一次比较至文件替换之间仍有竞争窗口；不承诺网络盘、断电或任意非合作编辑器的多文件事务。

`.gamecaden-install/` 保存安装锁、历史与恢复回执，不保存游戏进度。公共包升级不改写项目设计、记录、采用规则、接受状态或存档。项目接入和旧工作流迁移依据 [init](skills/init/SKILL.md) 的独立范围处理。
