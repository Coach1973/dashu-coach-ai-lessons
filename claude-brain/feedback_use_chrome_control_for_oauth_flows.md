---
name: feedback-use-chrome-control-for-oauth-flows
description: 教練已授權操控其真實登入瀏覽器(claude-in-chrome)時，任何需要「點擊授權/選擇帳號」的OAuth式流程(含CLI工具的tunnel login)都要直接用claude-in-chrome完成，不要叫教練自己點
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a7a813d3-3d3a-47de-831f-20836ed149a6
  modified: 2026-08-03T17:47:36.924Z
---

教練已經明確授權操控他真實登入的Chrome瀏覽器（見 [[project_bni_connect_backend_access_verified_2026-07-31]]，當時是操作BNI Connect CMS後台），這個授權範圍不是只限於「查資料」，也涵蓋任何需要點擊網頁按鈕才能完成的動作——包括CLI工具的OAuth登入流程（例如`cloudflared tunnel login`跳出的Cloudflare「選擇網域＋Authorize」網頁）。

**Why:** 2026-08-03深夜設定`chapters.bymyway.com`（bni-chapters系統對外開通）時，`cloudflared tunnel login`因為cert.pem過期需要重新走網頁授權。一開始請教練自己去瀏覽器點選網域+按Authorize，教練當場糾正兩點：①之前同類型網址（mentor100/namecard等）從沒這麼麻煩過（其實是憑證剛好在這次任務前過期，不是這次任務特別難，這點我backwards解釋清楚了）②「我本來就有授權你操控我的網頁，為什麼要我來做？」——這是更關鍵的糾正：忘記把既有授權類推到新的使用情境。改用`claude-in-chrome`工具（`tabs_context_mcp`→`navigate`到授權網址→`find`+`computer left_click`點選bymyway.com網域→點Authorize按鈕）後，30秒內完成，cert.pem正確寫入，完全不需要教練動手。

**How to apply:** 只要教練說過一次「你可以操控我的瀏覽器」，之後任何需要在網頁上點擊才能完成的動作——不限於原本授權的那個網站——都應該優先評估「這是不是能用claude-in-chrome自己點完」，而不是預設回去請教練點。CLI工具跳出的OAuth網頁（Google/GitHub/Cloudflare等任何服務的登入授權頁）都適用同一邏輯，因為那本質上也是「操控瀏覽器完成一個網頁動作」，跟操作BNI Connect後台沒有本質差異。

Related: [[project_bni_connect_backend_access_verified_2026-07-31]]、[[project_bni_chapters_public_launch_2026-08-03]]
