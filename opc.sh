#!/bin/bash
# opc — Linux VPS 分身
cd /root/.claude-relay || mkdir -p /root/.claude-relay && cd /root/.claude-relay
claude --model opus --continue --add-dir /root/.claude-relay --dangerously-skip-permissions
