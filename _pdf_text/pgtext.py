import pdfplumber,sys
pdf = r"C:/Users/Administrator/Desktop/WorkBuddy蓝皮书-.pdf"
pages=[int(x) for x in sys.argv[1].split(",")]
with pdfplumber.open(pdf) as d:
    for p in pages:
        t=(d.pages[p-1].extract_text() or "").replace("\n"," ")
        print(f"\n[p{p}] {t[:230]}")
