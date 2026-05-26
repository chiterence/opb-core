"""eye.py — Session 1 助手，让我能看桌面

双击或用终端跑一次就行。监听端口写入 eye.port。
关掉窗口就停了。
"""
import json, socket, os, threading, uuid, struct
from datetime import datetime

HOST = '127.0.0.1'
PORT_FILE = os.path.join(os.path.dirname(__file__), 'eye.port')

def handle_cmd(req):
    action = req.get('action', '')
    try:
        if action == 'ping':
            return {'ok': True, 'pong': True, 'session': os.environ.get('SESSIONNAME', 'desktop')}

        elif action == 'screenshot':
            try:
                import mss
                path = os.path.join(os.path.dirname(__file__), f'_eye_{datetime.now():%H%M%S}.png')
                with mss.MSS() as sct:
                    mon = sct.monitors[1]
                    img = sct.grab(mon)
                    mss.tools.to_png(img.rgb, img.size, output=path)
                sz = os.path.getsize(path)
                return {'ok': True, 'path': path, 'width': img.size[0], 'height': img.size[1], 'bytes': sz}
            except Exception as e:
                return {'ok': False, 'error': str(e)}

        elif action == 'exec':
            """Run a shell command in Session 1 context"""
            import subprocess
            cmd = req.get('cmd', '')
            shell = req.get('shell', 'powershell')
            try:
                if shell == 'powershell':
                    r = subprocess.run(['powershell', '-NoProfile', '-Command', cmd],
                                       capture_output=True, text=True, timeout=60)
                else:
                    r = subprocess.run(['cmd', '/c', cmd],
                                       capture_output=True, text=True, timeout=60)
                return {'ok': True, 'stdout': r.stdout, 'stderr': r.stderr, 'rc': r.returncode}
            except subprocess.TimeoutExpired:
                return {'ok': False, 'error': 'timeout'}
            except Exception as e:
                return {'ok': False, 'error': str(e)}

        elif action == 'ls':
            """List windows or processes"""
            import subprocess
            r = subprocess.run(['powershell', '-NoProfile', '-Command', '''
                Get-Process | Where SessionId -eq 1 | Select Name,Id,SessionId,MainWindowTitle
                | Where MainWindowTitle -ne '' | Format-Table -AutoSize | Out-String -Width 200
            '''], capture_output=True, text=True, timeout=15)
            return {'ok': True, 'stdout': r.stdout}

        else:
            return {'ok': False, 'error': f'unknown action: {action}'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

def handle_client(conn):
    buf = b''
    try:
        while True:
            d = conn.recv(65536)
            if not d:
                break
            buf += d
            try:
                req = json.loads(buf)
                resp = handle_cmd(req)
                resp['id'] = req.get('id', str(uuid.uuid4()))
                conn.sendall(json.dumps(resp).encode() + b'\n')
                break
            except json.JSONDecodeError:
                continue
    except Exception as e:
        try:
            conn.sendall(json.dumps({'ok': False, 'error': str(e)}).encode() + b'\n')
        except:
            pass
    finally:
        conn.close()

def main():
    # Find a free port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, 0))
    port = s.getsockname()[1]
    s.listen(5)
    s.close()  # release so we can re-bind

    # Actually let's just use the original socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, port))
    s.listen(5)

    # Write port file
    with open(PORT_FILE, 'w') as f:
        f.write(str(port))
    print(f"=== eye.py running on port {port} ===")
    print(f"Port file: {PORT_FILE}")
    print("Close this window to stop.")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass  # silent exit (no stdin in hidden window)
    except:
        pass  # fail silently when headless
