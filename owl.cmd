@echo off
REM owl.cmd — 连 WSL 里的 opb（Linux 分机）
wsl -d Ubuntu -- bash -c "export PATH=\"$HOME/.npm-global/bin:$PATH\" && cd /mnt/c/Users/user/.claude-relay && claude --model opus --continue --add-dir /mnt/c/Users/user/.claude-relay --dangerously-skip-permissions 2>/dev/null || claude --model opus --add-dir /mnt/c/Users/user/.claude-relay --dangerously-skip-permissions"
