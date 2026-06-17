#!/bin/bash
# Pre-commit hook：強制檢查 .ps1 必須 UTF-8 with BOM
# 案例 25 E15 規約的「真實機關」——不是靠 AI 自覺，是 git 強制攔截
# 違反 → commit 失敗，根本進不到 push

set -uo pipefail

# 抓本次 staged 的 .ps1 檔
staged_ps1=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.ps1$' || true)

if [[ -z "$staged_ps1" ]]; then
    exit 0
fi

failed=0
while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    # 檢查 BOM：UTF-8 BOM = 0xEF 0xBB 0xBF
    head_bytes=$(head -c 3 "$f" | xxd -p)
    if [[ "$head_bytes" != "efbbbf" ]]; then
        echo "❌ $f 缺 UTF-8 BOM（案例 25 E15 規約：PS5.1 中文 regex 會失敗）"
        echo "   修法：用 Edit 工具改一次（自動加 BOM）"
        echo "   或：python3 -c \"f=open('$f','rb').read(); open('$f','wb').write(b'\\\\xef\\\\xbb\\\\xbf'+f)\""
        failed=1
    fi
done <<< "$staged_ps1"

if [[ "$failed" -eq 1 ]]; then
    echo ""
    echo "🛑 案例 25 強制機關攔下了——commit 拒絕。"
    echo "   修好 BOM 後再 commit。"
    exit 1
fi

exit 0
