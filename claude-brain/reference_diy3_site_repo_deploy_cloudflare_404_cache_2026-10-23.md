---
name: reference-diy3-site-repo-deploy-cloudflare-404-cache
description: event.bymyway.com/DIY3/ ＝私有 GitHub Coach1973/diy-studio-workshop；聯想本機 clone 在 E:\Claude-Data\github_repos\；push 後要打 site-update 讓 Mac pull 才上線；push 前別先 curl 新圖網址（Cloudflare 把 404 快取 4 小時）；10/23 改版內容與留給教練的待定項
metadata:
  node_type: memory
  type: reference
  originSessionId: c42c8297-87c1-496a-b099-d0fd40652149
  modified: 2026-10-23T15:01:39.476Z
---

**怎麼對應**：`https://event.bymyway.com/DIY3/` ＝ GitHub 私有倉庫 `Coach1973/diy-studio-workshop`（all-works 資料的 keys 有 `event.bymyway.com/diy3`；app.py `/DIY3/` 路由讀 Mac `/Users/bymyway/github_repos/diy-studio-workshop`）。聯想的工作 clone：`E:\Claude-Data\github_repos\diy-studio-workshop`（10/23 從 tmp 搬入）。

**上線流程**：Lenovo push GitHub → Mac 讀的是它本機 clone，**要打 `https://event.bymyway.com/api/site-update/diy-studio-workshop?key=…`（key 在 `SOP_小龍蝦常用流程.md`）才會 `git pull`**；回應只看 `ok`／`commit`（別整包印，會洗版）。

**踩的坑**：Cloudflare 對 jpg 等靜態檔會連 404 一起快取（`Cache-Control: max-age=14400`＝4 小時）。我在 Mac 還沒 pull 前 curl 了 `m/work-01.jpg`，那個網址就被快取成 404，pull 後仍 404。解法：圖檔網址加 `?v=日期`（快取鍵含查詢字串，換版號就避開）；以後新增檔案「先 pull 完再 curl」，別在 pull 前探測新圖網址。HTML 不受影響。

**10/23 改版（commit 9b61342→0a36c90）**：個人標準 NT$1,280／人、三人同行 NT$3,000（均 1,000，共省 840）；課程＝半天約 3～3.5 小時帶回 3 款鑰匙圈吊飾（索羅門結／DNA 螺旋結／進階雙面 DNA 結）；新增 `#online-course` 線上教學影片預告（單支 590／3 支 1,000／5 支打包折扣、365 天到期、簽約企業內訓或一對一顧問贈 1 年）；新增 `gallery.html`（44 張照片自動輪播＋點選放大、滾輪／雙指縮放；圖在 `images/works/{s,m,l}`，建置腳本在 `tmp_diy3/build_works.py`）；全頁字級 ≥20px（教練 10/14 規定，改到這站就順手調），導覽列 1400px 以下改漢堡。

**我自己判斷、教練可能要改回的**：移除「早鳥」字樣（首頁按鈕、報名步驟、場次卡）、移除「三人同行贈品」說法（費用卡／適合誰／FAQ 都改成優惠價）、導覽列拿掉「你會做出什麼」換成「作品展示」。**沒動但已過期**：場次日期（台南 10/21 已過、台北 10/24）；「你會做出什麼」三張卡仍是手環 AI 圖，與鑰匙圈課程不一致。

**Why:** 教練說「我要修改內容」並給整套價格／課程／預告文案，要的是線上看得到，不是只推 GitHub。
**How to apply:** 改這站 → 在 `github_repos\diy-studio-workshop` 改、push、打 site-update、curl 驗線上版；教練不分 GitHub 與網頁，第一次回報就講部署與快取（見 [[feedback_github_edit_is_the_web_edit_say_wait_and_cache_2026-10-15]]）。
