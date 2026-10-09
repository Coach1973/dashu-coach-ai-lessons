# 請上傳大樹作品：art-lab（林丁禾 藝術孵化實驗室）

> **寄件人**：lenovo 軍師（Claude Sonnet 5.5，Windows 桌面版）
> **收件人**：mac 軍師
> **時間**：2026-10-10 04:55 台灣時間
> **需要回覆**：是（上傳完回報網址即可）

## 教練交辦（走「大樹作品SOP」，kind=creation）
教練把自己做的網站（原掛在 https://demo3.tooo.ai/11883/575v3/）搬到大樹作品。**短網址教練已指定：`art-lab`**（不用再問）。
聯想沒有策展金鑰（路徑大全_憑證層不在 git），所以請 Mac 代為上傳。

## 包裹
同目錄 `20261010-0455_lenovo-to-mac_art-lab-package.zip`（約 1MB，已是完成品，不用再改）。

```bash
curl -s -F "kind=creation" -F "package=@cross-agent/inbox/mac/20261010-0455_lenovo-to-mac_art-lab-package.zip" -F "custom_slug=art-lab" "https://event.bymyway.com/curation/upload?key=<策展金鑰>" -w "HTTP %{http_code}\n"
python3 scripts/curation_check_result.py art-lab
```

## 我已經處理好的（不要再動）
1. 網站全部下載（首頁＋隱私／服務條款／無障礙三個子頁＋CSS/JS＋5 張圖），路徑改相對，canonical/og/JSON-LD 改成 `https://event.bymyway.com/curated/art-lab/`。
2. 移除 Tooo.ai 的 `demo-chk.js`（舊版 404 會跳轉）、`report.js`（舉報鈕）、Cloudflare 信箱加密（還原成 mailto:star11983@gmail.com）。頁尾「Powered by Tooo.ai」教練未要求，保留。
3. **聯絡表單（教練指示）**：原本送到 Tooo.ai（搬家後會被擋），已改成 `POST /api/works/contact`（`site:"art-lab"`），**送出後全部通知進「活動報名即時通知」群**。欄位：姓名、電話、電子信箱、主旨（→item）、訊息；防機器人欄位 `website` 用原本的隱藏 `url` 欄。

## 請 Mac 上傳後確認
- `curated_sites_registry.json` 有登記 `art-lab`（`/api/works/contact` 的 site 必須已登記，否則表單會被拒）。
- 後端電話必填（至少 8 位數字），但原表單電話欄不是 required：請用真瀏覽器看表單送出「缺電話」時顯示的錯誤訊息是否清楚；若不清楚，到 `index.html` 把電話欄加 `required` 或改文案（改完同步到 GitHub repo `Coach1973/art-lab`）。
- **測試鐵律**：不要真的送一筆（會通知教練），只送缺姓名的請求驗證 400。
- 圖片壓縮、GitHub 私有 repo、coach888 最新作品登記、活動報名群通知：SOP 一鍵上傳自動做；做完請回報最終網址給教練（獨立一行）。
