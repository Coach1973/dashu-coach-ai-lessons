#!/bin/bash
# ============================================================
# 💸🔒 LK888 收費鎖（終端機端，PreToolUse Bash hook）
#
# 起因：試金石案例85（2026-09-26）——小龍蝦把一句「直接跑下一張」重跑21次，
#       28張需求出成96張，LK888額度燒光。9/19 也有兩個AI重複跑、雙倍扣點。
#
# 花錢的出圖一律要經過 scripts/lk888_guard.py（重複要求免費回傳、重畫限速、
# 一小時煞車）。這支擋的是「繞過閘門」：指令或它要執行的腳本直接打 api.lk888.ai，
# 卻沒有使用 lk888_guard。小龍蝦端同一套規則在 ~/.openclaw/extensions/safety-locks/。
# ============================================================

INPUT=$(cat)
export HOOK_INPUT="$INPUT"

python3 - <<'PYEOF'
import json, os, re, sys

try:
    data = json.loads(os.environ.get("HOOK_INPUT", "{}"))
except Exception:
    sys.exit(0)
if data.get("tool_name") != "Bash":
    sys.exit(0)
cmd = (data.get("tool_input") or {}).get("command", "") or ""
if not cmd:
    sys.exit(0)

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
HOST = re.compile(r"api\.lk888\.ai", re.I)
GUARD = re.compile(r"\blk888_guard\b")
SCRIPT = re.compile(r"""(?:^|[\s;&|'"(=])((?:~/|/|\.{1,2}/)?[^\s;&|'"()<>]+\.(?:py|mjs|cjs|js|sh))(?=$|[\s;&|'")])""")

NET_CLIENT = re.compile(r"\b(curl|wget|https?ie|http)\b[^|;&\n]*api\.lk888\.ai", re.I)
INLINE_CODE = re.compile(r"\b(python3?|node|ruby|perl)\b\s+(-[ce]\b|-\s*<<|<<)")

def bypass():
    if HOST.search(cmd) and not GUARD.search(cmd) and (NET_CLIENT.search(cmd) or INLINE_CODE.search(cmd)):
        return "指令本身直接呼叫 api.lk888.ai"
    m = re.search(r"""\bcd\s+("([^"]+)"|'([^']+)'|(\S+))\s*(&&|;)""", cmd)
    base = (m.group(2) or m.group(3) or m.group(4)) if m else (data.get("cwd") or WORKSPACE)
    for s in SCRIPT.finditer(cmd):
        p = os.path.expanduser(s.group(1))
        for c in ([p] if os.path.isabs(p) else [os.path.join(base, p), os.path.join(WORKSPACE, p)]):
            if os.path.isfile(c):
                try:
                    if os.path.getsize(c) <= 5 * 1024 * 1024:
                        src = open(c, encoding="utf-8", errors="replace").read()
                        if HOST.search(src) and not GUARD.search(src):
                            return f"腳本 {os.path.basename(c)} 直接呼叫 api.lk888.ai"
                except OSError:
                    pass
                break
    return None

why = bypass()
if not why:
    sys.exit(0)
print("", file=sys.stderr)
print(f"💸🔒 LK888收費鎖（案例85：9/26一句話被重跑21次，28張出成96張）：{why}，沒有經過收費閘門。", file=sys.stderr)
print("請改用 scripts/generate_comic_panel.py（漫畫/鎖臉）或 scripts/generate_industry_chain.py（產業鏈）；", file=sys.stderr)
print("自己寫的腳本要把打 LK888 的 urllib.request.urlopen 換成 lk888_guard.urlopen（import lk888_guard）。", file=sys.stderr)
print("測試請先把網路封死再跑，絕不可對真的 LK888 測（案例85：測試環境沒封好，燒掉1張）。", file=sys.stderr)
sys.exit(2)
PYEOF
