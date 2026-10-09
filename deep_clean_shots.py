#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
企鹅教师助手截图深度脱敏（第二轮）
问题：之前只填了侧边栏的一部分区域，底部仍残留个人信息（如"实习"标签）
方案：整条侧边栏（x < PANEL_LEFT）全部填成背景色，再把菜单面板挖回来
"""
import os

from PIL import Image

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '教师版蓝皮书', 'assets_opt')
SIDEBAR_BG = (236, 242, 254)


def is_bg(p, tol=18):
    return abs(p[0] - 236) + abs(p[1] - 242) + abs(p[2] - 254) <= tol


def deep_clean(fname):
    p = os.path.join(BASE, fname)
    im = Image.open(p).convert('RGB')
    w, h = im.size

    # 1. 先探测菜单面板的左边界（面板是纯白 255,255,255）
    panel_left = None
    for x in range(80, 400):
        # 统计该列的白色像素占比
        white = sum(1 for y in range(60, h - 40, 8) if im.getpixel((x, y)) == (255, 255, 255))
        if white > 30:
            panel_left = x
            break

    if panel_left is None:
        # 没有面板，整条侧边栏填平
        px = im.load()
        for y in range(28, h):
            for x in range(0, 200):
                px[x, y] = SIDEBAR_BG
        print('%s  无面板，整条侧边栏已填平' % fname)
        im.save(p)
        return

    # 2. 记录面板区域像素（挖回来用）
    panel_right = min(panel_left + 330, w)
    panel_top, panel_bottom = 50, h - 40
    panel = im.crop((panel_left, panel_top, panel_right, panel_bottom))

    # 3. 整条侧边栏填平（0 到 panel_left 全宽，含底部图标区）
    px = im.load()
    for y in range(28, h):
        for x in range(0, panel_left):
            px[x, y] = SIDEBAR_BG

    # 4. 把面板贴回
    im.paste(panel, (panel_left, panel_top))

    # 5. 校验：侧边栏区域现在是否全是纯背景色
    impure = sum(1 for y in range(28, h, 4) for x in range(0, panel_left, 4)
                 if not is_bg(im.getpixel((x, y))))
    total = len(range(28, h, 4)) * len(range(0, panel_left, 4))
    purity = (total - impure) / total * 100

    im.save(p)
    print('%s  面板左边界 x=%d  侧边栏纯度 %.1f%%  %s'
          % (fname, panel_left, purity, '✓ 干净' if purity > 98 else '⚠️ 仍有残留'))


for f in ['penguin_discover_apps.png']:
    deep_clean(f)