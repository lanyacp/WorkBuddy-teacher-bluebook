# -*- coding: utf-8 -*-
"""把单篇专题 Markdown 转成单文件 HTML（图片内嵌），复用 build_html.py 的模板与逻辑。"""
import importlib.util, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bh", os.path.join(BASE, "build_html.py"))
bh = importlib.util.module_from_spec(spec); spec.loader.exec_module(bh)

bh.SRC = os.path.join(BASE, "专题_360VR互动网页_零依赖手工作坊.md")
bh.OUT = os.path.join(BASE, "专题_360VR互动网页_零依赖手工作坊.html")
bh.MAX_W = 1400          # 界面截图文字较小，保留更高分辨率
bh.TEMPLATE = bh.TEMPLATE.replace(
    "WorkBuddy 教师实战蓝皮书 · 正式版（2026 年 10 月）",
    "360° 全景互动网页 · 零依赖手工作坊")
bh.main()
