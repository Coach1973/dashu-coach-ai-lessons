# 報名通知管線：sme-register-fn（教練 2026-08-05 親口交代，不要再查）

## 一句話
活動網站的「報名」按鈕，送出後會打 `https://sme-register-fn.netlify.app/.netlify/functions/register`，
教練的 LINE 就會收到通知。**這套是 Claude 做的系統，透過 bymyway.com 完成，能用就好。**

## 教練原話（2026-08-05 上午 11:40）
> 「這個我來告訴你，是透過 bymyway.com 完成的」
> 「你可以不用查，總之那個是 Claude 做的系統，反正它可以用就行了」

## 🔴 給未來的自己（三機通用）
**不要再花時間去挖 `sme-register-fn` 的原始碼在哪。** 教練已經明確表示不需要。
本場（2026-08-05）我一路查到 Netlify 站台（account `bymyway7`、無 GitHub repo 連結、
手動部署）、再查到 bymyway.com 的 WordPress REST 有 `code-snippets/v1` 外掛，
正要往下挖時被教練喊停——**這就是守則 #16「複雜的解法不一定是正確的解法」的現場**。
教練要的是「報名通知會進來」，不是「軍師搞懂整條架構」。

## 實務上只要記住這三件事
1. **端點**：`POST https://sme-register-fn.netlify.app/.netlify/functions/register`
2. **參數**：`{session, name, company, phone, email}`（`session` 會原樣出現在通知裡）
3. **慣例**：`session` 前面加活動前綴，教練一眼分得出來源
   - `【大樹小講】8/26（三） 午場 14:00–17:00`
   - `【個人報名通知】AI微論壇－嘉義場`

## 已接上這條線的站台
| 站台 | 檔案 | 狀態 |
|---|---|---|
| ai-talk-tw.netlify.app（AI微論壇） | `github_repos/ai-talk/index.html` | ✅ 原本就有 |
| bigtree-tw.netlify.app（大樹小講） | `github_repos/bigtree/index.html` | ✅ 2026-08-05 補上（commit `4b5b04a`） |
| bigtree/old、biz-gym、consultant 等 | 各自 index.html | ✅ 舊版本來就有 |

⚠️ 大樹小講改版成「大樹小講．無話不談」時**弄丟過這段通知**，變成純前端複製+開LINE，
教練完全收不到報名。改版既有頁面時，記得檢查 `submitRegistration()` 有沒有保留 `fetch`。

## 驗證方法（不用問教練也能自己測）
```bash
curl -s -X POST 'https://sme-register-fn.netlify.app/.netlify/functions/register' \
  -H 'Content-Type: application/json' \
  -d '{"session":"【系統測試·請忽略】","name":"測試","phone":"0000","company":"","email":""}'
# 回 {"ok":true} = 端點活著；但「教練真的收到」只有教練親眼確認才算數（守則 #15）
```
