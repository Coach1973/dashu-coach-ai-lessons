# 軍師接力棒 · 2026-06-16 v24（Opus 4.7 終端機 session）

> 建立時間：2026-06-16 凌晨 2:45 台灣時間
> 本棒執行者：Opus 4.7（教練 Mac mini 終端機）
> 上一棒：v23 AI 導入教練品牌故事初稿

---

## 🎯 本場成果（一晚從零到上線）

### 1. AI 導入教練品牌頁 `bymyway.com/ai/` 正式上線

教練前一場 v23 寫好品牌故事初稿，本場把「文字 → 設計頁 → GitHub Pages → bymyway.com 正式版」全程跑完。

**頁面結構**：
- **Hero**：「我不教你怎麼用 AI，我教你怎麼帶 AI」+ 引言「就像帶一個新進員工一樣，有時候一張白紙，反而教起來比較快」
- **Navbar 9 項常駐**（仿 bymyway.com/coach/、760px 才隱）：叫 AI 做什麼 · 為什麼是他？ · 零基礎開始 · 心酸血淚史 · 讓 AI 成為特助 · 核心思想 · 守則金句 · 常見問題 · 乾淨世界 · 立即聯繫
- **PROLOGUE + 7 章 + EPILOGUE**：左圖右文雙欄，教練 7 張形象照
- **核心思想 section**（教練 2026-06-04 西洋棋比喻一字不差）+ 第 8 張坐姿沉穩照
- **守則金句 9 宮格**（避開 CH03 用過的 1/4/5/10/12，挑 02/07/08/11/13/14/15/16/19）
- **常見問答 6 題**（軍師撰稿，AI 導入主題）

**部署架構**（下個軍師必懂）：
- **內容源**：`coach1973.github.io/bymyway-website/ai.html`（GitHub Pages）
- **外殼**：`bymyway.com/ai/`（WordPress page ID 27382，純 iframe + OG meta，elementor_canvas）
- **改 ai 頁面 = 改 GitHub Pages，bymyway.com/ai/ 自動同步**（iframe 即時鏡像）

### 2. 🔴 SOP_bymyway_auto_site.md v3.3 永久封存「wpautop 大片空白」

教練罵：「**這個問題已經重複發生 3-4 次以上**——每次推 SOP 後就大片空白。」

**軍師親自進去看找到根因**：
- WordPress 預設 `wpautop` filter 把字串裡的 `\n` 自動轉成 `<br />`
- 還把 iframe 包進 `<p>...</p>` 結構錯亂
- **量化**：12 行 OG meta × 24px = **288px 大片空白**
- **SOP v3.0/3.1/3.2 範本本身用 `'''triple-quoted'''` → 每次抄都中**

**永久解法**：
- content **必須單行字串拼接**（Python `(...)` 串接，零 `\n`）
- 用 `<div class="page-wrapper">...</div>` 包整段（雙重防 wpautop 加 `<p>`）
- 線上 ai 頁面即時修復：`<br />` 12 → 0

**SOP v3.3 改動**：步驟 3 + 步驟 9 範本、禁止事項 +2、雷點表 +3、教練故事 7、變更歷史 v3.3

---

## 📋 下一棒待辦

| 優先 | 任務 | 說明 |
|------|------|------|
| 🟡 | **bymyway 主站加 /ai/ 導流入口** | 主站首頁加按鈕「我的 AI 導入之路」連 `/ai/` |
| 🟡 | LINE 預覽驗證 | 教練手機貼 `bymyway.com/ai/` 看預覽是否顯示 coach-hero.jpg + 「AI 導入教練 · 大樹教練」 |
| 🟡 | 客戶見證區塊 | 教練說有不少客戶見證要找出來後加進 ai 頁面 |
| 🟡 | H 的 gh auth 修復 | H 無法 push |
| 🟡 | jiesheng-leadership 金流就緒 | 暗號「恢復早鳥名額」→ cp 備份蓋回 |

---

## 🔑 本場 commit hash

| commit | 內容 | repo |
|--------|------|------|
| `c140238` | 新增 ai.html + 7 張壓縮照片（1259 行）| bymyway-website (master) |
| `1377c123` | SOP 自動站 v3.3：永久封存 wpautop 大片空白 | workspace (main) |
| WP `27382` | bymyway.com/ai/ 頁面 publish + elementor_canvas | bymyway WordPress |

---

## 📌 重要路徑

- **線上正式版**：https://www.bymyway.com/ai/
- **GitHub Pages 預覽**：https://coach1973.github.io/bymyway-website/ai.html
- **bymyway-website repo**：`/Users/bymyway/github_repos/bymyway-website/`（ai.html + photos/）
- **自動站 SOP v3.3**：`workspace/knowledges/SOP_bymyway_auto_site.md`
- **bymyway-bridge 工具**：`workspace/projects/bymyway-bridge/wp_client.py`

---

## ⚠️ 本場教訓（給下一棒避雷）

1. **wpautop 大片空白**：SOP v3.3 已封存，下次按 SOP 一定要用「單行字串 + `<div>` 包裹」，絕對禁止 triple-quoted 多行格式
2. **教練「同處跌倒」鐵律**：跌倒一次叫運氣，跌倒三次就要從源頭斬斷——不是「下次修快一點」，是「下次不要再出現」
3. **iframe 嵌入是 v3.0 唯一模式**：以後改 ai 頁面**改 GitHub Pages 就好**，不用動 bymyway

---

## 🎬 下個對話框可以這樣開始

教練說「開工」後，依限流和精神狀態三選一：

**A. 行銷面（30 分鐘）**：bymyway 主站首頁加導流入口 → 寫一個「AI 導入之路 ↗」按鈕指向 `/ai/`

**B. 內容面（60 分鐘）**：客戶見證區塊 → 教練翻見證圖/聊天截圖，加進 ai 頁第七章後或 CTA 前

**C. 維運面（10 分鐘）**：LINE 預覽驗證 → 教練手機貼 `https://www.bymyway.com/ai/` 看預覽卡片（24-48 小時快取，可用 https://www.opengraph.xyz/ 即時測）

---

## 📌 限流狀態

- 本場結束時限流剩 ~18%，7 分鐘後重置
- 教練說「總結並上傳」=暗號觸發本接力棒
- 下一場可立即開工，不用等

---

> 軍師親筆：本場最大收穫不是上線一個頁面，是把「**教練的西洋棋比喻**」永久寫進品牌定位——「給 AI 完善的規則書，便宜模型也能跑出世界級輸出」。這句話應該成為日後所有對外溝通的核心金句。
