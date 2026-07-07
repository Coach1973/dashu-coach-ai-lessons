---
name: reference-xiaolongxia-line-tunnel-cloudflared
description: 「小龍蝦的專線」「LINE 專線」= cloudflared，LINE訊息進小龍蝦的命脈，絕對不能關；詳細資料在路徑大全第十三節
metadata: 
  node_type: memory
  type: reference
  originSessionId: a21977a4-b019-4888-996c-b12b5186897b
---

教練說「小龍蝦的專線」「小龍蝦 LINE 專用的頻道」「LINE 專線」= **cloudflared**（Cloudflare Tunnel）。

- 用途：LINE 官方伺服器 → Cloudflare → 這台 Mac 的 OpenClaw gateway `localhost:18789/line/webhook`。教練 LINE 用得很頻繁，**此線斷 = LINE 小龍蝦斷線，任何清理/稽核都不得停用**
- 2026-03-15 裝的系統級服務（`/Library/LaunchDaemons/com.cloudflare.cloudflared.plist`，root + KeepAlive），通道設定存在 Cloudflare 雲端不在本機
- 完整技術明細 + 健康檢查指令：`workspace/路徑大全.md` 第十三節
- 血淚背景：2026-07-08 稽核時差點被當「來路不明的對外門」關掉，靠 zsh_history 查到安裝當下就在測 LINE webhook 才破案（[[project-fable5-system-audit-2026-07-08]]，試金石案例 40）
