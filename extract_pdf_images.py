"""从官方蓝皮书 PDF 中提取全部内嵌图片。

PDF 由 VitePress 官网离线生成，图片是网页原图直接嵌入，
分辨率与原书一致，可直接用于教师版蓝皮书。
"""
import os

from pypdf import PdfReader

BLUE = "C:/Users/Administrator/Desktop/WorkBuddy蓝皮书-.pdf"
OUT = "教师版蓝皮书/assets_from_pdf"


def main():
    os.makedirs(OUT, exist_ok=True)
    reader = PdfReader(BLUE)

    total = 0
    seen = {}
    for pno, page in enumerate(reader.pages, start=1):
        for k, img in enumerate(page.images):
            data = img.data
            # 用内容哈希去重（同一张图在多页复用）
            import hashlib

            h = hashlib.md5(data).hexdigest()[:10]
            if h in seen:
                seen[h].append(pno)
                continue
            ext = os.path.splitext(img.name)[1] or ".png"
            if ext.lower() not in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
                ext = ".png"
            fn = f"pdf_p{pno:03d}_{k:02d}_{h}{ext}"
            with open(os.path.join(OUT, fn), "wb") as f:
                f.write(data)
            seen[h] = [pno]
            total += 1

    print(f"提取完成：{total} 张唯一图片 -> {OUT}")
    print(f"总大小：{sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) / 1024 / 1024:.1f} MB")
    print(f"页数：{len(reader.pages)}")


if __name__ == "__main__":
    main()