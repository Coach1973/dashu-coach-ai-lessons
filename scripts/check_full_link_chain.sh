#!/bin/bash
# check_full_link_chain.sh — 給定一個路徑，先查「這個路徑本身」是不是symlink，
# 再往下查子項目。不能只查子項目就斷言「沒有連結到別處」。
#
# 起因：試金石案例51（2026-07-17，聯想桌面版）——Windows那台只查子資料夾有沒有
# 被junction連結，沒查資料夾本身，結果Roaming\Zoom本身就是連結到E碟，
# 誤判「沒有連結」導致教練依此下令刪除，刪掉正在用的真實資料（1.8GB，
# 5-6場會議記錄消失）。這是查證層級的邏輯漏洞：只查了看得到的一層，
# 就對「有沒有」下絕對結論。
#
# macOS對應Windows junction的東西是symlink（用ls -la看到l開頭+箭頭），
# 這支腳本是Mac版的同款防護，任何「這個資料夾是否連結到別處」的判斷，
# 只要後續動作涉及刪除等不可逆操作，一律先跑這支腳本再下結論。
#
# 用法：./check_full_link_chain.sh <路徑>

set -euo pipefail

TARGET="${1:-}"
if [ -z "$TARGET" ]; then
    echo "用法：$0 <路徑>"
    exit 1
fi

if [ ! -e "$TARGET" ] && [ ! -L "$TARGET" ]; then
    echo "❌ 路徑不存在：$TARGET"
    exit 1
fi

echo "=== 查證：$TARGET ==="
echo ""

# 第一步：查節點本身是不是symlink（最關鍵的一步，案例51漏掉的就是這一步）
if [ -L "$TARGET" ]; then
    REAL_TARGET=$(readlink -f "$TARGET" 2>/dev/null || readlink "$TARGET")
    echo "🔴 SELF 是連結（symlink）"
    echo "   實際指向：$REAL_TARGET"
    echo ""
    echo "⚠️  停下：下面所有內容都是透過這個連結透明重導向的，"
    echo "   不能用「檢查子項目有沒有各自被連結」的方式判斷——子項目不會顯示"
    echo "   「我被連結了」，因為連結點設在上層，內容看起來完全正常。"
    echo "   任何刪除/搬移決定，都要意識到刪的其實是「$REAL_TARGET」這裡的東西。"
    exit 0
fi

echo "✅ SELF 不是連結，是真實資料夾/檔案"
echo ""

if [ -d "$TARGET" ]; then
    echo "=== 往下查子項目 ==="
    FOUND_LINK=false
    while IFS= read -r -d '' item; do
        if [ -L "$item" ]; then
            LINK_TARGET=$(readlink -f "$item" 2>/dev/null || readlink "$item")
            echo "🔗 子項目是連結：$item -> $LINK_TARGET"
            FOUND_LINK=true
        fi
    done < <(find "$TARGET" -maxdepth 3 -type l -print0 2>/dev/null)

    if [ "$FOUND_LINK" = "false" ]; then
        echo "（往下3層沒找到子項目層級的連結）"
    fi
fi

echo ""
echo "=== 結論 ==="
echo "路徑本身：真實資料（非連結）"
echo "子項目（往下3層）：$([ "${FOUND_LINK:-false}" = "true" ] && echo "有連結，見上方列表" || echo "沒有連結")"
