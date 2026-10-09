#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
企鹅教师助手截图 · 个人信息清理（坐标已精确定位）
清理项：
  1. 右上角「你在 WorkBuddy 里共度过 N 小时」白底条：y=10..46, x=615..1140
  2. 模型名「Space-Bunny」：输入框内右下区域
  3. 活动弹窗（部分图有）
坐标基于实测扫描结果，非估算。
"""
import os

from PIL import Image

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '教师版蓝皮书', 'assets_opt')
WHITE = (255, 255, 255)


def fill(im, box, color=WHITE):
    px = im.load()
    w, h = im.size
    x0, y0, x1, y1 = box
    for y in range(max(0, y0), min(h, y1)):
        for x in range(max(0, x0), min(w, x1)):
            px[x, y] = color


for fname in ['penguin_teaching_design.png', 'penguin_discover_apps.png',
              'penguin_home_school.png', 'penguin_growth.png']:
    p = os.path.join(BASE, fname)
    if not os.path.exists(p):
        print('SKIP %s' % fname)
        continue
    im = Image.open(p).convert('RGB')
    w, h = im.size

    # 1. 右上角使用时长白条（实测 y=10..46）
    fill(im, (612, 8, w, 48), WHITE)

    # 2. 模型名：找输入框右下角。用相对比例定位
    #    实测 teaching_design 中模型名在 y=365..395、x=700..830
    sy = h / 612.0
    my0, my1 = int(358 * sy), int(400 * sy)
    fill(im, (int(690 * w / 1200), my0, int(838 * w / 1200), my1), WHITE)

    # 3. 活动弹窗（discover_apps 特有，在右上偏下）
    if 'discover' in fname:
        fill(im, (int(690 * w / 1200), int(58 * sy), w - 20, int(168 * sy)), WHITE)

    im.save(p)
    print('%s  %dx%d  已清理右上角使用时长 + 模型名%s'
          % (fname, w, h, ' + 活动弹窗' if 'discover' in fname else ''))