# -*- coding: utf-8 -*-
"""从 pages90/*.jsx 按阅读顺序抽取每页全部文本，并标注提示词/注脚。"""
import os, re, json

PAGES = r"D:\projects\WorkBuddy\2026-06-17-11-18-20\ppt_ai_edu\pages90"
OUT = r"D:\projects\WorkBuddy\2026-06-17-11-18-20\_pages_dump.json"

FOOT = "AI赋能中小学教育教学 · 县域教师培训"


def strip_tags(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()


TEXT_RE = re.compile(r"<Text\b([^>]*)>(.*?)</Text>", re.S)


def classify(attrs, body):
    if "'#E5E7EB'" in attrs and "fontSize:19" in attrs:
        return "prompt"
    if "textAlign:'center'" in attrs:
        return "note"
    if "'#FBBF24'" in attrs and "fontWeight:'bold'" in attrs:
        return "plabel"
    if "'#9FC6D4'" in attrs or "'#9CA3AF'" in attrs:
        return "meta"
    if "fontSize:14" in attrs and "'#94A3B8'" in attrs:
        return "skip"
    return "body"


data = {}
for fn in sorted(os.listdir(PAGES)):
    if not fn.endswith(".jsx"):
        continue
    no = int(re.match(r"p(\d+)_", fn).group(1))
    t = open(os.path.join(PAGES, fn), encoding="utf-8").read()

    items = []
    for m in TEXT_RE.finditer(t):
        attrs, body = m.group(1), strip_tags(m.group(2))
        if not body or FOOT in body or re.fullmatch(r"\d{1,2} / 90", body):
            continue
        kind = classify(attrs, body)
        if kind == "skip":
            continue
        items.append({"k": kind, "t": body})

    # 合并相邻同 kind 的 body
    merged = []
    for it in items:
        if merged and merged[-1]["k"] == "body" == it["k"]:
            merged[-1]["t"] += "\n" + it["t"]
        else:
            merged.append(it)

    data[no] = {
        "title": next((x["t"] for x in merged if x["k"] == "body"), ""),
        "items": merged,
    }

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

np = sum(1 for v in data.values() for x in v["items"] if x["k"] == "prompt")
print("页数:", len(data), " 提示词条目:", np)
for no in [18, 49, 71, 82, 86]:
    v = data[no]
    print("\n--- P%02d  %s" % (no, v["title"][:30]))
    for x in v["items"][:9]:
        print("   [%s] %s" % (x["k"], x["t"].replace("\n", " ⏎ ")[:76]))
