import fitz, re

base = "D:/projects/WorkBuddy/2026-06-17-11-18-20/英语课程资料/"

books = {
    "七上(2024秋)": "英语七上 译林版（2024秋）.pdf",
    "七下(2025春)": "英语七下 译林版（2025春）.pdf",
    "八上(2025秋)": "【译林版】八年级上册(2025秋版)英语电子课本.pdf",
    "八下(2026春)": "【译林版】八年级下册(2026春版)英语电子课本.pdf",
    "九上(2026秋)": "2026秋译林版九年级上册英语彩色高清版.pdf",
}

for label, fn in books.items():
    print("="*70)
    print("课本:", label)
    print("="*70)
    doc = fitz.open(base + fn)
    toc = doc.get_toc()
    print("PDF内置书签(目录)条数:", len(toc))
    for lvl, title, page in toc[:40]:
        print(f"  {'  '*(lvl-1)}{title}  -> 页{page}")
    doc.close()
    print()
