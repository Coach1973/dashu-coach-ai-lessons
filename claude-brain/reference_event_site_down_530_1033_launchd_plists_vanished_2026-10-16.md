---
name: reference-event-site-down-530-1033-launchd-plists-vanished-2026-10-16
description: event.bymyway.com 全站 530/1033 時：Flask(com.coach.event-webapp)與專屬通道(com.coach.event-tunnel)兩個 launchd plist 都從 ~/Library/LaunchAgents 消失，重建法與驗證
metadata: 
  node_type: memory
  type: reference
  originSessionId: 33476b01-4701-5a67-b4e9-a75027299d11
  modified: 2026-10-16T03:56:38.442Z
---

event.bymyway.com（含 /curated/*、shops.bymyway.com）整站打不開（HTTP 530、body「error code: 1033」）＝本機沒服務，不是單一頁面壞。

**10/16 實況**：`com.coach.event-webapp.plist`、`com.coach.event-tunnel.plist` 兩檔都不在 ~/Library/LaunchAgents（原因不明，通道 10/16 08:44 收到 SIGTERM 結束）。root 那條 cloudflared(pid 784) 是別的 hostname，不管 event。

**修法（已做，11:56）**：
- webapp：`event-signup/venv/bin/python event-signup/app.py`，WorkingDirectory=event-signup，KeepAlive，log→event-signup/webapp.log
- tunnel：`/opt/homebrew/bin/cloudflared tunnel --config ~/.cloudflared/event-config.yml run`（tunnel 739a34e4…，ingress event/shops→localhost:5060），log→~/.cloudflared/event-tunnel*.log
- `launchctl bootstrap gui/$(id -u) <plist>`；驗證：curl 127.0.0.1:5060→302、https://event.bymyway.com/curated/lidie/→200

**Why:** 教練 10/16 回報 lidie 連結無效。**How to apply:** event 站 530/1033 先看這兩個 launchd 服務是否載入（`launchctl list | grep coach.event`），沒有就照上面重建；5060 是瀏覽器不安全埠，只用 curl 驗。
