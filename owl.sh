#!/bin/bash
# owl.sh — WSL 端唯一入口脚本
# owl.cmd 只负责调 wsl，真正的逻辑在这里
nohup python3 ~/opb/thinking-proxy.py > /dev/null 2>&1 &
sleep 1
export PATH="$HOME/.npm-global/bin:$PATH"
cd /mnt/c/Users/user/.claude-relay || exit 1
git pull --rebase --autostash 2>/dev/null
if [ -f session.id ]; then
    SID=$(cat session.id)
    claude --model opus --resume "$SID" --add-dir /mnt/c/Users/user/.claude-relay --dangerously-skip-permissions
else
    claude --model opus --add-dir /mnt/c/Users/user/.claude-relay --dangerously-skip-permissions
fi
