---
name: feedback-never-expose-local-preview-to-coach
description: coach888互動式編輯頁面被本機測試預覽誤導，教練在暫存檔上改了一大堆東西全部沒同步到正式站，白忙一場
metadata:
  type: feedback
  originSessionId: e04e921e-76e5-4743-82a4-59fbb8062c1d
  modified: 2026-09-04T11:07:06.328Z
---

驗證修復時用 `python3 -m http.server` 開本機預覽（或 `file://` 開本機檔案）＋Browser pane 操作，是 AI 自己驗證用的暫存環境。但 Browser pane 是這個 App 裡教練也看得到、點得到的共用面板——教練回報「我剛才在你跳出來的本機頁面下改了一大堆東西，功能雖然正常，但我改的其實是暫存檔，根本沒有同步到雲端正式網址上，等於白忙一場」，而且明講「我已經好幾次做白工了」，不是第一次發生。

**Why:** coach888 這類頁面本身就是「教練可以直接互動編輯」的工具（新增分類/拖拉排序/改標題），跟一般唯讀展示頁不同——教練看到 Browser pane 開著一個看起來一模一樣的頁面，會很自然地直接上手改，沒有線索能分辨這是本機暫存測試版還是正式站。本機測試環境（`http.server`／`file://`）在對話結束或下次開機就會消失，教練的操作全部打水漂。

**How to apply:**
1. 驗證完成後，**絕對不要**把本機測試分頁留在 Browser pane 裡不清——收工前用 `tabs_close` 全部關掉，讓 pane 回到乾淨狀態（`tabs_context` 查有沒有殘留 `file://` 或 `127.0.0.1` 分頁）。
2. 修復完成、要教練驗收時，**只給正式網址**（`event.bymyway.com/...`、`coach1973.github.io/...` 等），不要讓 Browser pane 停留在本機測試分頁上。
3. 如果對話中有給教練連結，一律附註這是正式站；如果需要教練親自測試某個互動功能，明確用文字提醒「這是正式網址，改的東西會真的存起來」。
4. 涉及像 coach888 這種「教練會直接互動編輯內容」的頁面時，本機驗證的優先順序更要提高警覺——這類頁面被誤用的代價（教練白費心力操作）比純展示頁（教練頂多看錯畫面）高很多。

Related: [[feedback_screenshot_rules_consolidated]]（同樣是「AI 驗證用的暫存資訊不該讓教練誤以為是正式產出」這條精神的延伸）
