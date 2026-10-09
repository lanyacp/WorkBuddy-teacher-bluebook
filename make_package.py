# -*- coding: utf-8 -*-
"""按《交付总清单》打包培训资料包。"""
import os, zipfile, datetime

PROJ = r"D:\projects\WorkBuddy\2026-06-17-11-18-20"
SRC = os.path.join(PROJ, "交付包")
PKG_NAME = "AI赋能中小学教育教学_培训资料包"
ZIP_PATH = os.path.join(PROJ, PKG_NAME + ".zip")

# 交付清单里的 7 件正式交付物（顺序即清单编号）
DOCS = [
    "00_交付总清单.docx",
    "01_前期准备清单.docx",
    "02_讲师手册.docx",
    "03_学员手册.docx",
    "04_AI赋能中小学教育教学_90页备料库.pptx",
    "05_90页PPT索引与裁剪指南.docx",
    "06_上课随身手册.docx",
]
# 可复跑脚本，放子目录
SCRIPTS = ["docx_kit.py", "gen_00_index.py", "gen_01_prep.py", "gen_02_teacher.py",
           "gen_03_student.py", "gen_05_index90.py", "gen_06_handbook.py"]

# 1) 清理临时文件
for fn in os.listdir(SRC):
    if fn.startswith("_") and fn.endswith(".txt"):
        os.remove(os.path.join(SRC, fn))
        print("清理临时文件:", fn)

# 2) 打包
if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)

with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for fn in DOCS:
        p = os.path.join(SRC, fn)
        if not os.path.exists(p):
            print("!! 缺失:", fn)
            continue
        z.write(p, arcname=os.path.join(PKG_NAME, fn))
        print("+ ", fn)
    have = [s for s in SCRIPTS if os.path.exists(os.path.join(SRC, s))]
    if have:
        sub = os.path.join(PKG_NAME, "附_生成脚本_可改版重跑")
        for s in have:
            z.write(os.path.join(SRC, s), arcname=os.path.join(sub, s))
        print("+ 附_生成脚本/", len(have), "个")

# 3) 校验
print("\n" + "=" * 60)
with zipfile.ZipFile(ZIP_PATH) as z:
    names = z.namelist()
    print("包内条目 %d 个，总大小 %.1f KB" % (
        len(names), os.path.getsize(ZIP_PATH) / 1024.0))
    for n in names:
        info = z.getinfo(n)
        print("   %8.1f KB   %s" % (info.file_size / 1024.0, n))
    bad = z.testzip()
    print("\n完整性:", "正常" if bad is None else "损坏 -> " + str(bad))
print("\n生成时间:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
print("ZIP 路径:", ZIP_PATH)
