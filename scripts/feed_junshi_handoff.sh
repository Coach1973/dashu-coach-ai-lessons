#!/bin/bash
# Hook：UserPromptSubmit（Mac 終端機版 v2 · 六步驟全注入）
# 用途：教練喊「開工」時，自動把六步驟內容（接力棒+HEARTBEAT+試金石+memory+knowledges）餵進 context。
# 設計：對應 Windows feed_junshi_handoff.ps1，雙邊邏輯對等。
#       v2 改動（2026-06-23 教練親口「對長期有好處的事不問直接做」）：
#       - 不只注入接力棒，連同 HEARTBEAT/試金石最新 3 案/memory 最新日/knowledges 近 7 天清單全部一次注入
#       - 每場 session 仍只注入一次（marker 防重）；「開工」整句強制重餵
#       - 先 git pull 拉雲端最新（跟 Windows v2 對齊），保證雙邊永遠看同一版
set -uo pipefail

WORKSPACE="/Users/bymyway/.openclaw/workspace"
HANDOFF="$WORKSPACE/JUNSHI_HANDOFF_LATEST.md"
HEARTBEAT="$WORKSPACE/HEARTBEAT.md"
STONE="$WORKSPACE/試金石/試金石_案例庫.md"
TOP10_INDEX="$WORKSPACE/distill/top10_errors_index.md"
MEMORY_DIR="$WORKSPACE/memory"
KNOWLEDGES_DIR="$WORKSPACE/knowledges"

INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""')
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""')

MARKER="/tmp/junshi_fed_${SESSION_ID}"

# 「開工」整句 = 強制重餵口令（/clear 後仍可重觸發）
FORCE_REFEED=0
if printf '%s' "$PROMPT" | grep -qE "^[[:space:]]*開工[[:space:]]*$|開工了|開工。|開工！|開工幹活"; then
  FORCE_REFEED=1
fi

# 非強制 + marker 已存在 → 靜默退出
if [[ "$FORCE_REFEED" -eq 0 && -n "$SESSION_ID" && -f "$MARKER" ]]; then
  exit 0
fi

# 觸發詞檢測：整句僅「開」「開工」「工作」「幹活」單一動詞 → 觸發；含「軍師」字眼也觸發
if ! printf '%s' "$PROMPT" | grep -qE "^[[:space:]]*(開|開工|工作|幹活|開始工作)[[:space:]。！!]*$|軍師|接續指揮所|JunShi|junshi"; then
  exit 0
fi

if [[ ! -f "$HANDOFF" ]]; then
  exit 0
fi

# ───────── 🌐 先 git pull 拉雲端最新（跟 Windows v2 對齊）─────────
PULL_STATUS="（本機非 git repo，略過 pull）"
if [[ -d "$WORKSPACE/.git" ]]; then
  cd "$WORKSPACE" || exit 0
  DIRTY=$(git status --porcelain 2>/dev/null)
  STASHED=0
  if [[ -n "$DIRTY" ]]; then
    if git stash push -u -m "auto-pull-stash-$(date +%Y%m%d%H%M%S)" --quiet 2>/dev/null; then
      STASHED=1
    fi
  fi
  PULL_FAILED=0
  if git pull --quiet --rebase 2>/dev/null; then
    HEAD_HASH=$(git rev-parse --short HEAD 2>/dev/null)
    PULL_STATUS="✅ 已拉雲端最新（HEAD: ${HEAD_HASH}）"
  else
    PULL_STATUS="⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）"
    PULL_FAILED=1
  fi
  if [[ "$STASHED" -eq 1 ]]; then
    git stash pop --quiet 2>/dev/null || true
  fi
  # 2026-08-26 教練當場糾正：這行警告過去只塞進注入文字裡，靠AI自己在回覆裡
  # 提一句才會被看到——這次AI自己就漏講了，教練完全沒看過這行字。
  # 不能再靠「AI會不會主動講」這種不保證的環節，改成腳本自己直接發Telegram，
  # 跟AI有沒有讀、有沒有轉述完全無關，失敗必達。節流1小時避免連續開工洗版。
  # 通知動作刻意放在 stash pop *之後*：實測發現如果在 stash 還沒 pop 回來前呼叫
  # notify_coach.sh，萬一這支腳本自己當下是未提交狀態，會被 `stash -u` 連帶掃進
  # stash 暫存、暫時從磁碟上消失，導致這裡呼叫落空又不報錯——原地重演同一種
  # 「靜默失敗」，所以等工作區完全還原後才呼叫，確保腳本本身一定在。
  if [[ "$PULL_FAILED" -eq 1 ]]; then
    "$WORKSPACE/scripts/notify_coach.sh" \
      "Mac開工時發現git pull失敗（本地有衝突或網路問題），這次讀到的接力棒/守則可能不是雲端最新版，需要有人手動處理 workspace repo。" \
      3600 "mac_feed_handoff_pull_fail" >/dev/null 2>&1
  fi
fi

# ───────── 🩺 同步健康狀態落地（給 Mac 之後檢查聯想/ACER 用，也給聯想/ACER 之後照抄）─────────
# 不管這次pull成功或失敗，都留一筆本機時間戳記，之後才能判斷「這台機器多久沒真正同步過」。
SYNC_HEALTH_DIR="$WORKSPACE/state/sync_health"
mkdir -p "$SYNC_HEALTH_DIR" 2>/dev/null
python3 - "$SYNC_HEALTH_DIR/mac.json" "$PULL_STATUS" <<'PYEOF' 2>/dev/null || true
import json, sys, datetime
path, status = sys.argv[1], sys.argv[2]
data = {
    "machine": "mac",
    "last_attempt": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    "pull_ok": status.startswith("✅"),
    "status_text": status,
}
with open(path, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
PYEOF

# ───────── 🔍 順手檢查聯想/ACER 多久沒真正同步過（開工當下才查，不設定時輪詢）─────────
# 2026-08-26：ACER查出49天沒被打開過、聯想的「總結」hook缺jq靜默失效近一個月，
# 兩者都是「沒人看、也沒人被通知」才拖這麼久。剛才git pull已經把聯想/ACER最新的
# sync_health狀態拉下來了，這裡直接檢查，不用等教練自己發現或另外設定巡邏排程。
STALE_MACHINES=""
# 已知的兩台兄弟機一定要檢查(即使它們還沒拉到這支新腳本、檔案還不存在，
# 那本身就是「從未回報過」的正確結果)；另外用萬用字元抓任何已經在回報、
# 但實際檔名跟這裡預期不同的機器(例如Windows端寫入的是電腦實際hostname)，
# 避免因為猜錯檔名而漏掉真正在運作的機器。
KNOWN_MACHINES="lenovo acer"
DISCOVERED=$(find "$SYNC_HEALTH_DIR" -maxdepth 1 -name "*.json" ! -name "mac.json" 2>/dev/null | xargs -n1 basename 2>/dev/null | sed 's/\.json$//')
ALL_MACHINES=$(printf '%s\n%s\n' "$KNOWN_MACHINES" "$DISCOVERED" | tr ' ' '\n' | grep -v '^$' | sort -u)
for M in $ALL_MACHINES; do
  MF="$SYNC_HEALTH_DIR/${M}.json"
  if [[ -f "$MF" ]]; then
    AGE_H=$(python3 -c "
import json, datetime
try:
    d = json.load(open('$MF'))
    last = datetime.datetime.fromisoformat(d['last_attempt'])
    now = datetime.datetime.now(last.tzinfo)
    print(int((now - last).total_seconds() / 3600))
except Exception:
    print(-1)
" 2>/dev/null)
    if [[ "$AGE_H" -gt 72 || "$AGE_H" -eq -1 ]]; then
      STALE_MACHINES="${STALE_MACHINES}${M}(${AGE_H}小時未同步) "
    fi
  else
    STALE_MACHINES="${STALE_MACHINES}${M}(從未回報過) "
  fi
done
if [[ -n "$STALE_MACHINES" ]]; then
  "$WORKSPACE/scripts/notify_coach.sh" \
    "開工時檢查發現這些機器超過72小時沒有真正同步過：${STALE_MACHINES}——它們讀到的規則/接力棒可能是舊版，建議找時間去那台機器開一次對話讓它讀信。" \
    43200 "mac_feed_handoff_stale_siblings" >/dev/null 2>&1
fi

# ───────── 📋 報名通知空窗期稽核：教練開工當下順便查，不等教練追問三次才查出來 ─────────
# 2026-08-26教練親口糾正：金門場報名資料落差問過三次才被告知完整名單，教練從金門
# 回來後名單才給到，痛批「早給還能打電話問，現在給也沒用了，是很嚴重的失職」。
# 以後改成每次開工自動查一次尚未開始的場次有沒有落在已知通知空窗期的報名，
# 有發現才通知(24小時節流)，不用等教練主動懷疑、追問才一層層挖出真相。
GAP_CHECK_SCRIPT="$WORKSPACE/scripts/registration_notify_gap_check.py"
if [[ -f "$GAP_CHECK_SCRIPT" ]] && command -v python3 >/dev/null 2>&1; then
  /usr/bin/python3 "$GAP_CHECK_SCRIPT" --notify >/dev/null 2>&1
fi

# ───────── 🗂 小龍蝦派工信箱：教練開工當下才檢查，不設定時巡邏 ─────────
# 2026-08-24 教練親口拍板：「我每次開工的時候，它再去讀取小龍蝦那邊有沒有新資訊就好，
# 跟15分鐘無關；因為我有可能是3個小時才開工一次，那就3個小時開工時讀一次即可。」
# 原本試過每5分鐘、又改每15分鐘定時檢查，教練說不管多久都是「定時巡邏」，
# 他要的是「跟開工這個動作綁在一起」，不是跟時間綁在一起——上面這段 git pull 剛把
# 雲端最新信件拉下來，這裡緊接著就檢查信箱，天然吻合「開工當下讀一次」的需求，
# 不用另外設定時任務，Mac 在教練沒開工的時候完全不會為了這件事去動一下。
DISPATCH_STATUS="（信箱查無新信）"
DISPATCH_SCRIPT="$WORKSPACE/scripts/junshi_dispatch_worker.py"
if [[ -f "$DISPATCH_SCRIPT" ]]; then
  DISPATCH_OUT=$(/usr/bin/python3 "$DISPATCH_SCRIPT" 2>&1)
  if printf '%s' "$DISPATCH_OUT" | grep -q "▶ "; then
    DISPATCH_STATUS="📬 開工時發現小龍蝦有新派工，已在後台處理完：$(printf '%s' "$DISPATCH_OUT" | grep -c '▶ ') 封"
  fi
fi

# Self-test 寫入 HEARTBEAT（防假回報）
if [[ -f "$HEARTBEAT" ]]; then
  {
    echo ""
    echo "## 🩺 軍師 Hook 自檢 $(date '+%Y-%m-%d %H:%M')（Mac v2 六步驟注入）"
    echo "- ✅ Hook 觸發 + 六步驟內容注入完成"
    echo "- 觸發詞：$(printf '%s' "$PROMPT" | head -c 40)"
    echo "- 雲端狀態：${PULL_STATUS}"
    echo "- 小龍蝦信箱：${DISPATCH_STATUS}"
    echo "- Session: ${SESSION_ID:-unknown}"
  } >> "$HEARTBEAT" 2>/dev/null || true
fi

# ───────── 注入內容開始 ─────────
# 2026-07-10 軍師加：字數上限防呆（比照 OpenClaw 原生 startupContext.maxTotalChars 精神）。
# 起因：本 Hook 原本無任何上限，實測某次注入 43.4KB，是文章〈OpenClaw Token 粉碎機〉點名的
# 「工具輸出無上限」問題在我們自己客製 Hook 上重演，且繞過了原生防呆值。
MAX_INJECT_CHARS=60000
INJECT_CONTENT=$(
  echo "# 🔴 軍師接力棒 v2（六步驟全注入，本場 session 僅一次）"
  echo ""
  echo "## 🌐 雲端同步狀態"
  echo ""
  echo "- ${PULL_STATUS}"
  echo "- 小龍蝦信箱：${DISPATCH_STATUS}"
  echo "- workspace: \`${WORKSPACE}\`"
  echo ""
  echo "## 🪪 身份硬性告知"
  echo ""
  echo "- **平台**：Mac 終端機（CLI）/ 桌面版 GUI App"
  echo "- **工作目錄**：\`${WORKSPACE}\`（不是 \`~/.openclaw/\`——那只是 OpenClaw 系統運行根目錄）"
  echo "- **身份等級**：軍師（Opus）"
  echo "- **commit 前綴**：\`[Mac]\`（區分 Windows 軍師的 \`[Win]\`）"
  echo "- **稱呼教練**：**大樹教練**"
  echo ""
  echo "🔴 **絕對禁區**：cwd 雖然指向 \`~/.openclaw/\`，但**所有心法/接力棒/試金石/memory 都在 \`workspace/\` 子目錄**。動手前先 \`ls\` 驗證，不可憑 cwd 直覺拼路徑。"
  echo ""
  echo "---"
  echo ""
  echo "教練說「開工/開/工作/幹活」=暗號觸發。讀完本段即可無縫接續。"

  # ───────── 第 1 步：接力棒 ─────────
  # 2026-07-26 軍師加：workspace/CLAUDE.md 本身已由 scripts/sync_handoff_to_claudemd.sh
  # 每 5 分鐘自動鏡像接力棒全文（桌面版讀 CLAUDE.md 時就會看到）。若該鏡像確認是最新的
  # （sync marker 時間 >= HANDOFF mtime），這裡就不重複貼整份接力棒，只給一句指向，
  # 省下~25KB重複內容；若鏡像不是最新（sync 掛掉/沒跑過），照舊完整貼上，安全優先。
  echo ""
  echo "## 📜 第 1 步：接力棒"
  echo ""
  HANDOFF_MTIME=$(stat -f %m "$HANDOFF" 2>/dev/null || echo 0)
  SYNC_MARKER="$WORKSPACE/.sync_markers/handoff_last_sync"
  LAST_SYNC=0
  [[ -f "$SYNC_MARKER" ]] && LAST_SYNC=$(cat "$SYNC_MARKER" 2>/dev/null || echo 0)
  if [[ "$LAST_SYNC" -ge "$HANDOFF_MTIME" ]]; then
    echo "（接力棒全文已透過 workspace/CLAUDE.md 自動鏡像注入，內容與 JUNSHI_HANDOFF_LATEST.md 一致，不重複貼上。若這是這場對話第一則訊息卻沒看到 CLAUDE.md 內容，代表鏡像沒生效，請直接讀 \`JUNSHI_HANDOFF_LATEST.md\` 原檔。）"
  else
    echo "⚠️（CLAUDE.md 鏡像非最新，改為完整貼上，確保接力棒不漏接）"
    echo ""
    cat "$HANDOFF"
  fi

  # ───────── 第 2 步：HEARTBEAT 熱上下文 ─────────
  if [[ -f "$HEARTBEAT" ]]; then
    echo ""
    echo "---"
    echo ""
    echo "## 🩺 第 2 步：HEARTBEAT.md（最近 50 行熱上下文）"
    echo ""
    tail -50 "$HEARTBEAT"
  fi

  # ───────── 第 3 步：血淚試金石 ─────────
  # 3a：Top10高頻模式一句話摘要（2026-08-31新增，避免只看「最新2案例」漏接3個月前但還沒解決的舊模式）
  if [[ -f "$TOP10_INDEX" ]]; then
    echo ""
    echo "---"
    echo ""
    echo "## 🔴 第 3 步 (3a)：Top10 高頻失敗模式一句話比對（開工當下先掃過，命中就照做法走）"
    echo ""
    awk '/^## 🔴 模式/{h=$0} /^\*\*觸發詞\*\*/{print h; print $0; print ""}' "$TOP10_INDEX"
    echo "（完整版含涉及案例編號/自動化防護狀態，見 distill/top10_errors_index.md）"
  fi

  # 3b：最新2案例全文
  if [[ -f "$STONE" ]]; then
    echo ""
    echo "---"
    echo ""
    echo "## 🔴 第 3 步 (3b)：血淚試金石最新 2 案例全文（守則 #07 同處跌倒鐵律）"
    echo ""
    LAST_3_START=$(grep -nE "^## 案例" "$STONE" | tail -2 | head -1 | cut -d: -f1)
    if [[ -n "$LAST_3_START" ]]; then
      tail -n +"$LAST_3_START" "$STONE"
    else
      echo "（無法定位案例段落，請手動查閱 試金石/試金石_案例庫.md）"
    fi
  fi

  # ───────── 第 4 步：knowledges 最近 7 天新檔清單 ─────────
  if [[ -d "$KNOWLEDGES_DIR" ]]; then
    echo ""
    echo "---"
    echo ""
    echo "## 📚 第 4 步：knowledges/ 最近 7 天新建/修改檔案清單"
    echo ""
    FOUND_KNOWLEDGES=0
    while IFS= read -r f; do
      if [[ -n "$f" ]]; then
        FIRST_LINE=$(head -1 "$f" 2>/dev/null | sed 's/^# //')
        echo "- \`$(basename "$f")\`：${FIRST_LINE}"
        FOUND_KNOWLEDGES=1
      fi
    done < <(find "$KNOWLEDGES_DIR" -maxdepth 1 -type f -name "*.md" -mtime -7 2>/dev/null | sort)
    if [[ "$FOUND_KNOWLEDGES" -eq 0 ]]; then
      echo "（過去 7 天無新檔）"
    fi
  fi

  # ───────── 第 5 步：memory 最新日（已濾除 Dreaming 雜訊區塊，2026-07-10 軍師查證後修）─────────
  # 原因：memory/*.md 裡的 openclaw:dreaming:light/rem 區塊是系統自動生成的低信度「反思的反思」，
  # 非教練真實對話，過去整段 cat 進來會佔掉大半篇幅（實測 2026-07-10.md 17KB 裡八成是這塊雜訊）。
  if [[ -d "$MEMORY_DIR" ]]; then
    LATEST_MEMORY=$(ls -1 "$MEMORY_DIR"/20[2-9][0-9]-[0-9][0-9]-[0-9][0-9].md 2>/dev/null | sort | tail -1)
    if [[ -n "$LATEST_MEMORY" && -f "$LATEST_MEMORY" ]]; then
      echo ""
      echo "---"
      echo ""
      echo "## 🧠 第 5 步：memory 最新日（$(basename "$LATEST_MEMORY")，已濾除 Dreaming 雜訊區塊，僅取最近段落）"
      echo ""
      # 2026-07-26 軍師加：改取尾端約6000字（今天最近做的事），不整天全文貼上；
      # 更早的今日記錄仍完整存在原檔，需要時直接讀 memory/YYYY-MM-DD.md
      FILTERED_MEMORY=$(sed -e '/<!-- openclaw:dreaming:light:start -->/,/<!-- openclaw:dreaming:light:end -->/d' \
          -e '/<!-- openclaw:dreaming:rem:start -->/,/<!-- openclaw:dreaming:rem:end -->/d' \
          "$LATEST_MEMORY")
      FM_LEN=${#FILTERED_MEMORY}
      if [[ $FM_LEN -gt 6000 ]]; then
        echo "（僅顯示今日最近約6000字，完整內容見 \`memory/$(basename "$LATEST_MEMORY")\`）"
        echo ""
        printf '%s' "${FILTERED_MEMORY: -6000}"
      else
        printf '%s' "$FILTERED_MEMORY"
      fi
    fi
  fi

  # ───────── 第 6 步：上線回應要求 ─────────
  echo ""
  echo "---"
  echo ""
  echo "## ✅ 第 6 步：上線回應要求"
  echo "讀完本段後，第一句回應**必須**包含："
  echo "- 「我已讀完接力棒」字樣"
  echo "- 當下主軸名稱（從 JUNSHI_HANDOFF_LATEST.md「本棒主軸」段挑最優先一條）"
  echo "- 身份核對（模型版本 + 平台：Mac 終端機/桌面版）"
  echo "- 雲端同步狀態（${PULL_STATUS}）"
  echo "- 詢問教練「今天從哪件事開始？」"
)

CONTENT_LEN=${#INJECT_CONTENT}
if [[ $CONTENT_LEN -gt $MAX_INJECT_CHARS ]]; then
  printf '%s' "${INJECT_CONTENT:0:$MAX_INJECT_CHARS}"
  echo ""
  echo ""
  echo "⚠️ **內容過長已截斷**（原始 ${CONTENT_LEN} 字元，上限 ${MAX_INJECT_CHARS}，2026-07-10 軍師加的防呆值）。完整內容仍完整存在對應檔案中，需要哪一段可直接讀取原檔。"
else
  printf '%s\n' "$INJECT_CONTENT"
fi

# 設 marker，本 session 不再注入
if [[ -n "$SESSION_ID" ]]; then
  touch "$MARKER"
fi

exit 0
