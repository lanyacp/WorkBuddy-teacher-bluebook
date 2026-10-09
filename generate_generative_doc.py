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
r = t1.add_run('AI赋能英语教学·"生成性质"活动设计'); set_run_font(r, size=21, bold=True, color=C_MAIN)
t2 = doc.add_paragraph(); t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t2.add_run('——用飞象老师 + 豆包/DeepSeek 网页版，少讲工具、多练产出'); set_run_font(r, size=14, bold=True, color=C_GREEN)
doc.add_paragraph()
info = doc.add_paragraph(); info.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = info.add_run('适配教材：牛津译林版初中英语\n'
                 '主用工具：①飞象老师（国家智慧中小学平台，权威、通用）\n'
                 '　　　　　②豆包 / DeepSeek 网页版（易上手、免工具讲解）\n'
                 '用途：3小时培训的"生成"模块方案 + 教师课后速查手册')
set_run_font(r, size=11)
doc.add_paragraph()
tip = doc.add_paragraph(); tip.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = tip.add_run('让AI当"共创伙伴"，把课堂从"做对题"变成"产出作品"'); set_run_font(r, size=12, bold=True, color=C_ORANGE)
doc.add_page_break()

# ===== 一、什么是"生成性质"活动 =====
H(doc, '一、什么是"生成性质"活动', 1)
P(doc, '在AI英语课堂里，按学生与AI的互动方式，教学任务可分为三类。本模块聚焦其中的"生成性质"。', indent=False)
make_table(doc, ['性质', '学生做什么', 'AI扮演什么', '典型任务'],
    [['输入性质', '接收、理解、记忆', '资料库 / 讲解员', '听力理解、词汇输入、课文精讲'],
     ['评测性质', '答题、被检测', '阅卷官 / 纠错题', '随堂测、分层练、错题归因'],
     ['生成性质', '与AI共创、产出作品', '共创伙伴 / 陪练', '协同写作、故事续写、角色对话、项目文案']],
    [1.1, 1.6, 1.6, 1.7], header_color='1A5F7A')
P(doc, '为什么"生成"最值得在培训里重点练？', bold=True, indent=False)
BUL(doc, '学生身份改变——从"做题者"变成"创作者"，语言真正被"用起来"，而不是被"考出来"。')
BUL(doc, 'AI定位改变——从"给答案的机器"变成"陪你一起想、一起写、一起改的伙伴"，最贴合英语核心素养的"表达与交流"。')
BUL(doc, '可迁移性最强——一旦学会"和AI一起产出"，写作、口语、项目式学习全都能套用同一套方法。')
P(doc, '本模块对应此前16种融合方法中的"输出训练（口语/写作/角色/创意）"与"思维应用（新闻/接龙/路径）"的生成环节。', indent=True, bold=True, color=C_GREEN)
doc.add_page_break()

# ===== 二、为什么是这两类工具 =====
H(doc, '二、为什么"生成性质"只用这两类工具', 1)
P(doc, '选工具的第一原则：县乡一线教师时间紧、设备杂、培训只有3小时——凡是需要"下载、注册、讲解界面"的工具，都会吃掉宝贵的实操时间。本模块据此只保留两类工具，各司其职。', indent=False)

H(doc, '工具① 飞象老师（国家智慧中小学平台）——互动生成的"权威底座"', 2)
BUL(doc, '权威可信：教育部认定的国家中小学智慧教育平台体系，学校放心、家长放心、进课堂无合规顾虑。')
BUL(doc, '通用性强：全国师生单点登录、免费、零安装，任何学校机房、平板、大屏都能直接用，不受地域和设备差异影响。')
BUL(doc, '适合承载"结构化互动生成"：角色扮演对话、口语创编闯关、单词/句型生成游戏——全班大屏互动、学生上台就能玩。')

H(doc, '工具② 豆包 / DeepSeek 网页版——开放式内容生成的"零门槛入口"', 2)
BUL(doc, '易上手：豆包几乎人人手机已装（国民级APP），DeepSeek 大家都用过、界面极简——基本不用讲"这是什么、怎么注册"。')
BUL(doc, '减少工具讲解流程：打开网页/APP → 粘贴提示词 → 看结果，三步就能用，省下的时间全留给"练产出"。')
BUL(doc, '学生端也能用：手机豆包随手可开，方便布置课前构思、课后润色等生成任务，把课堂延伸出去。')
BUL(doc, '适合承载"开放式内容生成"：协同写作、故事续写、剧本/海报文案、创意扩写、AI 反馈与润色。')

P(doc, '【工具分工一览】', bold=True, indent=False, color=C_RED)
make_table(doc, ['生成任务类型', '首选工具', '理由'],
    [['角色扮演 / 口语闯关 / 词汇游戏', '飞象老师', '国家平台互动模板，大屏全班参与、零安装'],
     ['协同写作 / 故事续写 / 项目文案', '豆包或DeepSeek网页版', '开放式LLM生成，免讲解、学生端可用'],
     ['脚本/海报/短剧（综合产出）', '豆包/DeepSeek生成 + 飞象老师展示', '前者出内容，后者做互动呈现']],
    [2.3, 2.0, 2.7], header_color='2E7D32')
P(doc, '说明：本模块专讲"生成性质"。输入、评测性质（如评讲页、跟读页、分层听测）仍可用此前方案中的其他工具，分工清晰、互不打架。', indent=True, size=9.5, color=C_GRAY)
doc.add_page_break()

# ===== 三、生成性质活动设计（译林版）=====
H(doc, '三、生成性质活动设计（译林版落地）', 1)
P(doc, '下面6个活动，覆盖"写、说、创、编、做"五种生成形态，均绑定牛津译林版单元。每个活动含：目标、工具、教师操作、可直接复制的提示词、预期产出与评价要点。', indent=False, size=9.5)

# 活动1
H(doc, '活动① 协同写作："AI陪我写"（豆包 / DeepSeek）', 3)
P(doc, '【译林定位】', bold=True, indent=False)
BUL(doc, '九上 Unit 3 Teenage problems（写建议信）')
BUL(doc, '八上 Unit 1 Friends（写朋友介绍）/ 八下 Unit 2 Travelling（写旅行博客）')
P(doc, '【目标】', bold=True, indent=False)
P(doc, '掌握段落结构与词块迁移，从"背范文"转向"和AI一起产出、再自己改"。', indent=True)
P(doc, '【教师操作】', bold=True, indent=False)
NUM(doc, '布置主题（如"给焦虑的同龄人写一封建议信"），明确词数、时态、必须包含的3个建议。')
NUM(doc, '学生用豆包/DeepSeek生成初稿（统一提示词见下）。')
NUM(doc, '引导"三改法"：①改结构（有没有开头-正文-结尾）②改词块（把简单词换成单元目标词块）③改语法（时态/单复数）。')
NUM(doc, '同桌互评+教师抽检，把"AI初稿"改成本人作品，杜绝直接抄。')
prompt_box(doc, '给学生的提示词（豆包/DeepSeek直接复制）',
    '我是初中英语学生。请和我一起写一篇"给同龄人建议信"，主题：缓解考试焦虑。\n'
    '要求：① 三段式（开头共情+正文3条建议+结尾鼓励），约80词；\n'
    '② 用上这些词块：be under pressure, had better, It\'s a good idea to..., why not...；\n'
    '③ 先用中文列出提纲，再写英文；写完请指出我可能写错的2个语法点让我自己改。')
P(doc, '【预期产出】', bold=True, indent=False)
P(doc, '每人一篇结构完整、含目标词块的英文建议信；并养成"AI初稿→自改→互评"的习惯。', indent=True)
P(doc, '【评价要点】', bold=True, indent=False)
P(doc, '结构完整度、目标词块使用数、自改痕迹（看得出改过而非照抄）。', indent=True, size=9.5, color=C_GRAY)

# 活动2
H(doc, '活动② 创意故事续写（豆包 / DeepSeek）', 3)
P(doc, '【译林定位】', bold=True, indent=False)
BUL(doc, '九上 Unit 8 Detective stories（侦探故事）')
BUL(doc, '七下 Unit 5 Amazing things（奇事/科幻小短文）')
P(doc, '【目标】', bold=True, indent=False)
P(doc, '训练叙事逻辑与过去时态，把"读故事"升级为"共创故事"。', indent=True)
P(doc, '【教师操作】', bold=True, indent=False)
NUM(doc, '让AI给出"悬念开头"（含3个线索），学生续写结尾，再让AI点评逻辑漏洞。')
NUM(doc, '进阶：分组接龙，每人写一段，AI负责"串场"并保证时态一致。')
prompt_box(doc, '给学生的提示词（豆包/DeepSeek直接复制）',
    '请用英文给我一个侦探故事的"悬念开头"（约60词，过去时），包含3个线索：\n'
    '① 一扇半开的窗 ② 桌上的奇怪脚印 ③ 消失的戒指。\n'
    '只写开头，留白给我续写结尾。写完我的结尾后，请帮我检查：时态是否一致、线索是否都用到。')
P(doc, '【预期产出】', bold=True, indent=False)
P(doc, '一段连贯的英文叙事 + 一份"逻辑自检清单"，叙事能力与过去时运用双提升。', indent=True)
P(doc, '【评价要点】', bold=True, indent=False)
P(doc, '情节连贯性、过去时准确率、三条线索是否全部回收。', indent=True, size=9.5, color=C_GRAY)

# 活动3
H(doc, '活动③ 角色对话创编 + 口语闯关（飞象老师）', 3)
P(doc, '【译林定位】', bold=True, indent=False)
BUL(doc, '七上 Unit 3 Welcome to our school（校园导游角色扮演）')
BUL(doc, '八上 Unit 3 A day out（出游计划对话）/ 七下 Unit 2 Neighbours（邻里交际）')
P(doc, '【目标】', bold=True, indent=False)
P(doc, '在真实情景中生成并操练功能句型，把"背对话"变成"演对话"。', indent=True)
P(doc, '【教师操作（飞象老师）】', bold=True, indent=False)
NUM(doc, '登录国家智慧中小学平台→进入飞象老师→选择"角色扮演/口语闯关"互动模板。')
NUM(doc, '把模板里的场景与句型替换成本单元内容（如"校园导游"：This is our... / Where is...? / Let me show you...）。')
NUM(doc, '大屏投屏，学生上台抽角色、即时生成并说出对话，AI给发音/表达反馈。')
NUM(doc, '小技巧：先全班跟读模板句型，再上台"生成"新对话，确保后排也跟得上。')
prompt_box(doc, '飞象老师内替换用的场景脚本（示例·七上U3）',
    '角色A=新同学，角色B=校园向导。\n'
    '必须用到句型：Welcome to our school! / Where is the...? / It\'s on the... floor. / Let me show you around.\n'
    '任务：向导带新同学参观图书馆、操场、食堂，每处说一句功能介绍。')
P(doc, '【预期产出】', bold=True, indent=False)
P(doc, '每组一段情景对话视频/录音 + 全班对功能句型的熟练运用。', indent=True)
P(doc, '【评价要点】', bold=True, indent=False)
P(doc, '句型覆盖率、交际得体性、语音流畅度（飞象老师自动评分可佐证）。', indent=True, size=9.5, color=C_GRAY)

# 活动4
H(doc, '活动④ 跨学科项目：双语海报/文案生成（豆包 / DeepSeek）', 3)
P(doc, '【译林定位】', bold=True, indent=False)
BUL(doc, '八下 Unit 1 Past and present（家乡变化）/ 七下 Unit 1 Dream homes（理想之家）')
BUL(doc, '九上 Unit 5 Art world（艺术家/画展介绍）')
P(doc, '【目标】', bold=True, indent=False)
P(doc, '整合信息、做图文表达，把英语变成"做项目"的工具。', indent=True)
P(doc, '【教师操作】', bold=True, indent=False)
NUM(doc, '分组定主题（如"我家乡的十年变化"），先搜集中文素材。')
NUM(doc, '用豆包/DeepSeek把素材转成英文海报文案+版面建议（标题/要点/口号）。')
NUM(doc, '学生排版成实物/电子海报，课堂"英语推介会"展示。')
prompt_box(doc, '给学生的提示词（豆包/DeepSeek直接复制）',
    '我们小组做"家乡十年变化"双语海报。中文素材：\n'
    '① 老房子变高楼 ② 泥路变柏油路 ③ 多了地铁。\n'
    '请生成英文海报文案：一个吸引人的英文标题 + 3条要点（每条约15词）+ 一句英文口号；\n'
    '并建议版面（标题位置/配图建议）。用词难度适合初中生。')
P(doc, '【预期产出】', bold=True, indent=False)
P(doc, '每组一份双语海报 + 一次英文口头推介，信息整合与表达能力同步练。', indent=True)
P(doc, '【评价要点】', bold=True, indent=False)
P(doc, '信息准确性、英文要点完整度、口头推介流利度。', indent=True, size=9.5, color=C_GRAY)

# 活动5
H(doc, '活动⑤ 词汇/句型"生成游戏"（飞象老师）', 3)
P(doc, '【译林定位】', bold=True, indent=False)
BUL(doc, '任意单元的"在用中生成"：单词造句PK、句型接龙、看图说话生成')
P(doc, '【目标】', bold=True, indent=False)
P(doc, '把孤立记词变成"用单词生成句子"的竞赛，词汇在产出中内化。', indent=True)
P(doc, '【教师操作（飞象老师）】', bold=True, indent=False)
NUM(doc, '飞象老师选"单词造句接龙/句型创编"类游戏模板。')
NUM(doc, '导入本单元目标词（英文:中文），设规则：用给定词造一个正确英文句得1分，接不上淘汰。')
NUM(doc, '大屏双人/小组PK，AI判句子正误并即时反馈，气氛拉满。')
prompt_box(doc, '飞象老师内词表与规则（示例·七上U5庆祝话题）',
    '词表：celebrate庆祝 / lantern灯笼 / tradition传统 / reunion团聚\n'
    '规则：每轮抽1词，10秒内用该词造一个完整英文句；造对得分，造错或超时淘汰；\n'
    '可小组接力，最后幸存组获胜。')
P(doc, '【预期产出】', bold=True, indent=False)
P(doc, '全班在游戏中产出大量正确句子，词汇从"认识"到"会用"。', indent=True)
P(doc, '【评价要点】', bold=True, indent=False)
P(doc, '造句正确率、用词准确度（飞象老师计分可量化）。', indent=True, size=9.5, color=C_GRAY)

# 活动6
H(doc, '活动⑥ 短剧脚本生成（豆包/DeepSeek + 飞象老师展示）', 3)
P(doc, '【译林定位】', bold=True, indent=False)
BUL(doc, '八下 Unit 4 A good read（书评/读书短剧）/ 七上 Unit 8 Fashion（服装秀解说）')
P(doc, '【目标】', bold=True, indent=False)
P(doc, '综合运用听说读写，小组产出可表演的英文短剧脚本。', indent=True)
P(doc, '【教师操作】', bold=True, indent=False)
NUM(doc, '豆包/DeepSeek生成短剧脚本框架（角色、场景、台词模板），学生填词改编。')
NUM(doc, '小组排练，用飞象老师"口语/展示"模板做课堂演出与评分。')
prompt_box(doc, '给学生的提示词（豆包/DeepSeek直接复制）',
    '请帮我们写一个简单的英文短剧脚本框架，主题："The best book I read"。\n'
    '角色：主持人+2位同学。场景：班级读书分享会。\n'
    '请给每人的台词留出{ }让我填自己的话，全剧约10句英文，用词适合初中生。')
P(doc, '【预期产出】', bold=True, indent=False)
P(doc, '每组一份可演出的英文短剧 + 一次课堂演出，综合语用能力集中体现。', indent=True)
P(doc, '【评价要点】', bold=True, indent=False)
P(doc, '脚本完整度、台词语言质量、团队协作与舞台表现。', indent=True, size=9.5, color=C_GRAY)
doc.add_page_break()

# ===== 四、教师零门槛操作流 =====
H(doc, '四、教师"零门槛"操作流', 1)

H(doc, '豆包 / DeepSeek 网页版（三步法）', 2)
NUM(doc, '打开：电脑开 deepseek.com 或手机开豆包APP（都已熟悉，不用讲）。')
NUM(doc, '粘贴：把附录提示词复制进去，把花括号里的单元/主题换成自己的。')
NUM(doc, '迭代：看结果，用大白话改——"太难了，降到初中水平""再加2个例子"，AI能懂。')

H(doc, '飞象老师（两步法）', 2)
NUM(doc, '进入：国家智慧中小学平台 → "用AI" / 飞象老师 → 选互动模板（角色扮演、口语闯关、单词游戏等）。')
NUM(doc, '替换+投屏：把模板里的场景、词表换成译林版本单元内容 → 大屏投屏，学生直接玩。')

P(doc, '【通用提示词公式（生成类）】', bold=True, indent=False, color=C_MAIN)
P(doc, '角色 + 任务 + 格式 + 约束（+示例）。例："你是初中英语写作陪练（角色），和我一起写建议信（任务），先列中文提纲再写英文、约80词（格式），用上3个目标词块、适合九年级（约束）。"记住这个公式，换单元只换内容、不换结构。', indent=True)
doc.add_page_break()

# ===== 五、嵌入3小时培训 =====
H(doc, '五、如何嵌入3小时培训时间轴', 1)
P(doc, '本模块建议放在培训"实操产出"段，与输入/评测性质穿插。参考排布：', indent=False)
make_table(doc, ['时段(约)', '内容', '生成性质落点'],
    [['第1小时', '概念+工具认知', '讲清"生成性质"定义与两类工具分工（飞象老师/豆包DeepSeek），省去工具讲解'],
     ['第1.5小时', '实操①写', '活动①②：现场用豆包/DeepSeek做协同写作+故事续写，学员跟做'],
     ['第2小时', '实操②说', '活动③⑤：现场用飞象老师做角色对话+词汇生成游戏，大屏互动'],
     ['第2.5小时', '实操③创编', '活动④⑥：项目海报/短剧脚本，小组产出作品'],
     ['第3小时', '展示+评价', '小组作品英语推介会，用评价要点打分；收尾强调"AI初稿≠本人作品"']],
    [1.2, 2.0, 3.3], header_color='1A5F7A')
P(doc, '一条主线：让每位老师带着"三样产出"离开——①一篇亲手改写的AI协同作文；②一个飞象老师互动游戏（已替换好译林词表）；③一份可复制的提示词卡。', indent=True, bold=True, color=C_RED)
doc.add_page_break()

# ===== 附录 提示词速查卡 =====
H(doc, '附录：生成性质提示词速查卡（复制即用）', 1)
P(doc, '直接粘到豆包 / DeepSeek 网页版或飞象老师，替换花括号内容即可。建议打印成单页贴在办公桌。', indent=False, size=9.5)

cards = [
    ('① 协同写作·建议信', '我是初中生。一起写"给同龄人建议信"，主题{缓解考试焦虑}：三段式约80词；用上词块{be under pressure, had better, why not}；先列中文提纲再写英文，最后指出我可能写错的2个语法点让我自己改。'),
    ('② 创意续写·侦探故事', '用英文给我侦探故事"悬念开头"约60词(过去时)，含3线索{半开的窗/奇怪脚印/消失的戒指}，只写开头留白给我续写；写完帮我检查时态一致与线索是否都用上。'),
    ('③ 角色对话·校园导游(飞象)', '角色A新同学/B向导，必用句型{Welcome to our school!/Where is...?/It\'s on the... floor./Let me show you around}，向导带参观{图书馆/操场/食堂}各说一句介绍。'),
    ('④ 项目文案·家乡变化', '小组做"{家乡十年变化}"双语海报，中文素材{老房变高楼/泥路变柏油/通地铁}；生成英文标题+3条要点(每条约15词)+一句口号，并建议版面；用词适合初中生。'),
    ('⑤ 词汇生成游戏(飞象)', '词表{celebrate庆祝/lantern灯笼/tradition传统/reunion团聚}；规则：每轮抽1词10秒内造完整英文句，对则得分错则淘汰，小组接力，幸存组胜。'),
    ('⑥ 短剧脚本·读书分享', '写英文短剧框架主题{The best book I read}，角色{主持人+2同学}场景{班级读书会}，每人的台词留{ }让我填，全剧约10句，适合初中生。'),
    ('⑦ 旅行博客(八下U2)', '以"{Last summer in Beijing}"为题写英文旅行博客约100词，含3个地点与1个感受，用过去时，附3张配图建议。'),
    ('⑧ 通用生成公式', '角色+任务+格式+约束。例：你是初中英语写作陪练，和我一起写{单元主题}，先列提纲再写英文约{80}词，用上{目标词块}，适合{年级}水平。'),
]
for title, content in cards:
    prompt_box(doc, title, content)

doc.add_paragraph()
P(doc, '设计说明：本模块专攻"生成性质"活动，工具刻意收敛为飞象老师（国家智慧中小学平台，权威通用）与豆包/DeepSeek网页版（易上手、免工具讲解），以最大化3小时培训的实操产出比。输入与评测性质活动可沿用其他工具方案，分工互补。', indent=True, size=9, color=C_GRAY)

out = 'D:/projects/WorkBuddy/2026-06-17-11-18-20/AI赋能英语教学_生成性质活动设计.docx'
doc.save(out)
print('SAVED:', out)
