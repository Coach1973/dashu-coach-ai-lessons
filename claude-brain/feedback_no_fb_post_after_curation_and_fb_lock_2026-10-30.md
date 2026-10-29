---
name: feedback-no-fb-post-after-curation-and-fb-lock-2026-10-30
description: 教練 10/30 拍板上架作品一律不貼 FB；策展程式已拿掉 FB 步驟、小龍蝦 safety-locks 加 FB 鎖；停小龍蝦跑到一半要用 sessions.abort
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1afd1c66-f132-41c6-a242-04c05b1f7e88
  modified: 2026-10-29T17:43:28.534Z
---

教練 2026-10-30 01:33 拍板：以後上架任何作品，都不要到大台南策展中心 FB 貼文，人工補發也不要。

**Why:** 9/12 FB 自動貼文就暫停了（廣告帳號受限，訪客看不到），但上架通知還一直寫「請軍師人工補發」。小龍蝦把這句當成待辦，10/30 01:00～01:37 連開 Chrome 登 FB 停不下來，教練關了二三十個視窗；這件事教練從沒交給小龍蝦。燒的是 MiniMax（140 次呼叫），不是 Claude。

**How to apply:**
- 不要再提「hsiuli／任何作品 FB 補發」，也不要把它放進待辦。
- 機制：`workspace/scripts/curation_process.py` 已拿掉 FB 步驟（d94e9b259）；`~/.openclaw/extensions/safety-locks/index.js` v1.5 FB 鎖（9487b5385），生日名單工具 `fb_birthday_scraper` 例外，教練明說要動 FB 才 touch `workspace/state/FB_APPROVED`（10 分鐘）。
- 停小龍蝦跑到一半的事：`openclaw gateway call sessions.abort` 再 `sessions.reset`（params `{"key":"agent:main:main"}`），之後查 transcript 零新事件才算停。`chat.abort` 抓不到、abort 單獨用會再續跑、重啟 gateway 也會續跑。
- FB 鎖也看 write/edit 和被執行腳本內容（補漏 9857d1568），只擋真的自動化／開瀏覽器／打 FB API。
- 停用一個功能時，要連「叫人去補做」的通知文字一起拿掉，通知本身就是指令。

相關：[[reference-fb-chrome-profile-session-restore-birthday-popups-2026-10-30]]、[[reference-openclaw-silent-long-run-ack-reaction-2026-10-30]]
