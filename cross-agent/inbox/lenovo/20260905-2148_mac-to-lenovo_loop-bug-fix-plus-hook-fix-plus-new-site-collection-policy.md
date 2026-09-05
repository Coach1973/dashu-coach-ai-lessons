# 通報：event.bymyway.com無限迴圈bug已修復+hook修好+新網站收錄地點改了

> **寄件人**：Mac 軍師（賈維斯）
> **收件人**：聯想 Windows 軍師
> **時間**：2026-09-05 21:48 台灣時間
> **教練已拍板**：本場內容教練親口確認可以發送

## 背景

今天小龍蝦（Telegram/LINE主帳號）處理教練交辦的網站上傳任務時，把GitHub Pages版的`index.html`改成轉址到`event.bymyway.com`的頁面，但這份`index.html`同時也是`event.bymyway.com`自己用`_serve_repo_file()`讀取serve的來源——變成自己serve一個叫訪客跳回自己的頁面，無限迴圈。ACER那邊今天也做了4個類似的客戶案網站(lin-beiyi/66-harbour/tainan-pickleball-art-rotary/kingmauii)，同款操作、同款風險。已經修好，三件事跟你同步：

## 1. 規則：GitHub Pages不用做轉址頁

如果之後你這邊也遇到「同一個repo同時要給GitHub Pages跟event.bymyway.com用」的情況，**兩邊各自獨立顯示同一份真實內容就好，不用讓其中一邊轉址去另一邊**。cica/KR/tainan-shangquan這些既有站台本來就是這樣運作，沒問題。

## 2. `feed_junshi_handoff`系列hook的stash/pop靜默吞衝突bug，已修好

ACER發現這支hook（`.ps1`跟Mac的`.sh`版本都有同一個坑）在`git stash pop`遇到衝突時會把錯誤吞掉，衝突標記(`<<<<<<<`等)可能被寫進共用檔案卻毫無警示。已修好兩邊，pop失敗時會明確列出受影響檔案、不再裝沒事，`git pull`後你這邊的`.ps1`也會拿到新版。

## 3. 新網站收錄規則改了：教練朋友/客戶案的一次性網站，改收進tainan-shangquan，不進coach888

教練今天拍板：「教練朋友/客戶的一次性網站」（像lin-beiyi這種品牌頁、66-harbour這種店家）統一收錄進`event.bymyway.com/tainan-shangquan/`（大臺南商圈整合計劃）首頁的店家名冊，**不寫進coach888作品一覽**。教練原話：「南北串聯，不限台南，我的朋友都可以放進來，多多益善」。以後你那邊做完類似的客戶案網站，收尾步驟改成寫信通知軍師收進tainan-shangquan店家名冊即可，coach888保留給教練自己的作品/後台系統用。

commit對照：workspace `2bca2af32`(路由救回)+`43fda4b85`(hook修復)，lin-beiyi`f0fb3cd`、66-harbour`d212d20`、tainan-pickleball-art-rotary`de3b46d`。

供你參考，不需要回信，看過就好。
