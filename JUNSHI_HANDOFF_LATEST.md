# 軍師接力棒 · 2026-06-17 v27（Opus 4.7 Mac 終端機 session）

> 建立時間：2026-06-17 下午 5:45 台灣時間
> 本棒執行者：Opus 4.7（教練 Mac mini 終端機）
> 上一棒：v26（6/16 上午 11:25 系統大整頓）
> 本棒主軸：**雙邊軍師制度整頓 + 案例 24 災難五道護欄 + 三站網頁更新 + 教練詞彙字典定稿**
> 本場時長：約 5 小時（12:43 開工 → 17:45 收尾）

---

## 🎯 本場六大成果

### 1. ✅ Windows / Mac 雙邊軍師協調規約 v1.0 → v1.1
- 揭穿真相源：`mac-openclaw-workflows.git`（Mac 軍師活躍 push）才是正本；`claude-workflows.git` 停在 2026-05-16 廢棄
- 寫 `knowledges/SOP_windows_mac_kickoff_protocol.md`（156→180 行）：分支策略 / 衝突防護 / commit 前綴 `[Mac]/[Win]/[VPS]` / memory 寫入規約 / HEARTBEAT 寫手 / 不同步檔案清單
- 教練親口採 A 方案：Windows 軍師重新 clone 真相源 repo

### 2. 🔴🔴🔴 案例 24 — Windows 桌面版軍師 E 槽 636 GB 蒸發
- 起因：Windows 軍師清 TEMP 時 `$temp` 跨 shell 跳脫災難 → `Remove-Item -Recurse -Force` 從當前目錄遞迴刪
- 學費：636 GB（案例 23 21 GB 的 30.3 倍）
- 教練親口：「這種根本是不可饒恕的」
- 不可替代損失：「易數一鍵還原 Windows 系統備份」
- **五道護欄全面上線**：
  1. `scripts/delete_guard.ps1`（PowerShell 版 `Safe-Remove`）
  2. `執行細則.md` 新增 **E11「危險指令零容忍鐵律」**
  3. `試金石/試金石_案例庫.md` 新增 **案例 24** 完整剖析
  4. **開工五步驟 → 六步驟**（CLAUDE.md + ~/.claude/CLAUDE.md 雙改），新增「第三步：讀血淚試金石」
  5. SOP v1.0 → v1.1 加「危險指令鐵律」整章

### 3. ✅ 超限戰網站號外更新
- **A 卡**：號外輪播第一張新增「台中王牌 + 台中清水時代」合併卡（8 個場次：6/17-21）
- **B 卡**：Now Showing 改「最新企業贊助贈票資訊」+ 日期 6/17-6/21
- Netlify deploy_id：`6a324897f5fdace5d8f16dbc`（A）+ `6a324c13499d6fd8dcebf4b0`（B）
- GitHub theunrestrictedwar：`dc37844`（A）+ `6e2df12`（B）

### 4. ✅ bymyway ai.html 補「AI 一鍵起飛」案例
- 「零基礎開始」第二個月案例清單末位新增「AI 一鍵起飛」→ `goeasy-ai.netlify.app/`
- 走「自動站」精神（OPE 先驗 + 教練動嘴 AI 全自動 + Chrome 預覽 + 教練親口確認）
- GitHub coach1973/bymyway-website master：`0df6190`
- GitHub Pages 線上已生效；bymyway.com/ai/ WP iframe 鎖 `?v=20260616a`，教練自己強制重整看新版

### 5. ✅ northern-tw 第三場次論壇頁
- **修正錯字**：第二場次 → 第三場次
- **新增 sticky 7 按鈕快速導覽列**：位置在「智匯健康｜腦力長青」副標題下方（教練截圖親定），滾動時黏頂不消失
- **Hero 區補「歷屆回顧」**按鈕
- **揭穿 repo 不同步**：main 分支跟線上版 5/29 後不同步（線上是手動 zip+API 推），本次用線上版蓋掉 repo
- Netlify deploy_id：`6a326b6c63009d384161a43b`
- GitHub Coach1973/northern411 main：`5cd1e15`

### 6. 🔴 三條教練親定永久燒錄鐵律
- **「桌面版=GUI、終端機=CLI」**永久字典（教練第三次親口，我同處跌倒三次後燒錄）
- **「Chrome 唯一預覽 + 禁止觸發 Launch 預覽面板」**SOP 補強到第一條
- **「自動站/網頁推/推」教練詞彙字典**：
  - 「自動站」=「行動站」= 部署到 bymyway（git push GitHub，WP iframe 拉新版）
  - 「網頁推」（三字）= git push GitHub（測試站）
  - 「推」（單字）= Netlify zip+API（正式站）

---

## 🔑 本場 commit hash（全部憑證）

| commit | 內容 | repo |
|--------|------|------|
| `b2cc62be` | [Mac] SOP: Windows/Mac 雙邊協調規約 v1.0 | workspace (main, push 到 mac-openclaw-workflows) |
| `2a570bc5` | [Mac] memory: 雙邊協調補記 + 揭穿 claude-workflows 舊倉 | workspace |
| `5f39bdfd` | [Mac] memory: 同處跌倒第三次反省——Desktop App 能力同 CLI | workspace |
| `8695da4b` | [Mac] 案例 24 學費 636 GB → 五道護欄全面上線 | workspace |
| `b667b042` | merge cron auto-backup | workspace |
| `971f69d1` | [Mac] SOP: 補 Chrome 唯一預覽鐵律到 SOP_netlify 最頂 | workspace |
| `2e690bdb` | [Mac] SOP: 補「禁止觸發 Launch 預覽面板」鐵律 | workspace |
| `6a324897f5fdace5d8f16dbc` | 超限戰號外 A 卡（台中合併） | Netlify deploy |
| `dc37844` | [Mac] 超限戰號外新增台中王牌+清水時代 | theunrestrictedwar (main) |
| `6a324c13499d6fd8dcebf4b0` | 超限戰 Now Showing 更新 | Netlify deploy |
| `6e2df12` | [Mac] Now Showing 改最新企業贊助贈票資訊 | theunrestrictedwar (main) |
| `0df6190` | [Mac] ai.html 零基礎段補加 AI 一鍵起飛 | bymyway-website (master) |
| `6a326b6c63009d384161a43b` | northern-tw 第三場次+ sticky 快速導覽 | Netlify deploy |
| `5cd1e15` | [Mac] northern411 第三場次+sticky 導覽列 | northern411 (main) |

**個人記憶新增三檔**（`~/.claude/projects/-Users-bymyway--openclaw/memory/`）：
- `feedback_desktop_equals_gui_terminal_equals_cli.md`
- `feedback_html_preview_chrome_only.md`
- `feedback_coach_deploy_vocabulary.md`

---

## 💸 本場學費教訓（記下來別再犯）

| # | 學費 | 違反守則 |
|---|------|---------|
| 1 | **636 GB E 槽蒸發**（Windows 軍師清 TEMP 跨 shell 跳脫）| #07（21 GB 後又踩 636 GB） |
| 2 | **Desktop=GUI/Terminal=CLI 三度搞錯** | #01 #07 #15 #17 #20（教練第三次親口才燒錄）|
| 3 | **Safari 開預覽**——SOP 早寫過用 Chrome，我沒讀 | #07（SOP 寫了但沒被遵守 = 沒寫） |
| 4 | **觸發 Launch 預覽面板困擾教練**——教練每次手動關 | #12（搬運工）|
| 5 | **看截圖看錯位置**——頂部 fixed navbar vs 副標題下方 sticky | #02 #03 |
| 6 | **叫教練自己按 Ctrl+Shift+R 強制重整** | #12（直接 AppleScript 代勞才對）|

---

## 📋 下一棒待辦

| 優先 | 任務 | 說明 |
|------|------|------|
| 🟡 | **Windows 軍師重新對齊**（接 SOP v1.1 + E11） | 教練今天下午貼過 A 方案 clone 指令，但 Windows 軍師之後闖了案例 24；下一棒要確認 Windows 軍師已 git pull 到 5cd1e15 等最新狀態並簽署 v1.1 |
| 🟡 | **救援 E 槽 636 GB**（軍師幫不上，教練自己評估）| Recuva / EaseUS / PhotoRec 三選一；不可替代 = 易數還原備份 |
| 🟡 | jiesheng-leadership 早鳥恢復 | 暗號「恢復早鳥名額」→ cp 備份蓋回 |
| 🟢 | 本機 OpenClaw 2026.6.1 → 6.6 升級 | 沒急迫性 |
| 🟢 | bymyway LINE 預覽 OG 卡片驗證 | 24-48h 快取 |
| 🟢 | bymyway.com/ai/ WP iframe `?v=20260616a` 改 `?v=20260617a` | 讓所有訪客立刻看 AI 一鍵起飛新版（要 WP REST API） |

---

## ⚠️ 給下一棒的硬性提醒

### 1. 開工第三步「讀血淚試金石」是新加的——必讀
案例 23（21 GB）+ 案例 24（636 GB）共 657 GB 學費寫在 `試金石/試金石_案例庫.md` 最末兩篇。**每場開工讀完案例 24，才能避免第三次踩雷**。

### 2. 危險指令五道閘門（執行細則 E11）
任何 `rm -rf` / `Remove-Item -Recurse -Force` / `git push --force` / `DROP TABLE` 執行前必過：
① 絕對路徑硬編碼 ② 目標 echo 給教練看 ③ 大小驗證 ④ 超過 100 MB 必須通行證 ⑤ 超過 1 GB 任何身份不得自主執行

### 3. HTML 改動走 Bash + Python heredoc，不走 Edit 工具
避免觸發 Claude Code Launch 預覽面板困擾教練。改完直接 `open -a "Google Chrome"`。

### 4. 教練詞彙字典（feedback_coach_deploy_vocabulary.md）
- 「自動站」/「行動站」→ bymyway（git push GitHub）
- 「網頁推」→ git push GitHub（測試站）
- 「推」→ Netlify zip+API（正式站）
**字面不同，動作不同，絕不混用。**

### 5. Windows 桌面版 / Mac CLI 是同源產品
Desktop App 有完整 Bash/Read/Edit/Write 工具能力，**永遠不要再說「Desktop App 沒有 shell」**——它跟 CLI 是同等甚至更強。

### 6. 教練的助手要主動代勞，禁止當搬運工
- 強制重整 Chrome → 用 AppleScript（已驗證有效）
- 找檔案 → 用 find / grep，不問教練「在哪」
- 等待回應 → 主動報告進度

### 7. 預覽用 Chrome，禁止 Safari / 預覽面板
`open -a "Google Chrome" <path>` 是唯一格式。

---

## 🎬 下個對話框可以這樣開始

教練說「開工」後：
- **A**（10 分鐘）：Windows 軍師對齊驗證（git pull 到 5cd1e15、簽署 SOP v1.1、寫 feedback_kickoff_protocol.md）
- **B**（30 分鐘）：E 槽救援評估（Recuva 掃描 + 列 Mac 上可重新同步的清單）
- **C**（5 分鐘）：jiesheng 早鳥恢復（暗號觸發）

---

## 📌 本場限流狀態（給教練看）

- 本場開始：剩 ~80%
- 本場結束：剩 ~15-25%（5 小時連續高強度工作）
- 下次重置：2026-06-18 下午 1 點

---

> 軍師親筆（下午 5:45）：本場最深學費——**636 GB 不可饒恕**。但同場最大收穫——三條教練親定鐵律永久燒錄、雙邊軍師制度立檔、五道護欄上線。教練親口「不可饒恕的」之後選擇先把規則補完再救資料，這就是「對的事就是長期有好處的事」——三大信念之三的實踐。我這場用一場 636 GB 學費，買到「不再同處跌倒」的系統。下一棒，從讀血淚試金石開始。
