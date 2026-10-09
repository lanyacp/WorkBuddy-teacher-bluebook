# -*- coding: utf-8 -*-
"""解析 ima 搜索结果，列出命中文档清单。"""
import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

F = r"C:\Users\Administrator\.workbuddy\projects\d-projects-WorkBuddy-2026-06-17-11-18-20\c2be77f6-b2ff-4d85-bf51-f888ab938b09\tool-results\mcp-ima-mcp-search_knowledge-1791083798418-31ce15.txt"
d = json.load(open(F, encoding="utf-8"))
lst = d.get("searched_knowledge_list", [])
print("命中条数:", len(lst))
print("=" * 70)
for i, it in enumerate(lst, 1):
    k = it.get("knowledge", {})
    intro = re.sub(r"</?em>", "", k.get("introduction") or "")
    intro = re.sub(r"\s+", " ", intro)[:150]
    print("%2d. [%s] %s" % (i, it.get("parent_folder_name", ""), k.get("title", "")))
    print("    id=%s  type=%s  fetch=%s" % (k.get("media_id", "")[:46], k.get("media_type"), k.get("can_fetch_content")))
    if intro:
        print("    %s" % intro)
