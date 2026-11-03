#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
素材整理：
  1) 抹掉 AI 生成图的右下角水印（用左侧相邻内容镜像覆盖 + 左缘羽化）
  2) 转 JPEG 质量 88（PNG 单张 3.5MB，网页加载太慢）

用法：python fix_assets.py
"""
import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, 'assets')

# 水印区域（2048x1024 图的右下角）
BOX = (1908, 944, 2048, 1024)

FILES = ['pano_1_wanchun.png', 'pano_2_dashuifa.png', 'pano_3_shanshui.png']


def remove_watermark(im):
    x0, y0, x1, y1 = BOX
    w, h = x1 - x0, y1 - y0
    # 从紧邻的左侧取同样大小的一块，水平翻转后覆盖
    src = im.crop((x0 - w, y0, x0, y1)).transpose(Image.FLIP_LEFT_RIGHT)
    mask = Image.new('L', (w, h), 255)
    d = ImageDraw.Draw(mask)
    fade = 16
    for i in range(fade):          # 左缘渐隐，避免出现硬接缝
        d.rectangle([i, 0, i, h], fill=int(255 * (1 - i / fade)))
    im.paste(src, BOX, mask)
    return im


def main():
    for f in FILES:
        p = os.path.join(ASSETS, f)
        if not os.path.exists(p):
            print('跳过（不存在）', f)
            continue
        im = Image.open(p).convert('RGB')
        im = remove_watermark(im)
        out = os.path.join(ASSETS, f.replace('.png', '.jpg'))
        im.save(out, 'JPEG', quality=88, optimize=True, progressive=True)
        old = os.path.getsize(p)
        new = os.path.getsize(out)
        print(f'{f}  {old/1024:.0f}KB  →  {os.path.basename(out)}  {new/1024:.0f}KB')
        os.remove(p)


if __name__ == '__main__':
    main()
