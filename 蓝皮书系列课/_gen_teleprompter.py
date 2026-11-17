# -*- coding: utf-8 -*-
"""把逐字稿转成可滚动的提词器页面。"""
import html
import re
from pathlib import Path

BASE = Path(r"D:/projects/WorkBuddy/2026-06-17-11-18-20/蓝皮书系列课")
SRC = BASE / "开场与前三课时_逐字稿.md"
OUT = BASE / "开场与前三课时_提词器.html"

lines = SRC.read_text(encoding="utf-8").splitlines()
sections = []          # (level, title, [html lines])
cur = None

def esc(s):
    return html.escape(s, quote=False)

def mark(s):
    s = esc(s)
    s = re.sub(r"【待补｜([^】]+)】", r'<span class="blank">【待补｜\1】</span>', s)
    s = re.sub(r"`([^`]+)`", r'<span class="cmd">\1</span>', s)
    return s

for raw in lines:
    ln = raw.strip()
    if not ln:
        continue
    if ln.startswith("# "):
        cur = [1, ln[2:].strip(), []]
        sections.append(cur)
        continue
    if ln.startswith("## "):
        cur = [2, ln[3:].strip(), []]
        sections.append(cur)
        continue
    if cur is None:
        cur = [2, "说明", []]
        sections.append(cur)
    if ln == "---":
        continue
    if ln.startswith("> "):
        cur[2].append('<p class="note">%s</p>' % mark(ln[2:]))
        continue
    if ln.startswith("- ") or ln.startswith("| "):
        cur[2].append('<p class="bullet">%s</p>' % mark(ln))
        continue
    body = ln
    is_speech = body.startswith("**") and body.endswith("**")
    if is_speech:
        body = body[2:-2]
    if body.startswith("（") or body.startswith("("):
        cls = "cue"
    elif not is_speech:
        cls = "plain"
    else:
        cls = "speech"
    if "不念稿" in body or "静音" in body and "定格" in body:
        cls += " silent"
    cur[2].append('<p class="%s">%s</p>' % (cls, mark(body)))

nav = []
blocks = []
for i, (lvl, title, body) in enumerate(sections):
    if lvl == 1 and i == 0:
        continue
    sid = "s%d" % i
    short = title.split("｜")[0].replace("一、", "").replace("二、", "").strip()
    nav.append('<a href="#%s">%s</a>' % (sid, esc(short)))
    tag = "h2" if lvl == 1 else "h3"
    blocks.append('<section id="%s"><%s>%s</%s>%s</section>' % (
        sid, tag, esc(title), tag, "\n".join(body)))

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Microsoft YaHei","PingFang SC",sans-serif;background:#F7FAFB;color:#1B2A38;line-height:1.9}
body.night{background:#101D28;color:#E8F1F4}
nav{position:sticky;top:0;z-index:9;background:#12304A;padding:10px 18px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
nav a{color:#CFE4EA;text-decoration:none;font-size:14px;padding:5px 11px;border-radius:6px;background:rgba(255,255,255,.1)}
nav a:hover{background:#1E9E8A;color:#fff}
nav button{margin-left:auto;background:transparent;border:1px solid #8FE0D2;color:#8FE0D2;border-radius:6px;padding:5px 12px;font-size:14px;cursor:pointer}
.wrap{max-width:860px;margin:0 auto;padding:28px 26px 90px}
h1{font-size:30px;color:#12304A;margin-bottom:6px}
body.night h1{color:#8FE0D2}
.lead{font-size:16px;color:#6B8090;margin-bottom:26px}
body.night .lead{color:#9FB6C2}
section{margin-bottom:34px;scroll-margin-top:64px}
h2{font-size:26px;color:#12304A;border-left:7px solid #1E9E8A;padding-left:14px;margin:38px 0 18px}
h3{font-size:22px;color:#1E9E8A;margin:30px 0 14px}
body.night h2,body.night h3{color:#8FE0D2}
p{margin:0 0 14px}
.speech{font-size:25px;line-height:1.95;letter-spacing:.3px}
.cue{font-size:17px;color:#6B8090;background:#EAF1F4;border-left:4px solid #9BB2BF;padding:9px 14px;border-radius:0 6px 6px 0}
body.night .cue{background:#1A2E3C;color:#9FB6C2}
.cue.silent{background:#E8833A;color:#fff;border-left-color:#C96A25;font-size:19px;font-weight:700}
.plain{font-size:19px}
.note{font-size:15px;color:#7C92A0;background:#fff;border:1px dashed #D5E2E8;padding:10px 14px;border-radius:8px}
body.night .note{background:#162734;border-color:#2A4657}
.bullet{font-size:17px;color:#5A7180;padding-left:18px}
body.night .bullet{color:#9FB6C2}
.blank{background:#FDEBD8;color:#B85C1A;border-radius:4px;padding:1px 6px;font-size:.85em;font-weight:700}
.cmd{background:#E4F4F0;color:#12776A;border-radius:4px;padding:1px 6px;font-size:.9em}
body.night .blank{background:#5A3418;color:#FFD6A8}
body.night .cmd{background:#12463E;color:#8FE0D2}
"""

HTML = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>开场 + 前三课时 · 提词器</title>
<style>%s</style></head><body>
<nav>%s<button onclick="document.body.classList.toggle('night')">切换夜间</button></nav>
<div class="wrap">
<h1>开场 + 前三课时 · 提词器</h1>
<p class="lead">大字是要念出口的；灰色小字是画面与动作提示，不用念；橙色是待补素材位。两段「不念稿」的静音跟做，照着停住就行。</p>
%s
</div></body></html>""" % (CSS, "".join(nav), "\n".join(blocks))

OUT.write_text(HTML, encoding="utf-8")
print("teleprompter ->", OUT, "| sections =", len(blocks))
