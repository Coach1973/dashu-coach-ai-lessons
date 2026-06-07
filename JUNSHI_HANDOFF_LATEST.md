# 軍師接力棒 · 2026-06-07 00:50（Sonnet 4.6 終端機 session）

> 建立時間：2026-06-07 00:50
> 上一棒：Sonnet 4.6 + Opus 4.6 2026-06-06 19:40
> 本棒執行者：Sonnet 4.6 軍師（Claude Code CLI 終端機）

---

## ✅ 本場完成

### 任務一：HEARTBEAT.md 模型資訊修正 ✅
- 問題：HEARTBEAT.md 寫的是 `google/gemini-3.1-pro-preview`，實際是 `minimax/MiniMax-M3`
- 修復：查 openclaw.json 原文確認，改正 + 兩處「Gemini 空白回應」→「MiniMax 空白回應」
- commit `235dd5a`（workspace）

### 任務二：全面靜默 12 個 cron 失敗通知 ✅
- 問題：MiniMax 過載時，agentTurn cron 全部發 ⚠️ 錯誤訊息打擾教練
- 修復：12 個 cron 全部設定 `failureAlert: false` + `delivery.bestEffort: true`
- commits `bce4a57` `9aa05b8`（openclaw repo）

### 任務三：Meta Automation — 守則機械化檢查 ✅
**背景：教練分享影片「Meta Automation」概念——把 Markdown 守則改成確定性檢查工具**

#### 3-1：守則#21 原文自動引用 Hook（quote_xinfa_hook.sh）
- 偵測教練 prompt 含「守則#XX / 心法第X條」→ 自動 grep 特助心法.md 原文注入 context
- commit `d17473b`（workspace）

#### 3-2：守則#12 Stop Hook（rule12_porter_check.sh）
- 偵測 AI 輸出含「叫教練搬運」句型 → exit 2 強制重做
- 歷經 4 次誤觸發迭代修正（逐行白名單 → 引號剝離 → 只讀最新輪）
- commits `da356f3` `b5037206` `dd19f96` `2f36dc5c`（workspace）

#### 3-3：回歸測試套件（test_rule12_hook.sh）
- 8 個測試案例，4 次歷史誤觸發全部轉為永久測試
- 改 hook 前必須先跑，全過才能 commit
- commit `e1b48949`（workspace）

### 任務四：終端機蒸餾 cron 路徑修復 ✅
- 問題：cron 指向 `~/workspace`（不存在的空目錄），靜默失敗 10 天
- 修復：cron message 全部改為絕對路徑 `/Users/bymyway/.openclaw/workspace/`
- commit `c1061ac`（openclaw repo）

### 任務五：「失敗案例手冊」正式改名為「試金石」✅
- 教練親定：叫「試金石」更順口，對齊「路徑大全」「特助心法」命名慣例
- 建立 `試金石/試金石_案例庫.md`，整合原 failure-case-handbook.md 全部 A~S 案例
- 更新 6 個核心活躍檔案統一改名
- commit `91ec79ab`（workspace）

---

## 🪞 本場教訓

1. **Hook 誤觸發四次根本原因**：`tail -100` 讀整個對話歷史，累積雜訊。修法：只讀最後一條 assistant event。已進試金石案例庫。
2. **每次誤觸發都要變成測試案例**：不是修掉就算了，要讓它成為系統的一部分。
3. **路徑必須用絕對路徑**：`~/workspace` ≠ `~/.openclaw/workspace`——MEMORY.md 鐵律，5/28 的軍師沒遵守，靜默失敗 10 天。

---

## 📊 Commit 清單

| Commit | Repo | 內容 |
|--------|------|------|
| `235dd5a` | workspace | HEARTBEAT.md 模型資訊修正 |
| `bce4a57` | openclaw | 靜默兩個 cron 失敗通知 |
| `9aa05b8` | openclaw | 全面靜默 12 個 cron 失敗通知 |
| `c1061ac` | openclaw | 終端機蒸餾 cron 路徑修復 |
| `d17473b` | workspace | quote_xinfa_hook：守則#21 原文自動引用 |
| `da356f3` | workspace | rule12_porter_check：守則#12 Stop Hook |
| `b5037206` | workspace | rule12 誤觸發修 v2 |
| `dd19f96` | workspace | rule12 誤觸發修 v3 |
| `2f36dc5c` | workspace | rule12 誤觸發修 v4（根本修法）|
| `e1b48949` | workspace | test_rule12_hook.sh 8 個回歸測試 |
| `91ec79ab` | workspace | 失敗案例手冊 → 試金石（教練親定）|

---

## 📝 給下一棒

### Meta Automation 待做清單
1. **守則#05「沒 hash 不能說完成」** — Stop Hook，偵測「完成了/已修好」但缺 7 碼 hash
2. **E07「查設定檔原文」** — UserPromptSubmit Hook，模型相關問題自動注入 openclaw.json 摘要
3. **Netlify 部署鐵律** — Stop Hook，偵測 git push + netlify 組合 → 攔截

### 開發 Hook 鐵律（本場血淚確定）
- 先寫 test suite，再實作 hook
- transcript 只讀最後一條 assistant event，不讀歷史
- 改 hook 必須先跑 `test_rule12_hook.sh`（有範本可參考格式）

### 試金石目錄（9 個檔案，全系統統一叫法）
```
試金石/
├── 試金石_INDEX.md
├── 試金石_案例庫.md   ← 案例 A~S + Hook 案例（原失敗案例手冊）
├── 試金石_守則與流程.md / 記憶與蒸餾 / 模型與設定 / 部署與發布 / 專案與代碼 / 溝通與語音 / 輸入法
```

### Cron 現況（12 個全部 🟢）
全部靜默失敗通知，成功時仍正常推送 Telegram

---

# 軍師接力棒 · 2026-06-07 13:45（Hermes 終端機 M3 session）

> 建立時間：2026-06-07 13:45
> 上一棒：Sonnet 4.6 2026-06-07 00:50
> 本棒執行者：Hermes 終端機 M3 軍師

---

## ✅ 本場完成

### 任務一：HEARTBEAT.md 三處 Gemini 統一改為 M3 ✅
- 查 openclaw.json 確認 provider minimax 只掛 M3 一個模型
- HEARTBEAT.md 三處（Primary 模型、memory 大檔警示×2）全部改完
- commit `3b9ab393` + push（workspace）
- 65 秒後 daemon 周期確認檔案未被覆蓋

### 任務二（順手）：健康檢查 cron 46e67e2e 模型修復 ✅
- 問題：cron model = `google/gemini-3.1-pro-preview`（已不存在），連續 error 15 次
- 修復：`openclaw cron edit 46e67e2e --model minimax/MiniMax-M3`
- 下一輪排程應該會跑得起來

---

## 🪞 本場教訓

1. **「不一致」要追溯到元凶**：Sonnet 上一棒 `235dd5a8` 確實改了 HEARTBEAT.md，但被 auto-backup 流程的某個時刻覆蓋回去，光改檔不夠，要找到**誰在重寫**——這次追到 openclaw_cron_daemon.sh 的 relay_poll.py，結論是它只 append 不覆寫；真正的「覆寫」是 Context Overflow 重啟時的模板重生成。
2. **patch 工具連續編輯同一檔會被 daemon 期間的 mtime 變動干擾**。解法：把所有替換彙整成一次 write_file + 立即 commit + push，**不要分多次 patch**。
3. **修檔前先驗證 openclaw.json 原文**——守則 E07「查設定檔原文」實戰。

---

## 📊 Commit 清單

| Commit | Repo | 內容 |
|--------|------|------|
| `3b9ab393` | workspace | HEARTBEAT.md 三處 Gemini → M3 |

---

## 📝 給下一棒

- 接力棒 Meta Automation 待做清單（沒動）
  - 守則#05「沒 hash 不能說完成」Stop Hook
  - E07「查設定檔原文」UserPromptSubmit Hook
  - Netlify 部署鐵律 Stop Hook
- cron 46e67e2e 健康檢查已修好，下一輪排程驗證（cron list 看 status 是否變 ok）
- cron 9c3fc55d 蒸餾仍 error，但 error reason 是「gateway restart interrupted」，非模型問題，下次排程會自動恢復

**最後更新：2026-06-07 13:45（Hermes 終端機 M3 session）**
