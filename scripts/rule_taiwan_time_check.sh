#!/bin/bash
# Hook：Stop（Claude Code 在回應結束前觸發）
# 用途：偵測 AI 這一輪是否處理過原始 UTC timestamp（jsonl/log 的 "...T..:..:..Z" 格式），
#       但最終回覆裡出現時鐘數字（HH:MM）卻沒有明確講「台灣時間」/「+8」換算的痕跡
#       命中 → exit 2 強制 Claude 重新檢查換算，並輸出修正指引
# 設計理念：不靠模型自覺，用 grep 確定性檢查
# 對齊：時間鐵律（2026-06-09 教練親罵，memory: feedback_taiwan_time_always.md）
#       「看到 Z 結尾自動 +8 呈現」「禁止口語講 UTC 時間當台灣時間」
# 觸發案例：2026-07-03 案例38——軍師查 session log 抓到 UTC timestamp（22:36:51.486Z），
#       換算「經過時間」沒錯，但把 22:36 這種原始 UTC 小時數字直接當台灣時間報給教練，
#       沒有 +8，教練當場抓到：「你的時間也不對，你到底是用哪一個國家的時間？」
# 保護機制：偵測 stop_hook_active=true 時放行，避免無限迴圈
# 軍師建立 2026-07-03
set -uo pipefail

INPUT=$(cat)
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)

[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0
[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# 抓「這一輪」的內容：從最後一個 type=="user" 事件之後，到檔案結尾為止的所有內容
# （tool_use / tool_result / assistant text 全部納入，用來判斷這一輪有沒有碰過 UTC timestamp）
# 同時單獨抓出「最後一條 assistant text」，用來檢查有沒有講「台灣時間」
RESULT=$(python3 - "$TRANSCRIPT_PATH" <<'PYEOF'
import sys, json

path = sys.argv[1]
try:
    with open(path) as f:
        lines = [l for l in f if l.strip()]
except Exception:
    sys.exit(0)

# 找最後一個 type=="user" 事件的位置（且非 tool_result 型態的 user 事件，儘量抓真人發話）
last_user_idx = None
for i in range(len(lines) - 1, -1, -1):
    try:
        evt = json.loads(lines[i])
    except Exception:
        continue
    if evt.get('type') == 'user':
        msg = evt.get('message', {})
        content = msg.get('content')
        # 純文字使用者訊息才算「這一輪的起點」；跳過 tool_result 型態的 user 事件
        if isinstance(content, str) or (isinstance(content, list) and any(
            isinstance(c, dict) and c.get('type') == 'text' for c in content
        )):
            last_user_idx = i
            break

if last_user_idx is None:
    last_user_idx = 0

turn_lines = lines[last_user_idx:]

# 🔴 只抓「實際內容文字」（訊息文字、tool_result 文字），
# 不可用整行 raw JSONL（每個事件本身的 "timestamp" 信封欄位一定含 UTC Z 格式，
# 會讓 touched_utc 恆為 true，2026-07-03 案例38後首次真實對話就誤報過一次）
def extract_texts(node):
    texts = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k == 'timestamp':
                continue  # 信封層的事件時間戳，不算「AI 處理過的內容」
            if k == 'text' and isinstance(v, str):
                texts.append(v)
            elif k == 'content' and isinstance(v, str):
                texts.append(v)
            else:
                texts.extend(extract_texts(v))
    elif isinstance(node, list):
        for item in node:
            texts.extend(extract_texts(item))
    return texts

content_texts = []
for line in turn_lines:
    try:
        evt = json.loads(line)
    except Exception:
        continue
    # 🔴 排除 type=="attachment"：這是 UserPromptSubmit hook 每輪自動注入的
    # 守則提醒文字（本身寫死含範例 "2026-06-09T06:25:36.752Z" 當教材），
    # 不是 AI 真正讀取/處理的外部資料，會讓 touched_utc 恆為 true
    # （2026-07-03 案例38後首次真實對話誤報，根因就是這段範例文字）
    if evt.get('type') == 'attachment':
        continue
    content_texts.extend(extract_texts(evt.get('message', evt)))
turn_raw_text = '\n'.join(content_texts)

# 這一輪是否出現過原始 UTC ISO timestamp（T..:..:..Z 或 T..:..:...Z 帶毫秒）
import re
utc_pattern = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z')
touched_utc = bool(utc_pattern.search(turn_raw_text))

# 抓最後一條 assistant text（給教練看的最終回覆）
last_assistant_text = ''
for line in reversed(lines):
    try:
        evt = json.loads(line)
    except Exception:
        continue
    if evt.get('type') == 'assistant':
        contents = evt.get('message', {}).get('content', [])
        texts = [c.get('text', '') for c in contents if isinstance(c, dict) and c.get('type') == 'text']
        last_assistant_text = '\n'.join(texts)
        break

print(json.dumps({
    'touched_utc': touched_utc,
    'last_assistant_text': last_assistant_text,
}))
PYEOF
)

[[ -z "$RESULT" ]] && exit 0

TOUCHED_UTC=$(printf '%s' "$RESULT" | /usr/bin/jq -r '.touched_utc')
LAST_TEXT=$(printf '%s' "$RESULT" | /usr/bin/jq -r '.last_assistant_text')

# 這一輪沒碰過 UTC timestamp → 跟本機關無關，放行
[[ "$TOUCHED_UTC" != "true" ]] && exit 0
[[ -z "$LAST_TEXT" ]] && exit 0

# 最終回覆裡有沒有出現任何「時鐘數字」模式（HH:MM 或 H點MM分 之類）
HAS_CLOCK_NUMBER=""
if printf '%s' "$LAST_TEXT" | grep -qE '[0-9]{1,2}:[0-9]{2}|[0-9]{1,2}[點时]'; then
  HAS_CLOCK_NUMBER="yes"
fi

# 沒有提到任何時鐘數字 → 這一輪雖然碰過 UTC，但沒有把時間講給教練聽，不算違規
[[ -z "$HAS_CLOCK_NUMBER" ]] && exit 0

# 最終回覆裡有沒有明確講「台灣時間」或「+8」換算字樣
HAS_TAIWAN_MARK=""
if printf '%s' "$LAST_TEXT" | grep -qE '台灣時間|台湾时间|\+8|GMT\+8|UTC\+8'; then
  HAS_TAIWAN_MARK="yes"
fi

# 有講清楚台灣時間 → 合規，放行
[[ -n "$HAS_TAIWAN_MARK" ]] && exit 0

# 違規：這一輪碰過原始 UTC timestamp，回覆裡也講了時鐘數字，但完全沒提「台灣時間」換算
LOG="$HOME/.openclaw/workspace/distill/rule_taiwan_time_violations.log"
mkdir -p "$(dirname "$LOG")"
{
  printf '[%s] session=%s\n' "$(date '+%Y-%m-%d %H:%M:%S')" \
    "$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // "unknown"' 2>/dev/null | cut -c1-8)"
  printf '%s\n' '---'
} >> "$LOG"

{
  printf '\n🕐🔒 時間鎖違規偵測（系統 grep，deterministic check）\n'
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  printf '這一輪你讀取/處理過原始 UTC timestamp（含 "T..:..:..Z" 格式），\n'
  printf '回覆裡也出現了時鐘數字，但完全沒有講「台灣時間」或「+8」換算字樣。\n\n'
  printf '📜 時間鐵律（教練 2026-06-09 親罵後寫死，案例38 再犯一次）：\n'
  printf '  「跟教練講時間 → 永遠先換算成台灣時間（Asia/Taipei，UTC+8）」\n'
  printf '  「看到 Z 結尾自動 +8 呈現，禁止口語講 UTC 時間當台灣時間」\n\n'
  printf '✅ 正確做法（請立刻檢查並修正）：\n'
  printf '  1. 回頭檢查剛才報給教練的每一個時鐘數字，是不是直接抄了 UTC 的 HH:MM\n'
  printf '  2. 全部 +8 小時重新換算（注意跨日：UTC 16:00 以後會跨到台灣隔天）\n'
  printf '  3. 回覆中明確標示「台灣時間」字樣，讓教練一眼確認你有換算過\n'
  printf '  4. 如果這次真的不需要報時間（只是剛好文字裡出現數字），可忽略此提醒\n\n'
  printf '違規記錄已寫入：%s\n' "$LOG"
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
} >&2

exit 2
