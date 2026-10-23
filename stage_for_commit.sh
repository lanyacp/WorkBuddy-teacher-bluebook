#!/usr/bin/env bash
# 一键暂存：排除不该入库的内容（Windows Git Bash + 中文路径）
# 为什么要写脚本：.gitignore 对顶层中文目录名匹配不可靠，
# 每次 git add -A 都会把「英语课程资料」加回来，必须显式移除。
set -e
cd "$(dirname "$0")"
export PATH="/c/Users/Administrator/.workbuddy/binaries/PortableGit/versions/1.2.0/usr/bin:$PATH"

PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"

git add -A

# 排除顶层中文目录（用 Python 处理，避免命令行中文编码问题）
"$PY" - <<'PYEOF'
import subprocess, os, sys

# 需要排除的路径片段（顶层目录）
EXCLUDE_KEYS = ['英语课程资料', 'assets_from_pdf']

out = subprocess.run(['git', 'diff', '--cached', '--name-only', '-z'],
                     capture_output=True).stdout.decode('utf-8')
files = [f for f in out.split('\0') if f]

targets = [f for f in files if any(k in f for k in EXCLUDE_KEYS)]
# 只排蓝皮书高清图库 assets/（VR 案例的 */assets/ 是运行必需，保留）
extra = [f for f in files if f.startswith('教师版蓝皮书/assets/')]
targets = sorted(set(targets + extra))

if not targets:
    print('[skip] 无需排除的内容')
    sys.exit(0)

lst = os.path.join('.git', '_exclude_list.txt')
with open(lst, 'w', encoding='utf-8') as f:
    f.write('\n'.join(targets))

n = 0
for i in range(0, len(targets), 30):
    batch = targets[i:i + 30]
    p = subprocess.run(['git', 'rm', '-r', '--cached', '-q', '--'] + batch,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if p.returncode == 0:
        n += len(batch)
    else:
        print('  失败 %d 个: %s' % (len(batch), p.stderr[:100]))
os.remove(lst)
print('[排除] %d 个文件（英语课程资料 / assets / assets_from_pdf）' % n)

# 复核
out = subprocess.run(['git', 'diff', '--cached', '--name-only', '-z'],
                     capture_output=True).stdout.decode('utf-8')
files = [f for f in out.split('\0') if f]
sizes = [(f, os.path.getsize(f)) for f in files if os.path.isfile(f)]
bad = [f for f in files if any(k in f for k in EXCLUDE_KEYS) or '/assets/' in f]
print('[复核] 入库 %d 文件 / %.2f MB / 最大 %.2f MB' % (
    len(files), sum(s for _, s in sizes) / 1024 / 1024,
    max(s for _, s in sizes) / 1024 / 1024))
print('[复核] 应排除项残留: %d' % len(bad))
print('[复核] assets_opt 图片: %d 张' % len([f for f in files if 'assets_opt' in f]))
PYEOF