# Fable 5 系統全盤稽核報告（2026-07-08 凌晨）

> 執行者：Mac 終端機軍師 **Fable 5**（教練親口指定的最高等級模型）
> 任務來源：接力棒 v48 + `knowledges/BRIEF_fable5_system_audit_2026-07-08.md`
> 方法：每一項都用可執行指令實際查證，不信文件宣稱；只診斷不動手改（對照 E11）
> 稽核範圍：25 個 hook、11 個 openclaw cron、20 個 LaunchAgents、系統 crontab、openclaw 通知原始碼全文、試金石案例庫、三機 git 設定

---

## 🔴 第一級：真的有問題，建議立刻修（3 件）

### 🔴1. Stop hook「自動同步」在自我餵養——每次對話結束都白推一次雲端

**問題**：`scripts/session_end_auto_push.sh` 的順序是「commit → push → 把推送紀錄寫進 HEARTBEAT.md」。
但 HEARTBEAT.md 本身就在它的同步清單裡——所以每推完一次，HEARTBEAT 立刻又變髒，下一次對話一結束又觸發 commit+push，**永遠停不下來**。

**證據**（親自查證，非推測）：
- 最近 24 小時 43 個 commit 裡有 8 個是「[Mac] session-end 自動同步」
- 7/8 凌晨 02:04 → 02:06 → 02:08 → 02:17 連環四推，後三次的同步內容**只有 HEARTBEAT.md 自己**（也就是只推「上一次推送的紀錄」）

**建議修法**（二擇一，都是小改動）：
- A：推送紀錄改寫到 `/tmp/session_end_push.log`，不要寫進會被同步的 HEARTBEAT.md
- B：寫 HEARTBEAT 紀錄的動作移到 commit **之前**，讓紀錄跟著同一個 commit 走

### 🔴2. 增量記憶蒸餾「雙引擎」——同一支腳本每 2 小時被跑兩次，其中一次還多花 LLM 錢

**問題**：兩套排程在做同一件事，彼此不知情：
| 引擎 | 排程 | 做法 |
|------|------|------|
| LaunchAgent `ai.openclaw.distill-incremental` | 每 7200 秒 | 直接跑 `distill_incremental.js` |
| openclaw cron「每2小時增量記憶蒸餾」 | `0 */2 * * *` | 開一個 **LLM 隔離 session**，再叫 LLM 去跑同一支 `distill_incremental.js` |

**證據**：`/tmp/distill_incremental.log` 今天 02:00 由 LaunchAgent 寫入；openclaw cron 同一小時（stagger 5 分鐘後）也跑了一次，`lastRunStatus: ok, lastDurationMs: 7925`。

**背景**：系統 crontab 裡的同款任務 2026-06-05 已註明「disabled，改用 ai.openclaw.cron-daemon」——但當時**只關了 crontab 那份，LaunchAgent 那份忘了關**，跟案例 37 白名單過期是同一種病：搬家搬一半，舊的沒拆。

**建議**：留 openclaw cron 那份（有 status 監控、失敗計數），卸載 LaunchAgent 那份。openclaw cron 版還能順便更新 CLIENT_PROFILE.md，功能是超集。

### 🔴3. relay 輪詢系統 7/2 已退役，但屍體還在每 60 秒跳動

**問題**：三機「學長/學弟」土法煉鋼 relay 已於 7/2 退役（改用官方 sessions_send，記憶檔 `project_mac_bot_relay_retired_2026-07-02.md` 有案），但：
- `ai.openclaw.relay-poll` LaunchAgent 還在**每 60 秒**跑 `relay_poll.py`
- 它讀的 `RELAY_QUEUE.json` 裡躺的是 **2026-05-25 的過期任務**（deadline 早過了 44 天）
- 每天還往 HEARTBEAT.md 寫一行「relay poll OK」（今天 02:50 那行就是它寫的）
- 同架構的 `ai.openclaw.council-orchestrator`（每 120 秒輪詢 BOT_MESSAGES.md 找 Council Mode 議程）的即時觸發端 bot-relay hook 已關閉，只剩輪詢端空轉

**這正是教練三次糾正的「無意義輪詢」（案例 36）+ 案例 34「過時的鎖要回頭砍」的活教材。**

**建議**：卸載 `ai.openclaw.relay-poll`；council-orchestrator 請教練確認 Council Mode（Telegram 群 -1003877502911）還用不用，不用就一併卸載。

---

## 🟡 第二級：有優化空間，不急但值得排程（6 件）

### 🟡4. 教練每說一句話，要先付 2.5 秒的「hook 稅」
10 個 UserPromptSubmit hook 實測合計 **2519 毫秒**，其中：
- `scan_cross_agent_inbox.sh`：1372ms（每句話都跑，還會在對話路徑上做 git pull 網路呼叫，5 分鐘節流）
- `scan_cross_machine_commits.sh`：898ms（每 session 首句跑一次，同樣做 git pull）
- 其餘 8 個合計約 250ms，健康。

**建議**：兩個掃描 hook 合併成一個；git pull 改成背景執行（`&`）或由 Stop hook 做，不擋教練說話。

### 🟡5. cron 失敗通知：目前乾淨，但「未來新任務」會重蹈覆轍
讀完 `server-cron-CJwAiILI.js`（114KB 現役檔）全文查證：失敗通知**只有兩條路**——門檻型 `sendCronFailureAlert`（7/6 已關）+ 單次型 `dispatchCronFailureDestinationNotifications`（7/7 已用 bestEffort 堵住）。**沒有第三條暗路**；全域失敗目的地（globalFailureDestination）未設定 ✅。4 個 announce 任務 bestEffort=True 已全部驗證生效 ✅。
**但**：新建 announce 任務時 bestEffort 預設是 false——未來哪天建新排程忘了加 `--best-effort-deliver`，單次失敗推播就會復發。這是案例 37「白名單式靜默過期」的同款結構。
**建議**：把「建 announce cron 必加 `--best-effort-deliver`」寫進 E09 cron 鐵律。

### 🟡6. WEBSITE_REPOS 白名單仍是手動清單
7/7 已補齊 13 個站台，目前正確。但根治法是動態掃 `~/github_repos/` 目錄（簡報也建議此方向），從此不會再有「新站台忘記登記」的靜默失效。全機掃描確認這是**唯一一份**寫死站台清單，沒有其他同類地雷。

### 🟡7. council_orchestrator.sh 有明文 Telegram bot token
已查證 repo（Coach1973/mac-openclaw-workflows）是**私有**，外洩風險有限。但同腳本明明已經會從 `auth-profiles.json` 讀 MiniMax 金鑰，bot token 應比照辦理。若該腳本隨 🔴3 一起退役，此項自動消失。

### 🟡8. 終端機對話管線有 4 個寫入者，git 歷史 6 成是機器雜訊
最近 24 小時 43 個 commit，27 個是自動任務（備份 9、蒸餾 8、session-end 同步 8、鏡像 2）。寫入者：crontab 每 15 分備份、每 30 分蒸餾、Stop hook 蒸餾（同一支腳本，5 分鎖）、每 30 分 recall 收割。
**建議**：Stop hook 已能即時蒸餾，crontab 的 30 分蒸餾可降頻為每 2 小時兜底；修好 🔴1 後 session-end 雜訊自然消失。

### 🟡9. 試金石案例庫編號三套並行
早期案例用字母（案例 A、B、C、D…），24 起用數字，聯想機另開 W 系列（W02、W03）；**案例 25 出現兩次**（兩個不同標題、不同內容）。跨機引用「案例 25」時會歧義。建議做一次編號統一 + 對照表。

---

## 🟢 第三級：查證過、很好、不用動（7 件）

1. **25 個 hook 腳本全部存在**，無斷頭掛空（E09 過關）
2. **5 個 PreToolUse 防呆鎖**（刪除/Netlify/截圖/跨機/預覽）全部對應真實血淚案例，符合案例 34 定調的「真出過事才上鎖」，沒有預防性亂鎖
3. **7/7 的 bestEffort 修復是真的**——4 個 announce 任務逐一驗證生效
4. **三機大腦架構乾淨**：`~/.claude/projects/.../memory` → symlink → `workspace/claude-brain`，隨 workspace repo 推送；remote 只剩 origin + lessons，7/8 的過期 remote 清理屬實
5. **VPS 分支隔離**（master 與 main 無共同祖先）是刻意防火牆，非漏洞——已在本報告正式記錄，防止未來誤合併
6. **junshi_task_worker 是 WatchPaths 事件驅動**（正確模式），log 停在 6/13 只代表沒新任務，非故障
7. **session-fix 與 terminal-watchdog 有真實戰功**：7/7 晚上 8:38 的 Context Overflow 就是 session-fix 自動救回的（HEARTBEAT 有案）

---

## 📋 未竟事項（需要教練決策或他機配合）

| 事項 | 原因 |
|------|------|
| 聯想 / ACER 兩機的同款稽核 | 只能在各自機器上跑；發跨機指令需教練拍板（案例 34 教訓，不私自發） |
| 🔴3 的 council-orchestrator 去留 | 需教練確認 Council Mode 還用不用 |
| 🔴1、🔴2 的修復執行 | 遵照簡報「稽核不順手改」原則，等教練說「修」即動工，三件合計約 15 分鐘 |

---

> Fable 5 親筆，2026-07-08 凌晨 03:05 台灣時間。
> 每一條發現都附了可重跑的查證方法，下一棒可以複驗。
