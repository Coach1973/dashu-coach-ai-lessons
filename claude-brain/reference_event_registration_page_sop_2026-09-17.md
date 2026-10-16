---
name: reference-event-registration-page-sop-2026-09-17
description: 教練親定「報名頁上架SOP」——TAVA AI等工具做的一頁式報名網頁(多為大樹小講/教練演講活動)上架到event.bymyway.com，涉及event.db寫入+即時Telegram通知，跟「策展SOP」是同一個「上架SOP」觸發詞下的另一條分支
metadata:
  type: reference
---

# 🎯 報名頁上架SOP（2026-09-17 教練口述，軍師制定）

> 跟其他三套既有SOP的關係（四者目標不同，不可混用）：
> - **網頁推SOP**（[[feedback_web_push_sop]]）：推送到GitHub測試站或Netlify正式站，教練說「網頁推/推」才觸發
> - **自動站**（[[feedback_coach_deploy_vocabulary]]）：部署到bymyway.com（WP iframe抓GitHub repo新版）
> - **策展SOP**（[[reference_curation_sop_2026-09-06]]）：**店家/品牌介紹網站**，靜態內容，上大台南策展中心，不涉及資料庫
> - **本SOP（報名頁上架SOP，NEW）**：**一頁式報名網頁**（多數是大樹小講活動或教練演講），需要即時寫入報名資料庫+觸發Telegram通知，上event.bymyway.com

## 🎯 自動分流判斷規則（教練說「上架SOP」，不用另外分兩個詞）

教練丟一個TAVA AI等工具做的網頁要上架，只要說「上架SOP」，AI 自己依內容判斷走哪條路，不用教練額外說明：

- **內容有報名表單**（姓名/電話/場次選擇/送出按鈕，通常是活動、演講、課程介紹）→ 走**本SOP**，上 event.bymyway.com
- **內容是店家/品牌介紹**（產品、地址、聯絡方式，沒有「報名」這件事）→ 走**策展SOP**，上大台南策展中心
- 真的分不出來（例如店家頁面也帶了一個簡單的聯絡表單，不確定算不算報名）→ 直接問教練，不要瞎猜

## 完整流程（五步）

**第一步｜教練生成網頁**
TAVA AI / Tooo.ai / Lovart.ai 等工具產出一頁式 HTML 報名頁，含表單欄位（姓名、電話，公司/Email/備註選填）。

**第二步｜建 GitHub Pages 靜態站**
跟策展SOP第三步同樣手法：建 repo（`coach1973/<slug>`，slug 用拼音或教練指定的短網址）、push、開 Pages。**這步不用 SCP、不用 VPS**，純靜態網頁，跟策展SOP的暫代頁機制無關。

**第三步｜報名表單接上共用 API（🔴 不要新建專屬端點）**
過去（tut-alumni／leader／KR／1010）每次都各自新建一個 `/api/<name>/join` 端點，程式碼越堆越多支要維護。**現在起一律重用已存在、通用的共用端點**：

```js
const BYMYWAY_API = 'https://event.bymyway.com/api/register';
fetch(BYMYWAY_API, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    slug: '<第四步建立的場次代碼>',
    name, phone, company, email, note,   // company/email/note選填，姓名+電話必填
    source: '<repo名稱，方便追來源>'
  })
});
```

這支端點（`event-signup/app.py` `api_register()`）是 fire-and-forget 設計：**永遠回 200**，不會擋住訪客報名體驗；成功時寫進 `event.db` 的 `signups` 表，並自動發 Telegram 到「活動報名即時通知」群組（教練+佩佩老師同見，不佔 LINE 配額）。就算 `slug` 打錯查無場次、或姓名/電話缺漏，也會發一則警示通知（不會讓報名者憑空消失），但這代表對接沒做好，不要靠這個保護網省略第四步。

**第四步｜在 event.db 建立場次代碼（slug）—— 這步跟第三步的 slug 必須完全一致**

兩種做法都可以：
- 網頁版（教練自己也能做）：登入 `event.bymyway.com/admin/sessions` 新增
- AI 直接用 curl（不用教練碰後台）：
```bash
curl -s -c /tmp/cookie.txt -d "username=0901056777" -d "password=88888" \
  https://event.bymyway.com/admin/login -o /dev/null
curl -s -b /tmp/cookie.txt -X POST https://event.bymyway.com/admin/sessions/save \
  -d "slug=<場次代碼>" -d "name=<活動名稱>" -d "event_date=YYYY-MM-DD" \
  -d "start_time=HH:MM" -d "location=<地點簡稱>" -d "venue=<場地全名>" \
  -d "address=<完整地址>" -d "status=active"
```
`events` 表欄位：`slug/name/event_date/start_time/site/slot_key/location/venue/address/transport/status/show_live_count/event_url`，不是每欄都要填，至少要有 `slug/name/event_date/status=active`。

**🔴 2026-09-17教練補充：如果這場活動屬於「大樹小講」(bigtree)系列，這步要多做一件事**——把第二步建好的報名頁 GitHub Pages 網址（`https://coach1973.github.io/<slug>/`）一併填進這筆 `events` 記錄的 `event_url` 欄位（用上面 `admin/sessions/save` 的 curl 指令時多帶一個 `-d "event_url=https://coach1973.github.io/<slug>/"`）。原因：`bigtree_publish.py` 本身已經有讀取 `event_url` 欄位的邏輯（不是新機制，這是既有的「我要看活動網頁」按鈕功能），只要這欄有值，大樹小講官網對應場次卡片就會自動出現連到這個報名頁的按鈕，不用另外手動改 bigtree 的原始碼或請教練確認。**這個關聯規則只適用於大樹小講系列**，其他非 bigtree 的一次性活動（如各校友會、企業內訓）不需要這步。

**第五步｜驗證**
```bash
curl -sI https://coach1973.github.io/<slug>/ | head -1     # GitHub Pages 應 200
```
接著送一筆**真實測試報名**，確認兩件事都成立：①Telegram「活動報名即時通知」群組收到通知 ②`event.db` 的 `signups` 表有新紀錄。驗證完把測試資料清掉。**不用另外通知教練**——Telegram 已經自動發了，這步系統已經做完，不用你再手動講一次。

## ⚠️ 特別注意

1. **不要用 LINE 通知**——2026-08-24 教練已拍板全面停用 LINE 推播（會扣月配額），只用 Telegram「活動報名即時通知」群組。
2. **深連結格式**：`?session=<場次名>&slot=<早半/午半/晚半>` 可以讓分享出去的連結直接預選場次，同一天多場次時務必帶 `slot`（同名場次分不出時段是舊坑，見 2026-08-25 教訓）。
3. **同一活動系列共用同一個 repo/網址**（例：`ai-forum` 台中場之後台南場沿用同網址覆蓋內容），網址代表「活動格式/系列」不代表地點，這是教練 2026-08-30 拍板的命名邏輯。
4. 這條路徑是純靜態 GitHub Pages + 呼叫外部 API，**不需要**在 `event-signup` 本身新增路由——那是像大樹小講(bigtree)這種需要「讀活 repo 即時渲染」的更進階做法，一次性報名頁不需要。
5. 教練若要求把已上線的報名頁短網址改掉，處理方式跟策展SOP的「改短網址三步驟」不同——報名頁只需要改 GitHub repo 名稱+events 表的 slug 欄位（兩處對齊即可，沒有暫代頁/redirect 機制），改完務必同步改第三步 JS 裡寫死的 slug，三處對不齊會變成「報名表單看起來正常但資料寫不進資料庫」。

## How to apply

教練說「上架SOP」時，先判斷內容類型（報名表單 vs 店家介紹）：報名頁照上面五步走；店家介紹走 [[reference_curation_sop_2026-09-06]]。不確定就問教練，不要瞎猜。

Related: [[reference_curation_sop_2026-09-06]]、[[project_bymyway_dynamic_hosting_escape_netlify_2026-08-30]]、[[feedback_web_push_sop]]

---
## 🛟 2026-10-16 從自動暫存救回的段落（原本在 2026-09-17 19:55 寫進來，被自動同步放回失敗弄丟；照原樣補回，未改寫）

**🔴 2026-09-17教練補充：如果這場活動屬於「大樹小講」(bigtree)系列，這步要多做一件事**——把第二步建好的報名頁網址一併填進這筆 `events` 記錄的 `event_url` 欄位。**⚠️2026-09-17實測修正：`event_url`不在`admin/sessions/save`表單白名單裡，用curl帶這個欄位會被靜默忽略（回應顯示成功，實際沒寫入，親身踩過一次）**，必須用直接寫DB的方式：
sqlite3 event-signup/event.db "UPDATE events SET event_url='<報名頁網址>' WHERE slug='<場次代碼>';"
