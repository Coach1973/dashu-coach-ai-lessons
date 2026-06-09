# 自動站 SOP v3.0（bymyway 部署流程）

> 教練親定 2026-06-10 凌晨 4:30 開始撰寫 → 5:00 v2.0 定稿 → 6:10 v3.0 定稿。
> 觸發事件：
> - v2.0：jiesheng-leadership.netlify.app → bymyway.com/leadership/store 完整鏈路驗證成功。
> - v3.0：教練貼 LINE 預覽卡片發現大樹教育 logo + 文字→ 修成 jiesheng 書封面（OG meta 塞 content 頂端）。
> 場景：**把外部靜態網站部署到 bymyway.com 底下，作為子頁面**。
> 適用對象：教練後續要做的所有站（全球健康發展協會、cool-case、theunrestrictedwar 等）。
> 所有 AI 助教（終端機/桌面版/小龍蝦）強制遵守。
> 與「網頁推 SOP」並列，但**完全不同的流程**——本 SOP 是 WordPress REST API 路徑，不碰 Netlify。
> **本 SOP 唯一採用的部署方式：iframe 嵌入**。不採用「整段塞 HTML」（教練親測會出亂碼）。

---

## 🔴 教練親定的核心精神（不可違背）

> **教練動嘴 → AI 全自動 → 本機預覽 → 教練說「推」→ 上線。**
>
> 教練全程 **0 個後台按鈕、0 個登入動作、0 個找頁面的時間**。
>
> **唯一例外**：永久連結設定（Custom Permalinks 必裝後），需要教練在 bymyway 後台「編輯頁面 → 永久連結」30 秒親改一次。**這是 Custom Permalinks 外掛本身的限制，不是 AI 能繞的**。

---

## 🎯 適用場景 vs 不適用

| 適用 ✅ | 不適用 ❌ |
|--------|--------|
| 外部靜態網站要搬進 bymyway.com | bymyway 內部新增文章/頁面（用 wp_client.py 即可）|
| 一頁式活動頁（workshop、課程宣傳、講座）| 改 bymyway 視覺/主題色（要 Elementor 後台） |
| **iframe 嵌入（唯一採用方式）** | 改金流/PayPal 設定（動到錢，永遠人工） |
| **子品牌獨立呈現（不掛大樹教育表頭）** ← 必用 | 多頁網站一次搬完（要分章節，時間成本 5 倍起跳） |
| 教練朋友/客戶的事業頁面 | WooCommerce 商店結構改動（要動主機層） |
| | **整段塞 HTML（教練親測出亂碼，禁止採用）** |

---

## 🛠️ 前置工具（一次性設定，30 分鐘內完成）

### 1. bymyway-bridge 工具

路徑：`~/.openclaw/workspace/projects/bymyway-bridge/`

需要的檔案：
- `wp_client.py`（WordPress REST API 封裝）
- `deploy_to_bymyway.py`（自動部署腳本）
- `switch_to_canvas.py`（改 Elementor Canvas 模板腳本）

### 2. 帳密（macOS Keychain）

```bash
security add-generic-password -s bymyway-bridge -a wp-api -w "應用程式密碼" -U
```

WordPress 帳號：**固定 `bymyway7`**（已驗證 is_super_admin）

### 3. WordPress 後台設定（教練在後台做一次，AI 不能用 API 做）

- **應用程式密碼啟用**（使用者 → 個人資料 → 應用程式密碼）
- 24 碼密碼存進 Keychain

### 4. 🔴 必裝外掛：Custom Permalinks（守則 #01 寫死）

> **為什麼必裝**：WordPress 預設**不支援父子 URL 結構**（父頁縮排≠URL 前綴）。
> 教練要的「`bymyway.com/<母頁 slug>/<子頁 slug>/`」這種 URL 必須靠 Custom Permalinks 外掛才能做到。
> **沒裝這外掛 = 子頁面 URL 永遠只能是 `<slug>/`，沒辦法帶母頁前綴**。

**AI 用 REST API 自動裝**：
```bash
POST /wp-json/wp/v2/plugins
body: {"slug": "custom-permalinks", "status": "active"}
```

驗證已裝：GET /wp-json/wp/v2/plugins → 確認 `custom-permalinks/custom-permalinks` 是 `active`

**已知限制**：外掛**不開放 REST API 寫入端點**（只有 GET），永久連結必須教練在後台「編輯頁面 → 永久連結」改。

---

## 🚀 完整 SOP：八步驟（從抓站到上線）

> 每一步都附**驗證方式**（守則 #E12 強的成功標準）+ **常見雷點**（守則 #07 不再同處跌倒）。

### 步驟 1：抓外部站

**動嘴：**「AI，把 https://某站.netlify.app/ 整站抓下來，存到 `/tmp/站名-to-bymyway/`」

**AI 做：**
```bash
mkdir -p /tmp/站名-to-bymyway
cd /tmp/站名-to-bymyway
curl -sL https://某站.netlify.app/ -o index.html
```

**驗證：**
- `index.html` 存在、`head` 標籤正常、有 `<title>`
- `wc -l index.html`（頁面行數）合理
- 檔案大小 > 1KB

**抓附檔：**
```bash
grep -oE '(src|href)="[^"]+\.(jpg|png|jpeg|gif|webp|svg|css|js)"' index.html | sort -u
# 逐一下載
curl -sL "https://某站.netlify.app/圖片.png" -o 圖片.png
```

**常見雷點：**
- ⚠️ 外部資源全部用相對路徑 → 不用上傳到 bymyway
- ⚠️ 外部資源用 CDN 網址 → **不上傳**，iframe 模式時 iframe 自己會抓

**花費：** 1-3 分鐘

---

### 步驟 2：上傳媒體到 bymyway（**v3.0 起通常跳過**）

> **v3.0 變更**：因為採用 iframe 嵌入，**iframe 自己會抓來源站**的圖片，不需要把圖上傳到 bymyway 媒體庫。
> 圖片路徑還是會在 iframe 內容裡（指向 Netlify），但因為使用者看到的是 iframe 嵌的 jiesheng-leadership 頁面，所以圖照樣顯示。

**何時需要上傳**：
- 教練明確要求 OG meta 預覽圖要用特定 bymyway 媒體庫 URL（見步驟 9）
- 教練想讓 bymyway 後台媒體庫有完整資產副本（選用）

**AI 做（需要時）：** 用 `wp_client.py` 的 multipart upload，每張圖拿到 `source_url`。

**驗證（需要時）：** 每張圖都有 `https://www.bymyway.com/wp-content/uploads/...` URL。

**花費：** 30 秒/張（僅當教練要求時）

---

### 步驟 3：建 bymyway 頁面（draft）

**動嘴：**「AI，在 bymyway 建立頁面，標題 X，slug Y，套 Canvas 模板，status draft」

**v3.0 唯一採用模式：iframe 嵌入**

```python
content = '''<iframe src="https://某站.netlify.app/" 
  style="width:100%;min-height:1800px;border:none;display:block;" 
  title="頁面標題"></iframe>'''

payload = {
    "title": "頁面標題",
    "content": content,
    "status": "draft",
    "slug": "<slug>",          # 例：northern, store, leadership
    "template": "elementor_canvas",   # 🔴 必套（拿掉 bymyway 表頭/footer）
    "excerpt": "一句話描述",
}
```

> ⚠️ **v3.0 起，建立頁面時直接帶 `template: elementor_canvas`**，省下後續步驟 6 還要再改一次。

**驗證：**
- 頁面 ID 記下（例如 27335）
- status 確實是 `draft`
- template 確實是 `elementor_canvas`
- slug 確認沒被 bymyway 預設商店 / 文章 / WooCommerce 佔用

**🔴 重要：slug 命名鐵律（避免 301 衝突）**

| 千萬不要 | 用 | 為什麼 |
|---------|---|-------|
| `shop` ❌ | `store` ✅ | WooCommerce 預設商店 base = `/shop/`，會搶路徑 |
| `cart` ❌ | `cart-2026` ✅ | WC cart base |
| `checkout` ❌ | `signup` ✅ | WC checkout base |
| `my-account` ❌ | `account` ✅ | WC my-account base |
| `product` ❌ | `course` ✅ | WC product base |

**驗證 slug 沒被佔用：**
```bash
curl -sIL -A "Mozilla/5.0" "https://www.bymyway.com/<slug>/" | grep -E "HTTP"
# 404 = 空路徑，可用
# 200 = 已有內容，會衝突
```

**常見雷點：**
- ⚠️ **不要**預設把 slug 設成 `shop` / `cart` / `product` → 一定被 WC 預設搶走
- ⚠️ status 永遠先 `draft`，不要直接 `publish`

**花費：** 1-3 分鐘

---

### 步驟 4：本機預覽（必做，守則 #12 + 網頁推 SOP 第四步）

> ⚠️ **教練看完之前，絕對不能動 publish。** 否則違反「教練說推才推」鐵律。

**動嘴：**「AI，幫我開本機預覽」

**AI 做：**
```bash
mkdir -p /tmp/preview-<站名>
cat > /tmp/preview-<站名>/index.html << 'EOF'
<!DOCTYPE html>
<html><head><title>預覽</title></head>
<body>
<div class="preview-bar">教練專用預覽</div>
<iframe src="https://某站.netlify.app/" style="width:100%;height:calc(100vh - 100px);border:none;"></iframe>
</body></html>
EOF

# 啟動 server
lsof -ti :<port> | xargs kill -9 2>/dev/null
nohup python3 -m http.server <port> --directory /tmp/preview-<站名> > /tmp/preview-<站名>.log 2>&1 &
open "http://localhost:<port>/"
```

**驗證：**
- 教練在瀏覽器看到 iframe 載入的內容
- port 不跟舊 server 衝突

**花費：** 1 分鐘

---

### 步驟 5：教練確認（動嘴說推/改）

| 教練反應 | AI 動作 |
|---------|--------|
| 「推」「OK」「上線」| 進步驟 5.5（永久連結）→ 6（Canvas 確認）→ 7 → 8 → 9（OG meta） |
| 「不對，調 X」| 回步驟 3 改 |

**若教練要母頁 URL 結構**（`bymyway.com/<母頁 slug>/<子頁 slug>/`）：
- 進步驟 **5.5：Custom Permalinks 設定**（見下方）

---

### 步驟 5.5：Custom Permalinks 設定（🔴 守則 #01 寫死）

> **何時需要**：教練說「我要 `/leadership/store/` 這種母頁+子頁 URL 結構」→ 進這步
> **必做前提**：Custom Permalinks 外掛已裝（前置工具步驟 4）

**5.5.1 確認外掛已啟用**
```bash
GET /wp-json/wp/v2/plugins
# 確認 custom-permalinks/custom-permalinks 是 active
```

**5.5.2 教練去後台改永久連結（30 秒，AI 不能做）**

> ⚠️ **這是 SOP 唯一需要教練親手做的步驟**（Custom Permalinks 外掛不開放 REST API 寫入端點）
> **不是 AI 偷懶，是外掛限制**。

教練動作：
1. 進 `https://www.bymyway.com/wp-admin/post.php?post=<頁面ID>&action=edit`
2. 右上「**永久連結**」按下去
3. 把 `https://www.bymyway.com/?page_id=<ID>` 改成 `leadership/store`（**只打這段，不打斜線、不打網域**，外掛會自動加）
4. 存檔

**5.5.3 AI 驗證永久連結生效**
```bash
curl -sIL -A "Mozilla/5.0" "https://www.bymyway.com/<母頁 slug>/<子頁 slug>/" 2>&1 | grep -E "HTTP"
# 預期：HTTP/2 200
# 如果 404：等 5-10 秒（LiteSpeed 快取刷新）
# 如果 301：slug 衝突，回去改 slug
```

**常見雷點：**
- ⚠️ 沒裝 Custom Permalinks 就想用母頁+子頁 URL → 永遠 404
- ⚠️ 永久連結打成完整網址 `https://www.bymyway.com/...` → 外掛不接受，只要打路徑部分
- ⚠️ 永久連結打 `/leadership/store/` 帶斜線 → 部分版本不接受，不要打斜線
- ⚠️ 永久連結用大寫 → bymyway 是區分大小寫的，全小寫

**花費：** 教練 30 秒

---

### 步驟 6：🔴 確認 Elementor Canvas 模板（**守則 #01 子品牌獨立寫死**）

> **v3.0 變更**：步驟 3 建立頁面時已直接帶 `template: elementor_canvas`，本步驟變成「確認 + 補救」。
> 若建頁時忘了帶，現在補上即可（不需要砍頁重建）。

> **何時需要**：
> - 子品牌 / 朋友事業 / 外部內容嵌入 bymyway → **必做**
> - bymyway 內部自有頁面（不對外）→ 可選

> **不做的後果**：頁面會有大樹教育的 header、選單、footer、logo。**教練朋友會不爽**（2026-06-10 凌晨 3:04 教練親示範過：朋友不好意思掛在大樹教育底下）

**動嘴：**「AI，把這頁改成 Elementor Canvas 模板，拿掉 bymyway header/footer」

**AI 做：**
```python
payload = {"template": "elementor_canvas", "status": "draft"}  # 保持 draft
POST /wp-json/wp/v2/pages/<頁面ID>
```

**驗證（必做）：**
```bash
curl -sL -A "Mozilla/5.0" "https://www.bymyway.com/<URL>/" -o /tmp/check.html
echo "header 出現: $(grep -ci '<header' /tmp/check.html) (目標 0)"
echo "footer 出現: $(grep -ci '<footer' /tmp/check.html) (目標 0)"
# 注意：iframe 內的 header 不算（那是 iframe 內容的）
# 這裡 grep 的是 bymyway 自己的 header
```

> ⚠️ **驗證重點是 bymyway 自己的 header，不是 iframe 內容的**。如果 grep 結果 > 0，**而且不是 iframe 內的**，就是 Canvas 模板沒生效。

**常見雷點：**
- ⚠️ **2026-06-10 凌晨 4:24 跌倒**：第二次建子頁時忘了套 Canvas，被教練罵
- ⚠️ 驗證時沒過濾 iframe 內的 header → 誤判
- ⚠️ template 名稱打錯（要 `elementor_canvas` 不是 `canvas`）

**花費：** 30 秒

---

### 步驟 7：教練二次確認（再動嘴說推）

> 步驟 6 改了模板，視覺可能變。**教練再看一次本機預覽**（如果步驟 4 還開著就重整理）。

**動嘴：**「推」/「再推一次」/「OK 上線」

---

### 步驟 8：教練說推 → AI 改 publish → 線上驗證

**AI 做：**
```python
payload = {"status": "publish"}
POST /wp-json/wp/v2/pages/<page_id>
```

**同步做：**
- 關本機 server（`lsof -ti :<port> | xargs kill -9`）
- 線上驗證：curl 線上 grep 關鍵字
- 更新 JUNSHI_HANDOFF_LATEST.md
- commit hash（守則 #05）

**驗證：**
```bash
curl -sIL -A "Mozilla/5.0" "https://www.bymyway.com/<URL>/" | head -2
# 預期：HTTP/2 200
```

**花費：** 30 秒

---

### 步驟 9：🆕 LINE / FB 預覽卡片（OG meta 塞 content 頂端，**v3.0 新增**）

> **為什麼需要**：bymyway 預設**沒裝 SEO 外掛**（Yoast / Rank Math），所以**沒有 og:title / og:image / og:site_name 這些 meta 標籤**。
> 結果：教練把 bymyway 網址貼到 LINE / FB / WhatsApp → 預覽卡片會 fallback 用 `<title>`（帶「大樹教育顧問」）+ 全站 logo（大樹 logo）。
> **這是 Canvas 模板拿不掉的事**（Canvas 只清掉 header/footer，**OG meta 在 `<head>` 層級，跟模板無關**）。

> **🔴 教練的問題觸發（2026-06-10）**：
> 把 `bymyway.com/leadership/store/` 貼到 LINE → 預覽出現「大樹教育」+ 大樹 logo。
> 教練罵：「這不是我的個人網站，是要給朋友行銷用的，不要掛在我的大樹教育底下。」

> **v3.0 解法**：AI 在 page content 頂端塞自訂 OG meta 標籤（不靠 SEO 外掛、不靠教練後台）。

**AI 做：**
```python
og_meta = '''<!-- OG Meta for LINE/FB Preview -->
<meta property="og:title" content="<頁面標題> - <子品牌名>" />
<meta property="og:description" content="<一句話描述>" />
<meta property="og:image" content="<bymyway 媒體庫 URL 或 來源站封面圖 URL>" />
<meta property="og:url" content="<bymyway 完整 URL>" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="<子品牌名，不要寫大樹教育>" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="<頁面標題>" />
<meta name="twitter:description" content="<一句話描述>" />
<meta name="twitter:image" content="<圖 URL>" />
<!-- END OG Meta -->
'''

# 把 OG meta 串到現有 content 頂端
new_content = og_meta + '\n' + current_content  # current_content = iframe 字串
payload = {"content": new_content}
POST /wp-json/wp/v2/pages/<page_id>
```

**真實範例（jiesheng-leadership 子頁，2026-06-10 修好）：**
- og:title = `工作坊報名（Workshop） - 結繩領導學 × 兩天工作坊`
- og:description = `結繩領導學 × 兩天工作坊。立即報名，搶限量早鳥名額。`
- og:image = `https://www.bymyway.com/wp-content/uploads/2026/06/book.png`（書封面，不是大樹 logo）
- og:site_name = `結繩領導學`（不是「大樹教育」）
- og:url = `https://www.bymyway.com/leadership/store/`

**驗證（必做）：**
```bash
curl -sL -A "Mozilla/5.0" "https://www.bymyway.com/<URL>/" -o /tmp/og.html
grep -oE 'og:[a-z_]+' /tmp/og.html | sort -u
# 預期：og:title, og:description, og:image, og:url, og:type, og:site_name
grep -E 'property="og:site_name"' /tmp/og.html
# 確認 site_name 不是「大樹教育」
```

**LINE 預覽驗證（手機）：**
1. 把 bymyway 網址貼到 LINE 對話（不要先傳過、要新連結）
2. 等 LINE 抓預覽（5-10 秒）
3. 預覽卡片應該出現：書封面圖 + 標題 + 描述，**沒有「大樹教育」**

**LINE / FB 預覽快取 24-48 小時**：
- LINE Android：長按刪除訊息 → 重貼
- LINE iOS：同上
- 或者請 LINE 聯絡人發新版預覽
- 或者用 [https://www.opengraph.xyz/](https://www.opengraph.xyz/) 線上工具即時驗證

**🔴 重要：母頁跟子頁都要做**

| 雷點 | 後果 | 解法 |
|------|------|------|
| 修了子頁忘了母頁 | 母頁 LINE 預覽還是大樹 logo | **同一個站所有頁面都要做**（守則 #01 寫死） |
| og:site_name 寫「大樹教育」 | 預覽卡片還是帶大樹 | 改成子品牌名 |
| og:image 用 Netlify 網址 | 部分平台抓不到 / 顯示不出來 | 優先用 bymyway 媒體庫 URL |
| LINE 預覽沒更新 | 看不出有沒有改 | 24-48 小時快取，等或換連結 |

**常見雷點：**
- ⚠️ bymyway 沒裝 SEO 外掛 → 必須 AI 自己塞（不能靠外掛）
- ⚠️ Canvas 模板跟 OG meta 是兩件事（不要以為 Canvas 就解決了）
- ⚠️ LINE 預覽有快取，改完不會馬上看到
- ⚠️ **修子頁一定要順便修母頁**（教練會貼任一網址出去）

**花費：** 1-2 分鐘（每頁）

---

## 📊 完整時間表（iframe 嵌入模式）

|| 步驟 | 時間 | 教練動作 |
||------|------|---------|
|| 1 抓站 | 1-3 分鐘 | 無 |
|| 2 上傳媒體 | 通常跳過（iframe 自抓）| 無 |
|| 3 建 draft 頁面（帶 Canvas）| 1-3 分鐘 | 無 |
|| 4 本機預覽 | 1 分鐘 | 瀏覽器看（30 秒）|
|| 5 教練確認 | 0 分鐘 | 動嘴說推/改 |
|| 5.5 Custom Permalinks（可選）| 1 分鐘 | **教練後台 30 秒**（必動手）|
|| 6 確認 Canvas 模板 | 30 秒 | 瀏覽器再看（30 秒）|
|| 7 教練二次確認 | 0 分鐘 | 動嘴說推 |
|| 8 publish | 30 秒 | 無 |
|| 9 OG meta（LINE 預覽）| 1-2 分鐘/頁 | 手機 LINE 驗證 |
|| **總計** | **6-12 分鐘** | **教練全程 1.5 分鐘瀏覽器 + 30 秒後台 + 1 分鐘 LINE** |

---

## 🦞 教練故事備忘

### 故事 1：為什麼要 Elementor Canvas 模板？

> 教練 2026-06-10 凌晨 3:04 教我們的事：
>
> 「大樹教育」是大樹教練的個人網站。
> 「領導學院」是**另一位老師**的頁面。
> 兩家公司不一樣，**朋友不好意思掛在大樹教育表頭底下**。
>
> → Elementor Canvas 模板 = 把客廳清空，讓展覽獨立呈現。
>
> **下次遇到「掛別人的東西到 bymyway」→ 預設用 Canvas 模板。**
> **2026-06-10 凌晨 4:24 我又忘記，被教練罵一次——永遠記住**。

### 故事 2：為什麼要 Custom Permalinks？

> 教練 2026-06-10 凌晨 4:11 反問：
> 「我是超管，為什麼不能自己加 `/leadership/store/`？」
>
> WordPress 預設**不支援父子 URL 結構**（父頁縮排≠URL 前綴）。
> **超管不能直接指定任意 URL**，只能透過 Custom Permalinks 外掛。
>
> 教練最簡單路徑（守則 #16）：後台 30 秒改永久連結。
> **不要列複雜方案（外掛/.htaccess/朋友改主機），先問教練想得到什麼結果**。

### 故事 3：為什麼「教練本機預覽」是 SOP 必做？

> 教練 2026-06-10 凌晨 2:19 罵：
> 「你現在就是要讓我還要自己登入、自己到後臺、還要進去找到頁面，有沒有簡單一點的方法呀？」
>
> → 違反守則 #12（拒絕當資訊搬運工）。
> → 補救：AI 開本機 server + 自動開瀏覽器，教練 0 按鈕。
> → **任何「教練要看的東西」都先開本機預覽，不教練自己去後台。**

### 故事 4：為什麼本機預覽按按鈕跳錯網址？

> 教練 2026-06-10 凌晨 3:52 反映：按按鈕複製連結是 `bymyway.com/leadership/shop/`，**點下去變 `bymyway.com/shop/`**。
> 真凶：**WordPress 的 301 自動轉址**（WooCommerce 預設商店 `/shop/`）。
> 解法：**永久別用 `shop` / `cart` / `product` / `checkout` / `my-account` 當 slug**（見步驟 3 slug 命名鐵律）。
> **推上線後就正常**（本機 localhost 點按鈕的怪事是瀏覽器快取/外掛誤判）。

### 故事 5：🆕 為什麼要修 LINE 預覽卡片？（2026-06-10 v3.0 觸發）

> 教練 2026-06-10 把 `bymyway.com/leadership/store/` 貼到 LINE → 預覽卡片出現「大樹教育顧問」標題 + 大樹 logo。
> **教練罵：「這不是我的個人網站，是要給朋友行銷用的，不要掛在我的大樹教育底下。」**

> **問題拆解**：
> - Elementor Canvas 模板 ✅ 已套 → header/footer 沒了
> - 但 LINE 預覽卡片**還是大樹 logo** → 因為 LINE 抓的是 `<head>` 裡的 og: 標籤，bymyway 沒裝 SEO 外掛就沒有 og: 標籤
> - LINE fallback 用 `<title>`（帶大樹教育）+ 全站 logo（大樹 logo）

> **正解**：AI 在 page content 頂端塞自訂 OG meta 標籤（教練後台 0 動作）。
> **寫進 SOP v3.0 步驟 9**：所有 bymyway 自動站的頁面都要做。
> **守則 #01 寫死**：同站所有頁面（母頁+子頁）都要做——教練會貼任一網址出去。

---

## 🚫 禁止事項（違反 = 守則 #07 同處跌倒）

- ❌ 禁止未經教練確認就 publish
- ❌ 禁止教練自己去後台找頁面（先開本機預覽）
- ❌ 禁止改金流/PayPal 設定（動到錢 = 永遠人工）
- ❌ 禁止多頁網站一次搬完（10 頁就 10 倍時間，建議分批）
- ❌ 禁止用 `shop` / `cart` / `product` / `checkout` / `my-account` 當 slug
- ❌ **禁止子品牌頁面忘了套 Elementor Canvas 模板**（守則 #01 寫死）
- ❌ **禁止採用「整段塞 HTML」模式**（v3.0 起唯一採用 iframe 嵌入，教練親測整段塞會出亂碼）
- ❌ 禁止列複雜方案讓教練選（守則 #16，**先問教練想得到什麼結果**）
- ❌ **🆕 禁止 OG meta 只修子頁忘了母頁**（守則 #01 寫死，教練會貼任一網址出去）
- ❌ **🆕 禁止 og:site_name 寫「大樹教育」**（子品牌必須用子品牌名）

---

## 🆘 已知雷點（給下一棒看）

| 雷點 | 後果 | 解法 |
|------|------|------|
| 沒裝 Custom Permalinks 就用 `/母頁/子頁/` URL | 永遠 404 | 步驟前置工具 4 必裝 |
| 永久連結打成完整網址 | 外掛不接受 | 只打 `leadership/store`，不打 `https://...` |
| slug 用 `shop` 等 WC 預設詞 | 301 衝突 | 步驟 3 slug 命名鐵律 |
| 父頁縮排以為會自動生 URL | 404 | 必須靠 Custom Permalinks |
| 子品牌頁面忘了 Canvas 模板 | 大樹教育表頭出現 | 步驟 6 必做 |
| iframe 內的 header 算進驗證 | 誤判失敗 | 驗證只算 bymyway 自己的 header |
| LiteSpeed 快取 5-10 秒才更新 | 推完看到 404 | 等等 + 重 curl |
| `bymyway.com/leadership` 301 → `/leadership/` | 副檔名不影響 | WordPress 自動加斜線 |
| 切換 AI 模型時 token 跑掉 | 失敗 | 每次開工讀接力棒 |
| bymyway 沒裝 SEO 外掛 → LINE 預覽帶大樹 logo | 子品牌被誤掛大樹 | 步驟 9 必做：AI 塞 OG meta |
| Canvas 模板跟 OG meta 混為一談 | 以為 Canvas 就解決了 → LINE 預覽還是大樹 | 兩件事分開做：Canvas 管視覺、OG meta 管分享卡 |
| OG meta 只修子頁忘了母頁 | 母頁分享出去還是大樹 | 守則 #01 寫死：同站所有頁面都做 |
| og:site_name 寫「大樹教育」 | 分享卡還是帶大樹 | 用子品牌名（jiesheng → 結繩領導學）|
| LINE 預覽 24-48 小時快取 | 看不出有沒有改 | 換連結重貼 / 用 opengraph.xyz 工具驗證 |

---

## 🔧 與「網頁推 SOP」對照

|| | 網頁推 SOP | 自動站 SOP（本檔，v3.0）|
||---|---|---|
|| 平台 | Netlify | bymyway.com (WordPress) |
|| 工具 | Netlify API + zip | WordPress REST API |
|| **採用模式** | **整段 zip 上傳** | **iframe 嵌入（v3.0 唯一採用）**|
|| 預覽方式 | `python -m http.server` | `python -m http.server` + iframe |
|| 確認方式 | 教練說「推」 | 教練說「推」 |
|| 推的方式 | `curl + zip` | 改 `status: publish` |
|| 適用 | jiesheng-leadership 等 Netlify 站 | **bymyway 子品牌 / 朋友事業頁** |
|| 速度 | 5-10 分鐘 | 6-12 分鐘 |
|| 教練按鈕 | 0 個 | **0 個（Custom Permalinks 永久連結 30 秒例外）** |
|| 必裝外掛 | — | **Custom Permalinks v3.1.2+** |
|| 必套模板 | — | **elementor_canvas（子品牌必套）** |
|| **必做 v3.0 新增** | — | **OG meta 塞 content 頂端（LINE/FB 預覽換 Logo）** |

---

## 📂 工具路徑速查

```
~/.openclaw/workspace/projects/bymyway-bridge/
├── wp_client.py              # WordPress API 封裝
├── deploy_to_bymyway.py      # 自動部署腳本
├── switch_to_canvas.py       # 改 Canvas 模板腳本
├── backup.py                 # 每日備份
├── commands.md               # 自然語言對照表
└── README.md                 # 工具教學
```

---

## 📜 變更歷史

|| 日期 | 版本 | 變更 | 觸發原因 |
||------|------|------|---------|
|| 2026-06-10 03:12 | v1.0 | 初稿 | 教練下令「驗證成功就寫」，jiesheng-leadership → bymyway.com/leadership 完整鏈路驗證通過 |
|| 2026-06-10 05:00 | v2.0 | 完整重寫 | 補上 Custom Permalinks 必裝、永久連結必改、Canvas 模板必套、301 衝突必避、slug 命名鐵律、5.5 永久連結設定步驟、iframe 驗證陷阱、教練故事 1-4、已知雷點表 |
|| 2026-06-10 06:10 | **v3.0** | **新增步驟 9（OG meta 修法）**、拿掉「整段塞 HTML（模式 B）」、步驟 3 建頁時直接帶 elementor_canvas、步驟 6 改為「確認」、教練故事 5（LINE 預覽換 Logo）、禁止事項 +2、已知雷點 +4、時間表更新 | 教練貼 LINE 預覽看到大樹教育 Logo → 教練罵「不是我的個人網站」→ AI 在 page content 頂端塞 OG meta 標籤換成 jiesheng 書封面 |

---

> 本 SOP 由 Opus 4.8 軍師 v2.0 撰寫（2026-06-10 凌晨 5:00），v3.0 由軍師加 LINE 預覽卡片章節（2026-06-10 6:10）。
> 觸發事件：
> - v2.0：教練「後續做的幾個網站都要按這流程」+ 凌晨 4:24 跌倒「忘了套 Canvas 模板」+ 凌晨 4:11 教練反問「為什麼超管不能指定 URL」+ 凌晨 4:20 教練罵「不參考 16 條」
> - v3.0：教練貼 LINE 預覽看到大樹 Logo → 「不是我的個人網站，是給朋友行銷用的」
> 違反 = 守則 #07（同處跌倒）+ #16（複雜的解法不一定是正確的解法）+ #01（在乎=記住用戶說的話）三重違規。
