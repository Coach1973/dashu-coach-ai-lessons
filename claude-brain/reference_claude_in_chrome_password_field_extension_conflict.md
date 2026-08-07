---
name: reference-claude-in-chrome-password-field-extension-conflict
description: claude-in-chrome自動化操作密碼欄位時可能被其他瀏覽器擴充功能(疑似密碼管理器)的浮層卡死，此時改用Flask test_client等效驗證+誠實告知教練視覺驗證缺口
metadata: 
  node_type: memory
  type: reference
  originSessionId: fc75ce1b-c241-4d2d-ac45-f4b2e9391167
  modified: 2026-08-07T18:59:42.068Z
---

2026-08-08，mentor100後台審核流程開發驗證時，用`claude-in-chrome`的`form_input`/`computer`工具嘗試登入`/admin/login`（帳號密碼輸入），無論是`form_input`直接填值、或用`computer`點座標+`type`打字，只要碰到密碼欄位（填值或按Enter送出）就開始出現`Error clicking: Cannot access a chrome-extension:// URL of different extension`，後續同一個分頁的所有操作（點擊、截圖、按鍵）全部連帶失敗，換全新分頁、換全新tab group都一樣，只有全新分頁在「還沒碰過密碼欄位」之前的操作是正常的。

**Why:** 這個錯誤訊息的意思是「有另一個瀏覽器擴充功能的畫面（chrome-extension://開頭的網址）擋在最上層，claude-in-chrome自己的自動化擴充功能沒有權限穿透去點擊」——典型情境是密碼管理器擴充功能（1Password/Bitwarden/Chrome內建密碼建議等）在密碼欄位被聚焦或送出時彈出自動填寫/儲存密碼的建議浮層，這個浮層屬於「別的擴充功能」，瀏覽器的安全機制本來就不允許擴充功能之間互相操控對方的UI，所以claude-in-chrome的點擊/截圖全部被擋下來，是環境限制不是程式bug，重試同一個分頁也沒用。

**How to apply:** 遇到這個錯誤時，不要在同一個卡死的分頁裡一直重試（觀察到會持續卡死，包括截圖都會失敗）。優先順序：① 換全新分頁、且該次測試流程刻意避開觸碰密碼欄位（例如用已登入狀態的頁面做視覺確認，不要每次都重新登入）② 若功能邏輯正確性是重點而非畫面像素級外觀，改用Flask `app.test_client()` + `session_transaction()`手動注入`sess['logged_in']=True`繞過登入，對照斷言(assert)每個步驟的資料庫狀態/HTML內容，這個方法比視覺截圖更精確也更快 ③ 誠實告知教練「這次視覺確認卡在瀏覽器擴充功能衝突，功能邏輯已用自動化測試驗證過，畫面麻煩您自己看一眼」，不要用「已經截圖確認過」這種話蒙混過去（守則#15），也不要為了硬要截圖成功而反覆重試浪費時間。這不是`feedback_html_preview_chrome_only.md`那條鐵律的例外——真正需要教練親眼確認的頁面（尤其是新版型/新樣式）還是要想辦法用Chrome開給教練看，只是「登入後台」這一步如果自動化卡死，功能驗證可以先用test_client頂上。
