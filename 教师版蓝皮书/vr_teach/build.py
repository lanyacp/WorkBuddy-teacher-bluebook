#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 index.src.html（源文件）+ assets/*.jpg 打包成 index.html（成品，双击即用）。

为什么必须打包？
  在 file:// 协议下，Chrome 把每个本地文件都当作独立来源（opaque origin），
  WebGL 的 texImage2D 会拒绝上传 <img> 元素：
      "The image element contains cross-origin data, and may not be loaded"
  结果就是全景画面全黑。
  把图片转成 base64 data URI 内嵌进 HTML 就没有这个问题，
  而且老师只需要「双击一个文件」，不用管 assets 目录。

用法：
  python build.py
  → 生成 index.html（成品，可直接发给学生）
"""
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "index.src.html"
OUT = ROOT / "index.html"

BLOCK_PAT = re.compile(
    r'(<script\s+id="(?P<id>[^"]+)"\s+type="text/plain"\s*>)(?P<body>.*?)(?P<close></script>)',
    re.S,
)


def to_data_uri(path: pathlib.Path) -> str:
    mime = "image/jpeg" if path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def fill_blocks(html: str) -> tuple[str, list[str]]:
    """把每个 <script id="pano_N" type="text/plain"> 块填上对应 assets 图片的 base64。"""
    done = []

    def repl(m: re.Match) -> str:
        bid = m.group("id")
        for ext in (".jpg", ".jpeg", ".png"):
            p = ROOT / "assets" / f"{bid}{ext}"
            if p.exists():
                uri = to_data_uri(p)
                done.append(f"{bid}{ext} ({p.stat().st_size/1024:.0f} KB → {len(uri)/1024:.0f} KB)")
                # 注意必须用命名组 close：group(3) 是 body 而不是 </script>
                return m.group(1) + uri + m.group("close")
        print(f"  ! 缺图：assets/{bid}.jpg")
        return m.group(0)

    return BLOCK_PAT.sub(repl, html), done


def main() -> int:
    if not SRC.exists():
        print("找不到 index.src.html")
        return 1

    html = SRC.read_text(encoding="utf-8")
    open_tags_before = html.count("<script")
    close_before = html.count("</script>")
    html, done = fill_blocks(html)

    if not done:
        print("没有找到任何 <script id=\"pano_N\" type=\"text/plain\"> 占位块")
        return 1

    # 结构自检：填充不得破坏标签配对，否则浏览器会把后续 <script> 当成纯文本吞掉
    if html.count("</script>") != close_before or html.count("<script") != open_tags_before:
        print("  ! 标签配对被破坏，拒绝输出")
        return 1

    for line in done:
        print(f"  √ 内嵌 {line}")

    OUT.write_text(html, encoding="utf-8")
    size = OUT.stat().st_size / 1024 / 1024
    print(f"\n完成：{OUT.name}   {size:.2f} MB")
    print("双击即可打开，零依赖、零联网。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
