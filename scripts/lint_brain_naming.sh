#!/usr/bin/env bash
# ============================================================
# lint_brain_naming.sh — 共用大腦命名公約檢查機關
# 規則見：claude-brain/reference_brain_naming_convention.md
# 合規：<type>_<snake_case>[_YYYY-MM-DD].md，type ∈ user/feedback/project/reference
# 用法：bash scripts/lint_brain_naming.sh   （回傳非 0 = 有違規）
# ============================================================
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRAIN="$(cd "$SCRIPT_DIR/.." && pwd)/claude-brain"

[ -d "$BRAIN" ] || { echo "❌ 找不到 $BRAIN"; exit 2; }

# 合規 regex：type_ + snake 詞(底線分隔) + 可選 _YYYY-MM-DD
OK_RE='^(user|feedback|project|reference)_[a-z0-9]+(_[a-z0-9]+)*(_[0-9]{4}-[0-9]{2}-[0-9]{2})?\.md$'

bad=0
while IFS= read -r f; do
  base="$(basename "$f")"
  [ "$base" = "MEMORY.md" ] && continue
  # 與 .gitignore 對齊：本機限定、不上雲的檔不檢查（daily 日誌 / 備份）
  case "$base" in daily_*.md|*.bak|*.bak.*) continue ;; esac
  if ! echo "$base" | grep -qE "$OK_RE"; then
    echo "❌ 不合規：$base"
    bad=$((bad+1))
  fi
done < <(find "$BRAIN" -maxdepth 1 -name '*.md' | sort)

if [ "$bad" -eq 0 ]; then
  echo "✅ claude-brain 全部檔名合規（公約：reference_brain_naming_convention.md）"
  exit 0
else
  echo "—— 共 $bad 個不合規，請改成 <type>_<snake_case>.md（描述用底線不用連字號）"
  exit 1
fi
