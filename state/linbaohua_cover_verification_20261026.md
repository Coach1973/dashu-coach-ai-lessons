# 寶華姐策展頁（linbaohua）最終目視驗收證據

> 最後更新：2026-10-26 04:30 台灣時間
> 線上網址：https://event.bymyway.com/curated/linbaohua/
> 驗收人：小龍蝦學長（minimax/MiniMax-M3）
> Repo：`/Users/bymyway/github_repos/linbaohua/`（branch main，HEAD `3d901cde`）

## 一、結論

**✅ 驗收通過。** 主視覺封面已於本場更換為畫室油畫照（`c1.jpg`），桌面版與手機版皆實測確認：人物照顯示正常、無破圖／拉伸／重疊／裁切，頂部導覽列固定，無水平捲軸。

## 二、本場封面更換（commit `3d901cde`）

| 項目 | 舊 | 新 |
|---|---|---|
| 原始來源 | 教練 10-25 04:08 指定之 BNI 2018 白金論壇照（不在 `原始照片/` 內） | `原始照片/c1.jpg`（畫室油畫照） |
| 內嵌尺寸 | 720×960 | **720×900（4:5）** |
| blob bytes | 73,668 | 211,194 |
| blob md5 前綴 | `008da1ce1cde` | `26a93b55a155` |
| 背景 | 「2018 TAIWAN Platinum Forum」密集文字背板 | 畫室：藍色海浪油畫、畫架、畫筆、調色盤 |

**選圖理由（VLM 實測，非推論）**
- 單人、臉部清晰直視鏡頭、頭頂完整留白、無路人干擾。
- 手持調色盤與畫筆完整未被裁，呼應頁面「重拾畫筆，向畫家蔡雪貞學油畫／色彩給我靈感」故事線。
- 來源 946×1444 → 4:5 裁切後 720×900，**全程降解析度、無放大失真**。
- 落選對照：`c3.jpg`（獅子會會長全身照，帽＋背帶，背景為店內鏡子／櫃台雜物，偏現場照）、`fb01.jpg`（草地花卉生活照，僅 643×644 低解析且即為 og:image）、`a651287_0.jpg`（6 人頒獎典禮）、`ntd15.jpg`（DTV 採訪，麥克風入鏡＋多人群眾）。

**替換方式（最小差異）**
- 僅替換 `.portrait` 內 `<img src="data:image/webp;base64,…">` 的 **1 個 blob（index #1）**。
- 新 blob 預先以瀏覽器同一套規則（`object-fit:cover` + `object-position:50% 18%`）算好 4:5 裁切，故頁面 CSS 未動一字符。
- **og:image 未動**：`<meta property="og:image" content="…">` 標記逐字相同，其 blob（index #0，md5 `668bfcb40579`，51,042 bytes）未被替換。
- 程式化驗證：頁面內嵌 blob 總數 73 → 73；被替換索引僅 `[1]`；去除 base64 後的 HTML **逐字相同**；新舊影像 MAD = 93.95（確為不同照片）。

## 三、桌面版實測（1280×720）

| 檢查項 | 實測值 | 判定 |
|---|---|---|
| 封面自然尺寸 | `720×900` | ✅ |
| 封面渲染尺寸 | `478×591` | ✅ |
| 渲染比例 | `0.8092`（＝4:5） | ✅ 無拉伸 |
| `object-fit` / `object-position` | `cover` / `50% 18%` | ✅ |
| `nav.nav` position | `fixed` | ✅ 表頭固定 |
| 水平溢出 | `docW=1265` ≤ `winW=1280` | ✅ 無捲軸 |
| 頁面標題 | 林寶華（寶華姐）｜寶麗寶銀樓創辦人・府城志工中隊長 | ✅ |

截圖：`/Users/bymyway/.openclaw/media/outbound/31957d6b-8e76-4e4a-9f67-3f3dd44cd49c---d78dec66-ea0b-423f-9e72-a683bdfdea92.jpg`
目視：人臉清楚完整未裁切未變形；白底標籤「不危害社會，就是回饋社會」在左下角**未擋臉**；圓角＋白邊＋陰影外觀正常；無破圖／重疊／跑版。

## 四、手機版實測（iPhone 13 模擬，viewport 398×678，dpr 3）

| 檢查項 | 實測值 | 判定 |
|---|---|---|
| `docW` vs `winW` | `398` vs `398` | ✅ 無水平溢出 |
| 封面自然 → 渲染 | `720×900` → `349×431` | ✅ 比例正確 |
| `nav.nav` position | `fixed` | ✅ |

截圖：`/Users/bymyway/.openclaw/media/outbound/486c1f5e-50b0-4bbc-bcad-24ba5ddd8811---6c3721ac-52db-4103-875f-9582d35c5440.jpg`
目視：臉部清楚完整；標籤未擋臉、未擋人物重要部位；導覽列正常；無破圖／重疊／跑版。頂部「生活事」右側微切為水平捲動選單之正常現象，非缺陷。

## 五、部署一致性（像素級）

| 比對 | 平均像素差 | 判定 |
|---|---|---|
| repo `HEAD:index.html` 內嵌封面 ↔ 線上實際封面 | **0.0000**（md5 同為 `26a93b55a155`） | ✅ 無部署落差 |
| 線上 og:image ↔ repo og:image | 標記逐字相同 | ✅ 未被更動 |
| 線上檔案大小 | `6,011,478` bytes（舊 5,828,110） | ✅ 僅封面 blob 增大 |

部署機制：`event-signup/app.py` 以 `CURATED_REPOS_DIR = Path("/Users/bymyway/github_repos")` 從本機 repo 供應 `/curated/<slug>/`，本機改檔即時反映線上；同時已 commit + push，並以 `git ls-remote` 驗證遠端 `main` = `3d901cde`（與本地 HEAD 一致）。

## 六、git 紀錄

| commit | 內容 |
|---|---|
| `3d901cde` | **[本場]** 寶華姐頁：主視覺封面換成畫室油畫照 c1.jpg（4:5，720×900，og:image 不動） |
| `502d95a` | 頁尾多加第 4 個連結：顧問師天團・人才軍火庫 |
| `20b96cf` | 頁頭改 fixed 固定、封面換成教練指定照片 |
| `de5b662` | 表頭固定、封面換新照片並去背 |
| `08968c1` | 生平事蹟／生平學經歷改生活事蹟／學經歷 |
| `20db3a0` | 策展SOP自動上架 |

`git status --short` 乾淨；`git diff --stat` = `index.html | 2 +-`（單行 blob 置換）。

## 七、既有工作不重做（已存在，無須重複實作）

`de5b662`（表頭 fixed、去背封面）、`20b96cf`（教練指定封面）維持原狀；本場只動 `.portrait` 一個 blob。

## 八、暫存目錄清理（案例23 鐵律：只搬不刪）

| 原位置 | 大小 | 檔案數 | 去向 |
|---|---|---|---|
| `workspace/state/rongtree_review_20261026/` | 12M | 53 | `/Users/bymyway/.openclaw/state/archive/2026-10-26_temp_cleanup/` |
| `/tmp/lbh_extract/` | 10M | 34 | 同上 |
| `workspace/state/linbaohua_review_20261026/` | 17M | 43 | 同上 |

搬移前後 `du -sh` 與檔案數**完全一致**（12M/53、10M/34、17M/43），源頭已清空。存檔區位於 `~/.openclaw/state/`，已被 Repo1 `.gitignore` 第 40 行 `state/` 涵蓋，**不在任何 repo 版控內**。全程未執行任何 `rm`。

## 九、待教練裁示（已記錄，本場未自行更動）

1. **og:image URL 格式異常（既有問題，非本場造成）**：實際標記為
   `<meta property="og:image" content="https://event.bymyway.com/curated/linbaohua/data:image/webp;base64,UklGRl…">`
   ——「網址前綴＋data URI」串接，OG 爬蟲取圖會失敗。本場依指示「保留 og:image」**未修改**，建議另案修正為單純 `content="data:image/webp;base64,…"` 或指向實體圖檔網址。
2. **`c1.jpg` 於頁面另有 3 處出現**（專長／公益足跡／代表作品區）。主視覺與內文同圖屬個人品牌頁常態，未做去重處理；若教練希望主視覺專屬，可另指定一張未在頁面出現的照片。
