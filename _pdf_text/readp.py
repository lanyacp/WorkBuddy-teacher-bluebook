import sys, pdfplumber
pdf = r"C:/Users/Administrator/Downloads/WorkBuddy教师手册.pdf"
import os
if not os.path.exists(pdf):
    pdf = r"D:/BaiduNetdiskDownload/项目汇总/WorkBuddy教师手册.pdf"
pages = [int(x) for x in sys.argv[1].split(",")]
with pdfplumber.open(pdf) as d:
    for p in pages:
        print(f"\n{'='*20} p{p} {'='*20}")
        print(d.pages[p-1].extract_text() or "")
