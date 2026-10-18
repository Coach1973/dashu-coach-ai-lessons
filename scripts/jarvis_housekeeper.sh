#!/bin/bash
# jarvis_housekeeper.sh — 賈維斯系統管家
#
# 教練 2026-08-25 親口下的最高等級指令：
#   「隨時隨地每隔一段時間自我檢測，清空沒有用的歷史背景，
#     把沒用的內容全部歸到歷史紀錄中，
#     系統中只保留現階段正在使用、最順暢且最需要的工作流，以及重要、核心思想的內容」
#
# 設計原則（教練同場強調「我很不喜歡這種那麼多次的資源浪費」）：
#   每週跑一次，不是高頻輪詢。一週一次 ≈ 一天 0.14 次，成本趨近於零。
#   歸檔一律用 mv 不用 rm——教練鐵律「珍貴資料只搬不刪」。
#   有發現才通知教練，沒發現就安靜（教練：不影響工作就別吵我）。

set -uo pipefail

WS="/Users/bymyway/.openclaw/workspace"
OC="/Users/bymyway/.openclaw"
NOTIFY="$WS/scripts/notify_coach.sh"
LOG="/Users/bymyway/Library/Logs/openclaw/jarvis_housekeeper.log"
TODAY=$(date '+%Y-%m-%d')
mkdir -p "$(dirname "$LOG")"
say() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }
FINDINGS=""
add() { FINDINGS="${FINDINGS}$1"$'\n'; }

say "===== 賈維斯管家開始 ====="

# ── 1. 歸檔過期的 session 原始檔（保留 30 天，且跳過系統正在引用的）──
ARCHIVED=$(python3 - <<'PY'
import json, os, time, shutil
S='/Users/bymyway/.openclaw/agents/main/sessions'
A=os.path.join('/Users/bymyway/.openclaw/agents/main/sessions_archive', time.strftime('%Y-%m-%d'))
inuse=set()
try:
    d=json.load(open(os.path.join(S,'sessions.json')))
    for v in d.values():
        for f in ('sessionFile','trajectoryFile','path'):
            if v.get(f): inuse.add(os.path.basename(v[f]))
except Exception:
    print('0 0'); raise SystemExit          # 讀不到就不敢動，安全優先
now=time.time(); n=0; sz=0
for f in os.listdir(S):
    if not f.endswith('.jsonl') or f in inuse: continue
    p=os.path.join(S,f)
    try:
        if (now-os.path.getmtime(p))/86400 > 30:
            os.makedirs(A, exist_ok=True)
            sz+=os.path.getsize(p); shutil.move(p, os.path.join(A,f)); n+=1
    except Exception: pass
print(f'{n} {sz//1048576}')
PY
)
SESS_N=$(echo "$ARCHIVED" | awk '{print $1}'); SESS_MB=$(echo "$ARCHIVED" | awk '{print $2}')
say "session 歸檔：$SESS_N 個 / ${SESS_MB}MB"
[ "${SESS_N:-0}" -gt 100 ] && add "📦 歸檔了 $SESS_N 個舊對話原始檔（${SESS_MB}MB），系統跑得更輕"

# ── 2. 記憶檔寫了卻沒進索引（守則#01：記不住就用不出來）──
# 2026-10-18 教練「解決問題，不要讓小龍蝦來提醒我有問題沒解決」：
#   ①主索引＋舊記憶索引都算已登記（舊版只看 MEMORY.md，把放在舊索引的 460 個檔全誤報）
#   ②不再看修改時間（10/16 倉庫還原讓所有檔 mtime 重置）
#   ③發現真漏收就自己補進舊記憶索引（只追加、不動檔案），不通知教練，結果寫進 log
HEALED=$(python3 - <<'PY'
import os, re
d='/Users/bymyway/.openclaw/workspace/claude-brain'
rd=lambda f: open(os.path.join(d,f),encoding='utf-8').read()
try:
    idx=rd('MEMORY.md')+rd('MEMORY_ARCHIVE_INDEX.md')
except Exception:
    print('0'); raise SystemExit
miss=sorted(f for f in os.listdir(d)
     if f.endswith('.md') and f not in('MEMORY.md','MEMORY_ARCHIVE_INDEX.md')
     and not f.startswith('daily_') and f not in idx)
lines=[]
for f in miss:
    t=rd(f)
    m=re.search(r'^description:\s*(.+)$',t,re.M)
    desc=m.group(1).strip().strip(chr(34)) if m else ''
    if not desc:
        m=re.search(r'^#\s*(.+)$',t,re.M); desc=m.group(1).strip() if m else f[:-3]
    lines.append('- [' + desc[:110] + '](' + f + ')')
if lines:
    import time
    with open(os.path.join(d,'MEMORY_ARCHIVE_INDEX.md'),'a',encoding='utf-8') as fh:
        fh.write('\n\n## %s 自動補登（賈維斯管家，%d 條）\n\n' % (time.strftime('%Y-%m-%d'),len(lines))+'\n'.join(lines)+'\n')
print(len(lines))
PY
)
say "記憶索引自動補登：${HEALED:-0} 條"

# ── 3. 防呆機關做好了卻沒裝上（教練 2026-07-12 重話的那個系統性問題）──
AUDIT=$(bash "$WS/scripts/audit_claude_hooks_registered.sh" 2>/dev/null | grep -c '  • ' || true)
AUDIT=$(printf '%s' "${AUDIT:-0}" | tr -dc '0-9'); AUDIT=${AUDIT:-0}
if [ "$AUDIT" -gt 0 ]; then
    say "未註冊 hook：$AUDIT 支"
    add "🔒 有 $AUDIT 支防呆機關寫好了卻沒接上，等於形同虛設"
fi

# ── 4. 空轉盤點：排程指向的腳本是否還存在（E09 cron 驗證鐵律）──
BROKEN=0
while IFS= read -r s; do
    [ -z "$s" ] && continue
    [ -e "$s" ] || { BROKEN=$((BROKEN+1)); say "排程指向不存在的腳本：$s"; }
done < <(crontab -l 2>/dev/null | grep -vE '^#' | grep -oE '/Users/[^ ]+\.(sh|py|js)' | sort -u)
[ "$BROKEN" -gt 0 ] && add "⚙️ 有 $BROKEN 個排程指向已經不存在的程式，會每次都失敗"

# ── 5. 資料有沒有確實上雲端 ──
UNCOMMITTED=$(git -C "$WS" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
LAST=$(git -C "$WS" log -1 --format='%at' 2>/dev/null || echo 0)
HOURS=$(( ( $(date +%s) - LAST ) / 3600 ))
say "未上雲端：$UNCOMMITTED 個檔案，上次備份 $HOURS 小時前"
[ "$HOURS" -gt 24 ] && add "☁️ 已經 $HOURS 小時沒有備份到雲端了"

# ── 6. 磁碟空間 ──
DISK=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
say "磁碟使用率：${DISK}%"
[ "${DISK:-0}" -gt 85 ] && add "💾 硬碟用到 ${DISK}% 了，該清一下"

# ── 通知：有發現才講，沒發現就安靜 ──
if [ -n "$FINDINGS" ]; then
    "$NOTIFY" "🤖 賈維斯管家週報（$TODAY）

$FINDINGS
需要我處理的話，跟我說一聲就好。" 518400 jarvis_weekly
    say "已通知教練"
else
    say "一切正常，不打擾教練"
fi

say "===== 結束 ====="
exit 0
