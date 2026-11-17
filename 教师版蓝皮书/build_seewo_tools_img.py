# -*- coding: utf-8 -*-
"""生成「希沃特有功能 × 提示词速查」中文配图（HTML + 本机 Chromium 渲染）。"""
from pathlib import Path
import subprocess
import time

from PIL import Image

BASE = Path(__file__).resolve().parent
OUT = BASE / "assets_opt" / "seewo_full_12_native_tools.png"
HTML = BASE / "_build_seewo_tools.html"
CHROME = (r"C:/Users/Administrator/AppData/Local/ms-playwright/"
          r"chromium_headless_shell-1228/chrome-headless-shell-win64/"
          r"chrome-headless-shell.exe")

PAPER = "#FBF8F2"
INK = "#26312F"
SUB = "#3F5A62"
RED = "#B4472B"
LINE = "#E5DFD0"

GROUPS = [
    ("A · 语文学科工具", RED, [
        ("汉字卡", "点名生字 → 笔顺、拼音、部首"),
        ("古诗词卡", "点名篇名与作者 → 原文、译文、朗读"),
        ("拼音卡", "点名带声调音节 → 正音、发音"),
    ]),
    ("B · 结构化梳理", "#3F5A62", [
        ("思维导图", "点名根节点与分支 → 逐级展开"),
        ("表格", "点名对照维度 → 同构并置"),
    ]),
    ("C · 课堂活动", "#7A2E1B", [
        ("判断对错", "点名 5 道题 + 答案（对对对错错）"),
        ("趣味选择", "点名单选 4 题 + 选项与解析"),
        ("知识配对", "点名左右两组 → 学生拖动"),
        ("超级分类", "点名分类框 + 待归词语"),
    ]),
    ("D · 其他学科", "#5B6E54", [
        ("函数图像", "点名表达式与观察任务"),
        ("四线三格", "点名英文词 → 规范书写"),
    ]),
]

cards = []
for title, color, rows in GROUPS:
    body = "".join(
        '<div style="display:flex;gap:10px;font-size:18px;color:%s;'
        'line-height:1.85;margin-bottom:8px">'
        '<span style="font-weight:700;color:%s;min-width:86px">%s</span>'
        '<span>%s</span></div>' % (INK, color, name, desc)
        for name, desc in rows)
    cards.append(
        '<div style="flex:1;min-width:0;background:#FFFFFF;border:1px solid %s;'
        'border-top:5px solid %s;border-radius:0 0 12px 12px;padding:18px 18px 14px">'
        '<div style="font-size:23px;font-weight:700;color:%s;margin-bottom:14px">%s</div>'
        '%s</div>' % (LINE, color, color, title, body))

html_doc = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;background:%s;font-family:"Microsoft YaHei","PingFang SC",sans-serif;color:%s;overflow:hidden}
</style></head><body>
<div style="padding:34px 40px 30px">
  <div style="font-size:16px;color:%s;letter-spacing:2px;margin-bottom:10px">点名才有 · 不点名就只是普通页面</div>
  <div style="font-size:38px;font-weight:700;margin-bottom:8px">希沃特有功能，提示词里要写哪几句</div>
  <div style="font-size:19px;color:%s;margin-bottom:26px">下面每一类都能单独塞进生成提示词，也能生成后追加；括号里就是必须说清的信息</div>
  <div style="display:flex;gap:16px;align-items:stretch">%s</div>
  <div style="display:flex;gap:16px;margin-top:16px;align-items:stretch">%s</div>
  <div style="margin-top:24px;background:%s;border-radius:10px;padding:16px 22px;font-size:21px;color:#FFFFFF;font-weight:700">
    组合模板：课题 + 页数区间 + 图片方案 + 特有功能清单（哪一页放哪个）+ 交付 .enbx
  </div>
</div>
</body></html>""" % (PAPER, INK, SUB, SUB, cards[0] + cards[1], cards[2] + cards[3], RED)

HTML.write_text(html_doc, encoding="utf-8")
if OUT.exists():
    OUT.unlink()
cmd = [CHROME, "--headless", "--no-sandbox", "--disable-gpu",
       "--hide-scrollbars", "--window-size=1080,760",
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

# 裁掉底部多余的纯背景行
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
