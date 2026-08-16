#!/bin/bash
# project_card_router.sh — 賈維斯計畫 Phase 1「自動接線員」
# Hook: UserPromptSubmit
# 作用：教練訊息命中專案別名（見 projects/INDEX.md）→ 自動注入該專案卡全文
# 設計：每場 session 每張卡只注入一次；單則訊息最多注入 2 張（控制 context 成本）
# 建立：2026-08-16 Fable 5（教練拍板賈維斯計畫後施工）
set -uo pipefail

INPUT=$(cat)
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // "nosession"' 2>/dev/null)

[ -z "$PROMPT" ] && exit 0

WS="/Users/bymyway/.openclaw/workspace"
INDEX="$WS/projects/INDEX.md"
MARKER_DIR="$WS/state/project_card_injected"

[ -f "$INDEX" ] || exit 0
mkdir -p "$MARKER_DIR"
# 清掉 7 天前的舊標記，避免無限堆積
find "$MARKER_DIR" -type f -mtime +7 -delete 2>/dev/null

MAX_CARDS=2
COUNT=0

# 只讀路由行（格式：id|別名,別名|相對路徑）
while IFS='|' read -r card_id aliases card_rel; do
  [ "$COUNT" -ge "$MAX_CARDS" ] && break
  [ -z "$card_id" ] && continue

  MARKER="$MARKER_DIR/${SESSION_ID}_${card_id}"
  [ -f "$MARKER" ] && continue   # 本場已注入過這張卡

  HIT=""
  IFS=',' read -ra ALIST <<< "$aliases"
  for alias in "${ALIST[@]}"; do
    [ -z "$alias" ] && continue
    if printf '%s' "$PROMPT" | grep -qiF "$alias"; then
      HIT="$alias"
      break
    fi
  done
  [ -z "$HIT" ] && continue

  CARD_FILE="$WS/projects/$card_rel"
  if [ ! -f "$CARD_FILE" ]; then
    echo "⚠️ 專案卡路由：INDEX 指向的卡片不存在（$card_rel），請修 projects/INDEX.md" >&2
    continue
  fi

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🗂 賈維斯接線員：偵測到「${HIT}」→ 自動送上專案病歷（本場僅此一次）"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  cat "$CARD_FILE"
  echo ""
  touch "$MARKER"
  COUNT=$((COUNT+1))
done < <(grep -E '^[a-z0-9-]+\|' "$INDEX")

exit 0
