#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量生成 360VR 案例所需的 AI 图片（全景 + 热点特写）。清单驱动。

把要生成的图写进 scenes.json（格式见同目录 scenes.example.json，提示词按
《专题_360VR全景互动网页.md》「设计规则」一节的公式拼装），脚本逐条调用
生图 API 保存到 output_dir，最后输出成败报告。

默认按「火山方舟（豆包 seedream，与即梦同源）」接口编写；即梦官方 API /
通义万相 / 智谱 CogView 等，只需改下面三个环境变量；请求体不兼容的厂商
改 call_api() 里的 body 组装即可（都有"文生图"一个接口，字段大同小异）。

环境变量：
  GEN_API_KEY    必填。生图服务的 API Key。不要写进代码，不要提交仓库。
  GEN_BASE_URL   默认 https://ark.cn-beijing.volces.com/api/v3 （火山方舟北京）
  GEN_MODEL      默认 doubao-seedream-3-0-t2i-250415 （豆包·Seedream 文生图）
  GEN_WATERMARK  默认 false（去水印）。账号无此权限报错时，改成 true 或删掉该参数。

用法：
  export GEN_API_KEY=xxxxxxxx        # Git Bash；CMD 用 set GEN_API_KEY=xxxxxxxx
  py gen_images.py scenes.json

特性：
  - 已存在的文件默认跳过（不重复花钱），加 --force 强制全部重生成
  - 模型不支持 2:1 尺寸时自动兜底：先按厂商支持的尺寸生成，再拉伸/裁切到 2:1
  - 单张失败重试 1 次，最终输出 missing 报告
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from io import BytesIO

BASE_URL = os.environ.get("GEN_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
MODEL = os.environ.get("GEN_MODEL", "doubao-seedream-3-0-t2i-250415")
API_KEY = os.environ.get("GEN_API_KEY", "")
WATERMARK = os.environ.get("GEN_WATERMARK", "false").lower() == "true"

PANORAMA_RATIO = 2.0   # 全景固定 2:1


def call_api(prompt, size):
    """调一次文生图接口，返回图片二进制。其余厂商改这里。"""
    body = {
        "model": MODEL,
        "prompt": prompt,
        "size": size,
        "response_format": "b64_json",
    }
    if not WATERMARK:
        body["watermark"] = False   # 方舟参数；无权限报错时设 GEN_WATERMARK=true
    req = urllib.request.Request(
        BASE_URL.rstrip("/") + "/images/generations",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + API_KEY,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read().decode("utf-8"))
    item = data["data"][0]
    if "b64_json" in item:
        return base64.b64decode(item["b64_json"])
    # 有些厂商只回 URL
    with urllib.request.urlopen(item["url"], timeout=120) as r:
        return r.read()


def save_with_ratio(raw, out_path, target_ratio):
    """按目标宽高比落盘：接近则原样保存；全景偏窄则拉伸，偏宽则居中裁切。"""
    from PIL import Image
    img = Image.open(BytesIO(raw)).convert("RGB")
    w, h = img.size
    now = w / h
    if abs(now - target_ratio) < 0.02:
        img.save(out_path, quality=90)
        return f"{w}x{h}"
    if target_ratio > now:
        img = img.resize((int(h * target_ratio + 0.5), h))       # 全景轻度拉伸可接受
    else:
        new_w = int(h * target_ratio + 0.5)
        x0 = (w - new_w) // 2
        img = img.crop((x0, 0, x0 + new_w, h))                   # 特写图裁掉两边
    img.save(out_path, quality=90)
    return f"{img.size[0]}x{img.size[1]} (由 {w}x{h} 调整)"


def main():
    if not API_KEY:
        print("未设置 GEN_API_KEY 环境变量。")
        print("  Git Bash:  export GEN_API_KEY=你的key")
        print("  CMD:       set GEN_API_KEY=你的key")
        print("key 在火山方舟控制台（或对应厂商后台）创建，切勿提交进仓库。")
        sys.exit(1)

    list_path = sys.argv[1] if len(sys.argv) > 1 else "scenes.json"
    force = "--force" in sys.argv
    with open(list_path, encoding="utf-8") as f:
        cfg = json.load(f)
    out_dir = cfg.get("output_dir", "assets")
    os.makedirs(out_dir, exist_ok=True)

    ok, skipped, failed = [], [], []
    for item in cfg["items"]:
        name = item["file"]
        out_path = os.path.join(out_dir, name)
        if os.path.isfile(out_path) and not force:
            skipped.append(name)
            print(f"跳过（已存在）: {name}")
            continue
        target = PANORAMA_RATIO if item.get("type") == "panorama" else None
        size = item.get("size", "2048x1024" if target else "1152x864")
        print(f"生成: {name}  [{size}] ...")
        raw = None
        for attempt in (1, 2):
            try:
                raw = call_api(item["prompt"], size)
                break
            except urllib.error.HTTPError as e:
                print(f"  第{attempt}次失败: HTTP {e.code} {e.read().decode('utf-8', 'ignore')[:200]}")
            except Exception as e:
                print(f"  第{attempt}次失败: {e}")
            time.sleep(2)
        if raw is None:
            failed.append(name)
            continue
        note = save_with_ratio(raw, out_path, target) if target else save_with_ratio(raw, out_path, 1.0)
        # type=image 时不强制比例：按生成原样保存
        ok.append((name, note))
        print(f"  完成: {name}  {note}")
        time.sleep(1)   # 轻微限速

    print(f"\n=== 报告 === 成功 {len(ok)} | 跳过 {len(skipped)} | 失败 {len(failed)}")
    for name in failed:
        print(f"  失败待重跑: {name}")
    if failed:
        print("修复提示词后重跑同一条命令即可（已成功的会自动跳过）。")


if __name__ == "__main__":
    main()
