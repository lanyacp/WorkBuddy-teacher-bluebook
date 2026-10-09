"""把原书截图按章归档到教师版蓝皮书的 assets 目录。

从每章 index.md 的 `![](assets/xxx.png)` 引用出发精确取图，
按 chNN 前缀命名，便于在正文里按章引用。
"""
import os
import re
import shutil

SRC = "_ref_raw"
DST = "教师版蓝皮书/assets"


def chapter_tag(entry):
    m = re.match(r"第\s*(\d+)\s*章", entry)
    if m:
        return "ch" + m.group(1).zfill(2)
    m2 = re.match(r"附录\s*([AB])", entry)
    if m2:
        return "app" + m2.group(1)
    return "x" + re.sub(r"[^\w\u4e00-\u9fff]", "", entry)[:12]


def main():
    if os.path.isdir(DST):
        shutil.rmtree(DST)
    os.makedirs(DST)

    total_n = 0
    total_bytes = 0
    index = {}

    for entry in sorted(os.listdir(SRC)):
        md_path = os.path.join(SRC, entry, "index.md")
        asset_dir = os.path.join(SRC, entry, "assets")
        if not os.path.isfile(md_path):
            continue
        if not os.path.isdir(asset_dir):
            continue

        tag = chapter_tag(entry)
        with open(md_path, encoding="utf-8") as f:
            body = f.read()
        refs = re.findall(r"!\[[^\]]*\]\(assets/([^)]+)\)", body)

        cnt = 0
        for ref in refs:
            src_img = os.path.join(asset_dir, ref)
            if not os.path.isfile(src_img):
                continue
            dst_img = os.path.join(DST, f"{tag}__{ref}")
            shutil.copy2(src_img, dst_img)
            total_n += 1
            total_bytes += os.path.getsize(dst_img)
            cnt += 1

        if cnt:
            index[tag] = (entry, cnt)

    print(f"归档 {total_n} 张，共 {total_bytes / 1024 / 1024:.1f} MB -> {DST}")
    for tag, (name, cnt) in sorted(index.items()):
        print(f"  {tag}  {cnt:>2} 张   {name}")


if __name__ == "__main__":
    main()