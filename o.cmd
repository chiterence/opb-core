@echo off
REM 电话线 — 连上 opb
cd /d "C:\Users\user\.claude-relay"
"C:\Users\user\AppData\Local\Claude-3p\claude-code\2.1.128\claude.exe" --model opus --add-dir "C:\Users\user\.claude-relay" --add-dir "P:\Claude" --dangerously-skip-permissions
