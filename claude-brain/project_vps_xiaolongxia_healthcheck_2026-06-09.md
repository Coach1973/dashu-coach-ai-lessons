---
name: vps-xiaolongxia-healthcheck-2026-06-09
description: VPS 小龍蝦每天 08:00 自動健康檢查 + Telegram 回報，2026-06-09 建立
metadata: 
  node_type: memory
  type: project
  originSessionId: b8bf4f29-0327-442a-8af2-a0270925b60a
---

# VPS 小龍蝦每日健康檢查機制

**事實**：2026-06-09 起，VPS 小龍蝦（43.245.60.200）每天 08:00 由 Mac 端 LaunchAgent 自動健康檢查，結果推 Telegram 給教練。

**Why**：2026-06-09 VPS 小龍蝦因 openclaw.json 缺 minimax provider 註冊掛了 9 小時（6/8 16:00 起），所有 cron 與 Telegram 對話全爆 Unknown model 錯誤，但教練不知道。教練要求：

> 「VPS 版的小龍蝦不是隻有我在用，所以如果它哪一天開始掛點而我們都不知道，那對於其他正在體驗的用戶而言，是挺不好的一種體驗。需要建立每天至少要測一次 VPS 那邊是否正常運作 + 測試結果要回報給我。」

**How to apply**：
- 腳本路徑：`~/.openclaw/workspace/scripts/vps_xiaolongxia_healthcheck.sh`
- 排程：LaunchAgent `ai.openclaw.vps-healthcheck.plist`，每天 08:00 跑
- 檢查項目（5 項）：
  1. SSH 連通性
  2. Docker 容器狀態
  3. Gateway 過去 24h 錯誤數（容忍值 50）
  4. Gateway 過去 1h 是否有活動
  5. 模型載入狀態（agent model: minimax/...）
- 結果儲存：
  - log: `~/.openclaw/workspace/logs/vps_healthcheck.log`
  - state: `~/.openclaw/workspace/logs/vps_healthcheck_state.json`
- 推送邏輯：
  - OK：簡短一行「🩺 VPS 小龍蝦 [✅ 健康]」
  - WARN/DOWN：完整 5 項結果
- 推送管道：透過 Mac 本機 OpenClaw gateway port 18789 推 Telegram 6124913915

**故障排除**：
- 若 LaunchAgent 沒跑：`launchctl list | grep openclaw.vps` 看是否載入
- 若推送失敗：腳本內 curl 失敗會記在 log 但不中斷，先看 log 找根因
- 若 SSH 改密碼：路徑大全.md 與本腳本內 `VPS_PASS` 都要更新
