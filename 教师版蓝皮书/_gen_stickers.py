#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成 6 张蓝皮书推广贴图 HTML（1080x1080 方图），供 Edge 截图为 PNG。

风格与封面 / 大数字架构图统一：#FFFDF8 底 + 橙 / 黄 / 青绿点缀。
关键内容全部用 flex 流内布局，不用 absolute 定位，避免无头截图裁切。
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, '_stickers')
os.makedirs(OUT, exist_ok=True)

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1080px; overflow:hidden; }
body { font-family:"Microsoft YaHei","PingFang SC",sans-serif; background:#FFFDF8; }
.page { width:1080px; height:1080px; position:relative; display:flex; flex-direction:column;
  padding:58px 76px 46px; background:#FFFDF8; color:#33302B; overflow:hidden; }
.page.warm { background:#D9743C; color:#fff; }
.topbar { position:absolute; top:0; left:0; right:0; height:11px;
  background:linear-gradient(90deg,#E8834A 0%,#D4A84B 52%,#5B9A8B 100%); }
.glow { position:absolute; width:640px; height:640px; border-radius:50%; right:-190px; top:-180px;
  background:radial-gradient(circle, rgba(232,131,74,.11), rgba(232,131,74,0) 70%); }
.glow2 { position:absolute; width:540px; height:540px; border-radius:50%; left:-210px; bottom:-190px;
  background:radial-gradient(circle, rgba(91,154,139,.11), rgba(91,154,139,0) 70%); }
.deco { position:absolute; top:150px; left:74px; opacity:.5; }
.head { display:flex; justify-content:space-between; align-items:center;
  font-size:16px; letter-spacing:2px; z-index:2; }
.brand { display:flex; align-items:center; gap:12px; font-weight:700; color:#B0653A; }
.brand i { width:9px; height:9px; border-radius:50%; background:#E8834A; display:block; }
.idx { font-size:15px; color:#A9A096; letter-spacing:3px; font-weight:700; }
.main { flex:1; display:flex; flex-direction:column; justify-content:center;
  align-items:center; text-align:center; z-index:2; }
.kicker { font-size:15px; letter-spacing:6px; font-weight:700; color:#B0653A; margin-bottom:24px; }
.big { font-size:186px; font-weight:800; line-height:1; letter-spacing:-8px; color:var(--c); }
.big .u { font-size:42px; letter-spacing:0; margin-left:16px; font-weight:700; }
.rule { width:88px; height:4px; border-radius:2px; background:var(--c);
  margin:36px 0 32px; opacity:.8; }
.title { font-size:44px; font-weight:800; line-height:1.55; letter-spacing:1px; }
.sub { font-size:20px; color:#8A8075; margin-top:26px; line-height:1.8; letter-spacing:1px; }
.foot { display:flex; justify-content:space-between; align-items:center;
  border-top:1px solid #EFE6D8; padding-top:22px; font-size:15px;
  color:#A9A096; letter-spacing:1px; z-index:2; }
/* 引号卡 */
.qmark { width:120px; height:88px; margin-bottom:22px; opacity:.34; }
.qtitle { font-size:56px; font-weight:800; line-height:1.55; margin-top:10px; letter-spacing:2px; }
.qsub { font-size:23px; color:#7A7167; margin-top:34px; letter-spacing:1px; }
/* 领取卡 */
.ctabig { font-size:74px; font-weight:800; line-height:1.35; letter-spacing:2px; }
.ctabig span { font-size:104px; color:#FFE6A8; }
.ctasub { font-size:27px; margin-top:34px; letter-spacing:2px; }
.ctasmall { font-size:18px; margin-top:18px; opacity:.78; letter-spacing:1px; }
/* 反白卡覆盖 */
.page.warm .brand, .page.warm .kicker, .page.warm .big,
.page.warm .rule, .page.warm .qmark { color:#fff; }
.page.warm .idx, .page.warm .sub, .page.warm .foot,
.page.warm .qsub { color:rgba(255,255,255,.84); }
.page.warm .foot { border-top-color:rgba(255,255,255,.35); }
.page.warm .brand i { background:#fff; }
.page.warm .rule { background:#fff; }
.page.warm .glow, .page.warm .glow2 { opacity:.3; }
"""

DECO = """<svg class="deco" width="120" height="120" viewBox="0 0 120 120">
  <path d="M60 14 l6 14 14 6 -14 6 -6 14 -6 -14 -14 -6 14 -6z" fill="#E8C9A8"/>
  <circle cx="20" cy="72" r="6" fill="#E8C9A8"/>
  <circle cx="98" cy="88" r="5" fill="#C7DED6"/>
  <circle cx="42" cy="104" r="4" fill="#E8C9A8"/>
</svg>"""


def page(no, inner, color, warm=False):
    cls = 'page warm' if warm else 'page'
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><style>
{CSS}
</style></head><body><div class="{cls}" style="--c:{color}">
  <div class="topbar"></div><div class="glow"></div><div class="glow2"></div>{DECO}
  <div class="head">
    <div class="brand"><i></i>赛博 Teacher 李 · 蓝皮书</div>
    <div class="idx">{no} / 06</div>
  </div>
  <div class="main">{inner}</div>
  <div class="foot">
    <span>WorkBuddy 教师实战蓝皮书</span><span>EDITION 2026 · 11</span>
  </div>
</div></body></html>"""


def numeric(kicker, big, unit, title, sub):
    return (f'<div class="kicker">{kicker}</div>'
            f'<div class="big">{big}<span class="u">{unit}</span></div>'
            f'<div class="rule"></div>'
            f'<div class="title">{title}</div>'
            f'<div class="sub">{sub}</div>')


cards = [
    ('01_主视觉_583页', '01', '#D9743C', False,
     numeric('TWO MONTHS OF WORK', '583', '页 PDF',
             '给县乡教师的<br>WorkBuddy 上手手册',
             '写了两个月 · 26 章 · 10 专题 · 161 张图')),

    ('02_26章_四篇正文', '02', '#5B9A8B', False,
     numeric('BOOK STRUCTURE', '26', '章',
             '四篇正文<br>按每天要做的事排',
             '先用起来 · 教学全流程 · 教研行政 · 进阶落地')),

    ('03_10专题5附录', '03', '#C98A2E', False,
     numeric('TOPICS & APPENDIX', '10', '个专题',
             '再加 5 个附录<br>难做的都写透了',
             '3D 模型 · 全景网页 · 数字人 · 微课 · 希沃白板')),

    ('04_161张图', '04', '#B0653A', False,
     numeric('REAL SCREENSHOTS', '161', '张图',
             '全部来自本机真实运行<br>做不出来的也写了',
             '图片全打包进 PDF，离线双击就能翻')),

    ('05_写给县乡学校', '05', '#3D6B5E', False,
     '<div class="kicker">WHY I WROTE IT</div>'
     '<svg class="qmark" viewBox="0 0 120 88">'
     '<path d="M8 80 C8 46 24 24 48 10 L53 30 C39 39 33 49 33 60 L49 60 L49 80 Z" fill="var(--c)"/>'
     '<path d="M66 80 C66 46 82 24 106 10 L111 30 C97 39 91 49 91 60 L107 60 L107 80 Z" fill="var(--c)"/>'
     '</svg>'
     '<div class="qtitle">县乡学校时间碎<br>设备杂、网不稳</div>'
     '<div class="qsub">书里每个做法，都按这个前提写过一遍</div>'),

    ('06_领取方式', '06', '#FFE6A8', True,
     '<div class="kicker">TAKE IT</div>'
     '<div class="ctabig">私信回复<br><span>蓝皮书</span></div>'
     '<div class="ctasub">583 页带图 PDF，直接发你</div>'
     '<div class="ctasmall">Gitee 与飞书地址见公众号文章</div>'),
]

for name, no, color, warm, inner in cards:
    p = os.path.join(OUT, name + '.html')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(page(no, inner, color, warm))
    print(name, '->', p)
