# -*- coding: utf-8 -*-
"""从指引原文 PDF 抽取「30个场景示例 + 18个行为示例」，生成结构化摘要（清洗版）。"""
import os, re, fitz

OUT = r"D:\projects\WorkBuddy\2026-06-17-11-18-20\参考资料"
PDF = os.path.join(OUT, "教师生成式人工智能应用指引(第一版).pdf")

d = fitz.open(PDF)
raw = "".join(d[i].get_text() for i in range(d.page_count))
d.close()
t = re.sub(r"\s+", "", raw)

SCENE_SECS = ["助力学习变革", "助力教学提质", "助力育人进阶", "助力评价增效", "助力管理升级", "助力研究创新"]
NORM_SECS = ["坚持育人主体地位", "加强内容审查把关", "恪守学术创作伦理", "引导学生规范使用", "合规合法处理数据", "践行技术智能向善"]

# 所有示例标记
pat = re.compile(r"【(场景示例|行为示例)(\d+)】[:：]?")
marks = list(pat.finditer(t))
# 所有章节锚点（场景6 + 规范6）—— 用 rfind 取正文标题（避开目录）
anchors = []
for s in SCENE_SECS + NORM_SECS:
    p = t.rfind(s)
    anchors.append((p, s))
anchors = [(p, s) for p, s in anchors if p >= 0]
anchors.sort()

def section_of(pos):
    cur = ""
    for p, s in anchors:
        if p < pos:
            cur = s
        else:
            break
    return cur

def clean(body):
    # 截到下一个章节标题（含「四、规范指引」等大标题）
    m = re.search(r"（[一二三四五六]）|[一二三四五六五]、[\u4e00-\u9fa5]{2,6}", body)
    if m:
        body = body[:m.start()]
    # 去掉页眉页脚
    body = re.sub(r"教师生成式人工智能应用(指引|指南)（第一版）\d*", "", body)
    return body.strip().rstrip("。")

def split_name_desc(body):
    body = clean(body)
    parts = re.split(r"[:：。]", body, maxsplit=1)
    name = parts[0].strip()[:14]
    desc = (parts[1] if len(parts) > 1 else "").strip()
    return name, (desc or body)[:150]

items = []
for i, m in enumerate(marks):
    end = marks[i + 1].start() if i + 1 < len(marks) else len(t)
    items.append({"kind": m.group(1), "num": int(m.group(2)),
                  "sec": section_of(m.start()), "body": t[m.end():end]})
scenes = [x for x in items if x["kind"] == "场景示例"]
behavs = [x for x in items if x["kind"] == "行为示例"]
print("场景示例:", len(scenes), "行为示例:", len(behavs))

L = ["# 《教师生成式人工智能应用指引（第一版）》要点摘录\n",
     "- **发布单位**：教育部教师队伍建设专家指导委员会",
     "- **发布时间**：2025 年 11 月",
     "- **主体结构**：场景指引（正面清单，30 个场景示例）+ 规范指引（约束清单，18 个行为示例）",
     "- **来源**：`教师生成式人工智能应用指引(第一版).pdf`（本目录）",
     "- **说明**：场景指引按「学习变革 / 教学提质 / 育人进阶 / 评价增效 / 管理升级 / 研究创新」六大助力各 5 例；规范指引按六大行为边界各 3 例。以下为原文摘录整理。\n",
     "## 一、场景指引 · 30 个场景示例（正面清单：可以怎么用）"]

def sec_head(name, catalog, L):
    idx = catalog.index(name) if name in catalog else 0
    L.append(f"\n### （{'一二三四五六'[idx]}）{name}\n")

cur = None
for x in scenes:
    if x["sec"] and x["sec"] != cur:
        cur = x["sec"]
        sec_head(cur, SCENE_SECS, L)
    name, desc = split_name_desc(x["body"])
    L.append(f"**{x['num']}. {name}**　{desc}\n")

L.append("\n## 二、规范指引 · 18 个行为示例（约束清单：什么不能做）")
cur = None
for x in behavs:
    if x["sec"] and x["sec"] != cur:
        cur = x["sec"]
        sec_head(cur, NORM_SECS, L)
    name, desc = split_name_desc(x["body"])
    L.append(f"**{x['num']}. {name}**　{desc}\n")

out_md = os.path.join(OUT, "00_指引要点摘录_30场景18行为.md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("写出:", out_md)
print("章节归属检查（前3/后3）：")
for x in scenes[:3] + scenes[-3:]:
    print("  ", x["kind"], x["num"], "->", x["sec"])
for x in behavs[:2] + behavs[-2:]:
    print("  ", x["kind"], x["num"], "->", x["sec"])
