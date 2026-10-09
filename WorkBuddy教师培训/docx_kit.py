# -*- coding: utf-8 -*-
"""交付包文档排版工具包（四份文档共用，保证风格统一）"""
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# 品牌色（沿用项目既有配色）
C_MAIN = "1A5F7A"   # 主色 深青
C_GREEN = "2E7D32"  # 辅色 绿
C_ORANGE = "F57C00" # 强调 橙
C_RED = "C0392B"    # 警示 红
C_GRAY = "333333"   # 正文
C_SUB = "5B6B7B"    # 次要
C_LINE = "D8E2E8"   # 边框

FONT = "Microsoft YaHei"


def set_run(run, size=21, bold=False, color=C_GRAY, name=FONT, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), name)
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    return run


def P(doc, text, size=21, bold=False, color=C_GRAY, align=None,
      space_before=2, space_after=4, indent=0, line=1.5, italic=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line
    if indent:
        pf.left_indent = Cm(indent)
    if align == 'c':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == 'r':
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run(p.add_run(text), size=size, bold=bold, color=color, italic=italic)
    return p


def H(doc, text, level=1, color=None, size=None, space_before=12, space_after=6):
    spec = {
        0: (30, C_MAIN, 20, 10),
        1: (26, C_MAIN, 16, 8),
        2: (23, C_GREEN, 12, 6),
        3: (21, C_ORANGE, 10, 4),
    }
    d_size, d_color, sb, sa = spec.get(level, spec[3])
    return P(doc, text, size=size or d_size, bold=True,
             color=color or d_color, space_before=sb, space_after=sa, line=1.3)


def BUL(doc, text, size=20, color=C_GRAY, indent=0.6, mark="●", mark_color=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(indent)
    pf.first_line_indent = Cm(-0.45)
    pf.space_before = Pt(1)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.45
    set_run(p.add_run(mark + " "), size=size - 3, color=mark_color or C_MAIN, bold=True)
    set_run(p.add_run(text), size=size, color=color)
    return p


def NUM(doc, idx, text, size=20, color=C_GRAY, indent=0.6):
    return BUL(doc, text, size=size, color=color, indent=indent,
               mark="%d." % idx, mark_color=C_MAIN)


def BOX(doc, title, lines, fill_hex="F4F8FA", bar=C_MAIN, title_color=None):
    """带底色 + 左侧色条的提示框（用单元格模拟）"""
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.rows[0].cells[0]
    shade(c, fill_hex)
    tcPr = c._tc.get_or_add_tcPr()
    borders = tcPr.find(qn('w:tcBorders'))
    if borders is None:
        borders = OxmlElement('w:tcBorders')
        tcPr.append(borders)
    for edge, w, col in (('left', 24, bar), ('top', 4, 'FFFFFF'),
                         ('bottom', 4, 'FFFFFF'), ('right', 4, 'FFFFFF')):
        el = OxmlElement('w:%s' % edge)
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), str(w))
        el.set(qn('w:color'), col)
        borders.append(el)
    c.text = ""
    first = c.paragraphs[0]
    first.paragraph_format.space_before = Pt(4)
    first.paragraph_format.space_after = Pt(2)
    set_run(first.add_run(title), size=20, bold=True, color=title_color or bar)
    for ln in lines:
        p = c.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.4
        set_run(p.add_run(ln), size=19, color=C_GRAY)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def cell_text(cell, text, size=18, bold=False, color=C_GRAY, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.35
    if align == 'c':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == 'r':
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for i, seg in enumerate(str(text).split("\n")):
        if i > 0:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.35
        set_run(p.add_run(seg), size=size, bold=bold, color=color)


def set_col_widths(table, widths_cm):
    table.autofit = False
    for row in table.rows:
        for i, w in enumerate(widths_cm):
            if i < len(row.cells):
                row.cells[i].width = Cm(w)


def make_table(doc, headers, rows, widths=None, head_fill=C_MAIN, size=17,
               head_size=18, zebra=True, aligns=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        shade(c, head_fill)
        cell_text(c, h, size=head_size, bold=True, color="FFFFFF", align='c')
    for ri, r in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(r):
            fill = "F7FAFB" if (zebra and ri % 2 == 1) else "FFFFFF"
            shade(cells[i], fill)
            al = aligns[i] if aligns else None
            bold = (i == 0 and len(headers) > 2)
            cell_text(cells[i], v, size=size, align=al, bold=bold,
                      color=C_MAIN if bold else C_GRAY)
    if widths:
        set_col_widths(t, widths)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def cover(doc, main, sub, meta_lines, tag=None):
    for _ in range(3):
        doc.add_paragraph()
    P(doc, tag or "县域中小学教师培训 · 交付包", size=19, color=C_ORANGE,
      align='c', bold=True, space_after=10)
    P(doc, main, size=40, bold=True, color=C_MAIN, align='c', line=1.2, space_after=10)
    P(doc, sub, size=24, color=C_GREEN, align='c', space_after=24)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run("─" * 22), size=20, color=C_LINE)
    for ln in meta_lines:
        P(doc, ln, size=18, color=C_SUB, align='c', space_after=4, line=1.5)
    doc.add_page_break()


def footer_note(doc, text):
    P(doc, text, size=16, color=C_SUB, align='c', space_before=10, italic=True)


def setup(doc):
    st = doc.styles['Normal']
    st.font.name = FONT
    st.font.size = Pt(21)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    for s in doc.sections:
        s.top_margin = Cm(2.2)
        s.bottom_margin = Cm(2.0)
        s.left_margin = Cm(2.4)
        s.right_margin = Cm(2.4)
