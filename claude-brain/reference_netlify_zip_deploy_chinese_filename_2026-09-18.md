---
name: reference-netlify-zip-deploy-chinese-filename-2026-09-18
description: "教Netlify zip deploy API對中文檔名/目錄直接拒絕解壓（error: Deploy failed while extracting zip），只能先用ASCII檔名"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5876ed8b-e8aa-57aa-a324-b2e2e2d54d6f
  modified: 2026-09-18T09:14:36.186Z
---

# Netlify zip deploy API 不接受中文檔名

2026-09-18 試圖把 bigtree-tw repo 的 HEAD 部署到 Netlify，遇到 5 次連續「Deploy failed while extracting zip」錯誤，最終查出根因：**Netlify 解壓 zip 時遇到中文檔名/目錄會直接失敗**，不論用什麼編碼策略（git archive / Python zipfile + UTF-8 flag 0x800 / STORED 不壓縮）。

**Why：** Netlify 的 zip 解壓服務對中文檔案的支援比想像中差，即使現代 zip 規範有 UTF-8 flag（general purpose bit 0x800），Netlify 似乎仍用 CP437 解碼或是有 bug。這是個隱性阻斷，會讓 Mac 上所有含中文檔名的 repo 都 deploy 失敗，但平常 deploy 大多數是純 ASCII 英文檔案所以不會遇到。

**How to apply：**

### 症狀
- Netlify API 上傳 zip 後，deploy state 卡在 `uploaded` 約 30~60 秒
- 最終 state 變 `error`，error_message: `Deploy failed while extracting zip`
- 沒有 build log 可查（zip deploy 無 build_id），純黑盒錯誤

### 已驗證無效的策略（5 次嘗試）
1. `git archive HEAD | zip` — 失敗
2. `git archive HEAD + zip -d 排除大目錄` — 失敗
3. Python `zipfile.ZIP_DEFLATED + flag_bits |= 0x800 (UTF-8 標記)` — 失敗
4. Python `zipfile.ZIP_STORED (無壓縮)` — 失敗
5. 排除大目錄 + UTF-8 flag — 失敗

### 唯一成功策略
- **完全排除所有中文檔名/中文目錄** — 過濾掉 `archive/大樹小講_歷史講座紀錄.html`、`archive/2026-07-01_創業x政府xAI講座/` 這類內容
- ASCII-only zip 立即 `state: ready`

### 部署 bigtree repo 的限制
- HEAD commit fdfaff0 新增 5 行到中文檔名 HTML（`archive/大樹小講_歷史講座紀錄.html`）
- 主頁 `index.html` 第 60 行有 `href="archive/大樹小講_歷史講座紀錄.html"`
- 這兩個檔案都無法 deploy

### 解法選項（教練需裁示）
| 選項 | 風險 | 適用情境 |
|---|---|---|
| **A. 中文檔名 rename 成 ASCII**（如 `archive/dashu-history.html`） | 破壞舊 URL、Google 索引失效、外站連結 404 | 一次性投資後 deploy 不再失敗 |
| **B. Netlify dashboard 手動上傳 zip**（繞過 API） | 教練手動操作，無法 commit 驗證 | 暫時單次 deploy |
| **C. 不 deploy 中文檔名檔案**，只在主辦活動的動態網站（`event.bymyway.com/bigtree/`）更新 10/3 KR EDM 連結 | 靜態版缺 10/3 內容，但動態版正常 | 教練決定接受靜態版過期 |

### 這次事故教訓
- **deploy 前先 `unzip -l <zip>` 看中文檔名**，如果出現 `����` 亂碼就會失敗
- 不要嘗試用編碼策略繞過，直接 rename 才是根本解
- 大型 deploy (10MB+) 失敗會覆蓋前次成功 deploy 的內容（Netlify 是 replace），**失敗前先 restore 回前次成功 deploy**

### Restore 指令
```bash
DEPLOY_ID="前次ready的deploy id"
curl -X POST -H "Authorization: Bearer $TOKEN" \
  "https://api.netlify.com/api/v1/sites/$SITE_ID/deploys/$DEPLOY_ID/restore"
```

### 本場實測
失敗 5 次 → restore 回 9/16 deploy `6aaae4738f7bad35092afcb8` → 線上恢復正常（中文檔案 301 redirect 都在）。10/3 KR 改動**未上線**，等教練選 A/B/C 方案。
