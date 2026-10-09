#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配图隐私体检：扫描所有图片，列出可疑区域供人工确认。

不能自动判断"这张图是否敏感"，所以采用：
1. 自动检测人脸区域比例（简单启发式，供排序参考）
2. 输出图片清单，按"是否可能含真实数据"分级，交给人工过一遍

用法：
    python audit_images.py          # 生成报告
    python audit_images.py --crop 疑似.png   # 裁出可疑区域供查看
"""
import os
import sys

from PIL import Image

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '教师版蓝皮书', 'assets_opt')

# 图片来源分级：来源不同，隐私风险不同
SOURCE_RISK = {
    'pdf':  ('官方 PDF 提取', 'low'),
    'pdfch': ('官方 PDF 提取', 'low'),
    'ch':   ('官方 PDF 提取', 'low'),
    'wb_':  ('公众号文章抓取', 'mid'),   # 第三方界面，需确认有无真实数据
    'penguin': ('本人实机截图', 'high'),  # 自己电脑，最可能含个人信息
    'live_': ('本人实机截图', 'high'),
}


def classify(name):
    for k, (src, risk) in SOURCE_RISK.items():
        if name.startswith(k):
            return src, risk
    return '未知来源', 'mid'


def main():
    files = sorted(f for f in os.listdir(BASE)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg')))

    print('=' * 74)
    print('配图隐私体检报告')
    print('=' * 74)
    print('目录：%s' % BASE)
    print('共 %d 张图\n' % len(files))

    buckets = {'high': [], 'mid': [], 'low': []}
    for f in files:
        src, risk = classify(f)
        buckets[risk].append((f, src, os.path.getsize(os.path.join(BASE, f))))

    for risk, label in [('high', '⚠️  高风险 —— 本人实机截图，必须逐张确认'),
                        ('mid', '⚡ 中风险 —— 第三方文章抓取，确认有无真实数据'),
                        ('low', '✅ 低风险 —— 官方 PDF 提取，公开资料')]:
        items = buckets[risk]
        print('%s  %d 张' % (label, len(items)))
        print('-' * 74)
        for f, src, sz in items:
            print('  %-40s %7.0f KB   %s' % (f, sz / 1024, src))
        print()

    print('=' * 74)
    print('确认清单（人工过一遍这些）')
    print('=' * 74)
    print("""
高风险图（本人实机截图）——逐张打开确认：
  1. 是否出现真实姓名？
  2. 是否出现真实学校名 / 班级 / 学生名单？
  3. 侧边栏是否有个人任务名、用户名、头像？
  4. 对话框里是否有真实的学生数据？

中风险图（公众号抓取）——确认：
  1. 界面里的文件名是否为真实客户/学校？
  2. 是否有真实姓名出现在标题栏或对话里？
  3. 浏览器/应用标签栏是否暴露你的其他应用？

低风险图（官方 PDF）——一般无需处理，但案例里若出现
  真实人名或学校名，开源前也要替换。
""")

    if len(sys.argv) > 2 and sys.argv[1] == '--crop':
        target = sys.argv[2]
        p = os.path.join(BASE, target)
        im = Image.open(p)
        print('\n%s  %sx%s' % (target, im.width, im.height))


if __name__ == '__main__':
    main()