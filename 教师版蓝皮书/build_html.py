#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把正式版 Markdown 构建成单文件 HTML（图片压缩后 base64 内嵌，浏览器双击即看）。

用法: python build_html.py
输入: WorkBuddy教师实战蓝皮书_正式版.md（由 build_official.py 生成）
输出: WorkBuddy教师实战蓝皮书_正式版.html

要点：代码块与图片先换成占位符再转 Markdown，最后回填——
避免缩进/列表上下文把图片行误变成代码块。
"""
import base64
import io
import os
import re
import sys

import markdown
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "WorkBuddy教师实战蓝皮书_正式版.md")
OUT = os.path.join(BASE, "WorkBuddy教师实战蓝皮书_正式版.html")
MAX_W = 1000          # 图片最大宽度（px）
QUALITY = 80          # 有损压缩质量

IMG_PAT = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
FENCE_PAT = re.compile(r'```.*?```', re.S)


def img_to_dataurl(path):
    if not os.path.isfile(path):
        return None
    try:
        im = Image.open(path)
        if im.mode in ("RGBA", "P", "LA"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            im = im.convert("RGBA")
            bg.paste(im, mask=im.split()[-1])
            im = bg
        elif im.mode != "RGB":
            im = im.convert("RGB")
        if im.width > MAX_W:
            h = round(im.height * MAX_W / im.width)
            im = im.resize((MAX_W, h), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=QUALITY, method=4)
        return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    except Exception as e:
        print("  [图] 失败 %s: %s" % (path, e))
        return None


def main():
    if not os.path.exists(SRC):
        print("找不到 %s，先运行 build_official.py" % SRC)
        sys.exit(1)
    text = open(SRC, encoding="utf-8").read()

    # ---- 0. 保护代码块 ----
    fences = []

    def stash_fence(m):
        fences.append(m.group(0))
        return "\n@@FENCE%d@@\n" % (len(fences) - 1)

    text = FENCE_PAT.sub(stash_fence, text)

    # ---- 1. 图片 → 占位符（收集 dataurl）----
    dataurls, missing = [], []

    def stash_img(m):
        alt, src = m.group(1), m.group(2)
        if src.startswith("http"):
            return m.group(0)
        d = img_to_dataurl(os.path.join(BASE, src))
        if d is None:
            missing.append(src)
            return "*（配图缺失：%s）*" % src
        dataurls.append(d)
        return "\n@@IMG%d@@\n" % (len(dataurls) - 1)

    text = IMG_PAT.sub(stash_img, text)
    print("[1] 图片收集 %d 张%s" % (len(dataurls),
          ("　缺失: " + ", ".join(missing)) if missing else ""))

    # ---- 2. Markdown → HTML ----
    body = markdown.markdown(
        text,
        extensions=["tables", "sane_lists"],
        output_format="html5",
    )
    print("[2] 正文转换完成 %.1f KB" % (len(body) / 1024))

    # ---- 3. 回填图片：<p>@@IMGn@@</p> 或裸占位 → <img> ----
    def restore_img(m):
        i = int(m.group(1))
        return '<img src="%s" alt="">' % dataurls[i]

    body = re.sub(r'(?:<p>)?\s*@@IMG(\d+)@\s*(?:</p>)?', restore_img, body)

    # ---- 4. 回填代码块（markdown 会把占位行包成 <p>，剥掉）----
    def restore_fence(m):
        i = int(m.group(1))
        code = fences[i]
        lang = re.match(r'```(\w+)', code)
        inner = re.sub(r'^```\w*\n?', '', code).rstrip('`').rstrip('\n')
        cls = ' class="lang-%s"' % lang.group(1) if lang else ''
        return '<pre><code%s>%s</code></pre>' % (
            cls, markdown.markdown(inner, output_format="html5")
            if False else escape_html(inner))

    body = re.sub(r'(?:<p>)?\s*@@FENCE(\d+)@\s*(?:</p>)?', restore_fence, body)
    print("[3] 回填完成：图 %d / 代码块 %d" % (len(dataurls), len(fences)))

    # ---- 5. 目录 ----
    used = {}

    def slugify(t):
        s = re.sub(r"\s+", "-", t.strip())
        key = s or "h"
        used[key] = used.get(key, 0) + 1
        return key if used[key] == 1 else "%s-%d" % (key, used[key])

    toc = []

    def head(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        t = re.sub(r"<[^>]+>", "", inner)
        level = int(tag[1])
        if level <= 2:
            sid = slugify(t)
            toc.append((level, t, sid))
            return '<%s%s id="%s">%s</%s>' % (tag, attrs, sid, inner, tag)
        return m.group(0)

    body = re.sub(r"<(h[12])([^>]*)>(.*?)</\1>", head, body, flags=re.S)
    toc_html = "".join(
        '<a class="lv%d" href="#%s">%s</a>' % (lv, sid, t)
        for lv, t, sid in toc)
    print("[4] 目录 %d 条" % len(toc))

    html = TEMPLATE.replace("__TOC__", toc_html).replace("__BODY__", body)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("[5] 输出 %s（%.1f MB）" % (os.path.basename(OUT),
                                     os.path.getsize(OUT) / 1024 / 1024))


def escape_html(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>WorkBuddy 教师实战蓝皮书 · 正式版（2026 年 10 月）</title>
<style>
:root{--ink:#1f2937;--mut:#6b7280;--line:#e5e7eb;--acc:#2f6fed;--bg:#f7f8fa}
*{box-sizing:border-box}
body{margin:0;font-family:"Microsoft YaHei","PingFang SC",system-ui,sans-serif;
  color:var(--ink);background:var(--bg);line-height:1.75;font-size:15.5px}
#side{position:fixed;top:0;left:0;bottom:0;width:270px;overflow-y:auto;
  background:#fff;border-right:1px solid var(--line);padding:18px 0 40px}
#side .brand{font-weight:800;font-size:15px;padding:0 16px 10px;border-bottom:1px solid var(--line);margin-bottom:8px}
#side a{display:block;padding:4px 16px 4px 26px;color:var(--mut);text-decoration:none;
  font-size:12.5px;border-left:3px solid transparent;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#side a.lv2{padding-left:38px}
#side a:hover{color:var(--acc);border-left-color:var(--acc);background:#f3f6ff}
#side a.lv1{font-weight:700;color:var(--ink);margin-top:8px;font-size:13px}
#main{margin-left:270px;max-width:900px;padding:36px 48px 120px;background:var(--bg)}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:34px 44px;
  box-shadow:0 1px 3px rgba(15,23,42,.05)}
h1{font-size:24px;border-bottom:2px solid var(--acc);padding-bottom:10px;margin-top:38px}
h1:first-child{margin-top:0}
h2{font-size:19px;margin-top:34px;border-left:5px solid var(--acc);padding-left:10px}
h3{font-size:16.5px;margin-top:26px}
h4{font-size:15px;margin-top:20px}
p{margin:12px 0}
blockquote{margin:14px 0;padding:10px 18px;background:#f2f6ff;border-left:4px solid var(--acc);
  border-radius:0 8px 8px 0;color:#27355c}
blockquote p{margin:6px 0}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13.5px;
  display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:7px 11px;text-align:left;vertical-align:top}
th{background:#eef2fb;font-weight:700}
tr:nth-child(even) td{background:#fafbfd}
code{background:#eef1f6;border-radius:4px;padding:1px 6px;font-size:13px;
  font-family:Consolas,"Courier New",monospace}
pre{background:#101828;color:#dbe4f3;border-radius:10px;padding:16px 18px;overflow-x:auto;line-height:1.6}
pre code{background:none;color:inherit;padding:0;font-size:12.8px}
img{max-width:100%;border-radius:8px;border:1px solid var(--line);margin:8px auto;
  display:block}
hr{border:none;border-top:1px dashed #c9d2e0;margin:30px 0}
a{color:var(--acc)}
ul,ol{padding-left:24px}
li{margin:5px 0}
@media print{#side{display:none}#main{margin:0;padding:0}.card{border:none;padding:0}}
@media (max-width:900px){#side{display:none}#main{margin:0;padding:16px}.card{padding:20px}}
</style>
</head>
<body>
<nav id="side"><div class="brand">📘 WorkBuddy 教师实战蓝皮书<br><small style="font-weight:400">正式版 · 2026 年 10 月</small></div>__TOC__</nav>
<main id="main"><div class="card">__BODY__</div></main>
</body>
</html>
"""

if __name__ == "__main__":
    main()
