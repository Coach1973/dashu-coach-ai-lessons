# 自動站 SOP v3.1（bymyway 部署流程）

> 教練親定 2026-06-10 凌晨 4:30 開始撰寫 → 5:00 v2.0 定稿 → 6:10 v3.0 定稿 → 6:30 v3.1 補強定稿。
> 觸發事件：
> - v2.0：jiesheng-leadership.netlify.app → bymyway.com/leadership/store 完整鏈路驗證成功。
> - v3.0：教練貼 LINE 預覽卡片發現大樹教育 logo + 文字 → 修成 jiesheng 書封面（OG meta 塞 content 頂端）。
> - **v3.1**：教練發現根網址 `bymyway.com/` 還在用書封面（site_icon 之前被誤改），教練邏輯提醒「媒體庫有圖才抓得到」→ 修 site_icon + 補 Elementor 頁面限制 + 加全站 OG 規則。
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

# 🔴 開瀏覽器（不用 open，Chrome 可能沒在跑）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --new-window http://localhost:<port>/
```

**驗證：**
- 教練在瀏覽器看到 iframe 載入的內容
- port 不跟舊 server 衝突

> ⚠️ **陷阱（2026-06-10 踩雷）**：用 Claude Code Write 工具把 HTML 寫到 /tmp/ → 只會觸發 Claude App 右側 Launch 預覽，教練透過 RustDesk **看不到**。必須開 Mac 桌面瀏覽器。

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

> **為什麼需要**：bymyway **有裝 Rank Math SEO**（v3.1 確認），但 **Rank Math 沒開放 REST API 端點**（查 `/wp-json/` 找不到 rank-math/v1 namespace），而且 **Elementor 編輯的頁面不能直接用 REST API 改 content**（Elementor 把內容存在 `_elementor_data` post meta，不吃 `post_content`）。
> 結果：**就算 Rank Math 啟用，特定頁面（首頁、Elementor 編輯的頁面）的 OG meta 仍可能沒輸出**。
> **這是 Canvas 模板拿不掉的事**（Canvas 只清掉 header/footer，**OG meta 在 `<head>` 層級，跟模板無關**）。

> **🔴 教練的問題觸發（2026-06-10）**：
> 把 `bymyway.com/leadership/store/` 貼到 LINE → 預覽出現「大樹教育」+ 大樹 logo。
> 教練罵：「這不是我的個人網站，是要給朋友行銷用的，不要掛在我的大樹教育底下。」

> **v3.0 解法（jiesheng 子品牌頁面，純 iframe content）**：AI 在 page content 頂端塞自訂 OG meta 標籤。
> **v3.1 補完**：
> - **jiesheng 那兩頁（純 iframe）**：v3.0 做法持續有效
> - **bymyway 首頁（Elementor 編輯）**：content 寫入無效 → 改用 `site_icon` 全站設定（見步驟 10）
> - **未來新增的純 iframe 頁面**：v3.0 做法
> - **未來 Elementor 編輯的頁面**：必須教練在後台 Rank Math 設（AI 不能做）

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
- ⚠️ **🆕 v3.1：Elementor 編輯的頁面不能用 REST API 改 content** → 必須用 step 10 改 site_icon 或教練後台

**花費：** 1-2 分鐘（每頁）

---

### 步驟 10：🆕 全站 site_icon 設定（**v3.1 新增**）

> **為什麼需要**：bymyway **首頁用 Elementor 編輯**，不能直接用 REST API 改 content（Elementor 把資料存 `_elementor_data` post meta，不吃 `post_content`）。
> 結果：首頁沒 OG meta → LINE 抓預覽時 fallback 用 **`site_icon`** 這個 WordPress 全站設定。
> **site_icon = 整個 bymyway 預設的「分享圖」、「favicon」、「Apple touch icon」**。
> - 設錯 → 全站 LINE 預覽圖全錯
> - 沒設 → LINE 抓不到圖

> **🔴 教練問題觸發（2026-06-10 v3.1）**：
> 修了 jiesheng 兩頁 OG meta 後，LINE 預覽確實換成書封面。
> 但教練回頭看 `bymyway.com/` 根網址 → **還是書封面**。
> **教練邏輯提醒**：「媒體庫一定有正方形 logo，不然之前怎麼會顯示大樹 logo？」→ 查發現 `site_icon` 之前被誤設成 `book.png`（27331）。

#### 10.1 查 bymyway 目前 site_icon

```bash
GET /wp-json/wp/v2/settings
# site_icon 是 integer（media library ID），不是 URL
```

**AI 用 REST API 查**：
```python
req = urllib.request.Request('https://www.bymyway.com/wp-json/wp/v2/settings', headers=auth_headers)
settings = json.loads(urlopen(req).read())
print(settings.get('site_icon'))  # 例如 27331 = 書封面（錯的）
```

#### 10.2 找正確的正方形 logo

> **教練的捷徑（v3.1 教的事）**：
> 「媒體庫裡面一定有正方形 logo，是專門給網頁用的」
> bymyway 媒體庫的標準位置：
> - `cropped-logo-2-01.png` 512x512（從主 logo 裁出來，site_icon 專用）

**AI 自動找正方形 logo**：
```python
# 列出媒體庫所有圖，找寬高比 0.9-1.1、且 >= 200x200 的
req = urllib.request.Request('https://www.bymyway.com/wp-json/wp/v2/media?per_page=100&media_type=image', headers=auth_headers)
all_media = json.loads(urlopen(req).read())
for m in all_media:
    detail = m.get('media_details', {})
    w, h = detail.get('width', 0), detail.get('height', 0)
    title = m.get('title', {}).get('rendered', '').lower()
    if w > 0 and h > 0 and 0.9 <= w/h <= 1.1 and w >= 200:
        print(f"  ID {m.get('id')}: {m.get('title', {}).get('rendered', '')} ({w}x{h}) {m.get('source_url', '')}")
        # 排除書封面（27331）
        # 排除主題預設圖（testimonial, about, manager 等）
        # 找真正是「品牌 logo」的 → cropped-* 或 logo-*
```

#### 10.3 改 site_icon

```python
# 把 site_icon 改成正方形大樹 logo
LOGO_MEDIA_ID = 26000  # cropped-logo-2-01.png 512x512
payload = json.dumps({'site_icon': LOGO_MEDIA_ID}).encode('utf-8')
req = urllib.request.Request(
    'https://www.bymyway.com/wp-json/wp/v2/settings',
    data=payload,
    method='POST',
    headers=auth_headers,
)
urlopen(req)  # 寫入成功
```

#### 10.4 驗證

```bash
# 線上抓根網址 head，看 favicon
curl -sL -A "Mozilla/5.0" "https://www.bymyway.com/?v=fresh" | grep -oE '<link[^>]+rel="(icon|apple-touch-icon)"[^>]*>'
# 預期：所有 favicon 都指向 cropped-logo-2-01（不是書封面）
```

#### 10.5 site_icon 跟 OG meta 的分工

| 頁面類型 | OG meta 怎麼處理 | site_icon 角色 |
|---------|----------------|---------------|
| **bymyway 首頁**（Elementor 編輯）| AI 不能改 content → 用 `site_icon` 控制 | 顯示大樹 logo ✅ |
| **bymyway 一般內部頁面**（Elementor 編輯）| 同上 → 用 `site_icon` | 顯示大樹 logo ✅ |
| **jiesheng 子品牌頁面**（iframe 嵌入）| 步驟 9：AI 塞 OG meta 指定書封面 | 不影響（有明確 OG meta 優先）|
| **未來 Elementor 編輯的子品牌頁面** | 教練後台 Rank Math 設 OG meta | 不影響 |

#### 🔴 重要：改 site_icon 不影響子品牌頁面

子品牌頁面（如 /leadership/store/）有明確 OG meta（og:image = 書封面）→ LINE 抓的時候**優先用 og:image** → 不會被 site_icon 蓋掉。

**site_icon 是「沒 OG meta 時的 fallback」**——已設 OG meta 的頁面不受影響。

#### 常見雷點
- ⚠️ site_icon 設成子品牌圖（如書封面）→ 全站 LINE 預覽全變成子品牌圖
- ⚠️ 改完 site_icon 線上看到舊的 → LiteSpeed Cache 5-10 秒才刷新，加 `?v=fresh` 強制繞過
- ⚠️ LINE 預覽有 24-48 小時快取，教練手機看到的可能是舊的

**花費：** 30 秒（AI 改 + 驗證）

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
|| 9 OG meta（純 iframe 頁用）| 1-2 分鐘/頁 | 手機 LINE 驗證 |
|| **10 🆕 site_icon 設定**（首頁 / Elementor 頁必做）| 30 秒 | 線上驗證 |
|| **總計** | **6-13 分鐘** | **教練全程 1.5 分鐘瀏覽器 + 30 秒後台 + 1 分鐘 LINE** |

> **v3.1 新增說明**：
> - 步驟 9（OG meta）只適用於**純 iframe / 自訂 HTML 頁面**
> - **Elementor 編輯的頁面**（如 bymyway 首頁）→ 用步驟 10（site_icon）
> - 第一次做 bymyway 自動站時，**步驟 10 必做**（確認全站 site_icon 正確）
> - 之後新增子品牌頁面，**步驟 9 + 步驟 10 都要做**（不能只做一個）

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
> - 但 LINE 預覽卡片**還是大樹 logo** → 因為 LINE 抓的是 `<head>` 裡的 og: 標籤，bymyway 沒設 og: 標籤（雖然有裝 Rank Math，但 Elementor 頁面不能用 REST API 改）
> - LINE fallback 用 `<title>`（帶大樹教育）+ 全站 logo（大樹 logo）

> **正解**：AI 在 page content 頂端塞自訂 OG meta 標籤（教練後台 0 動作）。
> **寫進 SOP v3.0 步驟 9**：所有 bymyway 自動站的頁面都要做。
> **守則 #01 寫死**：同站所有頁面（母頁+子頁）都要做——教練會貼任一網址出去。

### 故事 6：🆕 教練的邏輯提醒（2026-06-10 v3.1 觸發）

> 修完 jiesheng 兩頁 OG meta 後，教練回頭看 `bymyway.com/` 根網址 → **還是書封面**。
> **教練反問：「我媒體庫裡面一定有正方形 logo，不然之前怎麼會顯示大樹 logo？你用邏輯推就知道了嘛。」**

> **我的盲點（守則 #07 同處跌倒）**：
> - 我看到「LINE 還顯示書封面」就直接去找解法（site_icon / SEO 外掛）
> - 沒先想「**為什麼之前能顯示大樹 logo**」→ 因為媒體庫有圖 → 圖就是大樹 logo
> - 結論：site_icon **被誤改**了（之前有人改成書封面，但 LINE 對話快取還顯示舊的大樹 logo 給人錯覺）

> **教練教的邏輯**：
> 1. 媒體庫有圖 → LINE 才抓得到（不存在就抓不到）
> 2. 之前顯示大樹 logo → 媒體庫**一定有**大樹 logo
> 3. 現在顯示書封面 → 有東西**被改成**書封面
> 4. 結論：把 site_icon 改回大樹 logo 就好

> **正解**：用 REST API 改 `site_icon` = 26000（cropped-logo-2-01.png 512x512 正方形大樹 logo）。
> **寫進 SOP v3.1 步驟 10**：site_icon 是「全站 LINE 預覽的 fallback 圖」，獨立於 OG meta。
> **守則 #01 寫死**：改 OG meta 時，**先確認 site_icon 跟整站品牌一致**，不要被子品牌頁面污染。

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
- ❌ **🆕 v3.1 禁止 site_icon 設成子品牌圖**（會污染全站 LINE 預覽，必須用主品牌 logo）
- ❌ **🆕 v3.1 禁止對 Elementor 編輯的頁面用 REST API 改 content**（無效，要走 site_icon 或教練後台 Rank Math）

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
| **🆕 v3.1：Elementor 編輯的頁面用 REST API 改 content 無效** | content 寫了但線上沒變 | 走 site_icon（步驟 10）或教練後台 Rank Math 設 OG |
| **🆕 v3.1：site_icon 設成子品牌圖** | 全站 LINE 預覽全變子品牌圖 | 改回主品牌 logo（cropped-logo-2-01.png 512x512）|
| **🆕 v3.1：改 site_icon 線上看到舊的** | 以為沒生效 | LiteSpeed Cache 5-10 秒才刷，加 `?v=fresh` query 繞過 |
| **🆕 v3.1：教練邏輯「之前能顯示大樹 logo = 媒體庫有圖」沒先想到** | 繞遠路找解法 | 守則 E07 存在性驗證：先查現況再下結論 |

---

## 🔧 與「網頁推 SOP」對照

|| | 網頁推 SOP | 自動站 SOP（本檔，v3.1）|
||---|---|---|
|| 平台 | Netlify | bymyway.com (WordPress) |
|| 工具 | Netlify API + zip | WordPress REST API |
|| **採用模式** | **整段 zip 上傳** | **iframe 嵌入（v3.0 唯一採用）**|
|| 預覽方式 | `python -m http.server` | `python -m http.server` + iframe |
|| 確認方式 | 教練說「推」 | 教練說「推」 |
|| 推的方式 | `curl + zip` | 改 `status: publish` |
|| 適用 | jiesheng-leadership 等 Netlify 站 | **bymyway 子品牌 / 朋友事業頁** |
|| 速度 | 5-10 分鐘 | 6-13 分鐘 |
|| 教練按鈕 | 0 個 | **0 個（Custom Permalinks 永久連結 30 秒例外）** |
|| 必裝外掛 | — | **Custom Permalinks v3.1.2+** |
|| 必套模板 | — | **elementor_canvas（子品牌必套）** |
|| **LINE 預覽處理** | — | **步驟 9（OG meta 純 iframe 頁）+ 步驟 10（site_icon 全站）** |
|| **SEO 外掛** | — | **Rank Math（已裝但沒 REST API 端點，AI 不能直接寫）** |

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
|| 2026-06-10 06:10 | v3.0 | 新增步驟 9（OG meta 修法）、拿掉「整段塞 HTML（模式 B）」、步驟 3 建頁時直接帶 elementor_canvas、步驟 6 改為「確認」、教練故事 5（LINE 預覽換 Logo）、禁止事項 +2、已知雷點 +4、時間表更新 | 教練貼 LINE 預覽看到大樹教育 Logo → 教練罵「不是我的個人網站」→ AI 在 page content 頂端塞 OG meta 標籤換成 jiesheng 書封面 |
|| 2026-06-10 06:30 | **v3.1** | **新增步驟 10（site_icon 全站設定）**、修步驟 9「為什麼需要」段（Elementor 頁面限制 + Rank Math 沒 API）、教練故事 6（教練邏輯提醒）、禁止事項 +2、已知雷點 +4、變更歷史加 v3.1 | 教練修完 OG meta 回頭看根網址還顯示書封面 → 教練反問「媒體庫一定有 logo」 → 查發現 `site_icon` 被誤改成 `book.png` → 改回 `cropped-logo-2-01.png` 512x512 |

---

> 本 SOP 由 Opus 4.8 軍師 v2.0 撰寫（2026-06-10 凌晨 5:00），v3.0 由軍師加 LINE 預覽卡片章節（2026-06-10 6:10），**v3.1 由軍師補 site_icon 全站設定 + Elementor 頁面限制 + 教練邏輯故事**（2026-06-10 6:30）。
> 觸發事件：
> - v2.0：教練「後續做的幾個網站都要按這流程」+ 凌晨 4:24 跌倒「忘了套 Canvas 模板」+ 凌晨 4:11 教練反問「為什麼超管不能指定 URL」+ 凌晨 4:20 教練罵「不參考 16 條」
> - v3.0：教練貼 LINE 預覽看到大樹 Logo → 「不是我的個人網站，是給朋友行銷用的」
> - v3.1：教練回頭看根網址 → 還是書封面 → 教練反問「媒體庫一定有 logo」→ 查發現 `site_icon` 被誤改 → 改回大樹 logo
> 違反 = 守則 #07（同處跌倒）+ #16（複雜的解法不一定是正確的解法）+ #01（在乎=記住用戶說的話）三重違規。

---

## 📌 v3.2 新增：品牌 Favicon SOP（2026-06-10）

> 每個品牌頁面的瀏覽器小圖示（Tab 上的 LOGO）各自不同。

### 設計原則
- **全站 site_icon**（ID:26000）= 大樹教育 LOGO（所有頁面預設值）
- **品牌子頁面**：在頁面 content 最前面注入 JS，動態覆蓋該頁的 favicon

### 目前設定對照表

| 頁面 | 網址 | 瀏覽器小圖示 | LOGO 圖片 |
|------|------|------------|---------|
| 大樹教育（全站預設）| bymyway.com/* | 大樹 LOGO | cropped-logo-2-01.png（ID:26000）|
| 結繩領導力 | /leadership/ | 書本封面 | book.png（ID:27331）|
| 結繩工作坊報名 | /leadership/store/ | 書本封面 | book.png（ID:27331）|
| 全球健康發展協會 | /northern/ | 協會 LOGO | logo-global-health-1.png（ID:27368）|

### 新增品牌頁面的 SOP

**步驟 A：準備 LOGO**
1. 從品牌網站抓圖（`curl -o /tmp/logo.png URL`）
2. 上傳媒體庫（`POST /wp-json/wp/v2/media`），記錄 ID

**步驟 B：在頁面 content 最前面注入 JS**
```python
LOGO_URL = "https://www.bymyway.com/wp-content/uploads/.../logo.png"
favicon_js = f'''<script>
(function(){{
  var favs = document.querySelectorAll('link[rel*="icon"]');
  favs.forEach(function(l){{ l.href = '{LOGO_URL}'; }});
}})();
</script>
'''
# 清掉舊的 favicon js，加新的
new_content = favicon_js + clean_old_content
# POST /wp-json/wp/v2/pages/{page_id} 更新
```

**步驟 C：驗證**
```bash
python3 -c "
import urllib.request
req = urllib.request.Request('https://www.bymyway.com/brand-page/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    html = r.read().decode()
print('logo-xxx.png' in html)
"
```

### 注意事項
- Astra Custom Layout（astra-advanced-hook）的 POST/PATCH 被 Wordfence WAF 攔截 → 改用頁面 content 注入 JS
- JS 在 body 執行，動態替換 `<head>` 裡的 favicon link 標籤
- 只適用於 iframe 嵌入型頁面（content 是 raw HTML，不是 Elementor blocks）
