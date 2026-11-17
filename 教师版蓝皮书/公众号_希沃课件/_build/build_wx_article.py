# -*- coding: utf-8 -*-
"""把公众号成稿转成两份微信 HTML：
   - 推送版：纯正文、全内联 style、无 img / 无脚本 / 无 style 块，供 push.js 粘贴
   - 文章版：同上，额外带「复制全文（带格式）」按钮，供人工复制
   配图一律不嵌入，只留「（配图 NN｜说明）」提示行，按 wechat-inline-push 定稿流程人工插图。
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "公众号成稿_4步做出希沃课件.md"
OUT_PUSH = ROOT / "4步做出希沃课件-推送版.html"
OUT_PAGE = ROOT / "4步做出希沃课件-公众号文章.html"
TITLE = "workbuddy+希沃：4步直接在希沃里做出原生课件"

CAPTIONS = {
    "01": "成品，《赵州桥》思维导图页",
    "02": "技能市场 SkillHub 搜「希沃」",
    "03": "技能详情 v1.0.2，已启用",
    "04": "左侧技能菜单入口",
    "05": "连接成功，7916 端口与工具列表校验通过",
    "06": "连接状态反转，重启后 tools/list 就绪",
    "07": "阶段② 四条教学目标",
    "08": "阶段③ 大纲硬约束与 8 页内容页",
    "09": "汉字卡控件与开始授课",
    "10": "判断对错活动（备课态预览）",
}

P = 'font-size:16px;line-height:1.9;margin:0 0 16px;color:#26312F;'
H2 = ('font-size:21px;line-height:1.5;margin:32px 0 14px;padding-left:11px;'
      'border-left:4px solid #B4472B;color:#26312F;font-weight:700;')
CODE = ('background:#26312F;color:#F5F1E8;padding:14px 16px;border-radius:6px;'
        'font-family:Consolas,Monaco,monospace;font-size:14px;line-height:1.75;'
        'white-space:pre-wrap;word-break:break-all;margin:16px 0;')
QUOTE = ('background:#FBF3EF;border-left:4px solid #B4472B;padding:12px 16px;'
         'margin:16px 0;font-size:15px;line-height:1.9;color:#3F5A62;')
LI = 'font-size:16px;line-height:1.9;margin:0 0 8px 10px;color:#26312F;'
FIG = ('background:#F7F4EE;border:1px dashed #D8CFC0;border-radius:6px;'
       'padding:10px 14px;margin:18px 0;text-align:center;'
       'font-size:14px;color:#8A8A82;')
HR = 'border:0;border-top:1px solid #E5DFD0;margin:26px 0;'
TAG = 'font-size:13px;color:#8A8A82;line-height:1.8;margin:18px 0 0;'


def punct(t):
    """叙述文字按公众号标点禁忌收敛中文冒号，代码块不走这里。"""
    t = re.sub(r'：$', '。', t)
    return t.replace('：', '，')


def inline(t, keep_colon=False):
    if not keep_colon:
        t = punct(t)
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color:#B4472B;">\1</strong>', t)
    t = re.sub(r'`(.+?)`',
               r'<code style="background:#F5F1E8;padding:2px 5px;border-radius:3px;'
               r'font-size:14px;color:#3F5A62;">\1</code>', t)
    return t


raw = SRC.read_text(encoding="utf-8")
lines = re.sub(r"^#\s+.*\n", "", raw, count=1).splitlines()

parts = []
i = 0
while i < len(lines):
    s = lines[i].strip()
    if not s:
        i += 1
        continue
    m = re.match(r"^【配图\s*(\d{2})】$", s)
    if m:
        n = m.group(1)
        parts.append('<p style="%s">（配图 %s｜%s，请在此处插入对应编号图片）</p>'
                     % (FIG, n, html.escape(CAPTIONS.get(n, ""))))
        i += 1
        continue
    if s.startswith("```"):
        buf = []
        i += 1
        while i < len(lines) and not lines[i].strip().startswith("```"):
            buf.append(lines[i])
            i += 1
        i += 1
        parts.append('<section style="%s">%s</section>'
                     % (CODE, html.escape("\n".join(buf))))
        continue
    if s.startswith("> "):
        buf = []
        while i < len(lines) and lines[i].strip().startswith("> "):
            buf.append(lines[i].strip()[2:])
            i += 1
        parts.append('<section style="%s">%s</section>'
                     % (QUOTE, "<br>".join(inline(x) for x in buf)))
        continue
    if s.startswith("- "):
        while i < len(lines) and lines[i].strip().startswith("- "):
            parts.append('<p style="%s">· %s</p>'
                         % (LI, inline(lines[i].strip()[2:])))
            i += 1
        continue
    if s.startswith("## "):
        parts.append('<h2 style="%s">%s</h2>' % (H2, inline(s[3:])))
        i += 1
        continue
    if s == "---":
        parts.append('<hr style="%s">' % HR)
        i += 1
        continue
    if s.startswith("#AI"):
        parts.append('<p style="%s">%s</p>' % (TAG, html.escape(s)))
        i += 1
        continue
    parts.append('<p style="%s">%s</p>' % (P, inline(s)))
    i += 1

body = "\n".join(parts)

push_doc = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>%s</title></head>
<body style="max-width:677px;margin:0 auto;padding:0 2px;font-family:'Microsoft YaHei','PingFang SC',sans-serif;background:#FFFFFF;">
<section id="article">
%s
</section>
</body></html>""" % (html.escape(TITLE), body)
OUT_PUSH.write_text(push_doc, encoding="utf-8")

BUTTON = ('display:inline-block;background:#B4472B;color:#FFFFFF;border:0;'
          'border-radius:6px;padding:10px 20px;font-size:15px;cursor:pointer;')
TOOLBAR = ('max-width:677px;margin:0 auto 18px;padding:14px 16px;background:#F7F4EE;'
           'border-radius:8px;font-size:13px;color:#3F5A62;line-height:1.7;')
page_doc = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>%s</title></head>
<body style="margin:0;padding:24px 12px;background:#EDEAE3;font-family:'Microsoft YaHei','PingFang SC',sans-serif;">
<div id="toolbar" style="%s">
  <button id="copyBtn" style="%s" onclick="copyArticle()">复制全文（带格式）</button>
  <div style="margin-top:8px;">复制后到公众号编辑器粘贴。配图按 01–10 手动插入，替换掉对应的提示行。</div>
</div>
<section id="article" style="max-width:677px;margin:0 auto;padding:20px 18px;background:#FFFFFF;border-radius:8px;">
%s
</section>
<script>
async function copyArticle(){
  const el=document.getElementById('article');
  const item=new ClipboardItem({
    'text/html':new Blob([el.innerHTML],{type:'text/html'}),
    'text/plain':new Blob([el.innerText],{type:'text/plain'})
  });
  await navigator.clipboard.write([item]);
  const b=document.getElementById('copyBtn');
  b.textContent='已复制，去公众号粘贴';
  setTimeout(()=>b.textContent='复制全文（带格式）',2500);
}
</script>
</body></html>""" % (html.escape(TITLE), TOOLBAR, BUTTON, body)
OUT_PAGE.write_text(page_doc, encoding="utf-8")

for p in (OUT_PUSH, OUT_PAGE):
    t = p.read_text(encoding="utf-8")
    print("✓", p.name, round(p.stat().st_size / 1024), "KB",
          "内联", t.count('style="'), "img", t.count("<img"),
          "style块", t.count("<style"), "锚点", len(re.findall(r'href="#', t)))
