---
name: feedback-web-push-sop
description: 教練說「網頁推」時立刻調出的網頁部署 SOP——分兩類站台，流程不同但都要教練親口確認
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f59cc3d7-fb05-4bbb-8883-6ecb67081576
---

教練說「網頁推」= 啟動網頁部署流程。

**Why:** 2026-06-09 案例 24 血淚——未經確認就推，Netlify 扣點 + 首頁被覆蓋。教練親定此 SOP，所有 AI 助教強制遵守。

**How to apply:** 聽到「網頁推」，立刻走以下流程：

---

## 網頁推 SOP

### 第一步：確認站台類型

問教練「推哪一個站？」，然後查 Netlify API 確認部署模式：

| 類型 | 判斷方式 | 代表站台 |
|------|----------|----------|
| **GitHub 自動部署型** | 有 `build_settings.repo_url` | jiesheng-leadership |
| **手動上傳型** | 無 repo_url | 其餘 22 個 Netlify 站 |
| **GitHub Pages** | 不在 Netlify 上 | cool-case |

### 第二步：本機預覽讓教練看

1. 在本機跑 `python3 -m http.server <port>` 或用已開的預覽伺服器
2. `open http://localhost:<port>/` 開瀏覽器
3. **等教練親口說「推」或「沒問題」**

### 第三步：依站台類型推送

**GitHub 自動部署型（git push = Netlify 部署 = 扣點）：**
```bash
cd <本機 repo 路徑>
git add <改動的檔案>
git commit -m "說明"
git push origin main
```

**手動上傳型（zip + API）：**
```bash
cd <檔案目錄>
zip -r /tmp/deploy.zip .
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/zip" \
  --data-binary "@/tmp/deploy.zip" \
  "https://api.netlify.com/api/v1/sites/<site_id>/deploys"
```

**GitHub Pages（免費，不扣點）：**
```bash
cd <本機 repo 路徑>
git add <改動的檔案>
git commit -m "說明"
git push origin gh-pages
```

### 第四步：線上驗證

推完後 `curl` 線上版，grep 關鍵字確認新內容已上線。

---

**鐵律：第二步的「教練說推」不可跳過。AI 自己看了覺得沒問題 ≠ 教練確認。**

相關記憶：[[feedback-netlify-deploy-zip-api]]、[[reference-netlify-token]]
