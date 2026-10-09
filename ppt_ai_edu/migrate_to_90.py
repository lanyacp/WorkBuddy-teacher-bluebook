# -*- coding: utf-8 -*-
"""把现有32页迁移到 pages90 目录，并按 P01-P90 重命名 + 修正页脚页码。"""
import os, re, shutil

SRC = r"D:\projects\WorkBuddy\2026-06-17-11-18-20\ppt_ai_edu\pages"
DST = r"D:\projects\WorkBuddy\2026-06-17-11-18-20\ppt_ai_edu\pages90"
os.makedirs(DST, exist_ok=True)

# 源文件 -> (目标页码, 新slug)
MAP = {
    "slide_01_cover.jsx":     (1,  "cover"),
    "slide_02_position.jsx":  (2,  "position"),
    "slide_03_map.jsx":       (3,  "map"),
    "slide_04_objectives.jsx":(4,  "objectives"),
    "slide_06_core.jsx":      (7,  "core_view"),
    "slide_07_boundary.jsx":  (8,  "ability_boundary"),
    "slide_08_tools.jsx":     (10, "tool_map"),
    "slide_09_prompt.jsx":    (11, "prompt_formula"),
    "slide_10_safety.jsx":    (14, "safety_3rules"),
    "slide_11_sec1.jsx":      (15, "sec1_cover"),
    "slide_13_path.jsx":      (19, "learning_path"),
    "slide_16_sec2.jsx":      (31, "sec2_cover"),
    "slide_17_loop.jsx":      (32, "loop_overview"),
    "slide_20_sec3.jsx":      (47, "sec3_cover"),
    "slide_22_sec4.jsx":      (59, "sec4_cover"),
    "slide_24_sec5.jsx":      (70, "sec5_cover"),
    "slide_26_compare.jsx":   (72, "skill_vs_prompt"),
    "slide_27_threestep.jsx": (74, "skill_three_steps"),
}

for src_name, (page, slug) in sorted(MAP.items(), key=lambda x: x[1][0]):
    src = os.path.join(SRC, src_name)
    txt = open(src, encoding="utf-8").read()
    # 修正页脚页码 NN / 32 -> NN / 90
    txt = re.sub(r"(\d{2}) / 32", r"\1 / 90", txt)
    dst = os.path.join(DST, "p%02d_%s.jsx" % (page, slug))
    with open(dst, "w", encoding="utf-8") as f:
        f.write(txt)
    print("migrated -> p%02d_%s.jsx" % (page, slug))

print("\n已迁移 %d 页，其余 %d 页待新建" % (len(MAP), 90 - len(MAP)))
