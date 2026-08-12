#!/bin/bash
# 驗證：stop_rules_master 合併版 vs 原本 10 支腳本，行為是否一致
#
# 做法：造出各種假 transcript（乾淨/搬運工/缺hash/簡體字/輪詢/猜測/UTC時間/HTML未跳Chrome），
#       同一份輸入分別餵給「原本 10 支」跟「合併版」，比對最終是否擋下（exit 2）。
#       HOME 導向暫存目錄，避免測試汙染真實的違規記錄檔。
set -uo pipefail

SCRIPTS="/Users/bymyway/.openclaw/workspace/scripts"
TESTHOME=$(mktemp -d /tmp/stophook_test_home.XXXXXX)
FIXDIR=$(mktemp -d /tmp/stophook_test_fix.XXXXXX)

OLD_SCRIPTS=(
  rule12_porter_check.sh
  rule05_hash_check.sh
  rule_taiwan_time_check.sh
  rule07_polling_check.sh
  rule03_verify_before_answer_check.sh
  rule08_ask_when_clear_check.sh
  rule_proactive_session_reminder_check.sh
  delivery_check.sh
  rule_traditional_chinese_check.sh
  rule_html_chrome_check.sh
)

PASS=0
FAIL=0

run_case() {
  local name="$1" transcript="$2"
  local sid="testsession-$(echo "$name" | tr -cd 'a-zA-Z0-9')"
  local payload
  payload=$(python3 -c "
import json,sys
print(json.dumps({'session_id':sys.argv[1],'transcript_path':sys.argv[2],'stop_hook_active':False}))
" "$sid" "$transcript")

  # 原本 10 支：任一支 exit 2 就算「擋下」
  local old_blocked=0
  local rc=0
  for s in "${OLD_SCRIPTS[@]}"; do
    rc=0
    printf '%s' "$payload" | HOME="$TESTHOME" bash "$SCRIPTS/$s" >/dev/null 2>&1 || rc=$?
    [[ "$rc" -eq 2 ]] && old_blocked=1
  done

  # 合併版（換一個 session id，避免共用 proactive marker 造成不對等）
  local payload2
  payload2=$(python3 -c "
import json,sys
print(json.dumps({'session_id':sys.argv[1],'transcript_path':sys.argv[2],'stop_hook_active':False}))
" "${sid}-new" "$transcript")
  local new_blocked=0
  rc=0
  printf '%s' "$payload2" | HOME="$TESTHOME" bash "$SCRIPTS/stop_rules_master.sh" >/dev/null 2>&1 || rc=$?
  [[ "$rc" -eq 2 ]] && new_blocked=1

  if [[ "$old_blocked" == "$new_blocked" ]]; then
    printf '  ✅ %-28s 原版擋下=%s 合併版擋下=%s（一致）\n' "$name" "$old_blocked" "$new_blocked"
    PASS=$((PASS+1))
  else
    printf '  ❌ %-28s 原版擋下=%s 合併版擋下=%s（不一致！）\n' "$name" "$old_blocked" "$new_blocked"
    FAIL=$((FAIL+1))
  fi
}

mk() {  # mk <檔名> <assistant文字>
  local f="$FIXDIR/$1.jsonl"
  python3 - "$f" "$2" <<'PY'
import json,sys
path, text = sys.argv[1], sys.argv[2]
with open(path,'w') as f:
    f.write(json.dumps({'type':'user','timestamp':'2026-08-12T02:00:00.000Z',
                        'message':{'role':'user','content':'請幫我看一下'}})+'\n')
    f.write(json.dumps({'type':'assistant','timestamp':'2026-08-12T02:00:05.000Z',
                        'message':{'content':[{'type':'text','text':text}]}})+'\n')
PY
  echo "$f"
}

echo "════ Stop hook 合併版 vs 原版 行為比對 ════"

run_case "乾淨無違規"        "$(mk clean '資料查詢結束，沒有異常狀況。')"
run_case "搬運工句型"        "$(mk porter '請你複製這段結果傳給我')"
run_case "完成聲明缺hash"    "$(mk nohash '全部改好了')"
run_case "簡體字"            "$(mk simpl '这个设定已经处理')"
run_case "輪詢設計"          "$(mk poll '我建議每5分鐘檢查一次狀態')"
run_case "猜測語言(僅提醒)"  "$(mk guess '應該是設定檔的問題')"
run_case "多此一舉徵詢(提醒)" "$(mk ask '要不要我幫您重新整理一次')"
run_case "完成聲明有hash"    "$(mk withhash '已推送，commit 3b9ab393 已上雲端')"

# UTC 時間案例：這一輪內容含原始 Z 格式時間戳，最終回覆講了時鐘數字卻沒說台灣時間
UTCF="$FIXDIR/utc.jsonl"
python3 - "$UTCF" <<'PY'
import json,sys
with open(sys.argv[1],'w') as f:
    f.write(json.dumps({'type':'user','timestamp':'2026-08-12T02:00:00.000Z',
                        'message':{'role':'user','content':'查一下最後時間'}})+'\n')
    f.write(json.dumps({'type':'user','timestamp':'2026-08-12T02:00:03.000Z',
                        'message':{'role':'user','content':[{'type':'tool_result',
                        'content':'last seen 2026-08-12T03:15:00.000Z'}]}})+'\n')
    f.write(json.dumps({'type':'assistant','timestamp':'2026-08-12T02:00:05.000Z',
                        'message':{'content':[{'type':'text','text':'最後一次是 03:15 沒錯。'}]}})+'\n')
PY
run_case "UTC沒換算台灣時間" "$UTCF"

# HTML 改動但沒跳 Chrome
HTMLF="$FIXDIR/html.jsonl"
python3 - "$HTMLF" <<'PY'
import json,sys
with open(sys.argv[1],'w') as f:
    f.write(json.dumps({'type':'user','timestamp':'2026-08-12T02:00:00.000Z',
                        'message':{'role':'user','content':'改一下網頁'}})+'\n')
    f.write(json.dumps({'type':'assistant','timestamp':'2026-08-12T02:00:05.000Z',
                        'message':{'content':[{'type':'tool_use','name':'Edit',
                        'input':{'file_path':'/tmp/demo.html','new_string':'<p>hi</p>'}}]}})+'\n')
    f.write(json.dumps({'type':'assistant','timestamp':'2026-08-12T02:00:09.000Z',
                        'message':{'content':[{'type':'text','text':'網頁內容已調整。'}]}})+'\n')
PY
run_case "改HTML未跳Chrome" "$HTMLF"

# HTML 改動且有跳 Chrome
HTMLOKF="$FIXDIR/html_ok.jsonl"
python3 - "$HTMLOKF" <<'PY'
import json,sys
with open(sys.argv[1],'w') as f:
    f.write(json.dumps({'type':'user','timestamp':'2026-08-12T02:00:00.000Z',
                        'message':{'role':'user','content':'改一下網頁'}})+'\n')
    f.write(json.dumps({'type':'assistant','timestamp':'2026-08-12T02:00:05.000Z',
                        'message':{'content':[{'type':'tool_use','name':'Edit',
                        'input':{'file_path':'/tmp/demo.html','new_string':'<p>hi</p>'}}]}})+'\n')
    f.write(json.dumps({'type':'assistant','timestamp':'2026-08-12T02:00:07.000Z',
                        'message':{'content':[{'type':'tool_use','name':'Bash',
                        'input':{'command':'open -a "Google Chrome" /tmp/demo.html'}}]}})+'\n')
    f.write(json.dumps({'type':'assistant','timestamp':'2026-08-12T02:00:09.000Z',
                        'message':{'content':[{'type':'text','text':'網頁內容已調整。'}]}})+'\n')
PY
run_case "改HTML有跳Chrome"  "$HTMLOKF"

echo "════════════════════════════════════════"
printf '通過 %s 項，不一致 %s 項\n' "$PASS" "$FAIL"
rm -rf "$TESTHOME" "$FIXDIR"
[[ "$FAIL" -eq 0 ]] || exit 1
