---
name: project-unrestricted-war-website
description: 《超限戰》電影網站的 GitHub repo、Netlify 站台資訊與工作流程（含 2026-05-29 雙副本陷阱警告）
metadata: 
  node_type: memory
  type: project
  originSessionId: 74751326-4082-44ca-8fa5-4a18e20c30a3
---

《超限戰》電影網站，2026-05-27 建立並上線。

**How to apply:** 下次要繼續更新這個網站時，**先讀「雙副本陷阱」警告**，再按部署流程動手。

---

## 🔴🔴🔴 雙副本陷阱（2026-05-29 軍師血淚教訓）

**本機有兩個 clone**：
- `/tmp/theunrestrictedwar`（軍師慣用，重啟可能消失）
- `~/github_repos/theunrestrictedwar`（永久副本，別的 AI 慣用）

**死循環病灶**：
1. AI 改 `~/github_repos/` 的版本→git push→以為部署了
2. 但 Netlify **不會自動部署**（見下方）
3. 教練看網站沒改→再叫 AI 改→AI 又改 `~/github_repos/`→死循環

**鐵律**：
- 動手前 **兩個副本都 git pull 同步**到 origin/main 最新
- 改完任一副本後，另一副本也要 pull 同步
- 寧可選一個 working dir 用，不要兩邊改

---

## 🔴 部署流程鐵律：Netlify 不靠 GitHub 自動部署

theunrestrictedwar 是 **手動上傳型** Netlify 站（22/23 個教練站都是這種）：

**錯誤流程（小龍蝦/MiniMax 反覆中招）：**
- ❌ 只做 git add + commit + push → 以為上線了

**正確流程（每次更新）：**
1. 修改 index.html（**先 pull 同步雙副本**）
2. `zip -r /tmp/deploy.zip index.html 1779859916089.jpg`
3. `curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/zip" --data-binary "@/tmp/deploy.zip" "https://api.netlify.com/api/v1/sites/<site_id>/deploys"`
4. 等 30-90 秒，curl 線上 HTML 驗證
5. git add + commit + push 到 GitHub（保存歷史，不影響部署）
6. 兩個本機副本互相同步（git pull）

---

## GitHub Repo

- 網址：https://github.com/Coach1973/theunrestrictedwar
- 本機路徑 1：`/tmp/theunrestrictedwar`
- 本機路徑 2：`~/github_repos/theunrestrictedwar`（永久副本）
- 主要檔案：index.html、1779859916089.jpg（電影海報）

## Netlify 站台

- 正式版 Site ID：`86406013-6cdf-4bec-90e3-cdc9655bf124`
- 正式版網址：https://theunrestrictedwar.netlify.app
- 測試版 Site ID：`52d137b0-4bc7-4876-b9fa-3c11c35f272a`
- 測試版網址：https://theunrestrictedwar-test.netlify.app
- Netlify Token：見 [[reference-netlify-token]]

**Why:** 教練說要改什麼就改什麼，不需要教練動手，全程由軍師執行。但前提是**走對流程**，否則永遠改不上線。

相關記憶：[[feedback-netlify-deploy-zip-api]]、[[feedback-ai-image-compare-table]]
