#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""校验飞书文档里的图片是否为真图（而不是「无法导入该图片」占位图）"""
import json
import os
import re
import subprocess
import sys

CLI = r'C:\Users\Administrator\.workbuddy\binaries\node\cli-connector-packages\lark-cli.cmd'


def fetch(doc):
    p = subprocess.run(
        [CLI, 'docs', '+fetch', '--doc', doc, '--doc-format', 'xml'],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    return json.loads(p.stdout)['data']['document']['content']


def main():
    for doc in sys.argv[1:]:
        c = fetch(doc)
        imgs = re.findall(r'<img[^>]*/?>', c)
        real = [i for i in imgs if 'default.png' not in i]
        print(f'=== {doc} ===')
        print(f'  图片 block 总数   : {len(imgs)}')
        print(f'  真实文件名的图    : {len(real)}')
        print(f'  占位图(default)  : {len(imgs) - len(real)}')
        print(f'  残留锚点ZZANCHOR  : {len(re.findall(r"ZZANCHOR", c))}')
        print(f'  发现应用          : {c.count("发现应用")}')
        print(f'  企鹅教师助手      : {c.count("企鹅教师助手")}')
        if real:
            m = re.search(r'name="([^"]+)"', real[0])
            w = re.search(r'width="(\d+)"', real[0])
            print(f'  示例              : {m.group(1) if m else "?"}'
                  f'  width={w.group(1) if w else "?"}')
        print()


if __name__ == '__main__':
    main()