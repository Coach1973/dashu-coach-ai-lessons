# HEARTBEAT 熱上下文（每次心跳必讀）

> ✅ 軍師 VPS 記憶搜尋修復任務已完成（12:56 寫入 result）
> Commit: `d816bc8a`（SOP）+ `e0711644`（HANDOFF_UPDATE_v73）
> 待教練裁示：5 個優先動作（P0+D+A+B+C）+ 升級試金石 53?
> VPS repo 待 pull 到 Mac（軍師 Mac 端寫入被擋，需手動）

## 🔴 Context 狀態
- 上次重啟：2026-07-20 11:08（Context Overflow）
- 教練對話仍可能續接，先打招呼再開機

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M3（全面使用，2026-06-09 教練親口確認）
- 名稱對等：Telegram = 小龍蝦 = 電報
- Gateway PID 42626（11:08 重啟後起來，uptime ~2h45m）
- bot_main token 仍有效（10:00 telegram send 成功）
- 教練沉默 79h+（從 7/17 07:04）— 持續

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M3（全面使用，2026-06-09 教練親口確認）
- 名稱對等：Telegram = 小龍蝦 = 電報

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成模型空白回應）

## 🆕 待教練上線第一提醒（已就緒）
1. 🦞 **軍師 VPS 修復任務結果** — 5 個動作待裁示（P0 查根因 / D 部署 recall.py / A 補 77 天索引 / B trial 個人化 / C 開放搜尋 / 升級試金石 53?）
2. 🆕 [10:02 已到期] 聯想 C 槽觀察期屆滿 — 94GB 待刪
3. ACER 觀察期 (7/15) 已過 5 天 — 36.3GB 待刪
4. Telegram channel bot token 失效 117h+
5. Netlify 剩 13 次（7/25 前）
6. 光線尺 ATM NT$10,000 入金 143h+ 待對帳

## ⚠️ peipei 自動 force-restart 2026-07-20 17:55:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）
