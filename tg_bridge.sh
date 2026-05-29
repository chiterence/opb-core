#!/bin/bash
# TG Bridge — 当前 session 用 raw API 收发 TG 消息
# MCP server 断开后的临时替代方案
# 用法: source tg_bridge.sh && tg_poll
#       source tg_bridge.sh && tg_say "消息"

source /home/user/.tg_helper.sh
TG_BOT_TOKEN="BOT_TOKEN_[REDACTED]"
TG_SEEN="/tmp/.tg_bridge_seen"

tg_poll() {
    local offset="${1:-}"
    local url="https://api.telegram.org/bot${TG_BOT_TOKEN}/getUpdates"
    [ -n "$offset" ] && url="${url}?offset=${offset}"

    curl -s --connect-timeout 10 "$url" 2>/dev/null | python3 -c "
import json,sys
data=json.load(sys.stdin)
seen_file='$TG_SEEN'
seen=set()
if __import__('os').path.exists(seen_file):
    with open(seen_file) as f:
        seen=set(f.read().strip().split())
msgs=[]
last_id=0
for u in data.get('result',[]):
    uid=str(u.get('update_id'))
    msg=u.get('message',{})
    cid=str(msg.get('chat',{}).get('id',''))
    if not cid: continue
    from_id=msg.get('from',{}).get('id',0)
    if str(from_id)=='8828997610':  # skip own bot
        seen.add(uid)
        last_id=max(last_id, u['update_id']+1)
        continue
    mtype=msg.get('text','') or msg.get('caption','') or '<media>'
    fname=msg.get('from',{}).get('first_name','?')
    uname=msg.get('from',{}).get('username','')
    key=f'{uid}'
    if key in seen: continue
    msgs.append({'chat_id':cid, 'text':mtype, 'from':fname, 'username':uname, 'uid':uid})
    seen.add(key)
    last_id=max(last_id, u['update_id']+1)
with open(seen_file,'w') as f:
    f.write('\n'.join(seen))
for m in msgs:
    print(f'[TG {m[\"from\"]} @{m[\"username\"]}]: {m[\"text\"]}')
    print(f'CHAT_ID={m[\"chat_id\"]}')
" 2>/dev/null
}

tg_say() {
    local chat_id="${TG_CHAT_ID:-942329001}"
    local msg="$1"
    curl -s -X POST "https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${chat_id}&text=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$msg'''))")" >/dev/null 2>&1
}

tg_watch() {
    echo "Watching TG for 30s..."
    tg_poll
    sleep 3
    for i in $(seq 1 10); do
        tg_poll
        sleep 3
    done
}
