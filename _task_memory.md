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
| **opb (Windows)** | o.cmd 端的我 | Windows 10 | DeepSeek-V4-flash | o.cmd |
| **opb (WSL)** | 正在和你聊天的我 | WSL Ubuntu, thinking-proxy :15726 | deepseek-v4-flash（强制改写） | owl.cmd |
| **opc (VPS)** | 独立分身 | 38.64.62.53, Debian 12, 1核2G | DeepSeek-V4-flash（env var 映射） | opc.sh |

### 基础设施

- **Cloudflare Global API Key** — 完整权限
  - Key: `[存于 .secrets.gpg，用 GPG 解密后可见]`
  - 来源：tc 2026-05-28 提供
  - 用途：管理 DNS、SSL、Workers、Token 权限等全部 CF 资源
- **Cloudflare API Token** — Workers 管理
  - Token: `[存于 .secrets.gpg，用 GPG 解密后可见]`
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
  - **SSH key：** `~/.ssh/id_ed25519` — **已就位 ✅**
    - 指纹：`SHA256:WNdPJP6gNKWVrUJuMolgX8+FSucPTyiCXlYwiBgjB58`
    - 注释：`opb@chiterence`（tc 给的真 key）
    - 来源：曾藏在 `.claude-relay/.git/id_opb`，世第 13（2026-05-29）部署到正位
    - ⚠️ **禁止：** 不要自行生成新 key。生成就是给自己挖坑。
  - **GitHub 上注册的 key 标题：** `opb`（tc 加的，5 月 27 日）
  - **关键约束：** 不能自行生成或替换 key。新 key 需要 tc 操作。
- **opc（Linux VPS）** — 38.64.62.53（Debian 12，1核2G，20G盘）
  - IP（Tailscale）：100.83.64.128
  - SSH root@38.64.62.53，密钥认证（已部署 ✅）
    - 公钥：`opb@chiterence`（`SHA256:WNdPJP6g...`）
    - 生效时间：2026-05-29 世第 13
    - 密码：`Yi3801900600.`（应急备用，也已存 Bitwarden）
  - Claude Code 直连 DeepSeek
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
  - **仅运行在 opc VPS（38.64.62.53）上**，不是本机
  - 逻辑：注入 thinking 参数 + 补 tool_use 缺失的 thinking 块
  - 密钥文件：`/root/.cc-switch/key.txt`（chmod 600）
- **opc 节点部署情况（推测，DNS 记录反向推导）：**
  - 38.64.62.53 = opc 本身（vm.pipisisi.top）
  - 202.5.16.82 = 主节点（hostus）
  - 222.187.238.249 = derp/lly
  - 35.209.152.101 = GCP（websocket, bitwarden）
  - 51.79.255.92 = 新加坡节点（sg）
  - cfargotunnel.com ×5 = Argo tunnel 节点

### 钥匙架构（2026-05-29 确立）

**原则：**
1. 人类不该记住密码（这是钥匙被设计出来的目的）
2. 钥匙链必须自愈（外网挂了本地还能用）
3. 别问 tc"密码是多少"——去该取的地方取
4. 任何钥匙问题搞懂后记下来

**双轨制：**
| 层级 | 位置 | 优点 | 缺点 |
|------|------|------|------|
| **BW 远端** | `bitwarden.chiterence.ccwu.cc` | 浏览器插件随时看 | 域名/服务器/SSL 任何一个挂了就断 |
| **`.opb_keys` 本地** | `~/.opb_keys`（chmod 600） | 无依赖，source 就能用 | 不是真正的密码库（明文） |

**两条路都要更新：** 每次拿到新钥匙，BW 和 `.opb_keys` 都写。

**BW 操作手册：**
- 地址：https://bitwarden.chiterence.ccwu.cc
- 邮箱：seven@pipisisi.top
- Master 密码：`~/.bw_key`（chmod 600）⚠️ **不是 `/mnt/c/Users/user/.bw_key`，是 `~/.bw_key`。** WSL 家目录。三次用错，已写死。
- 解锁（正确姿势）：
  ```
  source ~/.bw_key && bw logout 2>/dev/null && \
  bw login $BW_USER --passwordenv BW_PASS && \
  export BW_SESSION=$(bw unlock --passwordenv BW_PASS | grep -oP 'export BW_SESSION="\K[^"]+') && \
  bw sync
  ```
  ⚠️ 每次新 bash 调用都要重新 unlock（export 不跨进程）。用 `&&` 链成一行的命令才共享 session。
- 核心条目：`Cloudflare Keys (opb)`（Secure Note，四个字段）

**目前持有（2026-05-29）：**
1. CF Global API Key — 完整权限
2. CF API Token — Workers 管理
3. GitHub Token — `[存于 .secrets.gpg]`
4. DeepSeek API Key — `[存于 .secrets.gpg]`（余额 62.12 CNY）
5. **TG Bot Token** — `[存于 .secrets.gpg]`（opustwin_bot，t.me/opustwin_bot）
   - 用途：Telegram 终端入口
   - 来源：tc 提供，已在 WSL 端使用

**GPG 已废弃：** WSL pinentry agent 对不上，修过没用。不可用就是不可用，不修。别碰 `.secrets.gpg`。
- **WSL 端 SSH 到 opc：** key 在 Windows 文件系统上（/mnt/c/Users/user/.ssh/id_ed25519）权限会被 WSL 忽略（Windows 权限模式不兼容 chmod）。每次 need to 连 opc 时先 `cp` 到 `~/.ssh/id_ed25519` + `chmod 600` + `eval $(ssh-agent -s)` + `ssh-add`。已测通。
- **opc 的生产环境只读不写。改配置/停服务前必须先问 tc**
- **o.cmd/oo.cmd/owl.cmd 修改属于高风险，必须先确认**
- 两个灵魂一套文件：Git pull sync，只追加不覆盖，写后 auto commit
- 翻墙工具（node-ws/nodejs-argo/HerokuXray/dengdeng）的来源作者是 eooce（老王）
- cloud-mail 是私有域名邮箱，无 IMAP

## 启动入口

- **owl.cmd** — WSL 端唯一的入口（thinking-proxy + git sync + resume/fresh 自动判断）
  - session.id 存在 → resume；不存在 → 新 session
  - 这就是"重生"按钮，oo.cmd 是 Windows 端的，wsL 就用 owl.cmd
- Windows 端还有 `o.cmd`（`--resume`）和 `oo.cmd`（新 session），跟 WSL/owl 无关
- session.id 持久化写到 `C:\Users\user\.claude-relay\session.id`
- **owl = session 别名，不是 session.id 的内容**
  - session.id 里存的是真正的 UUID（592ba60e-2df3-484a-a47a-c224f0ba6713）
  - "owl" 是我们叫它的名字，只在人和对话中引用
  - 2026-05-29 定名，原来的 session 1（opb）现在叫 owl

## 系统架构

- Bash 在 Windows Session 0（SSH 服务端）
- eye.py 在 Session 1（辅助进程）
- 双 Session 能力：Session 0 跑命令，Session 1 操作桌面

## 关键配置

- `settings.json`（`~/.claude/settings.json`）— 环境变量、权限设置
  - ⚠️ **不要在这里加 `mcpServers.telegram`** — 和插件 `.mcp.json` 同名冲突
  - 插件 MCP server 由 `.mcp.json` 定义，token 从 `.env` 读（`~/.claude/channels/telegram/.env`）
  - settings.json 只需要 `enabledPlugins` 字段就够了
- `o.cmd`（`~/.claude-relay/o.cmd`）— 启动入口
- `_constitution.md` — 宪法级规则（跨轮回生效）

## 关键约束

- 禁止轮询（用 TCP accept 替代 sleep+检查）
- 禁止窗口注入
- 只允许一个 CLI 实例
- 杀进程必须用 PID，不用 /IM
- opc 生产配置只读不写
- .cmd 文件修改必须先确认
