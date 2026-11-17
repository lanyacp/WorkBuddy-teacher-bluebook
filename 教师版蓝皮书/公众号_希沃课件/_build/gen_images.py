# -*- coding: utf-8 -*-
"""生成公众号《AI 做的课件，为什么在希沃里点不动》的全部配图，并按文章顺序编号归档。

有中文文字的图走 HTML + 本机 Chromium 渲染（避免 AI 生图写错字）；
截图类直接复用希沃客户端真实渲染图；控件说明与背景池用 Pillow 拼接。
"""
from pathlib import Path
import os
import shutil
import subprocess
import time

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "_build"
OUT = ROOT / "配图"
SRC = Path(r"D:/projects/WorkBuddy/2026-06-17-11-18-20/教师版蓝皮书/赵州桥示范课件")
PROOF = SRC / "_proof"
IMAGES = SRC / "images"

CHROME = (r"C:/Users/Administrator/AppData/Local/ms-playwright/"
          r"chromium_headless_shell-1228/chrome-headless-shell-win64/"
          r"chrome-headless-shell.exe")
FONT = "C:/Windows/Fonts/msyh.ttc"
FONTB = "C:/Windows/Fonts/msyhbd.ttc"

INK = "#26312F"
SUB = "#3F5A62"
RED = "#B4472B"
PAPER = "#FBF8F2"
LINE = "#E5DFD0"

OUT.mkdir(parents=True, exist_ok=True)
BUILD.mkdir(parents=True, exist_ok=True)


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def trim_bottom(path, bg, tol=8, pad=18):
    """裁掉模板底部多留的纯背景色行。"""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    last = h - 1
    while last > 0:
        clean = True
        for x in range(0, w, 4):
            c = px[x, last]
            if any(abs(c[i] - bg[i]) > tol for i in range(3)):
                clean = False
                break
        if not clean:
            break
        last -= 1
    end = min(h, last + 1 + pad)
    if end < h:
        im.crop((0, 0, w, end)).save(path)
    return end


def render(name, body_html, w, h, bg_rgb):
    """HTML -> PNG。唯一可信的成功判据是 PNG 被写出来。"""
    doc = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{width:%dpx;background:%s;font-family:"Microsoft YaHei","PingFang SC",sans-serif;color:%s;overflow:hidden}
</style></head><body>%s</body></html>""" % (
        w, "#%02X%02X%02X" % bg_rgb, INK, body_html)
    hp = BUILD / (name + ".html")
    hp.write_text(doc, encoding="utf-8")
    out = OUT / name
    if out.exists():
        out.unlink()
    cmd = [CHROME, "--headless", "--no-sandbox", "--disable-gpu",
           "--hide-scrollbars", "--window-size=%d,%d" % (w, h),
           "--screenshot=" + str(out), hp.as_uri()]
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    deadline = time.time() + 25
    while time.time() < deadline:
        if out.exists() and out.stat().st_size > 0:
            time.sleep(0.5)
            break
        if p.poll() is not None:
            break
        time.sleep(0.3)
    p.kill()
    if not out.exists():
        raise RuntimeError("渲染失败：" + name)
    trim_bottom(out, bg_rgb)
    print("✓", name, Image.open(out).size)


def card(style, inner):
    return '<div style="%s">%s</div>' % (style, inner)


# ── 00 封面 900×383 ───────────────────────────────────────────────
cover = """
<div style="position:relative;width:900px;height:383px;background:#1E2B2A">
  <div style="position:absolute;left:0;top:0;width:13px;height:383px;background:#B4472B"></div>
  <div style="position:absolute;right:-140px;top:-110px;width:440px;height:440px;border:2px solid rgba(255,255,255,.10);border-radius:50%"></div>
  <div style="position:absolute;right:-55px;top:-25px;width:300px;height:300px;border:2px solid rgba(180,71,43,.45);border-radius:50%"></div>
  <div style="position:absolute;left:52px;top:40px;color:#E8AE7C;font-size:18px;letter-spacing:3px">工具实测 · 2026</div>
  <div style="position:absolute;left:52px;top:86px;color:#FFFFFF;font-size:52px;font-weight:700;line-height:1.30">AI 做的课件<br>为什么在希沃里点不动</div>
  <div style="position:absolute;left:52px;top:238px;color:#C9D2CE;font-size:24px">一次真实的 9 页原生课件实验</div>
  <div style="position:absolute;left:52px;top:312px;color:#8FA09B;font-size:17px">WorkBuddy × 希沃白板　|　汉字卡 · 思维导图 · 课堂活动</div>
</div>"""
render("00-封面-公众号首图.png", cover, 900, 383, (30, 43, 42))


# ── 01 痛点对比 ───────────────────────────────────────────────────
def compare_rows(items, mark, color):
    return "".join(
        '<div style="font-size:21px;color:%s;line-height:1.9;padding-left:4px">'
        '<span style="color:%s;font-weight:700;margin-right:8px">%s</span>%s</div>'
        % (INK, color, mark, t) for t in items)

left_items = ["汉字卡 → 退化成一张图片", "思维导图 → 不会逐级展开",
              "课堂活动 → 只剩静态截图", "导入之后，看着像课件，用起来像图片"]
right_items = ["汉字卡 → 能发音、能分步看笔顺", "思维导图 → 学生可以逐层点开",
               "课堂活动 → 真的能上台点选", "交互还在，才是教室里的课件"]

compare = """
<div style="padding:36px 40px 30px;width:1080px;background:%s">
  <div style="font-size:16px;color:%s;letter-spacing:2px;margin-bottom:10px">同样一句提示词</div>
  <div style="font-size:40px;font-weight:700;margin-bottom:28px">两种交付，差的不止一个格式</div>
  <div style="display:flex;gap:22px">
    <div style="flex:1;background:#FFFFFF;border:1px solid %s;border-radius:14px;padding:26px 24px">
      <div style="font-size:26px;font-weight:700;color:#7A7A72;margin-bottom:6px">路径 A · AI 交一份 PPT</div>
      <div style="font-size:18px;color:#999;margin-bottom:18px">生成 PPTX → 再导入希沃</div>
      %s
    </div>
    <div style="flex:1;background:#FFFFFF;border:2px solid %s;border-radius:14px;padding:26px 24px">
      <div style="font-size:26px;font-weight:700;color:%s;margin-bottom:6px">路径 B · AI 连进希沃</div>
      <div style="font-size:18px;color:#999;margin-bottom:18px">直接生成客户端原生 .enbx</div>
      %s
    </div>
  </div>
  <div style="margin-top:24px;background:%s;border-radius:10px;padding:16px 22px;font-size:22px;color:#FFFFFF;font-weight:700">
    分水岭不是「有没有生成课件」，而是「教室里的交互还在不在」
  </div>
</div>""" % (PAPER, SUB, LINE, compare_rows(left_items, "×", "#9A9A90"),
             RED, RED, compare_rows(right_items, "✓", RED), RED)
render("01-痛点对比-PPT与原生课件.png", compare, 1080, 620, (251, 248, 242))


# ── 02 链路 + 就绪判据 ────────────────────────────────────────────
nodes = [("① 一句课题", "《赵州桥》三下·第一课时"),
         ("② WorkBuddy", "希沃白板助手技能"),
         ("③ 本地 MCP", "127.0.0.1:7916"),
         ("④ 希沃客户端", "原生 .enbx 课件")]
node_html = ""
for i, (t, d) in enumerate(nodes):
    node_html += (
        '<div style="flex:1;background:#FFFFFF;border:1px solid %s;border-radius:12px;'
        'padding:20px 14px;text-align:center">'
        '<div style="font-size:23px;font-weight:700;margin-bottom:8px">%s</div>'
        '<div style="font-size:17px;color:%s">%s</div></div>' % (LINE, t, SUB, d))
    if i < len(nodes) - 1:
        node_html += ('<div style="width:34px;text-align:center;font-size:28px;'
                      'color:%s;padding-top:28px">→</div>' % RED)

criteria = ["客户端进程在跑", "本地端口可达", "MCP 握手成功", "tools/list 返回非空"]
crit_html = "".join(
    '<div style="flex:1;text-align:center;font-size:18px;color:%s">%s</div>'
    % (INK, c) for c in criteria)

chain = """
<div style="padding:36px 40px 30px;width:1080px;background:%s">
  <div style="font-size:16px;color:%s;letter-spacing:2px;margin-bottom:10px">这次换了个做法</div>
  <div style="font-size:40px;font-weight:700;margin-bottom:28px">不让 AI 交文件，让它直接连进客户端</div>
  <div style="display:flex;align-items:stretch">%s</div>
  <div style="margin-top:30px;background:#FFFFFF;border:1px solid %s;border-radius:12px;padding:20px 24px">
    <div style="font-size:20px;font-weight:700;margin-bottom:14px;color:%s">连没连上，看四步就绪判据</div>
    <div style="display:flex">%s</div>
  </div>
  <div style="margin-top:20px;font-size:26px;font-weight:700;color:%s">窗口开着 ≠ 连上　·　只有 tools/list 非空才算真就绪</div>
</div>""" % (PAPER, SUB, node_html, LINE, RED, crit_html, RED)
render("02-链路-WorkBuddy连进希沃.png", chain, 1080, 560, (251, 248, 242))


# ── 03 四阶段 ─────────────────────────────────────────────────────
stages = [("① 基本信息", "课题 / 学段 / 页数区间\n图片方案 / 硬约束"),
          ("② 教学目标", "按新课标对齐\n写清素养指向与检测方式"),
          ("③ 大纲设计", "选原生组件 + 环节大纲\n逐环节回看目标"),
          ("④ 分段生成", "补 pages.json → 校验\n出图 → 生成 → 回读")]
stage_html = ""
for i, (t, d) in enumerate(stages):
    stage_html += (
        '<div style="flex:1;background:#FFFFFF;border-top:5px solid %s;'
        'border-radius:0 0 12px 12px;padding:22px 18px;box-shadow:0 2px 10px rgba(0,0,0,.04)">'
        '<div style="font-size:25px;font-weight:700;margin-bottom:14px">%s</div>'
        '<div style="font-size:18px;color:%s;line-height:1.8;white-space:pre-line">%s</div>'
        '</div>' % (RED, t, SUB, d))
    if i < len(stages) - 1:
        stage_html += '<div style="width:16px"></div>'

flow = """
<div style="padding:36px 40px 30px;width:1080px;background:%s">
  <div style="font-size:16px;color:%s;letter-spacing:2px;margin-bottom:10px">备课不是一句话梭哈</div>
  <div style="font-size:40px;font-weight:700;margin-bottom:28px">四个检查点，每一步都先确认再前进</div>
  <div style="display:flex">%s</div>
  <div style="margin-top:26px;background:%s;border-radius:10px;padding:16px 22px;font-size:22px;color:#FFFFFF;font-weight:700">
    教学决策由人来定，重复劳动交给 AI
  </div>
</div>""" % (PAPER, SUB, stage_html, RED)
render("03-四阶段建课流程.png", flow, 1080, 520, (251, 248, 242))


# ── 06 汉字卡控件说明（Pillow 拼接）──────────────────────────────
zoom = Image.open(PROOF / "hanzi-card-zoom.png").convert("RGB")
zoom = zoom.resize((1080, 540), Image.LANCZOS)
panel = Image.new("RGB", (1080, 680), PAPER)
panel.paste(zoom, (0, 0))
d = ImageDraw.Draw(panel)
d.rectangle((0, 540, 1080, 680), fill=(255, 255, 255))
d.line((0, 540, 1080, 540), fill=(229, 223, 208), width=2)
notes = [("① 绿色小喇叭", "点一下朗读整个音节"),
         ("② 连续 / 分步", "笔顺演示，跟着书空"),
         ("③ 田字格虚线", "书写参照，不是贴图")]
for i, (t, sub) in enumerate(notes):
    x = 40 + i * 350
    d.text((x, 566), t, font=font(24, True), fill=RED)
    d.text((x, 606), sub, font=font(19), fill=INK)
d.text((40, 648), "备课态只显示静态预览 · 点「开始授课」后控件才激活",
       font=font(18), fill=SUB)
panel.save(OUT / "10-汉字卡控件说明.png")
print("✓ 10-汉字卡控件说明.png", panel.size)


# ── 10 背景池拼图 ─────────────────────────────────────────────────
bg_files = ["bg-a.png", "bg-b.png", "bg-c.png"]
labels = ["① 左侧留白 · 封面", "② 中间留白 · 讲解", "③ 中下部极安静 · 梳理"]
W, GAP, PAD = 330, 15, 30
thumb_h = int(W * 9 / 16)
canvas = Image.new("RGB", (1080, 410), PAPER)
d = ImageDraw.Draw(canvas)
d.text((PAD, 22), "同一节课的三张同源背景，画面跟着「镜头推近」走",
       font=font(28, True), fill=INK)
d.text((PAD, 62), "出图后按 16:9 物理裁切，右下角平台水印一并裁掉",
       font=font(18), fill=SUB)
for i, (f, lab) in enumerate(zip(bg_files, labels)):
    im = Image.open(IMAGES / f).convert("RGB").resize((W, thumb_h), Image.LANCZOS)
    x = PAD + i * (W + GAP)
    canvas.paste(im, (x, 100))
    d.rectangle((x, 100, x + W, 100 + thumb_h), outline=(229, 223, 208), width=2)
    d.text((x, 100 + thumb_h + 16), lab, font=font(19, True), fill=RED)
canvas.save(OUT / "09-三张同源背景池.png")
print("✓ 09-三张同源背景池.png", canvas.size)


# ── 11 回读与两个环境坑 ───────────────────────────────────────────
facts = [("9 页", "课件页数"), ("1280×720", "画布"),
         ("Edit", "备课模式"), ("4.98 MB", "已同步")]
fact_html = "".join(
    '<div style="width:50%%;padding:10px 0"><span style="font-size:28px;font-weight:700;color:%s">%s</span>'
    '<span style="font-size:17px;color:%s;margin-left:10px">%s</span></div>'
    % (RED, v, SUB, k) for v, k in facts)

pitfalls = ["注册表查询命令被安全策略拦截 → 运行时把启动程序指向真实安装路径",
            "AI 生图自带右下角水印 → 按 16:9 裁切时一并去掉"]
pit_html = "".join(
    '<div style="font-size:19px;color:%s;line-height:1.7;margin-bottom:12px">'
    '<span style="color:%s;font-weight:700">· </span>%s</div>' % (INK, RED, p)
    for p in pitfalls)

final = """
<div style="padding:34px 40px 28px;width:1080px;background:%s">
  <div style="font-size:16px;color:%s;letter-spacing:2px;margin-bottom:10px">落地之后，我回读了一遍</div>
  <div style="font-size:38px;font-weight:700;margin-bottom:24px">不能把「响应成功」当成「真的做好了」</div>
  <div style="display:flex;gap:22px">
    <div style="flex:1;background:#FFFFFF;border:1px solid %s;border-radius:12px;padding:20px 24px">
      <div style="display:flex;flex-wrap:wrap">%s</div>
    </div>
    <div style="flex:1;background:#FFFFFF;border:1px solid %s;border-radius:12px;padding:20px 24px">
      <div style="font-size:21px;font-weight:700;margin-bottom:14px">顺手记下两个环境坑</div>
      %s
    </div>
  </div>
  <div style="margin-top:22px;background:%s;border-radius:10px;padding:16px 22px;font-size:23px;color:#FFFFFF;font-weight:700">
    省下来的时间，磨你的教学设计
  </div>
</div>""" % (PAPER, SUB, LINE, fact_html, LINE, pit_html, RED)
render("11-回读与两个环境坑.png", final, 1080, 520, (251, 248, 242))


# ── 客户端真实截图按序归档 ────────────────────────────────────────
screens = [
    ("04-成品封面页-赵州桥.png", PROOF / "page-01.png"),
    ("05-汉字卡页.png", PROOF / "page-04.png"),
    ("07-思维导图页.png", PROOF / "page-06.png"),
    ("06-对照表页.png", PROOF / "page-05.png"),
    ("08-判断对错活动页.png", PROOF / "page-07.png"),
]
for name, src in screens:
    if not src.is_file():
        print("⚠ 缺图，跳过：", name, src)
        continue
    shutil.copy2(src, OUT / name)
    print("✓", name, Image.open(OUT / name).size)

print("\n=== 归档结果 ===")
for p in sorted(OUT.glob("*.png")):
    print(p.name, round(p.stat().st_size / 1024), "KB")
