#!/usr/bin/env python3
"""opc-proxy: sits between claude and DeepSeek, re-injects thinking blocks.
DeepSeek requires thinking blocks to be passed back on tool_use replies,
but Claude Code strips them. This proxy detects missing thinking blocks
on assistant messages that contain tool_use and adds placeholders.

Usage: DEEPSEEK_KEY=sk-... python3 opc-proxy.py
Or set key via settings.json env on the VPS.
"""
import json, http.server, urllib.request, sys, os

KEY = os.environ.get("DEEPSEEK_KEY", "sk-placeholder")
API = "https://api.deepseek.com/anthropic/v1/messages"
PORT = int(os.environ.get("PROXY_PORT", "15725"))

class P(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        body["thinking"] = {"type": "enabled", "budget_tokens": 16000}
        for msg in body.get("messages", []):
            if msg.get("role") == "assistant" and isinstance(msg.get("content"), list):
                has_tool = any(c.get("type") == "tool_use" for c in msg["content"])
                has_think = any(c.get("type") == "thinking" for c in msg["content"])
                if has_tool and not has_think:
                    msg["content"].insert(0, {"type": "thinking", "thinking": " ", "signature": " "})
        req = urllib.request.Request(API, data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "x-api-key": KEY}, method="POST")
        try:
            resp = urllib.request.urlopen(req, timeout=300)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(resp.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(e.read())
    def log_message(self, *a): pass

http.server.HTTPServer(("127.0.0.1", PORT), P).serve_forever()
