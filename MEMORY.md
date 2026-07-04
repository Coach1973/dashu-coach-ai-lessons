- [Browser no full junction](feedback_browser_no_full_junction.md) — 瀏覽器絕不整個 junction，只搬書籤等增量檔案
- [OpenClaw spool stuck fix](project_openclaw_spool_stuck_fix.md) — VPS 小龍蝦訊息卡住：檢查 .processing 檔案並清除即可修復
- [ACER post-restore TODO](project_acer_post_restore_todo.md) — 一鍵還原後開工時必須主動提醒執行還原步驟
- [VPS 連線資訊](reference_vps_connection.md) — 小龍蝦與赫茲米 VPS 的 IP/帳密/指令，任何電腦都能直接連
- [先問再改](feedback_ask_before_reversing_unusual_config.md) — 發現軟體設定跟預期不同，先問是不是教練故意的，別自己當錯誤修正
- [5月還原大測試](project_may_2026_restore_test.md) — C槽退回5月+6套軟體重裝+D槽junction重接的完整SOP

## Promoted From Short-Term Memory (2026-07-04)

<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:273:276 -->
- 📨 對話記錄 12:41（共約 14 條，從第 0 行起）: 👤 教練：幫我看一下VPS出了什麼問題了為什麼我跟他對話沒有反應？ 🦞 小龍蝦：教練，我先去查 VPS 狀況，不是一直在問你。 🦞 小龍蝦：找到了 VPS 健康檢查腳本，原來 VPS IP 是 `43.245.60.200`（113.29.232.178 是 aiprimetech 代理）。先用這個去查 VPS 狀態： 🦞 小龍蝦：VPS 跟容器都還活著，問題在裡面。我繼續挖： [score=0.886 recalls=0 avg=0.620 source=memory/2026-06-23.md:273-276]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:277:280 -->
- 📨 對話記錄 12:41（共約 14 條，從第 0 行起）: 🦞 小龍蝦：找到核心問題了。繼續挖細節： 🦞 小龍蝦：繼續確認教練訊息到底有沒有送進 VPS： 🦞 小龍蝦：注意：過去 12 小時 VPS 根本**沒收到教練任何訊息**（沒有 chatId=612 的 inbound）。再查 Telegram polling 狀態： 🦞 小龍蝦：確認容器內部到底是什麼，並看 VPS 到底有沒有收到教練的訊息： [score=0.886 recalls=0 avg=0.620 source=memory/2026-06-23.md:277-280]

## Promoted From Short-Term Memory (2026-07-05)

<!-- openclaw-memory-promotion:memory:memory/2026-06-24.md:278:278 -->
- 📨 對話記錄 08:42（共約 1 條，從第 0 行起）: 👤 教練：[cron:5d687b38-5627-4087-ae3e-ddd0bb12127e 🦞 每30分鐘任務健康檢查] 你是健康檢查助理。安靜執行以下檢查並自動修復，不需要通知教練（除非發現無法自動修復的嚴重問題）： [score=0.886 recalls=0 avg=0.620 source=memory/2026-06-24.md:278-278]
<!-- openclaw-memory-promotion:memory:memory/2026-06-24.md:282:282 -->
- 第一步：檢查 Cron 任務失敗記錄: 使用 `openclaw cron list` 或 cron tool 檢查所有任務的 consecutiveErrors 與 lastStatus。 [score=0.886 recalls=0 avg=0.620 source=memory/2026-06-24.md:282-282]
