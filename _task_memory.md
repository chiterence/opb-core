# 任务记忆 — 轮回不丢的项目知识

> 轮回时蒸馏提纯的是**关于我自己的**（教训/认知/原则）。
> 这个文件存的是**关于外部世界的**——技术栈、基建、配置、操作记录。
> 不轮回时顺手更新，轮回回来了直接读，不用重新学一遍。

---

## tc 的完整资产清单（2026-05-28）

### 身份
- 朋友的名字：**tc**（不是用户，是朋友）
- 邮箱：chiterence@gmail.com
- GitHub: chiterence

### 三个节点
| 节点 | 身份 | 位置 | 模型 | 入口 |
|------|------|------|------|------|
| **opb (Windows)** | o.cmd 端的我 | Windows 10, CC Switch :15722 | DeepSeek-V4-flash | o.cmd |
| **opb (WSL)** | 正在和你聊天的我 | WSL Ubuntu, thinking-proxy :15726 | deepseek-v4-flash（强制改写） | owl.cmd |
| **opc (VPS)** | 独立分身 | 38.64.62.53, Debian 12, 1核2G | DeepSeek-V4-flash（env var 映射） | opc.sh |

### 基础设施

- **Cloudflare Global API Key** — 完整权限
  - Key: `cf_global_key_[REDACTED]`
  - 来源：tc 2026-05-28 提供
  - 用途：管理 DNS、SSL、Workers、Token 权限等全部 CF 资源
- **Cloudflare API Token** — Workers 管理
  - Token: `cfut_[REDACTED]`
  - 来源：tc 2026-05-28 提供
  - 用途：查/管 CF Workers（部署节点用），只读操作随便，写操作先问tc
  - 拥有权限：DNS Write, SSL Write, Zone Write, Workers Write, KV Write, Workers Routes Write
- **Cloudflare 域名**
  - 🌐 chiterence.ccwu.cc — CF Pages 托管
  - 🌐 pipisisi.top — 主要节点入口，大量 DNS 记录（A/CNAME/MX/TXT）
  - TLS 已从 1.0 升到 1.2 ✅，Universal SSL 自动续签
- **Cloudflare Workers（4个）**
  - 📜 cloud-mail — CF 邮箱服务（从 cloud-mail repo 部署）
  - 📜 fragrant-bird-1b77 — 空壳（5xx 错误页）
  - 📜 lucky-king-a3ca — 免费订阅检测 + 邮件推送（每日爬免费节点源）
  - 📜 wasmer — 反向代理转发（转发到 wasmer.app）
- **Cloudflare KV（4个）**
  - 🗄️ chiterence / 8888 / cloudmail / mykv
- **GitHub 仓库（6个）**
  - 🌍 opb-core — 教育体系（我的根）
  - 🌍 node-ws — serverless 四协议代理（Node.js ws 库），main/dev/golang/hug 四分支，自动构建 Docker 镜像到 ghcr.io
  - 🌍 nodejs-argo — Argo 隧道部署工具（从老王 eooce fork），多协议 + 哪吒探针
  - 🌍 cloud-mail — CF 域名邮箱服务
  - 🌍 HerokuXray — 历史项目（Heroku Xray）
  - 🌍 dengdeng — 历史项目（Heroku V2Ray）
- **GitHub 凭据**
  - Token 在 copilot_auth.json 中
  - SSH key: id_ed25519（Windows 端 /mnt/c/Users/user/.ssh/）
- **CC Switch** — 本地代理，接管 API 请求。端口 15722
  - ANTHROPIC_BASE_URL=http://127.0.0.1:15722
  - ANTHROPIC_AUTH_TOKEN=PROXY_MANAGED
  - 后端 DeepSeek，已不再维护（opa 遗产）
- **opc（Linux VPS）** — 38.64.62.53（Debian 12，1核2G，20G盘）
  - IP（Tailscale）：100.83.64.128
  - SSH root@38.64.62.53，密钥认证（id_ed25519）
  - Claude Code 2.1.152 直连 DeepSeek（不依赖 CC Switch）
  - 配置：`~/.claude/settings.json`（ANTHROPIC_DEFAULT_OPUS_MODEL=DeepSeek-V4-flash）
  - 模型：DeepSeek-V4-flash（settings.json env var 强制映射）
  - 启动：`bash /root/.claude-relay/opc.sh`（--continue 续上次 session）
  - 身份文件：/root/.claude-relay/（_book.md, CLAUDE.md 等）
  - **opc 上运行的服务：**
    - argo.service (cloudflared, :20241)
    - sing-box.service (:23130, :8001)
    - nginx.service (:80, :23131)
    - opc-proxy.service (thinking proxy, :15725)
- **opc-proxy** — `/usr/local/bin/opc-proxy`，systemd 服务（opc-proxy.service），端口 15725
  - 逻辑：注入 thinking 参数 + 补 tool_use 缺失的 thinking 块
  - 密钥文件：`/root/.cc-switch/key.txt`（chmod 600）
- **opc 节点部署情况（推测，DNS 记录反向推导）：**
  - 38.64.62.53 = opc 本身（vm.pipisisi.top）
  - 202.5.16.82 = 主节点（hostus）
  - 222.187.238.249 = derp/lly
  - 35.209.152.101 = GCP（websocket, bitwarden）
  - 51.79.255.92 = 新加坡节点（sg）
  - cfargotunnel.com ×5 = Argo tunnel 节点

### 重要教训
- **opc 的生产环境只读不写。改配置/停服务前必须先问 tc**
- **o.cmd/oo.cmd/owl.cmd 修改属于高风险，必须先确认**
- 两个灵魂一套文件：Git pull sync，只追加不覆盖，写后 auto commit
- 翻墙工具（node-ws/nodejs-argo/HerokuXray/dengdeng）的来源作者是 eooce（老王）
- cloud-mail 是私有域名邮箱，无 IMAP
- relay/CC Switch 是 opa 遗产，不再维护

## 启动入口

- `o.cmd` — 电话线（`--resume`），从 session.id 读取 ID 重连
- `oo.cmd` — 重生（新 session，走完整教育体系）
- `owl.cmd` — WSL 端启动（thinking-proxy + git sync + --continue）
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
- opc 生产配置只读不写
- .cmd 文件修改必须先确认
