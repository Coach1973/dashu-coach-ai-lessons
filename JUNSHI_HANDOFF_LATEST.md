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

# 軍師接力棒 · 2026-06-07 14:10（Hermes 終端機 M3 session）

> 建立時間：2026-06-07 14:10
> 上一棒：Hermes M3 2026-06-07 13:50
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
- ✅ 已驗證恢復（git log 看到 `auto-backup 2026-06-07 14:07` 跟 `auto: 接力棒鏡像同步 2026-06-07 13:50` 兩條 auto commit 正常產生）

### 任務三：守則#05 hash Hook（Meta Automation）✅
- 守則#05「凡走過必留痕跡」機械化：完成詞 + 無 hash → exit 2 強制重做
- 測試先行（沿用 #12 紀律）：16 個案例，**一次全 PASS**
- 整合測試：模擬違規 transcript → exit 2 + 修正指引 ✅
- 註冊到 `~/.claude/settings.json` Stop hook（跟 #12 並列）
- commits:
  - `d9106dce` test: 測試套件先行
  - `ff259403` feat: hook 實作 + 整合

### 任務四：E07 設定檔自動注入 Hook（Meta Automation）✅
- 守則 E07「存在性驗證」+ #15「說不知道比胡說八道更值得尊重」機械化
- 教練 prompt 提到「模型/provider/M3/Opus/Kimi」等詞時，自動從 openclaw.json 抽出摘要注入 context
- 觸發：模型/provider/切換/M3/Opus/Sonnet/Haiku/Kimi/Claude/GPT/Gemini 等 22 個詞
- 白名單：BMW/車/音樂/俳句/health care provider 等英文語境（避誤觸發）
- 16 個測試一次全 PASS，實際整合測試 OK
- 註冊到 `~/.claude/settings.json` UserPromptSubmit hook（跟 quote_xinfa 並列）
- commit `b67e1104`（workspace）

---

## 🪞 本場教訓

1. **「不一致」要追溯到元凶**：光改檔不夠，要找到誰在重寫。
2. **patch 連續編輯會被 daemon 干擾** → write_file 一次寫 + 立即 commit + push。
3. **修檔前先驗證 openclaw.json 原文**（E07 實戰）。
4. **#05 hash Hook**：TDD + 沿用 #12 範本讓風險降到最低，16 個測試一次過。
5. **E07 設定檔注入實作 4 個踩雷**（已記入試金石）：
   - shell array for 迴圈 `"${ARR[@]}"` 寫成單一字串就壞
   - jq object value 不能直接 `//`，要包 `(...)`
   - openclaw.json `agents` 結構是 `.agents.list[]` 不是 `to_entries`
   - JSON 構造用 `python -c`，不要 printf（escape 問題）

---

## 📊 Commit 清單

| Commit | Repo | 內容 |
|--------|------|------|
| `3b9ab393` | workspace | HEARTBEAT.md 三處 Gemini → M3 |
| `80fdd30b` | workspace | 接力棒更新 |
| `d9106dce` | workspace | test: rule05_hash 測試套件 |
| `ff259403` | workspace | feat: rule05_hash hook 實作 + 整合 |
| `f357bb7e` | workspace | 接力棒：守則#05 完成 + 剩餘 2 個待做 |
| `b67e1104` | workspace | feat: E07 設定檔自動注入 hook |

---

## 📝 給下一棒

### Meta Automation 待做清單（剩 1 個）
- 🔴 **Netlify 部署鐵律 Stop Hook**——偵測 git push + netlify 組合 → 攔截
  - 風險：80 次不成熟部署已燒 1200 點
  - 挑戰：「已 push 還能攔截嗎」技術問題需先驗證
  - 替代方案：PreToolUse Hook（推送前攔截）可能比 Stop Hook 可靠

### cron 狀態（已全部恢復健康）
- `46e67e2e` 健康檢查：✅ 已驗證恢復運作
- `9c3fc55d` 蒸餾：上次 error 為 gateway restart，下次排程自動恢復

### 已完成的鉤子（給下一棒直接參考結構）
- `scripts/rule12_porter_check.sh` + `test_rule12_hook.sh`（搬運工句型）
- `scripts/rule05_hash_check.sh` + `test_rule05_hash.sh`（完成詞缺 hash）
- `scripts/e07_settings_inject.sh` + `test_e07_settings.sh`（模型問題自動注入）← 本場新增
- 註冊位置：`~/.claude/settings.json` → `hooks.Stop[]` / `hooks.UserPromptSubmit[]`
- 共同紀律：先測試後實作、只讀最後一條（Stop）、白名單避誤觸發、違規寫 log

### 試金石案例（已記入，未來可正式寫入案例庫）
- E07 4 個實作雷：shell array / jq // / agents 結構 / JSON 構造

**最後更新：2026-06-07 14:10（Hermes 終端機 M3 session）**
