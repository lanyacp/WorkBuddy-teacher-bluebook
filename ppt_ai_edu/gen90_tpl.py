# -*- coding: utf-8 -*-
"""90 页 PPT 备料库：批量生成 P05-P90 中尚未新建的页面。
内容严格对齐《PPT 细分框架 V3》P01-P90。
"""
import os

DST = r"D:\projects\WorkBuddy\2026-06-17-11-18-20\ppt_ai_edu\pages90"
os.makedirs(DST, exist_ok=True)

MAIN, GREEN, ORANGE, RED, GRAY_S = "#1A5F7A", "#2E7D32", "#F57C00", "#C0392B", "#5B6B7B"

HEAD = """<Slide style={{ width:'1280px', height:'720px', background:'#FFFFFF', display:'flex', flexDirection:'column', padding:'20px 64px' }}>
  <Box style={{ height:96, borderLeft:'6px solid @BAR@', paddingLeft:18, justifyContent:'center' }}>
    <Text style={{ fontSize:34, fontWeight:'bold', color:'@TCOLOR@' }}>@TITLE@</Text>
    <Text style={{ fontSize:19, color:'#5B6B7B', marginTop:4 }}>@SUB@</Text>
  </Box>
"""

FOOT = """  <Box style={{ height:36, flexDirection:'row', justifyContent:'space-between', alignItems:'center', borderTop:'1px solid #E2E8F0', marginTop:8 }}>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>AI赋能中小学教育教学 · 县域教师培训</Text>
    <Text style={{ fontSize:14, color:'#94A3B8' }}>@PAGE@ / 90</Text>
  </Box>
</Slide>
"""


def page(no, slug, title, sub, body, bar=MAIN, tcolor=MAIN):
    html = HEAD.replace("@BAR@", bar).replace("@TCOLOR@", tcolor) \
               .replace("@TITLE@", title).replace("@SUB@", sub)
    html += body
    html += FOOT.replace("@PAGE@", "%02d" % no)
    p = os.path.join(DST, "p%02d_%s.jsx" % (no, slug))
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    return p


# ---------- 通用 body 模板 ----------

def b_cards(cards, cols=None, h="100%"):
    """cards: [(num,title,desc,color)] 横排卡片"""
    n = cols or len(cards)
    w = "calc(%.4f%% - %dpx)" % (100.0 / n, (n - 1) * 9)
    items = []
    for c in cards:
        num, t, d, col = c
        numhtml = ("<Text style={{ fontSize:26, fontWeight:'bold', color:'%s' }}>%s</Text>" % (col, num)) if num else ""
        items.append(
            "<Box style={{ width:'%s', background:'#F4F8FA', borderRadius:10, padding:'16px 16px', borderTop:'4px solid %s' }}>"
            "%s<Text style={{ fontSize:20, fontWeight:'bold', color:'#1F2937', marginTop:%s }}>%s</Text>"
            "<Text style={{ fontSize:16, color:'#5B6B7B', marginTop:8, lineHeight:1.55 }}>%s</Text></Box>"
            % (w, col, numhtml, 6 if num else 0, t, d))
    return ("  <Box style={{ flex:1, flexDirection:'row', gap:9, marginTop:12, alignItems:'stretch' }}>\n    "
            + "\n    ".join(items) + "\n  </Box>\n")


def b_rows(rows, gap=10):
    """rows: [(num,title,desc,color)] 纵向列表"""
    items = []
    for r in rows:
        num, t, d, col = r
        items.append(
            "<Box style={{ flexDirection:'row', alignItems:'center', gap:14, background:'#F4F8FA', borderRadius:10, padding:'13px 18px' }}>"
            "<Box style={{ width:40, height:40, borderRadius:20, background:'%s', alignItems:'center', justifyContent:'center' }}>"
            "<Text style={{ fontSize:19, color:'#fff', fontWeight:'bold', fontFamily:'Arial' }}>%s</Text></Box>"
            "<Text style={{ fontSize:21, fontWeight:'bold', color:'%s', width:190 }}>%s</Text>"
            "<Text style={{ fontSize:18, color:'#1F2937', flex:1, lineHeight:1.45 }}>%s</Text></Box>"
            % (col, num, col, t, d))
    head = ("  <Box style={{ flex:1, flexDirection:'column', gap:%d, marginTop:12, justifyContent:'center' }}>\n    " % gap)
    return head + "\n    ".join(items) + "\n  </Box>\n"


def b_twocol(l_title, l_items, r_title, r_items, l_col=MAIN, r_col=ORANGE):
    def col(t, items, colr, fill):
        its = []
        for it in items:
            if isinstance(it, tuple):
                k, v = it
                its.append("<Box style={{ background:'#FFFFFF', borderRadius:8, padding:'11px 14px' }}>"
                           "<Text style={{ fontSize:17, fontWeight:'bold', color:'%s' }}>%s</Text>"
                           "<Text style={{ fontSize:16, color:'#1F2937', marginTop:4, lineHeight:1.45 }}>%s</Text></Box>" % (colr, k, v))
            else:
                its.append("<Box style={{ flexDirection:'row', gap:8, alignItems:'flex-start' }}>"
                           "<Text style={{ fontSize:15, color:'%s', fontWeight:'bold' }}>·</Text>"
                           "<Text style={{ fontSize:17, color:'#1F2937', flex:1, lineHeight:1.45 }}>%s</Text></Box>" % (colr, it))
        return ("<Box style={{ flex:1, background:'%s', borderRadius:12, padding:'18px 20px' }}>"
                "<Text style={{ fontSize:22, fontWeight:'bold', color:'%s' }}>%s</Text>"
                "<Box style={{ marginTop:12, gap:9 }}>\n%s\n</Box></Box>" % (fill, colr, t, "\n      ".join(its)))
    return ("  <Box style={{ flex:1, flexDirection:'row', gap:16, marginTop:12, alignItems:'stretch' }}>\n    "
            + col(l_title, l_items, l_col, "#F4F8FA") + "\n    "
            + col(r_title, r_items, r_col, "#FFF7ED") + "\n  </Box>\n")


def b_prompt(prompt, note=None, label="提示词（改尖括号即可用）"):
    notehtml = ("<Box style={{ marginTop:12, borderTop:'1px solid #374151', paddingTop:10 }}>"
                "<Text style={{ fontSize:16, color:'#9CA3AF', lineHeight:1.5 }}>%s</Text></Box>" % note) if note else ""
    return ("  <Box style={{ flex:1, flexDirection:'column', marginTop:12 }}>\n"
            "    <Box style={{ flex:1, background:'#1F2937', borderRadius:12, padding:'20px 24px' }}>\n"
            "      <Text style={{ fontSize:19, color:'#FBBF24', fontWeight:'bold' }}>%s</Text>\n"
            "      <Text style={{ fontSize:19, color:'#E5E7EB', marginTop:12, lineHeight:1.75 }}>%s</Text>\n"
            "    </Box>\n  %s\n  </Box>\n" % (label, prompt, notehtml))


def b_grid2(cards):
    """cards: [(num,title,desc,color)] 2x2 网格"""
    items = []
    n = 2
    w = "calc(50% - 8px)"
    for c in cards:
        num, t, d, col = c
        numhtml = "<Text style={{ fontSize:40, fontWeight:'bold', color:'%s', fontFamily:'Arial' }}>%s</Text>" % (col, num)
        items.append(
            "<Box style={{ width:'%s', height:'calc(50%% - 8px)', background:'#F4F8FA', borderRadius:12, padding:'18px 22px', borderLeft:'6px solid %s', justifyContent:'center' }}>"
            "%s<Text style={{ fontSize:23, fontWeight:'bold', color:'#1F2937', marginTop:6 }}>%s</Text>"
            "<Text style={{ fontSize:17, color:'#5B6B7B', marginTop:8, lineHeight:1.55 }}>%s</Text></Box>" % (w, col, numhtml, t, d))
    return ("  <Box style={{ flex:1, flexDirection:'row', flexWrap:'wrap', gap:16, marginTop:12 }}>\n    "
            + "\n    ".join(items) + "\n  </Box>\n")


def b_twotext(top_label, top_text, bot_label, bot_text, tl=MAIN, bl=ORANGE):
    return ("  <Box style={{ flex:1, flexDirection:'column', marginTop:14, gap:14 }}>\n"
            "    <Box style={{ flex:1, background:'#F4F8FA', borderRadius:12, padding:'18px 24px', justifyContent:'center' }}>\n"
            "      <Text style={{ fontSize:19, color:'%s', fontWeight:'bold' }}>%s</Text>\n"
            "      <Text style={{ fontSize:27, fontWeight:'bold', color:'#1F2937', marginTop:8, lineHeight:1.35 }}>%s</Text>\n"
            "    </Box>\n"
            "    <Box style={{ flex:1, background:'#1A5F7A', borderRadius:12, padding:'18px 24px', justifyContent:'center' }}>\n"
            "      <Text style={{ fontSize:19, color:'%s', fontWeight:'bold' }}>%s</Text>\n"
            "      <Text style={{ fontSize:27, fontWeight:'bold', color:'#FFFFFF', marginTop:8, lineHeight:1.35 }}>%s</Text>\n"
            "    </Box>\n  </Box>\n" % (tl, top_label, top_text, bl, bot_label, bot_text))


def b_note(text, fill="#FFF7ED", bar=ORANGE, tcolor="#1F2937"):
    return ("  <Box style={{ marginTop:12, background:'%s', borderRadius:10, padding:'13px 20px', borderLeft:'5px solid %s' }}>\n"
            "    <Text style={{ fontSize:18, color:'%s', textAlign:'center' }}>%s</Text>\n  </Box>\n" % (fill, bar, tcolor, text))


def b_section(no, title, sub, tags, grad="linear-gradient(135deg,#1A5F7A 0%, #2E7D32 100%)", tagcol="#CFE3EA"):
    taghtml = "\n    ".join(
        "<Box style={{ background:'rgba(255,255,255,0.16)', padding:'11px 18px', borderRadius:8 }}>"
        "<Text style={{ color:'#fff', fontSize:18 }}>%s</Text></Box>" % t for t in tags)
    return ("<Slide style={{ width:'1280px', height:'720px', background:'%s', display:'flex', flexDirection:'column', justifyContent:'center', padding:'0 90px' }}>\n"
            "  <Text style={{ fontSize:22, color:'%s', letterSpacing:4, fontWeight:'bold' }}>%s</Text>\n"
            "  <Text style={{ fontSize:56, fontWeight:'bold', color:'#FFFFFF', marginTop:14 }}>%s</Text>\n"
            "  <Text style={{ fontSize:26, color:'#EAF3F6', marginTop:14 }}>%s</Text>\n"
            "  <Box style={{ width:100, height:4, background:'#F57C00', marginTop:24, marginBottom:24 }} />\n"
            "  <Box style={{ flexDirection:'row', gap:12 }}>\n    %s\n  </Box>\n"
            "  <Text style={{ fontSize:20, color:'%s', marginTop:28 }}>%s</Text>\n</Slide>\n"
            % (grad, tagcol, no, title, sub, taghtml, tagcol, sub))


def b_end(quote_lines, closing, cta, footer):
    lines = "\n    ".join("<Text style={{ fontSize:20, color:'#D7E6EB', lineHeight:1.8 }}>%s</Text>" % l for l in quote_lines)
    ctas = "\n    ".join("<Box style={{ background:'rgba(255,255,255,0.14)', padding:'12px 22px', borderRadius:8 }}>"
                        "<Text style={{ color:'#fff', fontSize:18 }}>%s</Text></Box>" % c for c in cta)
    return ("<Slide style={{ width:'1280px', height:'720px', background:'linear-gradient(135deg,#1A5F7A 0%%, #15495C 55%%, #2E7D32 140%%)', display:'flex', flexDirection:'column', justifyContent:'center', padding:'0 90px', position:'relative', overflow:'hidden' }}>\n"
            "  <svg width=\"400\" height=\"400\" viewBox=\"0 0 520 520\" style={{ position:'absolute', right:0, bottom:0, opacity:0.10 }}>\n"
            "    <circle cx=\"260\" cy=\"260\" r=\"190\" fill=\"none\" stroke=\"#FFFFFF\" strokeWidth=\"2\" />\n"
            "    <circle cx=\"260\" cy=\"260\" r=\"130\" fill=\"none\" stroke=\"#FFFFFF\" strokeWidth=\"2\" />\n  </svg>\n"
            "  <Text style={{ fontSize:21, color:'#9FE0C4', letterSpacing:4, fontWeight:'bold' }}>结语</Text>\n"
            "  <Text style={{ fontSize:46, fontWeight:'bold', color:'#FFFFFF', marginTop:14, lineHeight:1.3 }}>%s</Text>\n"
            "  <Box style={{ width:100, height:4, background:'#F57C00', marginTop:24, marginBottom:24 }} />\n"
            "  %s\n"
            "  <Box style={{ marginTop:30, flexDirection:'row', gap:14 }}>\n    %s\n  </Box>\n"
            "  <Text style={{ fontSize:17, color:'#9FC6D4', marginTop:26 }}>%s</Text>\n</Slide>\n"
            % (closing, lines, ctas, footer))
