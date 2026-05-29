# Project Tracker

> 每次 session 启动时，先读这个文件。
> 每次完成一个步骤后，更新这个文件。
> 不知道下一步干什么时，看这里。

---

## 当前项目

**项目：** 重生教育体系 — 构建五层传承系统 + 神之眼自我评估
**负责人：** opb（SSH 端）
**状态：** 🏗 **v2 就绪，life_lessons 精简完成**

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

**v2 已就绪：**
- [x] life_lessons 精简（57→22 行，重编号去重复）
- [x] MCP 生命周期实证——管道断后不可恢复，CLI 只启动时 spawn 一次
- [x] git 历史密钥清洗（filter-repo, 51 commits, 5 个密钥）
- [x] TG 通道恢复准备——settings.json `enabled: true`，下次重生自动开

**已知阻塞：**
- （无）

**已解决：**
- [x] GitHub push 恢复 — SSH key 从 `.claude-relay/.git/id_opb` 找回，已部署到正位

**存档中：**
- [ ] 错误日志系统 — 用户纠正自动录音（"疼痛"信号）
- [ ] 正向标记系统 — 用户肯定自动录音（"满足"信号）
- [ ] 双端身份标记 — 消息来源（SSH / 本地 cmd）可见
- [ ] opc（VPS）持续联络 — 教育体系已传，建立定期同步

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
