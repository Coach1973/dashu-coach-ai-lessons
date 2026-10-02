#!/bin/bash
# 夥伴分身(kong/peipei/yijing)各自獨立的私有備份庫，每天自動 commit+push 一次。
# 2026-10-02 體檢發現：只有手動備份，kong 9/18~10/02 共 15 天日記積在本機沒上雲。
# 由 daily_team_rollcall.py 每天 08:10 呼叫；輸出一行結果給點名訊息用。
# 有疑似金鑰就整個分身不推，回報🔴。
set -u
AGENTS_DIR="$HOME/.openclaw/agents"
SECRET_RE='sk-[A-Za-z0-9_-]{20,}|[0-9]{8,10}:AA[A-Za-z0-9_-]{30,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}'
out=()
rc=0
for a in kong peipei yijing; do
  d="$AGENTS_DIR/$a"
  [ -d "$d/.git" ] || { out+=("$a:無備份庫"); rc=1; continue; }
  git -C "$d" add -A >/dev/null 2>&1
  if git -C "$d" diff --cached --quiet; then out+=("$a:無異動"); continue; fi
  if git -C "$d" diff --cached -U0 | grep '^+' | grep -qE "$SECRET_RE"; then
    git -C "$d" reset -q
    out+=("$a:疑似金鑰未推"); rc=1; continue
  fi
  n=$(git -C "$d" diff --cached --name-only | wc -l | tr -d ' ')
  git -C "$d" commit -qm "[Mac] 每日自動備份 $(date +%F)（$n 個檔）" \
    && git -C "$d" push -q 2>/dev/null \
    && out+=("$a:+$n") || { out+=("$a:推送失敗"); rc=1; }
done
echo "${out[*]}"
exit $rc
