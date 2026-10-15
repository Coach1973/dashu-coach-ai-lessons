# 任務：榮樹下網站改版（大樹教練 2026-10-15 交辦）

你在 Coach1973/rongtree 倉庫。這是大樹教練（吳大樹）的 Podcast 品牌「榮樹下」網站，正式網址 https://event.bymyway.com/curated/rongtree/ 。

## 最重要的規定
- main 分支一推上去，正式網站就會自動換新（GitHub webhook）。所以只能在分支 `claude/rongtree-redesign` 上工作和推送。絕對不要推 main，不要開 PR，不要合併。
- 只改 index.html（必要時可以在 img/ 加新檔）。不要動 interview-flow.html、invite.html、volunteer.html、pledges.json。
- 不能改伺服器。頁面用到的 /api/rongtree/episodes、/api/rongtree/prep、/api/works/contact、/static/nav-burger.js 都在教練的 Mac 上，照原樣呼叫，網址不要改。
- 全部用繁體中文、白話。網頁上所有字最小 20px（教練規定，任何 font-size 或 font 簡寫都不能小於 20px）。
- 不要編造集數、來賓或數字，資料一律來自現有頁面內容或 /api/rongtree/episodes。

## 要做的兩件事

### 1. 主題區塊改成「文字標題＋超連結」清單
目前 id="eco"，標題「從樹上垂下的根，都扎進了真實的土地。」，四張大卡：榮樹下 IP‧商業導師席／讓電長在需要的地方／讓土地重新值錢／Run for Future 2027。
教練說主題會越來越多，要更精緻。現有圖片保留（可以縮成小圖），排版改成清單：每個主題一行，有標題、一句說明、超連結。以後加主題只要多加一行。四張卡原本的連結都要保留。
教練口中這四個主題叫：媒體與導師、綠能科技、生命農業與水、公益路跑。

### 2. Podcast 節目單和百集計畫合併成一區
目前「節目單」（id="episodes"）和「100 集，100 位領跑人」（id="hundred"）分開，要往下滑很多。
合併成一區，做成 1 到 100 的格子：
- 已播出的集數亮起來。資料來自 /api/rongtree/episodes，回傳格式 `{ok, episodes:[{id, url, title, version, desc, dur, date}]}`，目前 8 筆。
- 其他格子空著，寫「等你」之類的字，當作嘉賓招募。
- 點已播出的格子：在頁面上展開或彈出那一集的完整內容（標題、日期、長度、介紹、SoundOn 收聽連結）。如果那一集的來賓在現有頁面裡已經有個人網頁連結，也一起放。
- 點空格子：帶到「我也想坐上嘉賓席」那一區。
- 手機上要好按，格子不能太小。
- 保留原本兩區的精神（「100 集，100 位領跑人」這句要留）。
- 頂部選單和漢堡選單（nav-burger.js 的 data-links）裡的錨點要跟著更新，不能有斷掉的連結。

## 做完要
1. 在分支 `claude/rongtree-redesign` 上 commit 並 push。
2. 在同一個分支新增 `docs/to_junshi/2026-10-15_rongtree_redesign.md`，用白話寫：改了什麼、哪些錨點或連結改了、你怎麼驗證的（手機寬 400px 和桌機寬度都要看）、還有沒做完或不確定的地方。
3. 不要請教練做任何事。有疑問就寫在那封信裡，Mac 上的軍師會處理、驗收，然後才上線。
