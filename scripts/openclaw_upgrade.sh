#!/bin/bash
# 小龍蝦（OpenClaw）版本升級：備份 → 升級 → 驗證 → 出事一鍵回退
#
# 建立：2026-08-24（教練交辦「調查小龍蝦有沒有更新版本、效能效果有沒有更好、有沒有後遺症」）
# ⚠️ 教練說「調查清楚後回報，如果確實更好，我們再跟進更新」——所以這支腳本
#    刻意做成「要人明確執行才會動」，不掛任何自動排程、不會自己跑。
#
# 用法：
#   bash scripts/openclaw_upgrade.sh check      # 只看目前版本與可用版本，不動任何東西
#   bash scripts/openclaw_upgrade.sh upgrade    # 真的升級（會先自動備份）
#   bash scripts/openclaw_upgrade.sh verify     # 升級後健康檢查
#   bash scripts/openclaw_upgrade.sh rollback   # 退回升級前的版本
#
# 為什麼要這麼慎重：這台 Mac 的 OpenClaw 同時扛著教練 3 個 LINE 官方帳號
# （龍蝦小助教／BNI大台南小幫手／教練都在想什麼）+ 3 個 Telegram 帳號 + 24 個排程 +
# 18 支自訂 hook，掛掉就是對外服務全斷，不是只有教練自己不方便。

set -uo pipefail

WORKSPACE="/Users/bymyway/.openclaw/workspace"
STATE="$WORKSPACE/state"
NPM="/opt/homebrew/bin/npm"          # openclaw 裝在 homebrew 的 node 底下，不是 .hermes 那支
OPENCLAW="/opt/homebrew/bin/openclaw"
TARGET_TAG="extended-stable"          # 教練目前走的就是 6.x extended-stable 這條線
VERSION_FILE="$STATE/openclaw_version_before_upgrade.txt"
BASELINE="$STATE/plugins_baseline_2026-6-33.txt"

current() { "$OPENCLAW" --version 2>/dev/null | awk '{print $2}'; }

cmd_check() {
  echo "═══ 版本現況 ═══"
  echo "目前安裝：$(current)"
  echo
  echo "npm 上各條發佈線："
  "$NPM" view openclaw dist-tags 2>/dev/null
  echo
  echo "建議：走 extended-stable（教練目前的 6.x 線），latest 那條是不同 release line，"
  echo "      版號雖然比較大但發佈日期其實更早，換過去等於橫向跳線，風險比較高。"
}

cmd_upgrade() {
  local before target
  before="$(current)"
  target="$("$NPM" view "openclaw@$TARGET_TAG" version 2>/dev/null)"
  echo "═══ 準備升級：$before → $target ═══"
  if [[ "$before" == "$target" ]]; then
    echo "✅ 已經是 $TARGET_TAG 最新版，不用動。"; return 0
  fi

  echo "① 備份設定檔與版本號"
  cp "$HOME/.openclaw/openclaw.json" "$HOME/.openclaw/openclaw.json.bak-before-upgrade-$(date +%Y%m%d-%H%M%S)" || return 1
  echo "$before" > "$VERSION_FILE"
  "$OPENCLAW" plugins list > "$STATE/plugins_before_upgrade.txt" 2>&1
  echo "   設定檔已備份、外掛清單已存檔"

  echo "② 安裝 openclaw@$target"
  "$NPM" install -g "openclaw@$target" || { echo "❌ 安裝失敗，系統沒有被改動"; return 1; }

  echo "③ 重啟 gateway"
  "$OPENCLAW" gateway restart 2>&1 | tail -3

  echo "④ 等 15 秒讓服務起來"
  sleep 15
  cmd_verify
}

cmd_verify() {
  local rc=0
  echo "═══ 升級後健康檢查 ═══"
  echo "版本：$(current)"

  echo -n "① 外掛數量（基準 48 啟用 / 20 停用）："
  local plugins en dis
  plugins="$("$OPENCLAW" plugins list 2>&1)"
  en=$(printf '%s' "$plugins" | grep -cE "│ enabled ")
  dis=$(printf '%s' "$plugins" | grep -cE "│ disabled ")
  echo "$en 啟用 / $dis 停用"
  if [[ "$en" -lt 48 ]]; then
    echo "   🔴 啟用數變少了！很可能是新版新增的外掛不在 plugins.allow 白名單裡被關掉"
    echo "   → 比對：diff <(echo \"\$plugins\") $STATE/plugins_before_upgrade.txt"
    rc=1
  fi

  echo -n "② 自訂 hook 是否全部載入（設定裡啟用幾支，gateway 就該載入幾支）："
  local hooks_enabled hooks_loaded
  hooks_enabled=$(/usr/bin/python3 -c "
import json
d=json.load(open('$HOME/.openclaw/openclaw.json'))
e=d['hooks']['internal']['entries']
print(sum(1 for v in e.values() if v.get('enabled')))
" 2>/dev/null)
  hooks_loaded=$(grep -a "loaded .* internal hook" "$HOME/Library/Logs/openclaw/gateway.log" 2>/dev/null | tail -1 | grep -oE "loaded [0-9]+" | grep -oE "[0-9]+")
  echo "設定啟用 ${hooks_enabled:-?} 支／gateway 實際載入 ${hooks_loaded:-?} 支"
  [[ "${hooks_enabled:-0}" != "${hooks_loaded:-1}" ]] && { echo "   🔴 兩個數字對不上，代表有 hook 沒載入"; rc=1; }

  echo -n "③ Telegram 通道實測："
  local tg
  tg=$(/usr/bin/python3 -c "
import json,urllib.request
cfg=json.load(open('$HOME/.openclaw/openclaw.json'))
t=cfg['channels']['telegram']['accounts']['bot_main']['botToken']
print(json.load(urllib.request.urlopen(f'https://api.telegram.org/bot{t}/getMe',timeout=10))['result']['username'])
" 2>/dev/null)
  if [[ -n "$tg" ]]; then echo "✅ $tg"; else echo "🔴 打不通"; rc=1; fi

  echo -n "④ 排程是否還在（Status 欄應為 ok，不應出現 error/failed）："
  local cron_out cron_ok cron_bad
  cron_out=$("$OPENCLAW" cron list 2>/dev/null)
  cron_ok=$(echo "$cron_out" | grep -cE "\bok\b")
  cron_bad=$(echo "$cron_out" | grep -cE "\b(error|failed)\b")
  echo "${cron_ok} 筆正常"
  [[ "$cron_bad" -gt 0 ]] && { echo "   🔴 有 ${cron_bad} 筆排程狀態異常"; rc=1; }

  echo -n "⑤ 報名端點是否還活著："
  curl -s -m 15 -X POST https://event.bymyway.com/api/register \
    -H 'Content-Type: application/json' -d '{}' | grep -q "missing" \
    && echo "✅ 正常回應" || { echo "🔴 沒有正常回應"; rc=1; }

  echo
  if [[ $rc -eq 0 ]]; then
    echo "✅ 全部通過，升級成功。"
  else
    echo "🔴 有項目沒過——如要退回：bash scripts/openclaw_upgrade.sh rollback"
  fi
  return $rc
}

cmd_rollback() {
  if [[ ! -f "$VERSION_FILE" ]]; then
    echo "❌ 找不到升級前的版本記錄（$VERSION_FILE），無法自動回退"; return 1
  fi
  local before; before="$(cat "$VERSION_FILE")"
  echo "═══ 回退到 $before ═══"
  "$NPM" install -g "openclaw@$before" || { echo "❌ 回退安裝失敗"; return 1; }
  "$OPENCLAW" gateway restart 2>&1 | tail -3
  sleep 15
  echo "已回退，現在版本：$(current)"
  echo "⚠️ 設定檔沒有自動還原（升級不會改設定檔）；若真的被改到，"
  echo "   備份在 ~/.openclaw/openclaw.json.bak-before-upgrade-*"
}

case "${1:-check}" in
  check)    cmd_check ;;
  upgrade)  cmd_upgrade ;;
  verify)   cmd_verify ;;
  rollback) cmd_rollback ;;
  *) echo "用法：$0 {check|upgrade|verify|rollback}"; exit 2 ;;
esac
