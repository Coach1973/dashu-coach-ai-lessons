# 軍師接力棒 · 2026-06-14 v20（Opus 4.6 終端機 session）

> 建立時間：2026-06-14 下午 2:05 台灣時間
> 本棒執行者：Opus 4.6
> 上一棒：v19 任務橋＋快取清理＋SOP 更新

---

## 🎯 本場成果

### 1. 超限戰網頁完整復原＋部署（commit 9669ecd）
- theunrestrictedwar.netlify.app 從精簡版復原為歷史典藏版
- 內容：首映週（5/22-5/28）＋ 續映週（5/29-6/04）＋ 9 張企業贊助號外全部找回
- 從 git 歷史 commit `95e13ab` 挖出完整版，與最新版合併
- 部署方式：zip + Netlify API（手動上傳型，不是 git push）
- ⚠️ 本場踩雷：先用 git push（無效）、記憶裡的 Netlify token 少字元（401）→ 查路徑大全找到正確 token 修正
- 記憶檔 `reference_netlify_token.md` 已更新為正確 token

### 2. Windows 桌面版 Claude 讀取 GitHub 設定
- 教練問如何讓 Windows Claude Desktop 讀 GitHub
- 用 `gh auth token` 取得現有 token（不叫教練當搬運工）
- 提供 Claude Desktop MCP GitHub Server 設定（claude_desktop_config.json 格式）

### 3. 個人品牌網站接手（進行中）
- 已 clone `coach1973/bymyway-website` 到 `/Users/bymyway/github_repos/bymyway-website/`
- 來源：Windows 桌面版 Claude 製作，GitHub Pages 部署
- 線上版：https://coach1973.github.io/bymyway-website/
- 教練方向：**專注個人品牌，拿掉 AI 相關內容**
- 已完成三處修改：
  1. 品牌金句：「給 AI 完善的規則書…」→「你是誰，決定了別人怎麼看你；而不是，別人怎麼看你，決定了你是誰。」（出自海餅乾語錄）
  2. 身份標籤：「🤖 頂級特助系統創建者」→「📚 人才培育系統創辦人」
  3. 企業演講：「AI 落地與自動化」→「品德教育與傳統文化」
- 參考資料：
  - 官方網站 www.bymyway.com（已讀取首頁＋關於我們）
  - 海餅乾語錄（`~/Downloads/海餅乾語錄.docx`）——大量金句素材
- HTML 預覽已放桌面：`~/Desktop/bymyway-preview.html`
- **尚未 commit、尚未推送**，等教練看完預覽確認方向

### 4. 網頁推 SOP 複習
- 教練指示「看網頁推 SOP」，已讀取並確認 SOP 內容正確
- SOP 路徑：`workspace/knowledges/SOP_netlify_website_edit.md`
- SOP 裡的 token 正確 ✅

---

## 📋 下一棒待辦

| 優先 | 任務 | 說明 |
|------|------|------|
| 🔴 | bymyway 個人品牌網站繼續 | 教練看完預覽後，根據回饋調整內容，可能加語錄精選區塊 |
| 🟡 | bymyway 網站推送 | 教練確認後 git push（GitHub Pages 自動部署） |
| 🟡 | H 的 gh auth 修復 | H 無法 push，根因疑為不同 token store |
| 🟡 | jiesheng-leadership 金流就緒時 | 暗號「恢復早鳥名額」→ cp 備份蓋回 |

---

## 🔑 本場 commit hash

| commit | 內容 |
|--------|------|
| 9669ecd | 超限戰網頁完整復原（首映週+續映週+9號外） |

---

## 📌 重要路徑

- bymyway 網站 repo：`/Users/bymyway/github_repos/bymyway-website/`
- 海餅乾語錄：`~/Downloads/海餅乾語錄.docx`
- 官方網站：www.bymyway.com
- 超限戰 repo：`/Users/bymyway/github_repos/theunrestrictedwar/`
- 網頁推 SOP：`~/.openclaw/workspace/knowledges/SOP_netlify_website_edit.md`
- Netlify token（正確）：見 memory/reference_netlify_token.md

---

## ⚠️ 本場教訓

1. **theunrestrictedwar 是手動上傳型**——SOP 寫死禁止 git push 部署，我先 git push 浪費一步（守則 #07）
2. **Netlify token 要查路徑大全**——記憶檔存的 token 可能過期或不完整，路徑大全是真相源
3. **HTML 預覽放桌面**——教練多次提醒這是 SOP，App 裡的預覽看不清楚
