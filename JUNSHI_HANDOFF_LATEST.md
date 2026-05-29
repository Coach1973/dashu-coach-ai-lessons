# 軍師交接紙條（最新）

> 給下一個軍師：開工先讀這張，就能無縫接上，不用教練重講。
> 本場時間：2026-05-30 凌晨（Haiku 終端機特助完成）
> 寫紙條的人：終端機特助（Claude Haiku 4.5）

---

## ✅ 本場完成任務：northern-tw.netlify.app 論壇網站大改版

| 任務 | 結果 |
|------|------|
| 圖片遺失修復（11 張從舊 deploy 救回） | ✅ |
| 場次切換列（4/11 + 6/26） | ✅ |
| 6/26 完整場次建置（7 位講師、議程、報名、贊助） | ✅ |
| 626 設為首頁，411 移至成長足跡 | ✅ |
| 成長足跡加入 1206 桃園場 + 411 高雄場兩筆記錄 | ✅ |
| 場次切換列移至頁面最底部 | ✅ |
| 回到頂部浮動按鈕（右下角 ▲） | ✅ |
| 快速跳轉列（報名/論壇主題/演講者/議程/相關單位/廠商贊助） | ✅ |
| 中正大學 Logo 上傳並套用 | ✅ |
| 正式版推送完成 | ✅ |

---

## 🌐 網站資訊

| 站台 | URL | Netlify Site ID |
|------|-----|----------------|
| 正式版 | https://northern-tw.netlify.app/ | f1f3ed15-79b6-4bed-b4d1-0199a185a181 |
| 測試版 | https://northern-tw-test.netlify.app/ | 56d3fa7e-41bd-40d9-8000-2e9b779b0461 |

Netlify Token：nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838（到期 2027/05/14）

---

## ⚠️ 本地工作目錄（重開機會消失！）

最新版所有檔案在：/tmp/northern_images/
下次開工若 /tmp/northern_images 不存在，需從 Netlify 舊 deploy 重新拉檔案。
拉法：用 API 找最新 deploy ID，再下載每個檔案。

---

## 🗓 6/26 場次關鍵資訊

- 時間：2026 年 6 月 26 日（五）09:30–17:00
- 地點：國立中正大學創新大樓（嘉義縣民雄鄉大學路一段168號）
- 指導：嘉義縣衛生局
- 主辦：國立中正大學中小企業育成中心、全球健康發展協會、紐約北方醫學中心
- 報名費：免費，席次 200 位
- 實體報名：https://forms.gle/Htk4YENdd5m9rmmG8
- 線上報名：https://forms.gle/PHQjjADVXTyVbXGc7
- 贊助廠商：NT$30,000
- 入會表單：https://forms.gle/NjhHmEwxCUrw8FBW8

講師：宋昇峯、林明傑、吳啟裕、張克咸、楊尚儒、陳佩君、藍士哲

---

## 📌 待辦（下一棒）

- 1206 桃園場補完善（教練會提供報導花絮，不急）
- 626 報名表連結確認（Google Forms 是否正確）
- 626 議程如有更新再調整

---

## 🔴 部署鐵律

Netlify 是手動上傳型，每次更新：
1. 修改 /tmp/northern_images/index.html
2. zip -r deploy.zip .
3. curl API 推送（絕對不用 git push）
