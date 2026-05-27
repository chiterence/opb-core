@echo off
cd /d "C:\Users\user\.claude-relay"

:: 本地桌面直连（非SSH）→ 走 SSH 拿 PTY，绕开终端兼容问题
if "%SSH_CLIENT%"=="" (
    ssh -t user@127.0.0.1 "cd /d C:\Users\user\.claude-relay && o.cmd"
    exit /b
)

:: 已在 SSH/终端中，直接跑
set HTTP_PROXY=
set HTTPS_PROXY=
set NO_PROXY=localhost,127.0.0.1,*.local
"C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --continue --add-dir "C:\Users\user\.claude-relay" --add-dir "P:\Claude" --dangerously-skip-permissions
