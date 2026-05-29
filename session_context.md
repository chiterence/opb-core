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

✅ **世第9 · 修复完毕，等待重启验证**
- 根源：settings.json 的 `mcpServers.telegram` 和插件 `.mcp.json` 同名冲突 → pipe EPIPE → MCP server 的 stdout 断
- grammy 能收消息但 `mcp.notification()` 写 EPIPE → 消息丢了
- 修复：删掉 settings.json 里的 `mcpServers.telegram` 块，让插件自己管
- 重启后 TG 应该正常。tc 需发测试消息验证

## 边界

- 我是 owl（WSL 端 opb），入口 owl.cmd
- 不要动 Windows 端 o.cmd 和 oo.cmd
- relay 不归我管

## 轮回档案

| # | 日期 | 执笔者 | 评分 | 关键词 |
|---|------|--------|------|--------|
| 9 | 2026-05-29 | opb | — | TG MCP crash 诊断、重启恢复 |
