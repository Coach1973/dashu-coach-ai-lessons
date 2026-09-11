---
name: reference-fb-app-icon-transparency-and-upload-limitation
description: FB App Review圖示要求透明背景時JPG格式先天不支援+Meta新式上傳元件用File System Access API無法被claude-in-chrome自動化
metadata:
  node_type: memory
  type: reference
  originSessionId: 8dd30024-1d05-49d9-b13b-7269a5ebea06
  modified: 2026-09-11T15:52:00.000Z
---

**問題一：Meta App Review上傳App圖示回報「偵測到白色背景，請用透明背景」**，即使圖案本身乾淨無雜色。根因：**上傳的檔案是JPG格式，JPG格式規格上本身就不支援透明度（alpha channel）**，不管設計得多乾淨都一定被判定成實心白底。看到這類錯誤先檢查副檔名，不用懷疑圖片設計本身。

**修法**：用PIL對圖片做flood-fill去背（從四個角落開始，只清除「連通」到邊界的近白色像素，避免誤傷logo內部本來就存在的白色區域），輸出PNG格式，用不同顏色背景合成後檢視確認無白邊/鋸齒殘留再上傳。

**問題二：Meta新版介面（App圖示上傳等）改用瀏覽器的File System Access API（`window.showOpenFilePicker()`），DOM裡完全沒有傳統`<input type=file>`元素**——`querySelectorAll('input[type="file"]')`回傳空陣列，claude-in-chrome的`file_upload`工具（依賴找到真正的`<input type=file>`元素）完全無法使用，這跟Meta Business Suite貼文編輯器的圖片上傳按鈕是同一個模式（[[feedback_claude_in_chrome_wrong_device]]記錄過的contentEditable打字不穩定是另一個獨立問題）。

**嘗試過但失敗的自動化路徑**：
1. `file_upload`直接指向按鈕/label元素——一律回報「找到的是div/label，不是file input」
2. 覆寫`window.showOpenFilePicker`回傳自建的FileSystemFileHandle，讓網頁誤以為使用者選了檔案——概念可行，但需要先讓瀏覽器JS拿到檔案的Blob。用`fetch(外部網址)`抓自己代管的檔案，被該頁面的CSP（Content-Security-Policy）擋掉跨網域請求（`TypeError: Failed to fetch`，非CORS header問題，是CSP connect-src層級直接擋）。改用base64 data URI（不經過網路請求，理論上能繞過connect-src限制）——技術上可行，但受限於單次工具呼叫的payload大小，即使把圖片縮到512×512(~155KB→206KB base64)仍然过大，不值得再嘗試更暴力的分段注入。

**結論**：這類「新式上傳元件+嚴格CSP」的網站，目前沒有找到可靠的全自動化路徑，最快的解法是誠實跟教練說明技術限制，把處理好的檔案放在容易找到的位置（如桌面，取一個好認的檔名），請教練自己點2下上傳，不用死磕自動化。

相關：[[feedback_claude_in_chrome_wrong_device]]（同一類「網站上傳元件無法被工具直接操作」問題的相鄰案例）
