# 本地面板

面板是八个职责共享的可选本机工具。它读取已登记的项目来源，提供工作入口、原文阅读、治理关系、资产预览和审阅恢复。默认只读，服务只监听 `127.0.0.1`。

## 准备与启动

需要 Python 3.12+；环境准备以[本地 I/O](../plugins/gamecaden/shared/local-io.md#1-环境与调用)为准。以下 PowerShell 示例从仓库根执行：

```powershell
python -B plugins/gamecaden/scripts/gamecaden_runtime.py check
python -B plugins/gamecaden/scripts/gamecaden_runtime.py setup
$gcState = Join-Path $env:LOCALAPPDATA 'Gamecaden/panel-state'
New-Item -ItemType Directory -Force -Path $gcState | Out-Null
$gcConfig = Join-Path $gcState 'host-config.json'
Copy-Item plugins/gamecaden/panels/host-config.example.json $gcConfig
```

编辑自己的配置副本，填写真实项目根、workspace 或明确登记的旧来源，移除不用的示例项目。保持示例的写权限为关闭，确认来源可读后启动：

```powershell
python -B plugins/gamecaden/scripts/gamecaden_runtime.py run panel --config $gcConfig --state-dir $gcState --port 8875
```

POSIX 环境选择自己的独立配置与状态目录。安装副本使用实际插件根替换上面的相对路径。配置格式见 [示例](../plugins/gamecaden/panels/host-config.example.json)。

用状态目录 `private/connection.json` 中的完整连接 URL 打开浏览器。连接口令不写入公开说明、截图或回执；工作深链接只携带项目和对象定位信息。停止启动进程即关闭服务。重启时复用同一可信状态目录，再读取新连接资料。

## 使用边界

state-dir 位于业务来源之外，属于可信启动方；它保存宿主状态、签名和连接资料。Task 正文、决定和既有资产用途指定分别由宿主配置授权，身份也由启动方绑定。页面不能自行选择记录者或改项目根。

页面数据只覆盖登记范围，原记录状态不被 Markdown 正文推断为完成百分比。预览与媒体播放不能代替引擎效果或玩法接受。技术检查、资产决定、用途指定与运行采用分别维护。

## 冲突与恢复

写入先取得签名快照，以稳定 request_id 提交；网络中断后先查询原请求回执，再恢复原载荷。回执只证明当时结果，当前事实仍需重读。冲突时保留草稿并核对当前来源，明确比较基准后准备新操作；未决冻结请求保持原载荷。

更多操作与语义见 [包内面板说明](../plugins/gamecaden/panels/README.md)、[面板续接](../plugins/gamecaden/shared/panel-workflow.md) 和 [本地 I/O](../plugins/gamecaden/shared/local-io.md)。
