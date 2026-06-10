#!/bin/bash
# ============================================================
# 🈶🔒 繁體字門（Stop hook，2026-06-11 軍師建立）
#
# 起因：試金石案例 18——「我講繁體字，你回我簡體字？」
# 原理：AI 最後一條回覆若混入常見簡體字 → 擋下重寫。
# 沿用案例 F 防誤殺三件套：只讀最後一條、剝引號/程式碼、白名單。
# ============================================================
set -uo pipefail

INPUT=$(cat)
STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)
[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

python3 - "$TRANSCRIPT_PATH" <<'PYEOF'
import sys, json, re

try:
    lines = [l for l in open(sys.argv[1]) if l.strip()]
except Exception:
    sys.exit(0)

text = ""
for line in reversed(lines):
    try:
        evt = json.loads(line)
    except Exception:
        continue
    if evt.get("type") == "assistant":
        contents = evt.get("message", {}).get("content", [])
        text = "\n".join(c.get("text", "") for c in contents if c.get("type") == "text")
        break
if not text:
    sys.exit(0)

# 剝掉不該檢查的部分：程式碼區塊、行內代碼、引號內容、網址、檔名
text = re.sub(r"```[\s\S]*?```", " ", text)
text = re.sub(r"`[^`]*`", " ", text)
text = re.sub(r"「[^」]*」", " ", text)
text = re.sub(r"https?://\S+", " ", text)

# 高頻簡體字（取「簡繁不同形」且日常對話常見的字，避免簡繁同形字誤判）
SIMPLIFIED = "们后还过这说对时让见问题语术业东车书长门马鸟龙岁处见贝页风飞云电气当点没钱铁经维红绿丝织线练给绝统继绩网罗罚买卖读卖学觉览观规视设访证评识词译试话诚询谁请谅论"
hits = sorted(set(ch for ch in text if ch in SIMPLIFIED))
if not hits:
    sys.exit(0)

print("", file=sys.stderr)
print("🈶🔒 繁體字門：回覆混入簡體字，已擋下（案例 18：教練明令全繁體）。", file=sys.stderr)
print("偵測到簡體字：%s" % "、".join(hits), file=sys.stderr)
print("請把整段回覆改成繁體中文後重新輸出。", file=sys.stderr)
sys.exit(2)
PYEOF
