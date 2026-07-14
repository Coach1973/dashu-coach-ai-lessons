# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-07-14 12:08
> 對話記錄已完整存入 memory/2026-07-14.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-07-14.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-07-14 17:55:00
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 🩺 軍師 Hook 自檢 2026-07-14 18:02（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）
- Session: 870bc689-e1dc-4a85-aab1-8e965418cfe9

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-14 18:30
- ✅ 同步成功
- HANDOFF mtime: 1784024769
- 雲端同步：✅ 已推上雲端（commit 5fbca0ccc）

## 🩺 聯想軍師收工自檢 2026-07-14
- 本場：修復HEARTBEAT合併衝突標記、回應Mac截圖鎖稽核信（聯想這台matcher從未接上+python3是Store空殼，兩層問題，已寫screenshot_lock.ps1修復）、coach888/bigtree/jiesheng-leadership三站維運（新增場次、關閉過期場次、修正連結）、意外抓到自己上一棒Netlify部署的PowerShell反斜線路徑bug並修好、教練電腦睡眠問題全程用事件記錄查證診斷（滑鼠喚醒+AC永不休眠設定）、新開佩佩老師個人品牌頁改版專案(peipei-art)
- 接力棒已更新為 v67，CLAUDE.md已手動同步（Mac版sync腳本路徑寫死無法在Windows執行，下次如需自動化建議補一支.ps1版本）
- 🟡 自首：`make_zip.js`這支修bug用的工具還躺在session暫存區沒正式進repo，PowerShell Compress-Archive反斜線bug也還沒寫進試金石，都留給下一棒或自己下次記得補

## 🔄 接力棒→CLAUDE.md 自動同步 2026-07-14 21:25
- ✅ 同步成功
- HANDOFF mtime: 1784035363
- 雲端同步：✅ 已推上雲端（commit 36979bff7）
