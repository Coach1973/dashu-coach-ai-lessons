---
name: character-illustration-batch
description: 教練說任何圖片生成指令（「跑圖」「生圖」「漫畫」「分鏡」「storyboard」「章回小說」「插畫集」「用我照片當 reference」「角色要保持一致」「場景圖」⋯）→ 一律預設走 LK888（2026-09-28 教練親定，不再問 provider / model）。鎖臉版走 `/v1/images/edits` + 教練 reference；教練說「敘事版 / 不鎖臉 / 以劇情為主 / 避免視覺疲勞」→ 走 Narrative 版（`/v1/images/generations` 純文字，不帶 reference）。跑前必先讓教練選通知節奏（A 每張推 / B 每 N 張聚合 / C 跑完一次），預設 A。
---

# 觸發分流

| 教練訊息特徵 | 走哪個版 |
|---|---|
| **畫面裡有教練本人**（「分鏡」「漫畫」「章回小說」「用我照片當 reference」「角色要保持一致」「照之前的模式」「LK888生圖」⋯）| **🔒 鎖臉版**（`/v1/images/edits` + reference）|
| **畫面裡不要教練本人**（「敘事版」「narrative version」「以劇情為主」「不要每張都放教練本人」「避免視覺疲勞」「不鎖臉」「不用我照片」⋯）| **🎬 Narrative 版**（`/v1/images/generations`、不帶 reference）|

訊息同時含「漫畫/分鏡/storyboard」 + 「不要我本人/narrative/不鎖臉」 → **Narrative 版優先**（教練明確說不要鎖臉）。

❌ 不觸發：產業服務鏈（用 `industry-chain-prompt` skill）、結構化 infographic/poster/blueprint prompt（用 `infographic-lk888` skill）

> 任何時候覺得「畫面裡該不該有教練」判斷不出來 → **先問教練、不要瞎猜**（鐵律 #8 不擅自擴張）。

---

# 🔒 鎖臉版 SOP（2026-09-25 教練親定）

**適用**：教練本人形象要出現在畫面裡（單張也走這條）。

1. **確認 reference 圖**：`~/.openclaw/workspace/claude-brain/data/comic_reference/coach_face_reference.jpg`（254 KB 去背版，Ep2-4 驗證有效）。教練有新照片 → 更新 reference（同檔名覆蓋）
2. **走 `/v1/images/edits`**：`scripts/generate_comic_panel.py`，multipart/form-data 帶 image + prompt
3. **prompt 開頭必加 IDENTITY LOCK 段落**：明確告訴模型「以上傳的照片為唯一臉部參考，禁止自由發揮」
4. **prompt 結尾必加護欄**：no readable text / no Chinese / no English / no watermarks / no lapel pin / no name badge / no extra people / no gray hair / no white hair
5. **生成後自檢**：`view_image` 看圖，確認是亞洲中年男性 + 短黑髮無白 + 灰格紋西裝 + 教練氣質

**禁止行為**：用 `/v1/images/generations`（純文字）生圖 / 自己新寫一個不帶 reference 的生圖腳本 / 沒用 view_image 自檢就推 Telegram / 教練有疑慮時辯稱「可能 model 不行」

> 教練手動貼 ChatGPT / Gemini 時要自己上傳 5 張照片（LINE_ALBUM___260711_7.jpg 等），
> 小龍蝦無法代勞。本 SOP 只規範小龍蝦自動跑圖的行為。

---

# 🎬 Narrative 版 SOP（2026-09-26 教練親定）

**適用**：教練本人不出現、以場景/事件/隱喻/物件當主角。

| 項目 | 鎖臉版 | Narrative 版 |
|------|--------|--------------|
| Endpoint | `/v1/images/edits` | `/v1/images/generations` |
| Reference 圖 | 必帶 | **不帶**（純文字）|
| IDENTITY LOCK 段 | 必加 | **不加** |
| 教練本人 | 每張都有 | **不出現**（或僅剪影/遠景/暗示）|

1. 確認 narrative 觸發詞（「敘事版」「不鎖臉」「以劇情為主」⋯）
2. 走 `/v1/images/generations`：`scripts/generate_teamwork_manga_narrative.py` 風格腳本
3. 不帶 reference 圖：純文字 prompt
4. 不寫 IDENTITY LOCK 段
5. 場景描述段不要提「the Coach」：移除 `Recurring protagonist 'the Coach': ...` 段
6. 場景裡有「人」要出現：仍要遵守下方「成熟不蒼老」
7. 風格選擇：**禁用 `clean modern Japanese anime key-visual`**（會拉回 20s 動漫少年臉），
   改用 `cinematic semi-realistic illustration`
8. 跑前仍要先讓教練選通知節奏（A/B/C）
9. 仍要 `view_image` 自檢：確認教練本人沒有意外出現 + 人物年齡符合

---

# 📐 共同流程（兩個分支之後都走）

## 1. 接收素材並存檔

教練會丟：1~4 張 reference 照片 + HTML 故事框架（或純 prompt 清單）+ 角色描述

存到 `~/.openclaw/workspace/claude-brain/data/<任務日期>/`，原始檔跟處理後檔都留。
**inbound staging 不持久**，必須手動複製。

## 2. 選 reference 圖（鎖臉版用）

優先順序（AI 抓臉成功率遞減）：

1. **去背 + 3/4 側面 + 棚拍光線** ← 最佳
2. 純色/黑背景 + 正面半身 + 表情中性
3. 任意清晰照（避免多人合影、聚餐照雜訊）

存為 `comic_reference/coach_face_reference.jpg`（永遠同檔名，後續 panel 跑同一個 reference）。

## 3. 角色錨點模板（每個 prompt 必加前綴）

```
Consistent character design across all panels: a distinguished [年齡][國籍][性別][職業]
with [髮型 + 無白髮描述], [no/no facial hair], wearing [西裝 + 無配件],
[表情描述]; same face shape, same jawline, same nose, same eye spacing in every panel;
no lapel pin, no name badge, no extra accessories; refined, dignified, contemplative expression.
```

關鍵點：「same face shape / jawline / nose / eye spacing」鎖臉 / 「no lapel pin, no name badge」防 AI 把照片小配件帶入 / 教練說沒白髮 → 寫「fully dark no gray」/ 中文 prompt 必加禁簡體 + 防亂碼條款（沿用 `industry-chain-prompt` skill 規則）

## 4. 成熟不蒼老設定（2026-09-26 教練親定）

教練說「成熟但不要蒼老」 — 這是個**容易被 gpt-image-2 預設壓過**的設定，必須按下面寫法才會生效。

**後段（角色錨點）必加禁用清單**：
`NO gray hair, NO silver streaks, NO graying temples` / `NO crow's feet, NO forehead lines, NO nasolabial folds` / `NOT childlike, NOT teenagery, NOT 20-something`

**位置權重坑**：人物年齡設定必須寫進**前段場景描述**，不能只在後段 [CHARACTER ANCHOR]。
gpt-image-2 對 prompt 後段權重稀釋明顯（後段幾乎無影響）。

**風格衝突坑**（已驗證 4 次 prompt 失敗的根因）：
人物成熟是 critical 需求 → 用 `cinematic semi-realistic illustration` / `digital painting` / `concept art`，
**不要用 anime key-visual**。風格選擇要在 prompt **第一行**就寫，不要放在 STYLE 段尾。

## 5. 安全護欄後綴（每個 prompt 必加結尾）

```
no readable text, no Chinese text, no English text, no watermarks,
no lapel pin, no name badge, no extra people
```

即使 prompt 原本就有「no text」描述，仍要補上（防漏）。

## 6. 長寬解偵測（已驗證修正的 regex）

```python
import re
sl = prompt.lower()
if "double-page" in sl or re.search(r"\b21:9\b", sl):
    size = "1792x1024"   # 雙頁跨頁 21:9
elif re.search(r"\b16:9\b", sl) or "widescreen" in sl:
    size = "1536x1024"   # 16:9 橫幅
elif re.search(r"\b2:3\b", sl) or "portrait" in sl:
    size = "1024x1536"   # 直幅
else:
    size = "1536x1024"   # 預設橫幅
```

⚠️ `"2:3" in sl` 會把 "2:30 AM" 誤判為 portrait，必須 `\b` word boundary（2026-09-23 prompt 01 bug）。
⚠️ 檢查順序：21:9 → 16:9 → 2:3 → 預設。

---

# 🛠 腳本

| 用途 | 腳本 | 備註 |
|------|------|------|
| 單張測試 | `~/.openclaw/workspace/scripts/generate_comic_panel.py` | 從 generate_industry_chain.py 擴充走 `/v1/images/edits` + 帶 reference |
| 批次（A 節奏，canonical）| `~/.openclaw/workspace/scripts/comic_monitor.py` | 解析 HTML + 逐張生成 + 每張 pushPhoto |
| 批次（C 節奏）| `~/.openclaw/workspace/scripts/batch_comic_run.py` | **已棄用**，教練明確要 sendMediaGroup 才用 |
| Narrative 純文字生圖 | `~/.openclaw/workspace/scripts/generate_teamwork_manga_narrative.py` | 不帶 reference；v5 版 `generate_teamwork_manga_v5_anime_mature.py` 有 mtime 防呆 |

---

# 📬 通知節奏（跑前必確認，不再擅自聚合）

跑前一句：「這批 N 張，您要 **A 每張完成立即推**／**B 每 N 張聚合**／**C 跑完一次推**？」等教練答再開跑。**禁止替教練選**。

| 節奏 | 適用情境 | 實作 |
|------|---------|------|
| **A** 每張完成立即推（推薦預設）| 教練要看即時進度、要能安心去做別的事 | `comic_monitor.py` |
| **B** 每 N 張聚合一次 | 介於中間，N 多少跑前跟教練確認 | `comic_monitor.py` 加 threshold |
| **C** 跑完一次推 | 教練**明確**說「跑完一起給我」「不要一直通知」才用 | Telegram `sendMediaGroup`（最多 10 張/批、剩餘第二批）|

⚠️ **2026-09-23 教練親糾**：預設就用 C（sendMediaGroup 一次性聚合）= 失敗案例。
教練原話：「你叫我去睡，但是你這邊沒有進度啊，你得讓我看到進度，我才能放心去睡啊！」→ 從此跑前必先讓教練選。

---

# 📦 上架（comic 跑完後教練說「上架」「給網址」「發布」）

見 `publishing.md`。重點：

- Cloudflare 100 MB 上限 → 超過 PNG → sips JPEG q=85（縮 76%）或 pngquant lossy
- 上傳端點：`https://event.bymyway.com/curation/upload?key=***`，帶 `custom_slug`（教練親口確認、小寫英文/數字/短橫線）
- 完成確認：跑 `curation_check_result.py "<slug>"` 拿真正最終網址，不要用 `curl /curated/<slug>/` 猜

# ⚡ 批次執行安全（中途中斷恢復 / mtime 防呆 / 推送去重）

見 `runtime-safety.md`。重點：

- 兩個事故（2026-09-26）：compactor 重跑燒光 LK888 額度 / Telegram 重複推送
- 兩個 log：`state/lk888_run_history.json`（生成面）/ `state/telegram_push_history.json`（交付面）
- 教練說「重複」時兩個 log 都查，不能只查一個

# ⚠️ 已知陷阱

見 `pitfalls.md`（完整列表）。最常踩的 3 個：

| 陷阱 | 解法 |
|------|------|
| 用 `/v1/images/generations` 純文字生圖 → 跨圖換臉 | 改 `/v1/images/edits` + 帶 reference |
| 不問就用 sendMediaGroup 一次推 → 教練看不到進度 | 跑前先讓教練選 A/B/C |
| `"2:3" in sl` 踩到 "2:30 AM" | 用 `\b2:3\b` word boundary |

---

# 參考

- 腳本：`~/.openclaw/workspace/scripts/generate_comic_panel.py`（單張）、`comic_monitor.py`（A 節奏，canonical）、`batch_comic_run.py`（C 節奏，已棄用）
- 教練 Telegram chat_id：6124913915
- 教練形象照範本位置：`~/.openclaw/workspace/claude-brain/data/comic_reference/`
- 沿用禁簡體 + 防亂碼條款：`industry-chain-prompt` skill
- 來源案例：2026-09-23《證明給機器看》14 張漫畫插畫批次任務、《大副與軍師：32MB 封包攻防戰》四話 62 panels 上架 event.bymyway.com/curated/ai-story/
- 支援文件：`publishing.md`（上架）、`runtime-safety.md`（執行安全）、`pitfalls.md`（完整陷阱表）
- 批次跑完後教練說「下載」「打包」「私庫」→ `image-archive-github` skill（GitHub 私庫 + MANIFEST.md 一鍵打包，不是上架公開、不是 Telegram 推圖）