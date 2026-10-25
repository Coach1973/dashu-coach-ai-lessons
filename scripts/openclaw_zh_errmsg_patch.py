#!/usr/bin/env python3
"""把小龍蝦「Something went wrong…」英文錯誤訊息改成白話中文（2026-10-25 教練：看不懂英文）。

小龍蝦更新後 dist 檔會被覆蓋、檔名雜湊也會變，更新完重跑一次本腳本再重啟 gateway。
用法: python3 scripts/openclaw_zh_errmsg_patch.py        （改正在跑的 nvm 版）
先備份到 ~/.openclaw/state/backup_openclaw_zh_errmsg_<日期>/；已改過的檔案不會重複改。
"""
import datetime, glob, os, shutil

DIST = os.path.expanduser("~/.nvm/versions/node/v24.21.0/lib/node_modules/openclaw/dist")
LONG = "Something went wrong while processing your request. Please try again, or use /new to start a fresh session."
ZL = "剛剛處理這則訊息時出了狀況，請再傳一次；如果還是不行，請傳 /new 開新對話。"
SHORT = ["Something went wrong while processing your request. Please try again.",
         "Something went wrong while processing your message. Please try again."]
ZS = "⚠️ 剛剛處理這則訊息時出了狀況，請再傳一次。"

backup = os.path.expanduser("~/.openclaw/state/backup_openclaw_zh_errmsg_" + datetime.date.today().strftime("%Y%m%d"))
for path in glob.glob(DIST + "/**/*.mjs", recursive=True):
    s = open(path, encoding="utf-8").read()
    if "Something went wrong while processing" not in s:
        continue
    rel = os.path.relpath(path, DIST)
    os.makedirs(os.path.dirname(os.path.join(backup, rel)), exist_ok=True)
    shutil.copy2(path, os.path.join(backup, rel))
    s = s.replace(LONG, ZL)
    for t in SHORT:
        s = s.replace(t, ZS)
    open(path, "w", encoding="utf-8").write(s)
    print("改了", rel)
