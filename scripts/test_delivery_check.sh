#!/bin/bash
# 交付自檢門永久測試套件（案例 F 教訓：改 hook 必先跑測試，全過才能 commit）
S=/Users/bymyway/.openclaw/workspace/scripts/delivery_check.sh
PASS=0; FAIL=0
TMP=$(mktemp -d /tmp/test_delivery.XXXXXX)

check() {
  if [ "$2" = "$3" ]; then echo "✅ $1"; PASS=$((PASS+1)); else echo "❌ $1（期望 $2，實際 $3）"; FAIL=$((FAIL+1)); fi
}

# 製造一個假對話檔，最後一條 assistant 訊息 = $1
run() {
  local T="$TMP/t.jsonl"
  python3 -c "
import json, sys
text = sys.argv[1]
print(json.dumps({'type':'user','message':{'role':'user','content':'測試'}}))
print(json.dumps({'type':'assistant','message':{'role':'assistant','content':[{'type':'text','text':text}]}}, ensure_ascii=False))
" "$1" > "$T"
  echo "{\"transcript_path\":\"$T\",\"stop_hook_active\":false}" | bash $S >/dev/null 2>&1
  echo $?
}

check "1 說完成了+零憑證→擋"             2 "$(run '教練，任務完成了，請放心。')"
check "2 完成了+commit hash→放行"        0 "$(run '完成了，commit hash：6618b3f3，已推上雲端。')"
check "3 做好了+測試通過→放行"           0 "$(run '做好了，測試 11 項全數通過 ✅')"
check "4 還沒完成（否定句）→放行"        0 "$(run '這個還沒完成，明天繼續。')"
check "5 未來式承諾→放行"                0 "$(run '我接下來會把它完成，預計十分鐘。')"
check "6 引號內討論「完成了」→放行"      0 "$(run '偵測到 AI 常說「完成了」卻沒憑證，這是壞習慣。')"
check "7 普通回答無宣稱→放行"            0 "$(run '這個檔案在 scripts 資料夾裡。')"
check "8 已上線+驗證輸出→放行"           0 "$(run '已上線，驗證：HTTP 200，iframe 出現 3 次。')"
check "9 修好了+零憑證→擋"               2 "$(run '那個 bug 我修好了。')"

# 10 stop_hook_active=true → 放行（防無限迴圈）
T="$TMP/t.jsonl"
echo "{\"transcript_path\":\"$T\",\"stop_hook_active\":true}" | bash $S >/dev/null 2>&1
check "10 循環保護→放行" 0 $?

rm -rf "$TMP"
echo ""; echo "結果：$PASS 過 / $FAIL 失敗"
[ $FAIL = 0 ] && echo "🎉 全數通過" || exit 1
