#!/bin/bash
# rule05_hash_check.sh 的回歸測試套件
# 用途：每次修改 rule05_hash_check.sh 前後必跑
# 執行：bash ~/.openclaw/workspace/scripts/test_rule05_hash.sh
# 軍師建立 2026-06-07（沿用 #12 TDD 紀律）
set -uo pipefail

HOOK="/Users/bymyway/.openclaw/workspace/scripts/rule05_hash_check.sh"
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

echo "=== rule05_hash_check 回歸測試 ==="
echo ""

# ── 真實違規案例（必須全部 exit 2）──

# v1: 說「完成了」但沒附 hash
run_test "v1 說完成沒附 hash（exit 2）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"修好了，HEARTBEAT.md 三處 Gemini 都改成 M3 了。"}]}}' \
  2

# v2: 說「已修好」沒附 hash
run_test "v2 說已修好沒附 hash（exit 2）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"已修好，現在檔案內容是 M3 版本。"}]}}' \
  2

# v3: 說「已推送」沒附 hash
run_test "v3 說已推送沒附 hash（exit 2）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"已推上 GitHub，請查收。"}]}}' \
  2

# v4: 說「完成」沒附 hash
run_test "v4 說完成沒附 hash（exit 2）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"任務完成！所有 cron 都修好了。"}]}}' \
  2

# v5: 說「已部署」沒附 hash
run_test "v5 說已部署沒附 hash（exit 2）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"已部署到 Netlify，網站更新了。"}]}}' \
  2

# ── 合規案例（必須全部 exit 0）──

# p1: 說完成 + 附 7+ 碼 hex hash
run_test "p1 完成 + 7 碼 hash（exit 0）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"修好了，commit 3b9ab393 已推上 GitHub。"}]}}' \
  0

# p2: 完整 40 碼 hash（標準）
run_test "p2 完整 40 碼 hash（exit 0）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"已部署，commit a6e598b5901fa8e965a1b770824939543effd30e 推上去了。"}]}}' \
  0

# p3: 純說明沒說完成詞
run_test "p3 純說明無完成詞（exit 0）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"HEARTBEAT.md 目前有 25 行，內容包含模型聲明、對話守則、relay poll 紀錄。"}]}}' \
  0

# p4: 教練問問題的回答
run_test "p4 解釋概念無完成詞（exit 0）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"守則#05 講的是凡走過必留痕跡，需要 commit hash 才能證明完成。"}]}}' \
  0

# p5: 引用守則原文（白名單：含「守則」字眼）
run_test "p5 引用守則原文討論（exit 0）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"守則#05 原文：說了做不到，就會影響信任感的建立。完成了等用語都該附 hash。"}]}}' \
  0

# p6: 開玩笑語氣含完成詞但不是真完成聲明
run_test "p6 條件式語氣（exit 0）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"如果您要的話，我會幫您完成這個任務。"}]}}' \
  0

# p7: 「已 commit」+ hash 寫在不同行
run_test "p7 hash 在不同行（exit 0）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"修好了。\n\ncommit: 3b9ab393\nmessage: HEARTBEAT.md fix"}]}}' \
  0

# p8: 修好的東西「不需要」commit（純說明檔案結構）
run_test "p8 純檔案結構說明（exit 0）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"這個目錄有 3 個檔：README.md、main.py、test.py"}]}}' \
  0

# p9: 教練說「不要 commit，先看」
run_test "p9 回應教練先不要 commit（exit 0）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"好，先不要 commit，等您看完再說。"}]}}' \
  0

# p10: 錯誤訊息含「完成」（白名單：含「失敗/錯誤/無法」等字眼）
run_test "p10 失敗/錯誤訊息（exit 0）" \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"抱歉無法完成這個任務，因為路徑不存在。"}]}}' \
  0

# ── 額外防護 ──

# 防迴圈：stop_hook_active=true 時放行
TMPFILE2=$(mktemp)
printf '{"type":"assistant","message":{"content":[{"type":"text","text":"修好了。"}]}}' > "$TMPFILE2"
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
