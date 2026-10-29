#!/bin/bash
# jarvis_scorecard_trigger.sh — 賈維斯成績單變差時，自動在背景跑一次 jarvis-self-optimize（2026-10-30 教練拍板）
#
# 由 scripts/jarvis_scorecard.py --trigger 啟動（每週一 08:10 點名時，同一週最多一次）。
# 用法：jarvis_scorecard_trigger.sh "<變差的項目>"
#       JARVIS_TEST=1 jarvis_scorecard_trigger.sh "<原因>"   # 測整條路：換成一句便宜的題目，結果只印不送
#
# 為什麼這樣寫（沿用 tra_inbox_worker.sh 10/26 踩過的坑）：
#   輸出先寫在 workspace 外的暫存夾，做完才搬進 reports/jarvis/；背景 claude 關掉 hook，
#   所以權限改用白名單擋：只能讀寫檔、跑 python3 與 git，不能下 rm 之類的指令（N6）。
#   會改變行為的規則只出建議，不自己改（技能第 4 步的分級）。

WHY="${1:-（沒有帶原因）}"
WS=/Users/bymyway/.openclaw/workspace
CLAUDE_CLI=/Users/bymyway/.local/bin/claude
NOTIFY=$WS/scripts/notify_coach.sh
LOG=$WS/logs/jarvis_scorecard_trigger.log
DATE=$(date +%Y-%m-%d)
mkdir -p "$WS/logs" "$WS/reports/jarvis"
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

TMP=$(mktemp -d /tmp/jarvis_scorecard.XXXXXX)
REPORT=$TMP/report.md

if [ "${JARVIS_TEST:-0}" = "1" ]; then
  PROMPT="這是整條路的測試。請把一行字「測試報告：成績單觸發原因＝$WHY」寫進 $REPORT，然後只輸出一句「📈 賈維斯成績單自動體檢（測試）：整條路通了」。"
  ALARM=300
else
  PROMPT="你是大樹教練的 Mac 軍師，現在沒有人在線上，請自己完整跑一次賈維斯體檢。

觸發原因（賈維斯成績單，每週一自動算）：$WHY
成績單完整數字：執行 python3 $WS/scripts/jarvis_scorecard.py --json

做法：
1. 讀 ~/.claude/skills/jarvis-self-optimize/SKILL.md，照第 0～6 步跑。
2. 先追「變差的那幾項」的源頭：糾正變多→用 python3 $WS/scripts/rules_reminder_count.py --samples <上週一日期> 看教練糾正了什麼；重犯案例→讀那幾案，找出哪一類錯還沒變成程式（N8：同類第二次改源頭）；字數變多→找出這週新增的條文。
3. 只做技能第 4 步「AI 直接改並存檔」那一類；會改變行為的規則、執行細則與 CLAUDE.md 條文增刪，一律寫成建議，不要自己改。守則 21 條原文一字不動。
4. 有改檔就在 $WS 用 git add 指定檔案、git commit（訊息開頭 [Mac] 賈維斯成績單自動體檢：）、git push。
5. 第 7 步改成：完整報告用繁體中文 Markdown 寫進 $REPORT（五問結論、改了什麼附 commit 編號、等教練拍板的建議每項一句話＋好處）。
6. 最後只輸出要直接傳到教練 Telegram 的訊息：開頭固定「📈 賈維斯成績單自動體檢：」，白話、條列、600 字以內，講變差的原因、你改了什麼（附編號）、需要教練拍板的事。不要輸出思考過程。"
  ALARM=3600
fi

log "開始（測試=${JARVIS_TEST:-0}）原因：$WHY"
cd "$WS" || exit 1
perl -e "alarm $ALARM; exec @ARGV" "$CLAUDE_CLI" -p "$PROMPT" --model opus \
  --settings '{"disableAllHooks":true}' \
  --add-dir "$WS" --add-dir /Users/bymyway/.claude --add-dir /Users/bymyway/.openclaw --add-dir "$TMP" \
  --permission-mode acceptEdits \
  --allowedTools "Read,Glob,Grep,Edit,Write,WebSearch,WebFetch,Bash(python3:*),Bash(git status:*),Bash(git diff:*),Bash(git log:*),Bash(git add:*),Bash(git commit:*),Bash(git push:*),Bash(git pull:*),Bash(ls:*),Bash(wc:*),Bash(mkdir:*),Bash(cp:*)" \
  --output-format json < /dev/null > "$TMP/out.json" 2> "$TMP/err"
code=$?
MSG=$(python3 -c "
import json,sys
try:
    d=json.load(open(sys.argv[1])); r=(d.get('result') or '').strip()
    i=r.find('📈 賈維斯成績單自動體檢'); print(r[i:] if i>=0 else r)
    sys.stderr.write('turns=%s err=%s cost=%s\n' % (d.get('num_turns'), d.get('is_error'), d.get('total_cost_usd')))
except Exception as e:
    sys.stderr.write('解析失敗 %s\n' % e)
" "$TMP/out.json" 2>> "$LOG")
log "claude 結束 code=$code 訊息 ${#MSG} 字 報告 $( [ -s "$REPORT" ] && wc -c < "$REPORT" || echo 0) bytes"

DEST=""
if [ -s "$REPORT" ]; then
  DEST=$WS/reports/jarvis/${DATE}$( [ "${JARVIS_TEST:-0}" = "1" ] && echo _test ).md
  cp "$REPORT" "$DEST"
fi

if [ "$code" -ne 0 ] || [ -z "$MSG" ]; then
  MSG="📈 賈維斯成績單：數字變差（$WHY），自動體檢沒跑完（code=$code），請叫軍師接手。紀錄在 logs/jarvis_scorecard_trigger.log"
  cp "$TMP/err" "$WS/logs/jarvis_scorecard_trigger_last_err.txt" 2>/dev/null
elif [ -n "$DEST" ]; then
  MSG="$MSG

完整報告：workspace/reports/jarvis/$(basename "$DEST")"
fi

if [ "${JARVIS_TEST:-0}" = "1" ]; then
  echo "$MSG"
else
  if [ -n "$DEST" ]; then
    git -C "$WS" add "$DEST" && git -C "$WS" commit -q -m "[Mac] 賈維斯成績單自動體檢報告 $DATE" -- "$DEST" && git -C "$WS" push -q 2>> "$LOG"
  fi
  "$NOTIFY" "$MSG" || log "通知教練失敗"
fi
rm -rf "$TMP"
log "完成"
