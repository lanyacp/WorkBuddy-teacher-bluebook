# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import parse_xml

def set_run_font(run, font_name='微软雅黑', size=10.5, bold=False, color=None):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color

def add_heading_custom(doc, text, level=1):
    heading = doc.add_heading(level=level)
    run = heading.add_run(text)
    if level == 1:
        set_run_font(run, size=16, bold=True, color=RGBColor(0x1a, 0x5f, 0x7a))
    elif level == 2:
        set_run_font(run, size=14, bold=True, color=RGBColor(0x2e, 0x7d, 0x32))
    elif level == 3:
        set_run_font(run, size=12, bold=True, color=RGBColor(0xf5, 0x7c, 0x00))
    else:
        set_run_font(run, size=11, bold=True)
    heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return heading

def add_para_custom(doc, text, bold=False, indent=True, size=10.5, color=None):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.first_line_indent = Cm(0.74)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, color=color)
    return p

def add_bullet_para(doc, text, level=0, size=10.5):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Cm(0.74 + level * 0.5)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    set_run_font(run, size=size)
    return p

def add_number_para(doc, text, level=0, size=10.5):
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.left_indent = Cm(0.74 + level * 0.5)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    set_run_font(run, size=size)
    return p

def fill_cell_color(cell, hex_color):
    xml_str = '<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fill="' + hex_color + '"/>'
    shading = parse_xml(xml_str)
    cell._tc.get_or_add_tcPr().append(shading)

def add_prompt_box(doc, title, content):
    add_para_custom(doc, f"【{title}】", bold=True, indent=False, color=RGBColor(0x1a, 0x5f, 0x7a))
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.left_indent = Cm(0.74)
    run = p.add_run(content)
    set_run_font(run, size=9, color=RGBColor(0x33, 0x33, 0x33))
    return p

# ==================== 文档 ====================
doc = Document()
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
style.font.size = Pt(10.5)
style.paragraph_format.line_spacing = 1.5

# ===== 封面 =====
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title.add_run('AI赋能英语教学（译林版初中）融合应用方案')
set_run_font(title_run, size=20, bold=True, color=RGBColor(0x1a, 0x5f, 0x7a))

title2 = doc.add_paragraph()
title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
title2_run = title2.add_run('基于国家智慧中小学平台"用AI"应用 + 飞象老师的实操设计')
set_run_font(title2_run, size=15, bold=True, color=RGBColor(0x2e, 0x7d, 0x32))

doc.add_paragraph()
info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
info_run = info.add_run('教材版本：牛津译林版（初中七/八/九年级）\n工具原则：优先使用"国家智慧中小学"平台"用AI"应用（全国试用、账号单点登录、数据合规安全可靠）\n核心互动工具：飞象老师（做互动网页 / 游戏化课件，平台内可直接登录）\n配套：3小时实操培训时间轴 + 提示词速查卡')
set_run_font(info_run, size=12)

doc.add_page_break()

# ===== 一、方案总览 =====
add_heading_custom(doc, '一、方案总览', 1)

add_para_custom(doc, '【适用对象】', bold=True, indent=False)
add_para_custom(doc, '使用牛津译林版（初中）英语教材的七、八、九年级教师。本方案承接《AI赋能英语教学教研3小时培训方案》，将其中的"免费工具"原则进一步落地：把原文提到的16种AI英语融合方法，逐一替换为"国家智慧中小学"平台"用AI"应用及国内免费工具，并以译林版真实单元为案例，做到"拿来就能用"。所有推荐应用均通过平台账号单点登录、免费且数据安全合规，方便一线教师直接获取。')

add_para_custom(doc, '【设计原则】', bold=True, indent=False)
add_bullet_para(doc, '平台优先：能用国家智慧中小学平台"用AI"应用的，一律优先用平台应用——账号单点登录、数据合规、安全可靠，无需另注册')
add_bullet_para(doc, '免费优先：全部为国内产品且基础功能免费，打开网页即用，不装软件')
add_bullet_para(doc, '讲练比约3:7：每个融合方法都配可复制的提示词与一步实操')
add_bullet_para(doc, '学科强针对：所有案例绑定译林版单元话题，避免"通用模板不落地"')
add_bullet_para(doc, '红线不变：AI给的是草稿，教师必须二次加工；正式测评仍由老师把关')

add_para_custom(doc, '【16种融合方法·四维度框架】', bold=True, indent=False)
add_bullet_para(doc, '维度一 智能语言输入与习得（4种）：听力沉浸 / 词汇建构 / 语法渗透 / 跨文化模拟')
add_bullet_para(doc, '维度二 个性化语言输出训练（4种）：口语陪练 / 写作批改 / 角色扮演 / 创意写作')
add_bullet_para(doc, '维度三 互动教学场景创新（4种）：数字教师 / 词汇竞技 / 跨文化对比 / 影视剪辑')
add_bullet_para(doc, '维度四 批判性思维与综合应用（4种）：新闻辩论 / 故事接龙 / 路径规划 / 口语模考')

add_para_custom(doc, '【工具清单：国家智慧中小学平台"用AI"应用（优先使用）】', bold=True, indent=False)
add_bullet_para(doc, 'E听说（科大讯飞）：英语听说读写考全覆盖，AI语音识别、口语评分、智能批改、班级学情分析——听说训练首选')
add_bullet_para(doc, '飞象老师（猿辅导）：互动课件、游戏化课件、教学动画、AI命题/组题、大单元教案——做互动网页与课堂游戏首选，平台内单点登录、全国免费')
add_bullet_para(doc, '企鹅教师助手（腾讯）：AI课件、AI剧本教学、AI创意教学设计、多模态教学资源——备课与课件首选')
add_bullet_para(doc, '企鹅智慧学练（腾讯）：多模态AIGC，文生文/文生图/文生视频/AI播客——创意写作、影视、数字教师内容生成')
add_bullet_para(doc, '多智能体课堂（清华）：多AI角色实时对话，含英语课程——角色扮演、口语陪练、跨文化模拟、辩论')
add_bullet_para(doc, '希沃白板（全学科）：AI一键生成互动课件、课堂小游戏（抢答/小组PK/随机点名）、作业批改')
add_bullet_para(doc, '英语作文助手：全流程英文写作支持，纠错/批改/润色/素材/范文——写作批改首选')
add_bullet_para(doc, '作业批改助手：文本与图片输入，无需登录，班级批量使用')
add_bullet_para(doc, '学科对话助手：语文/英语等学科智能对话答疑——语法与疑问解答')
add_bullet_para(doc, '全链路AI备课：免费官方AI备课，教案生成/思维导图/智能出题/复习卡片，1-2分钟出方案')
add_bullet_para(doc, '题目推荐助手：输入题目生成多道不同难度相似题+解析+答案——组题与变式')
add_bullet_para(doc, 'SEED学生综合素质智能评价：五育成长画像——综合素质评价（可选）')

add_para_custom(doc, '【平台暂未覆盖、用国内免费补充】', bold=True, indent=False)
add_bullet_para(doc, '百词斩/墨墨背单词（词汇记忆与路径规划）、21世纪学生英文报（英语新闻语料）、腾讯文档（协作接龙）、可可英语/每日英语听力（听力真实语料）')

add_para_custom(doc, '【进阶（基地校试点，可关注）】', bold=True, indent=False)
add_bullet_para(doc, '星火教师助手（科大讯飞，AI课件/教学设计/智能体）、小乐老师（题库/智能批改/学情）、木疙瘩（多模态互动资源）')

doc.add_page_break()

# ===== 二、16种融合方案 总表 =====
add_heading_custom(doc, '二、16种融合方案 × 平台AI应用 × 译林版案例 总表', 1)
add_para_custom(doc, '下表为快速对照。原文"原工具"多为境外收费产品，已统一替换为"国家智慧中小学"平台"用AI"应用及国内免费工具；"译林案例"给出可直接套用的单元与话题。', indent=False)

# 总表：方法 | 原文工具 | 平台/国内替代 | 译林版案例
table = doc.add_table(rows=17, cols=4)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

headers = ['融合方法', '原文工具（境外）', '平台/国内免费替代', '译林版案例']
for i, h in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            set_run_font(run, bold=True, color=RGBColor(0xff, 0xff, 0xff), size=9)
    fill_cell_color(cell, '1A5F7A')

rows = [
    ['1 AI精准听力沉浸训练', 'ELSA Speak/BBC', 'E听说(听说/纠音评分)+可可英语(语料)', '七上U5 Let\'s celebrate!(节日聚会)'],
    ['2 AI可视化词汇建构', 'Pearson/Quizlet AI', '企鹅智慧学练(文生图/动画)+百词斩', '八上U5 Wild animals(动物词)'],
    ['3 AI语境化语法渗透', 'Grammarly EDU/DeepL', '全链路AI备课(智能出题)+英语作文助手(纠错)', '八上U1 Friends(比较级)'],
    ['4 AI跨文化场景模拟', 'ChatGPT+VR', '多智能体课堂+学科对话助手', '七上U5/八上U8(节日/应急礼仪)'],
    ['5 AI实时口语陪练纠错', 'Cambly/DeepSeek', 'E听说(口语评分)+多智能体课堂', '八上U3 A day out(旅行对话)'],
    ['6 AI写作批改润色', 'Writefull/Grammarly', '英语作文助手+作业批改助手', '九上U3 Teenage problems(建议信)'],
    ['7 AI角色扮演情景对话', 'ChatGPT+ElevenLabs', '多智能体课堂(多AI角色)+E听说', '七上U3 Welcome to school(向导)'],
    ['8 AI创意写作辅助拓展', 'Storybird/OpenAI', '企鹅智慧学练(AI对话)+英语作文助手', '九上U8 Detective stories(推理)'],
    ['9 AI数字教师答疑', 'Heygen数字人', '企鹅智慧学练(文生视频/AI播客)+企鹅教师助手', '八上U4 Do it yourself(步骤)'],
    ['10 AI词汇竞技游戏化(互动网页)', 'Kahoot!/Quizizz', '飞象老师(贪吃蛇/消消乐/互动课件)', '七上U1 This is me!(词汇游戏)'],
    ['11 AI跨文化对比分析', 'Culture Crossing AI', '多智能体课堂+企鹅教师助手', '九上U2 Colours(色彩文化)'],
    ['12 AI影视片段智能剪辑', 'Descript AI', '企鹅智慧学练(文生视频)+希沃白板', '九上U7 Films(电影片段)'],
    ['13 AI新闻摘要与辩论', 'NewsGuard/BBC', '学科对话助手+多智能体课堂+21世纪英文报', '九上U6 TV programmes(新闻)'],
    ['14 AI故事接龙逻辑续写', 'Inkitt AI', '企鹅智慧学练(AI对话)+腾讯文档', '九上U8 Detective stories(接龙)'],
    ['15 AI学习路径智能规划', 'Duolingo Max', 'E听说(个性化路径)+全链路AI备课(复习卡)+百词斩', '七上U2 My day(习惯路径)'],
    ['16 AI口语评分升学模考', 'TOEFL/IELTS AI', 'E听说(口语评分模考)+多智能体课堂', '八上U2 School life(口语)'],
]

for row_idx, row_data in enumerate(rows, start=1):
    for col_idx, text in enumerate(row_data):
        cell = table.rows[row_idx].cells[col_idx]
        cell.text = text
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.line_spacing = 1.25
            for run in para.runs:
                set_run_font(run, size=8.5)

for row in table.rows:
    row.cells[0].width = Inches(1.9)
    row.cells[1].width = Inches(1.5)
    row.cells[2].width = Inches(2.1)
    row.cells[3].width = Inches(1.6)

doc.add_page_break()

# ===== 三、四维融合方案详解 =====
add_heading_custom(doc, '三、四维融合方案详解（含提示词）', 1)
add_para_custom(doc, '每个方法给出：原文工具→平台/国内替代→译林版案例→操作步骤→可直接复制的提示词。提示词中的【】需按实际替换。涉及"国家智慧中小学"平台应用，均用平台账号单点登录，免费且数据安全。', indent=False)

# ---------- 维度一 ----------
add_heading_custom(doc, '维度一：智能语言输入与习得', 2)

add_heading_custom(doc, '方法1 AI精准听力沉浸训练', 3)
add_para_custom(doc, '替代方案：用"E听说"布置分层听力作业（系统自带分级语料+AI纠音评分），或用"全链路AI备课"生成听力练习；真实语料不足时用"可可英语/每日英语听力"补充。乡镇无网时可用平台离线布置的功能。', indent=False)
add_para_custom(doc, '译林案例：七上 Unit 5 Let\'s celebrate!（节日/聚会）。', indent=False)
add_prompt_box(doc, '提示词(在企鹅教师助手/E听说生成听力材料)',
    '你是一位初中英语听力材料编写者。请为主题"节日聚会点餐"生成3个版本的听力文本：\n·慢速版(约110词/分钟，附中文重点短语)\n·标准版(约140词/分钟，标出连读处)\n·快速版(约170词/分钟，供进阶)\n每版后附3道填空选择题。文本需贴合译林版七上U5词汇(celebrate, festival, present, dress up等)。')

add_heading_custom(doc, '方法2 AI可视化词汇建构', 3)
add_para_custom(doc, '替代方案：用"企鹅智慧学练"的AI绘画/文生图功能，为单词生成情境配图与动画；再导入"百词斩"自制词书，学生按图记忆。低龄学生可用动态描述强化具象记忆。', indent=False)
add_para_custom(doc, '译林案例：八上 Unit 5 Wild animals（giant panda, dolphin, bear…）。', indent=False)
add_prompt_box(doc, '提示词(在企鹅智慧学练生成配图)',
    '请为以下动物词汇生成可视化学习卡：giant panda, dolphin, bear, squirrel, kangaroo。\n每张卡包含：①音标与词性 ②1个译林版八上U5情境例句 ③1句形象记忆法 ④一段可用于AI绘画的配图描述(如"pandas eating bamboo")。')

add_heading_custom(doc, '方法3 AI语境化语法渗透', 3)
add_para_custom(doc, '替代方案：用"全链路AI备课"智能出题生成语法练习与微课框架，配合"英语作文助手"做语法纠错反馈，替代Grammarly EDU。', indent=False)
add_para_custom(doc, '译林案例：八上 Unit 1 Friends（形容词比较级/最高级）。', indent=False)
add_prompt_box(doc, '提示词(在企鹅教师助手/全链路AI备课输入)',
    '你是初中英语语法老师。学生常混淆形容词比较级与最高级。请生成5分钟微课：\n①用译林八上U1句子对比 "Tom is taller than Millie" 与 "Amy is the slimmest in her class"\n②标注变化规则(直接加-er/-est, 双写, 改y为i)\n③附8道情境选择题。输出结构化文本。')

add_heading_custom(doc, '方法4 AI跨文化场景模拟', 3)
add_para_custom(doc, '替代方案：在"多智能体课堂"搭建跨文化对话场景（无需VR设备），设定中外文化角色，学生用"学科对话助手"实时对话即可角色扮演。', indent=False)
add_para_custom(doc, '译林案例：七上 U5（中西方节日对比）/ 八上 U8 Natural disasters（应急礼仪）。', indent=False)
add_prompt_box(doc, '提示词(多智能体课堂/学科对话助手设定)',
    '你是一个耐心的中外文化向导。任务：帮助学生对比中西方节日。当用户说"春节"时，介绍其习俗并对比Christmas；当用户用错文化表达时温柔纠正。只说简单英语+中文解释。')

doc.add_page_break()

# ---------- 维度二 ----------
add_heading_custom(doc, '维度二：个性化语言输出训练', 2)

add_heading_custom(doc, '方法5 AI实时口语陪练纠错', 3)
add_para_custom(doc, '替代方案："E听说"提供口语评分与个性化纠音；"多智能体课堂"可设定外教/伙伴角色实时对话陪练，替代Cambly；乡镇缺外教的最佳替代。', indent=False)
add_para_custom(doc, '译林案例：八上 Unit 3 A day out（旅行点餐/问路）。', indent=False)
add_prompt_box(doc, '提示词(口语陪练·多智能体课堂/E听说)',
    '请扮演餐厅服务员，用简单英语和我对话，模拟译林八上U3"外出就餐"场景。我每说错一句(发音/语法/礼貌用语)，请先鼓励，再温柔纠正并给更自然的说法。每次只说1-2句。')

add_heading_custom(doc, '方法6 AI写作批改润色', 3)
add_para_custom(doc, '替代方案：用"英语作文助手"做全流程英文写作支持（纠错/批改/润色/素材），配合"作业批改助手"批量处理全班作业照片，替代Writefull/Grammarly。', indent=False)
add_para_custom(doc, '译林案例：九上 Unit 3 Teenage problems（写一封建议信）。', indent=False)
add_prompt_box(doc, '提示词(英语作文助手)',
    '请批改这份九年级英语建议信(关于teenage problems)。分层反馈：\n·基础版：标出语法/拼写错误并改正\n·进阶版：指出可升级的表达(如把"very good"换成"excellent")\n最后写一句鼓励性中文评语。')

add_heading_custom(doc, '方法7 AI角色扮演情景对话', 3)
add_para_custom(doc, '替代方案：在"多智能体课堂"搭建多角色智能体（不同教学风格/口音），学生用"E听说"评分纠音，替代ChatGPT+ElevenLabs。', indent=False)
add_para_custom(doc, '译林案例：七上 Unit 3 Welcome to our school!（校园向导/参观）。', indent=False)
add_prompt_box(doc, '提示词(多智能体课堂智能体)',
    '你在校门口当"校园向导"。学生扮演访客，你用简单英语介绍学校(教室、图书馆、操场)，并提问引导其回答。说错时给提示，不说答案。语气热情。')

add_heading_custom(doc, '方法8 AI创意写作辅助拓展', 3)
add_para_custom(doc, '替代方案：用"企鹅智慧学练"的AI对话（文生文）输入关键词生成故事开头与情节分支，配合"英语作文助手"做润色与素材补充，替代Storybird/OpenAI。', indent=False)
add_para_custom(doc, '译林案例：九上 Unit 8 Detective stories（推理故事）。', indent=False)
add_prompt_box(doc, '提示词(企鹅智慧学练AI对话)',
    '请以"校园侦探"为题，为译林九上U8写一段英语科幻推理故事开头(约60词)，关键词：mysterious note, lost watch, clever detective。再提供2个情节分支建议供学生续写。')

doc.add_page_break()

# ---------- 维度三 ----------
add_heading_custom(doc, '维度三：互动教学场景创新', 2)

add_heading_custom(doc, '方法9 AI数字教师答疑', 3)
add_para_custom(doc, '替代方案：用"企鹅智慧学练"的文生视频/图生视频/AI播客功能，把知识点生成带讲解的短视频或播客；配合"企鹅教师助手"制作多模态教学资源，替代Heygen数字人。', indent=False)
add_para_custom(doc, '译林案例：八上 Unit 4 Do it yourself（DIY步骤讲解）。', indent=False)
add_prompt_box(doc, '操作步骤',
    '①在企鹅教师助手建立"八上U4 DIY"多模态资源，整理教案与步骤图；②用企鹅智慧学练"文生视频/AI播客"把步骤讲解稿生成1分钟讲解短视频或音频；③发班级群/平台作业，供学生随时回看答疑。')

add_heading_custom(doc, '方法10 AI词汇竞技游戏化（互动网页）', 3)
add_para_custom(doc, '替代方案：用"飞象老师"（国家智慧中小学平台"用AI"应用，账号单点登录、全国免费）——上传单词表或输入一句话，即可生成"贪吃蛇""消消乐""连连看"等趣味单词游戏，以及互动课件、教学动画。无需写代码、无需装软件、网页直接打开，替代Kahoot!/Quizizz。', indent=False, color=RGBColor(0xc0, 0x00, 0x00))
add_para_custom(doc, '译林案例：七上 Unit 1 This is me!（爱好/自我介绍词汇）。', indent=False)
add_prompt_box(doc, '飞象老师操作步骤',
    '①用国家智慧中小学账号登录飞象老师(平台"用AI"区单点登录，或访问 feixianglaoshi.com)；\n②在输入框写："为译林七上U1生词(reading, dancing, swimming, cooking, drawing…)做一个英语单词消消乐/贪吃蛇游戏"；\n③等待AI生成，预览后可调整难度、增减词汇、改配色；\n④点击"使用/分享"，课堂直接打开，学生抢答计分，还能发布到社区与同事共享。')

add_heading_custom(doc, '方法11 AI跨文化对比分析', 3)
add_para_custom(doc, '替代方案：在"多智能体课堂"设定不同文化AI角色做对比对话，配合"企鹅教师助手"的AI创意教学设计生成对比活动，替代Culture Crossing AI。', indent=False)
add_para_custom(doc, '译林案例：九上 Unit 2 Colours（中西方色彩文化含义）。', indent=False)
add_prompt_box(doc, '提示词(多智能体课堂/企鹅教师助手)',
    '请对比中西方对"红色/白色/黄色"的文化含义，生成一张对比表(含义/例句/禁忌)，并写一段适合九年级学生的英文对话案例，用于译林九上U2文化拓展。')

add_heading_custom(doc, '方法12 AI影视片段智能剪辑', 3)
add_para_custom(doc, '替代方案：用"企鹅智慧学练"的文生视频/图生视频做关键帧解读与填空字幕，配合"希沃白板"AI一键生成互动课件循环练习，替代Descript AI。', indent=False)
add_para_custom(doc, '译林案例：九上 Unit 7 Films（电影片段听说）。', indent=False)
add_prompt_box(doc, '操作步骤',
    '①导入一段英文电影片段(如动画)；②用企鹅智慧学练"文生视频/图生图"提取核心句型并生成填空字幕解读；③用希沃白板生成互动课件(隐藏关键词让学生配音)；④导出练习视频，课堂循环使用。')

doc.add_page_break()

# ---------- 维度四 ----------
add_heading_custom(doc, '维度四：批判性思维与综合应用', 2)

add_heading_custom(doc, '方法13 AI新闻摘要与观点辩论', 3)
add_para_custom(doc, '替代方案：用"学科对话助手"做英语对话与辩论引导，"多智能体课堂"设定正反方AI角色，语料取自"21世纪学生英文报"（国内免费），替代NewsGuard/BBC。', indent=False)
add_para_custom(doc, '译林案例：九上 Unit 6 TV programmes（新闻/观点类节目）。', indent=False)
add_prompt_box(doc, '提示词(学科对话助手/多智能体课堂)',
    '请基于"21世纪学生英文报"难度，生成一篇关于"AI in daily life"的简易英语新闻(约120词)，含Pro/Con两方观点摘要，并设计1个班级辩论议题，附常用表达(From my perspective…)。')

add_heading_custom(doc, '方法14 AI故事接龙逻辑续写', 3)
add_para_custom(doc, '替代方案：用"企鹅智慧学练"AI对话做跨班故事接龙，用"腾讯文档"协作记录，替代Inkitt AI。', indent=False)
add_para_custom(doc, '译林案例：九上 Unit 8 Detective stories（班级接龙破案）。', indent=False)
add_prompt_box(doc, '提示词(企鹅智慧学练AI对话)',
    'A班已写开头："A mysterious note appeared on the teacher\'s desk…" 请分析其悬疑基调，建议B班续写方向(加入clue与dialogue推动情节)，并给3个可使用的英语连接词。')

add_heading_custom(doc, '方法15 AI学习路径智能规划', 3)
add_para_custom(doc, '替代方案：用"E听说"的个性化提升路径做听说规划，"全链路AI备课"生成复习卡片，配合"百词斩/墨墨背单词"（国内免费，自带规划）做日常背词，替代Duolingo Max。', indent=False)
add_para_custom(doc, '译林案例：七上 Unit 2 My day（习惯养成路径）。', indent=False)
add_prompt_box(doc, '提示词(全链路AI备课/E听说)',
    '我班七年级生词汇薄弱、听力一般。请基于译林七上U2 My day话题，生成一周英语学习路径：周一三五日背词(10分钟)、周二四听力(可可英语)、周末错题复习。输出打卡表与复习卡片。')

add_heading_custom(doc, '方法16 AI口语评分升学模考', 3)
add_para_custom(doc, '替代方案：用"E听说"的口语评分与升学模考功能（AI语音识别、口语评分、个性化纠音），配合"多智能体课堂"设定口语模考场景，替代TOEFL/IELTS AI。', indent=False)
add_para_custom(doc, '译林案例：八上 Unit 2 School life（升学口语话题）。', indent=False)
add_prompt_box(doc, '提示词(评分·E听说/多智能体课堂)',
    '请就话题"My school life"(译林八上U2)给我的英文作答按四维评分：流利度/发音/词汇多样性/语法准确性(各30分)，指出2个最该改进的点并给同义替换清单。')

doc.add_page_break()

# ===== 四、3小时培训时间轴（完善版） =====
add_heading_custom(doc, '四、3小时培训时间轴（完善版）', 1)
add_para_custom(doc, '在原3小时框架基础上，每个模块明确"对应哪些融合方法 + 使用哪个平台AI应用 + 译林版案例"，使16种方法全覆盖、讲练比约3:7。全程用国家智慧中小学平台账号登录，工具获取零门槛。', indent=False)

table2 = doc.add_table(rows=9, cols=4)
table2.style = 'Table Grid'
table2.alignment = WD_TABLE_ALIGNMENT.CENTER

headers2 = ['模块', '时长', '核心内容(融合方法·平台应用)', '译林版实操产出']
for i, h in enumerate(headers2):
    cell = table2.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            set_run_font(run, bold=True, color=RGBColor(0xff, 0xff, 0xff), size=9)
    fill_cell_color(cell, '2E7D32')

rows2 = [
    ['M0 破冰导入', '10分钟', '认知建立；引出六大痛点；介绍平台"用AI"入口与单点登录', '板书归类"最耗时环节"'],
    ['M1 平台+提示词', '25分钟', '方法3/6基础(角色+任务+要求)；初识全链路AI备课/英语作文助手', '首条指令:七上U1单词听写清单'],
    ['M2 AI辅助备课', '40分钟', '方法2/3/7/8(词汇卡/语法/角色/创意)；企鹅教师助手+全链路AI备课+多智能体课堂+企鹅智慧学练', '八上U1教案+企鹅教师助手课件+易混词卡'],
    ['M3 作业减负', '30分钟', '方法6/5(批改/口语陪练)；英语作文助手+作业批改助手+E听说/多智能体课堂', '批改一篇作文+口语陪练录音'],
    ['M4 互动与口语', '35分钟', '方法4/7/9/10(模拟/角色/数字人/游戏)；多智能体课堂+企鹅智慧学练+飞象老师', '飞象老师单词游戏+多智能体课堂角色'],
    ['M5 AI教研', '20分钟', '方法12/13/16(剪辑/新闻/评分)；希沃白板+企鹅智慧学练+学科对话助手+E听说', '试卷分析+新闻辩论题'],
    ['M6 总结答疑', '10分钟', '方法1/11/14/15(听力/对比/接龙/路径)；E听说+多智能体课堂+企鹅智慧学练+全链路AI备课', '速查卡+行动计划'],
    ['合计', '180分钟', '覆盖16种融合方法(平台AI应用为主+飞象老师做互动网页)', '可带回的成品包'],
]

for row_idx, row_data in enumerate(rows2, start=1):
    for col_idx, text in enumerate(row_data):
        cell = table2.rows[row_idx].cells[col_idx]
        cell.text = text
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.line_spacing = 1.25
            for run in para.runs:
                set_run_font(run, size=8.5)

for row in table2.rows:
    row.cells[0].width = Inches(1.4)
    row.cells[1].width = Inches(1.0)
    row.cells[2].width = Inches(2.6)
    row.cells[3].width = Inches(2.1)

doc.add_page_break()

# ===== 五、译林版单元 × 16方法 速查对照 =====
add_heading_custom(doc, '五、译林版单元 × 16方法 速查对照', 1)
add_para_custom(doc, '下列单元为牛津译林版（初中）常用话题，可优先套用对应融合方法。教师可按所教年级直接取用。', indent=False)

add_heading_custom(doc, '七年级（上册）', 3)
add_bullet_para(doc, 'U1 This is me! → 方法10(飞象老师词汇游戏)、方法2(可视化词汇)')
add_bullet_para(doc, 'U2 My day → 方法15(学习路径)')
add_bullet_para(doc, 'U3 Welcome to our school! → 方法7(多智能体课堂角色扮演向导)')
add_bullet_para(doc, 'U5 Let\'s celebrate! → 方法1(E听说听力)、方法4(跨文化模拟)')

add_heading_custom(doc, '八年级（上册）', 3)
add_bullet_para(doc, 'U1 Friends → 方法3(全链路AI备课语法比较级)')
add_bullet_para(doc, 'U2 School life → 方法16(E听说口语模考)')
add_bullet_para(doc, 'U3 A day out → 方法5(E听说/多智能体课堂口语陪练)')
add_bullet_para(doc, 'U4 Do it yourself → 方法9(企鹅智慧学练数字教师)')
add_bullet_para(doc, 'U5 Wild animals → 方法2(企鹅智慧学练可视化词汇)')
add_bullet_para(doc, 'U8 Natural disasters → 方法4(应急礼仪模拟)')

add_heading_custom(doc, '九年级（上册）', 3)
add_bullet_para(doc, 'U2 Colours → 方法11(跨文化对比)')
add_bullet_para(doc, 'U3 Teenage problems → 方法6(英语作文助手写作批改)')
add_bullet_para(doc, 'U6 TV programmes → 方法13(新闻辩论)')
add_bullet_para(doc, 'U7 Films → 方法12(影视剪辑)')
add_bullet_para(doc, 'U8 Detective stories → 方法8(创意写作)、方法14(故事接龙)')

doc.add_page_break()

# ===== 六、附录：提示词速查卡 =====
add_heading_custom(doc, '六、附录：译林版英语AI提示词速查卡', 1)
add_para_custom(doc, '以下六件套可直接复制，已适配译林版。配合"国家智慧中小学平台用AI应用 + 飞象老师"使用。', bold=True, indent=False)
add_para_custom(doc, '平台用AI一句话记：E听说练听说 → 飞象老师做互动游戏/动画 → 企鹅教师助手备课件 → 企鹅智慧学练做多模态创作 → 多智能体课堂做角色对话 → 英语作文助手改写作 → 全链路AI备课出教案 → 作业批改助手批量改 → 学科对话助手答疑问', bold=True, indent=False, color=RGBColor(0xc0, 0x00, 0x00))

add_prompt_box(doc, '1 写教案',
    '你是有10年经验的初中英语教师，请写【译林版+年级+单元】的【课型】教案，含目标/重难点/过程/板书/分层作业。（用"全链路AI备课"或"企鹅教师助手"生成）')
add_prompt_box(doc, '2 出分层作业',
    '请基于【年级+语法点】设计基础/提高/拓展三层作业，附答案。例：译林八上U1比较级。（用"全链路AI备课"智能出题或"题目推荐助手"）')
add_prompt_box(doc, '3 改作业',
    '请批改这张【年级】英语作业照片，指出错误、给修改建议和鼓励评语。（用"作业批改助手"或"英语作文助手"）')
add_prompt_box(doc, '4 做互动网页/游戏',
    '打开飞象老师，输入"为译林【年级+单元】生词做一个英语单词【消消乐/贪吃蛇/连连看】游戏"，生成后课堂直接打开，学生抢答计分。')
add_prompt_box(doc, '5 练口语',
    '请扮演【角色】，用简单英语和我对话，我每说错一句请温柔纠正。（用"E听说"或"多智能体课堂"）')
add_prompt_box(doc, '6 做教研',
    '请分析这份【年级】英语试卷，指出失分题型并给3条改进建议。（用"E听说"学情分析或"企鹅教师助手"）')

add_para_custom(doc, '新增两条（对应融合方法）', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))
add_prompt_box(doc, '7 跨文化对比',
    '请对比中西方对【色彩/节日】的文化含义，生成对比表+英文对话案例，用于译林【单元】。（用"多智能体课堂"或"企鹅教师助手"）')
add_prompt_box(doc, '8 学习路径',
    '基于译林【单元】话题，为我班学生生成一周英语学习路径与打卡表(背词/听力/错题)。（用"E听说"+"全链路AI备课"复习卡片）')

add_para_custom(doc, '【讲师备货清单】', bold=True, indent=False)
add_bullet_para(doc, '提前用国家智慧中小学账号登录，测试能打开：E听说、飞象老师、企鹅教师助手、企鹅智慧学练、多智能体课堂、希沃白板、英语作文助手、全链路AI备课、作业批改助手、学科对话助手')
add_bullet_para(doc, '准备1份真实学生英语作业照片、1份期中试卷+成绩表（备用）')
add_bullet_para(doc, '打印本速查卡每人1张；建好课后答疑群二维码')
add_bullet_para(doc, '准备1本译林版课本（七/八/九各一册演示用）')

# 保存
output_path = 'D:/projects/WorkBuddy/2026-06-17-11-18-20/AI赋能英语教学_译林版融合方案.docx'
doc.save(output_path)
print('文档已生成：' + output_path)
