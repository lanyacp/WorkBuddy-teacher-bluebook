"""下载 WorkBuddyGuide 原书蓝皮书的第一篇（基础操作篇）正文与配图。

用途：教师版蓝皮书直接复用原书已验证的操作步骤与界面截图，
     避免重新造轮子、也避免自己截图。
"""
import json
import os
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://raw.githubusercontent.com/AlephAITech/WorkBuddyGuide/main/"
TREE = "D:/projects/WorkBuddy/2026-06-17-11-18-20/_wb_tree.json"
OUT = "D:/projects/WorkBuddy/2026-06-17-11-18-20/_ref_raw"

# 需要抓取的篇章（教师版第一篇「先把工具用起来」主要复用这些）
WANT_PREFIXES = (
    "docs/bluebook/第一篇",
    "docs/bluebook/附录",
)


def load_paths():
    with open(TREE, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for node in data.get("tree", []):
        p = node.get("path", "")
        if not p.startswith(WANT_PREFIXES):
            continue
        if p.endswith("/"):
            continue
        if node.get("type") != "blob":
            continue
        out.append(p)
    return out


def safe_name(path):
    """把原路径压成安全的本地相对路径：保留两级目录 + 文件名"""
    rel = path[len("docs/bluebook/"):]
    parts = rel.split("/")
    if len(parts) == 1:
        return "index.md"
    chapter = re.sub(r'[\\/:*?"<>|]', "_", parts[-2])
    fname = re.sub(r'[\\/:*?"<>|]', "_", parts[-1])
    return f"{chapter}/{fname}"


def fetch(rel):
    dest = os.path.join(OUT, rel)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return ("SKIP", rel, os.path.getsize(dest))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    url = BASE + urllib.parse.quote(path_of[rel])
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=60).read()
            with open(dest, "wb") as f:
                f.write(data)
            return ("OK", rel, len(data))
        except Exception as e:  # noqa: BLE001
            if attempt == 2:
                return ("FAIL", rel, str(e)[:120])
    return ("FAIL", rel, "unknown")


path_of = {}

if __name__ == "__main__":
    paths = load_paths()
    mds = [p for p in paths if p.endswith(".md")]
    imgs = [p for p in paths if p.lower().endswith((".png", ".gif", ".jpg", ".jpeg"))]
    print(f"待下载：正文 {len(mds)} 个，配图 {len(imgs)} 张")

    for p in paths:
        path_of[safe_name(p)] = p

    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(fetch, list(path_of.keys())):
            results.append(r)

    ok = sum(1 for r in results if r[0] in ("OK", "SKIP"))
    fail = [r for r in results if r[0] == "FAIL"]
    total_bytes = sum(r[2] for r in results if isinstance(r[2], int))
    print(f"完成：成功 {ok}/{len(results)}，失败 {len(fail)}，共 {total_bytes/1024/1024:.1f} MB")
    for f in fail[:15]:
        print("  FAIL", f[1], f[2])