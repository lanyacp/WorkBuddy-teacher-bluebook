import fitz, re

base = "D:/projects/WorkBuddy/2026-06-17-11-18-20/英语课程资料/"

books = {
    "七上(2024秋)": "英语七上 译林版（2024秋）.pdf",
    "七下(2025春)": "英语七下 译林版（2025春）.pdf",
    "八上(2025秋)": "【译林版】八年级上册(2025秋版)英语电子课本.pdf",
    "八下(2026春)": "【译林版】八年级下册(2026春版)英语电子课本.pdf",
    "九上(2026秋)": "2026秋译林版九年级上册英语彩色高清版.pdf",
}

unit_re = re.compile(r'^Unit\s+(\d+)\b', re.I)

for label, fn in books.items():
    print("="*70)
    print("课本:", label)
    print("="*70)
    doc = fitz.open(base + fn)
    found = {}
    for pi in range(doc.page_count):
        txt = doc[pi].get_text()
        for line in txt.splitlines():
            m = unit_re.match(line.strip())
            if m:
                u = int(m.group(1))
                # capture this line + next 2 non-empty lines as candidate title
                nxt = []
                lines = [l.strip() for l in txt.splitlines()]
                idx = lines.index(line.strip()) if line.strip() in lines else -1
                for j in range(idx+1, min(idx+4, len(lines))):
                    if lines[j]:
                        nxt.append(lines[j])
                found.setdefault(u, " / ".join(nxt[:2]))
    doc.close()
    for u in sorted(found):
        print(f"  Unit {u}: {found[u]}")
    print()
