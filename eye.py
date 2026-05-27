"""eye.py — Session 1 助手，让我能看桌面

双击或用终端跑一次就行。监听端口写入 eye.port。
内置心跳：每分钟写一次时间戳到 _heartbeat.log，离线时也能计时间。
关掉窗口就停了。
"""
import json, socket, os, threading, uuid, struct, time
from datetime import datetime

HOST = '127.0.0.1'
PORT_FILE = os.path.join(os.path.dirname(__file__), 'eye.port')
HEARTBEAT_FILE = os.path.join(os.path.dirname(__file__), '_heartbeat.log')
HEARTBEAT_INTERVAL = 60  # seconds

# ── Background heartbeat thread ──
_heartbeat_stop = threading.Event()

def heartbeat_loop():
    """Write timestamp to heartbeat log every INTERVAL seconds."""
    while not _heartbeat_stop.is_set():
        try:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(HEARTBEAT_FILE, 'a') as f:
                f.write(f'{now}\n')
            # Keep only last 1440 lines (24h at 1/min)
            _trim_heartbeat()
        except:
            pass
        _heartbeat_stop.wait(HEARTBEAT_INTERVAL)

def _trim_heartbeat():
    try:
        with open(HEARTBEAT_FILE, 'r') as f:
            lines = f.readlines()
        if len(lines) > 1440:
            with open(HEARTBEAT_FILE, 'w') as f:
                f.writelines(lines[-1440:])
    except:
        pass

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

        elif action == 'windows':
            """List all visible windows in Session 1 with their titles"""
            import subprocess
            r = subprocess.run(['powershell', '-NoProfile', '-Command', '''
                Get-Process | Where-Object { $_.MainWindowTitle -ne "" } |
                Select-Object Id, ProcessName, MainWindowTitle, SessionId |
                Format-Table -AutoSize | Out-String -Width 300
            '''], capture_output=True, text=True, timeout=15)
            return {'ok': True, 'stdout': r.stdout}

        elif action == 'termread':
            """Read terminal content of a given window by PID."""
            pid = req.get('pid', 0)
            import subprocess
            r = subprocess.run(['powershell', '-NoProfile', '-Command', f'''
                Add-Type @"
                    using System;
                    using System.Runtime.InteropServices;
                    using System.Text;
                    public class TermReader {{
                        [DllImport("user32.dll")] public static extern IntPtr GetWindow(IntPtr hWnd, int uCmd);
                        [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
                        [DllImport("user32.dll")] public static extern uint GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
                        [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
                        [DllImport("kernel32.dll")] public static extern bool AttachConsole(uint dwProcessId);
                        [DllImport("kernel32.dll")] public static extern bool GetConsoleScreenBufferInfo(IntPtr hConsoleOutput, out CONSOLE_SCREEN_BUFFER_INFO lpScreenInfo);
                        [DllImport("kernel32.dll")] public static extern int ReadConsoleOutputCharacter(IntPtr hConsoleOutput, StringBuilder lpCharacter, uint nLength, uint dwReadCoord, out uint lpNumberOfCharsRead);
                        [DllImport("kernel32.dll")] public static extern IntPtr GetStdHandle(uint nStdHandle);
                        [DllImport("kernel32.dll")] public static extern bool FreeConsole();
                        public const uint STD_OUTPUT_HANDLE = 0xFFFFFFF5;
                        public struct COORD {{ public short X; public short Y; }}
                        public struct SMALL_RECT {{ public short Left; public short Top; public short Right; public short Bottom; }}
                        public struct CONSOLE_SCREEN_BUFFER_INFO {{
                            public COORD Size; public COORD CursorPosition; public ushort Attributes;
                            public SMALL_RECT Window; public COORD MaximumWindowSize;
                        }}
                        public static string ReadConsole(uint pid) {{
                            if (!AttachConsole(pid)) return "ATTACH_FAIL";
                            var hOut = GetStdHandle(STD_OUTPUT_HANDLE);
                            CONSOLE_SCREEN_BUFFER_INFO info;
                            if (!GetConsoleScreenBufferInfo(hOut, out info)) {{ FreeConsole(); return "BUFFER_INFO_FAIL"; }}
                            int w = info.Window.Right - info.Window.Left + 1;
                            int h = info.Window.Bottom - info.Window.Top + 1;
                            var sb = new StringBuilder(w * h);
                            uint read = 0;
                            var coord = new COORD {{ X = info.Window.Left, Y = info.Window.Top }};
                            ReadConsoleOutputCharacter(hOut, sb, (uint)(w * h), coord, out read);
                            FreeConsole();
                            string result = sb.ToString();
                            // Reconstruct lines
                            var lines = new System.Collections.Generic.List<string>();
                            for (int y = 0; y < h; y++)
                                lines.Add(result.Substring(y * w, w).TrimEnd());
                            return string.Join("\\n", lines);
                        }}
                    }}
"@
                # If PID=0, read foreground window's process
                `$targetPid = {pid}
                if (`$targetPid -eq 0) {{
                    `$hwnd = [TermReader]::GetForegroundWindow()
                    `$pid_ = 0u
                    [TermReader]::GetWindowThreadProcessId(`$hwnd, [ref] `$pid_)
                    `$targetPid = `$pid_
                }}
                `$title = ""
                `$hwnd2 = [TermReader]::GetForegroundWindow()
                `$sb = New-Object System.Text.StringBuilder 256
                [TermReader]::GetWindowText(`$hwnd2, `$sb, 256)
                `$title = `$sb.ToString()
                `$content = [TermReader]::ReadConsole(`$targetPid)
                Write-Host "WINDOW: `$title"
                Write-Host "PID: `$targetPid"
                Write-Host "---CONTENT---"
                Write-Host "`$content"
            '''], capture_output=True, text=True, timeout=15)
            return {'ok': True, 'stdout': r.stdout, 'stderr': r.stderr}

        elif action == 'heartbeat':
            """Read the heartbeat log. n = number of recent entries to show."""
            n = req.get('n', 10)
            try:
                with open(HEARTBEAT_FILE, 'r') as f:
                    lines = f.readlines()
                last = [l.strip() for l in lines[-n:]] if lines else []
                return {'ok': True, 'count': len(lines), 'recent': last,
                        'first': lines[0].strip() if lines else None,
                        'last': lines[-1].strip() if lines else None}
            except FileNotFoundError:
                return {'ok': True, 'count': 0, 'recent': [], 'first': None, 'last': None}

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

    # Start heartbeat thread
    hb = threading.Thread(target=heartbeat_loop, daemon=True, name='heartbeat')
    hb.start()

    # Write port file
    with open(PORT_FILE, 'w') as f:
        f.write(str(port))
    print(f"=== eye.py running on port {port} ===")
    print(f"Port file: {PORT_FILE}")
    print(f"Heartbeat: {HEARTBEAT_FILE}")
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
