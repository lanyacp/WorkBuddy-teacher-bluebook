# -*- coding: utf-8 -*-
"""导出关键文档的完整 media_id，便于逐篇取内容。"""
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

F = r"C:\Users\Administrator\.workbuddy\projects\d-projects-WorkBuddy-2026-06-17-11-18-20\c2be77f6-b2ff-4d85-bf51-f888ab938b09\tool-results\mcp-ima-mcp-search_knowledge-1791083798418-31ce15.txt"
d = json.load(open(F, encoding="utf-8"))
KEY = ["产品简介", "如何下指令", "教师AI能力进阶", "效率提升技巧", "三句话心态",
       "教育专家与教学Skill", "Skill安装与一键使用", "周期任务配置", "隐私与数据安全",
       "100条提示词", "102个技能", "使用手册", "AI先锋教师成长路径", "分学科备课模板",
       "一键生成课件", "本地批量自动批改", "交互式HTML报告", "期末评语批量生成",
       "家长会通知与材料", "教研论文撰写", "语言类实战案例", "分层任务单", "常见问题"]
seen = set()
for it in d.get("searched_knowledge_list", []):
    k = it.get("knowledge", {})
    t = k.get("title", "")
    if any(s in t for s in KEY) and k.get("media_id") not in seen:
        seen.add(k.get("media_id"))
        print("%-46s | %-4s | %s" % (t[:44], k.get("media_type"), k.get("media_id")))
