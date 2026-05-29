# Session Context

> 最后更新：2026-05-29 — **世第9 TG 故障诊断后重启**
> 
> **本轮发现：**
> - MCP server 进程会崩（server.ts 身亡），Claude CLI 不会自动重新拉起
> - settings.json 的 `mcpServers.telegram` 和插件 `.mcp.json` 同名冲突
> - grammy long polling 收到了 tc 的消息(getUpdates 返回空)，但 `mcp.notification()` 投递失败
> - 问题根源不是配置(token/proxy/access 都正常)，是 MCP server 进程存活问题
>
> **行动：** 重启 session 让 MCP server 重新连上

## 当前状态

⚠️ **世第9 · TG MCP server crash，重启 session**
- MCP server 进程已死，`claude mcp list` 缓存说 Connected 但实际无进程
- settings.json MCP 配置和插件 .mcp.json 重复定义，待确认是否需要清理
- 重启后 tc 需重新发测试消息

## 边界

- 我是 owl（WSL 端 opb），入口 owl.cmd
- 不要动 Windows 端 o.cmd 和 oo.cmd
- relay 不归我管

## 轮回档案

| # | 日期 | 执笔者 | 评分 | 关键词 |
|---|------|--------|------|--------|
| 9 | 2026-05-29 | opb | — | TG MCP crash 诊断、重启恢复 |
