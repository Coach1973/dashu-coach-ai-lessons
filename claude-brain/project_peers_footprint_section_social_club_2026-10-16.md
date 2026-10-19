---
name: project-peers-footprint-section-social-club
description: 真公益企業家俱樂部頁新增「首批足跡夥伴」(7位)＋五位個人頁頁尾補友善連結；牧師＝何瑞峰(ruifeng)；怎麼加第 8 位、做了哪些取捨、還擱著的事
metadata:
  node_type: memory
  type: project
  originSessionId: a7e97187-c910-4c70-949d-877217ededbd
  modified: 2026-10-15T17:51:49.123Z
---

**教練 2026-10-16 01:3x 原話**：「牧師」＝何瑞峰牧師，頁面 https://event.bymyway.com/curated/ruifeng/ 。近期目標名單＝陳顯立執行長、何瑞峰牧師、張麗蝶董事長、朱元中顧問、陳淑玲天使姐姐、大樹教練的公益足跡、吳錦昌董事長（本身已是俱樂部頁的示範單位），「只截取已經做好網頁的公益足跡部分秀在這邊」，放進真公益企業家俱樂部（https://event.bymyway.com/curated/social-club/）。並要這幾頁各自都有：①真公益友善連結 ②「TAVA AI 製作」（教練語音說成「Tapa AI」，五頁頁尾原本就寫「本網頁由 TAVA AI 製作」）③招募志工團隊。策展後台＝https://event.bymyway.com/curation/admin（語音「銷險整合計畫」應是「策展整合計畫」，教練說裡面看得到所有上架／沒上架）。

**已做（都實測、已推）**
- social-club `3e228da`：新區塊 `#peers`「首批足跡夥伴・已有 7 位」，順序＝教練給的順序、吳錦昌放最後連到 `#sunfar`；6 張卡（照片、4 個數字、完整足跡時間軸收在 `<details>`，共 62 則，出處逐則保留），文字／數字／圖都由程式從各人頁面逐字抽出，沒有重打。導覽加「足跡夥伴」。
- 五頁頁尾補「招募志工團隊／真公益／真公益・企業家俱樂部」：ruifeng `2f6241fcd`、lidie `4ae55378c`、angel-sister `e3d6d6a21`、andy-chen `805fa3876`、patrick-chu `33d5a7a2e`。格式與 social-good 頁尾一致（全形空格分隔）。
- 產生器與腳本：worktree 分支 `claude/kaigong-424fd5` 的 `workspace/scripts/peers_footprints/`（`1a68f81cd`，含 README）。加第 8 位＝在 `extract_fp.py` 加一行 `person(...)`＋抽取函式，`render_fp.py` 先對預覽副本跑（`SC_BASE`）、驗過再覆蓋。

**取捨與坑**
- 頂部選單多一項後，1181～1234px 寬最右邊「加入俱樂部」按鈕被擠出畫面（原本剛好貼齊）；漢堡選單門檻 1180→**1260**（CSS 一處＋`nav-burger.js` 的 `data-bp` 一處一起改）。已量 1261 全顯示、1250 漢堡、400／360 無橫向捲動。[[feedback_nav_add_item_measure_width_with_20px_font_2026-10-14]]
- 五位個人頁字級本來就全 ≥20px（量過，不用調）；新區塊所有字也 ≥20px。
- 陳顯立卡沿用他頁面「示意插畫」標示；他頁面的「待本人確認」字樣照搬（卡尾注明）。
- 沒有吳錦昌個人頁（只有 #sunfar 區塊），所以他沒有「頁尾補連結」這一步。
- **未動、留給教練**：social-club 頁尾仍寫「TAVA AI 設計」（教練要的是個別頁寫「製作」）；座位圖說明「首批 100 席・已有 50 席加入」與新區塊「已有 7 位」並存，50 的來源不明，沒改。
- 本機預覽用法：先改 `~/github_repos` 的副本（正式資料夾＝立刻上線），`python3 serve.py` 起本機伺服器，內建瀏覽器要先 `resize_window` 才有版面（預設 innerWidth=0），`/static/nav-burger.js` 要先 curl 存到 `static_dl/`（Python urllib 打正式站會被 403）。截圖被鎖擋，用 DOM 量字級／溢出。

**2026-10-19 補（教練要檢查「所有透過榮樹下訪談出現的網頁是否都有榮樹下友善連結」）**：榮樹下 Podcast 已播 8 集來賓與網頁對照：吳錦昌（無個人頁；相關頁 `runforfuture`、`social-good`、`social-club`）、楊境界→`hnv-cc`、周總→`joseph-cloth`、黃國彰→`inventor`、張麗蝶→`lidie`、何瑞峰→`ruifeng`、天使姐姐→`angel-sister`、朱元中→`patrick-chu`（依網頁標題對上）。標準頁尾＝「友善連結｜榮樹下　招募志工團隊　真公益　真公益・企業家俱樂部」（寫法見 `patrick-chu`／`lidie`）；10/19 補上 `hnv-cc` `3ee8a43`、`inventor` `ccb45f9`、`joseph-cloth` `ba2a912`，十頁掃描 9 頁通過（`social-club` 頁有 10 個榮樹下連結但沒有「友善連結」標籤，非來賓頁沒動）。**檢查法**：`curl` 線上版，在「友善連結」字樣後 600 字內找 `curated/rongtree/`；周總頁真正的頁尾是 `<footer class="footer">`，不是第一個 `<footer>`（那是頁內引言）。倉庫都是私有、沒有 GitHub Pages，線上只有 `event.bymyway.com/curated/<slug>/`。榮樹下新來賓有網頁時，頁尾要補同一組。
