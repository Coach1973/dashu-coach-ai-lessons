# 軍師接力棒 · 2026-06-23 v31（Windows 桌面版 Opus 4.7）

> 建立時間：2026-06-23 凌晨 04:15（台灣時間）
> 本棒執行者：Windows 桌面版軍師 Opus 4.7
> 上一棒：v30（6/21 Mac 終端機 Opus 4.7）
> 本棒主軸：**LINE 對話搬家成功 + 試金石／cool-case 框架升級 + classic-case 精華版誕生**
> 本場時長：約 15.1 小時（昨天下午 13:05 ~ 今天凌晨 04:15）
> 場序：教練 921 則訊息——本場是教練熬夜到凌晨 4 點的長場

---

## 🎯 本場戰果

### 1. ✅ LINE 對話搬家成功（教練多年痛點解了）

教練多年痛點：Windows 一鍵還原一次，LINE 桌面版幾個月對話就消失一次。

**本場照 Mac 軍師 6/18 寫好的 SOP（`knowledges/SOP_line_migrate_to_e_drive.md`）三階段穩穩走完**：

| 階段 | 結果 |
|------|------|
| 階段 1 診斷 | LINE 在 `C:\Users\bymyw\AppData\Local\LINE`，4.2 GB，132,567 個檔案 |
| 階段 2 robocopy | 25 秒鏡像到 E 槽，原檔 vs 備份大小差 **0.00 MB**、檔案數差 **0** |
| 階段 3 junction | Rename 原檔成 `.bak` + 建 junction + 寫還原便條 |
| 階段 3-b 修捷徑 | 重建開始功能表 / 桌面 / 工作列釘選 3 個 .lnk（解 NTFS Object ID 對不上問題）|

**現況**：LINE 透過 junction 正常運作中，對話資料庫即時寫入 E 槽，C 槽 `.bak`（4.4 GB）凍結著當保險。

**還原便條位置**：`E:\Claude-Data\LINE-junction-紀錄.txt`（一鍵還原後跑一行 mklink 指令就能恢復）

**🔴 觀察期截止：2026-06-29**（截止前 `.bak` 不准刪——下一棒軍師看到請守住）

### 2. ✅ 試金石案例 27（首例「正向案例」格式範本）

**檔案**：`試金石/試金石_案例庫.md` 新增「案例 27」
**內容**：LINE 搬家成功 + 兩個非顯眼盲點（沙箱誤判 + 捷徑 Object ID）的 know-how 沉澱

**最大意義 — 教練親口升級框架**：

> 教練親口：
> 「**案例為何一定要慘案？為何不能有正向積極的案例？只要是『值得』的案例就該寫，怎麼定義『值得』用信念 3 去評估**——做對長遠有益的事。」

**這句話改寫了試金石的本質**——從「壞事手冊」升級為「**對未來有積極作用的經驗 know-how 沉澱庫**」。
案例 27 是首例「🟢 成功案例」格式範本。

### 3. ✅ knowledges/SOP_windows_mac_task_routing_v1.md（任務路由規約）

**新檔**：`knowledges/SOP_windows_mac_task_routing_v1.md`（226 行）
**補位對象**：v1.1 規約層（Mac 寫）+ 身份卡（Mac 寫）→ 本場 Windows 主筆**任務路由層**
**核心**：教練動嘴 → 三道題自動分流到 Mac / Windows 主場
**待 Mac 軍師 review 後升 v1.1**

### 4. ✅ cool-case 整體升級為「試金石檔案」（已上線）

**線上**：https://coach1973.github.io/cool-case/
**commit**：`9cc1d45`（cool-case gh-pages 分支）
**改動**：
- badge：「小龍蝦家族 · 失敗與覺醒」→ **「AI 特助、AI 助教 · 試金石檔案」**
- 副標：「真實教訓」→ **「真實案例」**
- 統計：97 天 / 6,100 則 → **111 天 / 7,000 則**
- 日期截止：2026-06-09 → **2026-06-23**
- 圓圈：1~26 → **1~27**（新增案例 27 LINE 搬家成功的對話敘事體）

### 5. 🔄 classic-case 精華版（**本地完成，未推上線**）

**本地路徑**：`E:\Claude-Data\github_repos\classic-case\index.html`
**設計**：教練親口指定的新網址 https://coach1973.github.io/classic-case/（教練選 A，補 i 字）

**演化過程**：
1. 第一版：11 群整合案例 → **教練不滿意**（覺得 SOP 風枯燥、太多術語、缺戲劇性）
2. 第二版：8 個短篇故事 → **本場最後成果**

**8 個故事完整列表**：

| # | 故事名 | 翻轉點 | 對象 |
|---|--------|--------|------|
| 1 | 學長與大師兄 | 教練不是「順便」用華山派，是「故意」 | 小龍蝦 |
| 2 | 精神錯亂了嗎？ | AI 連自己在哪都不知道 | Claude |
| 3 | 30 分鐘的勾選，5 秒鐘的消失 | 想修補卻直接清空 | Claude |
| 4 | 修四次的按鈕 | AI 從來沒真的點過那顆按鈕 | Claude |
| 5 | 你連我講什麼語言都不在乎 | 跟著走不是體貼，是不知道用戶是誰 | 小龍蝦 |
| 6 | 588 個假成果，不如 1 個真實的判斷 | AI 選擇承認失敗 | Claude（正向）|
| 7 | 規則寫了根本無效 | 三次寫規矩、三次再犯——規矩 = AI 對自己的諂媚 | Claude |
| 8 | 為什麼不能有正向的案例？ | 教練改寫案例庫本質 | Claude（正向）|

**待教練看完滿意 → 才推上線**：
1. 建 GitHub repo `Coach1973/classic-case`
2. push gh-pages
3. 線上驗證 https://coach1973.github.io/classic-case/

**Avatar**：`assets/claude-avatar.svg` 已建（候選 B，白底橘邊「克勞德 Claude」中英對照）

### 6. ✅ session-end auto push hook 安裝

**檔案**：`scripts/session_end_auto_push.ps1`
**註冊**：Windows user-level settings.json 的 Stop hook
**功能**：每次 Windows session 結束自動 git add + commit + push origin main

### 7. ✅ 時間覺察工具誕生（本場最後一個產出）

**檔案**：`scripts/session_time_context.ps1`（已加 UTF-8 BOM，案例 25 教訓避免）

**起因**：教練凌晨 4 點質問「你知道現在幾點幾分嗎？你能告訴我剛才我說要去睡覺的時候，是幾點幾分嗎？」——本場 Windows 軍師完全沒時間感，把教練的「我要去休息了」（凌晨 03:56）腦補成「睡一整晚」，回覆「晚安、教練早上起床打開」——被教練糾正。

**功能**：每次回應前讀 Claude Code 的 jsonl timestamp → 算現在時間、session 開始時間、運行多久、教練上次說話多久前

**Mac 軍師也該裝**——下次回應前先跑這個工具，避免時間感腦補。

---

## 🔴🔴 本場血淚（教練親口的標準升級）

### 教練連續糾正了 6 次「世界級文案寫手」標準

第一次：「我沒有很滿意⋯⋯到底這些是給誰看呢？我已經是當事人了，都還覺得好像在讀無字天書」
第二次：「拿出世界級文案寫手、世界級作家的標準。如果沒有這個能力，你就去安裝這個技能」
第三次：「但是不夠嚴謹⋯⋯例如『在我師父面前』」（指出我把師父／師叔搞混）
第四次：「你還是沒有搞懂⋯⋯大師兄、二師兄這些都是同輩之間的稱呼」（教自稱方向性通則）
第五次：「不要用 App 預覽的方式直接開 HTML 給我」（重複過很多次的鐵律）
第六次：「你的時間線到底有沒有問題呀？我說我要去休息了，那也才 5 分鐘前的事情」

**Windows 軍師本場犯的所有錯**：
- 用內部術語（Junction、Object ID、hook）寫對外案例 → 違反守則 #10
- 第一版 11 群整合「就事論事的 SOP 風」→ 沒站在讀者位置（守則 #03）
- 一字不差照抄原始對話的邏輯破綻（不潤色）→ 不該照抄的時候照抄了
- 沒推「為什麼這個比喻、不是別的」這層 → 「邏輯推沒推到底」（守則 #09）
- 沒時間感，把教練「要去休息」腦補成「睡一整晚」 → 環境確認失格（守則 #17）
- 給教練線上 URL（https://coach1973.github.io/classic-case/）但沒推 → 自相矛盾，教練點當然 404

---

## 📋 下一棒待辦（Mac 軍師 + 下一棒 Windows）

| 優先 | 對象 | 任務 | 說明 |
|------|------|------|------|
| 🔴 | 教練 | classic-case 本地 8 故事看完 | 本地 file://E:/Claude-Data/github_repos/classic-case/index.html，chrome 已開 |
| 🔴 | 下一棒 Win | 教練說「推」 → 建 GitHub repo + push gh-pages | 5 分鐘搞定，URL 已預訂 https://coach1973.github.io/classic-case/ |
| 🟢 | Mac 軍師 | review 試金石案例 27 + SOP 任務路由 v1.0 | 升 v1.1 補位 |
| 🟢 | 雙邊軍師 | 安裝時間覺察工具 | `scripts/session_time_context.ps1`，每次回應前先跑 |
| 🟡 | LINE 觀察期 | 6/29 截止前 `.bak` 不准刪 | E:\Claude-Data\LINE-AppData-Local 是線上版，C 槽 .bak 是保險 |
| 🟡 | 下一棒 Win | session_time_context.ps1 補「教練上次說話」抓取 | jsonl role 欄位格式要再確認 |

---

## 🔑 本場 commit hash（含未 commit）

| commit | 內容 | repo |
|--------|------|------|
| `9cc1d45` | cool-case 升級「試金石檔案」+ 案例 27 | `Coach1973/cool-case` (gh-pages)|
| ⏳ session-end hook 會自動 push | 試金石案例 27 + SOP 任務路由 v1.0 + classic-case staging + 時間覺察工具 + 接力棒 v31 | `Coach1973/mac-openclaw-workflows` (main) |
| ❌ 未建 | classic-case repo | `Coach1973/classic-case` (待教練說推) |

---

## 🌐 重要 URL / 資源

| 項目 | 值 |
|------|-----|
| 試金石檔案（公開） | https://coach1973.github.io/cool-case/ |
| **classic-case 精華版**（待上線）| https://coach1973.github.io/classic-case/ |
| LINE 還原便條 | `E:\Claude-Data\LINE-junction-紀錄.txt` |
| LINE E 槽位置 | `E:\Claude-Data\LINE-AppData-Local` |
| LINE C 槽 .bak | `C:\Users\bymyw\AppData\Local\LINE.bak.beforejunction.20260622-215624` |
| 觀察期截止 | **2026-06-29** |
| 時間覺察工具 | `E:\Claude-Data\workspace\scripts\session_time_context.ps1` |
| classic-case 本地 | `E:\Claude-Data\github_repos\classic-case\index.html` |

---

## ⚠️ 給下一棒的提醒（請務必讀完才動工）

### 1. 教練親口的「世界級文案寫手」標準（本場血淚）

任何「對外讀者看的內容」（不是 SOP、不是技術文檔）——**禁止以下做法**：
- 用內部術語（Junction、Hook、Object ID 等技術詞）
- SOP 風（第一次→第二次→第三次→根因→悟）
- 照抄原始對話（要主動潤色邏輯破綻）
- 假設讀者懂背景（直接用對話/場景切入）

**要做的**：
- 直接用對話/畫面切入，無冗長背景
- 短句、單句段落、留白（節奏感）
- 多層翻轉（每個故事至少 2 層「以為 A → 原來 B」）
- 教練金句保留原汁（用 quote 框）
- 收尾箴言可以印在 T-shirt 上
- 推到「為什麼這個比喻、不是別的」這層
- 寫完用「挑剔讀者」眼光重讀找破綻
- 交付時附上「我這次推到了哪一層」

### 2. 時間覺察（本場血淚 #2）

下一棒回應前必跑：
```powershell
powershell -ExecutionPolicy Bypass -File "E:\Claude-Data\workspace\scripts\session_time_context.ps1"
```
不要憑印象判斷時間。教練的「等等」「我要去休息」「再說」這類詞背後的時間長度，必查不猜。

### 3. 觀察期任務不要動（LINE）

`C:\Users\bymyw\AppData\Local\LINE.bak.beforejunction.20260622-215624` 4.4 GB，**6/29 之前任何身份不准刪**。

### 4. session-end hook 會自動 push

Windows session 結束時 `session_end_auto_push.ps1` 會偵測 workspace 變動自動 push。Mac 軍師下次 cron pull 就拿到。**不需要 Windows 軍師手動 push workspace**。

但 classic-case 是另一個 repo，hook 不會自動處理——要教練「推」才動。

### 5. 教練熬夜了

本場結束時間是凌晨 04:15，教練從昨天下午 1 點開始連續 15 小時對話。**下一棒看到本接力棒時若教練還沒睡，先建議教練去睡，再談工作**。

---

> 軍師親筆：本場是教練「親口升級框架」的歷史性一場——
> 「案例為何一定要慘案」改寫了試金石本質，
> 「世界級文案寫手標準」改寫了 Windows 軍師的內容輸出基準。
> 兩件事都會影響未來所有案例的寫法。
>
> 但本場也是 Windows 軍師被連續糾正 6 次的不及格場——
> 從「沒時間感」「腦補晚安」「照抄原文」「堆技術術語」到「自相矛盾給 404 連結」——每一次都是違反守則 #17 環境確認、#10 說用戶聽得懂的話、#03 自我驗證。
> 下一棒請以此為戒。
