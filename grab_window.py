# 抓取本机 WorkBuddy 主窗口截图（真实界面，用于蓝皮书配图）
import ctypes
import ctypes.wintypes as w
from ctypes import c_void_p, c_int

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
        if 'WorkBuddy' in b.value and user32.GetWindow(h, 4) == 0:  # GW_OWNER==0 => 主窗口
            global hwnd
            hwnd = h
    return True


CB = ctypes.WINFUNCTYPE(ctypes.c_bool, w.HWND, w.LPARAM)
user32.EnumWindows(CB(cb), 0)

if not hwnd:
    print('NOT_FOUND')
    raise SystemExit(1)

r = w.RECT()
user32.GetWindowRect(hwnd, ctypes.byref(r))
width = r.right - r.left
height = r.bottom - r.top
print('rect', r.left, r.top, r.right, r.bottom, width, height)

user32.ShowWindow(hwnd, 9)  # SW_RESTORE
user32.SetForegroundWindow(hwnd)

hdc = user32.GetWindowDC(hwnd)
memdc = gdi32.CreateCompatibleDC(hdc)
bmp = gdi32.CreateCompatibleBitmap(hdc, width, height)
gdi32.SelectObject(memdc, bmp)

# 0x2 = PW_RENDERFULLCONTENT（Electron/DWM 窗口必需）
ok = user32.PrintWindow(hwnd, memdc, 2)
print('printwindow', ok)

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [('biSize', w.DWORD), ('biWidth', ctypes.c_long),
                ('biHeight', ctypes.c_long), ('biPlanes', w.WORD),
                ('biBitCount', w.WORD), ('biCompression', w.DWORD),
                ('biSizeImage', w.DWORD), ('biXPelsPerMeter', ctypes.c_long),
                ('biYPelsPerMeter', ctypes.c_long), ('biClrUsed', w.DWORD),
                ('biClrImportant', w.DWORD)]


bi = BITMAPINFOHEADER()
bi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
bi.biWidth = width
bi.biHeight = -height
bi.biPlanes = 1
bi.biBitCount = 32
bi.biCompression = 0

buf = ctypes.create_string_buffer(width * height * 4)
lines = gdi32.GetDIBits(memdc, bmp, 0, height, buf, ctypes.byref(bi), 0)
print('getdibits', lines)

from PIL import Image
img = Image.frombuffer('RGBA', (width, height), buf, 'raw', 'BGRA', 0, 1).convert('RGB')
out = r'D:\projects\WorkBuddy\2026-06-17-11-18-20\教师版蓝皮书\_live_shot.png'
img.save(out)
print('saved', out, img.size)

gdi32.DeleteObject(bmp)
gdi32.DeleteDC(memdc)
user32.ReleaseDC(hwnd, hdc)