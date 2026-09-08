---
name: reference-hermes-gateway-hang-watchdog-2026-09-08
description: Hermes(Mac桌面版)手機Telegram沒反應的根因是gateway process內部事件迴圈卡死但不crash，launchd KeepAlive測不到，已建heartbeat staleness watchdog每5分鐘自動偵測重啟
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4a84abf4-a5fc-4064-97eb-aae7b57eeaf6
  modified: 2026-09-08T02:45:44.125Z
---

教練回報「手機版Telegram的Hermes沒反應，已經出現過幾次」。查證`/Users/bymyway/.hermes/logs/gateway.log`：最後一筆活動停在當天04:00:36（Session expiry事件），到教練10:38發現為止已靜默6.5小時，過程中process(pid 43123)全程沒有crash紀錄——`ai.hermes.gateway.plist`的`KeepAlive:true`只在process真的exit時才會重啟，對「還活著但內部event loop卡死」完全沒用，這就是為什麼coach每次遇到都要自己發現、沒有東西會自動救回來。

**關鍵發現**：Hermes自己會把event loop存活訊號寫進`/Users/bymyway/.hermes/state/gateway.heartbeat`（JSON，`updated_at`欄位，正常每~30秒更新一次，跟有沒有訊息無關）——這比看`gateway.log`有沒有新訊息準確得多（沒訊息不代表卡住，但heartbeat該跳沒跳就是真卡住）。

**已修復（commit `be993e716`）**：新增`scripts/hermes_gateway_watchdog.sh` + `~/Library/LaunchAgents/ai.hermes.gateway-watchdog.plist`（`StartInterval:300`，每5分鐘跑一次）：讀heartbeat的`updated_at`，超過300秒沒更新就判定卡住，執行`launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway`強制重啟（已驗證10秒內恢復），並用bot_main token發Telegram通知教練（chat_id 6124913915）「已自動重啟，剛才交辦的事可能要重新確認進度」。已用假timestamp驗證偵測邏輯正確、健康狀態下零誤報。

**How to apply**：往後教練再回報「Hermes沒反應」，先查`hermes_gateway_watchdog.log`有沒有已經自動處理過；若watchdog本身沒觸發（例如launchd job被移除或heartbeat機制本身跟著卡死），才需要人工`launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway`。

Related: [[feedback_hermes_is_mac_desktop_vps_permanently_off]]（教練說「Hermes」預設指Mac桌面版）、[[project_hermes_desktop_agent_verified_2026-08-31]]（Hermes是Nous Research獨立agent框架，跟Claude Code/OpenClaw完全分開）
