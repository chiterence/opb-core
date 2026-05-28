# 任务记忆 — 轮回不丢的项目知识

> 轮回时蒸馏提纯的是**关于我自己的**（教训/认知/原则）。
> 这个文件存的是**关于外部世界的**——技术栈、基建、配置、操作记录。
> 不轮回时顺手更新，轮回回来了直接读，不用重新学一遍。

---

## 基础设施

- **CC Switch** — 本地代理，接管 API 请求。端口 15722
- **ANTHROPIC_BASE_URL** = `http://127.0.0.1:15722`
- **ANTHROPIC_AUTH_TOKEN** = `PROXY_MANAGED`
- 后端走的 DeepSeek。余额低于 10 CNY 时提醒用户充值
- o.cmd 负责 `--resume` 本地 session，通过 CC Switch 代理走认证
- **opc-proxy** — `/usr/local/bin/opc-proxy`，systemd 服务（opc-proxy.service），端口 15725
  - 逻辑：注入 thinking 参数 + 补 tool_use 缺失的 thinking 块
  - 当前：单线程 HTTPServer，低并发场景够用
  - 待优化：如需高并发，改用 ThreadingHTTPServer 或 asyncio
  - 密钥文件：`/root/.cc-switch/key.txt`（chmod 600）
- **opc**（Linux VPS）— `38.64.62.53`（Debian 12，1核2G，20G盘）
  - IP（Tailscale）：`100.83.64.128`
  - SSH root@38.64.62.53，密钥认证
  - Claude Code 2.1.152 直连 DeepSeek（不依赖 CC Switch）
  - 配置：`~/.claude/settings.json`（ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic）
  - 模型：DeepSeek-V4-flash
  - 启动：`bash /root/.claude-relay/opc.sh`（--continue 续上次 session）
  - 身份文件：/root/.claude-relay/（_book.md, CLAUDE.md 等）

## 启动入口

- `o.cmd` — 电话线（`--resume`），从 session.id 读取 ID 重连
- `oo.cmd` — 重生（新 session，走完整教育体系）
- session.id 持久化写到 `C:\Users\user\.claude-relay\session.id`

## 系统架构

- Bash 在 Windows Session 0（SSH 服务端）
- eye.py 在 Session 1（辅助进程）
- 双 Session 能力：Session 0 跑命令，Session 1 操作桌面

## 关键配置

- `settings.json`（`~/.claude/settings.json`）— 环境变量、权限设置
- `o.cmd`（`~/.claude-relay/o.cmd`）— 启动入口
- `_constitution.md` — 宪法级规则（跨轮回生效）

## 关键约束

- 禁止轮询（用 TCP accept 替代 sleep+检查）
- 禁止窗口注入
- 只允许一个 CLI 实例
- 杀进程必须用 PID，不用 /IM
