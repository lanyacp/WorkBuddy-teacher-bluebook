#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把 md 正文+ 图片按正确位置写入飞书文档。

踩坑结论（2026-10-08 实测）：
- `drive +import`：markdown 里的本地图片会变成 22KB 占位图「无法导入该图片…」，
  页面上看不到。文字正常。
- `docs +create --doc-format markdown`：`![]()` 直接丢弃。
- `docs +create --content x.xml`：`<img path="@./a.png"/>` 也丢弃。
- **唯一能真正上传图片的是 `docs +media-insert --doc TOKEN --file 本地路径 --type image`**。

所以流程变成：
  1. import 一份「纯文字 + 锚点段落」文档（每个图片位置留一段可定位的锚点文字）
  2. 逐张 media-insert，插到该锚点所在 block 的后面（block_insert_after）
  3. 全部插完后再删掉锚点段落

用法: python push_to_feishu.py <md文件> <飞书文档名>
"""
import json
import os
import re
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
# lark-cli 是 node 包，Windows 下必须用 .cmd 入口，不能靠 PATH
CLI = r'C:\Users\Administrator\.workbuddy\binaries\node\cli-connector-packages\lark-cli.cmd'
ENV = dict(os.environ)
ENV['PATH'] = (
    '/c/Users/Administrator/.workbuddy/binaries/PortableGit/versions/1.2.0/usr/bin:'
    '/c/Users/Administrator/.workbuddy/binaries/PortableGit/versions/1.2.0/mingw64/bin:'
    '/usr/bin:/bin:/c/Windows/System32:' + ENV.get('PATH', '')
)


def sh(args, cwd=None):
    p = subprocess.run(args, capture_output=True, text=True, env=ENV,
                       encoding='utf-8', errors='replace',
                       cwd=cwd or BASE)
    return (p.stdout or '') + (p.stderr or '')


def main():
    if len(sys.argv) < 3:
        print('用法: python push_to_feishu.py <md文件> <飞书文档名>')
        sys.exit(1)
    md = sys.argv[1]
    title = sys.argv[2]
    MD_DIR = os.path.dirname(os.path.abspath(md)) or'.'
    name = os.path.splitext(os.path.basename(md))[0]
    pure = os.path.join(MD_DIR, f'_pure_{name}.md')

    # ---- 1. 剥离图片，留锚点（锚点必须独占一行，才能成为独立 block）----
    with open(md, encoding='utf-8') as f:
        lines = f.read().split('\n')
    out, items = [], []
    for ln in lines:
        m = re.fullmatch(r'\s*!\[([^\]]*)\]\(([^)]+)\)\s*', ln)
        if m:
            alt, src = m.group(1), m.group(2)
            anchor = f'ZZANCHOR{len(items):03d}ZZ'
            items.append((anchor, src, alt))
            out.append('')          # 空行分隔
            out.append(anchor)     # 独占一行
        else:
            out.append(ln)
    with open(pure, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'[1] 剥离完成：{len(items)} 处配图')

    # ---- 2. 导入纯文字 ----
    r = sh([CLI, 'drive', '+import', '--file', pure, '--type', 'docx', '--name', title])
    mu = re.search(r'"url":\s*"(https://[^\"]+)"', r)
    if not mu:
        print('导入失败：', r[:500])
        sys.exit(1)
    url = mu.group(1)
    token = url.rsplit('/', 1)[-1]
    print(f'[2] 文字版已导入：{url}')
    time.sleep(2)

    # ---- 3. 定位所有锚点block ----
    r = sh([CLI, 'docs', '+fetch', '--doc', token,
            '--doc-format', 'xml', '--detail', 'with-ids'])
    blocks = r
    # 建立 锚点文字 -> block_id 映射
    anchors = {}
    # fetch 返回 JSON，先取出 content 字段（此时引号已正常，无需处理转义）
    content = blocks
    try:
        content = json.loads(blocks)['data']['document']['content']
    except Exception:
        pass
    pat = re.compile(
        r'<(\w+)\s+id="([A-Za-z0-9]{15,})"[^>]*>\s*ZZANCHOR(\d{3})ZZ\s*</\1>')
    for mm in pat.finditer(content):
        anchors[int(mm.group(3))] = mm.group(2)
    print(f'[3] 定位锚点 {len(anchors)}/{len(items)}')
    if len(anchors) < len(items):
        print('    ⚠️ 部分锚点未定位，将退回文末追加')

    # ---- 4. 逐张上传并插到对应锚点后 ----
    ok, fail = 0, []
    for idx, (anchor, src, alt) in enumerate(items):
        p = os.path.join(MD_DIR, src)
        if not os.path.isfile(p):
            fail.append((src, '文件不存在'))
            continue
        # 4a. 先上传，拿到图片 block_id
        r = sh([CLI, 'docs', '+media-insert', '--doc', token,
                '--file', p, '--type', 'image']
               + (['--caption', alt] if alt else []))
        mu = re.search(r'"block_id":\s*"([A-Za-z0-9]+)"', r)
        if not mu:
            fail.append((src, r[:100]))
            continue
        img_block = mu.group(1)
        ok += 1
        # 4b. 移动到锚点之后
        bid = anchors.get(idx)
        if bid:
            rr = sh([CLI, 'docs', '+update', '--doc', token,
                     '--command', 'block_move_after',
                     '--block-id', bid, '--src-block-ids', img_block])
            if '"ok": true' not in rr:
                #移动失败就保留在文末，不算失败
                pass
        if ok % 10 == 0:
            print(f'    {ok}/{len(items)}')
        time.sleep(0.05)

    print(f'[4] 图片上传 {ok}/{len(items)}')
    for s, e in fail:
        print('   失败：', s, e[:80])

    # ---- 5. 删掉锚点文字 ----
    removed = 0
    for idx, bid in sorted(anchors.items(), key=lambda kv: -kv[0]):
        rr = sh([CLI, 'docs', '+update', '--doc', token,
                 '--command', 'block_delete', '--block-id', bid])
        if '"ok": true' in rr:
            removed += 1
    print(f'[5] 锚点清理 {removed}/{len(anchors)}')

    os.remove(pure)
    print('\n完成：', url)


if __name__ == '__main__':
    main()