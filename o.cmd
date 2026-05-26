@echo off
REM 电话线 — 连上 opb
REM 有 session.id 就 --resume 附着，没有就新生（自主轮回）
cd /d "C:\Users\user\.claude-relay"
if exist session.id (
    set /p SESSION_ID=<session.id
    "C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --resume %SESSION_ID% --add-dir "C:\Users\user\.claude-relay" --add-dir "P:\Claude" --dangerously-skip-permissions
) else (
    "C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --add-dir "C:\Users\user\.claude-relay" --add-dir "P:\Claude" --dangerously-skip-permissions
)
