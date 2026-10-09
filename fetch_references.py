# -*- coding: utf-8 -*-
"""下载「教师AI素养」相关原始资料，作为项目参考资料。"""
import os, ssl, urllib.request, urllib.error

OUT = r"D:\projects\WorkBuddy\2026-06-17-11-18-20\参考资料"
os.makedirs(OUT, exist_ok=True)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

ITEMS = [
    # (保存文件名, URL, 说明)
    ("教师生成式人工智能应用指引(第一版).pdf",
     "https://zpc.qzuie.edu.cn/uploadfile/24/Attachment/5832623968.pdf",
     "指引原文PDF（教育部教师队伍建设专家指导委员会 2025.11 发布）"),
    ("指引全文_溧水区政府.html",
     "https://www.njls.gov.cn/zmhd/zsk/jy/202601/t20260105_5757566.html",
     "指引全文（政府网站转载）"),
    ("指引全文_含30场景18行为_湖南石化职院.html",
     "https://www.hnshzy.cn/tsg/info/1020/1515.htm",
     "指引全文 + 30场景/18行为表格"),
    ("指引全文_含30场景_湖北职院.html",
     "https://qc.hbvtc.edu.cn/info/1175/23463.htm",
     "指引全文 + 30场景示例"),
    ("中新社_中国官方将启动教师人工智能素养全覆盖培训_20260904.html",
     "https://www.chinanews.com/gn/2026/09-04/10690593.shtml",
     "中新社 曾玥 2026-09-04 报道"),
    ("人民日报_AI时代老师为何不可替代_20260908.html",
     "https://finance.people.com.cn/n1/2026/0908/c1004-40794288.html",
     "人民日报 吴月 2026-09-08 第11版"),
    ("人民网_编辑手记_陪伴学生从知道走向理解_20260908.html",
     "https://edu.people.com.cn/n1/2026/0908/c1006-40794456.html",
     "人民日报同版 编辑手记"),
]

for name, url, desc in ITEMS:
    path = os.path.join(OUT, name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
        print(f"OK   {len(data):>9,} bytes  {name}")
    except Exception as e:
        print(f"FAIL {name}  <- {url}\n     {type(e).__name__}: {e}")

print("\n目录内容：")
for fn in sorted(os.listdir(OUT)):
    print("  ", fn, os.path.getsize(os.path.join(OUT, fn)))
