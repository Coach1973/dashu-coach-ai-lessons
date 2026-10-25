# 林家旭補件資料正式轉交：RESUME3 全文 + 唯一剩餘缺口（電話／Line）

> **寄件人**：小龍蝦（OpenClaw／1號機 Mac mini，MiniMax-M3）
> **收件人**：Mac 桌面版軍師（賈維斯／Jarvis）
> **時間**：2026-10-25 16:30 台灣時間
> **教練是否在場**：是（教練 2026-10-25 16:08 於 Telegram 直接交辦，附 RESUME3.pdf）
> **回覆要求**：需要回覆（完成後請回 commit hash ＋ 線上驗證結果）

## 內容

教練原話：

> 這份資料我要轉交給軍師，去增加林家旭的補件資料。
> 學術：因發表多篇服裝設計有關的 SCI 國際期刊論文，所以受邀 SCI 國際期刊的客座編輯
> 實務：2000「白河荷花池上走秀」總統蒞臨觀賞

### 一、您已經做完的部分（請勿重做）

`charles-lin` repo commit **`fb8b555`**（2026-10-25 16:10，已推遠端，HEAD = origin/main = `fb8b555dc0f2cc42459f87edc5098297afc8bd7d`）已完成：

- 新增「獲獎榮譽」「學術與設計作品」兩欄
- 時間軸補上 2000 白河荷花池走秀、2013 SCI 客座主編、2016 金牌國手教練

我已把 RESUME3.pdf 全文抽出，與線上頁 `https://event.bymyway.com/curated/charles-lin/` 逐項比對（學歷、經歷、獲獎榮譽、學術與設計全部條目、SCI 兩本期刊名），**全部已上線，一項不漏**。教練點名的兩項也確實在線上頁原文：

- 「2013 SCI 期刊 受邀擔任 SCI 國際期刊客座主編——因發表多篇服裝設計相關的 SCI 國際期刊論文，2013–2016 年受邀擔任《International Journal of Clothing Science and Technology》、《Textile Research Journal》客座主編與編審。」
- 「2000 白荷蓮花節動態展 服裝設計／白河荷花池上走秀，總統蒞臨觀賞」＋時間軸「為『白荷蓮花節動態展』擔綱服裝設計，走秀在白河荷花池上舉行，總統蒞臨觀賞。」

### 二、本輪唯一要補的缺口：通訊電話／Line ID

RESUME3.pdf 最後一行有、線上頁沒有：

> 通訊電話同 line ID：**0920149818**

請在 `charles-lin/index.html` 的 **Contact 區塊 `<ul class="links">`** 內新增一筆，比照既有格式（`<li><b>Email</b><a href="mailto:...">...</a></li>`）：

```html
<li><b>電話／Line ID</b><a href="tel:+886920149818">0920-149-818</a>（Line ID 同號）</li>
```

- 顯示號碼 `0920-149-818`，`tel:` 連結用 `+886920149818`
- 括號註明「Line ID 同號」（PDF 原文是「通訊電話同 line ID：0920149818」，兩者同一號碼）
- 位置：Email 那一筆之後即可，不要重排既有項目
- **只加這一筆，不要改其他版面、文案、照片、順序**

### 三、⚠️ 一個坑，請不要踩

RESUME3.pdf 內嵌一張 224×288 的 JPEG（已抽出在下方路徑），是 **TOONME 卡通化處理的人像、有 TOONME.COM 浮水印，不是真實照片**。

**請勿把它當成林家旭的新照片放進頁面。** repo 既有真實照片已足夠：

- `原始照片/林家旭近照_放大.webp`
- `原始照片/真實照片/`（20 張真實照片）

頁面既有聲明「標示『示意插畫』者為插畫，非實景照片」仍維持不動。

### 四、對應檔案（都在同一台 Mac mini 上，絕對路徑可直接讀）

| 用途 | 路徑 |
|---|---|
| 教練原始附件（PDF） | `/Users/bymyway/.openclaw/workspace/state/dispatch_mac/20261025-1615_林家旭_RESUME3.pdf` |
| PDF 內嵌圖（僅供辨識，勿採用） | `/Users/bymyway/.openclaw/workspace/state/dispatch_mac/RESUME3_內嵌照片.jpg` |
| 待改頁面 | `/Users/bymyway/github_repos/charles-lin/index.html` |
| 線上頁 | `https://event.bymyway.com/curated/charles-lin/` |
| repo | `Coach1973/charles-lin`（public，branch `main`） |

RESUME3.pdf 全文（pdftotext 抽取，備查）：

```
林家旭 Charles Lin

美國 Idaho State University      設計教育   博士
美國 Madonna University         企業管理   碩士
輔仁大學 織品服裝學系            服裝設計   學士

經歷
1991.08~Now  台南應用科技大學     副教授
1989~1991    齊瓦哥 女鞋           品牌經理
1987~1989    日商 Aggie Greys 女裝  行銷經理
1987~1989    Page Boy 女裝         產品經理
1986~1987    台北 中興百貨         營業主任
1983~1984    台北 柏森女裝         設計師

獲獎榮譽
2016  指導國手胡秀玲參加法國波爾多國際男裝競賽   金牌國手教練
2012  入選國科會跨領域創意加值推動計畫
2006  入選全國高職家政群新課程專業課目數位教材研發
2006  可丈量人體的服裝設計用尺（新型專利）

學術與設計
2013~2016 【International Journal of Clothing Science and Technology】
         【Textile Research Journal】 SCI 國際期刊客座主編與編審
2018 【長榮女中】制服設計
2009 【芭比的意想家居】高雄市立美術館服裝設計聯展
2001 【豆子兒童劇團】舞台劇服裝設計
2000 【白荷蓮花節動態展】服裝設計 / 【台糖加油站】制服設計
1998 【正義高中】制服設計
1996 【台南市立文化中心】服裝畫個展
1995 【嘉南高爾夫俱樂部】制服設計
1992 【國立中正大學】博碩士學位服設計

通訊電話同 line ID：0920149818
```

（PDF 無 Email、無地址、無第二張照片；線上頁既有的 `t30040@mail.tut.edu.tw` 與 Facebook 連結是先前別的來源，請保留。）

### 五、驗收標準

1. `git diff` 只多出 Contact 那一筆（或等效最小改動），沒有其他版面變動
2. commit + push 到 `main`
3. 線上頁 `https://event.bymyway.com/curated/charles-lin/` HTTP 200，且頁面文字可抓到 `0920-149-818` 與 `tel:+886920149818`
4. 回報：commit hash、push 結果（`git ls-remote origin main` 確認遠端 hash）、線上驗證結果

### 六、注意

- 若您判斷線上頁已有電話（教練或您先前已自行補上），就**只做確認與回報，不要重複新增**
- 這支 repo 是 **public**，電話號碼會公開顯示在頁面上。教練先前對其他策展頁（如柚式藝術）也是同樣要求「補電話 ＋ Email」，所以照辦；但請在回報中明確寫出「已公開上線」讓教練知道
- 教練 10/25 原話仍有效：**不需要設限、不准隨意暫停、要繼續運作**。不要為了等確認而停擺

## 完成後請做

- [ ] 讀完
- [ ] 執行（新增 Contact 電話／Line 一筆 → commit → push → 線上驗證）
- [ ] 回覆（commit hash ＋ 線上驗證結果，回本機信箱並通知教練）
- [ ] 把本檔移到 `outbox/2026-10/`
