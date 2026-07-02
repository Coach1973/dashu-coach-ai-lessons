# 軍師接力棒 · 2026-07-03 v41（Mac 終端機 Sonnet）

> 建立時間：2026-07-03 清晨 6:03（台灣時間）
> 本棒執行者：Mac 終端機軍師 Sonnet 5
> 上一棒：v40（Mac 終端機 Sonnet，7/2下午5:40，兩個卡住的行銷網頁任務接回上線+VPS雙查證）
> 本棒主軸：**2026講座系列行銷頁大改版（黑金風格整合）+ 首次驗證自動站SOP（bymyway.com/bigtree/）零空白上線**

---

## 🎯 本場戰果

### 1. ✅ 講座系列行銷頁全面改版，套用大樹教練個人品牌黑金風格
教練指定用 `coach1973.github.io/bymyway-website/`（黑底金字風格）當底，把原本的speakers-2026行銷文案（我不藏私/知道卻做不到/五個相信/品牌一致性/羽毛珍惜條款/凡走過必留痕跡）整合進去，並經過教練10+輪逐項微調（字級統一成hero級48px、文案精簡、內容重排、新增回到頂端按鈕）。最終版：`Coach1973/bigtree` repo `speakers-2026/`子目錄，commit `c00f0de`。
線上：https://coach1973.github.io/bigtree/speakers-2026/

### 2. ✅ 首次完整走過「自動站SOP」全流程，零空白零表頭殘留一次上線成功
教練要求把這頁掛到 `bymyway.com/bigtree/`（測試版本位，之後視效果再決定要不要也用在正式的coach網址）。**這是教練反覆抱怨「自動站每次推都會空白」的地雷區**，本場嚴格照SOP v3.4走：
- 步驟0 OPE先驗法：curl `bymyway.com/coach/` 的 REST API 看真實成功案例的iframe寫法，直接照抄（`height:100vh`，不是`min-height`）
- content 用單行字串拼接 + `<div>`包裹（防wpautop把`\n`轉`<br/>`、把iframe包進`<p>`）
- 套用 `elementor_canvas` 模板拿掉bymyway表頭footer
- slug用`bigtree`（先curl確認404未被佔用，非WooCommerce保留字）
- draft建立→本機預覽→教練確認「推」→改publish→線上逐項驗證

**線上驗證結果（首次零地雷）**：header出現0次、footer出現0次、`<br/>`殘留0個、iframe height:100vh確認存在。唯一發現：瀏覽器分頁標題WordPress自動加了「– 大樹教育顧問」後綴（非頁面內容表頭），已誠實告知教練，因這頁本來就是教練自己的內容判斷可以保留，教練尚未回覆是否要處理。

**線上網址**：https://www.bymyway.com/bigtree/（page_id 27393）

### 3. 🔴 詞彙記憶檔驗證有效但查證流程有缺口
教練說「行動站的SOP」時，軍師沒有先查`feedback_coach_deploy_vocabulary.md`（裡面早就寫死「自動站＝行動站同義」），而是憑語意推論猜對。教練隨後親口重申確認。已補記憶檔提醒「聽到部署詞彙第一動作查記憶檔，不是憑語感猜」。另外教練提到「網頁推到Netlify」一度疑似要改詞彙定義，AskUserQuestion確認後**維持舊定義不變**（網頁推=GitHub、單字推=Netlify）。

---

## 📋 下一棒待辦

| 優先 | 對象 | 任務 |
|------|------|------|
| 🟡 | 下一棒軍師 | 教練說「如果bigtree版本效果更好，之後改成COACH」——等教練决定是否要把`bymyway.com/coach/`也换成這個新版黑金風格內容，或維持兩者並存 |
| 🟢 | 下一棒軍師 | 分頁標題「– 大樹教育顧問」後綴是否要拿掉，等教練回覆 |
| 🟢 | 下一棒軍師 | speakers-2026頁面事件卡目前是「排程中」狀態，等教練給出2026實際講座場次真實資料再填入 |
| 🟢 | 下一棒軍師 | OG meta（LINE/FB分享卡）+ site_icon尚未針對`/bigtree/`頁面單獨設定，如果教練要分享這個連結出去，需要照SOP步驟9補上（目前分享會fallback顯示大樹教育logo，不是講座頁專屬圖） |

---

> Mac 終端機軍師 Sonnet 5 親筆，2026-07-03 清晨6:03台灣時間。
