---
name: reference-netlify-token
description: 教練的 Netlify Personal Access Token，用於直接透過 API 更新所有 23 個 Netlify 網站，無需進後台
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2f6f31b2-9bc3-46fe-87f5-7f2b1bf9752f
---

Netlify Personal Access Token（Coach1973 帳號）：
`nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838`

到期日：2027/05/14

**🔴 每月積分週期：每月 25 日重置 1000 積分（教練 2026-06-18 親口告知）**
- 6/25 04:00 PT = 6/25 20:00 GMT+8 重置
- 下次重置：2026-06-25
- 提醒設定：每月 24 日早上主動提醒教練「明天 Netlify 積分重置，可重啟大量部署」

用法：
```
curl -H "Authorization: Bearer nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838" https://api.netlify.com/api/v1/sites
```

**共 23 個網站，22 個手動上傳（可透過此 token 直接 API 部署），1 個已連 GitHub（health-news-tw）。**

相關資訊見 [[reference_netlify_sites]]
