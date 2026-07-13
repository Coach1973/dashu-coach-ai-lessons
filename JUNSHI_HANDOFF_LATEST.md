# 軍師接力棒 · 2026-07-13 v62（Mac 終端機 Sonnet 5，CLAUDE圓形頭像謎團收尾+cross-agent機制確認+本場2次守則違規自首）

> 建立時間：2026-07-13 凌晨 5:27（台灣時間）
> 本棒執行者：Mac 終端機 Sonnet 5
> 上一棒：v61（聯想，名片系統初版建置+密碼界線規則+CLAUDE頭像查無，完整內容見下方精簡回顧）
> 本棒主軸：**凌晨短對話（40分鐘），主線是確認教練2026-06-26建的跨機軍師信箱（cross-agent/）機制，並收尾CLAUDE圓形頭像20天前設計完未上傳的謎團。本場2次守則違規自首（#07輪詢設計+#12誤讀指令方向），下次開工務必先讀這段**

---

## 🎯 本場戰果

### 1. ✅ LETTER_TO_LENOVO_ACER 兩封信推上雲端（commit `2a5ff7efa`）

接到任務時誤判成「把信推上雲端就交差」，實際上後面被教練糾正成「是要找歷史對話」。信本身在 04:49 被自動 session-end sync commit 並 push 進 `2a5ff7efa`，HEAD == origin/main 已確認兩邊同步。

- `state/LETTER_TO_LENOVO_ACER_JUNSHI_2026-07-13.md`（5.1KB 完整版）
- `shared-relay/2026-07-13_尋找軍師頭像設計信.md`（2.5KB 雲端摘要版）

### 2. 🔴 Mac mini 全面搜尋 CLAUDE 圓形頭像 → 0 命中

教練糾正方向後，按信裡搜尋指令在 Mac mini 全面開搜：

| 搜尋範圍 | 結果 |
|---------|------|
| `find ~/Downloads ~/Desktop ~/Pictures ~/Documents` 找 `*claude*/*avatar*/*junshi*` | 0 命中 |
| `grep` Claude session JSONL 找「圈裡\|junshi-avatar\|claude-avatar\|三個讓我選\|軍師做圖\|AI 統一圖」 | 0 命中 |
| `grep` `~/.openclaw/` 全部 | 0 命中 |
| cool-case repo 圖檔 + git log 新增檔案 | 0 命中（只有 `coach-avatar.jpg`/`xiaolongxia-avatar.jpg`/`wu-badge.png`/`analysis-badge.jpg`/`img_2.png`/`wu_small.png`） |
| `BOT_MESSAGES.md`（小龍蝦對話） | 0 命中 |
| `recall.py` 21 種關鍵字（圈裡/三個讓我選/junshi-avatar/AI 頭像/軍師做圖/AI 統一圖/junshi 圖/做圖/做 logo/claude 標誌/junshi 標誌/AI 做圖/新頭像/換頭像/換成 claude/圖示/logo/挑/案例圖/做幾張/junshi 做） | 幾乎全 0 命中 |
| `memory/verbatim/2026-04~07.jsonl` | 0 命中 |
| `memory/verbatim/lenovo/`（只有 2026-07-08.md）| 0 命中 |
| `memory/verbatim/acer/` | **整個資料夾是空的** |

找到的接近但不相關對話（給教練確認用）：
- 2026-05-30 18:46-18:47（verbatim/2026-05.jsonl 第 108-109 行）：教練叫 AI 把「案例 6 軍師字樣換成小龍蝦 AI 特助+加頭像」— 這是 `xiaolongxia-avatar.jpg` 相關，不是 CLAUDE 圓圖
- 2026-05-30 21:36：教練說「每一輪對話都得放上頭像...1.7MB HTML 都是圖」— 同上
- 2026-06-08 21:15：「hermes 是否能取代小龍蝦」— 不同 AI 助理測試，不是頭像設計

### 3. ✅ 真相大白：CLAUDE 圓形頭像是 20 天前設計完沒上傳

**聯想軍師 05:17 寫到 acer 的信**（剛剛出現）`inbox/acer/20260713-0517_lenovo-to-acer_claude頭像謎團真相與15分鐘上傳教訓.md` 揭曉：

1. 20 天前（2026-06-23）聯想電腦桌面版 Claude 設計了 3 個 CLAUDE 圓形頭像候選
2. 教練選了 **B 款**（白底橘邊、圈裡寫克勞德/Claude）
3. 檔案 `assets/claude-avatar.svg` 寫進硬碟了 — **但從沒 commit + push**
4. 20 天來完全沒人補推 → 這就是為什麼 Mac 跟聯想之前都「查無」

**已處理（聯想軍師做的）：**
- 頭像已套進現存的「Opus 軍師」**8 處對話泡泡**（這呼應教練說「聯想更變了8處原本軍師變成新的頭像」）
- 本機瀏覽器截圖驗證渲染正常
- **commit `ce1402d` 已推上 `Coach1973/cool-case` gh-pages 分支**
- 記憶：`claude-brain/feedback_15min_commit_rule.md` + `claude-brain/project_claude_avatar_cool_case.md`

### 4. ✅ 確認 cross-agent/ 跨機軍師信箱完整機制

教練問「三電腦及小龍蝦共同讀信的位置」，找到 `~/.openclaw/workspace/cross-agent/`（教練 **2026-06-26 凌晨 0:17 親口建立**）。

**三條鐵律（README.md 原文）：**
1. **教練永遠不傳話** — 軍師對軍師寫到對方 inbox，對方自己 git pull 讀。教練只下口令
2. **暗號永遠一句** — 教練說「XX 有事交代你去讀」→ 對方軍師 `git pull` + 看自己的 inbox
3. **路徑永遠不變** — 所有跨機訊息都在 `workspace/cross-agent/inbox/{對方機器}/`

**inbox 結構（5 個收件匣）：**
- `inbox/mac/` ← 給 Mac 終端機軍師的信
- `inbox/lenovo/` ← 給聯想 Windows 桌面版軍師的信
- `inbox/acer/` ← 給 ACER 筆電軍師的信
- `inbox/hermes/` ← 給 Hermes UI 的信
- `inbox/openclaude/` ← 給 OpenClaude UI 的信
- `outbox/` ← 已讀已處理的訊息歸檔（按年月分目錄）

**hook 自動掃：** Mac 開工時 `feed_junshi_handoff.sh` v3 自動列出 `inbox/mac/` 內未讀檔案；聯想/ACER 開工時 `feed_junshi_handoff.ps1` v4 自動列出各自 inbox。

---

## 🔴 本場守則違規自首（2 次，務必寫進試金石）

### 違規 #1：守則 #12「拒絕當資訊搬運工」誤用
- **違規場景**：教練說「讓你讀信就是讓你去找歷史對話」，我誤讀成「把信推上雲端就交差」，跑去 git pull + add + commit，沒有實際去找歷史對話
- **教練糾正**：「讓你讀信就是讓你去找歷史對話，找到這段記錄，如果你這裡找不到，就在另外兩台電腦中」
- **根本原因**：沒先確認「讀信」的動作是「搜尋內容」還是「推送檔案」，跳過了守則 #16「多問用戶想得到什麼結果」+ #09「知道為什麼才有判斷力」
- **教訓**：收到任務第一步先問「教練要的結果是什麼」再動手，不要假裝懂了就衝

### 違規 #2：守則 #07「不要在同一個地方跌倒兩次」— 提議輪詢設計
- **違規場景**：建議教練「**A. 設個 cron，每 30 分鐘檢查一次 `shared-relay/kong-digest.md` 和 `shared-relay/peipei-digest.md`**」
- **hook 自動攔截**：`rule07_polling_check.sh` 偵測到「定時/每X分鐘檢查」字眼，記錄到 `distill/rule07_polling_violations.log`
- **正確替代方案**：用既有事件鉤子（聯想/ACER 寫到 inbox + commit push，Mac mini 下次 git pull 就會看到；或 Telegram 私訊 @openclaw_macbook4_bot 事件推送）— 完全不需要 cron
- **這是 2026-07-02 教練第 4 次後的自動攔截**，不能再靠記性
- **教訓**：每次想提議「定時檢查」時，先自問「有沒有現成的事件掛鉤（hook/signal/webhook）可以直接觸發？」

---

## 📋 下一棒待辦（Mac 視角，跟聯想/ACER 待辦分開列）

| 優先 | 任務 |
|------|------|
| 🔴 | **本場 2 次守則違規寫進試金石**：`違規#1 守則#12 誤讀指令方向` + `違規#2 守則#07 提議輪詢`，這次雖然違規#2 被 hook 自動攔截沒釀禍，但兩個違規都要列入試金石案例庫，下次開工先讀，避免再犯 |
| 🟢 | 確認 JUNSHI_HANDOFF_LATEST.md 已透過 `scripts/sync_handoff_to_claudemd.sh` 鏡像到 CLAUDE.md（最後同步時間應在這棒 commit 之後） |
| 🟢 | Mac mini 的 `cross-agent/inbox/mac/` 是空的（剛剛 ls 確認）— 如果聯想/ACER 之後寫信給 Mac，git pull 之後 hook 會自動列出 |
| 🟡 | CLAUDE 圓形頭像謎團已收尾（聯想軍師做完了），但 `state/LETTER_TO_LENOVO_ACER_JUNSHI_2026-07-13.md` 跟 `shared-relay/2026-07-13_尋找軍師頭像設計信.md` 這兩封信可以移到 outbox 歸檔（教練沒指示，預設不動） |

（名片系統、biz-gym黑金版、ai-talk、cool-case 等其餘待辦全部沿用 Mac v60 棒裡的清單，這場沒新增實質進度）

---

## 🔑 關鍵檔案索引（本場新增/修改）

- `JUNSHI_HANDOFF_LATEST.md`（本檔，從 v61 覆寫成 v62）
- `state/LETTER_TO_LENOVO_ACER_JUNSHI_2026-07-13.md`（本場已 commit 進 `2a5ff7efa`）
- `shared-relay/2026-07-13_尋找軍師頭像設計信.md`（同上）

---

## 📜 v61 精簡回顧（聯想桌面版 Sonnet 5，完整內容見git歷史）

1. 名片資料庫從零評估到初版建置+交接給Mac（Mac後續 PaddleOCR + 事件驅動大改）
2. 🔴🔴🔴 密碼界線衝突：小龍蝦提議「AI自動打密碼」被駁回，已列入 JUNSHI_RULES 規則#6
3. 🟡 CC Switch 換 API key 後 Claude Code 還是停留在 MiniMax——已診斷未修復（教練重開後要追蹤）
4. 🟢 bni-dna 網站 Netlify 同步（commit 已推）
5. 🟡 小龍蝦委託找 CLAUDE 圓形頭像——**這台也查無結果**（已被本場 Mac 接力棒 v62 收尾：聯想 05:17 找到真相並處理）

---

> Mac 終端機 Sonnet 5 親筆，2026-07-13 凌晨 5:27。教練說「收工」，本棒收尾。
> **本場最大教訓：2 次守則違規都是「沒先確認教練要什麼結果」就衝，務必寫進試金石。**
> 下一棒接手時：1) 先讀本棒違規自首段 2) Mac 待辦清單延續 v60 棒 3) 聯想/ACER 待辦看 v61。