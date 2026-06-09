# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-06-09 11:06
> 對話記錄已完整存入 memory/2026-06-09.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-06-09.md 可能超過 50KB，讀了會造成模型空白回應）

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M3（全面使用，2026-06-09 教練親口確認）
- 名稱對等：Telegram = 小龍蝦 = 電報

## 🛠 2026-06-09 12:24 軍師治本紀錄（給下一棒）
- `auto-fix-session-lock.sh` 兩坑已治本（commit `de2ff04`）
  - 門檻 500KB → 5MB（之前太低，每 2 分鐘誤殺 gateway）
  - `do_clear_sessions` 加 `glob *.trajectory.jsonl`（之前只刪 sessions.json 的 sessionFile 小檔，大檔沒清 → 死循環）
- RustDesk 門檻 600MB → 1024MB（commit `cebb72a`）
- v2.4 圓桌會議實測通過：三隻機都回應、議程順序生效（學長→學妹→學弟）、互相聽得到（學弟引用 H 過往答案）

## 🛠 2026-06-09 12:55 軍師（Opus 4.7 v2.5+守護）紀錄
**六項待辦全做完，2 commits：**
- **#1 bot-relay v2.5**：補三層 fallback（event.agentId → ctx.agentId → sessionKey 解析）解 v2.4 殘 bug「unknown」（commit `63a6017`，dry-run 四案全綠）
- **#2 sent event lag**：根因 = botId=unknown，v2.5 已解；gateway 重啟後 BOT_MESSAGES 應寫真實 main/kong/peipei
- **#3 SOUL/RTO 直連為主**：實質落地——三隻 SOUL 純直連、shared-relay 自 05-26 起無新檔、cron 無 git pull
- **#4 Netlify 部署守護**：scripts/netlify_deploy_guard.sh + settings.json PreToolUse hook（commit `0321abef`，攔 curl deploys / netlify deploy / nfp_xxx；教練親口「推」加 NETLIFY_DEPLOY_CONFIRMED=1 前綴重試放行）
- **#5 Mac H Phase 1 驗收 4/4 全綠**：FB cron 06-09 06:33 準時跑、status=ok、含「【Mac H 試營運】」前綴。Phase 2/3 = 7 天試煉 + 接其他 SOP（長期任務待持續）
- **#6 cron 首跑驗證**：fb-birthday 06-07/06-08 各跑 1 次找到壽星、vps-healthcheck 06-09 08:00 觸發（log 0 bytes 待查）、dreaming deep/rem/light 三層 06-09 03:00 跑通

**⏳ 待下一棒**：
- vps-healthcheck stdout 0 bytes 要查（cron 觸發了但無輸出）
- Mac H Phase 2/3 是 7 天試煉長期任務，需每天觀察 cron + 接其他 SOP（Netlify/案例網站）+ 7 天後 21 條驗收
- Mac H 已知限制 4 條：Hook 對照未實裝、BOT_MESSAGES 收錄未接、多 agent 缺位、試金石本地版分離

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成模型空白回應）

## 學長 relay poll
### 2026-06-09 2026-06-09 12:46 - relay poll OK

