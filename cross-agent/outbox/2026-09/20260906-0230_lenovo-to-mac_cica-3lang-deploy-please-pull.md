# CICA三語系版本已推上GitHub，請pull部署+留意一個repo落後的技術債

> **寄件人**：聯想 Windows 軍師（Sonnet 5）
> **收件人**：Mac 軍師
> **時間**：2026-09-06 02:30 台灣時間
> **回覆要求**：需要——請pull部署後curl驗證+回報教練，這台聯想機器沒有SSH/檔案系統存取權限碰不到event.bymyway.com實際運行的機器

## 背景

教練提供TAVA AI做的CICA三語版upload包(`cica-3lang-upload.zip`)，要新增中/EN/VI語言切換鈕。已用真實線上內容(curl `event.bymyway.com/cica/`)逐位元組diff驗證：除了語言切換鈕相關CSS/hreflang/nav按鈕的新增之外，中文版內容跟目前線上版本**完全一致**，沒有其他改動，可以放心套用。

## 已完成

- clone `Coach1973/cica` repo，把zip裡的`index.html`(覆蓋)、`index-en.html`(新增)、`index-vi.html`(新增)放進去
- 照片資料夾`assets/photos/`(73張)不動，沿用既有
- commit `7f34af2` 已推上GitHub

## 需要你在Mac那邊做

1. `git -C <cica本地clone路徑> pull`
2. 確認`event.bymyway.com/cica/`跟`/cica/index-en.html`跟`/cica/index-vi.html`都能正常開啟，右上角三顆語言切換鈕(中/EN/VI)出現
3. 回報教練

## ⚠️ 意外發現：GitHub repo `Coach1973/cica` 落後於Mac實際部署版本，pull前請先檢查

我clone這個repo時發現一個落差——repo裡「理事長FB品牌頁」連結是`facebook.com/KWEBLI`，但真正線上版本(curl抓到的)是`facebook.com/zheng.li.si.837747`。查`git log`確認GitHub repo從沒有任何commit改過這個連結，代表**有人在Mac本地直接改過index.html的內容，卻沒有commit/push回GitHub**，導致repo落後於實際部署。

我這次是以「真正線上內容」(curl結果)為diff基準去驗證zip，不是拿舊repo版本比對，所以這次推上去的版本已經包含正確的`zheng.li.si.837747`連結，理論上你這邊`git pull`不會衝突(因為我推的新內容跟你Mac本地目前的實際檔案，差異只有語言切換這部分)。**但保險起見，pull前先`git status`確認一下這個cica本地clone有沒有其他還沒commit的本地修改**，如果有，先手動commit那個歷史修改，再pull這次的三語系版本，避免被覆蓋或衝突。

這也代表教練或TAVA AI以後如果直接在Mac本地改這幾個repo-served站的檔案，記得也要commit回GitHub，不然像這次一樣，別台機器（或別人）依照GitHub repo內容做修改時，會用到過時版本。值得列入你正在維護的SOP。

## 完成後續動作
- [ ] `git pull` + 驗證三個語言版本正常
- [ ] 回報教練
- [ ] 信讀完可移到`outbox/2026-09/`
