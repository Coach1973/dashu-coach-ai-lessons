---
name: reference-hermes-skills
description: Hermes 觸發詞對映 SOP（教練說什麼詞，就載入哪份 SOP 執行）。兩份 SOP 都在 ~/.hermes/skills/workflow/，內容已鏡像到 knowledges/
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2026-06-10-hermes-skills
---

# Hermes 觸發詞 SOP 對映表

> ⚠️ 這兩份 SOP 同時存在兩個位置，內容互相鏡像：
> - **Hermes skill 觸發版**（`~/.hermes/skills/workflow/`，含觸發詞 metadata，給 Hermes bot 用）
> - **OpenClaw 執行版**（`~/.openclaw/workspace/knowledges/`，詳細版，給小龍蝦讀）

## 🦞 兩份 SOP 一覽

### 1. 自動站 SOP（bymyway WordPress iframe 部署）

| 項目 | 值 |
|------|-----|
| **用途** | 把外部靜態網站部署到 bymyway.com 底下當子頁面（WordPress REST API） |
| **觸發關鍵字** | 「自動站 SOP」/「bymyway SOP」/「自動站」/「部署到 bymyway」 |
| **Hermes skill** | `~/.hermes/skills/workflow/auto-site-sop-bymyway/SKILL.md` |
| **OpenClaw 主檔** | `~/.openclaw/workspace/knowledges/SOP_bymyway_auto_site.md` |
| **步驟數** | 10 步（含 OG meta + site_icon）|
| **版本** | v3.1（2026-06-10 06:30）|
| **工具** | `wp_client.py` / `deploy_to_bymyway.py` / `switch_to_canvas.py`（在 `projects/bymyway-bridge/`）|

### 2. 網頁推 SOP（Netlify zip 上傳）

| 項目 | 值 |
|------|-----|
| **用途** | 把本機 HTML/CSS/JS 站 zip 上傳到 Netlify 站 |
| **觸發關鍵字** | 「網頁推 SOP」/「Netlify 部署」/「推 Netlify」 |
| **Hermes skill** | `~/.hermes/skills/workflow/web-push-sop-netlify/SKILL.md` |
| **OpenClaw 主檔** | `~/.openclaw/workspace/knowledges/SOP_netlify_website_edit.md` |
| **步驟數** | 3 步（建站 → 預覽 → 推）|
| **版本** | v1.1（2026-06-10 補對照表）|
| **教練按鈕數** | 0 個（守則 #08）|

## 🆚 怎麼分（不混用）

| 情境 | 用哪個 SOP |
|------|----------|
| 教練說「把 X 站掛到 bymyway」/「自動站 SOP」/「部署到 bymyway」 | → **自動站 SOP** |
| 教練說「推那個站」/「zip 推上去」/「推 Netlify」/「網頁推 SOP」 | → **網頁推 SOP** |
| 教練說「更新 leadership 站」/「推 jiesheng」 | → **網頁推 SOP**（Netlify 站）|
| 教練說「掛到 www.bymyway.com/xxx」 | → **自動站 SOP**（WordPress 子頁）|

## 🔴 共同鐵律

- 教練全程 **0 個後台按鈕**（守則 #12 不當搬運工）
- **先本機預覽 → 教練確認 → 才推**（守則 #08 討論=執行）
- **不混用**：Netlify 跟 bymyway 是兩種標的物，各有各的 SOP

## 📂 兩份 SOP 互相鏡像的證據

- `auto-site-sop-bymyway` 內文最後一節：「工具路徑速查」指到 `~/.openclaw/workspace/knowledges/SOP_bymyway_auto_site.md`
- `web-push-sop-netlify` 內文：「路徑大全參考」指到 `~/.openclaw/workspace/knowledges/reference_netlify_token.md`

## 🗓️ 建立時間
2026-06-10 06:56（教練主動告知，已記下）
