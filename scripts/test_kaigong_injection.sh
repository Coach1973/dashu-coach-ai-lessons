#!/bin/bash
# 開工注入自我測試（2026-09-27 建立）
# 起因：9/24 體檢後開工漏接三次（09-25 手機誤判跳過第4步、09-26 預覽只露2KB沒讀信、
# 09-27 對話框開在~/.openclaw 沒載入接力棒＋第6步只報🙋區），每次都只修眼前那個洞，
# 從沒有人把「開工注入到底長什麼樣」端到端跑一遍檢查。
# 這支用 KAIGONG_SELFTEST=1 模擬兩種開啟位置，檢查教練交辦、信件、接力棒、第6步都真的看得到。
# 由 .git/hooks/pre-commit 在改到開工程式或接力棒時自動執行；不過就擋下存檔。
WS="/Users/bymyway/.openclaw/workspace"
HOOK="${KAIGONG_HOOK:-$WS/scripts/feed_junshi_handoff.sh}"
FAIL=0

for CWD in "/Users/bymyway/.openclaw" "$WS"; do
  OUT=$(printf '{"session_id":"selftest-%s","prompt":"開工","cwd":"%s"}' "$$" "$CWD" | KAIGONG_SELFTEST=1 bash "$HOOK" 2>/dev/null)
  RESULT=$(OUT="$OUT" CWD="$CWD" HANDOFF="$WS/JUNSHI_HANDOFF_LATEST.md" python3 - <<'PY'
import os, re
out, cwd, handoff = os.environ["OUT"], os.environ["CWD"], open(os.environ["HANDOFF"]).read()
head = out[:2000]  # Claude Code 注入過長時只給模型看約 2KB 預覽
errs = []
if not out.strip():
    errs.append("注入內容是空的")
# 最新一棒有「下一場開工先做」→ 必須出現在預覽範圍內
m = re.search(r"^### 📋 下一場開工先做\n(.*?)(?=^###|^---)", handoff, re.S | re.M)
if m and m.group(1).strip() and "🎯 教練上一場交辦" not in head:
    errs.append("教練交辦沒有出現在前2000字（開工會漏接）")
if "📬 有寫給軍師的信" in out and "📬 有寫給軍師的信" not in head:
    errs.append("寫給軍師的信沒有出現在前2000字")
if "第 6 步" not in out:
    errs.append("缺第6步回報要求")
if "內容過長已截斷" in out:
    errs.append("注入被截斷")
# 對話框不在 workspace 底下時，workspace/CLAUDE.md 不會載入，接力棒必須完整貼上
if not cwd.startswith("/Users/bymyway/.openclaw/workspace") and "給跨對話框軍師讀的總結摘要" not in out:
    errs.append("對話框開在workspace外，接力棒卻沒有貼上")
print("OK" if not errs else "；".join(errs))
PY
)
  if [[ "$RESULT" != "OK" ]]; then
    echo "❌ 開工注入自我測試失敗（對話框位置：$CWD）：$RESULT"
    FAIL=1
  fi
done

[[ $FAIL -eq 0 ]] && echo "✅ 開工注入自我測試通過（~/.openclaw 與 workspace 兩種開啟位置）"
exit $FAIL
