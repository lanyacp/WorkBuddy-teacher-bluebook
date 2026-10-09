#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把教师版蓝皮书的 8 个 Markdown 文件合并成一份完整文档，并打包 ZIP。

用法：
    python build_bluebook.py
"""
import os
import re
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))

# 合并顺序：骨架与案例库 -> 四篇正文 -> 三个附录
FILES = [
    ("00_骨架与案例库/骨架设计.md", "第一部分 · 蓝皮书设计说明（骨架与案例库）"),
    ("00_骨架与案例库/案例库.md",   "第二部分 · 真实案例库（讲课可直接引用）"),
    ("第一篇_先把工具用起来.md",      "第三部分 · 第一篇　先把工具用起来"),
    ("第二篇_教学全流程工作流_上.md", "第四部分 · 第二篇　教学全流程工作流（7-11 章）"),
    ("第二篇_教学全流程工作流_下.md", "第五部分 · 第二篇　教学全流程工作流（12-16 章）"),
    ("第三篇_教研行政与成长.md",      "第六部分 · 第三篇　教研、行政与成长"),
    ("第四篇_进阶_从个人到区域.md",    "第七部分 · 第四篇　进阶：把工具变成你的系统"),
    ("附录A_常用指令模板.md",         "第八部分 · 附录 A　常用指令模板"),
    ("附录B_场景速查表.md",           "第九部分 · 附录 B　场景速查表"),
    ("附录C_红线清单.md",             "第十部分 · 附录 C　红线清单"),
]

OUT_MD = os.path.join(BASE, "WorkBuddy教师实战蓝皮书_完整版.md")
OUT_ZIP = os.path.join(BASE, "WorkBuddy教师实战蓝皮书_完整版.zip")


def build():
    parts = []
    total = 0
    for rel, title in FILES:
        path = os.path.join(BASE, rel)
        if not os.path.exists(path):
            print("  [跳过] 找不到文件：%s" % rel)
            continue
        text = open(path, encoding="utf-8").read()
        total += len(text)
        parts.append("\n\n---\n\n# %s\n\n> 来源文件：`%s`\n\n%s"
                     % (title, rel, text))
        print("  [合并] %-42s %6.1f KB" % (rel, len(text) / 1024))

    header = (
        "# WorkBuddy 教师实战蓝皮书\n\n"
        "> 面向县域中小学教师、教研员、校长的实战读本\n"
        ">\n"
        "> **26 章 · 四篇正文 · 三个附录 · 36 个可直接使用的指令模板 · 52 张实操截图**\n"
        ">\n"
        "> 改编自开源项目 AlephAITech/WorkBuddyGuide 的蓝皮书体例，\n"
        "> 内容全部替换为教师场景，并融合 10 个可溯源的真实区域实践案例。\n"
        ">\n"
        "> 第一篇与第四篇的界面截图直接复用官方原版，已按教师场景重新编排。\n"
        ">\n"
        "> 配套文件：\n"
        "> - 案例来源与政策依据见「第二部分 · 真实案例库」\n"
        "> - 红线部分见「附录 C」，**使用前请先读完**\n"
    )

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(header + "".join(parts))

    print("\n  合并完成：%s（%.1f KB）" % (os.path.basename(OUT_MD), total / 1024))

    img_dir = os.path.join(BASE, "assets_opt")
    img_list = []
    if os.path.isdir(img_dir):
        img_list = [f for f in sorted(os.listdir(img_dir))
                    if f.lower().endswith((".png", ".gif", ".jpg", ".jpeg"))]

    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(OUT_MD, "WorkBuddy教师实战蓝皮书_完整版.md")
        for rel, _ in FILES:
            p = os.path.join(BASE, rel)
            if os.path.exists(p):
                z.write(p, rel.replace("/", "/"))
        for name in img_list:
            z.write(os.path.join(img_dir, name), "assets/" + name)
        for extra in ("build_bluebook.py",):
            p = os.path.join(BASE, extra)
            if os.path.exists(p):
                z.write(p, extra)

    with zipfile.ZipFile(OUT_ZIP) as z:
        bad = z.testzip()
        print("  打包完成：%s（%.1f MB，%d 个条目，截图 %d 张，校验%s）"
              % (os.path.basename(OUT_ZIP),
                 os.path.getsize(OUT_ZIP) / 1024 / 1024,
                 len(z.namelist()),
                 len(img_list),
                 "正常" if bad is None else "异常：%s" % bad))


if __name__ == "__main__":
    print("=" * 60)
    print("WorkBuddy 教师实战蓝皮书 · 合并打包")
    print("=" * 60)
    build()
    print("\n提示：导入飞书时，直接上传 WorkBuddy教师实战蓝皮书_完整版.md，")
    print("      飞书会自动转换为在线文档，并自动内嵌 assets 下的所有截图。")
