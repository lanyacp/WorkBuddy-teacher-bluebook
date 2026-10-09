# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import parse_xml

C_MAIN = RGBColor(0x1a, 0x5f, 0x7a)
C_GREEN = RGBColor(0x2e, 0x7d, 0x32)
C_ORANGE = RGBColor(0xf5, 0x7c, 0x00)
C_RED = RGBColor(0xc0, 0x00, 0x00)
C_GRAY = RGBColor(0x33, 0x33, 0x33)

def set_run_font(run, font_name='微软雅黑', size=10.5, bold=False, color=None):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color

def H(doc, text, level=1):
    h = doc.add_heading(level=level)
    run = h.add_run(text)
    if level == 1:
        set_run_font(run, size=16, bold=True, color=C_MAIN)
    elif level == 2:
        set_run_font(run, size=14, bold=True, color=C_GREEN)
    elif level == 3:
        set_run_font(run, size=12, bold=True, color=C_ORANGE)
    else:
        set_run_font(run, size=11, bold=True)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return h

def P(doc, text, bold=False, indent=True, size=10.5, color=None):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.first_line_indent = Cm(0.74)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, color=color)
    return p

def BUL(doc, text, level=0, size=10.5, color=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Cm(0.74 + level * 0.5)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    set_run_font(run, size=size, color=color)
    return p

def NUM(doc, text, level=0, size=10.5):
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.left_indent = Cm(0.74 + level * 0.5)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    set_run_font(run, size=size)
    return p

def fill(cell, hex_color):
    xml = '<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fill="' + hex_color + '"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(xml))

def quote_box(doc, text):
    """一线教师原声引用框"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.74)
    p.paragraph_format.line_spacing = 1.4
    run = p.add_run('“' + text + '”')
    set_run_font(run, size=9.5, color=C_GRAY)
    run.italic = True
    return p

def prompt_box(doc, title, content):
    P(doc, '【' + title + '】', bold=True, indent=False, color=C_MAIN)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.left_indent = Cm(0.74)
    run = p.add_run(content)
    set_run_font(run, size=9, color=C_GRAY)
    return p

def make_table(doc, headers, rows, widths, header_color='1A5F7A', font_size=9):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, htext in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = htext
        for para in c.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in para.runs:
                set_run_font(r, size=font_size, bold=True, color=RGBColor(0xff, 0xff, 0xff))
        fill(c, header_color)
    for ri, row in enumerate(rows, start=1):
        for ci, text in enumerate(row):
            c = t.rows[ri].cells[ci]
            c.text = text
            for para in c.paragraphs:
                para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                para.paragraph_format.line_spacing = 1.25
                for r in para.runs:
                    set_run_font(r, size=font_size)
    for row in t.rows:
        for ci, w in enumerate(widths):
            row.cells[ci].width = Inches(w)
    return t

# ============ 创建文档 ============
doc = Document()
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
style.font.size = Pt(10.5)
style.paragraph_format.line_spacing = 1.5

# ===== 封面 =====
t1 = doc.add_paragraph(); t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t1.add_run('AI赋能英语教学·一线真实案例与痛点解法'); set_run_font(r, size=21, bold=True, color=C_MAIN)
t2 = doc.add_paragraph(); t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t2.add_run('——禅城区7校实践探索的痛点提炼与课堂落地'); set_run_font(r, size=15, bold=True, color=C_GREEN)
doc.add_paragraph()
info = doc.add_paragraph(); info.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = info.add_run('案例来源：佛山市禅城区中学英语教研《AI赋能英语教学实践探索》(一)—(七)\n'
                 '适配教材：牛津译林版初中英语\n'
                 '主用工具：WorkBuddy（Agent+Skill）+ 飞象老师（互动网页）+ 国家智慧中小学平台"用AI"应用\n'
                 '用途：作为3小时培训的"真实案例模块"，也可作教师课后速查手册')
set_run_font(r, size=11)
doc.add_paragraph()
tip = doc.add_paragraph(); tip.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = tip.add_run('痛点真 · 做法实 · 可复制 · 能迁移'); set_run_font(r, size=12, bold=True, color=C_ORANGE)
doc.add_page_break()

# ===== 一、为什么讲真实案例 =====
H(doc, '一、为什么用"真实案例"来讲', 1)
P(doc, '本手册不是理论汇编，而是禅城区7所学校一线英语教师"用了、错了、改了、成了"的真实记录。之所以把它放进培训，是因为：', indent=False)
BUL(doc, '痛点真——每一个痛点都来自真实课堂：讲评课学生走神、早读没人开口、作文范文记不住、语法备课量翻倍……老师们一听就懂、一看就有共鸣。')
BUL(doc, '做法实——每一个做法都经过课堂检验，形成了"工具研发—课堂应用—效果反馈"的完整闭环，不是纸上谈兵。')
BUL(doc, '可复制——所有做法都无需编程基础，"会用微信聊天就能用"，且都能打包成Skill反复调用。')
BUL(doc, '能迁移——本手册已将每个案例迁移到牛津译林版初中单元，拿来即用。')

P(doc, '【关于工具的一点说明】', bold=True, indent=False, color=C_RED)
P(doc, '7篇文章中，老师们主要用的是Trae（字节跳动的AI原生开发环境）和豆包，互动游戏用飞象老师。本次培训我们以WorkBuddy为主工具——请放心：WorkBuddy与Trae同属"AI Agent + Skill"平台，都能"对话式操作、无需编程、生成HTML工具、把经验打包成Skill反复用"，操作逻辑完全相通。文章里"用Trae做的一切"，在WorkBuddy里同样能做，且WorkBuddy的Skill生态更适合教师建专属工具库。互动游戏类（水果忍者、跟读动画）继续用飞象老师（国家智慧中小学平台"用AI"应用，账号单点登录、免费、安全）。', indent=True)
P(doc, '所以本手册的读法是：看痛点→看老师们的原始做法→看WorkBuddy/飞象老师如何实现同款→拿译林版指令直接试。', indent=True, bold=True, color=C_GREEN)
doc.add_page_break()

# ===== 二、7校案例总览表 =====
H(doc, '二、7校案例总览表', 1)
P(doc, '一张表看懂7所学校做了什么。（"环节"指对应的教学场景，"原始工具"是文章中实际所用，"本培训实现"是我们用WorkBuddy/飞象老师的等效方案）', indent=False, size=9.5)

headers = ['期数/学校', '核心痛点', 'AI做法', '原始工具', '本培训实现', '成果']
rows = [
    ['(一) 佛大附校\n招蔼珊·孙雅琪',
     '讲评课学生被动听、走神；基础弱跟不上；早读词汇跟读单调、发音无纠正',
     '试卷评讲交互HTML（1.0→3.0迭代）；词汇跟读互动页；需求打包成Skill',
     'Trae',
     'WorkBuddy生成评讲/跟读HTML+建Skill',
     '学生抢着上台点屏、主动验答案；错题整理正确率提升'],
    ['(二) 市实验学校\n杨小红',
     '期末评讲不直观；语法/完形命题耗时；答案分布不均',
     'AI Agent概念；交互HTML；语法/完形命题；分析真题→打包Prompt复用',
     'Trae',
     'WorkBuddy命题Skill+Prompt模板库',
     '命题效率大幅提升；沉淀个人Prompt库'],
    ['(三) 澜石中学\n罗浩',
     '完形讲评整理解析耗时；单词默写、早读单调',
     '完形评讲网页；单词拼写PK网页；"大声朗读种小树"早读激励(麦克风测音量)',
     'Trae',
     'WorkBuddy生成同款+飞象老师游戏',
     '基础弱学生也参与互动；早读氛围提升'],
    ['(四) 第十中学\n黄家裕',
     '学生表达停留机械记忆、难真实运用；课堂缺可视化评价；不会向AI表达需求',
     'My Daily Schedule Planner互动网页；用"语音讨论"引导完善需求',
     'Trae',
     'WorkBuddy对话式共创工具+评价页',
     '任务型输出；反思出"句式脚手架"改进方向'],
    ['(五) 佛外学校\n罗彩甜',
     '备课效率低；期末评讲；课前难激活旧知',
     '拓展阅读课例+HTML课件；对答案HTML；词汇小游戏；飞象老师水果忍者/微语境动画',
     'Trae+飞象老师',
     '沿用：WorkBuddy备课+飞象老师游戏',
     '备课效率大幅提升；全班参与、气氛热烈'],
    ['(六) 城北中学\n罗艳君·潘春燕',
     '泛听课难推行；视频难检测是否真懂；听测题难兼顾趣味与实效',
     '豆包(内容工厂)+Agent(专属助教)互补；化文为影；截取视频关键帧→图片排序；豆包生成分层听测题',
     '豆包+Trae',
     'WorkBuddy分层听测Skill+截图工具',
     '泛听课得以推行；精准捕捉理解盲区'],
    ['(七) 佛外高中部\n徐佳岚·游伟仪',
     '词汇听默单调；早读参差不敢开口；真题被动刷；范文记不住；语法备课翻倍',
     '"五化"：词汇游戏化/跟读标准化/真题闯关化/写作分层化/语法专题化',
     'Trae+飞象老师',
     'WorkBuddy五化Skill+飞象老师',
     '学生抢着闯关；金句迁移力提升；备课时间大幅缩短'],
]
make_table(doc, headers, rows, [0.95, 1.35, 1.65, 0.7, 1.2, 1.15], font_size=8)
doc.add_paragraph()
P(doc, '共性发现：7所学校、10余位教师，殊途同归地走出同一条路径——"区域培训→科组二次分享→带班试用→打磨迭代→打包Skill→常态应用"。这条路径，就是本培训希望每位老师带回学校复制的路径。', indent=True, bold=True, color=C_GREEN)
doc.add_page_break()

# ===== 三、六大高频痛点 × 解法卡 =====
H(doc, '三、六大高频痛点 × 解法卡（译林版落地）', 1)
P(doc, '把7篇案例中反复出现的痛点，归纳为一线最普遍的六类。每张卡片：真实痛点原声 → 解法思路 → WorkBuddy/飞象老师操作 → 译林版指令，可直接复制试用。', indent=False, size=9.5)

# 痛点1
H(doc, '痛点卡① 讲评课：学生被动听、走神，基础弱跟不上', 3)
P(doc, '【一线原声】', bold=True, indent=False)
quote_box(doc, '基础薄弱的孩子，还没听明白第一题，老师已经讲到第五题了。（澜石中学 罗浩）')
quote_box(doc, '原本容易走神的基础薄弱学生，也能借助页面对应知识点的讲解听懂内容、跟上进度。（佛大附校 招蔼珊）')
P(doc, '【解法思路】', bold=True, indent=False)
P(doc, '把"老师讲、学生听"的试卷/完形讲评，变成"学生点、自己验"的交互HTML页面——点击出答案与解析，可显示/隐藏、可重置进度，学生从被动听讲转为主动验答案。', indent=True)
P(doc, '【WorkBuddy操作】', bold=True, indent=False)
BUL(doc, '新建独立工作文件夹（重要：AI对该文件夹有完全读写权限，勿放桌面或重要文件）')
BUL(doc, '上传试卷/习题文档 → 输入指令生成交互HTML → 双击浏览器打开即用')
BUL(doc, '不满意就在同一对话继续说需求（调布局、标解题线索、颜色区分题型），多轮迭代到"最贴合讲课习惯"的版本')
BUL(doc, '满意后打包成Skill："试卷评讲页面生成器"，下次上传新卷一键复用')
prompt_box(doc, '译林版·评讲页指令',
    '请把这份文档生成一个"支持点击查看答案的交互式HTML评讲页面"：\n'
    '① 每题点击显示答案+解析，可一键显示/隐藏全部答案、可重置进度；\n'
    '② 用不同颜色区分题型（如语法填空/完形/阅读）；\n'
    '③ 标注每题解题线索关键词；\n'
    '④ 适配大屏触控，学生可上台点击；字体清晰、界面简洁。\n'
    '（内容：粘贴译林版八上Unit X的语法填空/完形习题）')

# 痛点2
H(doc, '痛点卡② 词汇：听默写形式单调，学生兴趣低、记不牢', 3)
P(doc, '【一线原声】', bold=True, indent=False)
quote_box(doc, '常规单词短语听默写的检测形式单调，学生容易兴趣不高，记忆效果差。（佛外高中部 徐佳岚）')
P(doc, '【解法思路】', bold=True, indent=False)
P(doc, '把默写变成游戏化互动：单词拼写PK、水果忍者切词、卡片跟读纠音，让学生"抢着上台"。', indent=True)
P(doc, '【飞象老师操作（互动游戏首选）】', bold=True, indent=False)
BUL(doc, '打开飞象老师网页（国家智慧中小学平台"用AI"应用，账号单点登录、学生免注册）')
BUL(doc, '导入"水果忍者/单词PK"模板链接 → 指令里替换成本单元要检测的单词短语')
BUL(doc, '3分钟生成双人PK切词游戏：切中正确词得分并发音，切错扣血；大屏触控，学生上台抢答')
BUL(doc, '小技巧：PK前挑一边做示例，以提问带全班过一遍，确保后排也跟得上')
P(doc, '【WorkBuddy操作（拼写/词形练习）】', bold=True, indent=False)
BUL(doc, '词库按"英文：中文释义"格式上传，各班词汇分开管理，生成拼写答题页（含朗读、计时计分、双人PK分屏）')
prompt_box(doc, '译林版·词汇游戏指令（飞象老师内更改词表即可）',
    '检测词表（译林版七上Unit 5 Let\'s celebrate 核心词）：\n'
    'celebrate：庆祝 / lantern：灯笼 / dragon：龙 / mooncake：月饼 / …\n'
    '要求：切中正确词得分并朗读发音，切错扣一颗心；双人PK；率先完成或高分者胜。')

# 痛点3
H(doc, '痛点卡③ 早读：节奏参差，基础弱不敢开口、发音没人纠', 3)
P(doc, '【一线原声】', bold=True, indent=False)
quote_box(doc, '早读是黄金时段，但现实常常是：班里节奏参差，基础偏弱的学生不好意思开口，一个早读下来几乎没出声。（佛外高中部）')
P(doc, '【解法思路】', bold=True, indent=False)
P(doc, '两招：①"标准英音跟读页"——高亮文字+标准发音，带全班齐读；②"大声朗读种小树"——用麦克风实时测音量，达标就解锁植物成长动画，把朗读变成看得见的激励。', indent=True)
P(doc, '【操作】', bold=True, indent=False)
BUL(doc, '跟读页(WorkBuddy)：导入跟读模板，粘贴短语/课文金句，设发音参数（英音、语速0.75-0.9、"先听→留白跟读→再听"循环）')
BUL(doc, '如AI机械音生硬，把文件导入飞象老师，一句指令"用标准英音播音腔替换音频，发音饱满清晰"即可优化')
BUL(doc, '激励页(WorkBuddy)："大声朗读种小树"——调用麦克风监测分贝，阈值和达标时长可自定义，达标解锁花蕾→花朵→小树；自动累计时长，方便追踪全班、开展班级PK')
prompt_box(doc, '译林版·跟读页指令',
    '请生成一个"标准英音跟读互动页面"：\n'
    '① 逐句高亮显示译林版八上Unit 3 A day out 的课文原句/重点短语；\n'
    '② 英音女声，句子语速0.75，每句"先听一遍→静音留白2秒供跟读→再听一遍"循环；\n'
    '③ 支持连续跟读模式、单句重复、点击卡片纠音；\n'
    '④ 附听写/默写切换。')

# 痛点4
H(doc, '痛点卡④ 写作：范文结构记不住、金句不会用、换题就卡壳', 3)
P(doc, '【一线原声】', bold=True, indent=False)
quote_box(doc, '作文复习有一个老大难问题：范文发下去了，学生读了，但结构记不住、金句不会用、换个题目就写不出来。（佛外高中部）')
P(doc, '【解法思路】', bold=True, indent=False)
P(doc, '把范文做成"四步闯关"：完整范文展示→结构剖析（标注开头/正文/结尾功能与句式）→划三句必背金句→挖空闯关（给中文按词块留横线，点击显示英文）。答对礼花音效，答错萌音，降低畏难情绪。', indent=True)
P(doc, '【WorkBuddy操作】', bold=True, indent=False)
BUL(doc, '导入本学期范文合集，指令按题型（译林版常见：邀请信、建议信、人物介绍、活动报道等）各设独立关卡')
BUL(doc, '每关四步推进；挖空按"词块"留横线而非单词，训练句块迁移能力')
prompt_box(doc, '译林版·写作闯关指令',
    '请把这些范文做成"写作分层闯关"HTML，每种题型一个独立关卡：\n'
    '每关四步：①完整范文展示 ②结构剖析（标注开头/正文/结尾的功能和常用句式）'
    '③划出3句必背亮点金句 ④挖空闯关（给中文，按词块留横线，点击横线显示对应英文）；\n'
    '答对弹礼花+音效，答错发可爱提示音。\n'
    '（范文：粘贴译林版九上Unit 3 Teenage problems 建议信范文等）')

# 痛点5
H(doc, '痛点卡⑤ 语法/命题：梳理知识点+分层练习+解析，备课量翻倍', 3)
P(doc, '【一线原声】', bold=True, indent=False)
quote_box(doc, '语法教学最让老师头疼的，是梳理单元核心语法点并配套分层练习题，还要配逐题解析——一套流程走下来，备课量翻倍。（佛外高中部）')
quote_box(doc, '生成题目后可能遇到答案分布不均（如全部为A），可先让AI分析真题答案分布规律，再补进Prompt。（市实验 杨小红）')
P(doc, '【解法思路】', bold=True, indent=False)
P(doc, '让AI一条龙生成"讲—练—评"闭环：语法梳理（表格+口诀+例句）→分层练习（单词填空→短语填空→句子翻译→语法填空）→逐题解析；难度不合适再一句话调整。命题类先"分析真题规律→打包Prompt/Skill"，之后改关键词即可批量出题。', indent=True)
P(doc, '【WorkBuddy操作】', bold=True, indent=False)
BUL(doc, '导入教材单元语法要求与练习格式范例 → 生成语法梳理+分层练习+解析')
BUL(doc, '难度微调："把第5题难度降到及格线附近学生的水平"')
BUL(doc, '命题防坑：先让AI分析近五年中考真题的选材/答案分布，再把规律补进Prompt，避免答案扎堆')
prompt_box(doc, '译林版·语法专题指令',
    '角色：初中英语命题专家。任务：为译林版八上Unit 1 Friends（核心语法：形容词比较级/最高级）'
    '生成"讲—练—评"闭环：\n'
    '① 语法梳理（用表格+口诀+典型例句）；\n'
    '② 分层练习：单词填空→短语填空→句子翻译→语法填空，各5题，难度由易到难；\n'
    '③ 每题附逐题解析（标注考点+解题关键）；\n'
    '约束：贴合中考题型、适合中等水平学生。格式：可直接导出的练习卷+答案解析。')

# 痛点6
H(doc, '痛点卡⑥ 听力/泛听：视频看了但不知是否真懂，检测难兼顾趣味与实效', 3)
P(doc, '【一线原声】', bold=True, indent=False)
quote_box(doc, '如何设置合理检测，兼顾趣味和实效，既不破坏轻松氛围，又能判断学生是否真正看懂听懂视频内容，是当前的关键问题。（城北中学 罗艳君）')
quote_box(doc, '如果没有AI，学校的泛听课难于推行，是AI的参与赋予了课堂新能量。（城北中学）')
P(doc, '【解法思路】', bold=True, indent=False)
P(doc, '"内容工厂+专属助教"互补：先用通用大模型（豆包/WorkBuddy）快速产素材，再用Agent+Skill定制检测工具。视频检测用"截取关键帧→图片排序"任务，把隐性理解变成可观察的操作；有声读物/动画用AI提取台词→生成分层听测题。', indent=True)
P(doc, '【WorkBuddy操作】', bold=True, indent=False)
BUL(doc, '生成"视频截图工具"：按指令精准截取视频指定时间关键帧 → 设计成"图片排序"听力任务，直观看到谁"卡壳"')
BUL(doc, '提取动画/有声读物台词 → 生成分层理解练习题（同一素材，基础/提高分层），泛听课得以常态推行')
BUL(doc, '播放策略：第1遍完整看（保兴趣与理解），第2-3遍截取片段做纯听力练习')
prompt_box(doc, '译林版·分层听测指令',
    '请基于这段动画/听力素材的台词，生成"分层理解练习题"：\n'
    '① 基础层：5题细节理解（听关键信息选择）；\n'
    '② 提高层：3题推理判断+2题同义转述（同一意思不同句式）；\n'
    '③ 附"图片排序"任务：给4-6个关键帧，学生按情节先后排序；\n'
    '每题标注考点，附答案解析。（素材主题贴合译林版对应单元话题）')
doc.add_page_break()

# ===== 四、方法论提炼 =====
H(doc, '四、从7篇提炼的4条方法论（避坑指南）', 1)
P(doc, '案例之外，7位分享教师反复强调的"通用心法"，比单个工具更值得带走。', indent=False)

H(doc, '心法1：Prompt万能公式', 2)
P(doc, '两种等效表述，任选其一记住即可：', indent=False)
BUL(doc, '角色 + 任务 + 格式 + 约束（+示例）——市实验杨小红版')
BUL(doc, '背景 + 角色 + 需求 + 限制 + 格式——城北中学版')
P(doc, '反例vs正例："帮我备节课"（AI不知备哪节、备什么）→ "帮我备一节译林版七下Unit 5的听说课，包含教学目标、教学过程和板书设计"（精准可用）。', indent=True)

H(doc, '心法2：Skill打包——从"每次重说"到"一句复用"', 2)
P(doc, '豆包/普通对话是"单次临时Prompt，每次都要完整复制"；Skill是"永久封装，一句口令批量出"。打包三级思路（城北中学总结）：', indent=False)
make_table(doc, ['级别', '适合', '做法'],
    [['简易通用版', '新手一键生成', '把整套需求和方案，让AI"整合为一个技能文件"，导入即用'],
     ['精细化教学版', '月考/专项训练', '约束更严（词数、生词量、考点配比、干扰项设计），调用skill-creator生成标准化技能包'],
     ['完整定义版', '团队复用', '生成可导出的SKILL.md文件，含触发条件、角色受众、产出要求、输出结构、复用说明']],
    [1.0, 1.6, 4.0], header_color='2E7D32')
P(doc, '一句话记住：Skill建好后，"用初二阅读批量生成器，主题中国传统节日"这样一句短指令，就能批量出多篇——这就是教师专属工具库的价值。', indent=True, bold=True, color=C_GREEN)

H(doc, '心法3：五个常见问题与应对（市实验杨小红总结）', 2)
make_table(doc, ['常见问题', '应对办法'],
    [['输出与教材不符', '给AI提供教材截图或具体文本，基于真实内容生成，不要凭空编造'],
     ['生成内容难度不当', '在Prompt中明确学生水平，如"中等偏下""及格线附近"'],
     ['一次生成太多、质量差', '分步执行，每步检查调整后再进行下一步'],
     ['不知如何修改输出', '用自然语言即可："改成选择题""增加词汇表"，AI能理解'],
     ['AI偶尔出错或"编造"', '永远审核！AI是助手不是权威，所有内容需教师专业判断']],
    [1.6, 4.4], header_color='F57C00')

H(doc, '心法4：三条底线原则', 2)
BUL(doc, '教师是最终决策者——AI提供素材和框架，是否适合学生由教师判断，这是底线。（多校共识）')
BUL(doc, '好工具是"磨"出来的——第一版难尽善尽美，靠多轮迭代+课堂反馈打磨，像打磨一节精品课。核心三点：敢迈第一步、愿及时调整、能坚持打磨。（佛大附校）')
BUL(doc, '从"技术炫技"到"素养导向"——优秀AI课堂应是"看不见技术，只看得到学习"，技术自然融入，学生在完成任务中不知不觉提升语言能力，而非被花哨功能分散注意。（第十中学 黄家裕）')
doc.add_page_break()

# ===== 五、嵌入3小时培训 =====
H(doc, '五、如何把这些案例嵌入3小时培训', 1)
P(doc, '本手册不是独立材料，而是培训各模块的"真实弹药"。建议嵌入方式：', indent=False)
make_table(doc, ['培训模块', '嵌入的案例/痛点', '教学用法'],
    [['开场·痛点共鸣', '六大痛点卡的"一线原声"', '开场即抛真实原声，让老师"对号入座"，瞬间共鸣、建立学习动机'],
     ['概念·什么是Agent+Skill', '(二)(三)(六) Agent自主干活、Skill打包', '用"实习老师备全套材料"的比喻+澜石/佛外真实Skill案例讲清概念'],
     ['实操·生成交互工具', '痛点卡①③④ 评讲页/跟读页/写作闯关', '现场用WorkBuddy复现佛大附校/佛外高中部同款，学员跟做'],
     ['实操·飞象老师游戏', '痛点卡② 水果忍者/单词PK', '现场用飞象老师复现佛外/城北词汇游戏，替换译林词表即出'],
     ['实操·命题与分层', '痛点卡⑤⑥ 语法专题/分层听测', '用WorkBuddy走"讲-练-评"闭环+分层听测，配防坑技巧'],
     ['进阶·打包Skill', '心法2 三级打包', '带学员把刚做的工具打包成个人Skill，带走"能复用的资产"'],
     ['避坑·答疑', '心法3 五个常见问题', '把学员操作中遇到的问题对号入座，给出即时应对'],
     ['升华·结课', '心法4 三条底线原则', '回到育人初心："看不见技术，只看得到学习"，避免为用而用']],
    [1.3, 2.0, 2.7], header_color='1A5F7A')
P(doc, '一条主线：让每位老师带着"三样东西"离开——①至少一个亲手做的交互工具；②至少一个打包好的个人Skill；③一份译林版指令速查卡。', indent=True, bold=True, color=C_RED)
doc.add_page_break()

# ===== 附录 指令速查卡 =====
H(doc, '附录：译林版指令速查卡（复制即用）', 1)
P(doc, '把下面的指令直接粘到WorkBuddy或飞象老师，替换花括号内的单元/内容即可。建议打印成单页贴在办公桌。', indent=False, size=9.5)

cards = [
    ('① 试卷/完形评讲页', '把这份{译林版八上Unit X}习题生成支持点击查看答案的交互HTML评讲页：点击出答案+解析，可一键显示/隐藏、可重置，颜色区分题型，标注解题线索，适配大屏触控。'),
    ('② 词汇游戏（飞象老师）', '导入"水果忍者"模板，检测词表为{译林版七上Unit5核心词，英文:中文}；切中得分并发音，切错扣心，双人PK，高分者胜。'),
    ('③ 标准英音跟读页', '生成英音跟读页：逐句高亮{译林版八上Unit3课文原句}，英音语速0.75，"先听→留白2秒跟读→再听"循环，支持连续跟读+点击纠音+听写切换。'),
    ('④ 早读激励"种小树"', '生成"大声朗读种小树"页：调用麦克风监测音量，达标解锁花蕾→花朵→小树，分贝阈值和时长可自定义，自动累计朗读时长，支持班级PK。'),
    ('⑤ 写作分层闯关', '把{译林版九上建议信范文}做成写作闯关：每关四步(范文展示→结构剖析→划3句金句→按词块挖空)，答对礼花音效。'),
    ('⑥ 语法讲练评闭环', '为{译林版八上Unit1比较级}生成"讲-练-评"：语法梳理(表格+口诀+例句)+分层练习(单词填空→短语→翻译→语法填空各5题)+逐题解析，适合中等生。'),
    ('⑦ 分层听力测试', '基于{动画/听力素材}台词生成分层听测：基础5题细节+提高3题推理+2题同义转述+图片排序任务，每题标考点附解析。'),
    ('⑧ 打包成Skill', '将上述{评讲页/命题}生成的全部需求和方案，整合为一个技能文件，命名"{XX老师_XX生成器}"，之后我发口令即直接执行、不再追问。'),
]
for title, content in cards:
    prompt_box(doc, title, content)

doc.add_paragraph()
P(doc, '致谢：本手册所有痛点与做法，均源自佛山市禅城区中学英语教研《AI赋能英语教学实践探索》(一)至(七)7所学校一线教师的真实实践。感谢招蔼珊、孙雅琪、杨小红、罗浩、黄家裕、罗彩甜、罗艳君、潘春燕、徐佳岚、游伟仪等老师的探索与分享。', indent=True, size=9, color=C_GRAY)

out = 'D:/projects/WorkBuddy/2026-06-17-11-18-20/AI赋能英语教学_一线案例与痛点解法.docx'
doc.save(out)
print('SAVED:', out)
