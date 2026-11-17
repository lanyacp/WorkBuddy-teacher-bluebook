# -*- coding: utf-8 -*-
"""把「视频素材下载」专题 Markdown 转成单文件 HTML（图片内嵌）。"""
import importlib.util, os

BASE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bh", os.path.join(BASE, "build_html.py"))
bh = importlib.util.module_from_spec(spec); spec.loader.exec_module(bh)

bh.SRC = os.path.join(BASE, "专题_视频素材下载.md")
bh.OUT = os.path.join(BASE, "专题_视频素材下载.html")
bh.MAX_W = 1200
bh.QUALITY = 86
bh.TEMPLATE = bh.TEMPLATE.replace(
    "WorkBuddy 教师实战蓝皮书 · 正式版（2026 年 10 月）",
    "视频素材下载 · 把「看得见、下不来」变成三步").replace(
    '📘 WorkBuddy 教师实战蓝皮书<br><small style="font-weight:400">正式版 · 2026 年 10 月</small>',
    '📘 WorkBuddy 教师实战蓝皮书<br><small style="font-weight:400">专题 · 视频素材下载</small>')
bh.main()
