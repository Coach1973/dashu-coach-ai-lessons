---
name: Hermes VPS 部署狀態
description: Hermes Agent 部署在 VPS 113.29.232.178，需要網頁 UI 和 Telegram 接入
type: project
originSessionId: f1631209-219a-43bd-8341-4e37f22f70a9
---
Hermes Agent 已部署在 VPS 113.29.232.178（root / C8GwSuyj）。

**Why:** 用戶想在 VPS 上跑 Hermes 作為 AI agent，接通訊平台使用。

**現況：**
- Docker 已安裝（29.5.0）
- hermes container 跑起來，port 8642 對外
- MiniMax API key 已寫入 ~/.hermes/.env
- Dashboard 跑在 container 內 port 9119（尚未對外開放）
- 尚未接任何通訊平台

**待辦：**
1. 重啟 container 補開 port 9119 → 讓用戶能用瀏覽器開網頁 UI
2. 設定 Telegram bot（需要用戶提供 Bot Token 或引導創建）
3. 設定 TELEGRAM_ALLOWED_USERS 或 GATEWAY_ALLOW_ALL_USERS=true

**How to apply:** 下次繼續時從「補開 9119 port」開始。
