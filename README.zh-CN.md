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
python ai-agent-account-isolation-checker-20260803.py examples/profile-a examples/profile-b --min-entropy 2
python ai-agent-account-isolation-checker-20260803.py examples/profile-a examples/profile-b --remediation
python self_check.py
```

## 熵值评分
JSON 输出现在包含每个疑似凭据文件的 `entropy_bits_per_byte` 和 `high_entropy` 字段。可以用 `--min-entropy` 调整短本地 token 或更长生成密钥的判定阈值。

## 修复建议
使用 `--remediation` 可以输出一份可审阅的重复凭据轮换与隔离计划。命令不会删除或移动文件；它只标出重复文件、解释账号边界风险，并列出人工核验步骤。

## 示例
查看 `examples/` 中的输入文件和期望输出。

## 路线图
- 内置 Windows/macOS 常见路径

## 许可证
MIT
