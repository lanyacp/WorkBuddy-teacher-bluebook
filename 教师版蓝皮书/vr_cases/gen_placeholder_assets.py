#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成 360VR 专题两个案例的示意版全景素材（程序化绘制，非 AI 生成）。

用途：让 vr_cases/ 里的两个 index.html 拿到手就能跑通全流程；
     正式素材请按《专题_360VR全景互动网页.md》里的素材提示词
     用 AI 生成（或实拍）后同名覆盖 assets/ 下的 jpg。

运行：
    py gen_placeholder_assets.py

全景图为等矩形投影示意：水平方向用整数频率正弦叠加保证左右边缘无缝相接。
"""
import math
import os
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
W, H = 2048, 1024          # 2:1 等矩形
HORIZON = H // 2           # 视平线在正中
TAU = 2 * math.pi


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def v_gradient(img, y0, y1, c0, c1):
    """竖直渐变：y0 处 c0 → y1 处 c1"""
    d = ImageDraw.Draw(img)
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        d.line([(0, y), (W, y)], fill=lerp(c0, c1, (y - y0) / span))


def ridge_y(x, base, amps, freqs, phases):
    """山脊高度曲线：整数频率正弦叠加，保证 0 和 W 处等高（无缝环绕）"""
    h = base
    for a, k, p in zip(amps, freqs, phases):
        h += a * math.sin(TAU * k * x / W + p)
    return h


def draw_ridge(img, color, base, amps, freqs, phases, fill_to=HORIZON + 8):
    """沿视平线画一层山脊剪影"""
    d = ImageDraw.Draw(img)
    pts = [(x, HORIZON - ridge_y(x, base, amps, freqs, phases)) for x in range(0, W + 1, 4)]
    pts += [(W, fill_to), (0, fill_to)]
    d.polygon(pts, fill=color)


def cloud(img, cx, cy, s, color):
    """一团云：三个椭圆；cx 离边远时才画，避免跨界断裂"""
    if cx < 160 * s or cx > W - 160 * s:
        return
    d = ImageDraw.Draw(img)
    d.ellipse([cx - 90 * s, cy, cx + 90 * s, cy + 46 * s], fill=color)
    d.ellipse([cx - 140 * s, cy + 16 * s, cx + 30 * s, cy + 52 * s], fill=color)
    d.ellipse([cx - 20 * s, cy + 14 * s, cx + 150 * s, cy + 54 * s], fill=color)


def pine(img, cx, base_y, h, color):
    """一棵松：三层三角"""
    d = ImageDraw.Draw(img)
    for i, w in enumerate((0.55, 0.75, 1.0)):
        top = base_y - h * (1 - i * 0.28)
        half = h * 0.42 * w
        d.polygon([(cx, top), (cx - half, base_y - i * h * 0.22), (cx + half, base_y - i * h * 0.22)], fill=color)


def save(img, name):
    path = os.path.join(BASE, name)
    img.save(path, quality=82)
    print(f"  {name}  {os.path.getsize(path)//1024} KB")


def hotspot_icon():
    """热点图标：透明底 + 白圈 + 暖橙圆心（两个案例共用）"""
    s = 256
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([28, 28, s - 28, s - 28], fill=(255, 159, 67, 235), outline=(255, 255, 255, 255), width=14)
    d.ellipse([s // 2 - 26, s // 2 - 26, s // 2 + 26, s // 2 + 26], fill=(255, 255, 255, 255))
    for name in (os.path.join("lushan", "assets", "hotspot.png"),
                 os.path.join("fraction_castle", "assets", "hotspot.png")):
        full = os.path.join(BASE, name)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        img.save(full)
        print(f"  {name}  {os.path.getsize(full)//1024} KB")


# ---------------- 案例一：庐山四视角（水墨青绿） ----------------
INK = {"sky_top": (176, 208, 224), "sky_low": (238, 244, 238),
       "far": (168, 200, 188), "mid": (116, 164, 148),
       "near": (70, 118, 100), "rock": (86, 110, 104)}


def lushan_front():
    """正面远观：层峦叠嶂 + 云雾 + 晨光"""
    img = Image.new("RGB", (W, H))
    v_gradient(img, 0, HORIZON, INK["sky_top"], INK["sky_low"])
    v_gradient(img, HORIZON, H, (210, 224, 214), (238, 238, 230))
    d = ImageDraw.Draw(img)
    d.ellipse([W * 0.68, 130, W * 0.68 + 110, 240], fill=(252, 240, 214))      # 晨光淡日
    draw_ridge(img, INK["far"], 150, (36, 22), (3, 7), (0.5, 2.1))
    cloud(img, W * 0.22, HORIZON - 150, 1.1, (240, 246, 242))
    cloud(img, W * 0.55, HORIZON - 120, 0.9, (236, 244, 240))
    draw_ridge(img, INK["mid"], 88, (30, 18), (4, 9), (1.2, 4.0))
    d.rectangle([0, HORIZON - 34, W, HORIZON - 6], fill=(226, 236, 230))        # 山腰雾带
    draw_ridge(img, INK["near"], 34, (18, 12), (5, 11), (2.6, 0.7))
    d.rectangle([0, HORIZON - 14, W, HORIZON + 2], fill=(232, 240, 234))
    save(img, os.path.join("lushan", "assets", "lushan_front.jpg"))


def lushan_side():
    """侧面仰望：陡峭崖壁 + 崖上松树"""
    img = Image.new("RGB", (W, H))
    v_gradient(img, 0, HORIZON, INK["sky_top"], INK["sky_low"])
    v_gradient(img, HORIZON, H, (196, 214, 204), (228, 232, 222))
    cloud(img, W * 0.2, 150, 1.0, (242, 246, 244))
    cloud(img, W * 0.62, 210, 0.8, (238, 244, 240))
    draw_ridge(img, INK["far"], 90, (26, 16), (3, 8), (1.9, 3.3))
    d = ImageDraw.Draw(img)
    # 主崖壁：右半边拔地而起（跨到图外也无需环绕，剪影底边直落到视平线以下）
    cliff = [(W * 0.46, HORIZON + 8), (W * 0.52, 150), (W * 0.60, 96),
             (W * 0.72, 130), (W * 0.86, 250), (W, 330), (W, HORIZON + 8)]
    d.polygon(cliff, fill=INK["rock"])
    d.polygon([(W * 0.52, 160), (W * 0.60, 110), (W * 0.70, 140), (W * 0.80, 260)],
              fill=(120, 146, 138))                                             # 崖壁亮面
    for cx, cy, s in ((W * 0.55, 190, 46), (W * 0.63, 150, 40), (W * 0.76, 250, 52)):
        pine(img, cx, cy + s, s, (52, 92, 78))
    draw_ridge(img, INK["near"], 26, (14, 10), (6, 13), (0.8, 2.9))
    save(img, os.path.join("lushan", "assets", "lushan_side.jpg"))


def lushan_inside():
    """山间漫步：两侧峭壁夹山道"""
    img = Image.new("RGB", (W, H))
    v_gradient(img, 0, HORIZON, INK["sky_low"], (244, 246, 240))
    v_gradient(img, HORIZON, H, (188, 206, 196), (150, 170, 158))
    d = ImageDraw.Draw(img)
    d.ellipse([W * 0.47, 190, W * 0.47 + 90, 280], fill=(250, 246, 230))        # 头顶一线天光
    # 左右崖壁
    d.polygon([(0, 0), (W * 0.30, 60), (W * 0.36, 300), (W * 0.33, HORIZON), (0, HORIZON)], fill=INK["rock"])
    d.polygon([(W, 0), (W * 0.72, 80), (W * 0.66, 320), (W * 0.70, HORIZON), (W, HORIZON)], fill=(76, 102, 96))
    pine(img, W * 0.28, HORIZON - 20, 90, (48, 88, 74))
    pine(img, W * 0.70, HORIZON - 30, 100, (52, 92, 78))
    # 中央石板山道：梯形收向视平线
    d.polygon([(W * 0.34, HORIZON), (W * 0.66, HORIZON), (W * 0.86, H), (W * 0.14, H)], fill=(206, 200, 182))
    for i in range(6):                                                          # 石板横缝
        t = (i + 1) / 7.0
        y = HORIZON + (H - HORIZON) * (t * t)
        half = W * 0.16 + W * 0.20 * t
        d.line([(W / 2 - half, y), (W / 2 + half, y)], fill=(178, 172, 156), width=max(2, int(6 * t)))
    save(img, os.path.join("lushan", "assets", "lushan_inside.jpg"))


def lushan_top():
    """山顶俯瞰：云海 + 群峰 + 远处鄱阳湖"""
    img = Image.new("RGB", (W, H))
    v_gradient(img, 0, 380, INK["sky_top"], (222, 234, 230))
    v_gradient(img, 380, H, (238, 242, 240), (252, 252, 248))
    d = ImageDraw.Draw(img)
    d.ellipse([W * 0.15, 90, W * 0.15 + 100, 190], fill=(252, 248, 228))
    # 远山尖刺破云海
    for cx, top, wd in ((W * 0.12, 430, 150), (W * 0.30, 396, 190), (W * 0.52, 416, 170), (W * 0.74, 440, 150)):
        d.polygon([(cx - wd, 470), (cx, top), (cx + wd, 470)], fill=INK["far"])
    # 云海：成排起伏椭圆
    for i in range(9):
        y = 470 + i * 26
        for k in range(10):
            cx = 90 + k * 220 + (i % 2) * 110
            r = 130 + (i * 17) % 60
            d.ellipse([cx - r, y, cx + r, y + 90 + i * 10], fill=(248, 250, 248) if i % 2 else (238, 244, 242))
    # 远处湖面
    d.ellipse([W * 0.60, 600, W * 0.92, 700], fill=(176, 208, 216))
    # 前景脚下峰顶
    d.polygon([(W * 0.30, H), (W * 0.5, 760), (W * 0.72, H)], fill=INK["near"])
    pine(img, W * 0.50, 800, 70, (44, 82, 68))
    save(img, os.path.join("lushan", "assets", "lushan_top.jpg"))


# ---------------- 案例二：分数城堡（儿童绘本明亮） ----------------
def room(wall0, wall1, floor0, floor1):
    """通用室内底图：上墙下地"""
    img = Image.new("RGB", (W, H))
    v_gradient(img, 0, HORIZON, wall0, wall1)
    v_gradient(img, HORIZON, H, floor0, floor1)
    return img


def table(img, cx, top, wd, ht, wood=(222, 184, 138)):
    """木桌：桌面上一个矩形（示意）"""
    d = ImageDraw.Draw(img)
    d.rectangle([cx - wd / 2, top, cx + wd / 2, top + ht], fill=wood)
    d.rectangle([cx - wd / 2 + 24, top + ht, cx + wd / 2 - 24, H - 40], fill=(190, 150, 104))


def house(img, cx, base, wd, ht, roof):
    """小木屋：方身 + 三角顶 + 门"""
    d = ImageDraw.Draw(img)
    d.rectangle([cx - wd / 2, base - ht, cx + wd / 2, base], fill=(246, 232, 200))
    d.polygon([(cx - wd / 2 - 20, base - ht), (cx, base - ht - wd * 0.42), (cx + wd / 2 + 20, base - ht)], fill=roof)
    d.rectangle([cx - wd * 0.12, base - ht * 0.52, cx + wd * 0.12, base], fill=(150, 108, 72))


def forest_entrance():
    """森林入口：小路 + 5 个木屋"""
    img = Image.new("RGB", (W, H))
    v_gradient(img, 0, HORIZON, (150, 204, 238), (216, 238, 246))
    v_gradient(img, HORIZON, H, (168, 214, 150), (110, 176, 108))
    d = ImageDraw.Draw(img)
    d.ellipse([W * 0.78, 90, W * 0.78 + 120, 210], fill=(255, 232, 150))        # 太阳
    cloud(img, W * 0.25, 140, 1.0, (250, 252, 252))
    # 远处树线
    for k in range(16):
        cx = 60 + k * 132
        pine(img, cx, HORIZON - (30 + (k * 37) % 40), 90 + (k * 53) % 60, (74, 142, 92))
    # 5 个小屋沿路两侧
    houses = ((W * 0.16, HORIZON + 46, 190, 120, (232, 106, 90)),
              (W * 0.38, HORIZON + 20, 150, 96, (240, 160, 66)),
              (W * 0.62, HORIZON + 20, 150, 96, (106, 176, 226)),
              (W * 0.84, HORIZON + 46, 190, 120, (156, 120, 204)),
              (W * 0.52, HORIZON - 4, 110, 70, (226, 96, 138)))
    for cx, base, wd, ht, roof in houses:
        house(img, cx, base, wd, ht, roof)
    # 中央小路
    d.polygon([(W * 0.42, HORIZON), (W * 0.58, HORIZON), (W * 0.72, H), (W * 0.28, H)], fill=(238, 224, 186))
    save(img, os.path.join("fraction_castle", "assets", "forest_entrance.jpg"))


def share_workshop():
    """分享工坊：厨房 + 长桌 + 大圆饼"""
    img = room((252, 240, 214), (246, 226, 188), (214, 170, 118), (176, 132, 88))
    d = ImageDraw.Draw(img)
    d.rectangle([0, HORIZON - 150, W, HORIZON], fill=(240, 204, 158))           # 墙裙
    for k in range(6):
        d.line([(k * W / 5, HORIZON - 150), (k * W / 5, HORIZON)], fill=(226, 186, 136), width=6)
    table(img, W / 2, HORIZON + 60, 900, 70)
    d.ellipse([W / 2 - 190, HORIZON + 6, W / 2 + 190, HORIZON + 116], fill=(238, 168, 88))   # 大圆饼
    for a in range(8):                                                          # 切 8 块的缝
        ang = TAU * a / 8
        x2, y2 = W / 2 + 185 * math.cos(ang), HORIZON + 61 + 55 * math.sin(ang)
        d.line([(W / 2, HORIZON + 61), (x2, y2)], fill=(206, 132, 62), width=5)
    for k in range(4):                                                          # 盘子
        px = W / 2 - 660 + k * 440
        d.ellipse([px - 70, HORIZON + 44, px + 70, HORIZON + 84], fill=(250, 250, 246))
    save(img, os.path.join("fraction_castle", "assets", "share_workshop.jpg"))


def fraction_house():
    """分数小屋：魔法图书馆 + 桌上数字方块"""
    img = room((222, 214, 244), (206, 196, 236), (150, 132, 190), (120, 104, 160))
    d = ImageDraw.Draw(img)
    for k in range(4):                                                          # 书架
        sx = 120 + k * 500
        d.rectangle([sx, HORIZON - 320, sx + 380, HORIZON - 20], fill=(120, 96, 150))
        for r in range(4):
            d.rectangle([sx + 14, HORIZON - 300 + r * 70, sx + 366, HORIZON - 250 + r * 70], fill=(236, 230, 246))
            for b in range(6):
                d.rectangle([sx + 26 + b * 56, HORIZON - 292 + r * 70, sx + 70 + b * 56, HORIZON - 258 + r * 70],
                            fill=[(240, 148, 120), (120, 180, 220), (150, 200, 130), (240, 200, 110)][(b + r) % 4])
    table(img, W / 2, HORIZON + 70, 860, 66, wood=(196, 172, 216))
    for k, c in enumerate([(240, 148, 120), (120, 180, 220), (240, 200, 110), (150, 200, 130)]):
        d.rounded_rectangle([W / 2 - 300 + k * 190, HORIZON + 14, W / 2 - 210 + k * 190, HORIZON + 104],
                            radius=14, fill=c, outline=(255, 255, 255), width=5)  # 数字方块
    save(img, os.path.join("fraction_castle", "assets", "fraction_house.jpg"))


def color_garden():
    """涂色花园：明亮画室 + 黑板图形 + 颜料"""
    img = room((248, 244, 236), (240, 234, 222), (198, 188, 172), (168, 156, 140))
    d = ImageDraw.Draw(img)
    d.rectangle([160, HORIZON - 340, W - 160, HORIZON - 40], fill=(58, 92, 74))  # 黑板墙
    d.rectangle([160, HORIZON - 340, W - 160, HORIZON - 332], fill=(150, 108, 72))
    d.ellipse([300, HORIZON - 260, 480, HORIZON - 80], outline=(250, 250, 244), width=10)   # 圆
    d.rectangle([640, HORIZON - 250, 860, HORIZON - 90], outline=(250, 250, 244), width=10) # 方
    d.polygon([(1080, HORIZON - 90), (1190, HORIZON - 250), (1300, HORIZON - 90)], outline=(250, 250, 244), width=8)
    d.polygon([(1500, HORIZON - 90), (1610, HORIZON - 250), (1720, HORIZON - 90), (1610, HORIZON - 170)],
              fill=(250, 250, 244))
    table(img, W / 2, HORIZON + 80, 900, 64)
    for k, c in enumerate([(238, 106, 90), (246, 196, 84), (110, 182, 118), (98, 156, 224), (156, 120, 204)]):
        px = W / 2 - 420 + k * 210
        d.ellipse([px - 44, HORIZON + 30, px + 44, HORIZON + 86], fill=c)        # 颜料碟
    save(img, os.path.join("fraction_castle", "assets", "color_garden.jpg"))


def origami_room():
    """折纸工坊：彩纸 + 纸飞机 + 纸鹤架"""
    img = room((250, 236, 226), (242, 222, 206), (206, 178, 148), (176, 146, 116))
    d = ImageDraw.Draw(img)
    for k in range(7):                                                          # 墙上彩纸串
        d.polygon([(120 + k * 280, HORIZON - 300), (200 + k * 280, HORIZON - 300),
                   (160 + k * 280, HORIZON - 220)],
                  fill=[(240, 148, 120), (120, 180, 220), (150, 200, 130), (240, 200, 110),
                        (156, 120, 204), (240, 148, 120), (120, 180, 220)][k])
    for k in range(3):                                                          # 飞着的纸飞机
        px, py = W * (0.25 + 0.25 * k), HORIZON - 150 + (k % 2) * 40
        d.polygon([(px, py), (px + 90, py + 26), (px + 30, py + 40)], fill=(250, 250, 246))
    table(img, W / 2, HORIZON + 70, 880, 66)
    for k, c in enumerate([(240, 148, 120), (120, 180, 220), (150, 200, 130), (240, 200, 110)]):
        d.polygon([(W / 2 - 320 + k * 200, HORIZON + 66), (W / 2 - 240 + k * 200, HORIZON + 6),
                   (W / 2 - 160 + k * 200, HORIZON + 66)], fill=c)               # 桌上折纸
    save(img, os.path.join("fraction_castle", "assets", "origami_room.jpg"))


def final_castle():
    """终极城堡：大厅 + 吊灯 + 宝座 + 蛋糕"""
    img = room((236, 224, 208), (216, 198, 178), (140, 110, 92), (108, 84, 70))
    d = ImageDraw.Draw(img)
    for k in range(5):                                                          # 石柱
        d.rectangle([140 + k * 460, HORIZON - 420, 220 + k * 460, HORIZON], fill=(196, 172, 142))
    d.ellipse([W / 2 - 130, HORIZON - 460, W / 2 + 130, HORIZON - 200], outline=(240, 200, 110), width=12)  # 吊灯
    d.polygon([(W / 2 - 240, HORIZON - 420), (W / 2 + 40, HORIZON - 420), (W / 2 - 100, HORIZON - 240)],
              fill=(206, 84, 74))                                               # 旗帜
    d.rectangle([W / 2 - 130, HORIZON - 260, W / 2 + 90, HORIZON - 40], fill=(150, 96, 66))  # 宝座背
    d.rectangle([W / 2 - 150, HORIZON - 120, W / 2 + 110, HORIZON - 40], fill=(172, 116, 80))
    table(img, W / 2 - 520, HORIZON + 80, 480, 56)
    d.ellipse([W / 2 - 620, HORIZON + 30, W / 2 - 420, HORIZON + 82], fill=(246, 222, 200))  # 蛋糕
    d.rectangle([W / 2 - 620, HORIZON + 44, W / 2 - 420, HORIZON + 62], fill=(238, 168, 180))
    table(img, W / 2 + 540, HORIZON + 90, 480, 56)
    d.ellipse([W / 2 + 440, HORIZON + 36, W / 2 + 640, HORIZON + 90], fill=(238, 190, 120))  # 披萨
    save(img, os.path.join("fraction_castle", "assets", "final_castle.jpg"))


def main():
    for sub in (os.path.join("lushan", "assets"), os.path.join("fraction_castle", "assets")):
        os.makedirs(os.path.join(BASE, sub), exist_ok=True)
    print("案例一 庐山四视角：")
    lushan_front(); lushan_side(); lushan_inside(); lushan_top()
    print("案例二 分数城堡六场景：")
    forest_entrance(); share_workshop(); fraction_house(); color_garden(); origami_room(); final_castle()
    print("热点图标：")
    hotspot_icon()
    print("完成。正式素材请按教程提示词用 AI 生成后同名覆盖。")


if __name__ == "__main__":
    main()
