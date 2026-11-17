# -*- coding: utf-8 -*-
"""从蓝皮书附录 A 提取各模板的可复制指令原文，供课程手册引用。"""
import re
from pathlib import Path

ROOT = Path(r"D:/projects/WorkBuddy/2026-06-17-11-18-20/教师版蓝皮书")
src = (ROOT / "附录A_常用指令模板.md").read_text(encoding="utf-8")

parts = re.split(r"(?=^### )", src, flags=re.M)
out = []
for part in parts:
    m = re.match(r"### ([^\n]+)", part)
    if not m:
        continue
    title = m.group(1).strip()
    blocks = re.findall(r"```[^\n]*\n(.*?)```", part, flags=re.S)
    if not blocks:
        continue
    body = blocks[0].strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    out.append("### %s\n%s\n" % (title, body[:520]))

txt = "\n".join(out)
print(txt)
print("\n[TOTAL BLOCKS] =", len(out))
