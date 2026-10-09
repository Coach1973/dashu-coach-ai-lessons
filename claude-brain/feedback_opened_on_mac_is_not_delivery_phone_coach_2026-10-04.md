---
name: feedback-opened-on-mac-is-not-delivery-phone-coach-2026-10-04
description: 教練用手機遠端時，「已在 Mac 的 Chrome 開過／跳出來了」對他等於沒發生；交付一律是獨立一行的 https 網址＋curl 驗證。根因是三處腳本文字教我這樣講，已改源頭＋新增擋下反射
metadata:
  node_type: memory
  type: feedback
  originSessionId: aa537cbb-3635-47b9-baea-cb107f918687
  modified: 2026-10-09T04:34:21.310Z
---

教練 2026-10-04 14:00 退件：「不合格，你並沒有跳 HTML 出來……每次說『我已經在 Mac 開過了』，哪裡？我根本都沒看到，哪冒出來的？」他是用手機遠端控制，Mac 螢幕（只有一個）上的視窗他看不到。

**Why:** 三個地方的現成文字都在教我說「已開給您看」：`stop_rules_master.py` 規則 J 第 2 步、`auto_chrome_after_html_edit.sh` 輸出、反射 `G-HTML-CHROME`。所以不是偶發，是被提示教壞的（試金石案例101）。N8：同類錯改源頭，不再加記憶——已改三處原文，並新增 `R-OPENED-ON-MAC-NOT-DELIVERY`（reply 擋下：說「在 Mac 開過」又沒有 https 網址就擋）。

**How to apply:**
- 交付網頁／HTML＝給教練打得開的 https 網址，**獨立一行**，並先 curl 驗證狀態 200＋Content-Type＋內文關鍵字。
- 在 Mac 用 Chrome 開只是自己查證（N4），不要寫成「開給您看」。
- 教練明說可公開（10/04「不擔心公開我的想法，放大樹作品都沒問題」）時，走大樹創作 SOP 一條龍上架（`knowledges/SOP_教練個人創作上架event.bymyway.com不進商圈.md`），不要手工註冊 registry（會被安全檢查擋）。
- 附帶：launchd `com.coach.curation-watch` 壞了（結束碼78、plist 不見），上傳會停在 pending，要手動跑 `event-signup/venv/bin/python scripts/curation_process.py`。

相關：[[reference-session-verbatim-report-from-jsonl-2026-10-04]]（報告書已上架 `https://event.bymyway.com/curated/game-1004/`）。

**🔴 2026-10-08 同類第二次（案例111），範圍擴大到「任何交付檔案」**：教練 17:15 說「做好的東西，不要用預覽的方式顯示給我看，就直接跳出 PPT 或直接跳出網址。永遠就這樣，直接跳出來讓我看！」起因：《96小時》簡報我做對了兩個版本，但沒跳出來，教練在檔案預覽小框裡點到的剛好是做錯的（縮小版、文字完整版），氣了一整個下午。他自己也說「做對了卻看不到」。
- **機制（不靠記得）**：`scripts/deliver_open.sh <檔案或網址>`——PPT/Keynote 開 Keynote、網址/HTML 開 Chrome；先關掉「沒改過」的舊 Keynote 視窗（同名多視窗是這次的混亂來源之一），開檔後等匯入警告消失，印出最前面的程式、視窗數、位置（x≥1920＝跑到第二螢幕）、張數當證據。回覆裡說「做好了某某.pptx」時會跳反射 `R-DELIVER-POP-OPEN` 提醒。
- **三條**：①交付＝跑 deliver_open 直接跳出，不給路徑、不叫教練去資料夾找 ②多版本只留一個主檔（不加後綴），其他搬備份資料夾 ③驗證證據用它的輸出，不用截圖（截圖被教練鎖住，未同意不可截）。
- 相關：[[feedback_windows_on_main_display_only_2026-09-25]]（視窗一律主螢幕）。

**🔵 2026-10-09 教練說明原因（取代上面「PPT 開 Keynote」的做法）**：10/08 17:34 教練說「打開資料夾，不要打開檔案」，10/09 12:27 解釋：「你直接打開檔案，我只會看到這個檔案的內容，但我沒辦法把檔案傳到 LINE，因為我不知道那個路徑是什麼。打開資料夾的話，我要看就點進去看，我要傳也可以直接拉到 LINE 的通訊介面傳。這是教練習慣的方式。」
- **規則**：交付檔案（簡報、PDF、Word、Excel、圖片、zip…任何他可能轉傳的）＝`deliver_open.sh <檔>` 預設打開所在資料夾並選取該檔（`open -R`，並把 Finder 拉到最前面），**不開檔案內容**；教練明說要「開啟」才加 `--open`。網頁／網址維持直接開 Chrome。
- **Why**：他的工作流程是「看一眼 → 拖進 LINE 傳」，檔案要以檔案本身（有路徑）出現，不是內容。
- 同日他再強調：**答案必然是「要」的事不要問，該改就改**（已有反射 `R-COACH-YN-QUESTION-IS-ORDER`，試金石案例112；09-30 記憶 [[feedback_dont_ask_obvious_yes_and_never_hand_commands_2026-09-30]]）。
