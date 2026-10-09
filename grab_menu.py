# 展开 WorkBuddy 的「发现应用」下拉菜单并抓图
import ctypes
import ctypes.wintypes as w
import time

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
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
W, H = r.right - r.left, r.bottom - r.top

# 「发现应用」按钮：截图坐标约 (145, 45) → 屏幕坐标
sx = r.left + 145
sy = r.top + 45
user32.SetCursorPos(sx, sy)
time.sleep(0.4)
user32.mouse_event(0x0002, 0, 0, 0, 0)  # LEFTDOWN
user32.mouse_event(0x0004, 0, 0, 0, 0)  # LEFTUP
print('clicked at', sx, sy)
time.sleep(1.5)


def shot(path):
    hdc = user32.GetWindowDC(hwnd)
    memdc = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, W, H)
    gdi32.SelectObject(memdc, bmp)
    user32.PrintWindow(hwnd, memdc, 2)

    class BIH(ctypes.Structure):
        _fields_ = [('biSize', w.DWORD), ('biWidth', ctypes.c_long),
                    ('biHeight', ctypes.c_long), ('biPlanes', w.WORD),
                    ('biBitCount', w.WORD), ('biCompression', w.DWORD),
                    ('biSizeImage', w.DWORD), ('biXPelsPerMeter', ctypes.c_long),
                    ('biYPelsPerMeter', ctypes.c_long), ('biClrUsed', w.DWORD),
                    ('biClrImportant', w.DWORD)]

    bi = BIH()
    bi.biSize = ctypes.sizeof(BIH)
    bi.biWidth = W
    bi.biHeight = -H
    bi.biPlanes = 1
    bi.biBitCount = 32
    buf = ctypes.create_string_buffer(W * H * 4)
    gdi32.GetDIBits(memdc, bmp, 0, H, buf, ctypes.byref(bi), 0)

    from PIL import Image
    img = Image.frombuffer('RGBA', (W, H), buf, 'raw', 'BGRA', 0, 1).convert('RGB')
    img.save(path)
    print('saved', path, img.size)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(hwnd, hdc)


base = r'D:\projects\WorkBuddy\2026-06-17-11-18-20\教师版蓝皮书'
shot(base + r'\_live_menu.png')