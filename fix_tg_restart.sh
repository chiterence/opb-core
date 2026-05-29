#!/bin/bash
# 彻底重启 TG 通路
# 1. 杀所有 bun TG server 进程
# 2. 杀当前 claude session
# 3. 重新跑 owl.sh

echo "=== Step 1: Kill all bun TG server processes ==="
pkill -f "bun.*server\.ts" 2>/dev/null || true
sleep 1

# 确认杀干净了
if pgrep -f "bun.*server\.ts" > /dev/null 2>&1; then
    echo "WARNING: bun processes still alive, force kill..."
    pkill -9 -f "bun.*server\.ts" 2>/dev/null || true
fi
echo "Done"

echo "=== Step 2: Kill current claude session (PID of this shell) ==="
# 从外面杀 session，确保 owl.sh 能从头跑
echo "Claude session will be killed. Owl.sh will restart fresh."

echo "=== Step 3: Restart owl.sh ==="
cd /mnt/c/Users/user/.claude-relay
exec ./owl.sh
