#!/usr/bin/env bash
# ============================================================
# 即梦出图封装 —— 模型固定 4.7，出图后自动下载到本地
#
# 用法：
#   ./jimeng.sh pano "提示词"     VR 全景图   4096x2048 / 4k / 4 张
#   ./jimeng.sh tex  "提示词"     球体贴图    2048x1024 / 2k / 4 张
#   ./jimeng.sh test "提示词"     试水/插画   1024x1024 / 2k / 2 张
#
# 产物目录： threejs_cases/jimeng_out/<用途>_<时间戳>/
#   - 图片文件
#   - log.txt  完整提交与查询回执（含 submit_id，可用于事后追查）
#
# 说明：
#   - 即梦 CLI 没有配置文件，参数只能每次显式给，所以固化在这里。
#   - text2image 本身没有 -o 参数，图不会自动落盘；
#     必须先拿 submit_id，再用 query_result --download_dir 才能存到本地。
#   - gen_status=querying 只代表提交成功，不代表出图成功；
#     脚本只在看到 success 时才认为拿到图。
# ============================================================

set -uo pipefail

# 模型：用户指定 4.7（支持 2k / 4k，全景的 4096x2048 靠它）
MODEL="${DREAMINA_MODEL:-4.7}"
BIN="${DREAMINA_BIN:-$HOME/bin/dreamina.exe}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTBASE="$ROOT/jimeng_out"

KIND="${1:-}"
PROMPT="${2:-}"

if [ -z "$KIND" ] || [ -z "$PROMPT" ]; then
  cat >&2 <<'EOF'
用法: jimeng.sh <pano|tex|test> "提示词"

  pano  VR 全景图   4096x2048 / 4k / 4 张
  tex   球体贴图    2048x1024 / 2k / 4 张
  test  试水/插画   1024x1024 / 2k / 2 张

例: ./jimeng.sh test "月球表面环形山特写，等距圆柱投影贴图，无光影，无文字"
EOF
  exit 2
fi

case "$KIND" in
  pano) W=4096; H=2048; RES=4k; N=4;;
  tex)  W=2048; H=1024; RES=2k; N=4;;
  test) W=1024; H=1024; RES=2k; N=2;;
  *)    echo "未知用途: $KIND（只支持 pano / tex / test）" >&2; exit 2;;
esac

if [ ! -x "$BIN" ]; then
  echo "找不到即梦 CLI：$BIN" >&2
  echo "重新安装： curl -s https://jimeng.jianying.com/cli | bash" >&2
  exit 3
fi

# 登录态前置检查，免得白跑一次提交
if ! "$BIN" user_credit 2>&1 | grep -q 'credit'; then
  echo "当前没有有效登录态，请先执行： dreamina login" >&2
  "$BIN" user_credit 2>&1 | head -3 >&2
  exit 4
fi

STAMP="$(date +%Y%m%d_%H%M%S)"
DIR="$OUTBASE/${KIND}_${STAMP}"
mkdir -p "$DIR"
LOG="$DIR/log.txt"

echo "---------------------------------------------"
echo "模型    : $MODEL"
echo "尺寸    : ${W} x ${H}  ($RES)"
echo "数量    : ${N} 张"
echo "输出目录: $DIR"
echo "---------------------------------------------"

# ---------- 第一步：提交并等待 ----------
SUBMIT_OUT="$("$BIN" text2image \
  --prompt="$PROMPT" \
  --width="$W" --height="$H" \
  --resolution_type="$RES" \
  --model_version="$MODEL" \
  --generate_num="$N" \
  --poll=240 2>&1)"
printf '%s\n' "$SUBMIT_OUT" | tee -a "$LOG"

# ---------- 提取 submit_id（兼容 JSON / key=value / 裸十六进制） ----------
extract_sid() {
  local s="$1" v
  v="$(printf '%s' "$s" | grep -oE '"submit_id"[[:space:]]*:[[:space:]]*"[^"]+"' | head -1 | sed -E 's/.*"([^"]+)"[[:space:]]*$/\1/')"
  [ -n "$v" ] && { printf '%s' "$v"; return; }
  v="$(printf '%s' "$s" | grep -oE 'submit_id[[:space:]]*[=:][[:space:]]*[0-9a-zA-Z]+' | head -1 | sed -E 's/submit_id[[:space:]]*[=:][[:space:]]*//')"
  [ -n "$v" ] && { printf '%s' "$v"; return; }
  printf '%s' "$s" | grep -oE '\b[0-9a-f]{16,}\b' | head -1
}

SID="$(extract_sid "$SUBMIT_OUT")"

if [ -z "$SID" ]; then
  echo "!! 没能从输出里提取到 submit_id。请把上面这段输出发给助手看。" >&2
  exit 5
fi
echo "submit_id: $SID"

# ---------- 第二步：查结果并下载到本地 ----------
DL_OUT="$("$BIN" query_result --submit_id="$SID" --download_dir="$DIR" 2>&1)"
printf '%s\n' "$DL_OUT" | tee -a "$LOG"

if printf '%s' "$DL_OUT" | grep -qi 'fail'; then
  echo "" >&2
  echo "!! 任务失败，失败原因：" >&2
  printf '%s\n' "$DL_OUT" | grep -iE 'fail_reason|reason' | head -3 >&2
  exit 6
fi

if printf '%s' "$DL_OUT" | grep -qi 'AigcComplianceConfirmation'; then
  echo "" >&2
  echo "!! 该模型首次使用需要网页授权确认：" >&2
  echo "   打开即梦网页完成一次确认，然后重新运行本命令。" >&2
  exit 7
fi

# ---------- 第三步：清点本地文件 ----------
echo "---------------------------------------------"
echo "本地文件："
FOUND=0
while IFS= read -r f; do
  FOUND=$((FOUND+1))
  printf '  %s  (%s KB)\n' "$(basename "$f")" "$(( $(stat -c%s "$f") / 1024 ))"
done < <(find "$DIR" -type f ! -name 'log.txt' -size +4k 2>/dev/null | sort)

if [ "$FOUND" -eq 0 ]; then
  echo "  （目录里还没有图片文件）" >&2
  echo "" >&2
  echo "可能原因：任务仍在排队（gen_status=querying）。" >&2
  echo "稍后单独取图：" >&2
  echo "  $BIN query_result --submit_id=$SID --download_dir=\"$DIR\"" >&2
  exit 8
fi

echo "---------------------------------------------"
echo "完成：$FOUND 张图已存到本地"
echo "下一步交给助手验收（按 pano / tex 各自的清单逐条判断）"
