#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把《专题_360VR全景互动网页.md》渲染成会话内可读的 tab 式 HTML fragment。"""
import base64
import io
import os
import re

import markdown
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(BASE, "教师版蓝皮书", "专题_360VR全景互动网页.md")
ASSETS = os.path.join(BASE, "assets_opt")
OUT = r"C:\Users\Administrator\.zcode\v2\visualizations\b0972f0118394f3ef932d75dbbb4526f270a4bac4bac6bf5dabfac0726ca22f0\vr-tutorial-reader.html"

with open(MD_PATH, encoding="utf-8") as f:
    src = f.read()

# 去掉编辑说明块（内部工作稿，读者不需要）
src = re.sub(r"> 【编辑说明[\s\S]*?（自行决定。\n", "", src, count=1)

html = markdown.markdown(src, extensions=["tables", "fenced_code"])

# 表格加样式类
html = html.replace("<table>", '<table class="table">')

# 图片内嵌：缩到 640 宽再 base64，保证会话内能显示
def embed_img(m):
    rel = m.group(1)
    p = os.path.join(BASE, "教师版蓝皮书", rel.replace("/", os.sep))
    if not os.path.isfile(p):
        p = os.path.join(ASSETS, os.path.basename(rel))
    if not os.path.isfile(p):
        return m.group(0)
    img = Image.open(p).convert("RGB")
    if img.width > 640:
        img = img.resize((640, int(img.height * 640 / img.width)))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=78)
    b64 = base64.b64encode(buf.getvalue()).decode()
    print(f"  内嵌 {os.path.basename(rel)}  {len(b64)//1024} KB(b64)")
    return f'<img src="data:image/jpeg;base64,{b64}" alt="" />'

html = re.sub(r'<img[^>]*src="([^"]+)"[^>]*/>', embed_img, html)

# 按 <h2> 切成节
parts = re.split(r"(<h2>.*?</h2>)", html)
sections = []  # (标题文本, 该节完整 html 含 h2)
buf = []
cur = None
for chunk in parts:
    if chunk.startswith("<h2>"):
        if cur is not None:
            sections.append((cur, "".join(buf)))
        cur = re.sub(r"<[^>]+>", "", chunk)
        buf = [chunk]
    else:
        buf.append(chunk)
if cur is not None:
    sections.append((cur, "".join(buf)))

# 分组成 8 个 tab
GROUPS = [
    ("导览与原理", ["这一讲你会做出什么", "第 0 步", "技术选型"]),
    ("第 1–3 步　素材与第一个页面", ["第 1 步", "第 2 步", "第 3 步"]),
    ("第 4–5 步　热点与多场景", ["第 4 步", "第 5 步"]),
    ("设计规则　热点与配图", ["设计规则"]),
    ("原理课与备选路线", ["第 6 步", "备选路线", "扩展"]),
    ("上线与避坑", ["第 7 步", "第 8 步", "避坑清单"]),
    ("操作案例（实跑验证）", ["操作案例"]),
    ("附录　速查 / E 提示词 / 分集", ["附 1", "附 2", "附 3"]),
]

def pick(keys):
    got = []
    for title, body in sections:
        if any(k in title for k in keys):
            got.append(body)
    return "".join(got)

nav, panels = [], []
for i, (label, keys) in enumerate(GROUPS):
    sid = f"tab{i}"
    active = " active" if i == 0 else ""
    sel = "true" if i == 0 else "false"
    nav.append(f'<button class="nav-link{active}" id="{sid}" role="tab" aria-controls="{sid}-panel" '
               f'aria-selected="{sel}" type="button">{label}</button>')
    hidden = "" if i == 0 else " hidden"
    panels.append(f'<div id="{sid}-panel" role="tabpanel" aria-labelledby="{sid}"{hidden}>{pick(keys)}</div>')

fragment = f'''<div id="vr-reader">
<style>
#vr-reader {{ font-size: 14px; }}
#vr-reader .nav.nav-pills {{ margin-bottom: 16px; }}
#vr-reader h1 {{ font-size: 22px; margin-bottom: 4px; }}
#vr-reader h2 {{ font-size: 18px; margin-top: 28px; padding-top: 18px; border-top: 1px solid var(--border); }}
#vr-reader h2:first-child {{ border-top: none; margin-top: 8px; padding-top: 0; }}
#vr-reader h3 {{ font-size: 15px; margin-top: 22px; font-weight: 500; }}
#vr-reader h4 {{ font-size: 14px; margin-top: 18px; font-weight: 500; }}
#vr-reader p, #vr-reader li {{ line-height: 1.75; }}
#vr-reader .table {{ width: 100%; margin: 12px 0; }}
#vr-reader .table th {{ background: var(--muted); }}
#vr-reader pre {{ background: var(--muted); border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; overflow-x: auto; }}
#vr-reader pre code {{ background: none; padding: 0; font-size: 12.5px; line-height: 1.6; }}
#vr-reader code {{ background: var(--muted); border-radius: 4px; padding: 1px 5px; }}
#vr-reader pre code {{ background: none; }}
#vr-reader blockquote {{ border-left: 3px solid var(--border); margin: 12px 0; padding: 2px 14px; color: var(--muted-foreground); }}
#vr-reader blockquote p {{ margin: 6px 0; }}
#vr-reader img {{ max-width: 100%; border-radius: 8px; border: 1px solid var(--border); display: block; margin: 10px auto; }}
#vr-reader hr {{ margin: 20px 0; }}
#vr-reader .reader-head {{ margin-bottom: 10px; }}
#vr-reader .reader-sub {{ color: var(--muted-foreground); margin: 2px 0 0; }}
</style>
<div class="reader-head">
  <h1>360° VR 全景互动网页：从一张全景图到一条能分享的链接</h1>
  <p class="reader-sub">WorkBuddy 教师实战蓝皮书 · 专题教程　｜　八节导航，点上方标签切换；正文 19 节全文在内</p>
</div>
<div class="nav nav-pills" role="tablist" aria-label="教程分节">
  {''.join(nav)}
</div>
{''.join(panels)}
</div>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(fragment)
print(f"\n写出: {OUT}  {os.path.getsize(OUT)//1024} KB")
