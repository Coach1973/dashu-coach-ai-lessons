#!/bin/bash
# 用途：把 workspace/特助心法.md（教練欽定唯一正式版，一字不差禁止自行詮釋）自動鏡像到
#       ~/.claude/CLAUDE.md 的「特助心法」標記區段，避免手動貼上去的內容跟源頭慢慢飄移。
# 起因：2026-07-31 教練看完一篇講 CLAUDE.md 規則會「只進不出、悄悄過期」的文章後，
#       要求對照健檢。實測發現「特助心法」段是手動貼的，已經跟源頭出現格式/日期標籤差異——
#       跟當年 E10~E12 分岔一個半月是同一種病，只是還沒傷到內容。仿照
#       sync_zhixingxize_to_claude_global.sh 的 mtime-marker 模式補上自動同步，根治問題。
# 觸發：手動跑 / openclaw cron 定期跑 / 軍師改完特助心法.md 後跑一次
# 範圍：只鏡像「最高指導原則」到「21.核心理念原文引用」這段核心內容，不含檔案開頭的
#       版權/授權聲明（那是給人看的文件識別資訊，不是要 AI 遵守的指令），也不含檔案結尾
#       特助心法.md 自己內部那份已經過時的執行細則(9條)舊副本（正式版在 執行細則.md，
#       由另一支腳本同步，避免同一份規則在 CLAUDE.md 裡出現兩次不同步的版本）。

set -uo pipefail

WS="/Users/bymyway/.openclaw/workspace"
SOURCE="$WS/特助心法.md"
TARGET="/Users/bymyway/.claude/CLAUDE.md"
MARKER_DIR="$WS/.sync_markers"
SYNC_MARKER="$MARKER_DIR/xinfa_last_sync"
# 不寫HEARTBEAT.md（小龍蝦開機必讀檔，2026-09-25查到被軍師日誌撐破2萬字上限）
LOG="$WS/state/junshi_automation.log"

START_MARK="<!-- XINFA_AUTOINJECT_START -->"
END_MARK="<!-- XINFA_AUTOINJECT_END -->"

mkdir -p "$MARKER_DIR"

[[ -f "$TARGET" ]] || { echo "❌ ~/.claude/CLAUDE.md 不存在"; exit 1; }
[[ -f "$SOURCE" ]] || { echo "❌ 特助心法.md 不存在：$SOURCE"; exit 1; }

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

core_match = re.search(r"(## 最高指導原則.*?)\n## 執行細則", source_content, re.DOTALL)
if not core_match:
    print("⚠️ 找不到特助心法.md 的段落邊界（## 最高指導原則 ... ## 執行細則），未寫入，請人工檢查")
    sys.exit(1)
core = core_match.group(1).rstrip()

new_block = f"""{start_mark}
# 特助心法（頂級特助俱樂部）

> 本區段由 `scripts/sync_xinfa_to_claude_global.sh` 自動鏡像 `workspace/特助心法.md` 核心內容（教練欽定唯一正式版，一字不差，禁止自行詮釋）。
> **最後同步：{stamp}**
> 不再手動維護此區段內容——要改守則，改 `特助心法.md`，這裡會自動跟上。

{core}
{end_mark}"""

if start_mark in target_content:
    pattern = re.compile(re.escape(start_mark) + r".*?" + re.escape(end_mark), re.DOTALL)
    new_content = pattern.sub(new_block, target_content)
else:
    old_section_pattern = re.compile(
        r"# 特助心法（頂級特助俱樂部）.*?\n---\n\n(?=<!-- ZHIXINGXIZE_AUTOINJECT_START -->)",
        re.DOTALL
    )
    if old_section_pattern.search(target_content):
        new_content = old_section_pattern.sub(new_block + "\n\n", target_content, count=1)
    else:
        print("⚠️ 找不到舊特助心法區段或既有marker，未寫入，請人工檢查")
        sys.exit(1)

if new_content != target_content:
    target.write_text(new_content, encoding="utf-8")
    print(f"✅ ~/.claude/CLAUDE.md 已同步特助心法.md（{stamp}）")
else:
    print("ℹ️ 內容無變化，跳過寫入")
PYEOF

RC=$?

if [[ "$RC" -eq 0 ]]; then
  echo "$SOURCE_MTIME" > "$SYNC_MARKER"
  {
    echo ""
    echo "## 🔄 特助心法.md→~/.claude/CLAUDE.md 自動同步 $(date '+%Y-%m-%d %H:%M')"
    echo "- ✅ 同步成功"
    echo "- SOURCE mtime: $SOURCE_MTIME"
  } >> "$LOG" 2>/dev/null || true
fi

exit $RC
