# -*- coding: utf-8 -*-
"""把单篇专题 Markdown 转成单文件 HTML（图片内嵌），复用 build_html.py 的模板与逻辑。"""
import importlib.util, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bh", os.path.join(BASE, "build_html.py"))
bh = importlib.util.module_from_spec(spec); spec.loader.exec_module(bh)

bh.SRC = os.path.join(BASE, "专题_3D教学模型.md")
bh.OUT = os.path.join(BASE, "专题_3D教学模型.html")
bh.MAX_W = 1200
bh.QUALITY = 82
bh.TEMPLATE = bh.TEMPLATE.replace(
    "WorkBuddy 教师实战蓝皮书 · 正式版（2026 年 10 月）",
    "3D 教学模型 · 让看不见的结构，转起来").replace(
    '📘 WorkBuddy 教师实战蓝皮书<br><small style="font-weight:400">正式版 · 2026 年 10 月</small>',
    '📘 WorkBuddy 教师实战蓝皮书<br><small style="font-weight:400">专题 · 3D 教学模型</small>')
bh.main()
