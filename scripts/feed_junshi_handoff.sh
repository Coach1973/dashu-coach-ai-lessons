#!/bin/bash
# Hook：UserPromptSubmit（Mac 終端機版 v3 · 心法＋最新一棒，2026-10-02）
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
HOOK_CWD=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.cwd // ""')

MARKER="/tmp/junshi_fed_${SESSION_ID}"

# 「開工」整句 = 強制重餵口令（/clear 後仍可重觸發）
FORCE_REFEED=0
if printf '%s' "$PROMPT" | grep -qE "^[[:space:]]*開工[0-9０-９:：[:space:]]*$|開工了|開工。|開工！|開工幹活"; then
  FORCE_REFEED=1
fi

# 非強制 + marker 已存在 → 靜默退出
if [[ "$FORCE_REFEED" -eq 0 && -n "$SESSION_ID" && -f "$MARKER" ]]; then
  exit 0
fi

# 觸發詞檢測：整句僅「開」「開工」「工作」「幹活」單一動詞 → 觸發；含「軍師」字眼也觸發
if ! printf '%s' "$PROMPT" | grep -qE "^[[:space:]]*(開|開工|工作|幹活|開始工作)[0-9０-９:：[:space:]。！!]*$|軍師|接續指揮所|JunShi|junshi"; then
  exit 0
fi

if [[ ! -f "$HANDOFF" ]]; then
  exit 0
fi

# ───────── 🌐 先 git pull 拉雲端最新（跟 Windows v2 對齊）─────────
# 2026-09-01 教練親口糾正：這段舊版用 `git pull --rebase`，但 workspace 裡
# terminal-notes/raw_sessions/*.jsonl、state/inbound_echo/*.jsonl 這類檔案
# 是這場對話自己即時在寫的（session逐字記錄+訊息落地），rebase 要求工作區
# 完全乾淨，幾乎每次「開工」當下都會撞到這些正在被寫入的檔案，導致近乎每次
# 都觸發「pull失敗」假警報（查 notify_coach.log 確認 8/30~9/1 至少6次）。
# 改用 fetch+ff-only merge：這種合併方式不要求工作區乾淨，只要incoming
# commits沒有動到本機正在變動的那幾個檔案就能成功，才是真正對應這個
# workspace「本機一直有背景寫入」這個常態的做法。ff-only失敗（真正分岔，
# 非僅髒污）才退回舊的 stash+rebase 流程搶救。
# 2026-09-27：KAIGONG_SELFTEST=1 時只產生注入內容給 test_kaigong_injection.sh 檢查，
# 不拉雲端、不發通知、不處理信箱、不寫log、不設marker（開工漏接三次都是注入內容的洞，要能反覆實測）
SELFTEST="${KAIGONG_SELFTEST:-0}"
PULL_STATUS="（自我測試，略過 pull）"
DISPATCH_STATUS="（自我測試，略過信箱）"
if [[ "$SELFTEST" != 1 ]]; then
PULL_STATUS="（本機非 git repo，略過 pull）"
if [[ -d "$WORKSPACE/.git" ]]; then
  cd "$WORKSPACE" || exit 0
  BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  PULL_FAILED=0
  POP_CONFLICT=0
  if git fetch --quiet 2>/dev/null && git merge --quiet --ff-only "origin/${BRANCH}" 2>/dev/null; then
    HEAD_HASH=$(git rev-parse --short HEAD 2>/dev/null)
    PULL_STATUS="✅ 已拉雲端最新（HEAD: ${HEAD_HASH}）"
  else
    # ff-only 失敗，代表本機有真正未推送的commit（非僅髒污檔案），才需要 stash+rebase 搶救
    DIRTY=$(git status --porcelain 2>/dev/null)
    STASHED=0
    if [[ -n "$DIRTY" ]]; then
      if git stash push -u -m "auto-pull-stash-$(date +%Y%m%d%H%M%S)" --quiet 2>/dev/null; then
        STASHED=1
      fi
    fi
    if git pull --quiet --rebase 2>/dev/null; then
      HEAD_HASH=$(git rev-parse --short HEAD 2>/dev/null)
      PULL_STATUS="✅ 已拉雲端最新（HEAD: ${HEAD_HASH}，經rebase搶救）"
    else
      PULL_FAILED=1
    fi
    POP_CONFLICT=0
    if [[ "$STASHED" -eq 1 ]]; then
      if ! git stash pop --quiet 2>/dev/null; then
        # 2026-09-05修復（ACER案例同款坑）：舊版用`|| true`吞掉stash pop衝突，
        # 衝突標記(<<<<<<< / ======= / >>>>>>>)會被寫進檔案卻毫無警示，只留一句
        # 「已拉雲端最新」誤導後續動作，衝突有可能被下一次commit直接汙染共用檔案。
        # 改成明確列出受影響檔案，stash留著不清掉，逼自己/教練手動處理。
        CONFLICT_FILES=$(git diff --name-only --diff-filter=U 2>/dev/null | tr '\n' ' ')
        PULL_STATUS="🔴 stash pop 衝突未解決！受影響檔案：${CONFLICT_FILES}——本地改動仍在stash裡，請手動 git stash pop 並解決衝突，不要直接commit"
        POP_CONFLICT=1
      fi
    fi
    # 2026-09-05補強（聯想同日實測撞到的邊界情況）：pop 回報成功(exit 0)但工作區
    # 仍殘留衝突標記的情況也要抓，不能只信 pop 的 exit code。
    if [[ "$POP_CONFLICT" -eq 0 ]]; then
      if git status --porcelain 2>/dev/null | grep -qE '^(UU|AA|DD|AU|UA|UD|DU) '; then
        CONFLICT_FILES=$(git diff --name-only --diff-filter=U 2>/dev/null | tr '\n' ' ')
        PULL_STATUS="🔴 stash pop 衝突未解決！受影響檔案：${CONFLICT_FILES}——工作區殘留衝突標記，請手動檢查解決，不要直接commit"
        POP_CONFLICT=1
      fi
    fi
    if [[ "$POP_CONFLICT" -eq 1 ]]; then
      PULL_FAILED=1
    fi
  fi
  # 三關判定才通知（2026-08-05教練親口「不影響工作就別吵我」同一原則）：
  # ①現在還真的壞嗎——跟origin比對HEAD，一致就代表最終結果是好的，不管中途
  #   哪個步驟報過失敗字樣，都不算數，不通知。②非暫時性——已經試過ff-only
  #   +stash rebase兩種手法都失敗才算真的卡住。二者都過才發Telegram。
  # 注意：POP_CONFLICT是「working tree被寫進衝突標記」的獨立問題，不能套用這套
  # 「HEAD追上origin就算好」的判定——衝突標記已經實際存在於檔案裡，跟HEAD對不對得上無關，
  # 一旦POP_CONFLICT成立就一定要通知，不能被下面的HEAD比對覆蓋掉。
  if [[ "$POP_CONFLICT" -eq 1 ]]; then
    "$WORKSPACE/scripts/notify_coach.sh" \
      "開工時git stash pop發生衝突，衝突標記已寫進檔案(${CONFLICT_FILES})，需要有人手動解決，不要讓後續commit把衝突標記帶上去。" \
      3600 "feed_handoff_pop_conflict" >/dev/null 2>&1
  elif [[ "$PULL_FAILED" -eq 1 ]]; then
    REMOTE_HASH=$(git rev-parse --short "origin/${BRANCH}" 2>/dev/null)
    LOCAL_HASH=$(git rev-parse --short HEAD 2>/dev/null)
    if [[ -n "$REMOTE_HASH" && "$REMOTE_HASH" == "$LOCAL_HASH" ]]; then
      PULL_STATUS="✅ 已是雲端最新（HEAD: ${LOCAL_HASH}，中途fetch/merge雖報錯但結果一致）"
    else
      PULL_STATUS="⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）"
      "$WORKSPACE/scripts/notify_coach.sh" \
        "Mac開工時發現git pull失敗（本地有衝突或網路問題），這次讀到的接力棒/守則可能不是雲端最新版，需要有人手動處理 workspace repo。" \
        3600 "mac_feed_handoff_pull_fail" >/dev/null 2>&1
    fi
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

# ───────── 🔕 2026-09-01教練拍板取消：跨機72小時未同步通知（原規則已移除）─────────
# 原本這裡會比對 sync_health_dir 下 lenovo.json/acer.json 等固定檔名的心跳時間戳，
# 超過72小時就發Telegram通知教練。但這個心跳檔案系統跟git commit是兩件不同的事：
# acer/lenovo那幾台機器其實都有正常總結、有真實commit(教練這邊查得到)，但因為
# 這支心跳腳本沒在那幾台機器上真正跑起來(或寫入的檔名跟這裡預期的不同，例如
# Windows端曾經寫入的是電腦實際hostname而非"lenovo")，導致天天誤報「從未回報過」
# 造成教練困擾。教練口頭裁示直接取消，不做檔名對照修正。若未來要重新做這類跨機
# 健康檢查，判斷依據應改讀各機器workspace repo的git log，而不是這個自訂心跳檔案。

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

# Self-test 寫入本機log（防假回報）。不寫HEARTBEAT.md：那是小龍蝦開機必讀檔，2026-09-25查到
# 軍師日誌佔它78%、撐破2萬字上限；原本的head -c 40照位元組切還把中文字切成亂碼寫進去。
{
  echo ""
  echo "## 🩺 軍師 Hook 自檢 $(date '+%Y-%m-%d %H:%M')（Mac v2 六步驟注入）"
  echo "- ✅ Hook 觸發 + 六步驟內容注入完成"
  echo "- 觸發詞：$(printf '%s' "$PROMPT" | python3 -c 'import sys; print(sys.stdin.read()[:40])')"
  echo "- 雲端狀態：${PULL_STATUS}"
  echo "- 小龍蝦信箱：${DISPATCH_STATUS}"
  echo "- Session: ${SESSION_ID:-unknown}"
} >> "$WORKSPACE/state/junshi_automation.log" 2>/dev/null || true
fi  # SELFTEST 結束

# ───────── 注入內容開始 ─────────
# 2026-07-10 軍師加：字數上限防呆（比照 OpenClaw 原生 startupContext.maxTotalChars 精神）。
# 起因：本 Hook 原本無任何上限，實測某次注入 43.4KB，是文章〈OpenClaw Token 粉碎機〉點名的
# 「工具輸出無上限」問題在我們自己客製 Hook 上重演，且繞過了原生防呆值。
# 2026-09-18 教練親自糾正：手機Remote Control(claude rc，透過tmux啟動)連進來的session
# 也會觸發這支hook，但下面原本寫死「軍師（Opus）」，導致MiniMax session誤自稱Opus軍師，
# 教練當場抓到兩個手機session都自稱Opus、根因就是這行寫死字串。
# 判斷依據（實測`ps eww`確認）：這台Mac全域shell環境本來就有ANTHROPIC_DEFAULT_OPUS_MODEL=
# MiniMax-M3等三個模型別名（不能拿來判斷，任何session都看得到這組值），真正的分歧點是
# claude rc host process啟動指令是`env -u ANTHROPIC_BASE_URL -u ANTHROPIC_API_KEY ... claude rc`
# ——手動清空這兩個真Anthropic憑證變數，逼子session退回用DEFAULT_*別名解析成MiniMax。
# 2026-09-25教練親自抓到：桌面版App(Code分頁)走OAuth登入，本來就不會設ANTHROPIC_API_KEY，
# 只有ANTHROPIC_BASE_URL(=https://api.anthropic.com)存在，原本「兩個缺一個就算手機」的
# 判斷把這種正常桌面版session也誤判成手機，導致第4步(knowledges)被跳過、身份也報錯。
# 手機host process的真實特徵是「兩個變數都被清空」，改用AND才符合實際情況。
if [ -z "${ANTHROPIC_BASE_URL:-}" ] && [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  IDENTITY_LINE="特助（MiniMax-M3，透過手機Remote Control連線，非Opus，額度與其他小龍蝦系統共用，需注意額度消耗）"
  IS_MOBILE=1
else
  IDENTITY_LINE="軍師（本機Claude session；實際模型請以每則assistant訊息的 message.model 欄位或系統提示為準，不要自行假設是Opus）"
  IS_MOBILE=0
fi
# 2026-09-18 教練問「要不要另設『手機開工』暗號區分」，軍師判斷：既然身份已能自動
# 偵測（IS_MOBILE），不需要教練多記一組指令，直接用同一個「開工」依偵測結果調整
# 注入份量——手機MiniMax的context window會隨session動態縮水(200K→163K→84K，見
# feedback_minimax_dynamic_context_cap_2026-09-17)，灌全套試金石全文+7天knowledges
# 清單+6000字memory對它負擔過重，改成精簡版：只給最關鍵的待辦+心跳狀態。

MAX_INJECT_CHARS=60000
INJECT_CONTENT=$(
  echo "# 🔴 軍師接力棒 v3（心法＋最新一棒；心法已在全域 CLAUDE.md 常駐，本場 session 僅一次）"
  echo ""
  # 2026-09-27教練抓到（FB申訴漏接）：上一棒「📋 下一場開工先做」寫了教練交辦，但①第1步
  # 以為workspace/CLAUDE.md會載入接力棒而不貼，實際對話框開在~/.openclaw時根本不會載入；
  # ②第6步只叫回報「🙋要教練決定」區，交辦事項不在那區。改成：最新一棒的交辦一律置頂注入，
  # 第6步第一件就報它。
  # 2026-10-02三補：各機寫法不一（「### 📋 下一場先做」「## 🎯 教練交辦…」），原本只認一種標題、
  # 又只抓檔案裡第一個，結果注入的是前一晚的舊交辦、最新的反而埋在下面。改成每種標題都認，挑時間最新的一段。
  NEXT_TASK=$(python3 - "$HANDOFF" <<'PY'
import re, sys
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
cands, ts = [], ""
for i, l in enumerate(lines):
    if l.startswith("## "):
        m = re.search(r"(20\d\d-\d\d-\d\d)\s*(\d\d:\d\d)", l)
        ts = f"{m.group(1)} {m.group(2)}" if m else ""
        if l.startswith("## 🎯"):
            end = next((j for j in range(i + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
            cands.append((ts, -i, lines[i:end]))
    elif re.match(r"^### 📋 下一場(開工)?(先做|第一件)", l):
        end = next((j for j in range(i + 1, len(lines)) if re.match(r"^(##|---)", lines[j])), len(lines))
        cands.append((ts, -i, lines[i + 1:end]))
if cands:
    print("\n".join(l for l in max(cands)[2] if l.strip()))
PY
)
  if [ -n "$NEXT_TASK" ]; then
    echo "## 🎯 教練上一場交辦：這一場第一件要做的事（開工回報第一行就要講，講完直接開始做）"
    echo ""
    printf '%s\n' "$NEXT_TASK"
    echo ""
  fi
  # 2026-09-26教練抓到：Sonnet寫給Opus的信(knowledges/LETTER_*)只在第4步清單裡佔一行，
  # 而本注入常超過10KB，Claude Code只給模型看前2KB預覽、其餘存成檔案，第2~6步實際上看不到，
  # 軍師開工沒讀信、教練要自己點名才看到。信件一律放最前面(預覽範圍內)並要求當場讀完。
  # 2026-09-26二度補：赫米斯/聯想寫給Mac的信放在cross-agent/inbox/mac/，原本只有派工程式讀，
  # 沒標DISPATCH的一般信件只會發Telegram叫教練「找人看一下」，從沒進到這份注入，
  # 教練得自己轉告軍師（搬運工）。現在信箱裡還沒歸檔的信一律列在這裡。
  LETTERS=$( { find "$WORKSPACE/knowledges" -maxdepth 1 -name 'LETTER_*.md' -mtime -3; \
               find "$WORKSPACE/cross-agent/inbox/mac" -maxdepth 1 -name '*.md'; } 2>/dev/null | sort)
  if [ -n "$LETTERS" ]; then
    echo "## 📬 有寫給軍師的信（開工必須先用 Read 讀完全文，回報時一行交代讀後結論）"
    echo ""
    printf '%s\n' "$LETTERS" | while read -r L; do echo "- \`$L\`"; done
    echo ""
  fi
  echo "> ⚠️ 本注入若顯示「Output too large … Preview」，代表第2~6步只露出開頭，**必須用 Read 讀完那個完整檔案**才算做完開工六步。"
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
  echo "- **身份等級**：${IDENTITY_LINE}"
  echo "- **commit 前綴**：\`[Mac]\`（區分 Windows 軍師的 \`[Win]\`）"
  echo "- **稱呼教練**：**大樹教練**"
  echo ""
  echo "🔴 **絕對禁區**：cwd 雖然指向 \`~/.openclaw/\`，但**所有心法/接力棒/試金石/memory 都在 \`workspace/\` 子目錄**。動手前先 \`ls\` 驗證，不可憑 cwd 直覺拼路徑。"
  echo ""

  # 2026-09-18教練親口糾正：手機(MiniMax)開新對話框時讀到同一份接力棒，會把
  # 教練本來要留給軍師討論的題目（標💬的項目）搶先當成任務回答掉，教練要的是
  # 「軍師專屬討論」跟「手機可以動手做的任務」要分清楚，手機看到💬不該回應。
  if [[ "$IS_MOBILE" -eq 1 ]]; then
    echo "🔴 **你是特助(MiniMax)，不是軍師**：接力棒待辦表裡任何標記「💬」的項目，是教練要親自跟軍師（Mac桌面版/終端機的Claude）討論的話題，**不是要你回答或執行的任務**。看到💬項目請完全略過——不要主動回應、不要搶答、不要在教練還沒對你提起前自己先提。你的任務範圍只有🔒(卡住等教練裁示，非你能動)/⏳(可執行)/✅(已完成)/⚠️(持續追蹤)這幾類明確任務，消耗token做事是你的強項，軍師專屬討論不是。"
    echo ""
  fi

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
  # 2026-09-27：workspace/CLAUDE.md只有對話框開在workspace底下才會被載入，開在~/.openclaw就看不到，一律完整貼上
  if [[ "$LAST_SYNC" -ge "$HANDOFF_MTIME" && "$HOOK_CWD" == "$WORKSPACE"* ]]; then
    echo "（接力棒全文已透過 workspace/CLAUDE.md 自動鏡像注入，內容與 JUNSHI_HANDOFF_LATEST.md 一致，不重複貼上。若這是這場對話第一則訊息卻沒看到 CLAUDE.md 內容，代表鏡像沒生效，請直接讀 \`JUNSHI_HANDOFF_LATEST.md\` 原檔。）"
  else
    # 2026-10-02 瘦身（教練「心＋最新一棒摘要」）：不再整份 30KB 全貼，只貼最新一棒＋「🙋要教練決定」區；
    # 前一棒、賈維斯進度表、🤫/🔧 區是 AI 自己的工作筆記，需要時 Read 原檔。
    echo "（精簡注入：只貼最新一棒摘要＋🙋區。前一棒／🤫／🔧區／封存索引請讀 \`JUNSHI_HANDOFF_LATEST.md\` 原檔，需要才讀。）"
    echo ""
    python3 - "$HANDOFF" <<'PY'
import sys, re
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
hdr = [i for i, l in enumerate(lines) if l.startswith("## 🔴 給跨對話框軍師讀的總結摘要")]
end = hdr[1] if len(hdr) > 1 else None
if not hdr or end is None:
    # 找不到標記就整份貼上，安全優先
    print("\n".join(lines)); sys.exit(0)
print("\n".join(lines[hdr[0]:end]).rstrip())
ask = [i for i, l in enumerate(lines) if l.startswith("### 🙋")]
if ask:
    j = ask[0] + 1
    while j < len(lines) and not lines[j].startswith("### "):
        j += 1
    print("\n" + "\n".join(lines[ask[0]:j]).rstrip())
PY
  fi

  # ───────── 第 1.5 步：待辦表過期偵測（2026-09-11教練糾正ACER誤報後新增） ─────────
  # 根因：🔒/⏳卡住的待辦，若在別的session被順手解決，沒人回頭改狀態，就會變成
  # 過期事實一路被當成真相講給教練聽（ACER案例：08-26已解決，放到09-11才被戳破）。
  # 不試圖自動判斷是否真的解決（需要語意理解做不到），改成把超過14天沒更新的
  # 🔒/⏳項目明確標出來，逼開工時主動口頭跟教練核對現況，不可直接讀出來當事實。
  STALENESS_SCRIPT="$WORKSPACE/scripts/handoff_staleness_check.py"
  if [[ -f "$STALENESS_SCRIPT" ]]; then
    echo ""
    echo "## ⚠️ 第 1.5 步：待辦表過期覆核（超過14天未更新的🔒/⏳項目：AI自己查證現況，不准拿去問教練；查不出來就移到「🤫等教練自己提起」區）"
    echo ""
    python3 "$STALENESS_SCRIPT" "$HANDOFF" 2>/dev/null || echo "（過期偵測腳本執行失敗，略過）"
  fi

  # 2026-10-02 開工改「心法＋最新一棒」（教練拍板方向）：拿掉第2~5步——實測當天
  # HEARTBEAT 尾50行全是09-23~09-27舊自檢紀錄、memory最新日只剩空標題、Top10與試金石2案例已由反射在對的時刻調出、
  # knowledges清單只是檔名。需要時各檔原地 Read：HEARTBEAT.md／試金石/試金石_案例庫.md／knowledges/／memory/。

  # ───────── 第 5.5 步：最近24小時教練跟其他AI說了什麼（2026-09-30 教練：「你知道其他的人都交接些什麼了嗎？」）─────────
  # 小龍蝦/Hermes常常做完不寫memory也不交接棒，只看交接檔會漏掉當天別的AI出包的事，所以直接讀原始對話記錄。
  echo ""
  echo "---"
  echo ""
  echo "## 🤝 第 5.5 步：最近24小時教練跟其他AI說了什麼（小龍蝦各頻道＋Hermes桌面版，原始對話記錄）"
  echo ""
  python3 "$HOME/.openclaw/workspace/scripts/today_other_agents_digest.py" 2>&1 | head -20
  echo ""
  echo "👉 有看到任務出包/教練不滿的跡象，開工回報第一行就要提，不要等教練自己講。"

  # ───────── AI團隊品質稽核彙整（2026-09-18 教練要求監督MiniMax小老弟品質後新增）─────────
  # stop_rules_master.py 的 13 條規則本來就對任何觸發Stop事件的session(含手機MiniMax
  # Remote Control)自動稽核，但違規記錄只是各自寫進 distill/*violations.log 沒人讀。
  # 這裡安靜地跑一次彙整：沒有新違規完全不輸出，有才印出來，不需教練或軍師手動去查。
  QA_DIGEST=""
  [[ "$SELFTEST" != 1 ]] && QA_DIGEST=$(python3 "$WORKSPACE/scripts/agent_team_qa_digest.py" 2>/dev/null)
  if [[ -n "$QA_DIGEST" ]]; then
    echo ""
    echo "---"
    echo ""
    printf '%s\n' "$QA_DIGEST"
  fi

  # ───────── 第 6 步：上線回應要求 ─────────
  echo ""
  echo "---"
  echo ""
  echo "## ✅ 第 6 步：上線回應要求（2026-09-24根源改版：開工不唸待辦）"
  echo "讀完本段後，回應**不超過5行**，只包含："
  echo "- 「我已讀完接力棒」＋身份核對（模型版本 + 平台）＋雲端同步狀態（${PULL_STATUS}），一行講完"
  echo "- 若最上方有「🎯 教練上一場交辦」：第二行就講這件事，並說「現在開始做」，回報完直接動手，不問「今天從哪件事開始」"
  echo "- 待辦表「🙋要教練決定」區裡**還沒問過**的項目（通常是零件；零件就完全不提待辦）"
  echo "- 詢問教練「今天從哪件事開始？」"
  echo "**禁止**：唸「🤫等教練自己提起」區、唸「🔧AI自己的工作清單」、列舉上一棒戰果、自己發現的系統異常。這些是AI自己的事，自己處理。"
  echo ""
  echo "（問教練之前的三關＝執行細則 N2，全域 CLAUDE.md 每場都已載入，這裡不重貼。）"
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
if [[ -n "$SESSION_ID" && "$SELFTEST" != 1 ]]; then
  touch "$MARKER"
fi

exit 0
