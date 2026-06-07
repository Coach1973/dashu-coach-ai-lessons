#!/bin/bash
# Hook：Stop（Claude Code 在回應結束前觸發）
# 用途：偵測 AI 上一輪輸出是否出現「完成/已修好/已推送」等聲明，但缺少 7+ 碼 hex commit hash
#       命中 → exit 2 強制 Claude 重做，並輸出修正指引
# 設計理念（Meta Automation，2026-06-07 教練親定）：
#       不靠模型自覺，用 grep 確定性檢查；error message 必須 actionable
#       對齊守則#05「凡走過必留痕跡」：沒有 hash = 沒做
# 守則#05 原文：「只有你做了 commit hash（雲端紀錄）才能証明你留下痕跡。
#                說了做不到，就會影響信任感的建立。」
# 保護機制：偵測 stop_hook_active=true 時放行，避免無限迴圈
# 軍師建立 2026-06-07
set -uo pipefail

INPUT=$(cat)
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)

# 已經循環過一次了，本次放行（避免無限迴圈）
[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0

[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# 只抓「最後一條」assistant 訊息——不讀歷史，避免舊輪次的內容誤觸發
# Claude Code transcript 是 jsonl，每行一個 event
LAST_TEXT=$(python3 - "$TRANSCRIPT_PATH" <<'PYEOF'
import sys, json

path = sys.argv[1]
try:
    with open(path) as f:
        lines = [l for l in f if l.strip()]
except Exception:
    sys.exit(0)

# 從後往前找最後一條 type=="assistant" 的 event
for line in reversed(lines):
    try:
        evt = json.loads(line)
        if evt.get('type') == 'assistant':
            contents = evt.get('message', {}).get('content', [])
            texts = [c.get('text', '') for c in contents if c.get('type') == 'text']
            print('\n'.join(texts))
            break
    except Exception:
        continue
PYEOF
)

[[ -z "$LAST_TEXT" ]] && exit 0

# 完成詞清單（聲明「事情做完了」的詞）
# 觸發條件：含這些詞 + 缺少 hex hash → 違規
COMPLETION_PATTERNS=(
  "完成了"
  "已修好"
  "已修完"
  "已修"
  "已修。"
  "修好了"
  "已處理"
  "處理好了"
  "已上傳"
  "已推送"
  "已 push"
  "推上去了"
  "推上 GitHub"
  "已部署"
  "已交付"
  "已建立"
  "已建立完成"
  "已設定"
  "設定好了"
  "已建立好"
  "已改完"
  "已改好"
  "改完了"
  "改好了"
  "已建置"
  "建置完成"
  "建置好了"
  "建好了"
  "已建好"
  "任務完成"
  "task 完成"
  "任務結束"
  "已就緒"
  "搞定"
  "完成！"
  "修完！"
  "搞定！"
)

# 白名單關鍵字：含這些字代表該行是在「討論/列舉/解釋/否定」守則，不是真的聲明完成
# 例如：「守則#05 講完成需要 hash」應該跳過
# 例如：「抱歉無法完成」應該跳過（否定）
WHITELIST_PATTERN='守則|不要|不應|不准|不會|不可|違反|列舉|引用|以下|清單|句型|原文|案例|範例|示例|例如|諸如|偵測|命中|示範|black.list|blacklist|討論|如果|假如|假設|除非|不然|等您|等教練|先不要|等一下|抱歉|無法|失敗|錯誤|不可|沒辦法|未完成|未通過|未驗證|未提交|可考慮|考慮|思考|想|應該|也許|或許|先看|先看您|先看一下|先給您看|想要|要|希望|建議|推薦|還沒|還不|尚未|等您|請您|待|或許|也許|大概|可能|約|預估|先|等等|先確認|先看'

HITS=""
# 逐行檢查（按換行符拆分）
while IFS= read -r LINE; do
  # 該行含白名單關鍵字 → 跳過
  if printf '%s' "$LINE" | grep -qE "$WHITELIST_PATTERN"; then
    continue
  fi
  # 檢查該行有無完成詞
  for PATTERN in "${COMPLETION_PATTERNS[@]}"; do
    if printf '%s' "$LINE" | grep -qF "$PATTERN"; then
      HITS+="  • 偵測到「${PATTERN}」"$'\n'
      break
    fi
  done
done <<< "$LAST_TEXT"

# 沒命中完成詞 → 放行
[[ -z "$HITS" ]] && exit 0

# 命中完成詞 → 檢查整個回覆有沒有 7+ 碼 hex hash
# 標準 commit hash 格式：7 碼短 hash 或 40 碼完整 hash
# 同時也接受 commit hash 前綴詞（"commit xxx", "hash: xxx"）
HAS_HASH=""
# 寬鬆匹配：任何 7+ 碼連續 [0-9a-f] 字元（不區分大小寫）
# 但要避免誤判英文單字，所以用 word boundary
if printf '%s' "$LAST_TEXT" | grep -qiE '\b[0-9a-f]{7,40}\b'; then
  HAS_HASH="yes"
fi

# 沒命中 hash → 違規
if [[ -z "$HAS_HASH" ]]; then
  # 去重
  HITS=$(printf '%s' "$HITS" | sort -u)
  [[ -n "$HITS" ]] && HITS+=$'\n'

  # 記錄違規
  LOG="$HOME/.openclaw/workspace/distill/rule05_violations.log"
  mkdir -p "$(dirname "$LOG")"
  {
    printf '[%s] session=%s\n' "$(date '+%Y-%m-%d %H:%M:%S')" \
      "$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // "unknown"' 2>/dev/null | cut -c1-8)"
    printf '%s' "$HITS"
    printf '%s\n' '---'
  } >> "$LOG"

  # stderr 輸出會在 exit 2 時被 Claude 看到，作為「重做指引」
  {
    printf '\n🚨 守則#05 違規偵測（系統 grep，deterministic check）\n'
    printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
    printf '剛才回覆出現「完成聲明」，但找不到 commit hash：\n'
    printf '%s' "$HITS"
    printf '\n📜 守則#05 原文（特助心法.md）：\n'
    printf '  「只有你做了 commit hash（雲端紀錄）才能証明你留下痕跡。」\n'
    printf '  「說了做不到，就會影響信任感的建立。」\n\n'
    printf '✅ 正確做法（請立刻補上 hash）：\n'
    printf '  1. 確認 git commit 已做，複製 7 碼短 hash（例：3b9ab393）\n'
    printf '  2. 在回覆中明確標示：「commit 3b9ab393」或「hash: 3b9ab393」\n'
    printf '  3. 如果是純說明（沒做事），把「修好了/完成了」等詞刪掉，改用「已修」開頭描述\n'
    printf '  4. 如果不該 commit（例如教練說「先看」），刪掉完成詞或加「待 commit」\n\n'
    printf '違規記錄已寫入：%s\n' "$LOG"
    printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  } >&2

  # exit 2 = 阻止 Claude 停止，stderr 內容會被當作「修正指引」注入給 Claude
  exit 2
fi

# 有 hash → 合規，放行
exit 0
