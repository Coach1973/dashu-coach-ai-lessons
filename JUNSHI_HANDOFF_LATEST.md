# 軍師接力棒 · 2026-06-14 v20（Opus 4.6 終端機 session）

> 建立時間：2026-06-14 下午 2:36 台灣時間
> 本棒執行者：Opus 4.6
> 上一棒：v19 任務橋＋快取清理＋SOP 更新

---

## 🎯 本場成果

### 1. 超限戰網頁完整復原＋部署（commit 9669ecd）
- theunrestrictedwar.netlify.app 從精簡版復原為歷史典藏版
- 內容：首映週（5/22-5/28）＋ 續映週（5/29-6/04）＋ 9 張企業贊助號外全部找回
- 部署方式：zip + Netlify API（手動上傳型）
- Netlify token 記憶檔已更正

### 2. 個人品牌網站改版（commit 9830c42，已推 GitHub Pages）
- Repo：`/Users/bymyway/github_repos/bymyway-website/`
- 線上版：https://coach1973.github.io/bymyway-website/
- 教練方向：**專注個人品牌，拿掉 AI 相關內容**
- 已完成：
  1. 品牌金句：AI 語錄 → 海餅乾語錄「你是誰，決定了別人怎麼看你」
  2. 身份標籤：「頂級特助系統創建者」→「人才培育系統創辦人」
  3. 企業演講：「AI 落地與自動化」→「品德教育與傳統文化」
  4. **新增「創業歷程」時間軸**（1997～2024，14 筆教練完整簡歷）
  5. **新增「智慧語錄」輪播**（19 句金句，來源：`~/Downloads/海餅乾語錄.docx`）
     - 左右箭頭＋底部翻頁＋圓點導航
     - 電腦 3 張、平板 2 張、手機 1 張
  6. 導覽列加了「創業歷程」連結
- HTML 預覽已在桌面：`~/Desktop/bymyway-preview.html`

### 3. Windows 桌面版 Claude 讀取 GitHub 設定
- 提供 MCP GitHub Server 設定格式
- 用 `gh auth token` 取得現有 token

---

## 📋 下一棒待辦

| 優先 | 任務 | 說明 |
|------|------|------|
| 🔴 | bymyway 網站繼續改版 | 教練看完後根據回饋調整；可能加更多語錄、加客戶見證（教練說會提供） |
| 🟡 | 客戶見證區塊 | 教練說他有不少客戶見證，要找出來後再做 |
| 🟡 | H 的 gh auth 修復 | H 無法 push |
| 🟡 | jiesheng-leadership 金流就緒時 | 暗號「恢復早鳥名額」→ cp 備份蓋回 |

---

## 🔑 本場 commit hash

| commit | 內容 | repo |
|--------|------|------|
| 9669ecd | 超限戰網頁完整復原 | theunrestrictedwar |
| 9830c42 | 個人品牌網站改版（去AI＋時間軸＋語錄輪播） | bymyway-website |
| 8831ed36 | 接力棒 v20 首版 | mac-openclaw-workflows |

---

## 📌 重要路徑

- bymyway 網站 repo：`/Users/bymyway/github_repos/bymyway-website/`
- 海餅乾語錄：`~/Downloads/海餅乾語錄.docx`（金句素材，19 句已用，可能還有更多）
- 官方網站：www.bymyway.com（七大公開課程、服務單位等參考）
- 超限戰 repo：`/Users/bymyway/github_repos/theunrestrictedwar/`
- 網頁推 SOP：`~/.openclaw/workspace/knowledges/SOP_netlify_website_edit.md`

---

## ⚠️ 本場教訓

1. theunrestrictedwar 是手動上傳型——SOP 寫死禁止 git push 部署
2. Netlify token 查路徑大全，不信記憶檔舊版
3. HTML 預覽放桌面是 SOP——App 裡的預覽看不清楚
