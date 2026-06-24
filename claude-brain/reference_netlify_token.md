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

用法：
```
curl -H "Authorization: Bearer nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838" https://api.netlify.com/api/v1/sites
```

⚠️ 注意：之前記憶檔存的 token 少了中間幾個字元（`...y6sE7yXnxHbmjJLgBMNxp...` → 正確是 `...EGqxokQ2WU9CERSRwLp4yVap...`），以路徑大全為準。

**共 23 個網站，22 個手動上傳（可透過此 token 直接 API 部署），1 個已連 GitHub（health-news-tw）。**

相關資訊見 [[reference_netlify_sites]]
