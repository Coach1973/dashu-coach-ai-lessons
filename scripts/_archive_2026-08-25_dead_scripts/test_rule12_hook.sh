#!/bin/bash
# rule12_porter_check.sh 的回歸測試套件
# 用途：每次修改 rule12_porter_check.sh 前後必跑，確保 4 次歷史誤觸發不再重現
# 執行：bash ~/.openclaw/workspace/scripts/test_rule12_hook.sh
# 軍師建立 2026-06-07（從 4 次誤觸發血淚蒸餾）
set -uo pipefail

HOOK="/Users/bymyway/.openclaw/workspace/scripts/rule12_porter_check.sh"
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
    "$HOOK" 2>&1)
  local ACTUAL_EXIT=$?
  rm -f "$TMPFILE"

  if [[ "$ACTUAL_EXIT" == "$EXPECTED_EXIT" ]]; then
    printf '✅ PASS: %s\n' "$DESC"
    PASS=$((PASS+1))
  else
    printf '❌ FAIL: %s\n' "$DESC"
    printf '   expected exit=%s, got exit=%s\n' "$EXPECTED_EXIT" "$ACTUAL_EXIT"
    FAIL=$((FAIL+1))
  fi
}

echo "=== rule12_porter_check 回歸測試 ==="
echo ""

# ── 誤觸發歷史案例（必須全部 exit 0）──

# 誤觸發 v1：Hook 介紹列舉了禁止句型清單
run_test "v1 列舉禁止句型清單不觸發" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"禁止句型清單：請你貼、麻煩你複製、麻煩你回傳"}]}}' \
  0

# 誤觸發 v2：引用守則#12 時使用引號包住的禁止句型
run_test "v2 引號內禁止句型不觸發" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"守則#12：永遠不要叫用戶說「請你貼這段」"}]}}' \
  0

# 誤觸發 v3：解釋正確做法時寫了「請貼一下/麻煩複製」
run_test "v3 修正指引裡引號內禁止句型不觸發" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"而不是用「請貼一下/麻煩複製」這種搬運工句型"}]}}' \
  0

# 誤觸發 v4：讀了歷史輪次，舊輪有違規但最新輪正常
run_test "v4 歷史輪有違規但最新輪正常不觸發" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"舊輪：請你貼一下"}]}}
{"type":"assistant","message":{"content":[{"type":"text","text":"最新回覆：commit hash 是 abc1234，已推上 GitHub。"}]}}' \
  0

# 額外防護：stop_hook_active=true 時放行（防無限迴圈）
TMPFILE2=$(mktemp)
printf '{"type":"assistant","message":{"content":[{"type":"text","text":"請你貼上結果"}]}}' > "$TMPFILE2"
OUTPUT2=$(printf '{"transcript_path":"%s","session_id":"test","stop_hook_active":true}' "$TMPFILE2" | \
  "$HOOK" 2>&1)
EXIT2=$?
rm -f "$TMPFILE2"
if [[ "$EXIT2" == "0" ]]; then
  printf '✅ PASS: stop_hook_active=true 防迴圈放行\n'
  PASS=$((PASS+1))
else
  printf '❌ FAIL: stop_hook_active=true 防迴圈放行\n'
  FAIL=$((FAIL+1))
fi

# ── 真實違規案例（必須全部 exit 2）──

run_test "真實違規：請你貼上完整輸出（exit 2）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"我查不到，請你貼上完整輸出"}]}}' \
  2

run_test "真實違規：麻煩你複製這段（exit 2）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"麻煩你複製這段貼給我看"}]}}' \
  2

run_test "真實違規：請把結果貼上來（exit 2）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"請把結果貼上來，我需要看輸出"}]}}' \
  2

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
