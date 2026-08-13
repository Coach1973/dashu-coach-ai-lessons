---
name: reference-xiaolongxia-line-tunnel-cloudflared
description: 「小龍蝦的專線」「LINE 專線」= cloudflared，LINE訊息進小龍蝦的命脈，絕對不能關；詳細資料在路徑大全第十三節
metadata: 
  node_type: memory
  type: reference
  originSessionId: a21977a4-b019-4888-996c-b12b5186897b
  modified: 2026-08-13T17:30:45.099Z
---

教練說「小龍蝦的專線」「小龍蝦 LINE 專用的頻道」「LINE 專線」= **cloudflared**（Cloudflare Tunnel）。

- 用途：LINE 官方伺服器 → Cloudflare → 這台 Mac 的 OpenClaw gateway `localhost:18789/line/webhook`。教練 LINE 用得很頻繁，**此線斷 = LINE 小龍蝦斷線，任何清理/稽核都不得停用**
- 2026-03-15 裝的系統級服務（`/Library/LaunchDaemons/com.cloudflare.cloudflared.plist`，root + KeepAlive），通道設定存在 Cloudflare 雲端不在本機
- 完整技術明細 + 健康檢查指令：`workspace/路徑大全.md` 第十三節
- 血淚背景：2026-07-08 稽核時差點被當「來路不明的對外門」關掉，靠 zsh_history 查到安裝當下就在測 LINE webhook 才破案（[[project-fable5-system-audit-2026-07-08]]，試金石案例 40）

**🔴 2026-08-14 新發現：process 活著 ≠ 連線活著**——`pgrep -l cloudflared` 只證明程式沒當掉，不能證明真的連得上 Cloudflare edge。實際踩到：process 存在、`curl localhost:18789/line/webhook` 也有回應，但 `/Library/Logs/com.cloudflare.cloudflared.err.log` 最後一筆連線紀錄停在 13 小時前，之後完全沒有 `Registered tunnel connection` 這類記錄——等於斷線 13 小時沒人發現，教練的 LINE 訊息全部石沉大海。**真正的健康檢查要多一步**：`tail -20 /Library/Logs/com.cloudflare.cloudflared.err.log`，看最後一筆時間戳是不是「最近」（不是有沒有錯誤字樣，QUIC 連線本來就會頻繁重試屬正常，重點是有沒有持續在動）。修復用 `sudo launchctl kickstart -k system/com.cloudflare.cloudflared`（root 服務，AI 沒有 sudo 密碼，必須請教練本人執行）。

**🔴 2026-08-14 新發現：gateway 不會自動重讀白名單**——`openclaw pairing approve line <code>` 核准後，新使用者的 ID 會寫進 `~/.openclaw/credentials/line-default-allowFrom.json`（不是 `line-pairing.json`，那個檔案設計上一直是空的 `requests: []`，容易查錯地方），但如果 gateway process 是在核准「之前」就啟動的，它不會動態重新讀取這個檔案，新核准的人一樣被當作未授權。核准新使用者後，如果對方持續沒反應，先比對 `ps -p <gateway_pid> -o lstart` 跟核准時間，process 啟動時間早於核准時間就要重啟：`launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`（這個是使用者層級服務，不需要 sudo）。
