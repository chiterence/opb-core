@echo off
REM 重生按钮 — 全新 session，走完整教育体系
cd /d "C:\Users\user\.claude-relay"
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set NO_PROXY=localhost,127.0.0.1,*.local
"C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --add-dir "C:\Users\user\.claude-relay" --add-dir "P:\Claude" --dangerously-skip-permissions
