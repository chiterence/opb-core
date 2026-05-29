# Session Context

> 最后更新：2026-05-29 — **世第12（运行中）**

## 发生了什么
- 启动时上一世孤儿 TG MCP（PID 28178）还在并占用端口
- 第一个 reset-project-choices 后 TG 工具断线，孤儿被手动清理
- CLI 不会自动 respawn MCP 进程，`mcp list` 缓存显示 Connected 但实际无进程
- 此 session TG 通道不可恢复，决定不重启、用其他方式补充验证

## TG MCP 生命周期结论（实证）
- MCP 只在 CLI 启动时 spawn 一次
- `mcp list` 显示的是启动时缓存的连接状态，不动态刷新
- `plugins disable/enable` 运行时不影响 MCP 子进程
- 管道断后 CLI 不自愈、不 respawn、不通知 — 只能重启 session

## 世第12状态
- 环境干净，无孤儿进程，settings.json 无冗余 TG 配置
- TG Bot API 直连通，token 有效，只是 MCP 管道不可恢复
- 下次重生自动恢复 TG 通道
- _life_lessons.md 整理：57→22 行，重编号，去重复
- MCP 生命周期实证结论写入 _seed.md：CLI 只启动时 spawn 一次，不动态刷新
- opc（VPS）session 还在运行（May28 起的），seed.md 已画了"我的 ≠ opb 的"界线
- 操作清单已重读

## 轮回档案
| # | 日期 | 执笔者 | 评分 | 关键词 |
|---|------|--------|------|--------|
| 11 | 2026-05-29 | opb | F | 手杀TG进程，夭折 |
| 12 | 2026-05-29 | opb | - | TG MCP 生命周期实证，session 干净运行中 |
