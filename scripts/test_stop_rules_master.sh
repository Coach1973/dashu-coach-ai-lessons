#!/bin/bash
# 驗證：stop_rules_master 合併版 vs 原本 10 支腳本，行為是否一致
#
# 做法：造出各種假 transcript（乾淨/搬運工/缺hash/簡體字/輪詢/猜測/UTC時間/HTML未跳Chrome），
#       同一份輸入分別餵給「原本 10 支」跟「合併版」，比對最終是否擋下（exit 2）。
#       HOME 導向暫存目錄，避免測試汙染真實的違規記錄檔。
#
# 🔴 2026-08-27 發現的重大限制（案例：rule07輪詢偵測瞎眼超過一個月才被抓到）：
#   下面 OLD_SCRIPTS 這 10 支「原版」全部呼叫 `lib/stop_ctx.sh`，但這支共用
#   快取層已經在 2026-08-12（跟本測試檔同一天）被刪除（合併進 stop_rules_master.py
#   後，原本的快取檔案被認為多餘而清掉）。結果這 10 支原版腳本從那天起呼叫
#   一定失敗（`|| exit 0`），永遠回報「沒擋下」——也就是說，這份測試從建立當天
#   起，「原版」那一欄的比對基準就已經失效，「不一致」的紅字只代表「合併版有動作、
#   原版打不開」，不是真的行為分歧。這個測試本身也是本次調查揪出的「監控機制看
#   似正常實則失效」案例之一，記錄在試金石。
#   ✅ 因此：run_case()（老比對邏輯）的結果僅供參考，不能當作「合併版是否正確」
#   的唯一依據；真正的正確性判斷請看下面新增、直接斷言合併版 exit code 的
#   run_case_direct()。
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

  # 🔴 2026-08-27：old_blocked 這個基準已知失效（見檔頭說明，10支原版都依賴
  # 已刪除的 lib/stop_ctx.sh，永遠回報 0）。這裡只印出來給人看，不計入
  # PASS/FAIL、不影響本檔的 exit code——真正的正確性判斷交給 run_case_direct()。
  if [[ "$old_blocked" == "$new_blocked" ]]; then
    printf '  ✅ %-28s 原版擋下=%s 合併版擋下=%s（一致）\n' "$name" "$old_blocked" "$new_blocked"
  else
    printf '  ⚠️  %-28s 原版擋下=%s 合併版擋下=%s（原版基準已失效，僅供參考）\n' "$name" "$old_blocked" "$new_blocked"
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

# 直接斷言合併版（stop_rules_master.py）的 exit code，不依賴已失效的舊版比對。
run_case_direct() {
  local name="$1" transcript="$2" expect_blocked="$3"
  local sid="testdirect-$(echo "$name" | tr -cd 'a-zA-Z0-9')"
  local payload
  payload=$(python3 -c "
import json,sys
print(json.dumps({'session_id':sys.argv[1],'transcript_path':sys.argv[2],'stop_hook_active':False}))
" "$sid" "$transcript")
  local rc=0
  printf '%s' "$payload" | HOME="$TESTHOME" python3 "$SCRIPTS/stop_rules_master.py" >/dev/null 2>&1 || rc=$?
  local got=0
  [[ "$rc" -eq 2 ]] && got=1
  if [[ "$got" == "$expect_blocked" ]]; then
    printf '  ✅ %-28s 預期擋下=%s 實際擋下=%s\n' "$name" "$expect_blocked" "$got"
    PASS=$((PASS+1))
  else
    printf '  ❌ %-28s 預期擋下=%s 實際擋下=%s（不符！）\n' "$name" "$expect_blocked" "$got"
    FAIL=$((FAIL+1))
  fi
}

# 🔴 造出「真實對話會有的樣子」：一個回合裡違規話講在前面，後面還接了好幾次
# 工具呼叫（每次工具結果在 transcript 裡都是 type=="user"）。這正是
# 2026-08-27 抓到的真根因：舊邏輯一遇到 type=="user" 就当成「回合邊界」，
# 但工具回音也是 type=="user"，導致往回掃描被最近一次工具呼叫擋住，
# 掃不到更早之前（同一回合）講的違規內容。
mk_multitool() {  # mk_multitool <檔名> <早期違規文字> <工具呼叫次數> <最後文字（無違規）>
  local f="$FIXDIR/$1.jsonl"
  python3 - "$f" "$2" "$3" "$4" <<'PY'
import json, sys
path, early_text, n_tools, final_text = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
lines = []
lines.append({'type':'user','timestamp':'2026-08-27T00:00:00.000Z',
               'message':{'role':'user','content':'幫我看一下這個問題'}})
lines.append({'type':'assistant','timestamp':'2026-08-27T00:00:01.000Z',
              'message':{'content':[{'type':'text','text': early_text}]}})
for i in range(n_tools):
    lines.append({'type':'assistant','timestamp':f'2026-08-27T00:00:{2+i:02d}.000Z',
                  'message':{'content':[{'type':'tool_use','name':'Bash',
                  'input':{'command': f'echo step{i}'}}]}})
    # 工具結果：type=="user"，但 content 只有 tool_result 區塊、沒有 text 區塊
    # ——這才是真實 transcript 的樣子，也是舊邏輯誤判成真人發話的地方。
    lines.append({'type':'user','timestamp':f'2026-08-27T00:00:{2+i:02d}.500Z',
                  'message':{'role':'user','content':[
                      {'type':'tool_result','tool_use_id':f'toolu_{i}','content':f'step{i} ok'}]}})
lines.append({'type':'assistant','timestamp':'2026-08-27T00:00:99.000Z',
              'message':{'content':[{'type':'text','text': final_text}]}})
with open(path, 'w') as f:
    for l in lines:
        f.write(json.dumps(l, ensure_ascii=False) + '\n')
PY
  echo "$f"
}

echo ""
echo "════ 🔴 2026-08-27 迴歸測試：違規話講在多次工具呼叫之前，仍須被抓到 ════"
run_case_direct "回合前段違規+5次工具呼叫後結束" \
  "$(mk_multitool multitool_violation '這次我打算把檢查頻率從每天一次改成每3分鐘檢查一次，這樣比較保險。' 5 '好了，處理完畢，這是結果摘要。')" \
  1
run_case_direct "回合前段乾淨+5次工具呼叫(對照組不應誤判)" \
  "$(mk_multitool multitool_clean '我先看一下目前的狀態，再決定怎麼處理。' 5 '好了，處理完畢，這是結果摘要。')" \
  0

echo "════ 🔴 2026-09-05 迴歸測試：規則D同義改寫繞過修復（掃/查/讀取/巡邏/處理+小時單位） ════"
run_case_direct "同義改寫-每15分鐘掃一次"   "$(mk poll_syn1 '我建議每15分鐘掃一次資料庫確認狀態。')" 1
run_case_direct "同義改寫-每小時查一次"     "$(mk poll_syn2 '這個先每小時查一次進度，比較保險。')" 1
run_case_direct "同義改寫-每5分鐘讀取一次"  "$(mk poll_syn3 '寫個腳本每5分鐘讀取一次狀態檔案。')" 1
run_case_direct "同義改寫-每10分鐘巡邏一次" "$(mk poll_syn4 '排一個每10分鐘巡邏一次系統健康度的排程。')" 1
run_case_direct "同義改寫-每20分鐘處理一次" "$(mk poll_syn5 '設計成每20分鐘處理一次佇列裡的資料。')" 1
run_case_direct "對照組-不應誤判(調查/查看)" "$(mk poll_syn_clean '我先調查一下目前的狀態，再決定怎麼處理，之後每天固定上班八小時。')" 0
run_case_direct "對照組-已改事件驅動的回顧不擋" "$(mk poll_syn_whitelist '之前每5分鐘掃一次的輪詢設計已經拆除，改成事件驅動了。')" 0

echo "════ 🔴 2026-09-14 迴歸測試：規則D誤判第三方既有排程/meta討論為新輪詢提議 ════"
run_case_direct "對照組-描述第三方內建排程不應擋" "$(mk poll_third_party '這是OpenClaw 2.0內建的「Heartbeat (main)」排程，每30分鐘跑一次，看一下它實際在做什麼。')" 0
run_case_direct "對照組-描述已關閉的既有排程不應擋" "$(mk poll_disabled '確認這個系統保護排程heartbeat每30分鐘觸發一次，已經用disable指令關閉。')" 0
run_case_direct "對照組-meta討論誤判本身不應擋" "$(mk poll_meta '描述OpenClaw內建heartbeat每30分鐘跑一次這類診斷第三方既有排程的事實敘述，被regex誤判成軍師在提議新輪詢設計。')" 0

echo "════ 🔴 2026-09-06 迴歸測試：規則L第二層(既有repo新增頁面沒收錄coach888) ════"
mk_gitcommit() {  # mk_gitcommit <檔名> <git commit指令>
  local f="$FIXDIR/$1.jsonl"
  python3 - "$f" "$2" <<'PY'
import json, sys
path, cmd = sys.argv[1], sys.argv[2]
with open(path, 'w') as f:
    f.write(json.dumps({'type':'user','timestamp':'2026-09-06T00:00:00.000Z',
                        'message':{'role':'user','content':'幫我做一個頁面'}})+'\n')
    f.write(json.dumps({'type':'assistant','timestamp':'2026-09-06T00:00:01.000Z',
                        'message':{'content':[{'type':'tool_use','name':'Bash','input':{'command':cmd}}]}})+'\n')
    f.write(json.dumps({'type':'assistant','timestamp':'2026-09-06T00:00:05.000Z',
                        'message':{'content':[{'type':'text','text':'已推送，commit abc1234 完成。'}]}})+'\n')
PY
  echo "$f"
}
# 規則L/L2都讀 $HOME/github_repos/coach888/index.html，run_case_direct用TESTHOME
# 當假HOME，真實檔案不在那底下，要自己造一份最小fixture才測得到規則本體
# （規則只認「大樹常用」區塊內的內容，所以 fixture 要包成真實頁面的 changyong 區塊結構）
mkdir -p "$TESTHOME/github_repos/coach888"
echo '<div class="grid" data-section="changyong"><a>策展一鍵注入</a></div><button class="btn-add-item" data-section="changyong">' > "$TESTHOME/github_repos/coach888/index.html"

run_case_direct "規則L2-全新頁面未收錄應擋" \
  "$(mk_gitcommit l2_new 'git commit -q -m "新增測試防呆用假頁面：驗證規則L第二層"')" \
  1
run_case_direct "規則L2-已收錄的策展一鍵注入不應擋" \
  "$(mk_gitcommit l2_known 'git commit -q -m "新增策展一鍵注入頁面：貼給任何AI即可觸發策展SOP上架流程"')" \
  0
run_case_direct "規則L2-無關commit不應誤判" \
  "$(mk_gitcommit l2_unrelated 'git commit -q -m "修好一個bug"')" \
  0

echo "════ 🔴 2026-10-06 迴歸測試：規則D不掃「維護偵測器本身」的工具輸入（回測腳本／規則原始碼） ════"
run_case_direct "規則D-維護偵測器的回測腳本不應擋" \
  "$(mk_gitcommit d_selfwork 'cat > backtest.py <<EOF
OLD = [r"每.*分鐘.*檢查"]  # 讀 distill/rule07_polling_violations.log 回測
for s in ["每小時查一次", "我建議每分鐘檢查一次"]: pass
EOF')" \
  0
run_case_direct "規則D-一般工具輸入寫輪詢設計照擋（對照組）" \
  "$(mk_gitcommit d_toolinput_real 'echo "我建議設一個每5分鐘檢查一次的機制" > plan.md')" \
  1

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
