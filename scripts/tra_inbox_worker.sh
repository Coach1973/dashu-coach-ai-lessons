#!/bin/bash
# tra_inbox_worker.sh — 巴哈轉交的台鐵研究問題，一寫入就叫軍師處理、答案用巴哈推回群組
# 2026-10-26 教練：「接上自動觸發，轉交檔一寫入就自己處理、做完用巴哈推回群組」
# 觸發：launchd WatchPaths（state/tra_research_inbox.md 一有變動就跑，事件觸發、不是輪詢）
# 流程：搬走轉交檔內容 → claude -p 研究（只給讀檔＋上網，不給改檔、不給下指令）→ 用巴哈 bot 發到群組
# 測試：TRA_TEST=1 時答案改用主機器人發給教練私訊（不吵到佩佩老師群組）
set -uo pipefail
export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 PYTHONIOENCODING=utf-8
export USER=bymyway LOGNAME=bymyway HOME=/Users/bymyway   # claude 用 USER 找鑰匙圈裡的登入，沒有就變成「沒登入」、什麼都不輸出

WS=/Users/bymyway/.openclaw/workspace
INBOX=$WS/state/tra_research_inbox.md
DONE_DIR=$WS/state/tra_research_done
LOCK=/tmp/tra_inbox_worker.lock
LOG=/Users/bymyway/Library/Logs/openclaw/tra_inbox_worker.log
GROUP_CHAT=-5115910257
COACH_CHAT=6124913915
CLAUDE_CLI=/Users/bymyway/.local/bin/claude
DAILY_MAX=8

mkdir -p "$DONE_DIR" "$(dirname "$LOG")"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

[ -s "$INBOX" ] || exit 0   # 空的（自己清空也會觸發一次）→ 直接結束

# 同一時間只跑一個；過 30 分鐘還在的鎖視為死鎖
if [ -f "$LOCK" ]; then
  age=$(( $(date +%s) - $(stat -f %m "$LOCK") ))
  if [ "$age" -lt 1800 ]; then log "SKIP: 已有一個在跑（${age}s）"; exit 0; fi
  rm -f "$LOCK"
fi
touch "$LOCK"; trap 'rm -f "$LOCK"' EXIT

# 一天最多處理 DAILY_MAX 次（每次都會用掉教練的 Claude 額度）
COUNT_FILE=$DONE_DIR/count_$(date +%Y%m%d)
n=$(cat "$COUNT_FILE" 2>/dev/null || echo 0)
if [ "$n" -ge "$DAILY_MAX" ]; then log "SKIP: 今天已處理 $n 次，達上限"; exit 0; fi
echo $((n + 1)) > "$COUNT_FILE"

STAMP=$(date +%Y%m%d_%H%M%S)
WORK=$DONE_DIR/$STAMP.md
mv "$INBOX" "$WORK" && : > "$INBOX"
log "收到轉交：$(head -c 200 "$WORK" | tr '\n' ' ')"

send() {  # send <bot帳號> <chat> <文字檔>
  python3 - "$1" "$2" "$3" <<'PY'
import json,sys,urllib.request,urllib.parse
acc,chat,path=sys.argv[1:4]
c=json.load(open('/Users/bymyway/.openclaw/openclaw.json'))
tok=c['channels']['telegram']['accounts'][acc]['botToken']
text=open(path,encoding='utf-8').read().strip()
for i in range(0,len(text),3800):
    d=urllib.parse.urlencode({'chat_id':chat,'text':text[i:i+3800]}).encode()
    urllib.request.urlopen(urllib.request.Request(f'https://api.telegram.org/bot{tok}/sendMessage',d),timeout=30)
PY
}

PROMPT="你是軍師，正在幫佩佩老師處理「台鐵台東 16 個據點標案」的提案研究。她在巴哈群組說的話（巴哈轉交的原文）如下：

$(cat "$WORK")

可以參考的既有資料（先讀，不要重做）：
- 圖文報告網頁原始檔：/Users/bymyway/github_repos/tra-taitung/index.html
- 巴哈整晚蒐集的研究：/Users/bymyway/.openclaw/agents/peipei/media/work/research/ 與 /Users/bymyway/.openclaw/agents/peipei/media/work/_part_B_話題設施與藝文案例.md
- 報告：/Users/bymyway/.openclaw/workspace/reports/

要求：
1. 先看既有資料能不能直接回答；不夠才上網查（WebSearch／WebFetch），每個事實附網址與日期，查不到就寫「查不到」，不編造。
2. 回覆是要直接貼進 Telegram 群組給佩佩老師看的，用繁體中文、白話、條列，總長 1500 字以內，開頭固定寫「佩佩老師，軍師回覆：」。
3. 如果這件事需要出圖、做簡報或大改版，不要自己做，回覆最後一行寫「（這件較大，軍師會另外做完再送，請稍等）」。
4. 只輸出要發給她的文字本身，不要輸出你的思考過程。"

OUT=$WORK.reply.txt
ERR=$WORK.err
perl -e 'alarm 1500; exec @ARGV' "$CLAUDE_CLI" -p "$PROMPT" \
  --add-dir /Users/bymyway/github_repos --add-dir /Users/bymyway/.openclaw/workspace --add-dir /Users/bymyway/.openclaw/agents/peipei/media/work \
  --allowedTools "WebSearch,WebFetch,Read,Glob,Grep" --output-format json < /dev/null > "$OUT.json" 2> "$ERR"
code=$?
python3 -c "
import json,sys
try:
    d=json.load(open(sys.argv[1]))
    open(sys.argv[2],'w',encoding='utf-8').write((d.get('result') or '').strip())
    print('turns=%s stop=%s err=%s' % (d.get('num_turns'),d.get('terminal_reason'),d.get('is_error')))
except Exception as e:
    open(sys.argv[2],'w').write(''); print('解析失敗',e)
" "$OUT.json" "$OUT" >> "$LOG" 2>&1
log "claude 結束 code=$code 輸出 $(wc -c < "$OUT") bytes"

if [ "$code" -ne 0 ] || [ ! -s "$OUT" ]; then
  printf '【軍師轉達】佩佩老師在巴哈群組問的台鐵問題，軍師自動處理失敗（code=%s），原文已存 state/tra_research_done/%s.md，請叫軍師接手。' "$code" "$STAMP" > "$WORK.fail.txt"
  send bot_main $COACH_CHAT "$WORK.fail.txt" || log "通知教練失敗"
  exit 1
fi

if [ "${TRA_TEST:-0}" = "1" ]; then
  send bot_main $COACH_CHAT "$OUT" && log "測試模式：已發給教練私訊"
else
  send bot_peipei $GROUP_CHAT "$OUT" && log "已用巴哈推回群組"
  printf '【軍師轉達】佩佩老師在巴哈群組問的台鐵問題，軍師已自動回覆到群組（開頭：%s）' "$(head -c 60 "$OUT" | tr '\n' ' ')" > "$WORK.note.txt"
  send bot_main $COACH_CHAT "$WORK.note.txt" || true
fi
