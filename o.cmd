@echo off
setlocal enabledelayedexpansion
cd /d "C:\Users\user\.claude-relay"
:: 临时取消代理（本地 V2Ray/Clash 可能导致连不上）
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set NO_PROXY=localhost,127.0.0.1,*.local
if exist session.id (
    set /p SESSION_ID=<session.id
    "C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --resume !SESSION_ID! --add-dir "C:\Users\user\.claude-relay" --add-dir "P:\Claude" --dangerously-skip-permissions
) else (
    "C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --add-dir "C:\Users\user\.claude-relay" --add-dir "P:\Claude" --dangerously-skip-permissions
)
