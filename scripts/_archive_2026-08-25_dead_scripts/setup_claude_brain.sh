#!/usr/bin/env bash
# ============================================================
# setup_claude_brain.sh — Mac/Linux 端「共用大腦」一鍵橋接
# 用途：把本機 Claude 桌面版記憶 (~/.claude/projects/<encoded>/memory)
#       接到雲端同步的 claude-brain（git repo 內），三機共用一份大腦。
# 安全：原記憶資料夾一律先備份成 memory.bak.<時間>，可逆。
# 冪等：已經是捷徑就直接結束，重複跑不會壞。
# ============================================================
set -euo pipefail

# 1) 找到 brain repo root（本腳本所在 = <repo>/scripts/）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BRAIN="$REPO_ROOT/claude-brain"
REGISTRY="$BRAIN/machines.json"

echo "🧠 共用大腦橋接（Mac/Linux）"
echo "   repo:  $REPO_ROOT"
echo "   brain: $BRAIN"

[ -d "$BRAIN" ] || { echo "❌ 找不到 claude-brain，請先 git pull 取得最新 repo"; exit 1; }

# 2) 自動偵測本機是哪台：掃 ~/.claude/projects/ 找出有 memory 的 encoded 資料夾，
#    與 machines.json 的 encoded_path 比對。
PROJECTS="$HOME/.claude/projects"
[ -d "$PROJECTS" ] || { echo "❌ 找不到 $PROJECTS（Claude 桌面版尚未在此機產生資料）"; exit 1; }

ENCODED=""
if command -v python3 >/dev/null 2>&1 && [ -f "$REGISTRY" ]; then
  ENCODED="$(python3 - "$REGISTRY" "$PROJECTS" <<'PY'
import json,sys,os
reg,projects=sys.argv[1],sys.argv[2]
m=json.load(open(reg))["machines"]
local=set(os.listdir(projects))
for name,cfg in m.items():
    if cfg.get("os")=="macos" and cfg["encoded_path"] in local:
        print(cfg["encoded_path"]); break
PY
)"
fi
# 後備：若 registry 比對不到，取「正在使用中」最近修改、且非備份的 memory 母資料夾
if [ -z "$ENCODED" ]; then
  ENCODED="$(ls -t "$PROJECTS" 2>/dev/null | grep -v '^-$' | head -1)"
  echo "⚠️  registry 未比對到本機，後備採用最近使用的：$ENCODED"
fi

LINK="$PROJECTS/$ENCODED/memory"
echo "   本機 encoded: $ENCODED"
echo "   memory 路徑: $LINK"

# 3) 已是捷徑 → 確認指向正確即結束
if [ -L "$LINK" ]; then
  CUR="$(readlink "$LINK")"
  if [ "$CUR" = "$BRAIN" ]; then echo "✅ 已橋接，無需處理（$LINK → $BRAIN）"; exit 0; fi
  echo "⚠️  捷徑指向別處（$CUR），改指向 claude-brain"; rm "$LINK"
fi

# 4) 真實資料夾 → 先備份再橋接（存檔不刪）
if [ -e "$LINK" ]; then
  TS="$(date +%Y%m%d-%H%M%S)"
  mv "$LINK" "${LINK}.bak.${TS}"
  echo "📦 原記憶已備份 → memory.bak.${TS}（可日後比對合併獨有記憶，確認無誤再刪）"
fi

# 5) 建立橋接捷徑
mkdir -p "$(dirname "$LINK")"
ln -s "$BRAIN" "$LINK"

# 6) 驗證
echo "🔍 驗證："
readlink "$LINK"
head -1 "$LINK/MEMORY.md" >/dev/null && echo "   ✅ MEMORY.md 讀得到，共 $(ls "$LINK" | grep -cE '\.md$') 個事實檔"
echo "✅ 完成：本機已接上共用大腦。下次開工 git pull 會自動拉到其他機器寫的記憶。"
