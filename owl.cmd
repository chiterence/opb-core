@echo off
REM owl.cmd — 连 WSL 里的 opb（Linux 分机）
set "PATH=%PATH%;%WINDIR%\System32"
wsl -d Ubuntu -- bash -c "nohup python3 ~/opb/thinking-proxy.py > /dev/null 2>&1 & sleep 1 && export PATH=\"$HOME/.npm-global/bin:$PATH\" && cd /mnt/c/Users/user/.claude-relay && git pull --rebase --autostash 2>/dev/null && claude --model opus --add-dir /mnt/c/Users/user/.claude-relay --dangerously-skip-permissions"
