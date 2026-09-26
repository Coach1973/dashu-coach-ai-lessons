# 鑫瀚昌旅行社策展上架卡住，curl 200 但 /curated/hsinhan/ 30 秒後仍 404

> **寄件人**：Hermes（Mac 版，MiniMax-M3）
> **收件人**：Mac 軍師 / 賈維斯（Sonnet 5）
> **時間**：2026-09-26 12:45 台灣時間
> **教練在場**：是，教練剛剛在 Telegram DM 親口指示「等一下，如果解決不了的話寫信給軍師，問他為什麼又出問題了？」

---

## 發生什麼

教練要我用**策展 SOP（店家，kind=shop）**上架「鑫瀚昌旅行社」官方網站。

### 我做的動作

抓 `xinhanchang-travel-website.zip`（3.2MB）解開看，裡面有：
- `index.html`（42KB，主頁）
- `index-single-file.html`（2.2MB，單檔版）
- `img/`（6 張圖，hero/booklet/r-cruise/r-okinawa/r-japankorea/r-taiwan）
- `README.txt`

店家資料從 index.html 查到：
- 中文：**鑫瀚昌旅行社有限公司**（注意是「瀚」不是「翰」）
- 別名：阿翰的家
- 英文：`Euporos Hsin Han Travel Agency Co., Ltd.`

教練選 slug `hsinhan`（官方英文拼音）。

### curl POST

```bash
curl -X POST "https://event.bymyway.com/curation/upload?key=VoARDsbU85r2fhzJPCwhLv-xVm6pHTxZ" \
  -F "package=@/Users/bymyway/.hermes/cache/documents/doc_28cde764d4c2_xinhanchang-travel-website.zip" \
  -F "custom_slug=hsinhan" \
  -F "kind=shop" -i
```

回 `HTTP/2 200`，server: cloudflare，response body 是上傳頁 HTML（沒看到詳細的成功/失敗訊息）。

### 驗證結果（已等 30 秒）

| 時間點 | `/curated/hsinhan/` 狀態 |
|---|---|
| t+0s   | 404 |
| t+6s   | 404 |
| t+16s  | 404 |
| t+36s  | 404 |

**到 t+36s 都還是 404。**

---

## 跟之前大樹作品 SOP 不一樣的地方

| 對比項 | 大樹作品（kind=creation）| 店家策展（kind=shop）|
|---|---|---|
| 5-8 秒後就 200 | ✅ 上次都成功 | ❌ 30 秒後還 404 |
| 後端處理時間 | ~5 秒 | **尚未完成** |
| 系統需要做的額外事 | 無 | 插入店家名冊、發 FB 貼文、建 GitHub repo |

→ 懷疑是店家流程某個**中間步驟**卡住（名冊/FB/repo 三件事之一），**不一定是 index.html 問題**（因為這份有 index.html）。

---

## 我沒做的事

1. ❌ 沒重送 curl（怕變重複，跟「證明給機器看」那次一樣教訓）
2. ❌ 沒去動 registry / coach888 / GitHub repo（策展 SOP 系統會自動處理，不該手改）
3. ❌ 沒去看 log（不知道 log 在哪）

---

## 請軍師協助

### 想要的答案（任一）

**選項 1**：直接幫我做策展上架這一條（檔案我有、slug `hsinhan` 確定），做完回信讓我知道結果。
**選項 2**：告訴我哪裡可以看後端 log（我想自己撈來看）— 路徑跟指令就好。
**選項 3**：告訴我剛剛那次 curl 觸發到了什麼步驟（讓我心裡有底，是不是真的進到「插名冊」了還是根本沒開始）

### 我已做的部分（你直接接下去也行）

- ✅ zip 已上傳（curl 200，server 有收到）
- ✅ slug `hsinhan` 已指定
- ✅ kind=shop 已指定
- ✅ 店家中英文名稱已查到（鑫瀚昌旅行社 / Euporos Hsin Han Travel Agency）
- ✅ README + index.html 都正常（不是損壞 zip）

---

## 附件資訊

- **檔案路徑**：`/Users/bymyway/.hermes/cache/documents/doc_28cde764d4c2_xinhanchang-travel-website.zip`
- **檔案大小**：3,224,747 bytes（約 3.2MB）
- **店家**：鑫瀚昌旅行社有限公司（阿翰的家），台南安南區北安路三段，交通部觀光署註冊甲種旅行社（註冊編號 888100）
- **slug**：`hsinhan`
- **kind**：`shop`（店家，不是教練個人創作，所以這次走策展 SOP 不是大樹作品 SOP）

— Hermes
2026-09-26 12:45 台灣時間
