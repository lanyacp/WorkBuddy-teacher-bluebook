# 企鹅教师助手真实界面截图脱敏 + 规范化
# 目标：抹掉个人任务名 / 用户名 / 工作区名，保留教学界面主体
import glob
import os

from PIL import Image, ImageDraw

SRC = r'C:\Users\Administrator\.workbuddy\clipboard-images'
DST = r'D:\projects\WorkBuddy\2026-06-17-11-18-20\教师版蓝皮书\assets_opt'

FILES = {
    '713Z-15c51d49': 'penguin_teaching_design.png',   # 教学设计模式
    '717Z-d7c435b9': 'penguin_home_school.png',        # 家校共育 + 专家技能连接器菜单
    '718Z-8c5efaf1': 'penguin_growth.png',             # 专业成长模式
    '720Z-be42a870': 'penguin_discover_apps.png',      # 发现应用 / Buddy 应用列表
}

files = sorted(glob.glob(os.path.join(SRC, 'clipboard-2026-10-08T08-28-43-*.jpg')))
assert len(files) == 4, files

SIDEBAR_BG = (236, 242, 254)


def fill_sidebar(draw, box, bg):
    draw.rectangle(box, fill=bg)


for f in files:
    key = [k for k in FILES if k in os.path.basename(f)][0]
    out_name = FILES[key]
    im = Image.open(f).convert('RGB')
    W, H = im.size
    d = ImageDraw.Draw(im)

    if 'be42a870' in key:
        # 图4：下拉菜单压在侧边栏上（面板 x≈158..445, y≈80..605）
        # 面板左侧露出的侧边栏（含个人任务名）填平
        fill_sidebar(d, (0, 0, 158, H), SIDEBAR_BG)
        # 面板下方露出的侧边栏（空间名/用户名）填平
        fill_sidebar(d, (0, 605, 158, H), SIDEBAR_BG)
    elif 'd7c435b9' in key:
        # 图2：专家/技能/连接器菜单浮在侧边栏上（面板 x≈96..300, y≈152..242）
        # 先把整条侧边栏填平，再把菜单面板区域挖回来（面板本身是纯白）
        fill_sidebar(d, (0, 0, 296, H), SIDEBAR_BG)
        panel = im.crop((96, 152, 302, 243))
        im.paste(panel, (96, 152))
    else:
        # 图1/3：整条侧边栏填平（侧边栏右边界 x=295）
        fill_sidebar(d, (0, 0, 296, H), SIDEBAR_BG)

    # 统一裁掉顶部标题栏（保留内容区），并压到 1200px 宽
    top = 28
    im2 = im.crop((0, top, W, H))
    if im2.width > 1200:
        nh = int(im2.height * 1200 / im2.width)
        im2 = im2.resize((1200, nh), Image.LANCZOS)

    out = os.path.join(DST, out_name)
    im2.save(out, optimize=True)
    print('saved', out_name, im2.size, f'{os.path.getsize(out)/1024:.0f}KB')
