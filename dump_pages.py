import fitz

base = "D:/projects/WorkBuddy/2026-06-17-11-18-20/英语课程资料/"

targets = {
    "七上(2024秋)": ("英语七上 译林版（2024秋）.pdf", [3,4,5]),
    "九上(2026秋)": ("2026秋译林版九年级上册英语彩色高清版.pdf", [0,1,2,3]),
}

for label,(fn,pages) in targets.items():
    print("="*70); print(label); print("="*70)
    doc = fitz.open(base+fn)
    for p in pages:
        if p < doc.page_count:
            t = doc[p].get_text()
            print(f"--- 页{p+1} ---")
            print(t[:2500])
    doc.close()
    print()
