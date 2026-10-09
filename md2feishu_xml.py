#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把教师版蓝皮书的 Markdown 转成飞书 DocxXML，重点解决图片不渲染的问题。

背景：lark-cli 的 drive +import 会把 markdown 的 ![]() 转成普通文本链接，
      docs +create --doc-format markdown 则直接丢弃图片。
      只有 XML 的 <img path="@./xxx.png"/> 才能真正内嵌图片。

用法：python md2feishu_xml.py <输入.md> <输出.xml>
"""
import re
import sys
import os

# ---------- 基础工具 ----------

BLOCK_TAGS = {
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote', 'hr', 'table',
    'img', 'pre', 'code', 'grid', 'callout', 'title',
}


def esc(text: str) -> str:
    """转义 XML 文本内容"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text


def inline(text: str) -> str:
    """处理行内格式：粗体、斜体、行内代码、链接"""
    # 先保护代码块内容，避免内部被处理
    codes = []

    def stash_code(m):
        codes.append(m.group(1))
        return f'\x00CODE{len(codes)-1}\x00'

    text = re.sub(r'`([^`]+)`', stash_code, text)

    # 链接 [文字](url)
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        lambda m: f'<a type="url-preview" href="{m.group(2)}">{inline_plain(m.group(1))}</a>',
        text,
    )
    # 粗体
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    # 斜体
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)

    # 还原代码
    def restore(m):
        return f'<code>{esc(codes[int(m.group(1))])}</code>'

    text = re.sub(r'\x00CODE(\d+)\x00', restore, text)
    return text


def inline_plain(text: str) -> str:
    """链接文字里的格式（只处理粗体/斜体，不递归处理链接）"""
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    return text


def split_row(line: str):
    """拆分表格行"""
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    cells = []
    buf = ''
    escaped = False
    for ch in s:
        if escaped:
            buf += ch
            escaped = False
            continue
        if ch == '\\':
            escaped = True
            buf += ch
            continue
        if ch == '|':
            cells.append(buf)
            buf = ''
            continue
        buf += ch
    cells.append(buf)
    return [c.strip() for c in cells]


def is_sep(line: str) -> bool:
    """判断是否为表格分隔行 |---|---|"""
    s = line.strip()
    if not s.startswith('|'):
        return False
    return bool(re.fullmatch(r'\|[\s:\-|]+\|?', s))


# ---------- 主转换 ----------

def convert(md: str, img_prefix: str = '@./') -> str:
    lines = md.split('\n')
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # 空行
        if not stripped:
            i += 1
            continue

        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m:
            lvl = len(m.group(1))
            txt = inline(m.group(2).strip())
            if lvl == 1 and not any(o.startswith('<title') for o in out[:3]):
                pass  # 第一个 h1 保留为 h1
            out.append(f'<h{lvl}>{txt}</h{lvl}>')
            i += 1
            continue

        # 分隔线
        if re.fullmatch(r'-{3,}', stripped):
            out.append('<hr/>')
            i += 1
            continue

        # 图片（关键修复点）
        m = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)', stripped)
        if m:
            alt, src = m.group(1), m.group(2)
            # 跳过本地不存在的文件
            local = src.replace('assets/', '').split('?')[0]
            if src.startswith('http'):
                out.append(f'<img href="{esc(src)}" caption="{esc(alt)}"/>')
            else:
                path = img_prefix + local
                cap = f' caption="{esc(alt)}"' if alt else ''
                out.append(f'<img path="{esc(path)}"{cap}/>')
            i += 1
            continue

        # 表格
        if stripped.startswith('|') and i + 1 < n and is_sep(lines[i + 1]):
            header = split_row(lines[i])
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(split_row(lines[i]))
                i += 1
            th = ''.join(f'<th><p>{inline(c)}</p></th>' for c in header)
            body = ''
            for r in rows:
                tds = ''.join(f'<td><p>{inline(c)}</p></td>' for c in r)
                body += f'<tr>{tds}</tr>'
            out.append(f'<table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>')
            continue

        # 引用块
        if stripped.startswith('>'):
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            inner = '\n'.join(buf)
            # 引用块内可能有列表/加粗，用简单段落处理
            segs = [s for s in inner.split('\n') if s.strip()]
            ps = ''.join(f'<p>{inline(s.strip())}</p>' for s in segs)
            out.append(f'<blockquote>{ps}</blockquote>')
            continue

        # 无序列表
        if re.match(r'^\s*[-*+]\s+', line):
            items = []
            while i < n and re.match(r'^\s*[-*+]\s+', lines[i]):
                items.append(re.sub(r'^\s*[-*+]\s+', '', lines[i]).strip())
                i += 1
            lis = ''.join(f'<li>{inline(it)}</li>' for it in items)
            out.append(f'<ul>{lis}</ul>')
            continue

        # 有序列表
        if re.match(r'^\s*\d+\.\s+', line):
            items = []
            while i < n and re.match(r'^\s*\d+\.\s+', lines[i]):
                items.append(re.sub(r'^\s*\d+\.\s+', '', lines[i]).strip())
                i += 1
            lis = ''.join(f'<li>{inline(it)}</li>' for it in items)
            out.append(f'<ol>{lis}</ol>')
            continue

        # 代码块 ```
        if stripped.startswith('```'):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith('```'):
                buf.append(lines[i])
                i += 1
            i += 1
            code = esc('\n'.join(buf))
            out.append(f'<pre><code>{code}</code></pre>')
            continue

        # 普通段落（连续非空行合并）
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r'^\s*(#{1,6}\s|>|\||[-*+]\s|\d+\.\s|```|!\[)', lines[i]):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append(f'<p>{inline(" ".join(buf))}</p>')
        else:
            i += 1

    return '\n'.join(out)


def main():
    if len(sys.argv) < 3:
        print('用法: python md2feishu_xml.py <输入.md> <输出.xml>')
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding='utf-8') as f:
        md = f.read()
    xml_body = convert(md)
    title = os.path.splitext(os.path.basename(src))[0]
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(xml_body)
    n_img = xml_body.count('<img ')
    print(f'转换完成: {dst}')
    print(f'  图片标签: {n_img} 个')
    print(f'  字符数: {len(xml_body)}')


if __name__ == '__main__':
    main()