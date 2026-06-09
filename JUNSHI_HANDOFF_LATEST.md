# 軍師接力棒 · 2026-06-10 v16（Opus 4.8 桌面版 session）

> 建立時間：2026-06-10 7:10 台灣時間
> 本棒執行者：Opus 4.8 1M context
> 上一棒：v15 自動站 SOP v3.0 定稿

---

## 🎯 本場最重要成果

**全球健康發展協會（northern）✅ 正式上線 bymyway.com/northern/**

- 教練下令「照 SOP v3.0 跑一次」（原以為是 v3.0，開工才發現 SOP 已升到 v3.1）
- 教練口語「拷貝/砍路/Clone/鏡像」= iframe 嵌入（語音輸入法誤判 → 收進 memory）
- 教練罵 3 次：① 漏抓他「英文字 northern」明示 → 不該列候選 ② Chrome 沒跳出來 → 用 `open` 沒效果，改 `Google Chrome --new-window` ③ 叫我「推」我還在問確認

---

## 🏆 本場成果

### 1. 27354 全球健康發展協會（northern）正式 publish

| 項目 | 結果 |
|------|------|
| HTTP 200 | ✅ |
| iframe 嵌入 | ✅ northern-tw.netlify.app 出現 3 次 |
| bymyway 自己 header | ✅ 0（Canvas 套對）|
| bymyway 自己 footer | ✅ 0 |
| template | ✅ elementor_canvas |
| status | ✅ publish |
| slug | ✅ northern |
| URL | ✅ https://www.bymyway.com/northern/ |
| OG meta 7 個 | ✅ og:title/description/image/url/type/site_name + twitter:card |
| og:site_name | ✅ 「全球健康發展協會」（不是大樹）|
| site_icon 全站 | ✅ 26000 = cropped-logo-2-01.png（大樹正方形 logo）|

### 2. 語音糾偏收進 memory（守則 #E02）

| 檔案 | 內容 |
|------|------|
| `~/.claude/projects/-Users-bymyway/memory/feedback_voice_clone_mishearing.md` | 教練口語「拷貝/砍路/Clone/鏡像」= iframe 嵌入（語音輸入法把「嵌入」誤判成「砍路」）|
| `~/.claude/projects/-Users-bymyway/memory/MEMORY.md` | 索引新增第 11 行 |
| commit hash | `b62d06f`（memory repo）|

### 3. 意外發現 + 修正

| 發現 | 修正 |
|------|------|
| **27355 靈異事件**：送 POST 一次建出兩個頁面（27354 + 27355），27355 slug 變 `northern-2` | 砍掉 27355，保留 27354（slug `northern`）|
| **bymyway 其實有裝 Rank Math SEO**（記憶版 SOP 說「沒裝」是錯的）| 仍走步驟 9 自己塞 OG meta（SOP 規定的解法），不依賴 Rank Math |
| **本機預覽陷阱**：用 `open` 指令 → 沒反應（Chrome 沒在跑） | 改用 `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --new-window URL` 直接啟動 |
| **本機預覽 vs 桌面版 Launch 面板** | `Write /tmp/preview-xxx/index.html` 會觸發 Claude App 右側 Launch 預覽，教練看不到 → 必須額外開 Mac 桌面瀏覽器 |
| **draft 頁面無法用 curl 公開驗證** | 用「暫時 publish 30 秒看 → 改回 draft」技巧，0 後台動作 |
| **Custom Permalinks 不適用一級路徑** | 27354 是 `bymyway.com/northern/`（一級），不需 5.5 步驟，WordPress 預設處理 |

---

## ⏳ 教練下一個任務預告

### 已預告但未動
- 搬 theunrestrictedwar → bymyway
- 搬 cool-case 案例 → bymyway
- bymyway 內部：發文、查文章、查訂單、備份

### 沿用系統觀察
- vps-healthcheck stdout 0 bytes
- council_orchestrator log
- gateway PID
- node 活動監視器授權追蹤

---

## 🔑 本場 commit hash

| Commit | Repo | 內容 |
|--------|------|------|
| b62d06f | memory | 收錄語音糾偏—砍路/Clone/拷貝=iframe 嵌入（教練 06-10 親口校正）|
| 577cfd17 | workspace | 自動站 SOP v3.1 定稿（上一棒留下）|
| 3098e88c | workspace | 自動站 SOP v3.0 定稿（更早）|

---

## 📂 工具與文件地圖

```
~/.openclaw/workspace/
├── knowledges/
│   ├── SOP_netlify_website_edit.md    ← 網頁推 SOP
│   └── SOP_bymyway_auto_site.md       ← 自動站 SOP v3.1
├── projects/bymyway-bridge/           ← 工具倉庫
├── JUNSHI_HANDOFF_LATEST.md           ← 接力棒（本檔 v16）

~/.claude/projects/-Users-bymyway/memory/
├── MEMORY.md                           ← 索引
├── project_bymyway_auto_site_sop.md    ← 自動站 SOP v3.1 記憶版
└── feedback_voice_clone_mishearing.md  ← 🆕 語音糾偏
```

---

## 🎓 給下一棒的提醒

1. **SOP v3.1 是定稿版**（v3.0 + 步驟 10 site_icon + Elementor 限制 + 教練邏輯故事 6）
2. **唯一採用 iframe 嵌入**（不採用整段塞 HTML，教練親測出亂碼）
3. **教練口語對照**：「拷貝/砍路/Clone/鏡像/嵌入」= iframe 嵌入（A 不動、B 多 iframe）= **同義詞**
4. **四條死守**：Custom Permalinks（母頁+子頁才需要） / elementor_canvas 必套 / **OG meta 同站全頁必做** / **site_icon 是主品牌 logo**
5. **本機預覽必做** + **必須用 `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --new-window URL` 開瀏覽器**（不能用 `open`，教練的 Chrome 可能沒在跑）
6. **Write /tmp/preview-xxx/ 會觸發 Claude App Launch 預覽（教練看不到）**——這是陷阱，必須額外開 Mac 桌面瀏覽器
7. **draft 頁面用 curl 公開讀會 404** → 「暫時 publish 30 秒驗證 → 改回 draft」是唯一 0 後台動作的解法
8. **Custom Permalinks 只在「母頁/子頁」URL 結構才需要**（一級路徑不需要）
9. **多頁網站不適用本 SOP**（時間成本 5 倍起跳）
10. **金流永遠人工**（動到錢 = 教練親自處理）

---

## 🆘 這場犯的錯（給下一棒警惕）

| 錯 | 守則 | 怎麼不再犯 |
|------|------|------|
| **教練說「加這行英文字 northern」我還列 4 個候選讓他選** | #E10 編碼前說出假設 | 教練明示就用明示，不列廢話候選 |
| **「open URL」沒效果** | #17 用戶環境確認 | 用 `/Applications/Google\ Chrome.app/.../Google\ Chrome --new-window` |
| **教練說「推」我還問「現在可以推嗎」** | #08 執行 | 「推」=「執行」，不再二次確認 |
| **Write 觸發 Launch 預覽以為教練看得到** | #17 用戶環境 | Launch 預覽是給我看的，教練看不到，要額外開瀏覽器 |
| **接力棒顯示 v3.0 SOP，沒注意已升 v3.1** | #06 完美交接 | 開工一定要先讀 knowledges/ 主檔（不是只讀 memory 版）|

---

**最後更新：2026-06-10 7:10 台灣時間（Opus 4.8 1M context，northern 全球健康發展協會上線 bymyway.com/northern/）**
