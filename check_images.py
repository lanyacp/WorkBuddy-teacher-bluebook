"""校验蓝皮书各 md 里的图片引用是否都有对应文件，并统计复用情况。"""
import os
import re
import sys

BASE = "教师版蓝皮书"


def main():
    total_ref = 0
    missing = []
    per_file = {}

    for fn in sorted(os.listdir(BASE)):
        if not fn.endswith(".md"):
            continue
        path = os.path.join(BASE, fn)
        with open(path, encoding="utf-8") as f:
            body = f.read()
        refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", body)
        ok = 0
        for r in refs:
            if r.startswith("http"):
                continue
            total_ref += 1
            p = os.path.join(BASE, r)
            if os.path.isfile(p):
                ok += 1
            else:
                missing.append((fn, r))
        if refs:
            per_file[fn] = (ok, len(refs))

    print("=== 各文件图片引用 ===")
    for fn, (ok, tot) in per_file.items():
        flag = "" if ok == tot else "   <-- 有缺失"
        print(f"  {fn:<36} {ok}/{tot}{flag}")

    print(f"\n合计引用 {total_ref} 张，缺失 {len(missing)} 张")
    for fn, r in missing[:25]:
        print(f"  MISSING  {fn}  ->  {r}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())