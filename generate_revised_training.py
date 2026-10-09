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

# ==================== 创建文档 ====================
doc = Document()
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
style.font.size = Pt(10.5)
style.paragraph_format.line_spacing = 1.5

# ===== 封面 =====
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title.add_run('AI赋能教学：WorkBuddy实战工作坊')
set_run_font(title_run, size=22, bold=True, color=RGBColor(0x1a, 0x5f, 0x7a))

title2 = doc.add_paragraph()
title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
title2_run = title2.add_run('一线教师数字素养提升培训方案')
set_run_font(title2_run, size=18, bold=True, color=RGBColor(0x2e, 0x7d, 0x32))

doc.add_paragraph()
info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
info_run = info.add_run('培训时长：3-3.5小时\n培训对象：一线中小学教师\n培训形式：讲解+实操+互动')
set_run_font(info_run, size=12)

doc.add_page_break()

# ===== 一、培训概述 =====
add_heading_custom(doc, '一、培训概述', 1)

add_para_custom(doc, '【培训背景】', bold=True, indent=False)
add_para_custom(doc, '随着人工智能技术的快速发展，AI已从"遥远的概念"转变为教师日常工作的得力助手。2024年教育部发布《教师数字素养》标准，明确提出教师应具备利用人工智能技术优化教学的能力。多数一线教师对AI有基本认识，但停留在"对话问答"层面，对AI Agent（智能体）和Skill（技能）等进阶应用缺乏了解。本培训聚焦WorkBuddy这一AI工作伙伴，帮助教师掌握其在教学全流程中的实战应用，真正达到减负增效。')

add_para_custom(doc, '【培训目标】', bold=True, indent=False)
add_bullet_para(doc, '了解AI Agent与Skill的核心概念，建立"AI工具思维"')
add_bullet_para(doc, '熟练掌握WorkBuddy的基础操作与核心功能')
add_bullet_para(doc, '能够使用WorkBuddy完成成绩分析、试卷分析、教案生成、PPT制作等高频教学任务')
add_bullet_para(doc, '学会创建自定义Skill，实现个性化教学辅助')
add_bullet_para(doc, '了解IMA知识库的基本概念，作为资料管理的补充工具')
add_bullet_para(doc, '建立"AI不是替代而是赋能"的正确认知，减轻工作负担，提升教学效率')

add_para_custom(doc, '【培训特色】', bold=True, indent=False)
add_bullet_para(doc, '聚焦WorkBuddy：不分散精力，一个工具讲深讲透')
add_bullet_para(doc, '去理论化：不讲算法原理，只讲"打开WorkBuddy，输入什么，得到什么"')
add_bullet_para(doc, '强实操性：每个环节都有动手任务，带着成果离开')
add_bullet_para(doc, '问题导向：所有案例来自一线教师真实工作场景')
add_bullet_para(doc, '即时互动：二维码投票、AI点名、小组实操，避免单向灌输')

doc.add_page_break()

# ===== 二、培训流程总览 =====
add_heading_custom(doc, '二、培训流程总览', 1)

table = doc.add_table(rows=6, cols=5)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

headers = ['阶段', '时长', '主题', '核心内容', '产出成果']
for i, h in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            set_run_font(run, bold=True, color=RGBColor(0xff, 0xff, 0xff))
    fill_cell_color(cell, '1A5F7A')

rows_data = [
    ['第一阶段\n宏观视野', '30分钟', 'AI发展态势\n与政策要求', 'AI从对话到Agent的演进\n国家政策与教师数字素养标准\nWorkBuddy的定位', '建立认知框架'],
    ['第二阶段\n工具认知', '35分钟', 'Agent+Skill\n核心概念', 'Agent与Skill是什么\nWorkBuddy界面与功能\nIMA知识库简介', '工具操作基础'],
    ['第三阶段\n深度实操', '95分钟', 'WorkBuddy\n教学实战', '成绩智能分析\n五维试卷精析\nSkill创建与应用\n教案与PPT生成', '个人Skill作品\n实操成果包'],
    ['第四阶段\n综合应用', '30分钟', '教学场景\n整合应用', '备课流程重构\n作业批改辅助\n家校沟通\n个性化学习方案', '个人行动计划'],
    ['第五阶段\n总结提升', '20分钟', '总结与\n持续学习', '今日要点回顾\n回去就能用的3个技能\n学习资源推荐', '行动承诺']
]

for row_idx, row_data in enumerate(rows_data, start=1):
    for col_idx, text in enumerate(row_data):
        cell = table.rows[row_idx].cells[col_idx]
        cell.text = text
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.line_spacing = 1.3
            for run in para.runs:
                set_run_font(run, size=9)

for row in table.rows:
    row.cells[0].width = Inches(1.2)
    row.cells[1].width = Inches(1.0)
    row.cells[2].width = Inches(1.3)
    row.cells[3].width = Inches(2.5)
    row.cells[4].width = Inches(1.5)

doc.add_paragraph()
add_para_custom(doc, '总时长：约3.5小时（含休息）\n工具聚焦：WorkBuddy（主）+ IMA（辅，仅知识库介绍）', bold=True, indent=False, color=RGBColor(0xc0, 0x00, 0x00))

doc.add_page_break()

# ===== 三、详细培训内容 =====
add_heading_custom(doc, '三、详细培训内容', 1)

# ---------- 第一阶段 ----------
add_heading_custom(doc, '第一阶段：宏观视野（30分钟）', 2)

add_heading_custom(doc, '环节1：AI发展态势——从对话到Agent（15分钟）', 3)
add_para_custom(doc, '【互动开场】（3分钟）', bold=True, indent=False)
add_para_custom(doc, '屏幕投放二维码，教师扫码回答："你平时用AI做什么？"（多选：查资料/写教案/改作业/做PPT/其他）。实时展示投票结果，讲师据此调整讲解侧重点。')

add_para_custom(doc, '【核心内容】（10分钟）', bold=True, indent=False)
add_number_para(doc, 'AI发展的三个阶段：')
add_bullet_para(doc, '第一阶段（2022-2023）：对话时代——ChatGPT、Claude等，以"问答"为核心', level=1)
add_bullet_para(doc, '第二阶段（2024）：Agent时代——AI从"回答问题"到"完成任务"，能自主调用工具、执行多步骤操作', level=1)
add_bullet_para(doc, '第三阶段（2025-）：Skill生态——Agent通过学习Skill（技能）不断扩展能力，从通用走向专业', level=1)

add_number_para(doc, '什么是Agent？什么是Skill？（用教学场景比喻）')
add_bullet_para(doc, 'Agent = 一个聪明但空手的助手——有理解力、有判断力，但初期什么工具都不会用', level=1)
add_bullet_para(doc, 'Skill = 助手学会的具体技能——如"批改作文""分析试卷""生成PPT"，每个Skill就是一个专项能力', level=1)
add_bullet_para(doc, '关系：Agent + Skill = 一个既有脑子、又有手艺的完整助手', level=1)

add_number_para(doc, 'WorkBuddy的定位：')
add_bullet_para(doc, 'WorkBuddy是一款AI工作伙伴，核心定位是"帮你完成工作"', level=1)
add_bullet_para(doc, '与ChatGPT的区别：ChatGPT是"问答型"，WorkBuddy是"任务型"——你提出目标，它自动拆解步骤、调用工具、完成输出', level=1)
add_bullet_para(doc, '教育领域应用：备课、分析、批改、生成、管理——贯穿教学全流程', level=1)

add_para_custom(doc, '【教师收获】', bold=True, indent=False)
add_para_custom(doc, '建立"AI不只是聊天工具"的认知，理解WorkBuddy是专门为"完成工作"设计的工具，比普通对话AI更强大。')

add_heading_custom(doc, '环节2：国家政策与数字素养要求（15分钟）', 3)
add_para_custom(doc, '【核心内容】', bold=True, indent=False)
add_number_para(doc, '政策文件梳理：')
add_bullet_para(doc, '《教师数字素养》教育行业标准（2024）：明确将"人工智能应用"纳入教师数字素养框架', level=1)
add_bullet_para(doc, '教育部人工智能助推教师队伍建设试点：多省已开展AI+教师培训', level=1)
add_bullet_para(doc, '新课标对信息素养的要求：不仅学生要学，教师更要先行', level=1)

add_number_para(doc, '教师数字素养五维度与AI的对应关系：')
add_bullet_para(doc, '数字化意识 → 认识AI能做什么、不能做什么', level=1)
add_bullet_para(doc, '数字化知识 → 了解Agent、Skill、Prompt等基本概念', level=1)
add_bullet_para(doc, '数字化能力 → 能使用AI工具完成备课、批改、分析等任务', level=1)
add_bullet_para(doc, '数字化伦理 → 正确使用AI，避免学术不端、隐私泄露', level=1)
add_bullet_para(doc, '专业发展 → 持续学习新工具，更新教学方法', level=1)

add_number_para(doc, '对一线教师的实际意义：')
add_bullet_para(doc, '不是"增加负担"，而是"减轻负担"——AI处理重复性工作，教师聚焦创造性工作', level=1)
add_bullet_para(doc, '未来考核方向——数字素养将纳入教师能力评价', level=1)
add_bullet_para(doc, '学校信息化建设的趋势——越早掌握，越能成为校内的"AI种子教师"', level=1)

add_para_custom(doc, '【互动环节】（2分钟）', bold=True, indent=False)
add_para_custom(doc, 'AI点名：屏幕随机抽取3位教师，分享"你最希望AI帮你做什么教学工作"。')

doc.add_page_break()

# ---------- 第二阶段 ----------
add_heading_custom(doc, '第二阶段：工具认知（35分钟）', 2)

add_heading_custom(doc, '环节3：WorkBuddy界面与核心功能（20分钟）', 3)
add_para_custom(doc, '【核心内容】', bold=True, indent=False)
add_para_custom(doc, '手把手带教师认识WorkBuddy，熟悉每个区域的功能。')

add_para_custom(doc, '界面四大区域：', bold=True)
add_bullet_para(doc, '对话区（中间）：与AI交互的主界面，输入指令、查看回答、上传文件')
add_bullet_para(doc, 'Skill区（左侧/右侧）：查看已安装Skill、安装新Skill、创建自定义Skill')
add_bullet_para(doc, '文件区（底部）：上传文档、图片、表格等素材，支持批量上传')
add_bullet_para(doc, '设置区（右上角）：模型选择、参数调整、个人偏好、历史记录')

add_para_custom(doc, '核心功能演示（讲师同步操作，学员跟着看）：', bold=True)
add_bullet_para(doc, '基础对话：输入一个简单问题，观察AI如何回答')
add_bullet_para(doc, '文件上传：上传一份Word文档，让AI总结内容')
add_bullet_para(doc, 'Skill安装：从Skill市场安装一个教学相关Skill，演示使用方法')
add_bullet_para(doc, '历史记录：展示如何查看和继续之前的对话')

add_para_custom(doc, 'WorkBuddy与普通AI对话工具的关键区别：', bold=True)
add_bullet_para(doc, '任务执行：不只是"回答问题"，而是"完成整个任务流程"')
add_bullet_para(doc, '文件处理：支持上传Excel、Word、PDF、图片，AI直接读取分析')
add_bullet_para(doc, 'Skill扩展：通过安装和创建Skill，不断扩展能力边界')
add_bullet_para(doc, '结果导出：分析结果可直接导出为Word、PDF、Markdown等格式')

add_heading_custom(doc, '环节4：Agent与Skill深度理解（10分钟）', 3)
add_para_custom(doc, '【核心内容】', bold=True, indent=False)
add_para_custom(doc, '用教学场景比喻，帮助教师建立直觉理解。')

add_para_custom(doc, 'Agent的本质：', bold=True)
add_bullet_para(doc, 'Agent = 一个能"理解任务→拆解步骤→调用工具→执行完成→反馈结果"的闭环系统')
add_bullet_para(doc, '与"简单对话"的区别：对话是"你说一句，我答一句"；Agent是"你说目标，我全程搞定"')
add_bullet_para(doc, '例子：你说"帮我分析这次期中考试的薄弱点"，Agent会自动：读取成绩表→统计分析→生成图表→给出教学建议→输出报告')

add_para_custom(doc, 'Skill的本质：', bold=True)
add_bullet_para(doc, 'Skill = 一个封装好的"能力包"，包含：做什么（目标）+ 怎么做（步骤）+ 用什么工具（资源）')
add_bullet_para(doc, '类比：Skill就像教师的"教学设计模板"——新手教师用模板能快速出课，Agent用Skill能快速完成专项任务')
add_bullet_para(doc, 'Skill的来源：官方提供、社区共享、自己创建')

add_para_custom(doc, 'Agent + Skill 的工作模式：', bold=True)
add_bullet_para(doc, '教师提出需求 → Agent理解意图 → 匹配合适Skill → 执行并返回结果 → 教师审核调整')
add_bullet_para(doc, '关键：教师依然是"决策者"，Agent是"执行者"，Skill是"专业能力库"')

add_heading_custom(doc, '环节5：IMA知识库简介（5分钟）', 3)
add_para_custom(doc, '【简要介绍】', bold=True, indent=False)
add_para_custom(doc, 'IMA是腾讯推出的知识库管理工具，核心定位是"帮你管理资料"。本培训不做深入讲解，仅做概念介绍，让教师了解有这样一个工具可以辅助资料管理。')

add_bullet_para(doc, 'IMA是什么：一个智能化的个人/团队知识库，可以存储、分类、检索教学资料')
add_bullet_para(doc, '核心功能：上传文档→智能分类→标签管理→问答检索→版本追踪')
add_bullet_para(doc, '与WorkBuddy的关系：IMA管资料，WorkBuddy用资料做事——两者可配合使用')
add_bullet_para(doc, '什么时候用IMA：资料太多找不到时、需要跨文档查找信息时、团队协作共享资源时')
add_bullet_para(doc, '建议：先学好WorkBuddy，有余力再探索IMA')

doc.add_page_break()

# ---------- 第三阶段（核心，WorkBuddy实战） ----------
add_heading_custom(doc, '第三阶段：WorkBuddy深度实操（95分钟）', 2)
add_para_custom(doc, '本阶段是培训核心，教师带着电脑，跟随讲师一步步操作，每个环节都有明确的产出物。全部围绕WorkBuddy展开。')

add_heading_custom(doc, '环节6：成绩智能分析（20分钟）', 3)
add_para_custom(doc, '【实操目标】', bold=True, indent=False)
add_para_custom(doc, '使用WorkBuddy完成一份成绩表的智能分析，生成包含统计、预警、建议的完整报告。')

add_para_custom(doc, '【工作痛点】', bold=True, indent=False)
add_para_custom(doc, '期中考试后，班主任需要统计班级均分、排名、分数段分布、找出薄弱题目、识别偏科学生。Excel操作不熟练的教师，光是拉透视表就要折腾半天。')

add_para_custom(doc, '【操作步骤】（讲师同步演示，学员跟着操作）', bold=True)
add_bullet_para(doc, '准备材料：提供一份样例成绩表（Excel，含学生姓名、各题得分、总分），或学员上传自己班级的成绩表')
add_bullet_para(doc, '上传文件：在WorkBuddy中点击"上传"，选择Excel成绩表')
add_bullet_para(doc, '输入分析指令：复制以下Prompt到对话框')
add_prompt_box(doc, '成绩分析Prompt',
    '请对上传的成绩表进行智能分析：\n1. 基础统计：班级均分、最高分、最低分、标准差、分数段人数分布（优秀90+/良好80-89/及格60-79/不及格60以下）\n2. 题目分析：各题得分率，标注低于60%的预警题目，分析错因推测\n3. 学生个体：识别前10%和后10%学生，分析偏科情况\n4. 教学建议：基于数据，给出3条具体可行的教学改进建议\n输出格式：先表格后文字，表格清晰对齐。')
add_bullet_para(doc, '查看AI输出：观察WorkBuddy如何生成结构化报告')
add_bullet_para(doc, '追问优化：如"请把预警题目按错误率从高到低排序""请给我一份需要重点关注的学生名单"')
add_bullet_para(doc, '导出保存：点击导出按钮，保存为Word/PDF格式')

add_para_custom(doc, '【时间对比】', bold=True, indent=False)
add_para_custom(doc, '传统方式：2小时（Excel操作+人工分析）→ WorkBuddy：10分钟，效率提升12倍', bold=True, color=RGBColor(0x2e, 0x7d, 0x32))

add_para_custom(doc, '【进阶玩法】', bold=True, indent=False)
add_bullet_para(doc, '上传两次考试成绩，让AI对比分析进步/退步学生')
add_bullet_para(doc, '上传多学科成绩，让AI分析偏科情况和综合排名')
add_bullet_para(doc, '让AI生成"家长通知"草稿：基于成绩分析，自动生成给家长的通知文字')

add_heading_custom(doc, '环节7：五维试卷精析（25分钟）', 3)
add_para_custom(doc, '【实操目标】', bold=True, indent=False)
add_para_custom(doc, '使用WorkBuddy完成一套试卷的五维度深度分析，生成可用于教研会议的专业报告。')

add_para_custom(doc, '【五维分析框架】', bold=True)
add_bullet_para(doc, '维度1：知识点覆盖——各章节/考点占比是否合理')
add_bullet_para(doc, '维度2：难度梯度——易中难比例是否符合教学阶段')
add_bullet_para(doc, '维度3：能力层级——记忆/理解/应用/分析/评价/创造的分布')
add_bullet_para(doc, '维度4：题型结构——选择/填空/解答/实验等比例')
add_bullet_para(doc, '维度5：信效度指标——区分度、预测效度等基础分析')

add_para_custom(doc, '【操作步骤】', bold=True)
add_bullet_para(doc, '准备材料：提供一份样卷（Word/PDF），或学员上传自己学校的试卷')
add_bullet_para(doc, '上传试卷：将试卷文件上传至WorkBuddy')
add_bullet_para(doc, '输入分析指令：')
add_prompt_box(doc, '五维试卷分析Prompt',
    '请对上传的试卷进行五维度深度分析：\n\n维度1：知识点覆盖——统计各章节/考点占比，判断是否合理，生成知识结构描述\n维度2：难度梯度——标注每道题难度（易/中/难），统计比例，判断是否符合当前教学阶段\n维度3：能力层级——按布鲁姆目标分类，标注每道题对应层级（记忆/理解/应用/分析/评价/创造）\n维度4：题型结构——统计各题型数量和分值占比\n维度5：质量评价——判断是否有偏题、怪题、重复题，给出整体信度评估\n\n输出要求：\n- 每个维度给出分析结论和改进建议\n- 用文本形式呈现数据表格（如饼图/柱状图的文字描述）\n- 总结3条最重要的改进建议\n- 输出为可直接用于教研报告的结构化文本')
add_bullet_para(doc, '结果优化：根据AI输出，教师补充人工判断，修正偏差（如某道题实际比AI判断的更难）')
add_bullet_para(doc, '导出保存：将分析报告导出为Word/PDF，存档备查')

add_para_custom(doc, '【产出物】', bold=True, indent=False)
add_para_custom(doc, '一份完整的五维试题分析报告，教师可直接用于教研会议或教学改进。')

add_para_custom(doc, '【互动环节】（5分钟）', bold=True, indent=False)
add_para_custom(doc, '小组讨论：3-4人一组，分享各自的分析结果，讨论"这份试卷最大的问题是什么"。每组推选1人汇报。')

add_heading_custom(doc, '环节8：创建自定义Skill——教学评一致性检查器（25分钟）', 3)
add_para_custom(doc, '【实操目标】', bold=True, indent=False)
add_para_custom(doc, '学会创建第一个个人Skill，理解Skill的核心价值：一次创建，永久复用。')

add_para_custom(doc, '【为什么需要创建Skill？】', bold=True, indent=False)
add_bullet_para(doc, '通用AI回答不够精准——每次都要重新描述需求')
add_bullet_para(doc, 'Skill把"需求描述"固化下来，下次直接调用')
add_bullet_para(doc, '可以分享给同事，形成校内Skill库')

add_para_custom(doc, '【操作步骤】', bold=True)
add_bullet_para(doc, '点击"创建Skill"按钮（通常在左侧Skill栏）')
add_bullet_para(doc, '填写基础信息：')
add_bullet_para(doc, 'Skill名称：教学评一致性检查器', level=1)
add_bullet_para(doc, '描述：输入教学目标和教学活动，自动检查两者是否匹配', level=1)
add_bullet_para(doc, '编写Prompt（核心步骤，讲师详细讲解）：')
add_prompt_box(doc, 'Skill Prompt模板',
    '你是一个教学评一致性检查专家。请分析以下教学目标与教学活动是否匹配：\n\n教学目标：{{目标}}\n教学活动：{{活动}}\n\n检查维度：\n1. 目标与活动对应性：活动是否直接服务于目标达成？\n2. 活动可评价性：活动完成后，能否判断目标是否达成？\n3. 评价方式明确性：是否有清晰的评价标准和方式？\n\n输出格式：\n- 表格呈现三维度检查结果（符合/部分符合/不符合）\n- 文字给出具体改进建议（200字以内）\n- 给出修改后的活动建议（可选）\n\n注意：客观分析，不夸大优点，也不刻意找茬。')
add_bullet_para(doc, '设置变量：用{{变量名}}标记需要用户填写的内容（如{{目标}}、{{活动}}），运行时系统会自动提示输入')
add_bullet_para(doc, '测试Skill：输入一段真实教案，观察AI输出质量')
add_bullet_para(doc, '调试优化：如果输出不满意，修改Prompt，重新测试')
add_bullet_para(doc, '保存命名："XX老师_教学评一致性检查器"')

add_para_custom(doc, '【产出物】', bold=True, indent=False)
add_para_custom(doc, '每位教师拥有一个可立即使用的个人Skill，能辅助日常备课质量检查。')

add_para_custom(doc, '【进阶Skill创意】（讲师提供思路，学员课后尝试）', bold=True, indent=False)
add_bullet_para(doc, '分层作业生成器：输入知识点，自动生成A/B/C三层作业')
add_bullet_para(doc, '课堂互动设计器：输入课题，自动设计3个互动环节')
add_bullet_para(doc, '家长会发言稿生成器：输入班级情况，自动生成发言稿')
add_bullet_para(doc, '错题归因分析器：输入学生错题，分析错误类型和补救建议')

add_heading_custom(doc, '环节9：教案与PPT快速生成（25分钟）', 3)
add_para_custom(doc, '【实操目标】', bold=True, indent=False)
add_para_custom(doc, '使用WorkBuddy完成教案生成和PPT大纲制作两个高频任务。')

add_para_custom(doc, '【任务1】快速生成教学教案（15分钟）', bold=True)
add_bullet_para(doc, '输入：')
add_prompt_box(doc, '教案生成Prompt',
    '请为《{课题名称}》生成一份完整教案。\n\n课程信息：\n- 学科：{学科}\n- 年级：{年级}\n- 课时：{时长}分钟\n- 课型：{新授课/复习课/实验课等}\n\n教案要求：\n1. 教学目标：三维目标（知识与技能/过程与方法/情感态度与价值观）\n2. 教学重难点：重点1个，难点1-2个\n3. 教学过程：\n   - 导入（3-5分钟）：设计1个引起兴趣的情境或问题\n   - 新授（15-20分钟）：分2-3个知识点，每个含讲解要点和互动设计\n   - 练习（10分钟）：分层练习题，基础题+提高题\n   - 小结（3-5分钟）：知识梳理+学生总结\n   - 作业：分层作业设计（A/B/C三层）\n4. 板书设计：主板书+副板书\n5. 教学反思：预设可能出现的问题及应对策略\n\n输出格式：结构化文本，可直接复制到Word教案模板。')
add_bullet_para(doc, 'AI输出：完整教案 → 教师审核修改 → 导出为Word')
add_bullet_para(doc, '技巧：如果某部分不满意，可以追问"请把导入环节改得更生动一些""请增加一个实验演示环节"')

add_para_custom(doc, '【任务2】PPT大纲快速生成（10分钟）', bold=True)
add_bullet_para(doc, '输入：')
add_prompt_box(doc, 'PPT大纲生成Prompt',
    '请为《{课题名称}》生成教学PPT大纲。\n\n课程信息：\n- 学科：{学科}\n- 年级：{年级}\n- 课时：{时长}分钟\n- 课型：{新授课/复习课/实验课等}\n\n大纲要求：\n1. 导入环节（1-2页PPT）：设计1个引起兴趣的情境或问题\n2. 新授环节（5-8页PPT）：分2-3个知识点，每页含标题、内容要点、设计意图\n3. 练习环节（2-3页PPT）：分层练习题展示\n4. 小结环节（1页PPT）：知识梳理框架\n5. 作业布置（1页PPT）：分层作业展示\n\n每页PPT标注：\n- 标题\n- 内容要点（ bullet points ）\n- 设计意图（为什么这样设计）\n- 需要的图片/视频素材建议\n- 互动环节的教师行为\n\n输出格式：结构化大纲，每页PPT独立成段。')
add_bullet_para(doc, 'AI输出结构化大纲 → 教师审核调整 → 复制到PPT软件制作')
add_bullet_para(doc, '进阶：如果WorkBuddy支持直接生成PPT文件，可演示一键导出功能')

add_para_custom(doc, '【时间对比】', bold=True, indent=False)
add_para_custom(doc, '传统方式：教案2小时+PPT 1.5小时 = 3.5小时 → WorkBuddy辅助：教案15分钟+PPT 10分钟 = 25分钟，效率提升8倍', bold=True, color=RGBColor(0x2e, 0x7d, 0x32))

doc.add_page_break()

# ---------- 第四阶段 ----------
add_heading_custom(doc, '第四阶段：综合应用与总结（30分钟）', 2)

add_heading_custom(doc, '环节10：WorkBuddy教学场景整合应用（20分钟）', 3)
add_para_custom(doc, '【核心内容】', bold=True, indent=False)
add_para_custom(doc, '将前面学到的工具和方法，整合为一线教师日常工作的完整解决方案。全部基于WorkBuddy。')

add_para_custom(doc, '场景1：备课流程重构（用WorkBuddy完成）', bold=True)
add_bullet_para(doc, '传统流程：找资料 → 写教案 → 做课件 → 准备习题 → 手写板书设计（2-3小时）')
add_bullet_para(doc, 'AI辅助流程：')
add_bullet_para(doc, '打开WorkBuddy，输入课题名称和基本信息（2分钟）', level=1)
add_bullet_para(doc, '生成教案框架（5分钟）', level=1)
add_bullet_para(doc, '生成PPT大纲（5分钟）', level=1)
add_bullet_para(doc, '生成分层练习题（5分钟）', level=1)
add_bullet_para(doc, '教师审核修改（15分钟）', level=1)
add_bullet_para(doc, '总耗时：约30-40分钟，效率提升4-5倍')

add_para_custom(doc, '场景2：作业批改辅助（用WorkBuddy完成）', bold=True)
add_bullet_para(doc, '上传学生作文/解答照片或文档，AI自动标注错误、给出评语模板')
add_bullet_para(doc, '教师只需审核AI批改结果，重点处理疑难个案')
add_bullet_para(doc, '效果：作文批改时间从30分钟/班降至10分钟/班')

add_para_custom(doc, '场景3：家校沟通模板（用WorkBuddy完成）', bold=True)
add_bullet_para(doc, '输入学生表现数据，AI生成不同风格（鼓励型/提醒型/详细型）的沟通文本')
add_bullet_para(doc, '教师选择并微调，直接发送给家长')

add_para_custom(doc, '场景4：个性化学习方案（用WorkBuddy完成）', bold=True)
add_bullet_para(doc, '输入学生错题记录和成绩分析，AI生成针对性补弱方案')
add_bullet_para(doc, '包含：薄弱知识点清单 → 推荐练习 → 学习计划 → 阶段目标')

add_para_custom(doc, '【互动环节】', bold=True, indent=False)
add_para_custom(doc, 'AI点名：抽取3位教师，分享"回去后最想立刻尝试的一个场景"。')

add_heading_custom(doc, '环节11：总结与行动计划（10分钟）', 3)
add_para_custom(doc, '【今日要点回顾】', bold=True, indent=False)
add_bullet_para(doc, 'WorkBuddy是"能完成任务的助手"，不只是"聊天工具"')
add_bullet_para(doc, 'Skill是"助手的能力包"，创建一次，永久复用')
add_bullet_para(doc, '教师的核心价值是"决策和设计"，AI负责"执行和重复劳动"')
add_bullet_para(doc, '先掌握WorkBuddy的核心功能，有余力再探索IMA知识库')

add_para_custom(doc, '【回去就能用的3个技能】', bold=True, indent=False)
add_bullet_para(doc, '技能1：用WorkBuddy分析下次考试成绩（省2小时）')
add_bullet_para(doc, '技能2：用WorkBuddy生成下周教案框架（省1.5小时）')
add_bullet_para(doc, '技能3：创建1个个人Skill，解决最高频的重复性任务')

add_para_custom(doc, '【持续学习资源】', bold=True, indent=False)
add_bullet_para(doc, 'WorkBuddy官方Skill市场：持续更新的教学Skill')
add_bullet_para(doc, '教师AI应用交流群：校内/区内的实践分享社群')
add_bullet_para(doc, '每月尝试1个新功能：积少成多，持续迭代')
add_bullet_para(doc, 'IMA知识库：当资料管理需求出现时，可作为进阶工具学习')

add_para_custom(doc, '【行动计划填写】', bold=True, indent=False)
add_para_custom(doc, '发放纸质/电子版《AI教学应用行动计划表》，教师填写：')
add_bullet_para(doc, '本学期我要用WorkBuddy完成的3项工作')
add_bullet_para(doc, '我准备创建的1-2个个人Skill')
add_bullet_para(doc, '预计能节省的时间和提升的效果')
add_bullet_para(doc, '需要同事或技术支持的环节')

doc.add_page_break()

# ===== 四、培训配套材料 =====
add_heading_custom(doc, '四、培训配套材料', 1)

add_heading_custom(doc, '讲师准备材料', 2)
add_bullet_para(doc, '演示用电脑：已安装WorkBuddy，登录好账号')
add_bullet_para(doc, '样例文件包：样卷（Word/PDF）、成绩表（Excel）、教案模板（Word）')
add_bullet_para(doc, 'PPT课件：本次培训的理论部分PPT（学员视角设计）')
add_bullet_para(doc, '二维码物料：互动投票、问卷、资源下载等二维码')
add_bullet_para(doc, '网络环境：确保培训场地WiFi稳定')
add_bullet_para(doc, '备用方案：如网络故障，准备离线录屏视频')

add_heading_custom(doc, '学员准备材料', 2)
add_bullet_para(doc, '笔记本电脑：能联网，建议提前注册WorkBuddy账号')
add_bullet_para(doc, '个人教学资料：1份近期教案、1份试卷或成绩表（用于实操）')
add_bullet_para(doc, '笔记本：记录关键操作步骤和个人心得')
add_bullet_para(doc, '《AI教学应用行动计划表》：培训结束时填写')

add_heading_custom(doc, '发放资料清单', 2)
add_bullet_para(doc, '《WorkBuddy快速上手指南》（1页A4纸）')
add_bullet_para(doc, '《10个教学实用Prompt模板》（可直接复制使用）')
add_bullet_para(doc, '《Agent+Skill概念图解》（1页可视化说明）')
add_bullet_para(doc, '《IMA知识库简介》（1页简要介绍）')
add_bullet_para(doc, '《AI教学应用行动计划表》（电子版+纸质版）')

doc.add_page_break()

# ===== 五、互动设计详解 =====
add_heading_custom(doc, '五、互动设计详解', 1)

add_para_custom(doc, '【二维码互动】', bold=True, indent=False)
add_bullet_para(doc, '适用环节：开场调研、工具选择投票、满意度反馈')
add_bullet_para(doc, '工具推荐：腾讯问卷、问卷星')
add_bullet_para(doc, '操作要点：提前生成二维码，大屏幕展示，实时刷新结果')

add_para_custom(doc, '【AI点名】', bold=True, indent=False)
add_bullet_para(doc, '适用环节：过渡环节、小组汇报人选')
add_bullet_para(doc, '实现方式：WorkBuddy随机抽取学员名单')
add_bullet_para(doc, '效果：增加趣味性，给内向教师参与机会')

add_para_custom(doc, '【小组实操】', bold=True, indent=False)
add_bullet_para(doc, '分组方式：4-5人一组，尽量同年级或同学科')
add_bullet_para(doc, '角色分工：组长（协调）、记录员（记录问题）、汇报员（展示成果）、技术支持（帮助操作困难者）')
add_bullet_para(doc, '讲师角色：巡回指导，重点帮助操作困难者')

add_para_custom(doc, '【成果展示】', bold=True, indent=False)
add_bullet_para(doc, '每组推选1个最佳Skill或分析成果')
add_bullet_para(doc, '屏幕投影展示，讲师点评亮点')
add_bullet_para(doc, '优秀成果可纳入学校共享资源库')

doc.add_page_break()

# ===== 六、时间控制建议 =====
add_heading_custom(doc, '六、时间控制建议', 1)

add_para_custom(doc, '【弹性调整原则】', bold=True, indent=False)
add_bullet_para(doc, '如学员基础较好：压缩第一、二阶段至40分钟，增加实操时间')
add_bullet_para(doc, '如学员基础较弱：延长第二阶段，确保WorkBuddy基本操作熟练')
add_bullet_para(doc, '如网络不稳定：提前准备离线录屏')
add_bullet_para(doc, '如时间紧张：优先保证环节6（成绩分析）、环节7（试卷分析）、环节8（Skill创建）')

add_para_custom(doc, '【关键时间节点】', bold=True, indent=False)
table3 = doc.add_table(rows=6, cols=3)
table3.style = 'Table Grid'
table3.alignment = WD_TABLE_ALIGNMENT.CENTER

headers3 = ['时间节点', '应完成环节', '提醒事项']
for i, h in enumerate(headers3):
    cell = table3.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            set_run_font(run, bold=True, color=RGBColor(0xff, 0xff, 0xff))
    fill_cell_color(cell, '1A5F7A')

rows3_data = [
    ['开始后30分钟', '完成第一阶段', '确保所有学员理解Agent+Skill概念'],
    ['开始后65分钟', '完成第二阶段', '确认学员已熟悉WorkBuddy界面'],
    ['开始后85分钟', '完成环节6', '每人完成1份成绩分析'],
    ['开始后110分钟', '完成环节7', '每人完成1份试卷分析'],
    ['结束前40分钟', '完成环节8', '每人至少创建1个Skill']
]

for row_idx, row_data in enumerate(rows3_data, start=1):
    for col_idx, text in enumerate(row_data):
        cell = table3.rows[row_idx].cells[col_idx]
        cell.text = text
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.line_spacing = 1.3
            for run in para.runs:
                set_run_font(run, size=9)

for row in table3.rows:
    row.cells[0].width = Inches(1.5)
    row.cells[1].width = Inches(2.5)
    row.cells[2].width = Inches(2.5)

doc.add_page_break()

# ===== 七、讲师注意事项 =====
add_heading_custom(doc, '七、讲师注意事项', 1)

add_bullet_para(doc, '语言风格：避免技术术语，多用教学场景比喻。如不用"API调用"，而用"让AI用某个工具"；不用"Prompt工程"，而用"怎么跟AI说话最有效"。')
add_bullet_para(doc, '聚焦WorkBuddy：反复强调本次培训的核心是WorkBuddy，IMA只是补充介绍，避免学员精力分散。')
add_bullet_para(doc, '心态引导：反复强调"AI不会取代教师，但会用AI的教师会取代不会用的"。打消抵触情绪。')
add_bullet_para(doc, '差异化指导：关注操作困难的教师，安排技术骨干学员协助，避免"跟不上"的挫败感。')
add_bullet_para(doc, '成果可视化：让教师带着"作品"离开（自己的Skill、分析报告、教案大纲），增强成就感。')
add_bullet_para(doc, '后续跟进：培训结束后1周，线上收集使用问题；1个月后，组织线上分享会。')

doc.add_page_break()

# ===== 八、附录：实用Prompt模板 =====
add_heading_custom(doc, '八、附录：实用Prompt模板', 1)
add_para_custom(doc, '以下模板可直接复制到WorkBuddy中使用：', bold=True, indent=False)

add_prompt_box