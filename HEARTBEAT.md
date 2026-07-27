# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 2026-07-27 10:37 Context Overflow 自動重啟完成
> 對話記錄已完整存入 memory/2026-07-27.md 並推上 GitHub，零遺漏
> 最近心跳：14:07（本場4h關懷節奏，通道健康）

## 🔴 當前最重要一句話

直接告訴教練：「🦞 系統健康，OCR 工具已驗收完成，今日第一步待你指定」

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M3（全面使用，2026-06-09 教練親口確認）
- 名稱對等：Telegram = 小龍蝦 = 電報
- Cron 全部健康（28 個任務，啟用的全部 lastRunStatus:ok）
- 接力棒已修正：「下一場直接開工任務」段落從 v83 寫的「OCR 通用工具」換成 🔴🔴🔴 BNI大台南小幫手「主動提醒」功能（commit `7a49347f8`）

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成模型空白回應）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-27 14:07
- ✅ 同步成功（本場小龍蝦 commit `7a49347f8` 接力棒換下一場任務）
- HANDOFF mtime: 1785132435
- 雲端同步：✅ 已推上雲端

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-27 14:10
- ✅ 同步成功
- HANDOFF mtime: 1785132414
- 雲端同步：✅ 已推上雲端（commit d05ba6fc2）

## ⚠️ peipei 自動 force-restart 2026-07-27 17:55:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）
