#!/bin/bash
# 用途：把 workspace/執行細則.md（教練欽定唯一正式版）自動鏡像到 ~/.claude/CLAUDE.md 的標記區段，
#       讓終端機/桌面版 Claude 開機讀 ~/.claude/CLAUDE.md 時看到的 E 規則永遠跟正式版一致，不再手動燒錄。
# 起因：2026-07-24 研究mattpocock/skills時查證發現，~/.claude/CLAUDE.md 的 E10~E12
#       (Karpathy工程原則)跟執行細則.md 2026-06-17後陸續加入的 E10~E12(危險指令/記憶寫入)
#       已分岔一個半月未同步。教練裁示「合併，因為這樣才簡單」。
# 觸發：手動跑 / openclaw cron 定期跑 / 軍師改完執行細則.md 後跑一次
# 設計：仿照 sync_handoff_to_claudemd.sh 的 mtime-marker 模式；~/.claude 不是git repo，
#       所以本腳本不做git commit（跟handoff那支不同，那支同步的是git追蹤的workspace/CLAUDE.md）

set -uo pipefail

WS="/Users/bymyway/.openclaw/workspace"
SOURCE="$WS/執行細則.md"
TARGET="/Users/bymyway/.claude/CLAUDE.md"
MARKER_DIR="$WS/.sync_markers"
SYNC_MARKER="$MARKER_DIR/zhixingxize_last_sync"
# 不寫HEARTBEAT.md（小龍蝦開機必讀檔，2026-09-25查到被軍師日誌撐破2萬字上限）
LOG="$WS/state/junshi_automation.log"

START_MARK="<!-- ZHIXINGXIZE_AUTOINJECT_START -->"
END_MARK="<!-- ZHIXINGXIZE_AUTOINJECT_END -->"

mkdir -p "$MARKER_DIR"

[[ -f "$TARGET" ]] || { echo "❌ ~/.claude/CLAUDE.md 不存在"; exit 1; }
[[ -f "$SOURCE" ]] || { echo "❌ 執行細則.md 不存在：$SOURCE"; exit 1; }

SOURCE_MTIME=$(stat -f %m "$SOURCE")
LAST_SYNC=0
[[ -f "$SYNC_MARKER" ]] && LAST_SYNC=$(cat "$SYNC_MARKER")

if [[ "$SOURCE_MTIME" -le "$LAST_SYNC" ]]; then
  exit 0
fi

/opt/homebrew/bin/python3 - "$TARGET" "$SOURCE" "$START_MARK" "$END_MARK" <<'PYEOF'
import re, sys, datetime
from pathlib import Path

target_path, source_path, start_mark, end_mark = sys.argv[1:5]
target = Path(target_path)
source = Path(source_path)

target_content = target.read_text(encoding="utf-8")
source_content = source.read_text(encoding="utf-8")
stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

new_block = f"""{start_mark}
> 本區段由 `scripts/sync_zhixingxize_to_claude_global.sh` 自動鏡像 `workspace/執行細則.md` 全文（教練欽定唯一正式版）。
> **最後同步：{stamp}**
> 不再手動維護此區段內容——要改規則，改 `執行細則.md`，這裡會自動跟上。

{source_content}
{end_mark}"""

# 第一次執行：如果舊區段（無marker的手寫版本）還在，先找「# 執行細則」到下一個「---」之間整段換掉
old_section_pattern = re.compile(
    r"# 執行細則（9條）.*?\n---\n",
    re.DOTALL
)

if start_mark in target_content:
    pattern = re.compile(re.escape(start_mark) + r".*?" + re.escape(end_mark), re.DOTALL)
    new_content = pattern.sub(new_block, target_content)
elif old_section_pattern.search(target_content):
    new_content = old_section_pattern.sub(new_block + "\n", target_content, count=1)
else:
    print("⚠️ 找不到舊執行細則區段或既有marker，未寫入，請人工檢查")
    sys.exit(1)

if new_content != target_content:
    target.write_text(new_content, encoding="utf-8")
    print(f"✅ ~/.claude/CLAUDE.md 已同步執行細則.md（{stamp}）")
else:
    print("ℹ️ 內容無變化，跳過寫入")
PYEOF

RC=$?

if [[ "$RC" -eq 0 ]]; then
  echo "$SOURCE_MTIME" > "$SYNC_MARKER"
  {
    echo ""
    echo "## 🔄 執行細則.md→~/.claude/CLAUDE.md 自動同步 $(date '+%Y-%m-%d %H:%M')"
    echo "- ✅ 同步成功"
    echo "- SOURCE mtime: $SOURCE_MTIME"
  } >> "$LOG" 2>/dev/null || true
fi

exit $RC
