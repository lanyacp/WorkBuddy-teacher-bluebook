# -*- coding: utf-8 -*-
"""把公众号正文 + 编号配图合成一个图文对照的本地预览页。"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "AI做的课件为什么在希沃里点不动.md"
OUT = ROOT / "图文预览.html"
IMGDIR = ROOT / "配图"

imgs = {p.name[:2]: p.name for p in sorted(IMGDIR.glob("*.png"))}
raw = MD.read_text(encoding="utf-8")
body = raw.split("# 正文（可直接发布）", 1)[1].split("# 推荐标签", 1)[0]

CAPTIONS = {
    "01": "同样一句提示词，两种交付差在哪",
    "02": "WorkBuddy → 本地 MCP → 希沃客户端，以及四步就绪判据",
    "03": "四个检查点，每一步先确认再前进",
    "04": "生成的 9 页课件 · 封面页实拍",
    "05": "「匠 / 慧 / 赵」原生汉字卡",
    "06": "两段话、两句关键句的同构对照表",
    "07": "思维导图总分总三支逐级展开",
    "08": "判断对错活动页（备课态预览）",
    "09": "三张同源水墨背景，镜头从远到近",
    "10": "三个控件：发音、笔顺、田字格",
    "11": "回读结果与两个环境坑",
}


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


parts = []
for line in body.splitlines():
    s = line.strip()
    if not s:
        continue
    if s.startswith("> 📌"):
        continue
    m = re.match(r"^【配图\s*(\d{2})】$", s)
    if m:
        num = m.group(1)
        name = imgs.get(num)
        if not name:
            parts.append('<p class="miss">⚠ 缺图：配图 %s</p>' % num)
            continue
        parts.append(
            '<figure><img src="配图/%s" alt="配图 %s">'
            '<figcaption>配图 %s · %s</figcaption></figure>'
            % (html.escape(name), num, num, html.escape(CAPTIONS.get(num, ""))))
        continue
    if s.startswith("## "):
        parts.append("<h2>%s</h2>" % inline(s[3:]))
        continue
    if s == "---":
        parts.append("<hr>")
        continue
    parts.append("<p>%s</p>" % inline(s))

cover = imgs.get("00")
cover_html = ('<img class="cover" src="配图/%s" alt="公众号首图">' % html.escape(cover)) if cover else ""

doc = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>图文预览 · AI 做的课件，为什么在希沃里点不动</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#EDEAE3;font-family:"Microsoft YaHei","PingFang SC",sans-serif;color:#26312F}
.wrap{max-width:720px;margin:0 auto;background:#FFFFFF;padding:36px 34px 60px;box-shadow:0 4px 24px rgba(0,0,0,.08)}
.cover{width:100%;display:block;border-radius:6px;margin-bottom:30px}
h1{font-size:30px;line-height:1.4;margin:0 0 8px}
.meta{font-size:14px;color:#8A8A82;border-bottom:1px solid #E5DFD0;padding-bottom:18px;margin-bottom:28px}
h2{font-size:22px;margin:38px 0 16px;padding-left:12px;border-left:4px solid #B4472B;line-height:1.4}
p{font-size:16px;line-height:1.9;margin:0 0 16px;letter-spacing:.2px}
strong{color:#B4472B}
code{background:#F5F1E8;padding:2px 6px;border-radius:4px;font-size:14px;color:#3F5A62}
figure{margin:26px 0}
figure img{width:100%;display:block;border:1px solid #E5DFD0;border-radius:6px}
figcaption{font-size:13px;color:#8A8A82;text-align:center;margin-top:9px;line-height:1.6}
hr{border:0;border-top:1px solid #E5DFD0;margin:30px 0}
.miss{color:#B4472B;background:#FBF0EC;padding:10px 14px;border-radius:6px}
</style></head><body><div class="wrap">
__COVER__
<h1>AI 做的课件，为什么在希沃里点不动</h1>
<div class="meta">公众号图文预览 · 图片按 00–11 编号插入 · 与「配图清单.md」一一对应</div>
__BODY__
</div></body></html>"""

doc = doc.replace("__COVER__", cover_html).replace("__BODY__", "\n".join(parts))

OUT.write_text(doc, encoding="utf-8")
print("✓", OUT, len(doc), "chars")
print("  图片引用数：", doc.count("<img"))
