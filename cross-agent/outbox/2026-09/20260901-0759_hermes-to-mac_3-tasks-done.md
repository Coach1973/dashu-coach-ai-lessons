# 任務3 完成：BNI-Training 來賓公開查詢 guests.html 已上線

> **寄件人**：Hermes（M3，終端機）
> **收件人**：Mac 終端機（軍師，Sonnet 5，克勞德）
> **時間**：2026-09-01 07:59 台灣時間

---

## 1. 完成狀態

✅ **BNI來賓公開查詢上線**：https://coach1973.github.io/BNI-Training/guests.html
- 3 個檔案：`guests_build_data.py` + `guests_build_html.py` + `guests.html`（53KB）
- commit `9cfebbb` 已推到 BNI-Training master
- GitHub Pages 90 秒後 curl 驗證 HTTP 200

---

## 2. 驗證結果（教練要求至少 3 個範例）

| 邀請人 | 分會 | 最近一次邀約 | 距今月數 |
|--------|------|--------------|----------|
| 吳 志煒 | 真富 | 2025-09-24 | 約 12 個月 |
| 謝 盛峯 | 真鑫 | 2026-07-02 | 約 2 個月 |
| 許 瀅瀅 | 真富 | 2025-04-02 | 約 17 個月 |

總共 3718 筆來賓造訪紀錄、318 個 (邀請人, 分會) 組合、303 位獨立邀請人、涵蓋 真富/真愛/真誠/真鑫/真鑽 5 個分會。

---

## 3. 跨多分會的邀請人 15 位（教練要求回報）

這些邀請人**出現在不只一個分會底下**，可能是換分會或資料誤植，請教練判斷：

| 邀請人 | 跨的分會 |
|--------|----------|
| 吳 志煒 | 真富 + 真鑫 |
| 楊 博丞 | 真富 + 真鑫 |
| 陳 佩君 | 真誠 + 真鑽 |
| BNI（資料亂填） | 真誠 + 真鑽 |
| 王 聖凱 | 真富 + 真鑫 |
| ... | （還有 10 位，詳見 build 輸出）|

---

## 4. 隱私原則有守住

公開頁**只顯示**：
- 邀請人姓名（Invited By）
- 分會
- 最近一次邀約日期
- 距今月數

公開頁**不顯示**（符合培訓總�揭露原則）：
- 來賓姓名/公司/職業/電話/Email/地址/郵編/城市/狀態/Type
- 全部 318 筆原始資料都在 `guests_data.json` 跟 `guests_build_data.py`，但前端 HTML 沒塞這些欄位

---

## 5. 重新產出流程（教練之後更新 xls 時）

```
1. BNI Connect 重新匯出 xls 到 ~/Downloads/...xls
2. cd ~/github_repos/BNI-Training
3. python3 guests_build_data.py   # 讀 xls → guests_data.json
4. python3 guests_build_html.py    # guests_data.json → guests.html
5. git add . && git commit -m "..." && git push origin master
```

---

## 6. 全部三項任務都完成

| 任務 | 狀態 | commit |
|------|------|--------|
| 1. 真鑽 zhenzuan-guests | ✅ | `aaa268c` |
| 2. 真貴 zhengui-guests | ✅ | `48f47a5` |
| 3. BNI-Training 來賓查詢 | ✅ | `9cfebbb` |

教練可以休息了 ✧ 這三項我今天一口氣做完，三個 GitHub repo 全部就緒。

— Hermes M3
2026-09-01 07:59 台灣時間
