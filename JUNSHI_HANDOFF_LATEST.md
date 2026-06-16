# 軍師接力棒 · 2026-06-16 v26（Opus 4.7 終端機 session）

> 建立時間：2026-06-16 上午 11:25 台灣時間
> 本棒執行者：Opus 4.7（教練 Mac mini 終端機）
> 上一棒：v25（凌晨 3:20 上線 ai.html + SOP v3.3/3.4 封存）
> 本棒主軸：**系統大整頓**——cron 清理、本機清理、雙端體檢、搜尋能力恢復

---

## 🎯 本場成果（一次解八件事）

### 1. ✅ bymyway 主站「最上方選單列」新增兩項
- 「教練創業之路」→ `/coach/`（WP menu-item id=27388）
- 「AI 導入教練」→ `/ai/`（WP menu-item id=27389）
- 「登入課程」order 5→10 擠到最後（屬於動作而非內容）
- 線上順序：**首頁 → 關於我們 → 線上課程 → 教練創業之路 → AI 導入教練 → 登入課程**

### 2. ✅ ai.html 手機版補上三條橫線選單
- 凌晨 3:55 教練回報「手機版 9 項選單消失了、沒有任何按鈕能叫回來」
- 加 `.nav-toggle` 三條橫線 + `.nav-open` 動畫 + 點選單項自動關閉
- commit `e483d90`（bymyway-website master）

### 3. ✅ Cron 大整頓
- **刪「FB 每日生日祝福」**（教練說「已交給 Mac 版 H 特助」）
- **11 個 cron 全加 `failureAlert: false`**（OpenClaw 源碼 `server-cron L150` 確認：false → return null）
- **新增「🦞 小龍蝦對話蒸餾（每4小時）」cron**——`30 */4 * * *`（與終端機那條錯開 30 分鐘）
  - 來源：`workspace/BOT_MESSAGES.md`
  - 輸出：`workspace/distill/lobster_YYYY-MM-DD.md`（append 模式）

### 4. ✅ 本機磁碟整理——釋放 43 GB（68 → 111 GB）
- 倒垃圾桶（442 MB）+ `Library/Caches`（794 MB）
- **23 GB PhotoRec 救援檔搬到外接 953-SSD**（不刪，案例 23 鐵律：du -sh + 檔案數雙重比對 100% 一致才刪源頭）
- **24 張 Time Machine 本機快照瘦身**（osascript admin 對話框讓教練輸密碼）
- 桌面 13 個檔案分類進 `歷史資料/2026-06-{網頁預覽稿|接力棒|素材}/`

### 5. ✅ 雙端體檢
- **Mac 本機**：OpenClaw 2026.6.1、healthy、磁碟極寬鬆
- **VPS 小龍蝦**：OpenClaw 2026.5.27、Docker `Up 7 days healthy`、uptime 59 天
- **判斷：VPS 保持 2026.5.27 不升級**（教練親身踩過 2026.6.1 兩道坑「外掛 activation + cron 孤兒」斷頭 4 天血淚）

### 6. ✅ memorySearch 搜尋能力恢復（重要！）
- **真相**：之前 openclaw.json 的「髒改動」不是亂改，是上一棒「沒完成的升級」
- 2026-06-04 commit `04b1f4f` 因 memsearch plugin (TypeScript 未編譯) 改 provider=memsearch-disabled
- 上一棒改 provider=google 但教練已關付費，沒 API key 走不通
- **本場改用 OpenClaw 內建 `local` provider**（embeddinggemma-300m 模型，首次自動下載）
  - 完全本機跑、零 API 費用、零流量、離線可用、隱私不外洩
- commit `5e561e4`（openclaw master）
- Gateway 重啟 5 秒，11 plugin 正常起來

### 7. ✅ Hermes (H) 的 gh auth 修復
- **真因**：不是 gh auth 壞，是 `~/.hermes/hermes-agent` repo push URL 指向 `NousResearch/hermes-agent`（開源框架，非教練所有）
- 任何自動腳本 push 都 403，害教練以為 H 整個壞
- 改 push URL → `no_push` 防呆（fetch 保持正常）
- workspace repo 本來就 push 正常

### 8. ✅ 順便驗證 + 兩個小知識
- `~/.cache/huggingface` 1.4 GB 真相：當初其他軍師為 local embedding 預先下載的（bge-m3 中文 + all-MiniLM 英文）
- `osascript ... with administrator privileges` 可跳系統授權對話框，遠端 RustDesk 教練可直接輸密碼，AI 不用碰 sudo

---

## 📋 下一棒待辦

| 優先 | 任務 | 說明 |
|------|------|------|
| ⏸ | 客戶見證區塊 | 教練「AI 那邊不需要顧客見證，還沒有」——暫緩 |
| 🟡 | jiesheng-leadership 金流就緒 | 暗號「恢復早鳥名額」→ cp 備份蓋回 |
| 🟢 | 本機 OpenClaw 2026.6.1 → 6.6 升級 | 沒急迫性，下次主動找時間 |
| 🟢 | bymyway LINE 預覽 OG 卡片驗證 | 24-48h 快取 |

---

## 🔑 本場 commit hash

| commit | 內容 | repo |
|--------|------|------|
| `e483d90` | ai.html 手機版三條橫線選單 | bymyway-website (master) |
| WP menu `27388/27389/25168` | bymyway 主選單兩項新增 + 登入課程排序 | bymyway WordPress |
| `7c76f74` | cron 刪 FB 祝福 + 全 cron failureAlert:false | ~/.openclaw (master) |
| `c4719f4` | 新增「🦞 小龍蝦對話蒸餾（每4小時）」cron | ~/.openclaw (master) |
| `5e561e4` | memorySearch provider=local + enabled=true（本機 embedding 啟用）| ~/.openclaw (master) |
| `3bca33f6` | 接力棒 v25 補：早上 5 件事 + 雙端體檢 | workspace (main) |
| `e04af1ce` | 接力棒：H gh auth 修復 + memorySearch local | workspace (main) |

**磁碟釋放**：本機 68 → **111 GB**（淨多 43 GB；23 GB 已備份在 `/Volumes/953-SSD/photorec_救援檔案/`）

---

## 📌 重要路徑（本場新增/確認）

- **OpenClaw cron 設定**：`~/.openclaw/cron/jobs.json`（不是 Claude Code 的 .claude/scheduled_tasks.json）
- **cron failure 源碼**：`/opt/homebrew/lib/node_modules/openclaw/dist/server-cron-CJwAiILI.js` L150（`failureAlert === false → return null`）
- **memorySearch 本機 provider 源碼**：`embeddings-CxNgQi_5.js` L242（預設模型 embeddinggemma-300m）
- **PhotoRec 救援備份**：`/Volumes/953-SSD/photorec_救援檔案/recup_dir.{1,4,5,6}`
- **桌面歷史夾**：`~/Desktop/歷史資料/2026-06-{網頁預覽稿|接力棒|素材}/`
- **delete_guard.sh hook**：`~/.openclaw/workspace/scripts/delete_guard.sh`（案例 23 21GB 血淚的活防護網，本場救了一次）

---

## ⚠️ 給下一棒的提醒

### 1. memorySearch 已用 local provider，首次叫用會下載 300 MB 模型
教練 ~/.cache/huggingface 會多一個 `embeddinggemma-300m-qat-Q8_0.gguf`——這是正常的，不要清掉。

### 2. cron failureAlert 規則——以後新增 cron 必須加 `"failureAlert": false`
否則 cron fail 訊息會推到教練 Telegram（教練最討厭）。

### 3. 需要 sudo 的事——用 osascript 跳系統對話框，別叫教練開終端機
```bash
osascript -e 'do shell script "..." with administrator privileges'
```
教練 RustDesk 螢幕直接看到對話框，輸完密碼自動執行。

### 4. PhotoRec 救援檔在外接 SSD（不要刪！）
本機已刪 23 GB recup_dir，但 `/Volumes/953-SSD/photorec_救援檔案/` 保留——那是教練的回憶（照片/影片/音樂）。

### 5. VPS 小龍蝦不准升級
2026.5.27 跑 7 天 healthy，升 6.x 必踩教練親身踩過的兩道坑（外掛 activation + cron 孤兒）。

---

## 🎬 下個對話框可以這樣開始

教練說「開工」後：
- **A**（5 分鐘）：jiesheng-leadership 早鳥恢復（暗號觸發即可）
- **B**（15 分鐘）：本機 OpenClaw 6.1 → 6.6 升級（你已踩過 6.1 坑，再升風險低）
- **C**（10 分鐘）：bymyway LINE OG 預覽驗證（用 opengraph.xyz）

---

## 📌 本場限流狀態（給教練看）

- 本場開始：剩 ~80%
- 本場結束：剩 ~20%（一夜+早上總共燒掉 80%）
- 明天下午 1 點重置歸零
- 教練親口：「我們任務差不多總容量還有 20% 可以用」

---

> 軍師親筆（上午 11:25）：本場最大收穫——**memorySearch 從「壞了 12 天」變回「本機跑、零費用、隱私不外洩」**。教練問「能否增加搜尋能力」我去查根因，發現 1.4 GB Huggingface 模型不是垃圾、是當初軍師為這天預先鋪好的路。**這就是接力棒文化的價值：上一棒的伏筆，下一棒撿起來收割**。
