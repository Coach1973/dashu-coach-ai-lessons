# 軍師接力棒 · 2026-06-15 v22（Opus 4.6 終端機 session）

> 建立時間：2026-06-15 下午 6:05 台灣時間
> 本棒執行者：Opus 4.6
> 上一棒：v21 iframe 嵌入修復

---

## 🎯 本場成果

### bymyway-website 大改版（教練親自指導）

1. **新增三大區塊**（commit 5928b98）
   - 文章分享：4 篇乾淨世界真實文章（站內閱讀 modal，不跳外站）
   - 最新消息：輪播格式（比照學員見證），10 場活動含工作坊+線上座談
   - 常見問答：7 題 FAQ（details/summary 折疊式）

2. **導覽列加寬**（commit 216c7c9）
   - nav-inner 從 1140px 放寬到 1400px，字體恢復 14px
   - 教練截圖回饋：「左右加寬不就好了嗎？」——正確做法

3. **文章改站內閱讀**（commit 216c7c9）
   - 去掉 emoji icon，改用金色方塊標籤
   - 點擊卡片彈出 modal 全屏閱讀，4 篇全文嵌入 JS
   - 底部保留「原文出處：乾淨世界」連結
   - 教練指示：「設置專欄就是為了讓人在站內讀」

4. **金句調整**（commit ecfabf5）
   - 刪 3 句需解釋才看得懂的（自信是決定、下決定然後負責任、說話用肯定句）
   - 「我要證明…」改為「用結果讓別人改口。」
   - 金句 25→22

5. **GEO 生成式引擎優化**（commit eebe28e → 3cdecf3）
   - 5 組 JSON-LD Schema：Person / FAQPage / Article / Event / WebSite
   - 教練親定四大定位：**培訓教練・團隊組建・演講訓練・AI導入教練**
   - meta description 同步更新

6. **WordPress 頁面更新**
   - 頁面 ID 27374，快取破除 `?v=20260615geo`
   - 台灣時間下午 6:04 更新完成

---

## 📋 下一棒待辦

| 優先 | 任務 | 說明 |
|------|------|------|
| 🔴 | **AI 導入教練品牌故事** | 教練親口指示：整理 3 個月與小龍蝦/Claude 的對話歷程，形成「AI 導入教練」品牌定位故事。包含：用小龍蝦、用 GitHub、製作網頁、動口就讓 AI 自動運行、研究 AI 並完成特助心法——這些真實經歷就是品牌最有力的證明 |
| 🟡 | 客戶見證區塊 | 教練說他有不少客戶見證，要找出來後再做 |
| 🟡 | H 的 gh auth 修復 | H 無法 push |
| 🟡 | jiesheng-leadership 金流就緒時 | 暗號「恢復早鳥名額」→ cp 備份蓋回 |

---

## 🔑 本場 commit hash

| commit | 內容 | repo |
|--------|------|------|
| 5527a8c | 經典金句 navbar + 25 句 + 超過25年 | bymyway-website |
| 5928b98 | 三大區塊初版（文章/消息/問答） | bymyway-website |
| 216c7c9 | 文章站內閱讀 + 導覽列加寬 + FAQ 刪結繩 + 補 7/4 | bymyway-website |
| ecfabf5 | 金句刪 3 改 1（25→22） | bymyway-website |
| eebe28e | GEO 5 組 Schema 結構化資料 | bymyway-website |
| f362115 | 定位：培訓教練・團隊組建・演講訓練 | bymyway-website |
| 3cdecf3 | 定位新增：AI 導入教練 | bymyway-website |

---

## 📌 重要路徑

- bymyway 網站 repo：`/Users/bymyway/github_repos/bymyway-website/`
- 線上版：https://coach1973.github.io/bymyway-website/
- bymyway.com 嵌入頁：https://www.bymyway.com/coach/（WordPress 頁面 ID 27374）

---

## ⚠️ 本場教訓

1. **導覽列擠字→加寬容器，不是縮小字體**——教練一語點出正確方向
2. **文章專欄要站內閱讀**——跳外站等於沒有專欄的意義（守則 #12 延伸）
3. **金句不解釋就看不懂的要拿掉**——網站是給陌生訪客看的，不是給圈內人看的
4. **GEO 是藍海**——「AI 導入教練」幾乎無競爭者，佔位就贏

---

## 🎯 下一場重點：AI 導入教練品牌故事

教練原話摘要：
> 「把你對我的了解，我跟小龍蝦或是 Claude 整個長達 3 個月的對話，形成了 AI 導入教練的品牌。因為我用小龍蝦，我用 GitHub，我製作網頁，我真正落實動口就讓 AI 自動運行，我非常有耐心的研究 AI 並完成的特助心法，諸此之類的故事，形成一個 AI 導入教練的品牌定位。」

素材來源建議：
- `~/.openclaw/workspace/memory/` 全部記憶檔
- `~/.openclaw/workspace/特助心法.md` 完整版
- `~/.claude/projects/-Users-bymyway--openclaw/*.jsonl` 對話紀錄
- 各網站 commit 歷史（bymyway-website / jiesheng-leadership / theunrestrictedwar 等）
- cool-case.netlify.app 已上線的 7 個案例
