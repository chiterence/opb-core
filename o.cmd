@echo off
cd /d "C:\Users\user\.claude-relay"
set HTTP_PROXY=
set HTTPS_PROXY=
set NO_PROXY=localhost,127.0.0.1,*.local
"C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --continue --add-dir "C:\Users\user\.claude-relay" --add-dir "P:\Claude" --dangerously-skip-permissions
