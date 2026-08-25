#!/bin/bash
# e07_settings_inject.sh 的回歸測試套件
# 用途：每次修改 e07_settings_inject.sh 前後必跑
# 執行：bash ~/.openclaw/workspace/scripts/test_e07_settings.sh
# 軍師建立 2026-06-07
set -uo pipefail

HOOK="/Users/bymyway/.openclaw/workspace/scripts/e07_settings_inject.sh"
PASS=0
FAIL=0

run_test() {
  local DESC="$1"
  local PROMPT="$2"
  local SHOULD_HIT="$3"  # "yes" 期望有注入，"no" 期望靜默
  local MUST_CONTAIN="$4"  # 注入內容必含的關鍵字（可空）

  local ACTUAL_HIT="no"
  local OUTPUT
  # 用 python 構造合法 JSON，避免 shell escape 問題
  local PAYLOAD
  PAYLOAD=$(PROMPT="$PROMPT" python3 -c "import json,os; print(json.dumps({'prompt': os.environ['PROMPT'], 'session_id': 'test'}))")
  OUTPUT=$(printf '%s' "$PAYLOAD" | bash "$HOOK" 2>&1)
  local EXIT=$?

  # 靜默：沒輸出 / 輸出只有 1-2 行 metadata
  if [[ -z "$OUTPUT" ]] || [[ $(printf '%s' "$OUTPUT" | wc -l) -le 2 ]]; then
    ACTUAL_HIT="no"
  else
    ACTUAL_HIT="yes"
  fi

  if [[ "$ACTUAL_HIT" == "$SHOULD_HIT" ]]; then
    if [[ -n "$MUST_CONTAIN" ]] && [[ "$SHOULD_HIT" == "yes" ]]; then
      if printf '%s' "$OUTPUT" | grep -qF "$MUST_CONTAIN"; then
        printf '✅ PASS: %s (含 %s)\n' "$DESC" "$MUST_CONTAIN"
        PASS=$((PASS+1))
      else
        printf '❌ FAIL: %s (缺 %s)\n' "$DESC" "$MUST_CONTAIN"
        printf '   output: %s\n' "$OUTPUT"
        FAIL=$((FAIL+1))
      fi
    else
      printf '✅ PASS: %s\n' "$DESC"
      PASS=$((PASS+1))
    fi
  else
    printf '❌ FAIL: %s\n' "$DESC"
    printf '   expected hit=%s, got hit=%s\n' "$SHOULD_HIT" "$ACTUAL_HIT"
    printf '   output (前 500 chars): %s\n' "${OUTPUT:0:500}"
    FAIL=$((FAIL+1))
  fi
}

echo "=== e07_settings_inject 回歸測試 ==="
echo ""

# ── 觸發案例（必須注入）──

# t1: 問「現在用什麼模型」
run_test "t1 問現在用什麼模型" \
  "現在用什麼模型" \
  "yes" \
  "minimax"

# t2: 問「provider」
run_test "t2 問 provider" \
  "切換 provider" \
  "yes" \
  "anthropic"

# t3: 提到 M3
run_test "t3 提到 M3" \
  "幫我換 M3 跑" \
  "yes" \
  "MiniMax-M3"

# t4: 提到 Opus
run_test "t4 提到 Opus" \
  "用 Opus 模式" \
  "yes" \
  "minimax"

# t5: 提到 Sonnet
run_test "t5 提到 Sonnet" \
  "Sonnet 跑得動嗎" \
  "yes" \
  "minimax"

# t6: 提到 Haiku
run_test "t6 提到 Haiku" \
  "Haiku 切回去" \
  "yes" \
  "minimax"

# t7: 提到 Kimi
run_test "t7 提到 Kimi" \
  "Kimi K2.6 還能用嗎" \
  "yes" \
  "minimax"

# t8: 提到模型切換
run_test "t8 提到切換" \
  "幫我切換到別的模型" \
  "yes" \
  "minimax"

# t9: 提到 baseUrl / api
run_test "t9 提到 api" \
  "API key 在哪" \
  "yes" \
  "openclaw.json"

# ── 非觸發案例（必須靜默）──

# s1: 純打招呼
run_test "s1 純打招呼" \
  "你好" \
  "no" \
  ""

# s2: 問無關問題
run_test "s2 問無關問題" \
  "今天天氣如何" \
  "no" \
  ""

# s3: 純工作指令（無模型詞）
run_test "s3 純工作指令" \
  "幫我寫個 Python 爬蟲" \
  "no" \
  ""

# s4: 提到「M3」當作車款名
run_test "s4 提到 M3 當車款" \
  "BMW M3 跟 M4 差在哪" \
  "no" \
  ""

# s5: 提到「provider」當作醫療
run_test "s5 提到 provider 當醫療" \
  "我是 health care provider" \
  "no" \
  ""

# s6: 提到 Opus 當音樂
run_test "s6 提到 opus 當音樂" \
  "Opus 4 跟 FLAC 差在哪" \
  "no" \
  ""

# s7: 空 prompt
run_test "s7 空 prompt" \
  "" \
  "no" \
  ""

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
