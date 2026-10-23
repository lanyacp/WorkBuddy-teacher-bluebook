# vr_cases —— 360VR 专题两个操作案例的可运行成品

配套教程：`../专题_360VR全景互动网页.md`「操作案例」一节（含全部提示词与实机截图）。

## 目录

```
vr_cases/
├── gen_placeholder_assets.py   ← 示意素材生成脚本（py 运行，可重复执行）
├── gen_images.py               ← AI 批量生图脚本（清单驱动，配合教程「设计规则」）
├── scenes.example.json         ← 生图清单示例（庐山 4 全景 + 1 热点特写，提示词已按五槽公式拼好）
├── simple/                     ← 最小进阶示例（step1/2/3，已实跑验证：单场景 → 热点标签 → 多场景漫游）
│   ├── step1.html              ← 第 1 步：一个场景
│   ├── step2.html              ← 第 2 步：热点标签（多标签弹卡）
│   ├── step3.html              ← 第 3 步：多场景 + 淡入淡出 + 返回
│   └── assets/                 ← 4 张庐山示意全景图
├── lushan/                     ← 案例一《题西林壁》四个视角观庐山
│   ├── index.html              ← 单文件网页，双击无效，必须走 HTTP
│   └── assets/                 ← 4 张全景图 + hotspot.png
└── fraction_castle/            ← 案例二《分数的初步认识》分数城堡五关闯关
    ├── index.html
    └── assets/                 ← 6 张全景图 + hotspot.png
```

## 最小进阶示例怎么跑

```bash
cd simple
python -m http.server 8080
# 浏览器打开 http://localhost:8080/step1.html → step2 → step3
```

## 用生图 key 批量生成正式素材（即梦 / 豆包等）

```bash
export GEN_API_KEY=你的key          # CMD: set GEN_API_KEY=你的key；key 勿入库
cp scenes.example.json scenes.json  # 复制一份改成自己的场景与提示词
py gen_images.py scenes.json
```

默认走火山方舟（豆包 Seedream，即梦同源）；其它厂商改 `GEN_BASE_URL` / `GEN_MODEL` 两个环境变量。详见教程「设计规则」一节。

## 怎么跑

```bash
cd vr_cases            # 本目录
python -m http.server 8080
# 浏览器打开 http://localhost:8080/lushan/ 或 /fraction_castle/
```

⚠️ 直接双击 index.html（file:// 方式）会报 CORS、图出不来。

## 关于 assets/ 里的全景图

**当前是程序化生成的示意版**（扁平插画风，2:1 等矩形、左右无缝），
作用是让两个案例拿到手就能跑通全流程。

正式使用时按教程案例一/案例二里的素材提示词用 AI 生成（或实拍），
**同名覆盖 assets/ 下对应的 jpg 即可**，代码不用改。

想重新生成示意版：

```bash
py gen_placeholder_assets.py
```

## 两个案例实测记录（2026-10-23，WorkBuddy 仓库内实跑）

- 案例一：四个视角切换、淡入淡出、面板/诗句联动、热点点击全部通过
- 案例二：入口 5 热点、顺序解锁、切饼 → 得星 → 解锁下一关全部通过
- 已知问题（教程踩坑表已收录）：切场景后相机朝向不自动重置
