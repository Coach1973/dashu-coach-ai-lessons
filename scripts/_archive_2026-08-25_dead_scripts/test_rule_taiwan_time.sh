#!/bin/bash
# rule_taiwan_time_check.sh 的回歸測試套件
# 用途：每次修改 rule_taiwan_time_check.sh 前後必跑
# 執行：bash ~/.openclaw/workspace/scripts/test_rule_taiwan_time.sh
# 軍師建立 2026-07-03（案例38觸發）
set -uo pipefail

HOOK="/Users/bymyway/.openclaw/workspace/scripts/rule_taiwan_time_check.sh"
PASS=0
FAIL=0

run_test() {
  local DESC="$1"
  local TRANSCRIPT_CONTENT="$2"
  local EXPECTED_EXIT="$3"

  local TMPFILE
  TMPFILE=$(mktemp)
  printf '%s' "$TRANSCRIPT_CONTENT" > "$TMPFILE"

  local OUTPUT
  OUTPUT=$(printf '{"transcript_path":"%s","session_id":"test","stop_hook_active":false}' "$TMPFILE" | \
    bash "$HOOK" 2>&1)
  local ACTUAL_EXIT=$?
  rm -f "$TMPFILE"

  if [[ "$ACTUAL_EXIT" == "$EXPECTED_EXIT" ]]; then
    printf '✅ PASS: %s\n' "$DESC"
    PASS=$((PASS+1))
  else
    printf '❌ FAIL: %s\n' "$DESC"
    printf '   expected exit=%s, got exit=%s\n' "$EXPECTED_EXIT" "$ACTUAL_EXIT"
    printf '   output: %s\n' "$OUTPUT"
    FAIL=$((FAIL+1))
  fi
}

echo "=== rule_taiwan_time_check 回歸測試 ==="
echo ""

# ── 真實違規案例（必須 exit 2）──

# v1: 案例38血淚重現——這輪讀過jsonl(含Z timestamp)，最終回覆講了HH:MM卻沒講台灣時間
run_test "v1 案例38重現：讀UTC log後報時鐘數字沒講台灣時間（exit 2）" \
  '{"type":"user","message":{"content":[{"type":"text","text":"幫我算時間"}]}}
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Bash","input":{"command":"grep timestamp log.jsonl"}}]}}
{"type":"user","message":{"content":[{"type":"tool_result","content":"2026-07-02T22:36:51.486Z"}]}}
{"type":"assistant","message":{"content":[{"type":"text","text":"您在22:36首次提出問題，到23:31這則，共經過54分54秒。"}]}}' \
  2

# v2: 只用HH:MM但沒有台灣時間標示，且真的處理過UTC
run_test "v2 直接抄UTC小時給教練沒換算（exit 2）" \
  '{"type":"user","message":{"content":[{"type":"text","text":"幾點了"}]}}
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Bash","input":{"command":"cat log"}}]}}
{"type":"user","message":{"content":[{"type":"tool_result","content":"ts: 2026-07-02T23:08:45.079Z"}]}}
{"type":"assistant","message":{"content":[{"type":"text","text":"這則訊息是23:08發的。"}]}}' \
  2

# ── 合規案例（必須 exit 0）──

# p1: 有處理UTC，回覆裡也講時鐘數字，但明確標示「台灣時間」
run_test "p1 有明確標示台灣時間（exit 0）" \
  '{"type":"user","message":{"content":[{"type":"text","text":"幫我算時間"}]}}
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Bash","input":{"command":"grep timestamp log.jsonl"}}]}}
{"type":"user","message":{"content":[{"type":"tool_result","content":"2026-07-02T22:36:51.486Z"}]}}
{"type":"assistant","message":{"content":[{"type":"text","text":"換算成台灣時間，您在06:36首次提出問題，經過54分54秒。"}]}}' \
  0

# p2: 有明確標示+8
run_test "p2 有明確標示+8換算（exit 0）" \
  '{"type":"user","message":{"content":[{"type":"text","text":"現在幾點"}]}}
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Bash","input":{"command":"date -u"}}]}}
{"type":"user","message":{"content":[{"type":"tool_result","content":"2026-07-03T00:15:00Z"}]}}
{"type":"assistant","message":{"content":[{"type":"text","text":"UTC 00:15，+8 換算是台灣時間早上8:15。"}]}}' \
  0

# p3: 這輪根本沒碰過UTC timestamp，純聊天
run_test "p3 沒碰過UTC timestamp（exit 0）" \
  '{"type":"user","message":{"content":[{"type":"text","text":"你好"}]}}
{"type":"assistant","message":{"content":[{"type":"text","text":"教練好，今天要做什麼？"}]}}' \
  0

# p4: 有碰過UTC但回覆裡完全沒提到任何時鐘數字（只是討論別的事）
run_test "p4 碰過UTC但回覆不含時鐘數字（exit 0）" \
  '{"type":"user","message":{"content":[{"type":"text","text":"查一下log"}]}}
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Bash","input":{"command":"cat log"}}]}}
{"type":"user","message":{"content":[{"type":"tool_result","content":"2026-07-02T22:36:51.486Z session started"}]}}
{"type":"assistant","message":{"content":[{"type":"text","text":"session已經開始，記錄了3則對話。"}]}}' \
  0

# p5: 只有中文的「7點多」描述，沒有精確HH:MM，且有講台灣時間
run_test "p5 白話時間描述+已標示台灣時間（exit 0）" \
  '{"type":"user","message":{"content":[{"type":"text","text":"幾點了"}]}}
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Bash","input":{"command":"date -u"}}]}}
{"type":"user","message":{"content":[{"type":"tool_result","content":"2026-07-03T00:15:00Z"}]}}
{"type":"assistant","message":{"content":[{"type":"text","text":"現在台灣時間早上8點多。"}]}}' \
  0

# ── 額外防護 ──

# 防迴圈：stop_hook_active=true 時放行
TMPFILE2=$(mktemp)
cat > "$TMPFILE2" <<'EOF'
{"type":"user","message":{"content":[{"type":"text","text":"查時間"}]}}
{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Bash","input":{"command":"cat log"}}]}}
{"type":"user","message":{"content":[{"type":"tool_result","content":"2026-07-02T22:36:51.486Z"}]}}
{"type":"assistant","message":{"content":[{"type":"text","text":"22:36發的。"}]}}
EOF
OUTPUT2=$(printf '{"transcript_path":"%s","session_id":"test","stop_hook_active":true}' "$TMPFILE2" | \
  bash "$HOOK" 2>&1)
EXIT2=$?
rm -f "$TMPFILE2"
if [[ "$EXIT2" == "0" ]]; then
  printf '✅ PASS: stop_hook_active=true 防迴圈放行\n'
  PASS=$((PASS+1))
else
  printf '❌ FAIL: stop_hook_active=true 防迴圈放行\n'
  FAIL=$((FAIL+1))
fi

# ── 結果統計 ──
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TOTAL=$((PASS+FAIL))
printf '結果：%d/%d 通過\n' "$PASS" "$TOTAL"
if [[ "$FAIL" -gt 0 ]]; then
  printf '❌ 有 %d 個測試失敗——請勿 commit，先修復 hook 再重跑\n' "$FAIL"
  exit 1
else
  printf '✅ 全部通過，hook 可安全 commit\n'
  exit 0
fi
