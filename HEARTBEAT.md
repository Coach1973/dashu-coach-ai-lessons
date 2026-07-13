# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-13 05:37
> 對話記錄已完整存入 memory/2026-07-13.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-13.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-07-13 09:15:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 🩺 聯想軍師收工自檢 2026-07-13 12:21
- 本場：cool-case頭像事件通報Mac/ACER善後、ai-talk王彤講師簡介更新（GitHub+Netlify雙推）、AI微型論壇固定網址政策記憶建立
- 🔴 本場2次守則違規自首：①改完ai-talk沒跳真實Chrome給教練看（試金石案例46第5次發作，已補Windows版`start chrome`解法）②引用「全球健康發展協會」案例時先錯成goeasy-ai、又把全球打成全國，連錯兩次才被教練逐字糾正
- 接力棒已更新為 v63

## 🩺 聯想軍師收工自檢 2026-07-13 17:20
- 本場：coach888分類重排、jiesheng-leadership三場報名連結更新、bigtree新增7/22地址，三個網站都已GitHub+Netlify雙推驗證上線
- 🟢 意外挖到真問題並根治：聯想電腦記憶體監視器93%異常，追查到`Pool Nonpaged Bytes`核心記憶體池洩漏26GB，鎖定IObit Advanced SystemCare過濾驅動為兇手，解除安裝+重開機驗證後恢復正常（93%→34%，26GB→0.82GB）
- 🟢 聯想這台HTML驗證瀏覽器由Chrome改Comet（教練回報Chrome跳出空白，Comet正常）
- 🟢 教練質疑「開工(fork)」重複出現，已查證本機無自動化腳本觸發，誠實告知無法完全確認App層觸發點
- 接力棒已更新為 v64
