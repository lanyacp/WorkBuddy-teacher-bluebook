import fitz, re, sys

base = "D:/projects/WorkBuddy/2026-06-17-11-18-20/英语课程资料/"

books = {
    "七上(2024秋)": "英语七上 译林版（2024秋）.pdf",
    "七下(2025春)": "英语七下 译林版（2025春）.pdf",
    "八上(2025秋)": "【译林版】八年级上册(2025秋版)英语电子课本.pdf",
    "八下(2026春)": "【译林版】八年级下册(2026春版)英语电子课本.pdf",
    "九上(2026秋)": "2026秋译林版九年级上册英语彩色高清版.pdf",
}

def first_pages_text(path, n=12):
    doc = fitz.open(path)
    pages = []
    for i in range(min(n, doc.page_count)):
        pages.append(doc[i].get_text())
    doc.close()
    return "\n".join(pages)

for label, fn in books.items():
    print("="*70)
    print("课本:", label, "| 文件:", fn)
    print("="*70)
    txt = first_pages_text(base + fn)
    # find lines containing Unit / Welcome / 单元
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    # Print lines that look like unit headers: contain 'Unit' or 'Welcome' or 'Comic'
    pat = re.compile(r'(Unit\s*\d+|Welcome|Comic|Integrated|Task|Study skills|Revision|Project|Assessment|Self[- ]?assessment)', re.I)
    seen = []
    for l in lines:
        if pat.search(l) and len(l) < 80:
            seen.append(l)
    # dedupe keep order
    out = []
    for s in seen:
        if s not in out:
            out.append(s)
    print("前12页含单元结构的行:")
    for s in out[:60]:
        print("  ", s)
    print()
