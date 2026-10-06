# 许可与第三方声明

Gamecaden自有代码和文档按[MIT](LICENSE)提供，版权归immortalbeating2。MIT声明适用于自有内容；以下第三方组件继续适用其原许可证。

## ELK.js

面板包含未修改的ELK.js 0.12.0，按EPL-2.0分发。

- 原包：[elkjs-0.12.0.tgz](https://registry.npmjs.org/elkjs/-/elkjs-0.12.0.tgz)。
- 项目与源码：[kieler/elkjs](https://github.com/kieler/elkjs)，版本标签v0.12.0；源码与构建说明由该项目提供。
- 原[NOTICE](panels/night/vendor/NOTICE.md)及[EPL全文](panels/night/vendor/ELK-LICENSE.md)随每份分发包保留。

MIT不改变该组件的许可、版权或通知。游戏资产及调用者导入的材料分别由其来源许可约束。

## Python依赖与设计参考

Python依赖由调用者的独立环境安装，见[requirements](scripts/requirements.txt)，不将虚拟环境或依赖包装入分发包。引擎profiles引用官方资料并说明工作流判断；引用文档不表示其上游内容改为MIT。
