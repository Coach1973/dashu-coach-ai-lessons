# 退役 LaunchAgents 存檔（2026-07-08 Fable5 稽核修復）

教練親口核准（2026-07-08 凌晨 3:05「當然是要修嘍」）後卸載，plist 原檔存此，隨時可復原。

| 檔案 | 原用途 | 退役原因 |
|------|--------|---------|
| ai.openclaw.distill-incremental.plist | 每2小時跑 distill_incremental.js | 與 openclaw cron「每2小時增量記憶蒸餾」重複（6/5 遷移只關了 crontab 忘了關這份）；openclaw cron 版功能是超集且有監控，保留該版 |
| ai.openclaw.relay-poll.plist | 每60秒輪詢 RELAY_QUEUE.json | relay 傳話系統 2026-07-02 已退役（改用官方 sessions_send），此哨兵空轉輪詢一個 5/25 的過期任務佇列 |

**復原方法**：`cp <plist> ~/Library/LaunchAgents/ && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/<plist>`
**注意**：council-orchestrator 教練指示先不動，不在此存檔範圍。
