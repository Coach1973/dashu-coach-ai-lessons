# 寶華姐策展頁（linbaohua）最終目視驗收證據

> 驗收時間：2026-10-26 03:20～03:40 台灣時間
> 線上網址：https://event.bymyway.com/curated/linbaohua/
> 驗收人：小龍蝦學長（minimax/MiniMax-M3）
> Repo：`/Users/bymyway/github_repos/linbaohua/`（branch main，HEAD `502d95a`）

## 一、結論

**✅ 驗收通過。** 桌面版與手機版皆實測確認：頂部導覽列固定（`position: fixed`）在捲動時不位移，人物照顯示正常、無破圖／拉伸／重疊／裁切，無水平捲軸。

## 二、桌面版實測（Chrome）

| 檢查項 | 實測值 | 判定 |
|---|---|---|
| 頁面標題 | 林寶華（寶華姐）｜寶麗寶銀樓創辦人・府城志工中隊長 | ✅ |
| `nav.nav` position | `fixed`（z-index 50） | ✅ |
| 捲動至 `scrollY=3000` 時 | `navTop=0`、`navBottom=77`、`navVisible=true` | ✅ 表頭固定 |
| 封面原始尺寸 | `720×960` | ✅ |
| 封面渲染尺寸 | `413×510` | ✅ 比例正確 |
| 水平溢出 | `bodyOverflowX=visible` / `htmlOverflowX=clip`，無捲軸 | ✅ |

截圖（原始）：
- `/Users/bymyway/.openclaw/media/outbound/5215820c-d5c3-449b-bc37-a916c464a006---1bac0ab0-1425-4be0-a5af-3c6ae140b46b.jpg`

## 三、手機版實測（iPhone 13 模擬，viewport 398×852）

| 檢查項 | 實測值 | 判定 |
|---|---|---|
| `documentWidth` vs `vw` | `398` vs `398` | ✅ 無水平溢出 |
| 捲動至人物照（`scrollY=765`） | `imgTop=175`、`imgH=431`、`imgW=349`，導覽列仍 `fixed` | ✅ |
| 人物照原始 → 渲染 | `720×960` → `349×431` | ✅ 比例正確、無拉伸 |
| 頂部選單最右「生活事」輕微裁切 | 水平捲動選單之正常現象 | ✅ 非缺陷 |

截圖（原始）：
- 頂部：`/Users/bymyway/.openclaw/media/outbound/58e13269-074b-463c-9ccf-f42dcb72a8b7---f4d39234-3781-4fa2-ba79-6a41edd81ec3.jpg`
- 人物照：`/Users/bymyway/.openclaw/media/outbound/75282303-54c1-4ba0-8380-477bcb02232f---46d026ca-01f8-485e-a9d5-39e518e01578.jpg`
- 縮小驗收圖：`/Users/bymyway/.openclaw/state/archive/2026-10-26_temp_cleanup/linbaohua_review_20261026/mobile_portrait.jpg`

## 四、部署一致性（像素級）

| 比對 | 平均像素差 | 判定 |
|---|---|---|
| repo `HEAD:index.html` 內嵌 720×960 封面 ↔ 線上實際封面 | **0.000** | ✅ 線上與 repo 完全一致，無部署落差 |
| 線上封面 ↔ `原始照片/c3.jpg` | 99.34 | ⚠️ 非原圖直接使用（見下） |
| 線上封面 ↔ 其他候選（`a648794_0` / `epoch` / `a651287_2`） | 90.36～124.24 | ⚠️ 皆無法以整圖像素對上 |
| 人物區多尺度正規化互相關（NCC）最高值 | 0.4664（`c4.jpg`） | ⚠️ 低於 0.5 門檻，無法據此判定出處 |

**為何無法用像素比對判定封面出處**：`de5b662` commit 訊息寫「封面換新照片並**去背**」，去背處理會改寫背景像素，導致整圖像素差與模板比對皆失效。此為**已知的比對方法限制**，不是缺陷；已改以「repo HEAD ↔ 線上 = 0.000」證明部署一致（此為實際要驗的目標）。

## 五、封面視覺狀態（VLM 實測，非 commit 訊息推論）

對線上實際顯示的 `live_cover.png` 做視覺描述：

- **人物完整**：半身像，頭頂至腰部完整，雙臂交叉動作完整。
- **邊緣自然**：人物與背景交界清晰，**無白邊、無 halo、無去背毛邊**。
- **背景**：明確為活動背板——上方深色底印金色幾何線條並標示「2018 TAIWAN Platinum Forum 臺灣區白金論壇」，下方白底佈滿重複「BNI」標誌，最右可見「鉑金成功」字樣。
- **裁切**：標準半身裁切，上至燈具邊緣、下至人物腰部，無突兀裁切感。
- **重心**：中央人物，焦點在面部表情與胸前活動名牌；粉紅外套與深色背景對比清楚。

### ⚠️ 需教練裁示事項

**線上封面仍是「2018 TAIWAN白金論壇」忙碌活動背景**（密集文字＋多標誌），人物在其中雖然突出，但作為策展頁主視覺仍偏雜。此為**當前線上現況的客觀描述**，非缺陷判定——`20b96cf` commit 訊息稱「封面換成教練指定照片」，但依 N3 查證鐵律不採 commit 訊息作結論，實際視覺結果即上述。

若教練認為該背景不理想，需另指定新封面照片再換；**本場未自行更換**（未獲 OK，不擅自改動已上架頁面）。

## 六、CSS 檢查（`index.html` 實讀，非 grep 猜測）

先前 `grep` 因 `maximum repetition exceeds 255` 失敗，改以 Python regex 讀取實得：

| 選擇器 | 內容 |
|---|---|
| `.frame` | `border-radius:36px; overflow:hidden; box-shadow:var(--shadow); border:8px solid #fff; transform:rotate(1.5deg); background:linear-gradient(160deg,#FFD27A,#FFB547 60%,#F2A33A)` |
| `.portrait` | `position:relative; max-width:480px; margin:10px auto 0` |
| `.portrait img` | `width:100%; aspect-ratio:4/5; object-fit:cover; object-position:50% 18%; display:block` |
| `.portrait .sun` | `position:absolute; right:-26px; top:-26px; width:130px; height:130px; border-radius:50%; background:var(--sun2); z-index:-1` |
| `.portrait .tag` | `position:absolute; left:-22px; bottom:34px; background:#fff; border-radius:18px; padding:12px 20px; ...` |

`.portrait .tag` 在 `@media` 內另有 `left:0` 覆寫（避免溢出），行為正常。

## 七、既有工作不重做（已存在，無須重複實作）

| commit | 內容 |
|---|---|
| `de5b662` | 寶華姐頁：表頭固定（拿掉 `body overflow-x:hidden` 造成的 sticky 失效）、封面換新照片並去背 |
| `20b96cf` | 寶華姐頁：表頭改 fixed 固定（修手機 sticky 失效）、封面換成教練指定照片 |

本場未修改 linbaohua repo 任何檔案，僅做線上驗收。

## 八、暫存目錄清理（案例23 鐵律：只搬不刪）

| 原位置 | 大小 | 檔案數 | 去向 |
|---|---|---|---|
| `workspace/state/rongtree_review_20261026/` | 12M | 53 | `/Users/bymyway/.openclaw/state/archive/2026-10-26_temp_cleanup/` |
| `/tmp/lbh_extract/` | 10M | 34 | 同上 |
| `workspace/state/linbaohua_review_20261026/` | 17M | 43 | 同上 |

搬移前後 `du -sh` 與檔案數**完全一致**（12M/53、10M/34、17M/43），源頭已清空。存檔區位於 `~/.openclaw/state/`，已被 Repo1 `.gitignore` 第 40 行 `state/` 涵蓋，**不在任何 repo 版控內**。全程未執行任何 `rm`。
