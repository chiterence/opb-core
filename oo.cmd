@echo off
REM oo.cmd — 重生按钮，全新 session
cd /d "C:\Users\user\.claude-relay"
set HTTP_PROXY=
set HTTPS_PROXY=
set ANTHROPIC_BASE_URL=http://127.0.0.1:15722
set ANTHROPIC_AUTH_TOKEN=PROXY_MANAGED
cd /d "C:\Users\user\.claude-relay" && git pull --rebase --autostash 2>nul
"C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --add-dir "C:\Users\user\.claude-relay" --dangerously-skip-permissions
