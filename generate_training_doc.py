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
    from docx.oxml import parse_xml
    xml_str = '<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fill="' + hex_color + '"/>'
    shading = parse_xml(xml_str)
    cell._tc.get_or_add_tcPr().append(shading)

# 创建文档
doc = Document()

# 设置默认中文字体
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
style.font.size = Pt(10.5)
style.paragraph_format.line_spacing = 1.5

# ===== 封面 =====
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title.add_run('AI赋能教学：从认知到实践')
set_run_font(title_run, size=22, bold=True, color=RGBColor(0x1a, 0x5f, 0x7a))

title2 = doc.add_paragraph()
title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
title2_run = title2.add_run('一线教师数字素养提升工作坊')
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
add_para_custom(doc, '随着人工智能技术的快速发展，AI已从"遥远的概念"转变为教师日常工作的得力助手。2024年教育部发布《教师数字素养》标准，明确提出教师应具备利用人工智能技术优化教学的能力。然而，多数一线教师虽然对AI有基本认识，但停留在"对话问答"层面，对AI Agent（智能体）和Skill（技能）等进阶应用缺乏了解，更未能将其系统性地融入教学全流程。')

add_para_custom(doc, '【培训目标】', bold=True, indent=False)
add_bullet_para(doc, '了解AI Agent与Skill的核心概念及发展趋势，建立"AI工具思维"')
add_bullet_para(doc, '掌握WorkBuddy、IMA等主流工具的基础操作与高级功能')
add_bullet_para(doc, '能够独立创建简单Skill，实现个性化教学辅助')
add_bullet_para(doc, '学会将AI工具应用于备课、试题分析、成绩分析、PPT生成等实际教学场景')
add_bullet_para(doc, '建立"AI不是替代而是赋能"的正确认知，减轻工作负担，提升教学效率')

add_para_custom(doc, '【培训特色】', bold=True, indent=False)
add_bullet_para(doc, '去理论化：不讲算法原理，只讲"用什么工具做什么事"')
add_bullet_para(doc, '强实操性：每个环节都有动手任务，带着成果离开')
add_bullet_para(doc, '问题导向：所有案例均来自一线教师真实工作场景')
add_bullet_para(doc, '即时互动：二维码投票、AI点名、小组实操，避免单向灌输')

doc.add_page_break()

# ===== 二、培训流程总览 =====
add_heading_custom(doc, '二、培训流程总览', 1)

# 创建总览表格
table = doc.add_table(rows=6, cols=5)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

# 表头
headers = ['阶段', '时长', '主题', '核心内容', '产出成果']
for i, h in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            set_run_font(run, bold=True, color=RGBColor(0xff, 0xff, 0xff))
    fill_cell_color(cell, '1A5F7A')

# 表格数据
rows_data = [
    ['第一阶段\n宏观视野', '30分钟', 'AI发展态势\n与政策要求', 'AI从对话到Agent的演进\n国家政策与教师数字素养标准', '建立认知框架'],
    ['第二阶段\n工具认知', '40分钟', 'Agent+Skill\n工具概览', '核心概念解析\nWorkBuddy vs IMA对比\n常用工具适用场景', '工具选择清单'],
    ['第三阶段\n深度实操', '90分钟', 'WorkBuddy\n+IMA实战', '创建自定义Skill\n教学评一致性设计\n五维试题精析\nPPT生成与成绩分析', '个人Skill作品\n实操成果包'],
    ['第四阶段\n综合应用', '30分钟', '教学场景\n整合应用', '备课流程重构\n作业批改辅助\n家校沟通模板\n个性化学习方案', '个人行动计划'],
    ['第五阶段\n总结提升', '20分钟', '总结与\n持续学习', '今日要点回顾\n回去就能用的3个工具\n学习资源推荐', '行动承诺']
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

# 设置列宽
for row in table.rows:
    row.cells[0].width = Inches(1.2)
    row.cells[1].width = Inches(1.0)
    row.cells[2].width = Inches(1.3)
    row.cells[3].width = Inches(2.5)
    row.cells[4].width = Inches(1.5)

doc.add_paragraph()
add_para_custom(doc, '总时长：约3.5小时（含休息）', bold=True, indent=False, color=RGBColor(0xc0, 0x00, 0x00))

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

add_number_para(doc, '什么是Agent？什么是Skill？（用比喻解释）')
add_bullet_para(doc, 'Agent = 一个聪明但空手的助手——有理解力、有判断力，但初期什么工具都不会用', level=1)
add_bullet_para(doc, 'Skill = 助手学会的具体技能——如"批改作文""分析试卷""生成PPT"，每个Skill就是一个专项能力', level=1)
add_bullet_para(doc, '关系：Agent + Skill = 一个既有脑子、又有手艺的完整助手', level=1)

add_number_para(doc, '教育领域的AI趋势：')
add_bullet_para(doc, '从"用AI查资料"到"用AI完成整个教学环节"', level=1)
add_bullet_para(doc, '从"一个人用"到"全校共享Skill库"', level=1)
add_bullet_para(doc, '从"通用AI"到"学科专用AI"（如数学解题Agent、语文批改Agent）', level=1)

add_para_custom(doc, '【教师收获】', bold=True, indent=False)
add_para_custom(doc, '建立"AI不只是聊天工具"的认知，理解Agent+Skill是接下来必须跟上的趋势。')

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
add_heading_custom(doc, '第二阶段：工具认知（40分钟）', 2)

add_heading_custom(doc, '环节3：常用AI工具概览——用对工具做对事（15分钟）', 3)
add_para_custom(doc, '【核心内容】', bold=True, indent=False)
add_para_custom(doc, '以一张对比表格，快速帮助教师建立"工具-场景"匹配意识，避免"什么工具都想试"的混乱。')

add_para_custom(doc, '工具分类与适用场景：', bold=True)
add_bullet_para(doc, '通用对话类：ChatGPT、Claude、文心一言、通义千问——适合：开放性问答、创意激发、文本润色')
add_bullet_para(doc, '智能助手类：WorkBuddy、IMA、豆包、讯飞星火——适合：深度工作辅助、流程自动化、知识管理')
add_bullet_para(doc, '垂直工具类：学科专用AI、批改工具、出题工具——适合：特定教学任务')
add_bullet_para(doc, '办公集成类：WPS AI、Office Copilot——适合：文档处理、表格分析、PPT生成')

add_para_custom(doc, '教师选择工具的原则：', bold=True)
add_bullet_para(doc, '先明确"我要做什么"，再选"什么工具最擅长"')
add_bullet_para(doc, '不要追求"全会"，先掌握1-2个主力工具用到熟练')
add_bullet_para(doc, '关注工具的持续更新——今天好用的功能，明天可能更好')

add_heading_custom(doc, '环节4：深度理解Agent与Skill（15分钟）', 3)
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

add_heading_custom(doc, '环节5：WorkBuddy vs IMA——有什么区别？（10分钟）', 3)
add_para_custom(doc, '【核心内容】', bold=True, indent=False)
add_para_custom(doc, '这是教师最容易混淆的问题，需要清晰对比。')

# WorkBuddy vs IMA 对比表格
table2 = doc.add_table(rows=7, cols=3)
table2.style = 'Table Grid'
table2.alignment = WD_TABLE_ALIGNMENT.CENTER

headers2 = ['对比维度', 'WorkBuddy', 'IMA（ima.copilot）']
for i, h in enumerate(headers2):
    cell = table2.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            set_run_font(run, bold=True, color=RGBColor(0xff, 0xff, 0xff))
    fill_cell_color(cell, '2E7D32')

rows2_data = [
    ['定位', 'AI工作伙伴\n（聚焦"做事"）', '腾讯知识库助手\n（聚焦"管知识"）'],
    ['核心功能', '多Agent协作、Skill创建、\n自动化任务流、代码执行', '知识库管理、文档智能问答、\n笔记整理、跨文档检索'],
    ['最适合', '需要AI帮你"完成工作"\n如：备课、分析、生成、编程', '需要AI帮你"管理知识"\n如：资料整理、快速查找、知识沉淀'],
    ['Skill生态', '强大的Skill市场，\n可自定义创建Skill', '以知识库为核心，\n通过插件扩展能力'],
    ['使用场景', '教学全流程自动化、\n数据分析、PPT生成', '教学资料管理、\n校本资源库建设'],
    ['关系', '两者可以配合使用：\nIMA管知识 → WorkBuddy用知识做事', '']
]

for row_idx, row_data in enumerate(rows2_data, start=1):
    for col_idx, text in enumerate(row_data):
        cell = table2.rows[row_idx].cells[col_idx]
        cell.text = text
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.line_spacing = 1.3
            for run in para.runs:
                set_run_font(run, size=9)

for row in table2.rows:
    row.cells[0].width = Inches(1.3)
    row.cells[1].width = Inches(2.5)
    row.cells[2].width = Inches(2.5)

add_para_custom(doc, '【一句话总结】', bold=True, indent=False)
add_para_custom(doc, 'WorkBuddy是"帮你干活的助手"，IMA是"帮你管资料的助手"。两者配合：IMA把教学资料整理好，WorkBuddy用这些资料生成教案、分析试卷、回答问题。')

add_para_custom(doc, '【互动环节】（3分钟）', bold=True, indent=False)
add_para_custom(doc, '屏幕投放二维码："根据今天的介绍，你更想先深入学哪个工具？"（WorkBuddy / IMA / 两个都想）实时展示结果，为后续实操环节做分组参考。')

doc.add_page_break()

# ---------- 第三阶段 ----------
add_heading_custom(doc, '第三阶段：深度实操（90分钟）', 2)
add_para_custom(doc, '本阶段是培训核心，教师带着电脑，跟随讲师一步步操作，每个环节都有明确的产出物。')

add_heading_custom(doc, '环节6：WorkBuddy基础操作与Skill创建（30分钟）', 3)
add_para_custom(doc, '【实操目标】', bold=True, indent=False)
add_para_custom(doc, '学会WorkBuddy基础界面操作，创建第一个个人Skill。')

add_para_custom(doc, '【步骤1】认识WorkBuddy界面（5分钟）', bold=True)
add_bullet_para(doc, '对话区：与AI交互的主界面')
add_bullet_para(doc, 'Skill区：查看已安装Skill、安装新Skill、创建自定义Skill')
add_bullet_para(doc, '文件区：上传文档、图片、表格等素材')
add_bullet_para(doc, '设置区：模型选择、参数调整、个人偏好')

add_para_custom(doc, '【步骤2】创建第一个Skill："教学评一致性检查器"（20分钟）', bold=True)
add_bullet_para(doc, '任务说明：创建一个Skill，输入教学目标和教学活动，AI自动检查两者是否一致。')
add_bullet_para(doc, '操作步骤：')
add_bullet_para(doc, '点击"创建Skill" → 填写Skill名称和描述', level=1)
add_bullet_para(doc, '编写Prompt（提示词）：告诉AI要做什么、按什么步骤、输出什么格式', level=1)
add_bullet_para(doc, '示例Prompt模板：', level=1)
add_bullet_para(doc, '"你是一个教学评一致性检查专家。请分析以下教学目标与教学活动是否匹配：\n教学目标：{目标}\n教学活动：{活动}\n检查维度：1.目标与活动对应性 2.活动可评价性 3.评价方式明确性\n输出格式：表格+文字建议"', level=2)
add_bullet_para(doc, '测试Skill：输入真实教案片段，验证效果', level=1)
add_bullet_para(doc, '保存并命名："XX老师_教学评一致性检查器"', level=1)

add_para_custom(doc, '【产出物】', bold=True, indent=False)
add_para_custom(doc, '每位教师拥有一个可立即使用的个人Skill，能辅助日常备课质量检查。')

add_heading_custom(doc, '环节7：WorkBuddy高阶应用——五维试题精析（25分钟）', 3)
add_para_custom(doc, '【实操目标】', bold=True, indent=False)
add_para_custom(doc, '使用WorkBuddy完成一套试卷的五维度深度分析，生成可视化报告。')

add_para_custom(doc, '【五维分析框架】', bold=True)
add_bullet_para(doc, '维度1：知识点覆盖——各章节/考点占比是否合理')
add_bullet_para(doc, '维度2：难度梯度——易中难比例是否符合教学阶段')
add_bullet_para(doc, '维度3：能力层级——记忆/理解/应用/分析/评价/创造的分布')
add_bullet_para(doc, '维度4：题型结构——选择/填空/解答/实验等比例')
add_bullet_para(doc, '维度5：信效度指标——区分度、预测效度等基础分析')

add_para_custom(doc, '【操作步骤】（20分钟）', bold=True)
add_bullet_para(doc, '准备材料：提供一份样卷（提前准备，或现场上传）')
add_bullet_para(doc, '上传试卷：将Word/PDF试卷上传至WorkBuddy')
add_bullet_para(doc, '调用分析：使用Prompt引导AI进行分析')
add_bullet_para(doc, '示例指令："请对这份试卷进行五维度分析：1.统计各知识点占比并生成饼图描述 2.标注每道题的能力层级 3.分析易中难比例 4.给出整体评价和改进建议。输出为结构化报告。"')
add_bullet_para(doc, '结果优化：根据AI输出，教师补充人工判断，修正偏差')
add_bullet_para(doc, '导出保存：将分析报告导出为Word/PDF，存档备查')

add_para_custom(doc, '【产出物】', bold=True, indent=False)
add_para_custom(doc, '一份完整的五维试题分析报告，教师可直接用于教研会议或教学改进。')

add_para_custom(doc, '【互动环节】（5分钟）', bold=True, indent=False)
add_para_custom(doc, '小组讨论：3-4人一组，分享各自的分析结果，讨论"这份试卷最大的问题是什么"。每组推选1人汇报，AI记录要点。')

add_heading_custom(doc, '环节8：IMA实操——知识库管理与教学资料整理（15分钟）', 3)
add_para_custom(doc, '【实操目标】', bold=True, indent=False)
add_para_custom(doc, '学会用IMA建立个人/学科知识库，实现教学资料的智能化管理。')

add_para_custom(doc, '【操作步骤】', bold=True)
add_bullet_para(doc, '创建知识库：新建"XX学科教学资源库"')
add_bullet_para(doc, '上传资料：批量上传教案、课件、试题、论文等（提前准备3-5份）')
add_bullet_para(doc, '智能问答：向知识库提问，如"我上学期关于函数的教学设计有哪些？"')
add_bullet_para(doc, '标签管理：为资料添加标签（年级/章节/课型/年份）')
add_bullet_para(doc, '与WorkBuddy联动：将IMA知识库作为WorkBuddy的参考资料源')

add_para_custom(doc, '【产出物】', bold=True, indent=False)
add_para_custom(doc, '一个包含个人教学资料的知识库，能实现智能检索和问答。')

add_heading_custom(doc, '环节9：综合应用——PPT生成与成绩分析（20分钟）', 3)
add_para_custom(doc, '【实操目标】', bold=True, indent=False)
add_para_custom(doc, '综合运用WorkBuddy完成PPT生成和成绩分析两个高频任务。')

add_para_custom(doc, '【任务1】快速生成教学PPT大纲（10分钟）', bold=True)
add_bullet_para(doc, '输入："请为《XX》这节课生成PPT大纲，要求：导入3分钟、新授15分钟、练习10分钟、小结2分钟。包含互动环节设计。"')
add_bullet_para(doc, 'AI输出结构化大纲 → 教师审核调整 → 导出为PPT或Markdown')
add_bullet_para(doc, '技巧：使用WorkBuddy的PPT Skill，可一键生成带版式的PPT文件')

add_para_custom(doc, '【任务2】学生成绩智能分析（10分钟）', bold=True)
add_bullet_para(doc, '上传：Excel成绩表（含学生姓名、各题得分、总分）')
add_bullet_para(doc, '分析指令："请分析这份成绩表：1.统计班级均分、最高分、最低分、标准差 2.找出各题得分率，标注低于60%的题目 3.按分数段统计人数分布 4.识别需要重点关注的学生（偏科/退步）5.给出教学改进建议"')
add_bullet_para(doc, '结果：生成包含图表描述的文字报告，可导出使用')

add_para_custom(doc, '【产出物】', bold=True, indent=False)
add_para_custom(doc, 'PPT大纲文档 + 成绩分析报告，均为可直接使用或稍作修改即可使用的成品。')

doc.add_page_break()

# ---------- 第四阶段 ----------
add_heading_custom(doc, '第四阶段：综合应用与总结（30分钟）', 2)

add_heading_custom(doc, '环节10：一线教学场景整合应用（20分钟）', 3)
add_para_custom(doc, '【核心内容】', bold=True, indent=False)
add_para_custom(doc, '将前面学到的工具和方法，整合为一线教师日常工作的完整解决方案。')

add_para_custom(doc, '场景1：备课流程重构', bold=True)
add_bullet_para(doc, '传统流程：找资料 → 写教案 → 做课件 → 准备习题 → 手写板书设计（2-3小时）')
add_bullet_para(doc, 'AI辅助流程：')
add_bullet_para(doc, '用IMA检索已有资源（2分钟）', level=1)
add_bullet_para(doc, '用WorkBuddy生成教案框架（5分钟）', level=1)
add_bullet_para(doc, '用WorkBuddy生成PPT大纲和初稿（10分钟）', level=1)
add_bullet_para(doc, '用WorkBuddy生成分层练习题（5分钟）', level=1)
add_bullet_para(doc, '教师审核修改（15分钟）', level=1)
add_bullet_para(doc, '总耗时：约40分钟，效率提升3-4倍')

add_para_custom(doc, '场景2：作业批改辅助', bold=True)
add_bullet_para(doc, '用WorkBuddy的批改Skill：上传学生作文/解答，AI自动标注错误、给出评语模板')
add_bullet_para(doc, '教师只需审核AI批改结果，重点处理疑难个案')
add_bullet_para(doc, '效果：作文批改时间从30分钟/班降至10分钟/班')

add_para_custom(doc, '场景3：家校沟通模板', bold=True)
add_bullet_para(doc, '用WorkBuddy生成个性化家校沟通话术：输入学生表现数据，AI生成不同风格（鼓励型/提醒型/详细型）的沟通文本')
add_bullet_para(doc, '教师选择并微调，直接发送')

add_para_custom(doc, '场景4：个性化学习方案', bold=True)
add_bullet_para(doc, '输入学生错题记录和成绩分析，AI生成针对性补弱方案')
add_bullet_para(doc, '包含：薄弱知识点清单 → 推荐练习 → 学习计划 → 阶段目标')

add_para_custom(doc, '【互动环节】', bold=True, indent=False)
add_para_custom(doc, 'AI点名：抽取3位教师，分享"回去后最想立刻尝试的一个场景"。')

add_heading_custom(doc, '环节11：总结与行动计划（10分钟）', 3)
add_para_custom(doc, '【今日要点回顾】', bold=True, indent=False)
add_bullet_para(doc, 'AI Agent是"能完成任务的助手"，Skill是"助手的能力包"')
add_bullet_para(doc, 'WorkBuddy帮你做事，IMA帮你管知识，两者配合更高效')
add_bullet_para(doc, '教师的核心价值是"决策和设计"，AI负责"执行和重复劳动"')
add_bullet_para(doc, '不要追求全会，先掌握1-2个工具，用到熟练再扩展')

add_para_custom(doc, '【回去就能用的3个工具】', bold=True, indent=False)
add_bullet_para(doc, '工具1：用WorkBuddy生成下周教案框架（省1小时）')
add_bullet_para(doc, '工具2：用IMA建立个人教学资源库（长期收益）')
add_bullet_para(doc, '工具3：用WorkBuddy分析下次考试成绩（省2小时）')

add_para_custom(doc, '【持续学习资源】', bold=True, indent=False)
add_bullet_para(doc, 'WorkBuddy官方Skill市场：持续更新的教学Skill')
add_bullet_para(doc, 'IMA知识库社区：分享和获取优质教学资源')
add_bullet_para(doc, '教师AI应用交流群：校内/区内的实践分享社群')
add_bullet_para(doc, '每月尝试1个新Skill：积少成多，持续迭代')

add_para_custom(doc, '【行动计划填写】', bold=True, indent=False)
add_para_custom(doc, '发放纸质/电子版《AI教学应用行动计划表》，教师填写：')
add_bullet_para(doc, '本学期我要用AI完成的3项工作')
add_bullet_para(doc, '我准备使用的工具组合')
add_bullet_para(doc, '预计能节省的时间和提升的效果')
add_bullet_para(doc, '需要同事或技术支持的环节')

doc.add_page_break()

# ===== 四、培训配套材料 =====
add_heading_custom(doc, '四、培训配套材料', 1)

add_heading_custom(doc, '讲师准备材料', 2)
add_bullet_para(doc, '演示用电脑：已安装WorkBuddy、IMA，登录好账号')
add_bullet_para(doc, '样例文件包：样卷（Word/PDF）、成绩表（Excel）、教案模板（Word）')
add_bullet_para(doc, 'PPT课件：本次培训的理论部分PPT（学员视角设计）')
add_bullet_para(doc, '二维码物料：互动投票、问卷、资源下载等二维码，提前打印或投影')
add_bullet_para(doc, '网络环境：确保培训场地WiFi稳定，或准备热点备用')
add_bullet_para(doc, '备用方案：如网络故障，准备离线录屏视频作为替代')

add_heading_custom(doc, '学员准备材料', 2)
add_bullet_para(doc, '笔记本电脑：能联网，建议提前安装WorkBuddy和IMA')
add_bullet_para(doc, '个人教学资料：1份近期教案、1份试卷或成绩表（用于实操）')
add_bullet_para(doc, '笔记本：记录关键操作步骤和个人心得')
add_bullet_para(doc, '《AI教学应用行动计划表》：培训结束时填写')

add_heading_custom(doc, '发放资料清单', 2)
add_bullet_para(doc, '《WorkBuddy快速上手指南》（1页A4纸）')
add_bullet_para(doc, '《IMA知识库管理简明教程》（1页A4纸）')
add_bullet_para(doc, '《10个教学实用Prompt模板》（可直接复制使用）')
add_bullet_para(doc, '《Agent+Skill概念图解》（1页可视化说明）')
add_bullet_para(doc, '《AI教学应用行动计划表》（电子版+纸质版）')

doc.add_page_break()

# ===== 五、互动设计详解 =====
add_heading_custom(doc, '五、互动设计详解', 1)

add_para_custom(doc, '【二维码互动】', bold=True, indent=False)
add_bullet_para(doc, '适用环节：开场调研、工具选择投票、满意度反馈')
add_bullet_para(doc, '工具推荐：腾讯问卷、问卷星、腾讯文档收集表')
add_bullet_para(doc, '操作要点：提前生成二维码，大屏幕展示，实时刷新结果')
add_bullet_para(doc, '效果：打破单向讲授，让教师感受到"我的声音被听到"')

add_para_custom(doc, '【AI点名】', bold=True, indent=False)
add_bullet_para(doc, '适用环节：过渡环节、小组汇报人选、随机抽取分享者')
add_bullet_para(doc, '实现方式：WorkBuddy随机抽取学员名单，或预设名单用随机函数抽取')
add_bullet_para(doc, '效果：增加趣味性，避免总是"积极分子"发言，给内向教师参与机会')

add_para_custom(doc, '【小组实操】', bold=True, indent=False)
add_bullet_para(doc, '分组方式：4-5人一组，尽量同年级或同学科')
add_bullet_para(doc, '角色分工：组长（协调进度）、记录员（记录问题）、汇报员（成果展示）、技术支持（帮助操作困难者）')
add_bullet_para(doc, '讲师角色：巡回指导，重点帮助操作困难者，收集共性问题统一解答')

add_para_custom(doc, '【成果展示】', bold=True, indent=False)
add_bullet_para(doc, '每组推选1个最佳Skill或分析成果')
add_bullet_para(doc, '用屏幕投影展示，讲师点评亮点')
add_bullet_para(doc, '优秀成果可纳入学校共享资源库')

doc.add_page_break()

# ===== 六、时间控制建议 =====
add_heading_custom(doc, '六、时间控制建议', 1)

add_para_custom(doc, '【弹性调整原则】', bold=True, indent=False)
add_bullet_para(doc, '如学员基础较好：压缩第一阶段（宏观视野）至20分钟，增加实操时间')
add_bullet_para(doc, '如学员基础较弱：延长第二阶段（工具认知），确保概念理解到位')
add_bullet_para(doc, '如网络不稳定：提前准备离线录屏，确保实操环节不受影响')
add_bullet_para(doc, '如时间紧张：优先保证环节6（Skill创建）和环节7（试题分析），其他环节可精简')

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
    ['开始后70分钟', '完成第二阶段', '确认学员已分清WorkBuddy和IMA'],
    ['开始后100分钟', '完成环节6', '每人至少创建1个Skill'],
    ['开始后130分钟', '完成环节7', '每人完成1份试题分析'],
    ['结束前30分钟', '完成环节9', '确保PPT和成绩分析都实操过']
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
add_bullet_para(doc, '心态引导：反复强调"AI不会取代教师，但会用AI的教师会取代不会用的"。打消"学习新技术太麻烦"的抵触情绪。')
add_bullet_para(doc, '差异化指导：关注操作困难的教师，安排技术骨干学员协助，避免"跟不上"的挫败感。')
add_bullet_para(doc, '成果可视化：让教师带着"作品"离开（自己的Skill、分析报告、PPT大纲），增强成就感和持续使用动力。')
add_bullet_para(doc, '后续跟进：培训结束后1周，线上收集使用问题和心得；1个月后，组织线上分享会，展示优秀应用案例。')

doc.add_page_break()

# ===== 八、附录 =====
add_heading_custom(doc, '八、附录：实用Prompt模板', 1)

add_para_custom(doc, '以下模板可直接复制到WorkBuddy中使用：', bold=True, indent=False)

add_heading_custom(doc, '模板1：教学评一致性检查', 3)
p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.5
run = p.add_run('你是一个教学评一致性检查专家。请分析以下教学目标与教学活动是否匹配：\n教学目标：{在此输入目标}\n教学活动：{在此输入活动}\n\n检查维度：\n1. 目标与活动对应性：活动是否直接服务于目标达成？\n2. 活动可评价性：活动完成后，能否判断目标是否达成？\n3. 评价方式明确性：是否有清晰的评价标准和方式？\n\n输出格式：\n- 表格呈现三维度检查结果（符合/部分符合/不符合）\n- 文字给出具体改进建议（200字以内）\n- 给出修改后的活动建议（可选）')
set_run_font(run, size=9, color=RGBColor(0x33, 0x33, 0x33))

add_heading_custom(doc, '模板2：五维试题分析', 3)
p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.5
run = p.add_run('请对以下试卷进行五维度深度分析：\n\n维度1：知识点覆盖——统计各章节/考点占比，判断是否合理\n维度2：难度梯度——标注每道题难度（易/中/难），统计比例\n维度3：能力层级——按布鲁姆目标分类，标注每道题对应层级（记忆/理解/应用/分析/评价/创造）\n维度4：题型结构——统计各题型数量和分值占比\n维度5：质量评价——判断是否有偏题、怪题、重复题，给出整体信度评估\n\n输出要求：\n- 每个维度给出分析结论和改进建议\n- 生成知识结构图描述（可用文本图表呈现）\n- 总结3条最重要的改进建议')
set_run_font(run, size=9, color=RGBColor(0x33, 0x33, 0x33))

add_heading_custom(doc, '模板3：快速生成PPT大纲', 3)
p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.5
run = p.add_run('请为《{课题名称}》生成教学PPT大纲。\n\n课程信息：\n- 学科：{学科}\n- 年级：{年级}\n- 课时：{时长}分钟\n- 课型：{新授课/复习课/实验课等}\n\n大纲要求：\n1. 导入环节：设计1个引起兴趣的情境或问题（3-5分钟）\n2. 新授环节：分2-3个知识点，每个包含讲解要点和互动设计（15-20分钟）\n3. 练习环节：设计分层练习题，基础题+提高题（10分钟）\n4. 小结环节：知识梳理+学生总结（3-5分钟）\n5. 作业布置：分层作业设计\n\n输出格式：\n- 结构化大纲，每页PPT标注标题、内容要点、设计意图\n- 标注需要的图片/视频素材建议\n- 标注互动环节的教师行为')
set_run_font(run, size=9, color=RGBColor(0x33, 0x33, 0x33))

add_heading_custom(doc, '模板4：学生成绩分析', 3)
p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.5
run = p.add_run('请对以下成绩表进行智能分析：\n\n分析要求：\n1. 基础统计：班级均分、最高分、最低分、标准差、分数段人数分布\n2. 题目分析：各题得分率，标注低于60%的预警题目\n3. 学生个体：识别前10%和后10%学生，分析偏科情况\n4. 进步/退步：对比上次考试，标注进步最大和退步最大的学生（如有历史数据）\n5. 教学建议：基于数据，给出3条具体可行的教学改进建议\n\n输出格式：\n- 数据表格（文本格式）\n- 分析结论（分点呈现）\n- 重点关注学生名单及原因\n- 教学改进建议')
set_run_font(run, size=9, color=RGBColor(0x33, 0x33, 0x33))

add_heading_custom(doc, '模板5：家校沟通话术生成', 3)
p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.5
run = p.add_run('请为以下学生生成家校沟通话术：\n\n学生情况：\n- 姓名：{姓名}\n- 近期表现：{表现描述}\n- 成绩变化：{成绩情况}\n- 需要沟通的重点：{重点事项}\n\n沟通要求：\n- 风格：{鼓励型/提醒型/详细分析型/简短通知型}\n- 语气：尊重家长、客观描述、不贴标签、给出具体建议\n- 长度：{简短（100字内）/适中（300字内）/详细（500字内）}\n\n输出格式：\n- 微信/短信版本（简短）\n- 电话沟通提纲（要点式）\n- 详细书面版本（如需正式沟通）')
set_run_font(run, size=9, color=RGBColor(0x33, 0x33, 0x33))

# 保存
output_path = 'D:/projects/WorkBuddy/2026-06-17-11-18-20/AI赋能教学_一线教师数字素养培训方案.docx'
doc.save(output_path)
print('文档已生成：' + output_path)
