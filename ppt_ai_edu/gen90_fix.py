# -*- coding: utf-8 -*-
"""用统一模板重新生成 14 个迁移页，消除 .map() 字面量，保证可被顺序抽取。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen90_tpl import *

M, G, O, R = "#1A5F7A", "#2E7D32", "#F57C00", "#C0392B"

# ---------- P02 课程定位 ----------
page(2, "position", "课程定位", "五个班型，一套内容。按班型裁剪页码即可，不必重写", b_rows([
    ("1", "基础班（通识）", "全体教师　｜　模块 M + 工具 + 数据安全　｜　3-6 学时", M),
    ("2", "学科班", "学科骨干　｜　板块一 + 板块二　｜　12 学时", M),
    ("3", "进阶班（新技术）", "骨干 / 青年教师　｜　板块五 Skill + 自动化　｜　6 学时", G),
    ("4", "教研班", "教研组长 / 骨干　｜　板块三 + 论文写作　｜　12 学时", G),
    ("5", "管理班", "班主任 / 德育　｜　板块四　｜　6 学时", O),
], gap=11) + b_note("授课比例：讲座 30% · 实操 40% · 工作坊/跟岗 20% · 成果展评 10%",
                    "#1A5F7A", M))

# ---------- P04 学习目标 ----------
page(4, "objectives", "学习目标", "今天不讲工具清单，只讲四件你能带走的事", b_grid2([
    ("会提问", "能写出一条完整提示词", "说清角色、任务、要求三要素，抄学员手册的模板就能用", M),
    ("会应用", "能用 AI 产出一份真实材料", "教案、学情问卷、错题本、评语，至少一样真的做出来", G),
    ("会沉淀", "能把重复流程写成模板", "骨干学员能交出一个自建 Skill，一个人建好全组受益", O),
    ("会判断", "能识别 AI 输出哪里不对", "知道哪些必须人工复核，哪些根本不能用", R),
]) + b_note("结业时每人交一份「AI 赋能教学案例」，骨干学员另交一个自建 Skill", "#FFF7ED", O))

# ---------- P08 AI 能与不能 ----------
page(8, "ability_boundary", "AI 能做什么，不能做什么", "先划边界，再谈用法。这一页能省掉你很多焦虑", b_twocol(
    "能做，而且做得快",
    ["大量重复性的文字工作（教案、评语、通知）",
     "按模板批量生成（试题、练习、变式）",
     "整理归纳（错题归类、成绩分析、资料汇总）",
     "提供多版本供你挑选对比",
     "陪你练口语、随时提问"],
    "做不了，也别交给它",
    ["替你判断学生到底学会了没有",
     "替你做价值引领和情感沟通",
     "保证事实正确、保证不超纲",
     "替你承担责任（签字的是你）",
     "处理未脱敏的学生隐私数据"],
    G, R) + b_note("AI 始终是助手，育人主体永远是老师　——　出自《教师生成式人工智能应用指引》",
                    "#F4F8FA", M))

# ---------- P10 工具地图 ----------
page(10, "tool_map", "免费工具地图", "8 款够用了。每个工具只讲一个最常用场景，不要贪多", b_cards([
    ("", "DeepSeek", "对话大模型　｜　写教案、拟提示词、改文字　｜　网页版直接开", M),
    ("", "豆包", "对话大模型　｜　手机随时问答　｜　App 课前装好", M),
    ("", "腾讯元宝", "对话大模型　｜　做主力工具之一、备用　｜　微信小程序", M),
    ("", "腾讯 ima", "个人知识库　｜　存试卷、建错题库　｜　P37 要用", G),
    ("", "Kimi", "长文本　｜　读整本教材单元　｜　长文本是它的长处", G),
    ("", "问卷工具", "表单收集　｜　学情问卷、家长回执　｜　问卷星免注册可试用", G),
    ("", "扣子 Coze", "工作流　｜　批量自动化，进阶　｜　课上演示不要求上手", O),
    ("", "WorkBuddy", "桌面客户端　｜　Skill 技能　｜　课前务必发安装包", O),
], cols=4) + b_note("建议只挑 2 样用熟 21 天。全学一遍，等于一个都没学会", "#FFF7ED", O))

# ---------- P11 提示词公式 ----------
body11 = ("  <Box style={{ flex:1, flexDirection:'column', marginTop:12, gap:12 }}>\n"
          "    <Box style={{ flexDirection:'row', gap:12 }}>\n"
          "      <Box style={{ flex:1, background:'#1A5F7A', borderRadius:12, padding:'16px 18px' }}>\n"
          "        <Text style={{ fontSize:25, fontWeight:'bold', color:'#FFFFFF' }}>角色</Text>\n"
          "        <Text style={{ fontSize:17, color:'#CFE3EA', marginTop:8, lineHeight:1.5 }}>你是一位有 10 年教龄的初中英语教师</Text>\n"
          "      </Box>\n"
          "      <Box style={{ flex:1, background:'#2E7D32', borderRadius:12, padding:'16px 18px' }}>\n"
          "        <Text style={{ fontSize:25, fontWeight:'bold', color:'#FFFFFF' }}>任务</Text>\n"
          "        <Text style={{ fontSize:17, color:'#D5EBD9', marginTop:8, lineHeight:1.5 }}>请帮我为七年级设计一份 Unit 1 写作任务</Text>\n"
          "      </Box>\n"
          "      <Box style={{ flex:1, background:'#F57C00', borderRadius:12, padding:'16px 18px' }}>\n"
          "        <Text style={{ fontSize:25, fontWeight:'bold', color:'#FFFFFF' }}>要求</Text>\n"
          "        <Text style={{ fontSize:17, color:'#FDEBD0', marginTop:8, lineHeight:1.5 }}>80 词左右，含 3 个可替换点，用初中词汇</Text>\n"
          "      </Box>\n"
          "    </Box>\n"
          "    <Box style={{ background:'#1F2937', borderRadius:12, padding:'16px 20px' }}>\n"
          "      <Text style={{ fontSize:19, color:'#E5E7EB', marginTop:12, lineHeight:1.7 }}>你是一位有 10 年教龄的初中英语教师。请帮我为七年级设计一份 Unit 1 写作任务。要求 80 词左右，含 3 个可替换点，用初中词汇。</Text>\n"
          "    </Box>\n"
          "    <Box style={{ flexDirection:'row', gap:12, flex:1 }}>\n"
          "      <Box style={{ flex:1, background:'#EAF4EA', borderRadius:10, padding:'12px 14px' }}>\n"
          "        <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32' }}>追问细化</Text>\n"
          "        <Text style={{ fontSize:16, color:'#1F2937', marginTop:6, lineHeight:1.45 }}>太简单了，改成每项配 2-3 句示例</Text>\n"
          "      </Box>\n"
          "      <Box style={{ flex:1, background:'#EAF4EA', borderRadius:10, padding:'12px 14px' }}>\n"
          "        <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32' }}>给范例</Text>\n"
          "        <Text style={{ fontSize:16, color:'#1F2937', marginTop:6, lineHeight:1.45 }}>照这个格式再写一份：附上你已认可的一段</Text>\n"
          "      </Box>\n"
          "      <Box style={{ flex:1, background:'#EAF4EA', borderRadius:10, padding:'12px 14px' }}>\n"
          "        <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32' }}>限定输出</Text>\n"
          "        <Text style={{ fontSize:16, color:'#1F2937', marginTop:6, lineHeight:1.45 }}>用表格输出，每题标注难度与知识点</Text>\n"
          "      </Box>\n"
          "      <Box style={{ flex:1, background:'#EAF4EA', borderRadius:10, padding:'12px 14px' }}>\n"
          "        <Text style={{ fontSize:18, fontWeight:'bold', color:'#2E7D32' }}>让它自检</Text>\n"
          "        <Text style={{ fontSize:16, color:'#1F2937', marginTop:6, lineHeight:1.45 }}>写完自查有无超纲，并标出存疑处</Text>\n"
          "      </Box>\n"
          "    </Box>\n"
          "  </Box>\n")
page(11, "prompt_formula", "提示词公式：角色 + 任务 + 要求",
     "全场最重要的一页。后面每个板块都靠它，砍了后面全废", body11)

# ---------- P14 三条红线 ----------
page(14, "safety_3rules", "数据安全三条红线", "只有 10 分钟，但每一条都不能破。全场唯一必须讲的内容",
     b_cards([
         ("1", "学生隐私数据不上传", "姓名、身份证、住址、电话先脱敏，用「学生 A / 学生 B / 班级 1」代替。录课堂音视频前要先向学生与监护人说明并取得单独授权。", R),
         ("2", "AI 输出必须人工复核", "批改、评语、试题、分析结论都要老师把关。AI 给的是草稿，出问题签字的是你，责任不会转移给工具。", R),
         ("3", "成文内容标注 AI 参与", "论文、课题、案例如实说明 AI 辅助情况。核心论点与论证过程必须自己完成，不能直接提交生成内容。", R),
     ], cols=3) + b_note("这三条会在讲到学生信息、评语批改、论文写作时反复回扣。提示卡已发到手", "#FCEBEA", R))

# ---------- 章节页 ----------
SECS = [
    (15, "sec1_cover", "板块一　P15 - P30", "学科赋能", "从「做课件」升级到「提质量」",
     ["理念层", "流程层", "学科层", "质量层", "跨学科"],
     "AI 的价值不在做 PPT，而在于按学科特点重塑教学理念与流程"),
    (31, "sec2_cover", "板块二　P31 - P46", "学情闭环", "采集 → 分析 → 错题 → 出题 → 分层 → 组卷",
     ["学情采集", "分析可视化", "试卷储存", "错题集", "个性化出题", "分层作业"],
     "这是全场最容易出成果的一个板块，务必留足实操时间"),
    (47, "sec3_cover", "板块三　P47 - P58", "教研与专业成长", "把 AI 嵌进研修，也写进论文与职称",
     ["校本研修", "集体备课", "听课评课", "设计打磨", "论文写作", "课题职称"],
     "超时优先砍这一块，砍掉不影响学员获得感"),
    (59, "sec4_cover", "板块四　P59 - P69", "学生管理与家校协同", "班主任与科任教师的日常，最碎也最耗时",
     ["班会设计", "批量评语", "家长会材料", "分场景话术", "成长档案", "班级数据"],
     "非班主任班可把家校部分合并讲，重点放合规与班级数据"),
    (70, "sec5_cover", "板块五　P70 - P83　压箱底", "Skill 技能与自动化", "把「每次都要交代一长串要求」，打包成「以后一句话就能跑」",
     ["什么是 Skill", "为什么最该学", "三步走", "教学例子", "沉淀自己的", "自动化"],
     "以 WorkBuddy 为例，教育版已上架 15 个即插即用教学 Skill"),
]
for no, slug, no_lbl, title, sub, tags, tail in SECS:
    with open(os.path.join(DST, "p%02d_%s.jsx" % (no, slug)), "w", encoding="utf-8") as f:
        f.write(b_section(no_lbl, title, sub, tags, tagcol="#CFE3EA").replace(
            "  <Text style={{ fontSize:20, color:'#CFE3EA', marginTop:28 }}>%s</Text>" % tail,
            "  <Text style={{ fontSize:20, color:'#CFE3EA', marginTop:28 }}>%s</Text>" % tail))

# ---------- P19 学习路径图 ----------
page(19, "learning_path", "学习路径图", "把单元从「起点」画到「终点证据」，每级台阶标明怎么检验",
     b_rows([
         ("1", "起点", "学生现在会什么。这是基线，不是零起点", "#94A3B8"),
         ("2", "台阶一 · 概念理解", "能用自己的话把概念说清", M),
         ("3", "台阶二 · 基本应用", "能在单一情境里用起来", G),
         ("4", "台阶三 · 迁移探究", "换个情境还能用，会举一反三", O),
         ("5", "终点 · 证据", "拿得出可检验的产出：作品、解题过程、讲解录音", R),
     ], gap=11) + b_prompt(
         "你是一位有 10 年教龄的＜学科＞教师。请把＜年级＞＜单元＞的所有知识点，"
         "设计成一张从易到难的学习路径图，每个台阶标出检验方式。"
         "分成「起点—概念理解—基本应用—迁移探究—终点证据」五级。",
         None, "提示词（改尖括号即可用）")
     + b_note("AI 出的路径图必须自己改，至少改 3 处，那 3 处就是你的教学判断", "#FFF7ED", O))

# ---------- P32 六步闭环 ----------
page(32, "loop_overview", "六步闭环", "采数据 → 看得懂 → 出得准，形成可重复的循环",
     b_rows([
         ("1", "学情采集", "表单建问卷 / AI 出题 / 扫码收数据，课前 3 分钟收完", M),
         ("2", "分析与可视化", "一键统计 / 学情画像 / 找薄弱点", G),
         ("3", "试卷储存与分析", "用 ima 个人知识库存历次试卷，长期追踪", G),
         ("4", "错题集", "AI 识错 / 错因归类 / 自动成错题本", O),
         ("5", "个性化出题", "按薄弱点定向出题 / 一题多变", O),
         ("6", "分层作业与组卷", "基础 / 提高 / 拓展三层，照细目表组卷", R),
     ], gap=10) + b_note("闭环的意思是：这一步的产出，是下一步的输入。走到学生数据这步回头讲红线", "#EAF4EA", G))

# ---------- P74 三步走 ----------
page(74, "skill_three_steps", "三步走：找装 → 触发 → 微调", "现场走一遍，你就知道该在哪一步花时间",
     b_rows([
         ("1", "找 / 装", "在技能市场搜索你学科的技能，一键安装。11 大类教师技能，按学科找", M),
         ("2", "触发", "用一句自然语言指令触发。要素 = 学科 + 年级 + 教材版本 + 单元/主题 + 数量难度 + 产出格式", G),
         ("3", "微调", "产出后对话修改，比如「选择题增加到 10 道」，确认后再导出", O),
     ], gap=12) + b_note("触发指令模板：学科＜学科＞｜年级＜年级＞｜版本＜教材版本＞｜单元＜单元/主题＞｜数量难度＜数量与难度＞｜产出＜格式＞",
                         "#1F2937", "#1F2937"))

print("14 页已重新生成")
