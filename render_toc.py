import fitz

base = "D:/projects/WorkBuddy/2026-06-17-11-18-20/英语课程资料/"
out = "D:/projects/WorkBuddy/2026-06-17-11-18-20/英语课程资料/_toc_imgs/"

import os
os.makedirs(out, exist_ok=True)

# image PDFs -> render candidate TOC pages
image_books = {
    "七下": "英语七下 译林版（2025春）.pdf",
    "八上": "【译林版】八年级上册(2025秋版)英语电子课本.pdf",
    "八下": "【译林版】八年级下册(2026春版)英语电子课本.pdf",
}

for label, fn in image_books.items():
    d = fitz.open(base + fn)
    for p in [4, 5, 6]:
        if p < d.page_count:
            pix = d[p].get_pixmap(dpi=95)
            path = f"{out}{label}_p{p+1}.png"
            pix.save(path)
            print("saved", path)
    d.close()

# 九上 TOC (has text) -> dump page 1-2
d = fitz.open(base + "2026秋译林版九年级上册英语彩色高清版.pdf")
for p in [0,1]:
    t = d[p].get_text()
    if t.strip():
        print(f"=== 九上 页{p+1} ===")
        print(t[:1500])
d.close()
