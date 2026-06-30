#!/bin/bash
# ACER 端：每 2 小時把今日 memory 蒸餾推到雲端
# 對應備忘：knowledges/2026-06-30_跨機verbatim蒸餾備忘.md（交付物 B）
# 作者：Mac 軍師 Sonnet 4.6（2026-06-30 上午）
# 目標讀者：ACER 軍師（請依本機 workspace 實際路徑調整 WORKSPACE）
set -uo pipefail

# === 環境設定（ACER 軍師請改成自己 workspace 路徑）===
WORKSPACE="${ACER_WORKSPACE:-/d/openclaw/workspace}"   # 預設 ACER D 槽（Git Bash 路徑）
AGENT_TAG="[ACER]"
VERBATIM_DIR="$WORKSPACE/memory/verbatim/acer"

[[ ! -d "$WORKSPACE" ]] && { echo "WORKSPACE_NOT_FOUND: $WORKSPACE"; exit 0; }
mkdir -p "$VERBATIM_DIR"

cd "$WORKSPACE" || exit 1

# === 台灣時間日期（UTC+8）===
TODAY=$(TZ='Asia/Taipei' date '+%Y-%m-%d')
SRC="$WORKSPACE/memory/$TODAY.md"
DST="$VERBATIM_DIR/$TODAY.md"

[[ ! -f "$SRC" ]] && { echo "NO_MEMORY: $SRC"; exit 0; }

# === 抽 🦞 小龍蝦 bullet → 蒸餾檔（沿用 Mac 端規則）===
python3 - "$SRC" "$DST" "$AGENT_TAG" "$TODAY" <<'PYEOF'
import re, sys, datetime
src, dst, tag, today = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
content = open(src, encoding='utf-8').read()
skip = [r'HEARTBEAT_OK', r'replied with.*HEARTBEAT', r'cron job status output',
        r'async exec.*completed', r'heartbeat poll', r'context overflow', r'session restart']
entries = []
for m in re.finditer(r'🦞 小龍蝦：([\s\S]*?)(?=👤 教練：|---|\Z)', content):
    for line in m.group(1).split('\n'):
        t = line.lstrip()
        if not t.startswith('- '): continue
        t = t[2:].strip()
        if len(t) < 30: continue
        if any(re.search(p, t) for p in skip): continue
        entries.append(f"{tag} {t[:300]}")
if not entries:
    print("NO_ENTRIES"); sys.exit(0)
hh = datetime.datetime.now().strftime('%H:%M')
header = (f"# {tag} verbatim · {today}\n\n"
          f"> 自動蒸餾 · 共 {len(entries)} 則 · 更新時間 {hh} (Asia/Taipei)\n>\n"
          f"> 試金石候選 marker：🪨 試金石候選：<一句話總結>\n\n")
open(dst, 'w', encoding='utf-8').write(header + '\n'.join(f"- {e}" for e in entries) + '\n')
print(f"WROTE: {len(entries)} entries")
PYEOF

# === git add + commit + push ===
git add "memory/verbatim/acer/$TODAY.md" >/dev/null 2>&1
if ! git diff --staged --quiet 2>/dev/null; then
    COUNT=$(grep -c '^- ' "$DST" 2>/dev/null || echo "?")
    git commit -m "auto: ACER 對話蒸餾 $TODAY（${COUNT} 則）" >/dev/null 2>&1
    git push origin main >/dev/null 2>&1 && echo "PUSHED: $COUNT entries"
else
    echo "NO_CHANGE"
fi
