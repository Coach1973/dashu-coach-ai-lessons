#!/bin/bash
# ⚠️ 【Windows 聯想機專用，本機（Mac）不適用】2026-08-25 賈維斯體檢標註
# Mac 端同功能已在 stop_rules_master.py 規則 I（繁體字鎖）內，這支是給聯想那台用的，
# 在 Mac 沒註冊進 settings.json 是正確狀態，不是漏裝。
# 已合併：Stop（Windows 端專用，Mac 實際執行者為 stop_rules_master.py）
# 用途：掃描這一輪最終回覆文字，偵測是否混入簡體字，命中 → exit 2 強制重新檢查並修正
# 設計理念：不靠模型自覺（教練第4次抓到AI輸出滑成簡體字，前3次都在Mac的OpenClaw系統靠rule_traditional_chinese_check.sh擋下，
#           這台Windows的Claude Code從沒配過同款機制），用grep確定性檢查，比照Mac那套邏輯
# 對齊：全繁體中文鐵律（memory: feedback_chinese_only.md，試金石案例44）
# 環境差異：這台機器沒裝jq、python3是WindowsApps壞掉的stub（exit 49），改用node.js做JSON解析
# 保護機制：偵測 stop_hook_active=true 時放行，避免無限迴圈
# 軍師建立 2026-07-25（案例44第4犯後，聯想Windows Claude Code補漏）
set -uo pipefail

INPUT=$(cat)

STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | node -e "
try { const d = JSON.parse(require('fs').readFileSync(0,'utf8')); process.stdout.write(String(!!d.stop_hook_active)); } catch(e) { process.stdout.write('false'); }
" 2>/dev/null)
[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0

TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | node -e "
try { const d = JSON.parse(require('fs').readFileSync(0,'utf8')); process.stdout.write(d.transcript_path || ''); } catch(e) {}
" 2>/dev/null)
[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

LAST_TEXT=$(node -e "
const fs = require('fs');
const path = process.argv[1];
let lines;
try { lines = fs.readFileSync(path, 'utf8').split('\n').filter(l => l.trim()); } catch(e) { process.exit(0); }
let lastText = '';
for (let i = lines.length - 1; i >= 0; i--) {
  let evt;
  try { evt = JSON.parse(lines[i]); } catch(e) { continue; }
  if (evt.type === 'assistant') {
    const content = evt.message && evt.message.content;
    if (Array.isArray(content)) {
      lastText = content.filter(c => c && c.type === 'text').map(c => c.text || '').join('\n');
    } else if (typeof content === 'string') {
      lastText = content;
    }
    break;
  }
}
process.stdout.write(lastText);
" "$TRANSCRIPT_PATH" 2>/dev/null)

[[ -z "$LAST_TEXT" ]] && exit 0

# 簡體字專用字元表（僅列「簡體特有、不會出現在正常繁體文字」的高頻字，避免誤判），與Mac版同一份清單
SIMPLIFIED_CHARS='这|讲|们|读|时|间|触|设|帐|额|门|儿|发|开|关|报|华|归|图|网|页|数|应|术|处|战|显|复|备|环|层|阶|观|议|语|记|认|识|让|从|众|学|国|说|话|现|会|对|还|过|动|转|输|变|传|车|军|阵|队|员|团|独|电|视|频|络|该|种|样|专|习|亲|头|简|构|济|导|计|谁|难|临|尽|尝|双|书|终|绝|细|统|继|绍|补|龙|阳|阴|币|达|与|灵|码|钱|银|销|营'

MATCHED=""
while IFS= read -r ch; do
  [[ -z "$ch" ]] && continue
  MATCHED="${MATCHED}${ch}、"
done < <(printf '%s' "$LAST_TEXT" | grep -oE "$SIMPLIFIED_CHARS" | sort -u)
MATCHED="${MATCHED%、}"

[[ -z "$MATCHED" ]] && exit 0

LOG="/e/Claude-Data/mac-openclaw-workflows/distill/rule_traditional_chinese_violations_win.log"
mkdir -p "$(dirname "$LOG")"
{
  printf '[%s] matched=%s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$MATCHED"
} >> "$LOG"

{
  printf '\n🈶🔒 繁體字鎖違規偵測（Windows Claude Code, deterministic check）\n'
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  printf '這一輪回覆裡偵測到疑似簡體字：%s\n\n' "$MATCHED"
  printf '📜 全繁體中文鐵律（教練唯一指定，第4犯，2026-07-25）：\n'
  printf '  「對話全程繁體中文，不夾簡體、不夾英文」\n\n'
  printf '✅ 正確做法（請立刻檢查並修正）：\n'
  printf '  1. 回頭逐字檢查剛才的回覆，把上面列出的每個字改成繁體對應字\n'
  printf '  2. 常見對照：这→這 讲→講 们→們 读→讀 时→時 间→間 设→設 额→額 发→發 开→開 关→關\n'
  printf '  3. 重新輸出乾淨的繁體版本給教練，不要只回覆這次有改就好，要整段重新確認過一遍\n\n'
  printf '違規記錄已寫入：%s\n' "$LOG"
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
} >&2

exit 2
