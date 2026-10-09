# -*- coding: utf-8 -*-
# AI赋能英语教学_3小时培训课程设计 v2（课标锚定·真实译林版）
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
C_LIGHT = RGBColor(0xee, 0xf6, 0xf8)

def set_run_font(run, font_name='微软雅黑', size=10.5, bold=False, color=None, italic=False):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.italic = italic
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
    run = p.add_run('"' + text + '"')
    set_run_font(run, size=9.5, color=C_GRAY, italic=True)
    return p

def prompt_box(doc, title, content):
    P(doc, '【' + title + '】', bold=True, indent=False, color=C_MAIN)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.left_indent = Cm(0.74)
    run = p.add_run(content)
    set_run_font(run, size=9, color=C_GRAY)
    return p

def make_table(doc, headers, rows, widths, header_color='1A5F7A', font_size=8.5, alt_row=True):
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
                for r in para.runs:
                    set_run_font(r, size=font_size)
            if alt_row and ri % 2 == 0:
                fill(c, 'F2F8FA')
    # column widths
    for col, w in zip(t.columns, widths):
        col.width = Cm(w)
    return t

def card(doc, title, body_lines, color=C_MAIN):
    """简易信息卡：标题+若干行（标题加粗蓝色）"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.74)
    p.paragraph_format.space_before = Pt(4)
    r = p.add_run('▍ ' + title)
    set_run_font(r, size=11, bold=True, color=color)
    for line in body_lines:
        P(doc, line, size=10)

# =========================================================
doc = Document()
# 默认页边距
for sec in doc.sections:
    sec.top_margin = Cm(2)
    sec.bottom_margin = Cm(2)
    sec.left_margin = Cm(2.2)
    sec.right_margin = Cm(2.2)

# ============== 封面 ==============
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run('AI赋能英语教学')
set_run_font(r, size=26, bold=True, color=C_MAIN)
subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.paragraph_format.space_before = Pt(6)
r = subtitle.add_run('—— 3小时一线教师培训课程设计 · 课标锚定版')
set_run_font(r, size=14, bold=True, color=C_GREEN)
meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta.paragraph_format.space_before = Pt(12)
r = meta.add_run('面向县乡初中英语教师 · 译林版（五四学制7-9年级）· 飞象老师+豆包/DeepSeek')
set_run_font(r, size=11, color=C_GRAY)
P(doc, '', indent=False)
P(doc, '【课程设计依据】', bold=True, color=C_MAIN, indent=False)
P(doc, '· 《义务教育英语课程标准（2022年版）》—— 核心素养四要素、课程内容六要素、主题语境三范畴')
P(doc, '· 译林版英语教材（七上/七下/八上/八下/九上，2024-2026新版）真实单元主题')
P(doc, '· 禅城区初中英语 7 校《AI赋能英语教学实践探索》(一)~(七) 一线案例与痛点')
P(doc, '· 16种AI赋能英语课堂融合方法（输入·过程·输出·评测四维）')
doc.add_page_break()

# ============== 第一章 总览 ==============
H(doc, '第一章 课程总览（顶层锚定）', level=1)
H(doc, '1.1 课程定位', level=2)
P(doc, '本培训面向县乡一线初中英语教师，3 小时工作坊形态。聚焦"教师用 AI 解决真教学问题"，全程围绕译林版（2024-2026 新版）七年级至九年级上册的真实单元任务，以课标核心素养与主题语境为顶层锚点，确保 16 种 AI 融合方法"有用、能用、立得住"。')
P(doc, '工具收敛：国家智慧中小学平台"用AI"系列（飞象老师、智能学伴、VR/微课等，权威通用） + 豆包/DeepSeek 网页版（生成性任务，人人手机已装/熟，免讲解）。', bold=True, color=C_ORANGE)

H(doc, '1.2 课程标准顶层锚点（2022 版义教课标）', level=2)
P(doc, '【核心素养四要素】—— 决定"教到什么程度"')
BUL(doc, '语言能力：基础要素。指学生在特定情境下参与主题语言活动时表现出的语言理解和表达能力。')
BUL(doc, '文化意识：价值取向。指对中外文化的理解和优秀文化的鉴赏，跨文化认知、态度与行为选择。')
BUL(doc, '思维品质：心智特征。指思维个性特征，反映学生在理解、分析、比较、推断、批判、评价、创造等方面的层次和水平。')
BUL(doc, '学习能力：关键要素。指积极运用和主动调适英语学习策略、拓展学习渠道、提升学习效率的意识和能力。')
P(doc, '【课程内容六要素】—— 决定"教什么"：主题、语篇、语言知识、文化知识、语言技能、学习策略。（六要素相互关联、融合互动，AI 全部可加持。）')
P(doc, '【主题语境三大范畴】—— 决定"主题往哪走"：')
BUL(doc, '人与自我：以"我"为视角，设置"生活与学习""做人与做事"等主题群')
BUL(doc, '人与社会：以"社会"为视角，设置"社会服务与人际沟通""文学、艺术与体育""历史、社会与文化""科学与技术"等主题群')
BUL(doc, '人与自然：以"自然"为视角，设置"自然生态""环境保护""灾害防范""宇宙探索"等主题群')
P(doc, '【学段目标】7~9 年级为三级，对应义教英语课程的最高学段。本培训全部示例均锚定三级要求。', color=C_ORANGE)

H(doc, '1.3 五条课程设计原则', level=2)
BUL(doc, '【锚定课标】每一法、每一活动，都能在"核心素养×课程内容×主题语境"三角中找到落点，避免技术与教学脱节。')
BUL(doc, '【真实教材】所有示例来自译林版（2024-2026 新版）7-9 年级真实单元（含模块/主题/子主题/语法项目），教师可直接对照自己下周要上的课。')
BUL(doc, '【痛点驱动】从禅城区 7 校一线实践提炼 6 大真实痛点，每痛点对应一套可复用解法。')
BUL(doc, '【零门槛工具】少讲工具多练产出：飞象老师（国家平台，权威通用） + 豆包/DeepSeek（生成/开放问答，免讲解）。')
BUL(doc, '【学带三样】每位学员带走：①亲手做的 AI 互动工具/游戏 ②经 AI 协同并自改的教学成品 ③译林版提示词速查卡。')

H(doc, '1.4 16 种融合方法 × 课标三维度 × 真实单元', level=2)
P(doc, '16 法按"输入·过程·输出·评测"四维组织（详见第二章总表）。每条方法都标注：①所属课标主题范畴 ②对应核心素养 ③真实译林版单元示例。')

H(doc, '1.5 工具分工', level=2)
make_table(doc,
    ['工具', '主要用途', '为什么用', '替代/兜底'],
    [
        ['飞象老师（国家智慧中小学平台）', '互动游戏/角色扮演/词汇闯关/大屏活动', '教育部官方平台，权威、通用、零安装', '豆包生成互动文本+PPT演示'],
        ['豆包/DeepSeek 网页版', '协同写作/故事续写/项目文案/开放生成', '人手已装/熟，三步即用', '腾讯元宝/Kimi 等同类'],
        ['国家平台"用AI"其他应用', '智能学伴答疑/VR 情景/微课资源/口语评测', '单点登录、权威内容', '教研网/学科网资源'],
    ],
    widths=[5.2, 5.5, 3.5, 2.5])

doc.add_page_break()

# ============== 第二章 16法总表 ==============
H(doc, '第二章 16 种 AI 融合方法总表（课标+真实单元）', level=1)
P(doc, '下表是本培训的"工具索引"。每条方法给出：①分类（四维） ②课标主题范畴 ③核心素养指向 ④译林版真实单元示例 ⑤首选工具。', color=C_GRAY)

methods = [
    # (编号, 名称, 维度, 主题范畴, 核心素养, 译林单元示例, 工具)
    ('①', 'AI 词汇跟读互动页', '输入', '人与自我·生活与学习', '语言能力/学习能力', '七上U2 Hobbies / 八上U1 Friendship', '飞象老师/国家平台'),
    ('②', 'AI 听力分层跟测', '输入', '人与社会·社会服务', '语言能力/学习能力', '八下U1 Past and present / 八上U5 Wild animals', '国家平台/豆包'),
    ('③', 'AI 语篇结构可视化', '过程', '人与自我·做人与做事', '思维品质/语言能力', '九上U1 Know yourself（写推荐信）/ 八下U4 A good read', '飞象老师/豆包'),
    ('④', 'AI 语法规则发现卡', '过程', '人与自我·生活与学习', '思维品质/语言能力', '八上U1 Friendship（比较级）/ 九上U1（宾语从句）', '豆包/DeepSeek'),
    ('⑤', 'AI 写作协同+自改', '输出', '人与自我·做人与做事', '语言能力/思维品质', '九上U1（推荐信）/ 八上U2 School life（介绍）/ 八下U3 在线旅游攻略', '豆包/DeepSeek'),
    ('⑥', 'AI 角色对话生成', '输出', '人与社会·人际沟通', '语言能力/文化意识', '七下U2 Neighbourhoods（邻里）/ 八上U1 Friendship（朋友）', '飞象老师'),
    ('⑦', 'AI 词汇游戏化闯关', '过程', '人与自我·生活与学习', '学习能力/语言能力', '七上U7 Be wise with money / 七上U6 My clothes', '飞象老师（水果忍者/记忆翻牌）'),
    ('⑧', 'AI 完形/阅读评讲页', '评测', '人与自我·生活与学习', '语言能力/思维品质', '七下U8 Wonderland（Down the rabbit hole）/ 八上U1 Friendship', '飞象老师/国家平台'),
    ('⑨', 'AI 故事续写与海报', '输出', '人与社会·历史社会与文化', '思维品质/文化意识', '七下U4 Chinese folk art（剪纸）/ 八下U1 Past and present（家乡变化海报）', '豆包/DeepSeek+飞象'),
    ('⑩', 'AI 跨学科项目策划', '输出', '人与社会·科学与技术', '思维品质/学习能力', '八下U1 Project 1（A travel guide to a country）/ 七下U8 Project 2（school newspaper about nature）', '豆包+飞象展示'),
    ('⑪', 'AI 口语情景微剧', '输出', '人与社会·文学艺术与体育', '语言能力/文化意识', '八上U1 Friendship（友谊情景剧）/ 九上U8 Detective stories（短剧）', '飞象老师+豆包脚本'),
    ('⑫', 'AI 阅读策略脚手架', '过程', '人与自我·做人与做事', '学习能力/思维品质', '八下U1（The rise of Shenzhen 略读精读分层）/ 八上U5（Protecting pandas 论证）', '国家平台/豆包'),
    ('⑬', 'AI 错题归因与分层练', '评测', '人与自我·生活与学习', '学习能力/语言能力', '八上U3 To be a good learner / 八下U2 Amazing China', '国家平台/豆包'),
    ('⑭', 'AI 文化对比微项目', '输出', '人与社会·历史社会与文化', '文化意识/思维品质', '七下U1 Home（不同国家住宅）/ 八上U2 School life（Unusual schools）/ 八下U3（Around the world）', '豆包+飞象'),
    ('⑮', 'AI 环保议题辩论', '输出', '人与自然·环境保护', '思维品质/文化意识', '八下U8 A green world（Going green）/ 八上U5 Wild animals（保护大熊猫）', '飞象老师辩论+豆包论据'),
    ('⑯', 'AI 单元复习闯关地图', '评测', '人与自我·生活与学习', '学习能力/语言能力', '任一单元（自适应复习，如八下U5-8 A better world 串复习）', '飞象老师/国家平台'),
]

make_table(doc,
    ['编号', '方法', '维度', '课标主题范畴', '核心素养', '译林版真实单元示例', '工具'],
    methods,
    widths=[1.0, 4.2, 1.2, 4.0, 3.2, 4.8, 2.6], font_size=8.5)

doc.add_page_break()

# ============== 第三章 模块设计 M0-M6 ==============
H(doc, '第三章 7 个培训模块（3 小时时间轴）', level=1)
P(doc, 'M0 痛点破冰 → M1 工具熟悉 → M2 写作协同（输出） → M3 阅读与语法（过程） → M4 词汇与口语（输出） → M5 评讲与分层（评测） → M6 自带三样。每一模块都标"主题范畴+核心素养+真实单元"三锚。', color=C_GRAY)

# ---- M0 ----
H(doc, 'M0 痛点破冰（15 分钟）', level=2)
P(doc, '【课标锚点】主题范畴：人与自我·做人与做事｜核心素养：思维品质（批判）/学习能力（反思）｜真实单元：八上U3 To be a good learner（"如何成为更好的语言学习者"主题）', color=C_ORANGE)
BUL(doc, '导入：6 张一线原声卡片（来源 7 校案例），教师两两讨论"我也有同感"哪一条。')
BUL(doc, '共识：6 大痛点 → 讲评课被动走神、词汇听默单调、早读不敢开口、写作结构记不住、语法备课翻倍、听力检测难兼顾趣味与实效。')
BUL(doc, '本模块产出：每位学员写下"我最想 AI 帮我解决的 1 个痛点"，贴到墙上。')

# ---- M1 ----
H(doc, 'M1 工具熟悉与提示词基础（20 分钟）', level=2)
P(doc, '【课标锚点】课程内容六要素：主题/语篇/语言知识/文化知识/语言技能/学习策略｜核心素养：学习能力｜真实单元：七上U1 This is me!（自我介绍主题）', color=C_ORANGE)
BUL(doc, '飞象老师两步：①国家平台账号登录 ②选"用AI"→"飞象老师"→选模板→生成互动页。')
BUL(doc, '豆包/DeepSeek 三步：①打开网页 ②粘提示词 ③复制结果。')
BUL(doc, '提示词公式（角色+任务+格式+约束），用七上U1 This is me! 自我介绍任务演练。')
prompt_box(doc, '豆包/DeepSeek 提示词（七上U1 This is me!）',
'''你是一名有 10 年教龄的初中英语教师。请为七年级学生设计一份"My Self-introduction"写作清单，要求：①包含姓名/年龄/学校/爱好/梦想 5 项 ②每项给出 2-3 句英文示例 ③给出 1 段 60 词左右的范例。请用中文讲清每一句为什么这样写，便于学生模仿。''')

# ---- M2 ----
H(doc, 'M2 写作协同 + 推荐信实战（30 分钟）', level=2)
P(doc, '【课标锚点】主题范畴：人与自我·做人与做事｜核心素养：语言能力/思维品质/文化意识｜真实单元：九上U1 Know yourself（"为班里职位写一封推荐信"任务，对应方法⑤）', color=C_ORANGE)
BUL(doc, '步骤：①拆解九上U1 D2 范信的结构（开头-主体-结尾-礼貌语） ②豆包生成"推荐班长/学习委员"两版底稿 ③教师用红笔自改 ④飞象老师/PPT 展示对照原版。')
prompt_box(doc, '豆包/DeepSeek 提示词（九上U1 推荐信）',
'''你是一名初中英语教师。请根据九上U1 D2 范文（写给 Mr Wu 推荐 David 当学生会主席），生成一份【学习委员】推荐信。要求：①80-100 词 ②结构完整（开头介绍目的、被推荐人 2-3 个品质、总结、礼貌署名）③语言适合九年级，能直接给学生做范例；④标出 3 个可替换点，便于课堂改编。''')
P(doc, '【延展·生成性质活动】七下U3 My hometown 或 八下U1 Past and present 主题：让豆包生成"我的家乡/家乡变化"双语文案（1 段中文+1 段英文），用于项目布展。', color=C_GREEN)

# ---- M3 ----
H(doc, 'M3 阅读与语法：语篇结构可视化 + 规则发现卡（35 分钟）', level=2)
P(doc, '【课标锚点】课程内容要素：语篇/语言知识｜核心素养：思维品质（分析/推断）/语言能力｜真实单元：九上U1 范信语篇、八上U1 Friendship（比较级语法）、八下U4 A good read', color=C_ORANGE)
BUL(doc, '语篇结构可视化：飞象老师生成"九上U1 D2 推荐信"的结构图，标注开头/主体/结尾，让学生看到"英文推荐信长这样"。')
BUL(doc, '语法规则发现卡：豆包提示词，把八上U1 比较级规则做成"前后对比+口诀"。')
prompt_box(doc, '豆包/DeepSeek 提示词（八上U1 比较级规则发现）',
'''你是一名初中英语教师。把八上U1 Friendship 的比较级与最高级规则，做成一张 A4 "规则发现卡"：左侧列 5 条规则（用"原级→比较级→最高级"举例 nice/nicer/nices），右侧列 3 条易错点（双写/变y/不规则）。要求用初中生能懂的中文+英文示例，最后给一句口诀（如"一停二去三改四记"）。''')
BUL(doc, '真实任务：每位学员用八下U4 Gulliver in Lilliput 短文，5 分钟内让豆包生成"5 句话故事结构卡"。')

# ---- M4 ----
H(doc, 'M4 词汇与口语：游戏化闯关 + 角色对话（35 分钟）', level=2)
P(doc, '【课标锚点】课程内容要素：语言技能/主题｜核心素养：语言能力/学习能力/文化意识｜真实单元：七上U2 Hobbies、七上U7 Be wise with money、七下U2 Neighbourhoods、八上U1 Friendship', color=C_ORANGE)
BUL(doc, '飞象老师游戏化：把七上U2 Hobbies 词汇表做成"记忆翻牌"游戏；把七上U7 Be wise with money 词汇做成"水果忍者"（一线案例同款）。')
BUL(doc, '角色对话生成：飞象老师/豆包生成"和邻居借东西/和新朋友聊天"对话脚本，七下U2 Neighbourhoods 主题。')
prompt_box(doc, '豆包/DeepSeek 提示词（七下U2 角色对话）',
'''你是一名初中英语教师。请为七下U2 Neighbourhoods 单元生成一段"借工具"的角色对话脚本：Mike 想借邻居 Mrs Wang 的 ladder，30 句以内，含礼貌表达（Could I ...?/Sure./Sorry, I'm using it ...）。生成英文+中文对照，并标出可替换的关键词，便于学生改写为"借书/借自行车"。''')
P(doc, '【真实产出】学员现场在飞象老师里建一个 5 题闯关游戏，发班级群用。', color=C_GREEN)

# ---- M5 ----
H(doc, 'M5 评讲与分层：完形评讲页 + 错题归因（30 分钟）', level=2)
P(doc, '【课标锚点】课程内容要素：语言技能/学习策略｜核心素养：语言能力/学习能力/思维品质｜真实单元：八上U1 Friendship 完形、七下U8 Wonderland、七下U4 Chinese folk art', color=C_ORANGE)
BUL(doc, '完形评讲页：飞象老师把八上U1 Reading 完形 5 道错题做成"点选+解析"互动页，一线案例同款。')
BUL(doc, '错题归因：豆包出 3 道题分层（A 基础/B 进阶/C 挑战），做错题归因标签（词汇/语法/逻辑）。')
prompt_box(doc, '豆包/DeepSeek 提示词（八上U1 完形评讲）',
'''你是一名初中英语教师。八上U1 Friendship Reading 完形，学生最容易错 5 题（关于友谊/性格/比较级）。请生成"错题评讲页"内容：①每题 1 段解析（中英双语） ②标出错因（生词/搭配/逻辑）③给 1 道同类型变式练习。请用 markdown 表格输出，便于导入飞象老师。''')

# ---- M6 ----
H(doc, 'M6 带走三样（15 分钟）', level=2)
P(doc, '【课标锚点】核心素养：学习能力（自我管理/反思）/ 主题范畴：人与自我·做人与做事｜真实单元：自选下周要上的课', color=C_ORANGE)
BUL(doc, '产出 1：亲手做的 AI 互动工具/游戏（飞象老师闯关/角色对话/评讲页任一）。')
BUL(doc, '产出 2：经 AI 协同并自改的教学成品（推荐信/词汇卡/海报/脚本任一）。')
BUL(doc, '产出 3：译林版提示词速查卡（附录 A 自取，圈出自用 3 张）。')
BUL(doc, '15 分钟配对互评：每人展示 30 秒，同伴打分+提 1 条改进建议，贴墙上带回去。')

doc.add_page_break()

# ============== 第四章 16法详解 ==============
H(doc, '第四章 16 种融合方法详解（备课字典）', level=1)
P(doc, '每条方法给出：① 课标三锚 ② 教师操作 ③ 译林版提示词 ④ 风险与底线。教师可按"下周要上的单元"直接查表复用。', color=C_GRAY)

H(doc, '方法① AI 词汇跟读互动页（输入）', level=3)
P(doc, '【主题范畴】人与自我·生活与学习｜【核心素养】语言能力/学习能力｜【真实单元】七上U2 Hobbies（"What do you like to do?" 主题）')
prompt_box(doc, '国家平台/飞象老师 提示词',
'''在国家智慧中小学平台"用AI"→ 飞象老师选"跟读模板"。导入七上U2 Hobbies 单元词汇表（paint/draw/play football/read books 等），生成：①英文发音 ②中文释义 ③例句跟读 ④自评打分。设班级 40 人，1 个游戏大屏可投。''')
P(doc, '【底线】禁止把"跟读打分"作为唯一评价；与教师课堂提问结合，避免学生只跟 AI 练。')

H(doc, '方法② AI 听力分层跟测（输入）', level=3)
P(doc, '【主题范畴】人与社会·社会服务与人际沟通｜【核心素养】语言能力/学习能力｜【真实单元】八上U5 Wild animals（Protecting pandas 听力）')
prompt_box(doc, '国家平台/豆包 提示词',
'''在国家平台"用AI"→ 智能学伴选"听力分层"。导入八上U5 Reading 听力原文（保护大熊猫），生成 3 套题：A 基础（5 题/原速）/B 进阶（5 题+复述）/C 挑战（听后写 3 句观点）。每题 1 解析。''')

H(doc, '方法③ AI 语篇结构可视化（过程）', level=3)
P(doc, '【主题范畴】人与自我·做人与做事｜【核心素养】思维品质/语言能力｜【真实单元】九上U1 D2 推荐信（推荐 David 当学生会主席）')
prompt_box(doc, '飞象老师/豆包 提示词',
'''把九上U1 D2 推荐信用飞象老师做"结构卡片墙"：开头（介绍推荐人/目的）→ 主体（3 个品质 + 1 个例子）→ 结尾（总结+礼貌语）。每段标中文功能（破题/佐证/收束）。学生可点开看范例句。''')

H(doc, '方法④ AI 语法规则发现卡（过程）', level=3)
P(doc, '【主题范畴】人与自我·生活与学习｜【核心素养】思维品质/语言能力｜【真实单元】八上U1 Friendship（比较级/最高级）；九上U1（宾语从句）')
prompt_box(doc, '豆包/DeepSeek 提示词',
'''把"比较级"的 5 条规则做成 A4 卡片，左规则+右例句+右下角口诀。初中生 30 秒能看懂。''')

H(doc, '方法⑤ AI 写作协同+自改（输出）', level=3)
P(doc, '【主题范畴】人与自我·做人与做事｜【核心素养】语言能力/思维品质/文化意识｜【真实单元】九上U1 推荐信（任务重点）；八上U2 School life（介绍学校）；八下U3 The world at one click（旅游攻略）')
prompt_box(doc, '豆包/DeepSeek 提示词（九上U1 推荐信）',
'''生成 80-100 词的"学习委员"推荐信底稿：开头-主体 2-3 品质-结尾。标 3 个可替换点，便于学生改写。''')
P(doc, '【底线】AI 出稿→教师/学生必须自改；写完后要回到九上U1 范信对照，避免风格漂移。')

H(doc, '方法⑥ AI 角色对话生成（输出）', level=3)
P(doc, '【主题范畴】人与社会·人际沟通｜【核心素养】语言能力/文化意识｜【真实单元】七下U2 Neighbourhoods（邻里互动）；八上U1 Friendship（朋友间）')
prompt_box(doc, '飞象老师/豆包 提示词',
'''生成"借工具"角色对话脚本（Mike 借 Mrs Wang 的 ladder），30 句内+礼貌表达+英文中文对照+可替换关键词。''')

H(doc, '方法⑦ AI 词汇游戏化闯关（过程）', level=3)
P(doc, '【主题范畴】人与自我·生活与学习｜【核心素养】学习能力/语言能力｜【真实单元】七上U2 Hobbies；七上U6 My clothes, my style；七上U7 Be wise with money')
prompt_box(doc, '飞象老师 提示词',
'''在飞象老师选"记忆翻牌/水果忍者"模板，导入七上U7 词汇（allow/save/spend/wallet/pocket money 等），生成 5 关游戏，最后一关加"小测试"。''')
P(doc, '【一线案例】澜石中学罗浩、佛外学校罗彩甜均使用飞象老师游戏化，单词默写合格率显著提升。')

H(doc, '方法⑧ AI 完形/阅读评讲页（评测）', level=3)
P(doc, '【主题范畴】人与自我·生活与学习｜【核心素养】语言能力/思维品质｜【真实单元】七下U8 Wonderland（Down the rabbit hole）；八上U1 Friendship 完形；八下U1 The rise of Shenzhen')
prompt_box(doc, '飞象老师/国家平台 提示词',
'''选"评讲模板"，把八上U1 完形 5 道易错题做成"点选+解析"互动页，每题 1 段中英双语解析+同类型变式 1 道。''')

H(doc, '方法⑨ AI 故事续写与海报（输出）', level=3)
P(doc, '【主题范畴】人与社会·历史社会与文化｜【核心素养】思维品质/文化意识｜【真实单元】七下U4 Chinese folk art（剪纸故事）；八下U1 Past and present（家乡变化）')
prompt_box(doc, '豆包/DeepSeek 提示词（八下U1 家乡变化）',
'''生成双语海报文案（中文标题"我的家乡 20 年"+英文 3 句话介绍），突出 1 个变化（交通/建筑/教育），便于学生改写。''')

H(doc, '方法⑩ AI 跨学科项目策划（输出）', level=3)
P(doc, '【主题范畴】人与社会·科学与技术｜【核心素养】思维品质/学习能力｜【真实单元】八下U1 Project 1（A travel guide to a country）；七下U8 Project 2（school newspaper about nature）')
prompt_box(doc, '豆包/DeepSeek 提示词（八下U1 Project 1）',
'''为八下U1 Project 1（A travel guide to a country）生成项目脚手架：①选国家 ②找 3 段语料（Welcome/Wild/History 各 1 段） ③做 A4 双面宣传册文字稿。给初中生 1 节课能完成。''')

H(doc, '方法⑪ AI 口语情景微剧（输出）', level=3)
P(doc, '【主题范畴】人与社会·文学艺术与体育｜【核心素养】语言能力/文化意识｜【真实单元】八上U1 Friendship（友谊微剧）；九上U8 Detective stories（侦探短剧）')
prompt_box(doc, '飞象老师+豆包 提示词',
'''豆包生成"友谊冲突-和解"3 分钟英文短剧脚本（5 角色），飞象老师选"配音+分镜"模板，让学生分组录音配字幕。''')

H(doc, '方法⑫ AI 阅读策略脚手架（过程）', level=3)
P(doc, '【主题范畴】人与自我·做人与做事｜【核心素养】学习能力/思维品质｜【真实单元】八下U1 The rise of Shenzhen（略读-精读-批判三层）；八上U5 Protecting pandas（论证结构）')
prompt_box(doc, '国家平台/豆包 提示词',
'''把"略读找主旨/精读找细节/批判找立场"三步做成八下U1 阅读脚手架：每步 1 张卡+2 个"学生常见错法"+1 句"教师反馈话术"。''')

H(doc, '方法⑬ AI 错题归因与分层练（评测）', level=3)
P(doc, '【主题范畴】人与自我·生活与学习｜【核心素养】学习能力/语言能力｜【真实单元】八上U3 To be a good learner（学习策略主题）；八下U2 Amazing China（高频词与语法）')
prompt_box(doc, '国家平台/豆包 提示词',
'''针对八下U2 单元错题，生成 3 道分层题（A 词汇/B 句型/C 段落），每题配 1 个"错因标签"（生词/搭配/逻辑/时态）。''')

H(doc, '方法⑭ AI 文化对比微项目（输出）', level=3)
P(doc, '【主题范畴】人与社会·历史社会与文化｜【核心素养】文化意识/思维品质｜【真实单元】七下U1 Home（不同国家住宅对比）；八上U2 School life（Unusual schools around the world）；八下U3 Around the world')
prompt_box(doc, '豆包+飞象 提示词',
'''生成"中国 vs 英国学生一天"双语对比清单（上学时间/科目/午餐/作业/通勤 5 维度），飞象老师做成投票互动页。''')

H(doc, '方法⑮ AI 环保议题辩论（输出）', level=3)
P(doc, '【主题范畴】人与自然·环境保护｜【核心素养】思维品质/文化意识｜【真实单元】八下U8 A green world（Going green）；八上U5 Wild animals（保护大熊猫）')
prompt_box(doc, '飞象老师+豆包 提示词',
'''豆包生成正反方论据（"是否应禁止使用一次性塑料"），飞象老师选"辩论模板"分正反方 4v4，每方 1 句立场+2 个论据+1 句反驳。''')

H(doc, '方法⑯ AI 单元复习闯关地图（评测）', level=3)
P(doc, '【主题范畴】人与自我·生活与学习｜【核心素养】学习能力/语言能力｜【真实单元】自选（下例：八下U5-8 A better world 串复习）')
prompt_box(doc, '飞象老师/国家平台 提示词',
'''把八下U5-U8 4 个单元的"单元首页"主题词、核心语法、必背词块做成 4 关闯关地图，最后一关做"项目复盘"（8 分钟内讲完 4 单元最大收获）。''')

doc.add_page_break()

# ============== 第五章 生成性质专项 ==============
H(doc, '第五章 生成性质专项（飞象老师 + 豆包/DeepSeek）', level=1)
H(doc, '5.1 什么是"生成性质"', level=2)
P(doc, '与"输入性质"（跟读/听力/阅读）和"评测性质"（完形/纠错/分层练）相对，"生成性质"是让学生用英语产出新内容——写、说、创、编、做。本培训把生成性质的开放生成环节统一收敛到豆包/DeepSeek 网页版，互动呈现统一收敛到飞象老师，最大化实操密度。')

H(doc, '5.2 工具分工再确认', level=2)
make_table(doc,
    ['任务类型', '首选工具', '为什么这样分'],
    [
        ['角色对话/口语闯关/词汇游戏', '飞象老师', '权威、通用、大屏可投、互动即时'],
        ['协同写作/故事续写/项目文案/海报', '豆包/DeepSeek', '人人手机已装/熟，三步即用'],
        ['短剧/海报综合呈现', '豆包出脚本+飞象老师展示', '脚本 AI 出、互动 AI 演'],
    ],
    widths=[6.5, 4.0, 6.2])

H(doc, '5.3 6 个译林版生成性质活动（学员产出）', level=2)
P(doc, '每个活动 6 元素：①目标 ②对应真实单元 ③工具 ④教师操作 ⑤提示词 ⑥预期产出。', color=C_GRAY)

# 活动 1-6
generative_acts = [
    ('活动① 协同写作：写一封推荐信', '九上U1 Know yourself（推荐班长/学习委员）',
     '【教师操作】①拆解九上U1 D2 范信结构 ②学生列出"推荐谁+3 个理由" ③豆包生成底稿 ④学生自改 ⑤对照范信微调 ⑥班级互评 1 句',
     '豆包/DeepSeek 提示词', '你是一名初中英语教师。请根据九上U1 D2 范信结构，生成 80-100 词【学习委员】推荐信，标 3 个可替换点。'),
    ('活动② 故事续写：Down the rabbit hole 续', '七下U8 Wonderland',
     '【教师操作】①全班共读七下U8 Reading ②豆包生成 3 个续写方向（爱丽丝长大/回到现实/新冒险） ③小组选 1 方向写 100 词 ④飞象老师做成"续写展览"',
     '豆包/DeepSeek 提示词', '为七下U8 Wonderland 的 Down the rabbit hole 写 3 个续写开头（各 30 词）：①爱丽丝长大后 ②回到现实世界 ③开启新冒险。用初中词汇。'),
    ('活动③ 角色对话创编：邻里互动', '七下U2 Neighbourhoods',
     '【教师操作】①飞象老师"角色对话"模板 ②豆包生成"借工具/问路/约时间" 3 个场景 ③学生选 1 场景改编 + 替换关键词 ④大屏演练 ⑤其他组评分',
     '飞象老师/豆包 提示词', '为七下U2 Neighbourhoods 生成 3 段角色对话（借工具/问路/约时间），每段 15 句内，含礼貌表达和可替换关键词。'),
    ('活动④ 家乡/校园变化双语海报', '八下U1 Past and present',
     '【教师操作】①豆包生成"家乡 20 年变化"双语文案模板 ②学生选 1 主题（交通/建筑/教育/饮食）填内容 ③飞象老师选"海报模板"成稿 ④班级布展',
     '豆包/DeepSeek 提示词', '为八下U1 Past and present 写双语海报：中文标题"我的家乡 20 年"，英文 3 句介绍+1 张图位说明（学生可换图）。'),
    ('活动⑤ 词汇生成游戏：种小树/记忆翻牌', '七上U2 Hobbies / 七上U7 Be wise with money',
     '【教师操作】①飞象老师选"记忆翻牌/水果忍者" ②导入单元词表 ③设置 5 关 + 1 挑战 ④小组 pk ⑤错词回炉',
     '飞象老师 提示词', '为七上U7 词汇做"水果忍者"游戏：单词落下，砍对加分，砍错扣分，5 关后排行榜。'),
    ('活动⑥ 读书短剧脚本 + 分镜', '八下U4 A good read / 九上U8 Detective stories',
     '【教师操作】①豆包生成 3-5 分钟短剧脚本 5 角色 ②飞象老师"配音+分镜"模板 ③学生录音 ④家长群/班级群展演',
     '豆包/DeepSeek 提示词', '为八下U4 Gulliver in Lilliput 生成 3 分钟短剧脚本（5 角色），含中英对照台词和分镜描述。'),
]

for title_, unit, ops, prompt_t, prompt_c in generative_acts:
    P(doc, '▎' + title_, bold=True, color=C_MAIN, indent=False)
    P(doc, '【真实单元】' + unit, color=C_ORANGE, indent=False)
    P(doc, ops, indent=False, size=10)
    prompt_box(doc, prompt_t, prompt_c)
    P(doc, '', indent=False)

H(doc, '5.4 生成类提示词公式', level=2)
P(doc, '【公式】背景 + 角色 + 任务 + 限制 + 格式。例如："【背景】九上U1 推荐信单元【角色】你是有 10 年教龄的英语教师【任务】生成 80-100 词学习委员推荐信【限制】用初中词汇，标 3 个可替换点【格式】开头-主体-结尾"。')

H(doc, '5.5 5 类常见问题与对策', level=2)
BUL(doc, '【AI 出稿太成人化】→ 在提示词加"用初中词汇/句长不超过 12 词"；出稿后让学生自己改 3 句。')
BUL(doc, '【学生直接抄 AI】→ 用"自改 3 句+对照范信 1 处"硬约束；过程比结果重要。')
BUL(doc, '【跨学科主题跑偏】→ 限定真实单元为唯一语料源，提示词中明示"严格依据七下U4 Chinese folk art Reading"。')
BUL(doc, '【生成内容超纲】→ 提示词加"符合九年级课标三级要求，不出现生僻语法"。')
BUL(doc, '【互动页太大班用不了】→ 飞象老师选"小组模式"（4-6 人一队），避免 40 人挤 1 个游戏。')

doc.add_page_break()

# ============== 第六章 一线案例与痛点 ==============
H(doc, '第六章 一线案例与痛点（禅城区 7 校实践）', level=1)
P(doc, '本章将 7 篇《AI赋能英语教学实践探索》（禅城区初中英语，一~七）原文中的真实痛点与做法提炼出来，与本课程 16 法和译林版真实单元逐条对齐。', color=C_GRAY)

H(doc, '6.1 7 校案例总览', level=2)
make_table(doc,
    ['学校/老师', '一线痛点', '原文做法（原始工具）', '本培训实现（统一工具线）', '可对应真实单元'],
    [
        ['佛大附校 招蔼珊/孙雅琪', '讲评课学生被动走神', 'Trae 生成互动讲评 HTML 页、词汇跟读', '飞象老师生成评讲页 + 词汇跟读页', '八上U1 Friendship 完形/七上U2 Hobbies'],
        ['市实验学校 杨小红', '命题/备课耗时', 'Agent + Prompt 辅助命题', '豆包/DeepSeek 出题 + 飞象老师发布', '八下U2 Amazing China 单元题'],
        ['澜石中学 罗浩', '完形/单词枯燥', '完形评讲、单词 PK、种小树', '飞象老师闯关 + 飞象老师评讲页', '七上U7 Be wise with money/七下U8'],
        ['第十中学 黄家裕', '写作/规划无抓手', 'My Daily Schedule Planner', '飞象老师做"周计划生成器"', '七上U4 School days'],
        ['佛外学校 罗彩甜', '词汇操练单调', '飞象老师"水果忍者"', '飞象老师原版（直接沿用）', '七上U7 Be wise with money'],
        ['城北中学 罗艳君/潘春燕', '听力检测难兼顾趣味+分层', '豆包 + Trae 分层听测', '国家平台"智能学伴"分层 + 飞象老师闯关', '八上U5 Wild animals'],
        ['佛外高中部 徐佳岚/游伟仪', '五类课型效率低', '词汇游戏化/跟读标准化/真题闯关化/写作分层化/语法专题化（"五化"）', '本培训 16 法中⑦①⑤④⑯ 五法分别承接', '全五册通用'],
    ],
    widths=[3.5, 3.0, 4.5, 4.0, 3.5], font_size=8)

H(doc, '6.2 六大痛点×解法卡（指向真实单元）', level=2)

pain_cards = [
    ('痛点① 讲评课学生被动走神',
     '“讲完形我讲得口干，学生该睡的睡该玩的玩。”——一线原声（佛大附校 招蔼珊）',
     '解法思路：把"我讲他们听"改为"他们点+AI 评"。',
     '操作：飞象老师生成"完形评讲页"→ 学生当堂点选错题 → AI 弹解析+同类型变式 1 道。',
     '对应单元：八上U1 Friendship 完形/七下U8 Wonderland',
     '【飞象老师提示词】选"评讲模板"，导入八上U1 完形 5 道易错题，做成"点选+解析+变式"3 屏互动。'),
    ('痛点② 词汇听默单调',
     '“单词听写学生恨，我也恨。”——一线原声（澜石中学 罗浩）',
     '解法思路：把"听写"换成"游戏闯关+排行榜"。',
     '操作：飞象老师"水果忍者/记忆翻牌/种小树"模板，导入单元词表。',
     '对应单元：七上U2 Hobbies / 七上U7 Be wise with money',
     '【飞象老师提示词】为七上U7 词汇做"水果忍者"：单词落下→ 砍对加分/砍错扣分→ 5 关后排行榜。'),
    ('痛点③ 早读不敢开口',
     '“早读齐读像念经，个别抽问一片沉默。”——一线原声（第十中学 黄家裕）',
     '解法思路：把"全班齐读"换成"跟读打分+自评+互评"。',
     '操作：飞象老师"跟读模板"→ 学生小组用手机/平板跟读 → AI 打分 → 选 3 个最高分全班展。',
     '对应单元：七上U1 This is me! / 七上U2 Hobbies / 八上U1 Friendship',
     '【飞象老师提示词】选"跟读模板"导入七上U2 Hobbies Reading，英文发音+中文释义+例句+自评打分。'),
    ('痛点④ 写作结构记不住',
     '“学生背模板也写不出一封像样的信。”——一线原声（佛大附校 孙雅琪）',
     '解法思路：把"背模板"换成"看结构卡→AI 出底稿→自改→对照"。',
     '操作：飞象老师"九上U1 推荐信结构卡"→ 豆包生成底稿 → 学生自改 3 句 → 对照范信。',
     '对应单元：九上U1 Know yourself（推荐信任务）',
     '【豆包提示词】根据九上U1 D2 范信结构生成 80-100 词学习委员推荐信，标 3 个可替换点。'),
    ('痛点⑤ 语法备课翻倍',
     '“上比较级 + 最高级 5 课时，备课资料翻一周。”——一线原声（市实验 杨小红）',
     '解法思路：把"自己翻资料"换成"AI 出规则卡 + 教师加 1 个本地例子"。',
     '操作：豆包出"规则发现卡" → 教师加 1 个本地/学生身边的例子 → 飞象老师做成练习。',
     '对应单元：八上U1 Friendship（比较级）/ 九上U1（宾语从句）',
     '【豆包提示词】把八上U1 比较级规则做成 A4 卡片：左侧 5 条规则+右侧 3 条易错点+右下角口诀。'),
    ('痛点⑥ 听力检测难兼顾趣味与实效',
     '“听力测验像在考纪律，趣味和分层顾不上。”——一线原声（城北中学 罗艳君/潘春燕）',
     '解法思路：把"一套题打全班"换成"AI 分 3 层 + 闯关模式"。',
     '操作：国家平台"智能学伴"分层（A 基础/B 进阶/C 挑战）→ 飞象老师做成闯关地图。',
     '对应单元：八上U5 Wild animals（保护大熊猫 听力）/ 七下U5 Animal friends',
     '【国家平台提示词】选"听力分层"，导入八上U5 听力原文，生成 3 套（A/B/C 各 5 题），每题 1 解析。'),
]

for i, (t, q, idea, op, unit, prompt) in enumerate(pain_cards, 1):
    P(doc, '▎' + t, bold=True, color=C_RED, indent=False)
    quote_box(doc, q)
    P(doc, '解法思路：' + idea, indent=False, size=10)
    P(doc, '教师操作：' + op, indent=False, size=10)
    P(doc, '对应真实单元：' + unit, color=C_ORANGE, indent=False, size=10)
    prompt_box(doc, prompt.split('【')[1].split('】')[0], '【' + prompt.split('【')[1].split('】')[0] + '】' + prompt.split('】',1)[1])
    P(doc, '', indent=False)

H(doc, '6.3 4 条方法论（来自 7 校经验总结）', level=2)
BUL(doc, '提示词公式："背景 + 角色 + 任务 + 限制 + 格式"（与第五章一致）。')
BUL(doc, 'Skill 封装 3 级：① 单元级（一个单元的固定流程） ② 任务级（推荐信/海报/对话） ③ 教学法级（讲评/分层/闯关）。')
BUL(doc, '5 个常见问题（与 5.5 同）：成人化/直接抄/跑偏/超纲/太大班用不了。')
BUL(doc, '3 条底线：① AI 出稿必自改 ② 学生数据不出校园 ③ 教师判断不可被 AI 替代。')

doc.add_page_break()

# ============== 第七章 附录 ==============
H(doc, '第七章 附录（速查与备货）', level=1)

H(doc, '附录A 译林版 5 册单元×16 法速查', level=2)
P(doc, '下方列出 5 册共 40 个真实单元主题，每单元标注 1-3 个最契合的方法编号。讲师备课时可按"下周单元→查表→选法"两步搞定。', color=C_GRAY)

units_quick = [
    # (册, 单元, 主题, 主题范畴, 推荐方法)
    ('七上','U1','This is me!','人与自我·生活与学习','①②⑤'),
    ('七上','U2','Hobbies','人与自我·生活与学习','①②⑦'),
    ('七上','U3','Welcome to our school!','人与社会·社会服务','⑤⑨'),
    ('七上','U4','School days','人与自我·生活与学习','④⑤'),
    ('七上','U5','A healthy lifestyle','人与自我·生活与学习','⑨⑩'),
    ('七上','U6','My clothes, my style','人与自我·生活与学习','⑦⑨'),
    ('七上','U7','Be wise with money','人与自我·生活与学习','⑦⑧'),
    ('七上','U8','Let’s celebrate!','人与社会·历史社会与文化','⑨⑭'),
    ('七下','U1','Home','人与社会·历史社会与文化','⑨⑭'),
    ('七下','U2','Neighbourhoods','人与社会·人际沟通','⑥'),
    ('七下','U3','My hometown','人与社会·历史社会与文化','⑨⑭'),
    ('七下','U4','Chinese folk art','人与社会·历史社会与文化','⑨⑭'),
    ('七下','U5','Animal friends','人与自然·自然生态','⑨⑫'),
    ('七下','U6','Beautiful landscapes','人与自然·自然生态','⑨⑫'),
    ('七下','U7','Outdoor fun','人与自我·生活与学习','⑦'),
    ('七下','U8','Wonderland','人与自我·做人与做事','⑧⑨⑪'),
    ('八上','U1','Friendship','人与自我·做人与做事','①②④⑤⑥⑧⑪'),
    ('八上','U2','School life','人与社会·社会服务','⑨⑭'),
    ('八上','U3','To be a good learner','人与自我·做人与做事','④⑫⑬'),
    ('八上','U4','Hands-on fun','人与自我·生活与学习','⑦'),
    ('八上','U5','Wild animals','人与自然·自然生态','⑨⑫⑮'),
    ('八上','U6','Seasons','人与自然·自然生态','⑨⑫'),
    ('八上','U7','The natural world','人与自然·自然生态','⑨⑫⑮'),
    ('八上','U8','Safe and sound','人与自然·灾害防范','⑨⑫'),
    ('八下','U1','Past and present','人与社会·历史社会与文化','⑤⑨⑫'),
    ('八下','U2','Amazing China','人与社会·历史社会与文化','⑨⑬'),
    ('八下','U3','The world at one click','人与社会·科学与技术','⑨⑭'),
    ('八下','U4','A good read','人与自我·做人与做事','⑪⑫⑬'),
    ('八下','U5','Good manners','人与社会·社会服务','⑨⑪'),
    ('八下','U6','Sunshine for all','人与社会·社会服务','⑨⑪'),
    ('八下','U7','Charities','人与社会·社会服务','⑨⑪'),
    ('八下','U8','A green world','人与自然·环境保护','⑨⑮⑯'),
    ('九上','U1','Know yourself','人与自我·做人与做事','③④⑤'),
    ('九上','U2','Colours','人与自我·做人与做事','⑨⑭'),
    ('九上','U3','Teenage problems','人与自我·做人与做事','⑨⑫'),
    ('九上','U4','Growing up','人与自我·做人与做事','⑤⑪'),
    ('九上','U5','Art world','人与社会·文学艺术与体育','⑨⑪'),
    ('九上','U6','TV programmes','人与社会·文学艺术与体育','⑨⑪'),
    ('九上','U7','Films','人与社会·文学艺术与体育','⑨⑪'),
    ('九上','U8','Detective stories','人与社会·文学艺术与体育','⑪⑫'),
]

make_table(doc,
    ['册','单元','主题','主题范畴','推荐方法'],
    units_quick,
    widths=[1.4, 1.2, 4.0, 5.5, 4.5], font_size=8)

H(doc, '附录B 提示词速查卡（按真实单元分类，复制即用）', level=2)

prompt_cards = [
    # 类别, 单元, 工具, 提示词
    ('写作类','九上U1 推荐信','豆包/DeepSeek',
     '你是有 10 年教龄的初中英语教师。请根据九上U1 D2 范信结构，生成 80-100 词【学习委员】推荐信，标 3 个可替换点。'),
    ('写作类','八下U1 家乡变化海报','豆包/DeepSeek',
     '为八下U1 Past and present 写双语海报：中文标题"我的家乡 20 年"+英文 3 句介绍（交通/建筑/教育 选 1 主题）。'),
    ('写作类','八上U2 School life 介绍','豆包/DeepSeek',
     '为八上U2 School life 写"My school life"80 词短文，含作息/课程/课外活动 3 段，标 3 个可替换点。'),
    ('写作类','八下U4 推荐一本书','豆包/DeepSeek',
     '为八下U4 A good read 写 80 词书评，含故事简介+喜欢原因 1 段+推荐语，模仿 D2 推荐信结构。'),
    ('口语类','七下U2 借东西对话','飞象老师/豆包',
     '为七下U2 Neighbourhoods 生成 3 段角色对话（借工具/问路/约时间），15 句内，礼貌表达+可替换关键词。'),
    ('口语类','八上U1 Friendship 友谊微剧','豆包+飞象',
     '为八上U1 写 3 分钟友谊短剧脚本（5 角色），含冲突-和解，含中英对照台词和分镜。'),
    ('口语类','九上U8 Detective stories 短剧','豆包+飞象',
     '为九上U8 写 3 分钟侦探短剧脚本（5 角色），含嫌疑人+线索+推理，初中词汇。'),
    ('词汇类','七上U2 Hobbies 跟读','飞象老师',
     '导入七上U2 Hobbies 单元词汇，做"跟读+释义+例句+自评"4 屏互动。'),
    ('词汇类','七上U7 Be wise with money 水果忍者','飞象老师',
     '为七上U7 词汇做"水果忍者"游戏：单词落下→ 砍对加分/砍错扣分→ 5 关排行榜。'),
    ('词汇类','七上U6 My clothes 记忆翻牌','飞象老师',
     '为七上U6 词汇做"记忆翻牌"游戏：4×4 卡片配对+词义题+排行榜。'),
    ('阅读类','八下U1 The rise of Shenzhen 脚手架','国家平台/豆包',
     '为八下U1 阅读做"略读-精读-批判"3 步脚手架，每步 1 张卡+2 错法+1 反馈话术。'),
    ('阅读类','八上U5 Protecting pandas 论证结构','豆包',
     '为八上U5 提取"保护大熊猫"3 条核心论证（栖息地/立法/公众参与），每条 1 张卡+1 例句。'),
    ('语法类','八上U1 比较级规则发现卡','豆包/DeepSeek',
     '把八上U1 比较级与最高级规则做 A4 卡片：左 5 条规则+右 3 条易错点+口诀。'),
    ('语法类','九上U1 宾语从句规则卡','豆包/DeepSeek',
     '把九上U1 宾语从句（that 引导）做 A4 卡片：左 3 条规则+右 3 个例句+右下口诀。'),
    ('文化类','七下U1 各国住宅对比','豆包+飞象',
     '生成"中国/英国/日本/非洲"4 国住宅双语对比清单（材料/层数/院落/采光 5 维度），飞象老师做投票。'),
    ('文化类','八上U2 Unusual schools 对比','豆包+飞象',
     '为八上U2 School life 写 3 段"Unusual schools"对比（蒙古/芬兰/秘鲁），双语+飞象投票。'),
    ('环保类','八下U8 A green world 辩论','飞象老师+豆包',
     '豆包生成"是否应禁止一次性塑料"正反方各 3 论据，飞象老师做 4v4 辩论模板。'),
    ('环保类','八上U5 Wild animals 项目','豆包+飞象',
     '为八上U5 写"保护大熊猫"项目方案：①现状 3 句 ②原因 3 句 ③行动 3 句，初中词汇+飞象海报。'),
    ('项目类','八下U1 Project 1 国别指南','豆包+DeepSeek',
     '为八下U1 Project 1（A travel guide to a country）生成项目脚手架：选国家+3 段语料+A4 双面宣传册文字稿。'),
    ('项目类','七下U8 Project 2 自然主题报纸','豆包+DeepSeek',
     '为七下U8 Project 2（school newspaper about nature）写 4 版主题：奇观/植物/动物/行动，初中词汇+ 配图位。'),
    ('评测类','八上U1 完形评讲页','飞象老师',
     '导入八上U1 完形 5 道易错题，做"点选+解析+同类型变式 1 道"3 屏互动。'),
    ('评测类','八上U3 学习策略错题归因','国家平台/豆包',
     '为八上U3 错题生成分层题（A 词汇/B 句型/C 段落），每题配 1 个"错因标签"。'),
]

for cat, unit, tool, prompt in prompt_cards:
    P(doc, '【' + cat + '】' + unit + '（' + tool + '）', bold=True, color=C_GREEN, indent=False, size=10)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.left_indent = Cm(0.74)
    r = p.add_run(prompt)
    set_run_font(r, size=9, color=C_GRAY)
    P(doc, '', indent=False)

H(doc, '附录C 讲师备货清单', level=2)
BUL(doc, '电脑+投影（飞象老师/PPT 演示用）')
BUL(doc, '学员手机（豆包/DeepSeek 现场试用）')
BUL(doc, '打印本：附录 B 提示词速查卡（每学员 1 份）')
BUL(doc, '国家智慧中小学平台账号（飞象老师登录）')
BUL(doc, '便利贴/白板墙（6 大痛点 + 三样产出展评用）')
BUL(doc, '可选：二维码贴纸（学员扫国家平台/飞象老师/豆包/DeepSeek 入口）')

H(doc, '附录D 教-学-评一致性自检', level=2)
P(doc, '每次课前用 4 个问题自检：')
NUM(doc, '我让学生练的，是否对应课标核心素养（语言/文化/思维/学习）四要素中至少 1 项？')
NUM(doc, '我用的方法，是否落在主题范畴（人与自我/社会/自然）三范畴中至少 1 个？')
NUM(doc, 'AI 出的内容，是否经过学生/教师自改？是否避免直接使用？')
NUM(doc, '我带走的"三样东西"，下周真实课能用上吗？')

# ============== 封底 ==============
doc.add_page_break()
foot = doc.add_paragraph()
foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = foot.add_run('—— 本课程设计基于《义务教育英语课程标准（2022年版）》与译林版（2024-2026新版）教材 ——')
set_run_font(r, size=10, color=C_GRAY)
foot2 = doc.add_paragraph()
foot2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = foot2.add_run('工具线：国家智慧中小学平台 · 飞象老师 · 豆包/DeepSeek 网页版')
set_run_font(r, size=10, color=C_GRAY)
foot3 = doc.add_paragraph()
foot3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = foot3.add_run('一线依据：禅城区初中英语《AI赋能英语教学实践探索》(一)~(七) 7 校案例')
set_run_font(r, size=10, color=C_GRAY)

out = "D:/projects/WorkBuddy/2026-06-17-11-18-20/AI赋能英语教学_3小时培训课程设计_课标锚定版.docx"
doc.save(out)
print("SAVED:", out)
