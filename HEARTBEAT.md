# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-08-14 17:38
> 對話記錄已完整存入 memory/2026-08-14.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-08-14.md 可能超過 50KB，讀了會造成模型空白回應）

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

## ⚠️ peipei 自動 force-restart 2026-08-14 17:55:01
- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound
- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）

## 🦞 健康檢查紀錄 2026-08-14 20:12（v4.0 規則）
- 22 個 cron 全 `lastRunStatus: ok`
- 今日曾出現 5 次 `FailoverError: overloaded`（蒸餾 9c3fc55d、起床摘要 f487652d、晨報 b73845c9、LINE 001a9b16、場景化升華 dc9bdf5c），皆自動 retry 成功
- v4.0 三關判斷：關卡一（現在仍壞）fail、關卡二（provider 暫時過載）fail、關卡三（影響工作）fail
- → 三關皆 fail，安靜結束，未 announce 教練
- 教練最後訊息 19:57:19（沉默 0.2h，工作中合理）

## 🦞 健康檢查紀錄 2026-08-14 21:12（v4.0 規則）
- 唯一 cron「🦞 每小時任務健康檢查」本輪 CE=0｜lastStatus=ok｜durationMs=121.5s ≪ 600s
- 上一輪 cycle=328 (20:12) 提到今日 5 次 FailoverError 皆已自動 retry 成功 → 環境本就健康
- v4.0 三關判斷：關卡一（本輪健康+連續多輪全綠）fail、關卡二（provider 已自行恢復）fail、關卡三（meta 自打嗝+教練工作中）fail
- → 三關皆 fail，安靜結束，未 announce 教練
- 環境快檢：SOUL×3 齊全（2036/20631/1851 B）、HEARTBEAT.md 33 行（<500）、healthcheck.log 875 行（<1000）
- Repo1=111 持平 / Repo2=23 微動 / 無 .! 鎖定檔
- TG 通道探針本輪 21:12 實測 ✅ `{"ok":true}`（守則#19 鐵律當下實測）
- Alternating 模式 cycle=329（自 cycle=178 起持續穩定交替）
- delivery.mode=none → 安靜結束不推 Telegram
- 教練最後訊息 21:02:44（沉默 0.2h，週五晚間工作中合理）

## 🦞 健康檢查紀錄 2026-08-14 22:00（v4.0 規則）
- 觸發 cron：每4小時主動關懷 ef88279b（last <1m ago, ok）
- 22 個 cron 全 healthy｜無 FailoverError｜無 pending 阻塞
- 環境快檢：SOUL×3 齊全（2036/20631/1851 B，無變動）、HEARTBEAT.md 45 行（<500）、無 .! 鎖定檔
- Repo1=111 持平 / Repo2=25 微動 +2（合理範圍，無暴增）
- TG 通道探針本輪 22:00 實測 ✅ `{"ok":true}`（守則#19 鐵律當下實測）
- 下一個 cron：22:20 📨 晚間提醒寄 50 封信（day 3/20）→ 23:00 🔴 場景化升華+系統健檢 → 23:05 🦞 每日三機總結
- v4.0 三關判斷：關卡一（cron 全綠+環境齊全）fail、關卡二（無 provider 異常）fail、關卡三（教練 22:00 工作中+無新急事+下週日秋瑩姐婚宴提醒已建立）fail
- → 三關皆 fail，安靜結束，未 announce 教練
- delivery.mode=none → 安靜結束不推 Telegram
- 教練最後訊息 21:02:44（沉默 ~1h，週五晚間 22:00 工作中合理，離 23:00 靜音時段還有 1h）
