import fitz, re

base = "D:/projects/WorkBuddy/2026-06-17-11-18-20/英语课程资料/"

books = {
    "七下(2025春)": "英语七下 译林版（2025春）.pdf",
    "八上(2025秋)": "【译林版】八年级上册(2025秋版)英语电子课本.pdf",
    "八下(2026春)": "【译林版】八年级下册(2026春版)英语电子课本.pdf",
    "九上(2026秋)": "2026秋译林版九年级上册英语彩色高清版.pdf",
}

unit_line = re.compile(r'^\s*(\d+)\s*$')  # page number column sometimes
module_re = re.compile(r'Module\s*\d', re.I)
unit_re = re.compile(r'Unit\s*\d', re.I)

for label, fn in books.items():
    print("="*70); print(label); print("="*70)
    doc = fitz.open(base+fn)
    best = -1; bestcount = 0
    for pi in range(doc.page_count):
        t = doc[pi].get_text()
        # count 'Unit N' standalone-ish occurrences
        cnt = len(unit_re.findall(t))
        if cnt > bestcount:
            bestcount = cnt; best = pi
    print(f"最佳目录候选页: 第{best+1}页 (Unit出现{bestcount}次)")
    if best>=0:
        print(doc[best].get_text()[:3000])
    doc.close()
    print()
