#!/bin/bash
# system_patrol.sh — 系統巡檢（每小時一次，取代原本各自為政的多支排程）
#
# 教練 2026-08-25 親口重新裁定頻率：
#   「除非有什麼是特別重要的、需要這樣以外，其他都應該是觸發機制」
#   「我其實很不喜歡這種那麼多次的資源浪費」
#
# 設計：原本 5 支排程各自用不同間隔跑（合計 528 次/天），
#       改成一支每小時跑一次、一次做完（24 次/天），降 95%。
#       每支子檢查本身都很輕（讀檔案大小、ps 記憶體、一次 SSH），合併不會變慢。
#
# 為什麼是每小時而不是更久：
#   VPS 掛掉時外部朋友會收不到回覆，教練裁定「一到兩個小時檢查一次就可以」，取下限。
#
# 為什麼不是事件觸發：
#   這三項監測的都是「慢慢惡化」型狀況（記憶體漸漸漲、連線悄悄斷、檔案慢慢變大），
#   沒有明確的事件可以掛。已逐項確認過，不是偷懶用輪詢。

set -uo pipefail
WS="/Users/bymyway/.openclaw/workspace"
LOG="/Users/bymyway/Library/Logs/openclaw/system_patrol.log"
mkdir -p "$(dirname "$LOG")"
say() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

say "───── 巡檢開始 ─────"

# ── 1. 小龍蝦端：對話檔爆滿 / session 卡住 / gateway 與 RustDesk 記憶體洩漏 ──
#    ⚠️ 這監控的是 OpenClaw 小龍蝦（Telegram/LINE），
#    不是教練在 Claude 桌面版右下角看到的那個百分比——兩套系統各自獨立。
if [ -x /Users/bymyway/.openclaw/scripts/auto-fix-session-lock.sh ]; then
    bash /Users/bymyway/.openclaw/scripts/auto-fix-session-lock.sh >/dev/null 2>&1
    say "小龍蝦端檢查完成（對話檔／session鎖／記憶體）"
fi

# ── 2. 佩佩老師的線是否卡住 ──
#    教練認為「同一套系統會一起壞」，但查證顯示這是 channel 層級的卡住
#    （單一 bot 連線停止，gateway 本身正常），所以小龍蝦可能好好的而佩佩那條斷了。
#    2026-06 底密集發作 184 次，07/05 一次，08/24 一次——已大幅收斂但沒絕跡。
#    保留檢查但併進巡檢，成本從一天 288 次降到跟著巡檢跑 24 次。
if [ -x "$WS/scripts/peipei_stuck_force_restart.sh" ]; then
    bash "$WS/scripts/peipei_stuck_force_restart.sh" >/dev/null 2>&1
    say "佩佩老師線況檢查完成"
fi

# ── 3. VPS 小龍蝦（服務 9 位外部朋友）──
#    它自己會先嘗試 docker restart 修復，修不好才通知教練。
if [ -x "$WS/scripts/vps_polling_healthcheck.sh" ]; then
    bash "$WS/scripts/vps_polling_healthcheck.sh" >/dev/null 2>&1
    say "VPS 健康檢查完成"
fi

# ── 4. 【教練 2026-08-25 親口要求】小龍蝦對話快滿了要「事前」提醒 ──
#    教練原話：「我們很早以前就跟小龍蝦提醒過，如果額度要快滿了它要主動提醒我，
#              其實我從來沒有聽到小龍蝦提醒過我。」
#    為什麼舊機制沒響：既有的 context-overflow-guard hook 用「對話輪次」計數（20/30/38 輪），
#    但真正觸發搶救的是「檔案大小超過 5MB」——兩把不同的尺。
#    一輪如果貼了大量內容，檔案可能還沒到 38 輪就先爆，預警根本來不及響。
#    解法：預警改用跟搶救同一把尺（檔案大小），到 70% 就先講，讓教練有時間自己收尾。
LIMIT=5000000          # 跟 auto-fix-session-lock.sh 的 JSONL_SIZE_LIMIT 一致
WARN=$(( LIMIT * 70 / 100 ))
NEWEST=$(ls -t /Users/bymyway/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null | head -1)
if [ -n "$NEWEST" ] && [ -f "$NEWEST" ]; then
    SZ=$(stat -f%z "$NEWEST" 2>/dev/null || echo 0)
    PCT=$(( SZ * 100 / LIMIT ))
    say "小龍蝦對話用量：${PCT}%（$(( SZ / 1048576 ))MB / $(( LIMIT / 1048576 ))MB）"
    if [ "$SZ" -ge "$WARN" ]; then
        # 節流 4 小時：避免同一個快滿的對話每小時都吵一次
        "$WS/scripts/notify_coach.sh" "🦞 小龍蝦的對話快滿了（已用 ${PCT}%）

目前這個對話累積到 $(( SZ / 1048576 ))MB，上限是 $(( LIMIT / 1048576 ))MB。

滿了我會自動存檔重開、不會掉資料，但那當下的對話脈絡會斷。
如果您手上這件事快談完了，收個尾再繼續會比較順。

（不用回覆，讓您心裡有底而已）" 14400 lobster_ctx_warn
        say "已發出對話快滿預警（${PCT}%）"
    fi
fi

say "───── 巡檢結束 ─────"
exit 0
