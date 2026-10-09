import pdfplumber, re
pdf = r"C:/Users/Administrator/Desktop/WorkBuddy蓝皮书-.pdf"
# 用每章特征正文句来定位（目录页不会有这些句子）
anchors = {
 "ch02_下载安装登录": ["选择对应版本", "下载完成后", "双击安装包"],
 "ch03_主界面任务工作区": ["工作空间", "对话区", "任务列表"],
 "ch04_第一个任务": ["新建任务", "第一个任务"],
 "ch06_专家和专家团": ["专家团", "召唤专家"],
 "ch07_连接器": ["连接器", "授权"],
 "ch11_自动化任务": ["自动化", "定时"],
 "ch23_打造Skill": ["蒸馏", "SKILL.md"],
 "ch25_多Agent": ["多Agent", "多 Agent"],
 "ch26_自动化可靠性": ["可靠性"],
}
with pdfplumber.open(pdf) as d:
    pages=[(i+1,(d.pages[i].extract_text() or "")) for i in range(len(d.pages))]
for k,kws in anchors.items():
    hits=[p for p,t in pages if any(kw in t for kw in kws)]
    print(f"{k:24s} 命中页: {hits[:14]}")
