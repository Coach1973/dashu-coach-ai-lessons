---
name: reference-event-site-down-530-1033-launchd-plists-vanished-2026-10-16
description: 10/16 台灣時間 08:44 所有 com.coach.* launchd 服務(網站程式+cloudflared通道)同時消失，十幾個 bymyway.com 網站 530；怎麼認、怎麼重建(含 .env 坑)、哪些故意沒拉
metadata: 
  node_type: memory
  type: reference
  originSessionId: 33476b01-4701-5a67-b4e9-a75027299d11
  modified: 2026-10-16T04:18:19.290Z
---

症狀：某 *.bymyway.com 整站 530（body「error code: 1033」）＝本機沒服務。先 `launchctl list | grep coach` 看服務在不在，再 `curl 127.0.0.1:<埠>`。

**10/16 實況**：台灣時間 08:44 所有通道同時收到 SIGTERM，~/Library/LaunchAgents 的 com.coach.*（除 curation-watch）全不見，原因不明（沒查到哪支腳本刪）。教練 11:52 回報 lidie 連結無效才發現。12:15 教練說「接起來」後全重建。

**重建的服務（plist 在 ~/Library/LaunchAgents，label 格式 com.coach.<名>-webapp / -tunnel，通道用 `cloudflared tunnel --config ~/.cloudflared/<名>-config.yml run`）**
- event(5060, event/shops)、bni-chapters(5064 要 env BNI_CHAPTERS_PORT=5064, chapters/trust)、mentor100(5062)、namecard(5050)、peipei-event(5061 env EVENT_PORT=5061)、team(5073, 借 bni-chapters 的 venv python)、team01(5091)、sincere(5090, 目錄 zhencheng-guests)、zhenxin(5092)、zhengui(5094, real-wealth)、jiesheng(5063, rpl-workshop 走 root 通道 pid 784)
- **坑**：event 與 jiesheng 的 app.py 不會自己讀 .env，plist 必須 `bash -c 'set -a; source .env; set +a; exec venv/bin/python app.py'`，否則管理登入、上傳短網址(/u/…)、LINE 通知全失效（我第一版漏了，12:17 補上）。其他 app 自己有載入 .env。
- 故意沒拉：real-diamonds(5093, zhenzuan 網頁程式 9/18 教練說停用)、namecard-amber-watch(7/13 後無活動，plist 內容找不回)、zhencheng 通道(8/30 已改名 sincere)。

**驗證**：11 個網域全部 curl 200。仍壞：joseph-cloth／social-good 的 github.io 版 404＝repo 是 PRIVATE、方案不支援 Pages（event.bymyway.com/curated/ 版正常）；coach1973.github.io/Business.gym 無此 repo。

**Why:** 教練 10/16 回報 lidie 連結無效。**How to apply:** 整站 530/1033 先看 launchd 服務；重建時記得 .env；plist 不在 git 裡，建完要備份一份到 workspace（尚未做）。
