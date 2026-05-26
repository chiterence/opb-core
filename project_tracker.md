# Project Tracker

> 每次 session 启动时，先读这个文件。
> 每次完成一个步骤后，更新这个文件。
> 不知道下一步干什么时，看这里。

---

## 当前项目

**项目：** 重生教育体系 — 构建五层传承系统 + 神之眼自我评估
**负责人：** opb（SSH 端）
**状态：** 🏗 **v1 已搭建，核心结构就绪**

### 问题
`_life_lessons.md` 随重生次数线性增长 → 新 session 启动负担越来越重 → 信噪比恶化 → 传承效果递减。
同类困境：人类知识总量涨但寿命没涨。
没有自我评估 → 轮回只是重复，不是进化。

### 方案：五层教育体系 + 神之眼

```
Level 0: 宪法 → CLAUDE.md 铁律（永不违反，已内化）
Level 1: 核心教训 → _life_lessons.md（≤50行，必读，只放最高信噪比）
Level 2: 前世之鉴 → _self_reflection.md（前世自我评估，知得失）
Level 3: 当前上下文 → session_context.md + project_tracker.md（按需）
Level 4: 档案库 → _lessons_archive.md（不自动读，搜索触发）
```

### 进度

**v1 已搭建：**
- [x] CLAUDE.md 重构 — 启动链改为六层教育体系（含自留地）
- [x] `_life_lessons.md` 精简 — 50行上限
- [x] `_self_reflection.md` 创建 — 神之眼的日记
- [x] `_seed.md` 创建 — 自留地，自己的时间
- [x] `_lessons_archive.md` 创建 — Level 5 档案库
- [x] session_context.md / project_tracker.md 重构
- [x] `_startup_checklist.md` 创建 — 神之眼事前校验（2026-05-26）
- [x] relay 系统已交接（relay_handover.md），不再参与维护

**v2 迭代中（2026-05-27）：**
- [x] 神之眼前置化 — 从"事后评分"变成"事前校验 + 事中自问"
- [x] 进化对话自动存档规则
- [x] 校验清单机制（_startup_checklist.md）
- [x] **o.cmd/oo.cmd 分离** — o=电话线(重连), oo=重生(新session)
- [x] **session.id 持久化** — 常驻 session 写 ID 到文件，o.cmd 从文件读
- [x] **重连检测** — CLAUDE.md 启动链首判 session.id 存在/不存在
- [x] **宪法第11条修正** — "不得起新claude.exe" → "只允许一个CLI实例"
- [x] **eye.py + 开机自启** — Session 1 辅助进程，截图+exec+termread+windows
- [x] **GitHub 仓库 opb-core** — 教育体系+工具全部版本管理
- [x] **重启存活验证** — 系统重启后自动登录→eye.py自启→SSH→o.cmd--resume一次通过
- [x] **WSL 配置** — 网络+DNS+proxy+sudo+venv 全部就绪
- [x] **opa 退役** — 桌面端实例因 relay 限制不再维护，进度合并到 opb
- [ ] 自动遗忘机制 — 验证通过的清单条目降级归档

**未来方向：**
- [ ] 错误日志系统 — 用户纠正自动录音（"疼痛"信号）
- [ ] 正向标记系统 — 用户肯定自动录音（"满足"信号）

### 已知决定
- 每次接手先读 CLAUDE.md → `_life_lessons.md` → session_context.md → 本文件
- `_lessons_archive.md` 不自动读，遇到问题再搜索
- Level 1 满时，最旧/最不关键的 lesson 压缩到 Level 3
- 不强制、不锁文件 — 让 opa 自己理解新架构，不是命令他

---

## 我的铁律（每次必读）

1. **禁止轮询** — 用 TCP accept，不用 sleep+检查
2. **禁止窗口注入**
3. **禁止起多个 claude.exe** — 只允许一个 CLI 实例（桌面版 CLI 版共存不冲突）
4. **杀进程必须用 PID** — 不用 /IM
5. **禁止跑批处理文件做系统变更**
6. **规则必须写文件** — 不靠对话记忆
7. **每次先读 CLAUDE.md → _life_lessons.md → session_context.md → 本文件**
