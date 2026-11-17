# -*- coding: utf-8 -*-
"""把极简教程正文 + 编号配图合成图文预览（相对路径版 + 图片内嵌独立版）。"""
from pathlib import Path
import base64
import html
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC_NAME = sys.argv[1] if len(sys.argv) > 1 else "极简教程_4步生成希沃原生课件.md"
TITLE = sys.argv[2] if len(sys.argv) > 2 else "workbuddy+希沃：4步直接在希沃里做出原生课件"
STEM = Path(SRC_NAME).stem
MD = ROOT / SRC_NAME
OUT = ROOT / (STEM + "_预览.html")
OUT_ALONE = ROOT / (STEM + "_预览_独立版.html")
IMGDIR = ROOT / "极简教程_配图"

imgs = {p.name[:2]: p.name for p in sorted(IMGDIR.glob("*.png"))}
CAPTIONS = {
    "01": "成品：《赵州桥》思维导图页",
    "02": "技能市场 SkillHub 搜「希沃」，第一项即希沃白板助手",
    "03": "技能详情 v1.0.2，开关已启用",
    "04": "左侧「技能」菜单里的另一个入口",
    "05": "连接成功：7916 端口、工具列表校验通过、保持备课态",
    "06": "连接状态反转：重启客户端后 tools/list 才就绪",
    "07": "阶段② 四条教学目标卡片",
    "08": "阶段③ 大纲硬约束：8 页内容 + 1 页封面",
    "09": "汉字卡控件：喇叭 / 连续 / 分步，需点「开始授课」",
    "10": "判断对错活动（备课态模板预览）",
}

raw = MD.read_text(encoding="utf-8")
if "# 正文" in raw and "# 发布说明" in raw:
    body = raw.split("# 正文", 1)[1].split("# 发布说明", 1)[0]
else:
    body = re.sub(r"^#\s+.*\n", "", raw, count=1)


def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def figure(num):
    name = imgs.get(num)
    if not name:
        return '<p class="miss">⚠ 缺图：配图 %s</p>' % num
    return ('<figure><img src="极简教程_配图/%s" alt="配图 %s">'
            '<figcaption>配图 %s · %s</figcaption></figure>'
            % (html.escape(name), num, num, html.escape(CAPTIONS.get(num, ""))))


lines = body.splitlines()
parts = []
i = 0
while i < len(lines):
    s = lines[i].strip()
    if not s:
        i += 1
        continue
    m = re.match(r"^【配图\s*(\d{2})】$", s)
    if m:
        parts.append(figure(m.group(1)))
        i += 1
        continue
    if s.startswith("```"):
        buf = []
        i += 1
        while i < len(lines) and not lines[i].strip().startswith("```"):
            buf.append(lines[i])
            i += 1
        i += 1
        parts.append("<pre><code>%s</code></pre>" % html.escape("\n".join(buf)))
        continue
    if s.startswith("> "):
        buf = []
        while i < len(lines) and lines[i].strip().startswith("> "):
            buf.append(lines[i].strip()[2:])
            i += 1
        parts.append("<blockquote>%s</blockquote>" % "<br>".join(inline(x) for x in buf))
        continue
    if s.startswith("| ") and i + 1 < len(lines) and re.match(r"^\|[\s\-|]+\|$", lines[i + 1].strip()):
        header = [x.strip() for x in s.strip("|").split("|")]
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip().startswith("| "):
            rows.append([x.strip() for x in lines[i].strip().strip("|").split("|")])
            i += 1
        th = "".join("<th>%s</th>" % inline(x) for x in header)
        tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(x) for x in r) for r in rows)
        parts.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (th, tr))
        continue
    if s.startswith("- "):
        buf = []
        while i < len(lines) and lines[i].strip().startswith("- "):
            buf.append("<li>%s</li>" % inline(lines[i].strip()[2:]))
            i += 1
        parts.append("<ul>%s</ul>" % "".join(buf))
        continue
    if s.startswith("## "):
        parts.append("<h2>%s</h2>" % inline(s[3:]))
        i += 1
        continue
    if s == "---":
        parts.append("<hr>")
        i += 1
        continue
    parts.append("<p>%s</p>" % inline(s))
    i += 1

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#EDEAE3;font-family:"Microsoft YaHei","PingFang SC",sans-serif;color:#26312F}
.wrap{max-width:700px;margin:0 auto;background:#FFFFFF;padding:34px 32px 56px;box-shadow:0 4px 24px rgba(0,0,0,.08)}
h1{font-size:29px;line-height:1.4;margin:0 0 8px}
.meta{font-size:13px;color:#8A8A82;border-bottom:1px solid #E5DFD0;padding-bottom:16px;margin-bottom:26px}
h2{font-size:22px;margin:34px 0 14px;padding-left:11px;border-left:4px solid #B4472B}
p{font-size:16px;line-height:1.9;margin:0 0 14px}
strong{color:#B4472B}
code{background:#F5F1E8;padding:2px 6px;border-radius:4px;font-size:14px;color:#3F5A62}
pre{background:#26312F;color:#F5F1E8;padding:16px 18px;border-radius:8px;overflow-x:auto;line-height:1.7;font-size:14px;margin:16px 0}
pre code{background:none;color:inherit;padding:0}
blockquote{background:#FBF3EF;border-left:4px solid #B4472B;padding:12px 16px;margin:16px 0;font-size:15px;line-height:1.85;color:#3F5A62}
blockquote code{background:#F3E7E1}
ul{padding-left:22px;margin:0 0 16px}li{font-size:16px;line-height:1.9;margin-bottom:4px}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th,td{border:1px solid #E5DFD0;padding:9px 12px;text-align:left;line-height:1.7}
th{background:#FBF8F2;font-weight:700}
figure{margin:22px 0}figure img{width:100%;display:block;border:1px solid #E5DFD0;border-radius:6px}
figcaption{font-size:13px;color:#8A8A82;text-align:center;margin-top:8px}
hr{border:0;border-top:1px solid #E5DFD0;margin:28px 0}
.miss{color:#B4472B;background:#FBF0EC;padding:10px 14px;border-radius:6px}
</style></head><body><div class="wrap">
<h1>__TITLE__</h1>
<div class="meta">极简操作教程 · 配图 01–10 按步骤顺序编号</div>
__BODY__
</div></body></html>"""

doc = TEMPLATE.replace("__BODY__", "\n".join(parts)).replace("__TITLE__", html.escape(TITLE))
OUT.write_text(doc, encoding="utf-8")


def embed(m):
    path = ROOT / m.group(1)
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return 'src="data:image/png;base64,%s"' % data


alone = re.sub(r'src="(极简教程_配图/[^"]+)"', embed, doc)
OUT_ALONE.write_text(alone, encoding="utf-8")

refs = re.findall(r"配图 (\d{2})", doc)
print("✓", OUT.name, round(OUT.stat().st_size / 1024), "KB")
print("✓", OUT_ALONE.name, round(OUT_ALONE.stat().st_size / 1024 / 1024, 2), "MB")
print("  图片引用顺序:", re.findall(r'src="极简教程_配图/(\d{2})-', doc))
print("  缺图提示:", doc.count("缺图"))
