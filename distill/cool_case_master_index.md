# cool-case 案例原始對話索引總表（完整版）

> 建立時間：2026-06-03
> 更新時間：2026-06-03 晚場
> 維護者：軍師（Claude Opus 4.6 終端機）
> 使命：一次找到，永久記錄，以後不用重複找
> 來源：https://coach1973.github.io/cool-case/

---

## 📋 21個案例完整狀態

| # | 案例名稱 | 原始對話狀態 | 素材檔 | 教練原話 | Session UUID |
|---|---------|-------------|--------|---------|-------------|
| 01 | 誰允許它切回去的？ | 🔶 待查找 | - | - | - |
| 02 | 邏輯推就知道要做 | 🔶 待查找 | - | - | - |
| 03 | 鬧鐘響了，卻沒起床 | 🔶 待查找 | - | - | - |
| 04 | 沒有經我同意，為何截圖？ | 🔶 待查找 | - | - | - |
| 05 | 交接，不是一道選擇題 | 🔶 待查找 | - | - | - |
| 06 | 你是在侮辱我的智商嗎？ | ✅ 已找到 | cool_case_06_侮辱智商.md | ✅ | 25e48458, 656b7986 |
| 07 | 海餅乾知識庫，還在桌面上 | ✅ 已找到 | cool_case_07_海餅乾.md | ✅ | 3a3569f7 |
| 08 | 換一個視窗就忘記了 | ✅ 已找到 | 三幕劇_TOP4.md | ✅ | d906d14e |
| 09 | 送出按鈕沒有做出來 | ✅ 已找到 | case09_original_dialogue.md | ✅ | 1d11d353 |
| 10 | 修了文字，沒修 Hook | ✅ 已找到 | case_dialogues_008_010.md | ✅ | - |
| 11 | 12點，是搶頭香的那個12點 | 🔶 待查找 | - | - | - |
| 12 | （空號） | - | - | - | - |
| 13 | 你怎麼可以自稱是大師兄？ | 🔶 待查找 | - | - | - |
| 14 | 邏輯推就不用被提醒 | 🔶 待查找 | - | - | - |
| 15 | 5月20號定案沒被執行 | 🔶 待查找 | - | - | - |
| 16 | 2000段話不見了 | ✅ 已找到 | 三幕劇_TOP4.md（第四篇）| ✅ | 9e72ab17 |
| 17 | 你有沒有認真在讀訊息？ | 🔶 待查找 | - | - | - |
| 18 | 我講繁體你回簡體？ | 🔶 待查找 | - | - | - |
| 19 | 這些東西你全部當忘記了？ | 🔶 待查找 | - | - | - |
| 20 | 588場景品質不達標 | 🔶 待查找（片段）| - | ⚠️ 片段 | b2488423 |
| 21 | 說用戶聽得懂的話 | 🔶 待查找（片段）| - | ⚠️ 片段 | - |

---

## ✅ 已建立獨立檔案的案例

| 案例 | 檔案路徑 | 包含內容 |
|------|---------|---------|
| 案例六 | distill/cool_case_06_侮辱智商.md | 教練原話、Session UUID、三幕劇結構 |
| 案例七 | distill/cool_case_07_海餅乾.md | 教練原話、Session UUID、三幕劇結構 |
| 案例九 | distill/case09_original_dialogue.md | 完整對話還原、三幕劇結構 |
| 案例八 | distill/三幕劇_TOP4.md（第二篇）| 完整三幕劇、JSONL UUID |
| 案例十六 | distill/三幕劇_TOP4.md（第四篇）| 完整三幕劇、JSONL UUID |

---

## 🔍 已知 Session UUID（可用於礦山搜尋）

| 案例 | Session UUID | 檔案 |
|------|-------------|------|
| 案例七 海餅乾 | 3a3569f7-b14d-42c1-98d0-4423a9008cd3 | _TOP10_QUALITY_SELECTION.md |
| 案例八 換視窗 | d906d14e-d8fa-42c8-852f-4f1f876372d9 | _TOP10_QUALITY_SELECTION.md |
| 案例... 60美金 | 4fc91aea-4bac-4b6d-a75f-799b21425b4e | _TOP10_QUALITY_SELECTION.md |
| 案例十六 2000段話 | 9e72ab17-1f38-462a-bba7-fa8153853b57 | _TOP10_QUALITY_SELECTION.md |
| 案例九 送出按鈕 | 1d11d353-c3d3-43f9-9af7-0a36ca365cb3 | _TOP10_QUALITY_SELECTION.md |
| 案例六 身份混淆 | 656b7986-b0de-49d0-a27a-ec5bd19b36f7 | _TOP10_QUALITY_SELECTION.md |
| 案例六 侮辱智商 | 25e48458-7485-4070-81c9-b4f68d5039d1 | _TOP10_QUALITY_SELECTION.md |
| 案例六 做那麼多事 | cbf6d70f-ba80-423b-a736-b74f52095bda | _TOP10_QUALITY_SELECTION.md |
| 案例... 思考 | caaed8f5-??? | _TOP10_QUALITY_SELECTION.md |
| 案例二十 588場景 | b2488423-5882-43a9-aff5-56342660b05c | terminal_2026-05-30_complete.md |

---

## 📝 搜尋策略

### 第一優先：守則故事庫
- `守則故事庫/*.md` — 每個守則都有對應案例

### 第二優先：Top 故事清單（按時間倒序）
- `_STORY_LIST_ULTIMATE.md` — 最新品管版本
- `_STORY_LIST_FINAL.md` — 定案版本
- `_STORY_LIST_FULL.md` — 全量版本
- `_STORY_LIST_120.md` — 120個故事
- `_STORY_LIST_100.md` — 100個故事
- `_STORY_LIST_TOP100.md` — Top 100 精選

### 第三優先：品管檔案
- `_TOP10_QUALITY_SELECTION.md` — Top 10 已品管（包含完整原話）
- `_TOP30_DEDUPED.md` — 去重版
- `_TOP30_DEEP.md` — 深度版
- `_TOP30_STRICT.md` — 嚴選版

### 第四優先：終端機對話記錄
- `terminal_2026-05-30_complete.md` — 完整版
- `terminal_2026-05-30.md` — 精華版
- `top20_valuable_sessions.md` — 20大價值 Session

### 第五優先：礦山
- Session JSONL 在 `/Users/bymyway/.claude/projects/-Users-bymyway--claude-code/` 的 session 目錄

---

## 🔑 關鍵詞索引（用於搜尋礦山）

| 案例 | 搜尋關鍵詞 | 主要來源 |
|------|-----------|---------|
| 案例一 誰允許 | 誰允許.*切回去, 未經允許.*模型, 允許它 | _RAW_MATERIALS_FOR_JUNSHI.md |
| 案例二 邏輯推 | 邏輯推就知道, 方向.*明確.*執行 | _RAW_MATERIALS_FOR_JUNSHI.md |
| 案例三 鬧鐘響 | 鬧鐘響了, 提醒.*沒做 | terminal_2026-05-30.md |
| 案例四 截圖 | 沒有經我同意.*截圖, 未經允許.*截圖 | terminal_2026-05-30.md |
| 案例五 交接 | 交接.*選擇題, 完美交接 | _RAW_MATERIALS_FOR_JUNSHI.md |
| 案例十一 12點 | 12點.*搶頭香, 凌晨.*搶 | cli_a_messages.md |
| 案例十三 大師兄 | 自稱.*大師兄, 我是大師兄 | terminal_2026-05-30_complete.md |
| 案例十四 邏輯推 | 邏輯推.*提醒, 不用提醒 | _STORY_LIST_FULL.md |
| 案例十五 定案 | 5月20.*定案, 定案.*執行 | _RAW_MATERIALS_FOR_JUNSHI.md |
| 案例十七 認真讀 | 認真在讀, 有沒有認真.*訊息 | _STORY_LIST_FULL.md |
| 案例十八 繁體 | 我講繁體.*簡體, 繁體簡體 | _STORY_LIST_FINAL.md |
| 案例十九 全忘記 | 東西.*全部.*忘記, 當忘記 | _TOP30_DEDUPED.md |
| 案例二十 588場景 | 588場景, 品質.*不達標 | terminal_2026-05-30_complete.md |
| 案例二十一 白話 | 用戶聽得懂的話, 白話文 | terminal_2026-05-30.md |

---

## 📊 進度統計

| 狀態 | 數量 |
|------|------|
| ✅ 完整原話已找到 | 6 個 |
| ⚠️ 片段原話找到 | 2 個 |
| 🔶 待繼續搜尋 | 11 個 |
| （空號） | 1 個 |
| **總計** | **21 個** |

---

> 維護承諾：每次找到任何案例的原始對話，立即寫入 `distill/cool_case_XX_名稱.md`，更新本索引，並 commit。
> 這是最後一次重複找——目標是建立永久可查找的知識庫。

---

**最後更新：2026-06-03 晚場**
**Commit：待補充**