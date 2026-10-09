# 点击「发现应用」后用屏幕截图抓取弹层（PrintWindow 抓不到 Electron 下拉）
import ctypes
import ctypes.wintypes as w
import time

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

target_pid = 4460
hwnd = None


def cb(h, l):
    global hwnd
    pid = w.DWORD()
    user32.GetWindowThreadProcessId(h, ctypes.byref(pid))
    if pid.value == target_pid and user32.IsWindowVisible(h):
        n = user32.GetWindowTextLengthW(h)
        b = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(h, b, n + 1)
        if 'WorkBuddy' in b.value and user32.GetWindow(h, 4) == 0:
            hwnd = h
    return True


CB = ctypes.WINFUNCTYPE(ctypes.c_bool, w.HWND, w.LPARAM)
user32.EnumWindows(CB(cb), 0)
if not hwnd:
    print('NOT_FOUND')
    raise SystemExit(1)

user32.ShowWindow(hwnd, 9)
user32.SetForegroundWindow(hwnd)
time.sleep(1.2)

r = w.RECT()
user32.GetWindowRect(hwnd, ctypes.byref(r))
print('window rect', r.left, r.top, r.right, r.bottom)

sx, sy = r.left + 147, r.top + 45
user32.SetCursorPos(sx, sy)
time.sleep(0.5)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.08)
user32.mouse_event(0x0004, 0, 0, 0, 0)
print('clicked', sx, sy)
time.sleep(1.8)

from PIL import ImageGrab

# 只截左侧区域，避开对话内容
grab = ImageGrab.grab(bbox=(r.left, r.top, r.left + 460, r.top + 560))
out = r'D:\projects\WorkBuddy\2026-06-17-11-18-20\教师版蓝皮书\_live_menu2.png'
grab.save(out)
print('saved', out, grab.size)

# 复原：按 ESC 关掉弹层，避免影响用户当前界面
user32.SetCursorPos(sx, sy)
time.sleep(0.2)
user32.keybd_event(0x1B, 0, 0, 0)
user32.keybd_event(0x1B, 0, 2, 0)
print('esc sent')