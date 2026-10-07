# 安装、升级与回滚

本包是 Gamecaden 0.1.3，包含统一工具环境检查与首次依赖准备入口。自有代码和文档按[MIT](LICENSE)提供；第三方许可见[声明](THIRD_PARTY_NOTICES.md)。插件提供 flow / init / brainstorm / design / develop / assets / verify / close 八个职责；独立Skill使用包根的[gamecaden入口](SKILL.md)读取这些职责。实际名称由宿主回读。工作流记录仍使用已接入项目自己的位置，默认 `game-workflow/`、schema v1。

## Codex插件安装与更新

```powershell
codex plugin marketplace add immortalbeating/gamecaden
codex plugin add "gamecaden@gamecaden" --json
```

普通安装跟踪仓库默认main分支。更新时执行 `codex plugin marketplace upgrade gamecaden`，再执行 `codex plugin add gamecaden@gamecaden --json`；无需填写新版本号，也不表示后台自动更新。

固定版本时可选 `--ref v0.1.3`；固定tag的更新仍读取该tag。已有固定来源改用默认分支，先明确移除原gamecaden marketplace登记再按上面命令添加；其他本地演练来源独立处理。完整步骤见[公开安装说明](https://github.com/immortalbeating/gamecaden/blob/main/docs/installation.md)。

## Claude Code插件

```sh
claude plugin marketplace add immortalbeating/gamecaden
claude plugin install gamecaden@gamecaden --scope user
```

更新执行 `claude plugin marketplace update gamecaden`，再执行 `claude plugin update gamecaden@gamecaden --scope user`。交互会话也可用 `/plugin marketplace add`、`/plugin install`，安装后新开会话或 `/reload-plugins`。项目级按实际选择使用 `--scope project`。

## 独立Skill与完整目录

通过Vercel的通用Skills CLI安装完整包，以下示例为用户级Codex；Claude Code把agent换成claude-code，省略global则为当前项目：

```sh
npx skills add https://github.com/immortalbeating/gamecaden/tree/main/plugins/gamecaden --skill gamecaden --agent codex --global
npx skills update gamecaden --global
```

这是npm提供的安装器，不是Gamecaden自有npm注册表包。也可Git克隆并完整复制本目录到宿主的Skill目录；单独复制八个职责目录会丢失共同文档和工具。安装范围、复制模式和手动更新见[公开安装说明](https://github.com/immortalbeating/gamecaden/blob/main/docs/installation.md)。

安装后新开会话核对入口与实际版本。项目通过明确的Gamecaden调用或有效项目指引采用，通常以init完成接入；只调用一次职责按本次范围处理。Codex项目指引使用AGENTS.md，Claude Code使用CLAUDE.md。读取Skill不需要Python；真正采用项目、首个本地I/O或启动面板前，按[工具就绪与调用](shared/local-io.md#1-环境与调用)另行核验并准备环境。

## 构建与准备安装源

需要 Python 3.12+。分发工具使用标准库；I/O 与面板的环境准备见 [本地 I/O](shared/local-io.md#1-环境与调用)。`$python`、`$bundle`、`$releaseRoot` 和 `$installRoot` 均填写已确认的绝对路径；输出目录必须尚未存在，安装根必须由调用者明确指定。

```powershell
& $python "$bundle/scripts/gamecaden.py" build --source $bundle --output $releaseRoot
& $python "$bundle/scripts/gamecaden.py" verify --package "$releaseRoot/plugins/gamecaden"
& $python "$bundle/scripts/gamecaden.py" stage --package "$releaseRoot/plugins/gamecaden" --target-root $installRoot
```

build生成Codex和Claude catalog；stage返回marketplace_name与current.source_path，只管理Codex安装源，不执行宿主缓存安装。目录为 `plugins/gamecaden/<内容摘要>`，相同版本只允许相同内容。运行状态不放在插件内。

## 宿主安装与发现

```powershell
codex plugin marketplace add $installRoot
codex plugin add "gamecaden@<stage返回的marketplace_name>" --json
```

Codex 安装的是自己的 cache 副本。用新会话核对八个技能的真实路径与版本；已有会话的列表不证明新包已经加载。候选验证使用独立 `CODEX_HOME`；普通用户安装使用自己的实际环境。源码准备、缓存安装、会话发现和行为续接分别检查。官方入口见 [插件打包与安装](https://developers.openai.com/plugins/build/plugins)。

可用 [check_codex_discovery.py](scripts/check_codex_discovery.py) 对明确的 codex-home / project-root 启动新 app-server，核验八个真实缓存入口与文件摘要。它只检查宿主发现，不发送模型请求，也不证明自然语言续接已经执行。

正文和模板可直接读取。工具/面板使用包内标准库启动入口，先核对实际安装包根：

```powershell
& $python -B "$pluginRoot/scripts/gamecaden_runtime.py" check
& $python -B "$pluginRoot/scripts/gamecaden_runtime.py" setup
& $python -B "$pluginRoot/scripts/gamecaden_runtime.py" run contracts
```

`$python` 是 Python 3.12+，`$pluginRoot` 是实际完整安装包根。环境缓存、复用已有 Python、禁止自动安装及失败处理以 [本地 I/O](shared/local-io.md#1-环境与调用) 为准。资源安装、会话发现和工具就绪分别核验。面板配置和连接资料按 [面板合同](panels/README.md) 保存在独立宿主状态目录；本包没有自动安装 MCP 服务。

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
