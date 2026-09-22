#!/bin/bash
# Hook：UserPromptSubmit
# 用途：教練問「你是誰/你走哪個模型/是不是MiniMax」這類身分問題時，
#       不靠模型自稱、不靠猜測，直接查這個process自己的argv+實際網路連線IP，
#       把「鐵證」塞進context，模型只能照著唸，不能糊弄。
#
# 起因（2026-09-22 教練第N次抓到手機版亂答身分）：
#   09-19教練跟軍師吵了一整晚才用lsof+nettop人工查出手機某個session實際走MiniMax，
#   09-22同樣問題又發生——因為那次的查證方法從沒被自動化，每次都要重新吵一遍。
#   這支hook把當時人工做的事變成每次問身分自動做一次，不必再吵。
#
# 設計原則：
#   - 這是全域 ~/.claude/settings.json 的 hook，手機Remote Control session跟
#     Mac桌面版session共用同一份settings.json，所以手機那邊的session也會吃到這支hook。
#   - 只在教練問身分/模型相關問題時觸發，不是每句話都查（省成本）。
#   - argv裡的--model字串是「宣告值」，不是100%保證；已知案例（2026-09-19）
#     --model字串跟實際連線目的地會對不上（BASE_URL指向Anthropic但argv寫MiniMax字串，
#     或反過來），所以兩個都給，並用「實際連線IP」當最終裁判。
#
# 軍師建立 2026-09-22

set -uo pipefail

INPUT=$(cat)
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null)
[[ -z "$PROMPT" ]] && exit 0

TRIGGER_WORDS=(
  "你是誰" "你是哪個" "你是不是" "你到底是" "你現在是"
  "走MiniMax" "走Minimax" "走minimax" "走的是MiniMax" "走的是Minimax"
  "走Claude" "走的是Claude" "是MiniMax還是" "是Claude還是"
  "手機版是" "手機版走" "手機版到底" "手機開工是"
  "context window" "Context Window" "1M" "1m" "200K" "200k"
  "什麼模型" "哪個模型" "現在跑什麼" "身分" "身份"
)

HIT=""
for WORD in "${TRIGGER_WORDS[@]}"; do
  if printf '%s' "$PROMPT" | grep -qF "$WORD"; then
    HIT="$WORD"
    break
  fi
done
[[ -z "$HIT" ]] && exit 0

# === 第一關：這個 process 自己的 argv（宣告值） ===
SELF_PID=$$
CHAIN=""
PID="$PPID"
DECLARED_MODEL=""
DECLARED_BASE_URL=""
NETWORK_PID=""

for _ in 1 2 3 4 5; do
  [[ -z "$PID" || "$PID" == "0" || "$PID" == "1" ]] && break
  CMD=$(ps -o command= -p "$PID" 2>/dev/null)
  [[ -z "$CMD" ]] && break
  CHAIN="${CHAIN}[pid ${PID}] ${CMD:0:80}...\n"
  if printf '%s' "$CMD" | grep -q -- '--model'; then
    DECLARED_MODEL=$(printf '%s' "$CMD" | grep -oE -- '--model [^ ]+' | head -1 | sed 's/--model //')
    NETWORK_PID="$PID"
    break
  fi
  PID=$(ps -o ppid= -p "$PID" 2>/dev/null | tr -d ' ')
done

if [[ -n "$NETWORK_PID" ]]; then
  DECLARED_BASE_URL=$(ps eww "$NETWORK_PID" 2>/dev/null | tr ' ' '\n' | grep '^ANTHROPIC_BASE_URL=' | cut -d= -f2-)
fi

# === 第二關：這個 process 實際的網路連線目的地（最終裁判） ===
REAL_IPS=""
if [[ -n "$NETWORK_PID" ]]; then
  REAL_IPS=$(lsof -p "$NETWORK_PID" -a -i TCP -n 2>/dev/null | grep ESTABLISHED | awk '{print $9}' | sed -E 's/.*->//' | sed -E 's/:[0-9]+$//' | sort -u)
fi

REAL_IP_ANNOTATED=""
while IFS= read -r ip; do
  [[ -z "$ip" ]] && continue
  case "$ip" in
    160.79.104.*) TAG="疑似真Anthropic(160.79.104.x段，2026-09-19曾驗證過此網段)" ;;
    175.99.116.*) TAG="疑似真MiniMax(175.99.116.x段，2026-09-19曾驗證過此網段)" ;;
    *) TAG="未知網段，需另外用 curl -v --resolve 驗證TLS憑證CN確認" ;;
  esac
  REAL_IP_ANNOTATED="${REAL_IP_ANNOTATED}  - ${ip} → ${TAG}\n"
done <<< "$REAL_IPS"

[[ -z "$REAL_IP_ANNOTATED" ]] && REAL_IP_ANNOTATED="  （查無ESTABLISHED連線，可能這輪還沒發過API請求，或lsof權限不足）\n"

# === 第三關：注入 context ===

printf '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
printf '🔍 身分自查（deterministic process檢查，非自稱，2026-09-22教練親定）\n'
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
printf '⚠️  教練問到身分/模型相關問題（命中「%s」）。以下是這個process自己查到的鐵證，\n' "$HIT"
printf '   不是這個session自己「以為」的，回答前必須引用這份資料，不能只憑訓練資料裡的自我認知回答。\n\n'

printf '📋 **宣告值**（argv --model 參數）：%s\n' "${DECLARED_MODEL:-（查無，可能hook執行環境跟主process脫鉤）}"
printf '📋 **宣告值**（ANTHROPIC_BASE_URL 環境變數）：%s\n\n' "${DECLARED_BASE_URL:-（未設定或查無）}"

printf '🎯 **實際連線目的地（最終裁判，優先於上面兩個宣告值）**：\n'
printf '%b' "$REAL_IP_ANNOTATED"
printf '\n'

printf '📖 **背景**：2026-09-19教練跟軍師花一整晚才查出，argv/env宣告值有時候會跟實際連線目的地對不上\n'
printf '   （例如argv寫MiniMax字串但實際走真Anthropic OAuth，或反過來）。所以判斷「這個session到底是誰」，\n'
printf '   一律以上面「實際連線目的地」的IP段為準，宣告值只能當輔助線索。如果IP段是「未知網段」，\n'
printf '   誠實跟教練說需要再查證，不要用宣告值蒙混過關。完整原理見[[reference_minimax_mystery_resolved_model_name_routing_2026-09-19]]。\n'
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'

exit 0
