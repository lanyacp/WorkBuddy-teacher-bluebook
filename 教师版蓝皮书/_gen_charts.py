#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成 4 张公众号架构图 HTML（暖色系，与封面统一），供 Edge 截图。"""
import os

OUT = '_charts'
os.makedirs(OUT, exist_ok=True)

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1000px; overflow:hidden; }
body {
  font-family:"Microsoft YaHei","PingFang SC",sans-serif;
  background:#FFFDF8; color:#33302B; position:relative;
}
.page { width:1000px; position:relative; background:
  radial-gradient(circle at 88% 8%, rgba(232,131,74,.09) 0, rgba(232,131,74,0) 32%),
  radial-gradient(circle at 8% 92%, rgba(91,154,139,.09) 0, rgba(91,154,139,0) 30%),
  #FFFDF8; }
.topbar { position:absolute; top:0; left:0; right:0; height:9px;
  background:linear-gradient(90deg,#E8834A 0%,#D4A84B 50%,#5B9A8B 100%); }
.wrap { padding:52px 60px; }
.kicker { font-size:15px; letter-spacing:4px; color:#B0653A; font-weight:700; }
h1 { font-size:42px; font-weight:800; letter-spacing:1px; margin-top:12px; }
.lead { font-size:18px; color:#7A7167; margin-top:12px; line-height:1.6; }
.foot { margin-top:34px; padding-top:16px; border-top:1px solid #EFE6D8;
  display:flex; justify-content:space-between; font-size:14px; color:#A9A096; letter-spacing:1px; }
"""

def page(h, body, foot_l, foot_r):
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><style>
{CSS}
html,body {{ height:{h}px; }} .page {{ height:{h}px; }}
</style></head><body><div class="page"><div class="topbar"></div>
<div class="wrap">{body}
<div class="foot"><span>{foot_l}</span><span>{foot_r}</span></div>
</div>
</div></body></html>"""

# ---------------- 图 1　容量总览 ----------------
cards = [
    ('583', '页', '完整 PDF', '#D9743C'),
    ('26', '章', '四篇正文', '#5B9A8B'),
    ('10', '个', '实操专题', '#C98A2E'),
    ('5', '个', '速查附录', '#B0653A'),
    ('50', '条', '指令模板', '#5B9A8B'),
    ('161', '张', '真实配图', '#D9743C'),
]
c1 = '<div class="kicker">CONTENT AT A GLANCE</div><h1>这本书有多大</h1>'
c1 += '<div class="lead">写了两个月，把两年攒下的东西整理成一本能照着做的书。</div>'
c1 += '<div class="grid">'
for num, unit, label, color in cards:
    c1 += f'''<div class="card">
      <div class="num" style="color:{color}">{num}<span class="unit">{unit}</span></div>
      <div class="lbl">{label}</div></div>'''
c1 += '</div>'
EXTRA1 = """
.grid { display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin-top:38px; }
.card { background:#fff; border:1px solid #EFE6D8; border-radius:14px;
  padding:26px 20px 22px; text-align:center; }
.num { font-size:66px; font-weight:800; line-height:1; letter-spacing:-2px; }
.unit { font-size:20px; font-weight:700; margin-left:6px; letter-spacing:0; }
.lbl { margin-top:14px; font-size:17px; color:#8A8075; letter-spacing:2px; }
"""
html1 = page(720, c1, 'WorkBuddy 教师实战蓝皮书 · 2026 年 11 月版', '583 页 / 离线可读').replace('</style>', EXTRA1 + '</style>')

# ---------------- 图 2　四篇架构 ----------------
parts = [
    ('01', '6', '先把工具用起来', '第 1–6 章', '安装登录 · 下指令 · Skill · Word/Excel/PPT/PDF', '#E8834A', '#FBEDE1'),
    ('02', '10', '教学全流程工作流', '第 7–16 章', '备课 · 课件 · 作业 · 出卷 · 批改 · 错题本 · 家校', '#C98A2E', '#FBF2DF'),
    ('03', '6', '教研行政与成长', '第 17–22 章', '教研 · 听评课 · 培训微课 · 文书 · 课题 · 档案', '#5B9A8B', '#E7F1EE'),
    ('04', '4', '进阶与区域落地', '第 23–26 章', '定时任务 · 造 Skill · 多 Agent · 从个人到区域', '#B0653A', '#F7E9DC'),
]
c2 = '<div class="kicker">BOOK STRUCTURE</div><h1>四篇二十六章，按每天要做的事排</h1>'
c2 += '<div class="rows">'
for idx, n, title, rng, desc, color, bg in parts:
    c2 += f'''<div class="row" style="background:{bg}">
      <div class="big" style="color:{color}">{n}<span>章</span></div>
      <div class="mid"><div class="idx">第 {idx} 篇</div><div class="ttl">{title}</div></div>
      <div class="rgt"><div class="rng">{rng}</div><div class="desc">{desc}</div></div>
    </div>'''
c2 += '</div>'
EXTRA2 = """
.rows { margin-top:30px; display:flex; flex-direction:column; gap:14px; }
.row { display:flex; align-items:center; border-radius:14px; padding:20px 26px; }
.big { width:130px; font-size:56px; font-weight:800; line-height:1; }
.big span { font-size:18px; margin-left:5px; font-weight:700; }
.mid { flex:1; border-left:1px solid rgba(0,0,0,.08); padding-left:26px; }
.idx { font-size:14px; color:#9A9085; letter-spacing:2px; }
.ttl { font-size:24px; font-weight:700; margin-top:5px; }
.rgt { text-align:right; max-width:400px; }
.rng { font-size:15px; color:#B0653A; font-weight:700; }
.desc { font-size:14px; color:#7A7167; margin-top:7px; line-height:1.5; }
"""
html2 = page(760, c2, '四篇正文 · 合计 26 章', '第 6 章是全书地基').replace('</style>', EXTRA2 + '</style>')

# ---------------- 图 3　教学全流程链路 ----------------
flow = ['备课', '课件', '分层作业', '出卷', '批改', '错题本', '阅读写作', '英语听说', '理化生', '家校共育']
c3 = '<div class="kicker">TEACHING WORKFLOW</div><h1>第二篇十章，串成一节课的顺序</h1>'
c3 += '<div class="lead">从拿到课标到把结果反馈给家长，一章一件事，每章都写清怎么提需求、怎么验收。</div>'
for row in range(2):
    c3 += '<div class="chain">'
    for j in range(5):
        i = row * 5 + j
        name = flow[i]
        c3 += f'<div class="step"><div class="n">{i+1:02d}</div><div class="s">{name}</div></div>'
        if j < 4:
            c3 += '<div class="arrow">›</div>'
    c3 += '</div>'
c3 += '<div class="bar"><span class="bignum">10</span><span class="bartext">章连起来，就是一位教师从备课到反馈的完整动线</span></div>'
EXTRA3 = """
.chain { display:flex; align-items:center; justify-content:space-between;
  flex-wrap:nowrap; gap:6px; margin-top:36px; }
.chain + .chain { margin-top:14px; }
.step { width:150px; flex:none; background:#fff; border:1px solid #EFE6D8;
  border-radius:12px; padding:18px 8px; text-align:center; }
.n { font-size:26px; font-weight:800; color:#D9743C; }
.s { font-size:16px; font-weight:700; margin-top:6px; color:#4A443E; }
.arrow { font-size:24px; color:#D9BBA6; font-weight:700; }
.bar { margin-top:32px; background:#FBEDE1; border-radius:14px; padding:22px 30px;
  display:flex; align-items:center; gap:24px; }
.bignum { font-size:60px; font-weight:800; color:#B0653A; line-height:1; }
.bartext { font-size:19px; color:#7A5A45; font-weight:600; }
"""
html3 = page(750, c3, '第二篇 · 第 7–16 章', '10 章 / 一条动线').replace('</style>', EXTRA3 + '</style>')

# ---------------- 图 4　专题与附录 ----------------
topics_l = ['3D 教学模型', 'MG 动画与代码生成视频', '360 全景网页·极简流程', '360 全景网页·完整版', '实时互动数字人']
topics_r = ['微课视频制作全流程', '希沃白板原生课件', '教学资源下载', '教师用 WorkBuddy 开发工具', '教师个人工作台搭建实录']
appendix = [('A', '50 条指令模板'), ('B', '场景速查表'), ('C', '红线清单'), ('D', '增补素材与提示词'), ('E', '2026 年 10 月补遗')]

c4 = '<div class="kicker">TOPICS & APPENDIX</div><h1>十个专题，五个附录</h1>'
c4 += '<div class="two"><div class="col"><div class="ch"><span class="cn">10</span> 个实操专题，专挑难做的</div>'
for t in topics_l:
    c4 += f'<div class="item"><i></i>{t}</div>'
c4 += '</div><div class="col"><div class="ch" style="visibility:hidden">占位</div>'
for t in topics_r:
    c4 += f'<div class="item"><i></i>{t}</div>'
c4 += '</div></div>'
c4 += '<div class="apx"><div class="ahead"><span class="cn">5</span> 个附录，先读红线清单</div><div class="alist">'
for k, v in appendix:
    c4 += f'<div class="ac"><b>{k}</b><span>{v}</span></div>'
c4 += '</div></div>'
EXTRA4 = """
.two { display:flex; gap:26px; margin-top:26px; }
.col { flex:1; }
.ch { font-size:18px; font-weight:700; color:#B0653A; margin-bottom:14px; }
.cn { font-size:34px; font-weight:800; color:#D9743C; margin-right:6px; }
.item { display:flex; align-items:center; gap:10px; font-size:16px; color:#4A443E;
  padding:11px 14px; background:#fff; border:1px solid #EFE6D8; border-radius:9px; margin-bottom:9px; }
.item i { width:8px; height:8px; border-radius:50%; background:#E8834A; flex:none; }
.apx { margin-top:22px; background:#E7F1EE; border-radius:14px; padding:20px 24px; }
.ahead { font-size:18px; font-weight:700; color:#3D6B5E; margin-bottom:14px; }
.alist { display:flex; gap:10px; }
.ac { flex:1; background:#fff; border-radius:9px; padding:12px 10px; text-align:center; }
.ac b { display:block; font-size:24px; color:#5B9A8B; }
.ac span { display:block; font-size:13px; color:#7A7167; margin-top:5px; line-height:1.4; }
"""
html4 = page(890, c4, '10 专题 + 5 附录', '全部带实测截图').replace('</style>', EXTRA4 + '</style>')

files = [
    ('01_容量总览', 720, html1),
    ('02_四篇二十六章架构', 760, html2),
    ('03_教学全流程十章', 750, html3),
    ('04_十个专题五个附录', 890, html4),
]
for name, h, html in files:
    p = os.path.join(OUT, name + '.html')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print(name, '->', p, 'H=', h)
