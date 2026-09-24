#!/bin/bash
# Hook：UserPromptSubmit
# 用途：偵測教練 prompt 提及「模型 / provider / 切換 / M3 / Opus / Sonnet / Haiku / Kimi」等詞，
#       自動從 ~/.openclaw/openclaw.json 注入「當前模型設定摘要」到 context。
# 設計理念（Meta Automation，2026-06-07 教練親定）：
#       守則 E07「存在性驗證 + 語音糾偏」+ 守則#15「說不知道比胡說八道更值得尊重」的工程化檢查。
#       與其讓模型靠記憶回答「現在用什麼模型」，
#       不如 hook 主動把 openclaw.json 摘要塞進 context，模型不必靠記憶答。
# 觸發訊號（中文優先，避免英文語境誤觸發）：
#       - 模型 / provider / 切換模型 / 用什麼模型
#       - M3 / MiniMax / Claude / Opus / Sonnet / Haiku / Kimi
# 白名單（避開英文語境）：
#       - BMW / 車 / 音樂 / FLAC / ALAC / health care / care provider
# 軍師建立 2026-06-07
set -uo pipefail

INPUT=$(cat)
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null)

# 沒有 prompt 就靜默退出
[[ -z "$PROMPT" ]] && exit 0

CONFIG="$HOME/.openclaw/openclaw.json"
[[ -f "$CONFIG" ]] || exit 0

# === 第一關：偵測是否為模型/設定相關問題 ===

# 觸發詞清單（用 -F 固定字串匹配，避免正則表達式效能問題）
TRIGGER_WORDS=(
  "模型"
  "provider"
  "切換"
  "用什麼模型"
  "現在用什麼"
  "現在跑什麼"
  "目前用什麼"
  "M3"
  "MiniMax"
  "Opus"
  "Sonnet"
  "Haiku"
  "Kimi"
  "K2.5"
  "K2.6"
  "Claude"
  "GPT"
  "Gemini"
  "baseUrl"
  "API key"
  "API設定"
  "openclaw.json"
)

# 白名單關鍵字（包含這些字就跳過，避免英文語境誤觸發）
WHITELIST_WORDS=(
  "BMW"
  "車款"
  "汽車"
  "M3 Competition"
  "M3 CS"
  "Opus 4"
  "FLAC"
  "ALAC"
  "lossless"
  "無損音樂"
  "無損格式"
  "Kimi 韓"
  "Kimi 演員"
  "Kimi 綜藝"
  "韓星 Kimi"
  "Haiku 俳句"
  "俳句"
  "Sonnet 十四行詩"
  "十四行詩"
  "health care"
  "care provider"
  "service provider"
  "internet provider"
  "email provider"
  "payment provider"
  "Claude 角色"
  "Claude 動漫"
  "Sonnet 角色"
)

# 檢查是否觸發
HIT=""
for WORD in "${TRIGGER_WORDS[@]}"; do
  if printf '%s' "$PROMPT" | grep -qF "$WORD"; then
    # 觸發詞命中 → 再檢查白名單
    WHITELISTED="no"
    for WL in "${WHITELIST_WORDS[@]}"; do
      if printf '%s' "$PROMPT" | grep -qF "$WL"; then
        WHITELISTED="yes"
        break
      fi
    done
    if [[ "$WHITELISTED" == "no" ]]; then
      HIT="$WORD"
      break
    fi
  fi
done

# 沒命中 → 靜默退出
[[ -z "$HIT" ]] && exit 0

# === 第二關：抽出 openclaw.json 摘要 ===

# 用 jq 抽出 providers / models / agents
SUMMARY=$(/usr/bin/jq -c '{
  primary_model: ((.models.providers.minimax.models[0].id // "未設定")),
  all_providers: [
    .models.providers | to_entries[] |
    { provider: .key, models: ([.value.models[]?.id] // ["unknown"]), baseUrl: ((.value.baseUrl // "n/a")) }
  ],
  agents: [
    (.agents.list // []) | .[] |
    { name: .id, model: ((.model // "(inherit)")), workspace: ((.workspace // "n/a")) }
  ],
  model_mode: ((.models.mode // "未設定"))
}' "$CONFIG" 2>/dev/null)

# 抓取失敗 → 靜默退出
[[ -z "$SUMMARY" ]] && exit 0

# === 第三關：注入 context ===

printf '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
printf '⚙️  設定檔原文注入（N3 查證鐵律自動驗證，openclaw.json 摘要）\n'
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
printf '⚠️  教練在 prompt 提到「%s」相關詞，以下是 openclaw.json 實際設定。\n' "$HIT"
printf '   回答時以這份設定為準，不靠記憶（執行細則 N3 + 守則#15）。\n\n'
printf '🔴 範圍提醒（2026-09-19案例補丁）：這份openclaw.json只管OpenClaw閘道(小龍蝦/Telegram/LINE\n'
printf '   agent)的模型路由，跟「這個Claude Code session本身在跑什麼模型」是兩回事——尤其`claude rc`\n'
printf '   啟動的Remote Control session，啟動前會unset掉ANTHROPIC_BASE_URL/API_KEY等變數，不吃這份設定，\n'
printf '   直連api.anthropic.com。若教練問的是「這個對話框/手機這個session」本身的模型，不要只回這份摘要，\n'
printf '   先查session啟動指令的--sdk-url/--model參數(ps aux)或systemreminder裡的model欄位才是準的。\n\n'

printf '📋 **當前主要模型（primary）**：%s\n\n' "$(printf '%s' "$SUMMARY" | /usr/bin/jq -r '.primary_model')"

printf '📦 **所有 provider**：\n'
printf '%s' "$SUMMARY" | /usr/bin/jq -r '.all_providers[] | "  - \(.provider) (\(.baseUrl)): \(.models | join(", "))"'
printf '\n\n'

printf '🤖 **agents 模型設定**：\n'
printf '%s' "$SUMMARY" | /usr/bin/jq -r '.agents[] | "  - \(.name): model=\(.model), workspace=\(.workspace)"'
printf '\n\n'

printf '🔧 **models.mode**：%s\n' "$(printf '%s' "$SUMMARY" | /usr/bin/jq -r '.model_mode')"

printf '\n（來源：%s）\n' "$CONFIG"
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'

exit 0
