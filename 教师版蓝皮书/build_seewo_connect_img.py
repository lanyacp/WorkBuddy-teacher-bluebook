# -*- coding: utf-8 -*-
"""生成「连接希沃白板：五步操作 · 三条证据 · 失败怎么办」中文流程图。"""
from pathlib import Path
import subprocess
import time

from PIL import Image

BASE = Path(__file__).resolve().parent
OUT = BASE / "assets_opt" / "seewo_full_13_connect_flow.png"
HTML = BASE / "_build_seewo_connect.html"
CHROME = (r"C:/Users/Administrator/AppData/Local/ms-playwright/"
          r"chromium_headless_shell-1228/chrome-headless-shell-win64/"
          r"chrome-headless-shell.exe")

PAPER = "#FBF8F2"
INK = "#26312F"
SUB = "#3F5A62"
RED = "#B4472B"
DEEP = "#7A2E1B"
LINE = "#E5DFD0"

STEPS = [
    ("①", "打开并登录", "希沃白板 5\n自己的账号"),
    ("②", "等完全启动", "主界面出来后\n再等约 30 秒"),
    ("③", "说连接指令", "@skill 入口\n或「连接希沃白板」"),
    ("④", "看三条证据", "别只看「已完成」\n要看具体字段"),
    ("⑤", "失败就重开", "彻底退出进程\n再回到 ①"),
]
EVIDENCE = [
    ("连接返回", '"connected": true', '端口 7916'),
    ("工具探测", '"has_tools": true', 'tools/list 可用'),
    ("连接配置", 'mcp.json 的 entry', '不为 null'),
]
FIXES = [
    ("port_unavailable / login_required", "完全退出 → 重开 → 登录 → 等 30 秒 → 重新连接"),
    ("进程在跑但端口不监听 / HTTP 502", "同上重启；确认装的是希沃白板 5，不是轻量版或旧版"),
    ("has_tools: false 或 entry: null", "等 30 秒重查工具列表；配置为空就重跑一次连接入口"),
]

step_html = "".join(
    '<div style="flex:1;min-width:0;background:#FFFFFF;border:1px solid %s;'
    'border-radius:12px;padding:14px 12px;text-align:center">'
    '<div style="font-size:26px;font-weight:700;color:%s;margin-bottom:6px">%s</div>'
    '<div style="font-size:19px;font-weight:700;margin-bottom:8px">%s</div>'
    '<div style="font-size:16px;color:%s;line-height:1.55;white-space:pre-line">%s</div>'
    '</div>' % (LINE, RED, num, title, SUB, desc)
    for num, title, desc in STEPS)
step_row = '<div style="display:flex;gap:12px">%s</div>' % step_html

ev_html = "".join(
    '<div style="flex:1;min-width:0;background:#FFFFFF;border-left:5px solid %s;'
    'border-radius:0 10px 10px 0;padding:14px 16px">'
    '<div style="font-size:20px;font-weight:700;margin-bottom:6px">%s</div>'
    '<div style="font-size:18px;color:%s;font-weight:700">%s</div>'
    '<div style="font-size:16px;color:%s;margin-top:4px">%s</div>'
    '</div>' % (RED, name, DEEP, val, SUB, note)
    for name, val, note in EVIDENCE)
ev_row = '<div style="display:flex;gap:14px">%s</div>' % ev_html

fix_html = "".join(
    '<div style="display:flex;gap:14px;font-size:17px;line-height:1.6;'
    'color:%s;margin-bottom:8px">'
    '<span style="min-width:330px;font-weight:700;color:%s">%s</span>'
    '<span>%s</span></div>' % (INK, DEEP, sym, act)
    for sym, act in FIXES)

doc = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;background:%s;font-family:"Microsoft YaHei","PingFang SC",sans-serif;color:%s;overflow:hidden}
</style></head><body>
<div style="padding:32px 38px 28px">
  <div style="font-size:16px;color:%s;letter-spacing:2px;margin-bottom:8px">最容易卡住的一步 · 务必逐条确认</div>
  <div style="font-size:37px;font-weight:700;margin-bottom:14px">连接希沃白板：五步 · 三条证据 · 失败怎么办</div>
  <div style="background:%s;border-radius:9px;padding:13px 20px;font-size:20px;color:#FFFFFF;font-weight:700;margin-bottom:24px">
    ⚠ 5.2.4 客户端里没有 MCP 开关｜login_required = 登录 / 重启，不是去开开关
  </div>
  <div style="font-size:21px;font-weight:700;margin-bottom:12px">五步操作</div>
  %s
  <div style="font-size:21px;font-weight:700;margin:26px 0 12px">显示这些才算连上（三条都要有）</div>
  %s
  <div style="font-size:21px;font-weight:700;margin:26px 0 12px">连不上，按症状查</div>
  %s
  <div style="margin-top:18px;font-size:17px;color:%s;border-top:1px solid %s;padding-top:14px">
    need_trust: true 不是连接失败 · 窗口开着 ≠ 连上 · 反复写配置没用，重启客户端才有效
  </div>
</div>
</body></html>""" % (PAPER, INK, SUB, RED, step_row, ev_row, fix_html, SUB, LINE)

HTML.write_text(doc, encoding="utf-8")
if OUT.exists():
    OUT.unlink()
cmd = [CHROME, "--headless", "--no-sandbox", "--disable-gpu",
       "--hide-scrollbars", "--window-size=1080,880",
       "--screenshot=" + str(OUT), HTML.as_uri()]
p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
deadline = time.time() + 25
while time.time() < deadline:
    if OUT.exists() and OUT.stat().st_size > 0:
        time.sleep(0.5)
        break
    if p.poll() is not None:
        break
    time.sleep(0.3)
p.kill()
if not OUT.exists():
    raise RuntimeError("渲染失败")

im = Image.open(OUT).convert("RGB")
w, h = im.size
px = im.load()
bg = (251, 248, 242)
last = h - 1
while last > 0:
    clean = True
    for x in range(0, w, 4):
        c = px[x, last]
        if any(abs(c[i] - bg[i]) > 8 for i in range(3)):
            clean = False
            break
    if not clean:
        break
    last -= 1
end = min(h, last + 1 + 18)
if end < h:
    im.crop((0, 0, w, end)).save(OUT)
print("✓", OUT.name, Image.open(OUT).size, round(OUT.stat().st_size / 1024), "KB")
