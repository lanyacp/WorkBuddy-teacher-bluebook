# -*- coding: utf-8 -*-
"""
把带 <style> 块的 HTML 转成「微信能保住格式」的内联样式 HTML。

为什么需要这一步：
微信公众号编辑器不认 <style> 标签，只认写在元素上的 style=""。
带 <style> 的稿子直接复制粘贴或直接推送，class 全部失效，看起来就是"格式没了"。

它额外做了三件微信专属的脏活：
  1. 解析 :root 里的 CSS 变量，把 var(--x) 换成真实色值（微信不认 CSS 变量）
  2. 渐变背景补一层纯色兜底（微信可能剥掉 linear-gradient，白字会消失）
  3. 宽度/内边距适配手机（880px 容器 → 677px，微信图文标准宽度）

用法：
    python inline_wechat.py 输入.html [输出.html] [--no-fit]

--no-fit  只做内联，不改版式（适合本来就是 677px 的稿子）
不传输出名时，默认在原名后加「_微信版」。
依赖：premailer（pip install premailer）
"""
import io
import os
import re
import sys
import urllib.parse

from premailer import transform

# 手机适配：内联前追加到 </style> 之前，后定义的规则覆盖前面的
FIT_CSS = """
.wrap{max-width:677px;padding:22px 14px 36px}
body{font-size:16px;line-height:1.85;background:#fff}
p{font-size:16px;line-height:1.9}
.card{padding:20px 16px;border-radius:12px;margin-bottom:16px}
.cover{padding:26px 20px;border-radius:12px}
.cover h1{font-size:23px}
.step{margin-bottom:18px}
.step .head{padding:13px 16px;background-color:#2f6fed}
.step .head .t{font-size:17px}
.step .bd{padding:16px 16px 18px}
.blk{padding:13px 14px}
.copy{padding:14px 14px}
.mock{padding:14px 15px}
.toc{padding:16px 18px}
.note{padding:12px 14px}
.qa{padding:13px 14px}
h2{font-size:18px;margin:26px 0 12px}
h3{font-size:16px;margin:20px 0 9px}
"""


def resolve_css_vars(html):
    """把 :root{--x:val} 收集成表，再把全文 var(--x) 换成真实值。"""
    table = {}
    for block in re.findall(r":root\s*\{([^}]*)\}", html):
        # 值后面可能是 ; 也可能是块尾的 }，两个都要认，否则最后一个变量会漏解析
        for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;}]+)", block):
            table[m.group(1)] = m.group(2).strip()

    def _sub(m):
        name = m.group(1)
        return table.get(name, m.group(2) or "")

    # var(--x) 或 var(--x, 兜底值)
    html = re.sub(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)", _sub, html)
    return html, table


def backup_gradients(html):
    """渐变后面补一句纯色，防止微信剥掉渐变后白字看不见。"""
    def _sub(m):
        decl = m.group(0)
        colors = re.findall(r"#[0-9a-fA-F]{6}", m.group(1))
        if not colors:
            return decl
        return decl + ";background-color:" + colors[0]

    return re.sub(
        r"background\s*:\s*(linear-gradient\([^;]*\))", _sub, html
    )


def demote_pseudo_elements(html):
    """
    把 X::before{content:"Y";...} 降级成真实 <span>。

    伪元素只能写在 <style> 里，而微信会整块剥掉 <style>，所以这类"Q/A 小徽标"
    会静默消失。这里把 content 里的文字变成一个真实的 span，样式照搬，必定保留。
    """
    count = 0
    for m in re.finditer(r"([^{}]+?)::before\s*\{([^}]*)\}", html):
        selector, decls = m.group(1).strip(), m.group(2)
        cm = re.search(r"""content\s*:\s*["']([^"']*)["']""", decls)
        if not cm or not cm.group(1):
            continue
        text = cm.group(1)

        # 去掉 content，剩下的声明直接当内联样式用
        style = re.sub(r"""content\s*:\s*["'][^"']*["']\s*;?""", "", decls)
        style = re.sub(r"\s*;+\s*", ";", style).strip().strip(";")
        span = '<span style="%s">%s</span>' % (style, text)

        # 选择器取最后一段（.qa .q::before → q），给该 class 的元素开头插入
        cls = re.findall(r"\.([A-Za-z0-9_-]+)", selector)
        if not cls:
            continue
        target = cls[-1]
        pat = re.compile(r'(<(\w+)[^>]*class="[^"]*\b' + re.escape(target) + r'\b[^"]*"[^>]*>)')

        def _ins(mm):
            return mm.group(1) + span

        html, n = pat.subn(_ins, html)
        count += n
    return html, count


def strip_leftover_styles(html):
    """premailer 会把无法内联的规则（伪元素、nth-child、:root）留在 <style> 里。
    微信反正会剥掉，留着只会让编辑器误处理，直接删干净。"""
    return re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.S)


def inline_file(src, out=None, fit=True):
    if out is None:
        base, ext = os.path.splitext(src)
        out = base + "_微信版" + ext

    html = io.open(src, encoding="utf-8").read()
    before = len(re.findall(r'style="', html))

    html, var_table = resolve_css_vars(html)
    html = backup_gradients(html)
    html, badge_count = demote_pseudo_elements(html)

    if fit:
        html = re.sub(r"</style>", FIT_CSS + "\n</style>", html, count=1)

    # 不传 base_url：否则 premailer 会把图片的相对路径改写成 file:// 绝对地址并做
    # URL 编码，后续推送脚本按本地文件去读就会找不到。保持相对路径，交给推送脚本处理。
    res = transform(
        html,
        keep_style_tags=False,  # 微信不认 <style>，转完就删掉
        remove_classes=False,   # class 留着无害，也方便回看
    )

    # lxml 序列化时会把中文文件名转义成 %E4%B8%BB...，导致推送脚本按本地路径读不到文件。
    # 对本地相对路径做一次解码还原（http/data 的不动）。
    def _unquote_local(m):
        pre, val, post = m.group(1), m.group(2), m.group(3)
        if "://" in val or val.startswith(("data:", "//")):
            return m.group(0)
        return pre + urllib.parse.unquote(val) + post

    res = re.sub(r'(<img[^>]*\ssrc=")([^"]+)(")', _unquote_local, res, flags=re.I)
    res = re.sub(r'(<a[^>]*\shref=")([^"]+)(")', _unquote_local, res, flags=re.I)
    res = strip_leftover_styles(res)

    after = len(re.findall(r'style="', res))
    io.open(out, "w", encoding="utf-8").write(res)

    print("输入  %s  (%.1f KB, 内联 style %d 处)" % (os.path.basename(src), os.path.getsize(src) / 1024, before))
    print("输出  %s  (%.1f KB, 内联 style %d 处)" % (os.path.basename(out), os.path.getsize(out) / 1024, after))
    print("CSS 变量: 解析 %d 个, 残留 var() %d 处" % (len(var_table), len(re.findall(r"var\(", res))))
    print("手机适配:", "已开启" if fit else "关闭")
    print("伪元素降级: %d 处（Q/A 徽标已变成真实 span）" % badge_count)
    print("残留 <style> 块:", bool(re.search(r"<style[\s>]", res)))

    srcs = re.findall(r'<img[^>]*\ssrc="([^"]+)"', res, flags=re.I)
    local = [s for s in srcs if "://" not in s and not s.startswith("data:")]
    missing = [s for s in local if not os.path.exists(s)]
    print("图片 %d 张, 本地 %d 张, 找不到 %s" % (len(srcs), len(local), missing or "无"))
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)
    inline_file(args[0], args[1] if len(args) > 1 else None, fit=("--no-fit" not in flags))
