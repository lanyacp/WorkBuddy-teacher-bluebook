#!/bin/bash
# 公众号草稿推送（服务器版，走官方 API，图片自动传图床）
cd "$(dirname "$0")"

APPID="wx21e33dcc3d10cb6b"
AUTHOR="${WECHAT_AUTHOR:-李亚威}"
TITLE="做一个能转的 360 课堂网页"
DIGEST="五步做出能拖着转的课堂网页，不写代码不装软件。每一步写清点哪里、会看到什么、卡住怎么办，另附 13 个常见问题。"

if [ -z "$WECHAT_SECRET" ]; then
  printf "请输入公众号 AppSecret（输入不回显）: "
  read -s WECHAT_SECRET
  echo
fi
if [ -z "$WECHAT_SECRET" ]; then echo "没拿到 AppSecret，退出"; exit 1; fi

export WECHAT_APPID="$APPID"
export WECHAT_SECRET="$WECHAT_SECRET"
export WECHAT_AUTHOR="$AUTHOR"
export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1

echo "== 检查 Python =="
python3 -V || { echo "没有 python3"; exit 1; }

echo
echo "== [1/2] 试跑：上传图片并替换，不建草稿 =="
python3 push_draft_server.py --html article.html --title "$TITLE" --digest "$DIGEST" --dry-run
if [ $? -ne 0 ]; then echo "试跑失败，看上面的报错"; exit 1; fi

echo
printf "试跑 OK 吗？确认正式推送请输入 y ："
read YN
if [ "$YN" != "y" ]; then echo "已取消，没建草稿"; exit 0; fi

echo
echo "== [2/2] 正式推送，含封面 =="
python3 push_draft_server.py --html article.html --title "$TITLE" --digest "$DIGEST" --cover cover.png
echo
echo "完成。去 mp.weixin.qq.com → 内容管理 → 草稿箱 查看。"
