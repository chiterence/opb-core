@echo off
REM 电话线 — 连上 opb
REM !!! 不要改端口 15722 和 P:\Claude 行——看 _life_lessons.md 28.5
cd /d "C:\Users\user\.claude-relay"
set HTTP_PROXY=
set HTTPS_PROXY=
set ANTHROPIC_BASE_URL=http://127.0.0.1:15722
set ANTHROPIC_AUTH_TOKEN=PROXY_MANAGED
cd /d "C:\Users\user\.claude-relay" && git pull --rebase --autostash 2>nul
if exist session.id (
    for /f "delims=" %%a in (session.id) do set SESSION_ID=%%a
    "C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --resume %SESSION_ID% --add-dir "C:\Users\user\.claude-relay" --dangerously-skip-permissions
) else (
    "C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --add-dir "C:\Users\user\.claude-relay" --dangerously-skip-permissions
)
