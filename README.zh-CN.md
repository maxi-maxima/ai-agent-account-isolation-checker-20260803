# AI Agent 账号隔离检查器

## 解决的痛点
开发者会在多个 Agent 账号/配置间切换，误共享 token 或 session 文件会破坏隔离。

## 为什么现在值得做
CLI 编程 Agent 与账号切换工具升温，本地配置卫生变得更重要。

## 安装 / 运行
需要 Python 3.9+，无第三方依赖。

```bash
python *.py --help
python ai-agent-account-isolation-checker-20260803.py examples/profile-a examples/profile-b --json
python self_check.py
```

## 示例
查看 `examples/` 中的输入文件和期望输出。

## 路线图
- 内置 Windows/macOS 常见路径
- 熵值评分
- 生成修复脚本

## 许可证
MIT
