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

# 创建文档
doc = Document()
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
style.font.size = Pt(10.5)
style.paragraph_format.line_spacing = 1.5

# ===== 封面 =====
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title.add_run('WorkBuddy + IMA 应用场景详解')
set_run_font(title_run, size=22, bold=True, color=RGBColor(0x1a, 0x5f, 0x7a))

title2 = doc.add_paragraph()
title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
title2_run = title2.add_run('从"单兵作战"到"协同赋能"')
set_run_font(title2_run, size=18, bold=True, color=RGBColor(0x2e, 0x7d, 0x32))

doc.add_paragraph()
info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
info_run = info.add_run('配套《AI赋能教学：一线教师数字素养培训方案》\n用途：讲师备课参考 / 学员课后复习')
set_run_font(info_run, size=12)

doc.add_page_break()

# ===== 一、一句话定位 =====
add_heading_custom(doc, '一、一句话定位', 1)
add_para_custom(doc, '很多老师分不清WorkBuddy和IMA的区别，本质上就一句话：', bold=True, indent=False, color=RGBColor(0xc0, 0x00, 0x00))

add_para_custom(doc, 'WorkBuddy = 帮你干活的助手（聚焦"做事"）', bold=True, indent=False, color=RGBColor(0x1a, 0x5f, 0x7a))
add_para_custom(doc, 'IMA = 帮你管资料的助手（聚焦"管知识"）', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))
add_para_custom(doc, '两者联合 = 先用IMA把资料管好，再用WorkBuddy用这些资料去完成任务', bold=True, indent=False, color=RGBColor(0xf5, 0x7c, 0x00))

doc.add_paragraph()
add_para_custom(doc, '类比生活场景：IMA像你的书房书柜，把所有书分类放好；WorkBuddy像你请的家教，拿着书柜里的书帮你出题、改作业、写报告。没有书柜，家教到处找书浪费时间；没有家教，书柜里的书只是放着，没法帮你解决问题。')

doc.add_page_break()

# ===== 二、WorkBuddy 专属应用场景 =====
add_heading_custom(doc, '二、WorkBuddy 专属应用场景：用它"完成工作"', 1)
add_para_custom(doc, '以下场景，WorkBuddy是最优甚至唯一选择。IMA无法独立完成这些任务。', bold=True, indent=False, color=RGBColor(0x1a, 0x5f, 0x7a))

add_heading_custom(doc, '场景1：教案/PPT/试卷生成（内容创造）', 3)
add_para_custom(doc, '【工作痛点】', bold=True, indent=False)
add_para_custom(doc, '写一份教案需要2-3小时，做PPT又需要1-2小时，原创试题更费时。年轻教师经验不足，老教师想创新但精力不够。')
add_para_custom(doc, '【WorkBuddy怎么做】', bold=True, indent=False)
add_bullet_para(doc, '输入：课题名称+学科+年级+课时+特殊要求（如"需要小组讨论环节"）')
add_bullet_para(doc, 'AI输出：完整教案框架（含教学目标、重难点、教学过程、板书设计）')
add_bullet_para(doc, '继续追问："请把这份教案转成PPT大纲，每页标注动画和互动设计"')
add_bullet_para(doc, '再追问："请基于这节课的知识点，生成5道分层练习题（基础2道+提高2道+拓展1道）"')
add_para_custom(doc, '【时间对比】传统方式4小时 → WorkBuddy辅助40分钟，效率提升6倍', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))
add_prompt_box(doc, '可用Prompt',
    '请为《{课题}》生成一份完整教案。\n要求：\n- 学科：{学科}，年级：{年级}，课时：{时长}分钟\n- 包含：教学目标（三维目标）、教学重难点、教学过程（导入/新授/练习/小结/作业）、板书设计\n- 新授环节需包含至少1次学生互动（小组讨论/提问/动手操作）\n- 作业设计分层：A层基础题、B层提高题、C层拓展题\n输出格式：结构化文本，可直接复制到Word教案模板中。')

add_heading_custom(doc, '场景2：成绩智能分析（数据处理）', 3)
add_para_custom(doc, '【工作痛点】', bold=True, indent=False)
add_para_custom(doc, '期中考试后，班主任需要统计班级均分、排名、分数段分布、找出薄弱题目、识别偏科学生。Excel操作不熟练的教师，光是拉透视表就要折腾半天。')
add_para_custom(doc, '【WorkBuddy怎么做】', bold=True, indent=False)
add_bullet_para(doc, '上传：Excel成绩表（含学生姓名、各题得分、总分）')
add_bullet_para(doc, '指令："请分析这份成绩表，给出班级均分、标准差、各题得分率、分数段人数分布、偏科学生名单、教学改进建议"')
add_bullet_para(doc, 'AI输出：结构化分析报告，包含数据表格和文字结论')
add_bullet_para(doc, '进阶：上传两次考试成绩，AI自动对比进步/退步学生，生成追踪名单')
add_para_custom(doc, '【时间对比】传统方式2小时（Excel操作+人工分析）→ WorkBuddy 10分钟，效率提升12倍', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))
add_prompt_box(doc, '可用Prompt',
    '请对以下成绩表进行智能分析：\n1. 基础统计：班级均分、最高分、最低分、标准差、分数段人数分布（优秀/良好/及格/不及格）\n2. 题目分析：各题得分率，标注低于60%的预警题目，分析错因推测\n3. 学生个体：识别前10%和后10%学生，分析偏科情况（哪科强哪科弱）\n4. 对比分析：如有历史数据，标注进步最大和退步最大的学生\n5. 教学建议：基于数据，给出3条具体可行的教学改进建议\n输出格式：先表格后文字，表格清晰对齐。')

add_heading_custom(doc, '场景3：作业/作文自动批改（重复劳动替代）', 3)
add_para_custom(doc, '【工作痛点】', bold=True, indent=False)
add_para_custom(doc, '一个班50人，批改一次作文，人均5分钟，总共250分钟（4小时）。评语千篇一律，学生看不出自己的问题在哪。')
add_para_custom(doc, '【WorkBuddy怎么做】', bold=True, indent=False)
add_bullet_para(doc, '上传：学生作文照片或Word文档（可批量上传）')
add_bullet_para(doc, '指令："请批改这篇作文，标注错别字、语病、结构问题，给出具体修改建议，最后写一段50字以内的评语"')
add_bullet_para(doc, 'AI输出：逐篇标注+评语，教师只需审核，重点处理疑难个案')
add_bullet_para(doc, '批量模式：上传全班作文，AI生成"班级共性问题汇总"（如"80%学生存在流水账问题"）')
add_para_custom(doc, '【时间对比】传统方式4小时/班 → WorkBuddy 40分钟/班（含审核），效率提升6倍', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))
add_prompt_box(doc, '可用Prompt',
    '请批改以下{年级}学生作文，按以下维度评分：\n1. 立意（20分）：主题是否明确、是否有新意\n2. 结构（20分）：开头/中间/结尾是否完整，过渡是否自然\n3. 内容（30分）：事例是否具体、细节是否丰富\n4. 语言（20分）：用词是否准确、有无语病、修辞运用\n5. 书写（10分）：卷面、错别字\n\n输出要求：\n- 每项给出得分和简要理由（30字以内）\n- 标注3个最突出的问题和修改建议\n- 写一段50字以内的总评语（鼓励为主，指出1个改进方向）\n- 格式：表格+文字')

add_heading_custom(doc, '场景4：自定义Skill创建（个性化自动化）', 3)
add_para_custom(doc, '【工作痛点】', bold=True, indent=False)
add_para_custom(doc, '每个教师的教学风格不同、学科不同、学生情况不同。通用AI回答往往不够精准，需要反复调教。')
add_para_custom(doc, '【WorkBuddy怎么做】', bold=True, indent=False)
add_bullet_para(doc, '创建"教学评一致性检查器"：输入教学目标和活动，AI自动检查匹配度')
add_bullet_para(doc, '创建"分层作业生成器"：输入知识点，AI按难度生成A/B/C三层作业')
add_bullet_para(doc, '创建"家校沟通话术生成器"：输入学生表现，AI生成不同风格的沟通文本')
add_bullet_para(doc, '创建"课题申报助手"：输入研究方向，AI生成文献综述框架、研究方法建议')
add_para_custom(doc, '【核心价值】一次创建，永久复用。越用越顺手，形成个人教学工具箱。', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))

doc.add_page_break()

# ===== 三、IMA 专属应用场景 =====
add_heading_custom(doc, '三、IMA 专属应用场景：用它"管理知识"', 1)
add_para_custom(doc, '以下场景，IMA是最优甚至唯一选择。WorkBuddy无法替代IMA的知识库管理功能。', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))

add_heading_custom(doc, '场景1：个人教学资源库建设（资料聚合）', 3)
add_para_custom(doc, '【工作痛点】', bold=True, indent=False)
add_para_custom(doc, '教师的教学资料散落在电脑、U盘、微信文件、钉钉群、百度网盘各处。找一份去年用过的教案，要翻10分钟。新学期的课件，往往从零开始做，忘了上学期已经做过类似的。')
add_para_custom(doc, '【IMA怎么做】', bold=True, indent=False)
add_bullet_para(doc, '创建知识库：按学科/年级/学期建立分类（如"2025春_八年级数学"）')
add_bullet_para(doc, '批量上传：把教案、课件、试题、论文、学生作品等全部导入')
add_bullet_para(doc, '智能标签：系统自动识别内容并建议标签，也可手动添加（如"函数""几何""期中复习"）')
add_bullet_para(doc, '快速检索：需要时问"我上学期关于二次函数的教案有哪些？"，秒出结果')
add_para_custom(doc, '【核心价值】从"人找资料"变成"资料等人"，告别重复造轮子。', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))

add_heading_custom(doc, '场景2：跨文档智能问答（知识提取）', 3)
add_para_custom(doc, '【工作痛点】', bold=True, indent=False)
add_para_custom(doc, '学校发了新的教学大纲，又发了评价指南，还有课程标准。三份文件加起来100多页，教师想知道"本学期关于实验探究的要求是什么"，要逐份翻找。')
add_para_custom(doc, '【IMA怎么做】', bold=True, indent=False)
add_bullet_para(doc, '上传：把大纲、课标、评价指南等文件全部导入同一个知识库')
add_bullet_para(doc, '提问："本学期关于实验探究的教学要求有哪些？请综合三份文件回答。"')
add_bullet_para(doc, 'AI输出：整合三份文件的相关内容，给出结构化答案，并标注来源页码')
add_bullet_para(doc, '追问："这些要求中，哪些是我目前教案里没有覆盖到的？"')
add_para_custom(doc, '【核心价值】跨文档整合，AI帮你"读厚书"，提取精华。', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))

add_heading_custom(doc, '场景3：读书笔记与教研资料整理（知识沉淀）', 3)
add_para_custom(doc, '【工作痛点】', bold=True, indent=False)
add_para_custom(doc, '教师读了一篇好论文，当时有感触，但过两个月就忘了内容。参加教研会记了笔记，回去再也没翻开。知识没有沉淀，就无法复用。')
add_para_custom(doc, '【IMA怎么做】', bold=True, indent=False)
add_bullet_para(doc, '上传论文/笔记：拍照或导入PDF，AI自动提取核心观点、研究方法、结论')
add_bullet_para(doc, '生成摘要：AI生成500字摘要，标注"对我的教学有什么启发"')
add_bullet_para(doc, '关联知识库：把这篇论文与已有的教学资料关联，形成知识网络')
add_bullet_para(doc, '复习提问：过段时间问"上个月我读的那篇关于项目式学习的论文，核心观点是什么？"')
add_para_custom(doc, '【核心价值】知识从"读过"变成"记住"，从"记住"变成"能用"。', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))

add_heading_custom(doc, '场景4：校本/年级组共享资源库（团队协作）', 3)
add_para_custom(doc, '【工作痛点】', bold=True, indent=False)
add_para_custom(doc, '年级组内，好教案只有作者自己有，其他教师不知道。新教师想学习老教师的经验，但老教师没时间手把手教。')
add_para_custom(doc, '【IMA怎么做】', bold=True, indent=False)
add_bullet_para(doc, '创建共享知识库：年级组长建立"2025八年级数学组资源库"')
add_bullet_para(doc, '组员上传：每位教师上传自己的精品教案、原创试题、学生佳作')
add_bullet_para(doc, '权限管理：设置可见范围（全组/仅备课组/仅个人）')
add_bullet_para(doc, '智能问答：新教师问"王老师关于函数概念的导入设计是什么？"，直接获取王老师的教案内容')
add_bullet_para(doc, '版本追踪：教案更新后自动保留历史版本，可追溯修改过程')
add_para_custom(doc, '【核心价值】经验从"个人拥有"变成"集体资产"，新教师快速成长，老教师经验传承。', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))

doc.add_page_break()

# ===== 四、联合使用场景：1+1>2 =====
add_heading_custom(doc, '四、联合使用场景：WorkBuddy + IMA 协同作战', 1)
add_para_custom(doc, '以下场景，单独用任何一个工具都无法达到最佳效果，必须配合使用。这也是培训要传递给教师的核心思维："不是选一个，而是学会搭配"。', bold=True, indent=False, color=RGBColor(0xf5, 0x7c, 0x00))

add_heading_custom(doc, '联合场景1：智能备课全流程（IMA找资料 → WorkBuddy生成内容）', 3)
add_para_custom(doc, '【流程图解】', bold=True, indent=False)
add_para_custom(doc, 'IMA阶段（5分钟）：')
add_bullet_para(doc, '在IMA知识库中搜索："我上学期关于\'函数图像\'的教案和课件"')
add_bullet_para(doc, '找到3份历史资料，快速浏览，确定哪些可以复用')
add_bullet_para(doc, '把有用的资料片段标记为"参考素材"')
add_para_custom(doc, 'WorkBuddy阶段（15分钟）：', bold=False, indent=False)
add_bullet_para(doc, '把IMA中找到的资料上传到WorkBuddy')
add_bullet_para(doc, '指令："基于这些资料，帮我生成一份新的教案，要求：保留上次有效的导入设计，但新授环节增加一个小组探究活动，作业增加一道跨学科综合题。"')
add_bullet_para(doc, 'AI生成新教案 → 教师审核修改 → 导出为Word')
add_para_custom(doc, 'IMA阶段（2分钟）：', bold=False, indent=False)
add_bullet_para(doc, '把新教案上传回IMA知识库，更新"函数图像"标签')
add_bullet_para(doc, '备注："2025春_修订版_增加了探究活动"')
add_para_custom(doc, '【时间对比】传统备课3小时 → 联合使用22分钟，效率提升8倍。更关键的是：新教案站在旧教案基础上，一次比一次好。', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))

add_heading_custom(doc, '联合场景2：期中考试后深度复盘（IMA存试卷 → WorkBuddy分析 → IMA存报告）', 3)
add_para_custom(doc, '【流程图解】', bold=True, indent=False)
add_para_custom(doc, 'IMA阶段（3分钟）：')
add_bullet_para(doc, '把本次期中试卷、答案、评分标准上传到IMA知识库，归入"2025春_期中考试"文件夹')
add_bullet_para(doc, '同步上传：往年期中试卷（用于对比分析）')
add_para_custom(doc, 'WorkBuddy阶段（10分钟）：', bold=False, indent=False)
add_bullet_para(doc, '从IMA下载试卷，上传至WorkBuddy')
add_bullet_para(doc, '上传Excel成绩表')
add_bullet_para(doc, '五维分析指令："请对这份试卷进行知识点覆盖、难度梯度、能力层级、题型结构、质量评价五维度分析。同时对比去年的期中试卷，分析出题风格的变化。"')
add_bullet_para(doc, 'AI生成分析报告 → 教师补充人工判断 → 导出PDF')
add_para_custom(doc, 'IMA阶段（2分钟）：', bold=False, indent=False)
add_bullet_para(doc, '把分析报告上传回IMA，归入同一文件夹')
add_bullet_para(doc, '在知识库中建立关联："这份报告对应这份试卷，下次出卷时参考"')
add_bullet_para(doc, '教研组共享：其他教师可以在IMA中搜索"2025春期中考试分析"，直接查看')
add_para_custom(doc, '【核心价值】不仅分析了本次考试，还形成了可复用的"考试分析档案"，为下次出题提供数据支撑。', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))

add_heading_custom(doc, '联合场景3：课题研究辅助（IMA管文献 → WorkBuddy写内容）', 3)
add_para_custom(doc, '【流程图解】', bold=True, indent=False)
add_para_custom(doc, 'IMA阶段（持续进行）：')
add_bullet_para(doc, '建立"课题文献库"，按主题分类上传所有参考文献')
add_bullet_para(doc, '每篇文献由AI生成摘要，标注核心观点和研究方法')
add_bullet_para(doc, '需要时问："关于项目式学习在数学教学中的应用，我读过哪些文献？核心观点分别是什么？"')
add_para_custom(doc, 'WorkBuddy阶段（写作时）：', False, False)
add_bullet_para(doc, '从IMA导出文献摘要，上传至WorkBuddy')
add_bullet_para(doc, '指令："基于这些文献，帮我撰写\'国内外研究现状\'部分，要求：按时间线梳理，标注每篇文献的核心贡献，指出研究空白。"')
add_bullet_para(doc, 'AI生成初稿 → 教师审核修改 → 导出Word')
add_para_custom(doc, 'IMA阶段（完成后）：', False, False)
add_bullet_para(doc, '把论文初稿上传回IMA，归入"课题进展"')
add_bullet_para(doc, '建立版本管理：v1.0_研究现状 → v2.0_研究方法 → v3.0_完整论文')
add_para_custom(doc, '【核心价值】文献管理和论文写作无缝衔接，避免"找文献2小时、写论文1小时"的低效状态。', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))

add_heading_custom(doc, '联合场景4：学生个性化学习方案（IMA存学生档案 → WorkBuddy生成方案）', 3)
add_para_custom(doc, '【流程图解】', bold=True, indent=False)
add_para_custom(doc, 'IMA阶段（平时积累）：')
add_bullet_para(doc, '为每个学生建立"学习档案"：历次成绩、错题记录、课堂表现、作业情况')
add_bullet_para(doc, '家长沟通记录也归入档案，形成完整画像')
add_bullet_para(doc, '需要时问："请列出本学期数学成绩波动最大的5名学生，并分析可能原因。"')
add_para_custom(doc, 'WorkBuddy阶段（方案生成）：', False, False)
add_bullet_para(doc, '从IMA导出特定学生的档案数据')
add_bullet_para(doc, '指令："基于张三同学的错题记录和成绩趋势，生成一份为期2周的补弱计划。重点突破\'二次函数应用题\'，每天30分钟，包含：当天任务、推荐练习题、自测方式。"')
add_bullet_para(doc, 'AI生成个性化方案 → 教师审核调整 → 发给家长和学生')
add_para_custom(doc, 'IMA阶段（跟踪记录）：', False, False)
add_bullet_para(doc, '把方案存入学生档案，2周后对比执行效果')
add_bullet_para(doc, '形成循环：诊断→方案→执行→评估→调整')
add_para_custom(doc, '【核心价值】从"面向全班"到"面向个人"，真正实现因材施教。且所有数据可追溯，不是拍脑袋决策。', bold=True, indent=False, color=RGBColor(0x2e, 0x7d, 0x32))

doc.add_page_break()

# ===== 五、选择决策树 =====
add_heading_custom(doc, '五、选择决策树：遇到问题时，我该用哪个？', 1)
add_para_custom(doc, '以下是教师最常问的问题，直接按图索骥：', bold=True, indent=False)

table_qa = doc.add_table(rows=11, cols=3)
table_qa.style = 'Table Grid'
table_qa.alignment = WD_TABLE_ALIGNMENT.CENTER

headers_qa = ['教师遇到的问题', '推荐工具', '为什么']
for i, h in enumerate(headers_qa):
    cell = table_qa.rows[0].cells[i]
    cell.text = h
    for para in cell.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            set_run_font(run, bold=True, color=RGBColor(0xff, 0xff, 0xff))
    fill_cell_color(cell, '1A5F7A')

rows_qa = [
    ['我要写一份新教案', 'WorkBuddy', '内容生成是它的强项'],
    ['我去年做过类似教案，想找出来参考', 'IMA', '知识库检索是它的强项'],
    ['我要分析这次考试成绩', 'WorkBuddy', '数据处理和分析是它的强项'],
    ['我要找某份文件里的具体条款', 'IMA', '跨文档精准搜索是它的强项'],
    ['我要批改50篇作文', 'WorkBuddy', '批量重复任务替代是它的强项'],
    ['我要整理读书笔记和教研资料', 'IMA', '知识沉淀和分类管理是它的强项'],
    ['我要做PPT', 'WorkBuddy', '内容生成+结构化输出是它的强项'],
    ['我要和同事共享教案资源', 'IMA', '团队协作和权限管理是它的强项'],
    ['我要写课题论文的研究现状', '两者联合', 'IMA管文献 + WorkBuddy写作'],
    ['我要给学生做个性化补弱方案', '两者联合', 'IMA存档案 + WorkBuddy生成方案']
]

for row_idx, row_data in enumerate(rows_qa, start=1):
    for col_idx, text in enumerate(row_data):
        cell = table_qa.rows[row_idx].cells[col_idx]
        cell.text = text
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.line_spacing = 1.3
            for run in para.runs:
                set_run_font(run, size=9)

for row in table_qa.rows:
    row.cells[0].width = Inches(2.5)
    row.cells[1].width = Inches(1.5)
    row.cells[2].width = Inches(2.5)

doc.add_page_break()

# ===== 六、给教师的行动建议 =====
add_heading_custom(doc, '六、给教师的行动建议：从0到1，从1到N', 1)

add_para_custom(doc, '【第一周】先上手一个工具', bold=True, indent=False, color=RGBColor(0x1a, 0x5f, 0x7a))
add_bullet_para(doc, '如果你最头疼的是"写东西"：先学WorkBuddy，用它生成1份教案')
add_bullet_para(doc, '如果你最头疼的是"找东西"：先学IMA，把电脑里的教案全部上传，建立知识库')
add_bullet_para(doc, '不要两个同时学，先精通一个，再扩展另一个')

add_para_custom(doc, '【第一个月】形成习惯', bold=True, indent=False, color=RGBColor(0x1a, 0x5f, 0x7a))
add_bullet_para(doc, '每周用WorkBuddy生成至少1份教案或PPT大纲')
add_bullet_para(doc, '每次考试后用WorkBuddy分析成绩，报告存入IMA')
add_bullet_para(doc, '把IMA知识库作为"第二大脑"，重要资料随时上传')
add_bullet_para(doc, '创建1-2个个人Skill，解决最高频的重复性任务')

add_para_custom(doc, '【第一学期】建立系统', bold=True, indent=False, color=RGBColor(0x1a, 0x5f, 0x7a))
add_bullet_para(doc, '备课流程：IMA找资料 → WorkBuddy生成 → 审核修改 → IMA归档')
add_bullet_para(doc, '考试流程：IMA存试卷 → WorkBuddy分析 → IMA存报告')
add_bullet_para(doc, '教研流程：IMA管文献 → WorkBuddy写作 → IMA存成果')
add_bullet_para(doc, '分享经验：在教研组内推广，带动同事一起使用')

add_para_custom(doc, '【持续迭代】每月尝试一个新功能', bold=True, indent=False, color=RGBColor(0x1a, 0x5f, 0x7a))
add_bullet_para(doc, 'WorkBuddy：每月从Skill市场安装1个新Skill，或自己创建1个')
add_bullet_para(doc, 'IMA：每月整理一次知识库，删除过期资料，更新标签体系')
add_bullet_para(doc, '联合使用：每月探索一个新的联合场景，逐步覆盖全部教学工作')

doc.add_page_break()

# ===== 七、附录：更多Prompt模板 =====
add_heading_custom(doc, '七、附录：更多可直接使用的Prompt模板', 1)

add_prompt_box(doc, 'WorkBuddy：分层作业生成器',
    '请基于知识点"{知识点}"，生成分层作业：\n\nA层（基础巩固，适合后30%学生）：\n- 5道选择题（直接应用公式/概念）\n- 3道填空题（基础计算）\n\nB层（能力提升，适合中间40%学生）：\n- 3道解答题（需要多步骤推理）\n- 2道应用题（联系生活实际）\n\nC层（拓展挑战，适合前30%学生）：\n- 1道探究题（开放性，无标准答案）\n- 1道跨学科综合题（与其他学科结合）\n\n输出格式：每题标注难度、预估耗时、核心考查点。')

add_prompt_box(doc, 'WorkBuddy：课堂互动设计',
    '请为《{课题}》设计3个课堂互动环节：\n\n要求：\n1. 互动1（导入阶段，3分钟）：引起兴趣，与知识点相关\n2. 互动2（新授阶段，5分钟）：小组讨论或动手操作，突破重难点\n3. 互动3（练习阶段，3分钟）：游戏化或竞赛形式，巩固知识\n\n每个互动包含：\n- 教师指令（说什么）\n- 学生行为（做什么）\n- 时间控制\n- 预期效果\n- 可能的意外情况及应对')

add_prompt_box(doc, 'IMA：跨文档提问示例',
    '请综合以下文档，回答我的问题：\n\n问题："本学期关于实验探究的教学要求是什么？"\n\n要求：\n1. 从《课程标准》《教学大纲》《评价指南》三份文件中提取相关内容\n2. 按"知识要求/能力要求/评价要求"分类整理\n3. 标注每条要求的来源文档和页码\n4. 指出三份文件中要求不一致的地方\n5. 给出我目前教案中可能缺失的环节建议')

add_prompt_box(doc, 'WorkBuddy：家长会发言稿生成',
    '请帮我写一份家长会发言稿。\n\n背景：\n- 班级：{年级}{班级}\n- 会议主题：{主题，如期中总结/学习方法指导/家校合作}\n- 时长：{时长}分钟\n- 重点内容：{需要强调的几点}\n\n要求：\n- 开场：简短亲切，拉近距离（1分钟）\n- 主体：数据+案例，客观呈现班级情况（占70%时间）\n- 建议：给家长的具体可操作建议，避免空泛（占20%时间）\n- 结尾：感谢+期待合作（1分钟）\n- 语气：专业但不生硬，亲切但不随意\n\n输出格式：完整发言稿，标注段落时长建议。')

add_prompt_box(doc, 'WorkBuddy+IMA联合：基于知识库的教学反思',
    '请基于我上传的教学资料，帮我撰写教学反思。\n\n资料：\n1. 本节课教案（IMA中找到的上次版本）\n2. 本节课课件\n3. 学生课堂练习照片/扫描件\n4. 学生课后作业抽样（3份优、3份中、3份差）\n\n反思维度：\n1. 目标达成度：预设目标是否达成？哪些达成了，哪些没有？\n2. 教学环节有效性：每个环节的时间分配是否合理？学生参与度如何？\n3. 学生表现分析：从作业和练习中看，学生的典型错误是什么？反映出什么认知障碍？\n4. 改进方向：如果重上这节课，我会做哪些调整？具体怎么调整？\n\n输出格式：结构化反思报告，每个维度先分析后结论，最后给出3条具体改进建议。')

# 保存
output_path = 'D:/projects/WorkBuddy/2026-06-17-11-18-20/WorkBuddy与IMA应用场景详解.docx'
doc.save(output_path)
print('文档已生成：' + output_path)
