# -*- coding: utf-8 -*-
# 測試 ask_gate.py：正例都取自 2026-10-28～11-04 真實對話；反例是該放行的情況。執行：python3 scripts/test_ask_gate.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ask_gate import find_asks, should_block

BLOCK = [
    "做好了。\n要我現在改 RPL 的時間嗎？",
    "已完成。\n接下來要我繼續調這支程式，還是先停在這裡？",
    "要不要我順手去修那支自動報數的程式？它會一直給偏高的數字。",
    "你要我把這四張傳到佩君老師的群組嗎？還是你先自己看一下？",
    "要不要現在改成中性寫法？",
    "這樣的順序可以嗎？",
    "**下一步：** 你要不要我把按鈕字調到 20px 並推上線？",
]
PASS = [
    ("花錢類不擋", "要我把小龍蝦升級到最新版嗎？"),
    ("對外發言不擋", "要我現在對外發送這則訊息嗎？"),
    ("收尾框總結問法不擋", "對話容量 17%，要現在總結嗎？"),
    ("方向不明只問一句不擋", "您想要什麼結果？"),
    ("語音辨識確認不擋", "您說的是『XXXX』嗎？是不是語音輸入錯誤？要我先查嗎？"),
    ("引號內是引用句型不擋", "舊規則抓的句型是「要不要我」這種，現在已改程式。"),
    ("程式碼區塊不擋", "```\n要不要我現在做嗎？\n```\n已完成。"),
    ("如果…說一聲不擋", "- 如果您希望我直接幫您上架，說一聲就行。"),
    ("陳述句不擋", "我已經做完了，commit 是 abc123。"),
    ("只在開頭出現、不在結尾不看", "要不要我先查？\n" + "\n".join("第%d行" % i for i in range(12)) + "\n完成。"),
]
ok = True
for t in BLOCK:
    b, _ = should_block(t)
    if not b:
        ok = False; print("❌ 應該擋卻沒擋：", t[:40])
for name, t in PASS:
    b, _ = should_block(t)
    if b:
        ok = False; print("❌ 不該擋卻擋了：", name, "|", t[:40])
# 自述理由的標記要放行
tagged = "要不要把最前面那排擴大到 32 位？\n【只有您能決定：您的喜好】"
if should_block(tagged)[0]:
    ok = False; print("❌ 有【只有您能決定】標記卻還是擋")
if not find_asks("要不要把最前面那排擴大到 32 位？"):
    ok = False; print("❌ 沒標記時應該命中")
print("✅ 全部通過（擋 %d 例、放行 %d 例、標記放行 1 例）" % (len(BLOCK), len(PASS)) if ok else "有失敗")
sys.exit(0 if ok else 1)
