#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""下载飞书文档里指定关键词之后的图片，验证内容是否为企鹅教师助手真实界面"""
import json
import os
import re
import subprocess

CLI = r'C:\Users\Administrator\.workbuddy\binaries\node\cli-connector-packages\lark-cli.cmd'
ENV = dict(os.environ)
ENV['PATH'] = ('/c/Users/Administrator/.workbuddy/binaries/PortableGit/versions/1.2.0/usr/bin:'
               '/c/Users/Administrator/.workbuddy/binaries/PortableGit/versions/1.2.0/mingw64/bin:'
               '/usr/bin:/bin:/c/Windows/System32:' + ENV.get('PATH', ''))
BASE = r'D:\projects\WorkBuddy\2026-06-17-11-18-20'

DOC = 'EhtidUe3moDtTExY5qdc1SIRnrd'
KW = sys_kw = '找到「发现应用」' if False else None


def sh(args):
    p = subprocess.run(args, capture_output=True, text=True, env=ENV,
                       encoding='utf-8', errors='replace', cwd=BASE)
    return p.stdout or ''


out = sh([CLI, 'docs', '+fetch', '--doc', DOC])
data = json.loads(out)
content = data['data']['document']['content']

# 抓所有 img 标签及其后续 caption
imgs = re.findall(r'<img[^>]*name="([^"]+)"[^>]*/>', content)
print('img count', len(imgs))
for n, name in enumerate(imgs):
    print(n, name)
