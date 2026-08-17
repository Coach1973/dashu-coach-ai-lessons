---
name: feedback-two-machines-same-chrome-extension-conflict
description: Mac跟聯想同時開Claude瀏覽器擴充功能且同時執行任務時，自動化連線會搶到對方機器，教練親自抓出根因(2026-08-17)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ed21277a-b31b-465c-951d-965316ab4b7f
  modified: 2026-08-17T11:08:00.000Z
---

Mac跟聯想電腦如果**同時**登入Claude瀏覽器擴充功能、又**同時**都在執行browser automation任務，兩邊的連線會串在一起——Mac這邊呼叫瀏覽器工具，實際連到的可能是聯想電腦那台的Chrome分頁(反之亦然)，因為兩邊資料是連通的。

**Why：** 2026-08-17真實踩到：Mac這場對話操作ezPay，讀到的帳號(bymyway/大樹教育)跟教練在Mac螢幕上實際看到的(gtbctainan/BNI)對不上，一度懷疑是分頁混淆或截圖錯誤，來回排查十幾輪(截圖比對兩個螢幕、確認tab group隔離機制)都解釋不通，最後教練自己想通：**根因是聯想電腦當時也同時在用同一組帳號的擴充功能執行任務，兩邊搶線**。這不是「哪個分頁」的問題，是「哪台機器」的問題，用截圖/tab id比對永遠查不出來，只能從「當下是不是兩台機器同時在用擴充功能」這個角度切入才對。

**How to apply：** 遇到瀏覽器自動化讀到的帳號/資料跟教練親眼看到的對不上時，**第一個該問的問題是「現在是不是有另一台機器也同時在跑瀏覽器自動化/開著同一組擴充功能」**，不要先鑽進「是不是分頁搞混了」這種同機器內的解釋——那條路排查半天都是死巷。確認方法：請教練檢查另一台機器當下有沒有也在執行類似任務，或乾脆請對方先登出擴充功能再重試。

**🔴 2026-08-17教練裁示的永久解法**：兩台機器改用不同瀏覽器裝Claude擴充功能，從根本避免搶線，不用每次臨場判斷。
- **Mac**：維持用Chrome
- **聯想（Windows）**：改用**Microsoft Edge**，教練已在聯想那台裝好官方Claude擴充功能（來源必須是`https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn`這個Anthropic官方認證版本，Edge市集裡另外那些「Claude Helper」「Claude Studio」都是第三方仿冒品，不能裝）
- **給聯想那邊軍師的提醒**：以後任何開網頁操作（claude-in-chrome MCP工具）一律確認是在Edge裡執行，不要用Chrome，這樣就不會再跟Mac這邊的Chrome擴充功能搶線串連

**✅ 2026-08-17 21:23教練口頭確認：聯想已切換Edge完成**——教練當面確認聯想那台機器的browser automation已改用Edge，Chrome版搶線問題視為結案，往後兩機物理隔離常態化，不用再追蹤。
