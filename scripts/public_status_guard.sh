#!/bin/bash
# 公開交接棒上線前的機密掃描：發現帳密、金鑰、主機位址、電話、Email、身分證、統編、檔案路徑就擋下（exit 1）。
# 用法：public_status_guard.sh <檔案>
F="${1:?用法：public_status_guard.sh <檔案>}"
[ -f "$F" ] || { echo "❌ 找不到 $F"; exit 1; }

/usr/bin/python3 - "$F" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
checks = [
    ("金鑰／Token", r"sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_\w{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[abprs]-[A-Za-z0-9-]{10,}|eyJ[A-Za-z0-9_-]{20,}\.|-----BEGIN [A-Z ]*PRIVATE KEY"),
    ("帳密字樣", r"(?i)(password|passwd|密碼|token|api[_ ]?key|secret)\s*[:：=]\s*\S+"),
    ("IP 位址", r"(?<![\d.])\d{1,3}(?:\.\d{1,3}){3}(?![\d.])"),
    ("Email", r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    ("手機號碼", r"(?<!\d)09\d{2}[-\s]?\d{3}[-\s]?\d{3}(?!\d)"),
    ("市話", r"(?<!\d)0\d{1,2}-\d{6,8}(?!\d)"),
    ("身分證字號", r"(?<![A-Za-z])[A-Z][12]\d{8}(?!\d)"),
    ("統編／8碼數字", r"(?<![\d/.:-])(?!20\d{6})\d{8}(?![\d/.:-])"),
    ("銀行帳號", r"(?<!\d)\d{3}-\d{2}-\d{5,7}-\d(?!\d)"),
    ("本機檔案路徑", r"/Users/|~/\.|[A-Z]:\\\\|\.openclaw"),
]
hits = []
for name, rx in checks:
    for m in re.finditer(rx, text):
        line = text.count("\n", 0, m.start()) + 1
        hits.append(f"  第{line}行［{name}］{m.group(0)[:40]}")
if hits:
    print("🚫 公開交接棒擋下：發現不能公開的內容，改掉再發布")
    print("\n".join(hits))
    sys.exit(1)
print("✅ 機密掃描通過")
PY
