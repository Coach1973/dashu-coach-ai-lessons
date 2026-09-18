---
name: reference-sendbeacon-cors-credentials-gotcha-2026-09-18
description: "navigator.sendBeacon跨網域請求會帶credentials:'include'，伺服器CORS設Access-Control-Allow-Origin萬用字元或漏Allow-Credentials都會被瀏覽器整個擋下，且beacon本身不回報失敗"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 03318971-0b8e-4d14-a5f7-ece34565e951
  modified: 2026-09-18T14:51:42.815Z
---

幫 coach888（GitHub Pages `coach1973.github.io/coach888/`）加「依點擊次數即時排名」功能時，前端用 `navigator.sendBeacon` 打 `event.bymyway.com` 的新端點記錄點擊，第一版伺服器端 CORS header 沿用既有 `/api/coach888/state` 端點的寫法（`Access-Control-Allow-Origin: "*"`），結果本機用真實 Chrome 點擊測試，production API 完全沒收到任何資料——`fetch` 呼叫不到，`sendBeacon` 本身也不會拋出任何 JS 例外或 Promise rejection（它是 fire-and-forget 設計），唯一線索是瀏覽器 console 裡的 CORS 錯誤訊息。

**Why：** `navigator.sendBeacon()` 送出的跨網域請求，瀏覽器會自動帶 `credentials: 'include'`（不像一般 `fetch()` 預設是 `same-origin`，不會夾帶 cookie）。CORS 規範明確禁止 credentialed 請求搭配萬用字元 `Access-Control-Allow-Origin: *`——伺服器必須回傳發送請求的實際 Origin，而且還要**額外明確加上** `Access-Control-Allow-Credentials: true`，兩個條件缺一個，瀏覽器都會整個擋下請求。這台專案裡其他用 `fetch()` 呼叫且沒設 `credentials` 選項的既有端點（如 `coach888_state` 的 sync）不會踩到這個坑，因為預設 `credentials:'same-origin'` 不會觸發這條規則——這正是為什麼舊寫法在別處用得好好的，換到 sendBeacon 就整個失效。

**How to apply：** 任何要用 `navigator.sendBeacon` 打跨網域 API 的功能，伺服器端 CORS header 必須同時滿足兩點：①`Access-Control-Allow-Origin` 回傳 `request.headers.get("Origin")`（不能用 `*`）②明確加上 `Access-Control-Allow-Credentials: "true"`。除錯時光看「API 有沒有回應」不夠，因為 beacon 從來就不會告訴你它失敗了——必須直接查瀏覽器 console 的 CORS 錯誤訊息，或直接查伺服器端資料有沒有真的寫入來驗證。
