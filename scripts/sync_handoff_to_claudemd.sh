#!/bin/bash
# 用途：把 JUNSHI_HANDOFF_LATEST.md 自動鏡像到 CLAUDE.md 的標記區段，
#       讓桌面版 Claude.app 啟動讀 CLAUDE.md 時直接看到最新接力棒，不靠模型自律去翻檔案。
# 觸發：手動跑 / cron 每 5 分鐘 / 軍師結束 session 改完接力棒後跑一次
# 設計：HANDOFF mtime > 上次同步時間才動工，沒變化就不動 CLAUDE.md（避免 git noise）

set -uo pipefail

WS="/Users/bymyway/.openclaw/workspace"
CLAUDE_MD="$WS/CLAUDE.md"
HANDOFF="$WS/JUNSHI_HANDOFF_LATEST.md"
MARKER_DIR="$WS/.sync_markers"
SYNC_MARKER="$MARKER_DIR/handoff_last_sync"
LOG="$WS/HEARTBEAT.md"

START_MARK="<!-- HANDOFF_AUTOINJECT_START -->"
END_MARK="<!-- HANDOFF_AUTOINJECT_END -->"

mkdir -p "$MARKER_DIR"

# 檔案檢查
[[ -f "$CLAUDE_MD" ]] || { echo "❌ CLAUDE.md 不存在"; exit 1; }
[[ -f "$HANDOFF"   ]] || { echo "❌ JUNSHI_HANDOFF_LATEST.md 不存在"; exit 1; }

HANDOFF_MTIME=$(stat -f %m "$HANDOFF")
LAST_SYNC=0
[[ -f "$SYNC_MARKER" ]] && LAST_SYNC=$(cat "$SYNC_MARKER")

# HANDOFF 沒變動就退出（避免每分鐘無謂改 CLAUDE.md）
if [[ "$HANDOFF_MTIME" -le "$LAST_SYNC" ]]; then
  exit 0
fi

# 用 python 處理多行替換（sed 多行麻煩）
python3 - "$CLAUDE_MD" "$HANDOFF" "$START_MARK" "$END_MARK" <<'PYEOF'
import re, sys, datetime
from pathlib import Path

claude_md_path, handoff_path, start_mark, end_mark = sys.argv[1:5]
claude_md = Path(claude_md_path)
handoff   = Path(handoff_path)

claude_content  = claude_md.read_text(encoding="utf-8")
handoff_content = handoff.read_text(encoding="utf-8")
stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

new_section = f"""{start_mark}
## 🔴 最新接力棒（系統自動鏡像，桌面版啟動必讀）

> 本區段由 `scripts/sync_handoff_to_claudemd.sh` 自動同步，鏡像 `JUNSHI_HANDOFF_LATEST.md` 全文。
> **最後同步：{stamp}**
> 任何模型（Opus / Sonnet / Haiku，桌面版 / 終端機）讀到 CLAUDE.md 都會看到，**不靠主動翻檔**。
> 若本區段內容跟 `JUNSHI_HANDOFF_LATEST.md` 不同步，代表同步腳本掛掉，請通報教練。

---

{handoff_content}

---

> ⬆️ 接力棒鏡像結束。以下回到 CLAUDE.md 原本內容。
{end_mark}"""

if start_mark in claude_content and end_mark in claude_content:
    # 已有標記區段：替換內容
    pattern = re.compile(re.escape(start_mark) + r".*?" + re.escape(end_mark), re.DOTALL)
    new_content = pattern.sub(new_section, claude_content)
else:
    # 首次安裝：在第一個「## 🎖️ Claude 軍師接位提示」之前插入
    anchor = "## 🎖️ Claude 軍師接位提示"
    if anchor in claude_content:
        new_content = claude_content.replace(
            anchor,
            new_section + "\n\n---\n\n" + anchor,
            1
        )
    else:
        # 退而求其次：放最上面（# 標題之後）
        lines = claude_content.split("\n", 1)
        new_content = lines[0] + "\n\n" + new_section + "\n\n" + (lines[1] if len(lines) > 1 else "")

if new_content != claude_content:
    claude_md.write_text(new_content, encoding="utf-8")
    print(f"✅ CLAUDE.md 已同步最新接力棒（{stamp}）")
else:
    print("ℹ️ 內容無變化，跳過寫入")
PYEOF

RC=$?

if [[ "$RC" -eq 0 ]]; then
  echo "$HANDOFF_MTIME" > "$SYNC_MARKER"
  # 寫進心跳檔留證
  {
    echo ""
    echo "## 🔄 接力棒→CLAUDE.md 自動同步 $(date '+%Y-%m-%d %H:%M')"
    echo "- ✅ 同步成功"
    echo "- HANDOFF mtime: $HANDOFF_MTIME"
  } >> "$LOG" 2>/dev/null || true

  # A 段：CLAUDE.md 有實際變動才 commit + push（避免 git noise）
  cd "$WS" 2>/dev/null || exit 0
  if ! git diff --quiet CLAUDE.md 2>/dev/null; then
    PUSH_RESULT="push 失敗（離線或網路問題，commit 已留本機）"
    if git add CLAUDE.md 2>/dev/null \
       && git commit -m "auto: 接力棒鏡像同步 $(date '+%Y-%m-%d %H:%M')" >/dev/null 2>&1; then
      COMMIT_HASH=$(git rev-parse --short HEAD)
      if git push origin main >/dev/null 2>&1; then
        PUSH_RESULT="✅ 已推上雲端（commit $COMMIT_HASH）"
      else
        PUSH_RESULT="⚠️ commit $COMMIT_HASH 已留本機，但 push 失敗"
      fi
    fi
    {
      echo "- 雲端同步：$PUSH_RESULT"
    } >> "$LOG" 2>/dev/null || true
  fi
fi

exit $RC
