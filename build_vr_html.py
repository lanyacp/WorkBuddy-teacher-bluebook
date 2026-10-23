#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把《专题_360VR全景互动网页.md》渲染成独立 HTML 阅读版（单文件，图片内嵌 base64）。

产出：教师版蓝皮书/专题_360VR全景互动网页.html
双击即可浏览，可直接发给别人，不依赖 assets 文件夹和网络。

用法：
    py build_vr_html.py                          # 默认渲染完整版教程
    py build_vr_html.py 教师版蓝皮书/某教程.md    # 渲染指定教程（HTML 输出到同名 .html）
"""
import base64
import io
import os
import re
import sys

import markdown
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(BASE, sys.argv[1]) if len(sys.argv) > 1 else os.path.join(
    BASE, "教师版蓝皮书", "专题_360VR全景互动网页.md")
OUT_PATH = os.path.splitext(MD_PATH)[0] + ".html"
IMG_WIDTH = 1024   # 独立浏览用更大图，单文件约 1MB

with open(MD_PATH, encoding="utf-8") as f:
    src = f.read()

# 从 md 提取一级标题作页面标题，正文中不再重复渲染
_title_m = re.search(r"^# (.+)$", src, re.M)
DOC_TITLE = _title_m.group(1).strip() if _title_m else "教程"
src = re.sub(r"^# .*\n", "", src, count=1) if _title_m else src

# 去掉编辑说明块（并入蓝皮书时删除的内部工作稿，阅读版不放）和 md 自带的一级标题（页面模板已有）
src = re.sub(r"> 【编辑说明[\s\S]*?自行决定。\n", "", src, count=1)
src = re.sub(r"^# .*\n", "", src, count=1)

html = markdown.markdown(src, extensions=["tables", "fenced_code"])
html = html.replace("<table>", '<table class="table">')


# ---- 图片内嵌 base64 ----
def embed_img(m):
    rel = m.group(1)
    p = os.path.join(BASE, "教师版蓝皮书", rel.replace("/", os.sep))
    if not os.path.isfile(p):
        return m.group(0)
    img = Image.open(p).convert("RGB")
    if img.width > IMG_WIDTH:
        img = img.resize((IMG_WIDTH, int(img.height * IMG_WIDTH / img.width)))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=80)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<img src="data:image/jpeg;base64,{b64}" alt="" loading="lazy" />'


html = re.sub(r"<img[^>]*src=\"([^\"]+)\"[^>]*/>", embed_img, html)

# ---- 给 h2/h3 编锚点 id，并提取目录 ----
toc = []          # (level, title, id)
counter = [0, 0]  # h2, h3 计数

def add_id(m):
    level = int(m.group(1))
    text = m.group(2)
    if level == 2:
        counter[0] += 1
        counter[1] = 0
        sid = f"sec-{counter[0]}"
    else:
        counter[1] += 1
        sid = f"sec-{counter[0]}-{counter[1]}"
    plain = re.sub(r"<[^>]+>", "", text)
    toc.append((level, plain, sid))
    return f'<h{level} id="{sid}">{text}</h{level}>'

html = re.sub(r"<h([23])>(.*?)</h\1>", add_id, html)

toc_html = "".join(
    f'<a class="toc-l{lv}" href="#{sid}">{t}</a>' for lv, t, sid in toc
)

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>__TITLE__</title>
<style>
:root {
  --bg: #fafaf9; --fg: #1c1917; --muted-fg: #78716c;
  --border: #e7e5e4; --code-bg: #f5f5f4; --th-bg: #f5f5f4; --accent: #0f766e;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0c0a09; --fg: #e7e5e4; --muted-fg: #a8a29e;
    --border: #292524; --code-bg: #1c1917; --th-bg: #1c1917; --accent: #2dd4bf;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font-family: "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif;
  font-size: 15px; line-height: 1.85;
}
.layout { display: flex; max-width: 1280px; margin: 0 auto; }
nav.toc {
  width: 264px; flex: none; position: sticky; top: 0;
  max-height: 100vh; overflow-y: auto; padding: 28px 8px 40px 20px;
  border-right: 1px solid var(--border); font-size: 13px;
}
nav.toc .toc-title { font-weight: 600; margin-bottom: 10px; letter-spacing: .05em; color: var(--muted-fg); }
nav.toc a {
  display: block; color: var(--fg); text-decoration: none;
  padding: 4px 10px; border-radius: 6px; line-height: 1.5;
}
nav.toc a:hover { background: var(--code-bg); }
nav.toc a.toc-l2 { font-weight: 500; margin-top: 6px; }
nav.toc a.toc-l3 { color: var(--muted-fg); padding-left: 26px; }
main { flex: 1; min-width: 0; padding: 36px 44px 120px; max-width: 900px; }
h1 { font-size: 26px; line-height: 1.4; margin: 0 0 6px; }
.doc-sub { color: var(--muted-fg); font-size: 13px; margin-bottom: 28px; }
h2 { font-size: 21px; margin: 44px 0 14px; padding-top: 26px; border-top: 1px solid var(--border); }
h2:first-of-type { border-top: none; padding-top: 0; }
h3 { font-size: 17px; margin: 30px 0 10px; }
h4 { font-size: 15px; margin: 22px 0 8px; }
p, li { line-height: 1.9; }
table.table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 13.5px; }
.table th, .table td { border: 1px solid var(--border); padding: 7px 11px; text-align: left; vertical-align: top; }
.table th { background: var(--th-bg); font-weight: 600; }
pre {
  background: var(--code-bg); border: 1px solid var(--border); border-radius: 10px;
  padding: 14px 16px; overflow-x: auto; line-height: 1.6;
}
pre code { background: none; padding: 0; font-size: 13px; }
code { background: var(--code-bg); border-radius: 4px; padding: 1px 6px; font-size: .92em; }
blockquote {
  margin: 14px 0; padding: 4px 18px; color: var(--muted-fg);
  border-left: 3px solid var(--accent); background: var(--code-bg); border-radius: 0 8px 8px 0;
}
blockquote p { margin: 8px 0; }
img { max-width: 100%; border-radius: 10px; border: 1px solid var(--border); display: block; margin: 14px auto; }
hr { border: none; border-top: 1px solid var(--border); margin: 30px 0; }
#backtop {
  position: fixed; right: 26px; bottom: 30px; display: none;
  width: 42px; height: 42px; border-radius: 50%; border: 1px solid var(--border);
  background: var(--code-bg); color: var(--fg); font-size: 18px; cursor: pointer;
}
#backtop.show { display: block; }
@media (max-width: 960px) {
  .layout { flex-direction: column; }
  nav.toc { position: static; width: auto; max-height: none; border-right: none; border-bottom: 1px solid var(--border); padding: 16px 20px; }
  main { padding: 24px 20px 90px; }
}
@media print {
  nav.toc, #backtop { display: none; }
  main { max-width: none; padding: 0; }
  body { background: #fff; color: #000; }
}
</style>
</head>
<body>
<div class="layout">
  <nav class="toc">
    <div class="toc-title">目 录</div>
    __TOC__
  </nav>
  <main>
    <h1>__TITLE__</h1>
    <p class="doc-sub">WorkBuddy 教师实战蓝皮书 · 专题教程　｜　独立阅读版，双击即开、可整文件转发</p>
    __CONTENT__
  </main>
</div>
<button id="backtop" aria-label="返回顶部" onclick="scrollTo({top:0,behavior:'smooth'})">↑</button>
<script>
const btn = document.getElementById('backtop');
addEventListener('scroll', () => btn.classList.toggle('show', scrollY > 600), { passive: true });
</script>
</body>
</html>
"""

page = PAGE.replace("__TITLE__", DOC_TITLE).replace("__TOC__", toc_html).replace("__CONTENT__", html)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(page)
print(f"写出: {OUT_PATH}")
print(f"大小: {os.path.getsize(OUT_PATH) / 1024:.0f} KB，目录条目 {len(toc)} 条")
