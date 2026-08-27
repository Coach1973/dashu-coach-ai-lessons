---
name: project-speakers2026-bigtree-launch
description: 大樹教練2026講座系列行銷頁完整改版+bymyway自動站首次零空白上線，最終網址與關鍵決策
metadata: 
  node_type: memory
  type: project
  originSessionId: 99c3ea2b-7e18-4617-8ac4-bd4cd1cc69fa
---

# 2026講座系列行銷頁 · bigtree 上線（2026-07-03）

## 現況（本場 session 定案）

**線上網址**：
- GitHub Pages 原始版：https://coach1973.github.io/bigtree/speakers-2026/
- bymyway 正式版（iframe嵌入，自動跟GitHub Pages同步）：https://www.bymyway.com/bigtree/（page_id 27393）

**風格來源**：套用大樹教練個人品牌黑金風格（`coach1973.github.io/bymyway-website/`），整合原本speakers-2026行銷文案（我不藏私/知道卻做不到/五個相信/品牌一致性/羽毛珍惜條款/凡走過必留痕跡）。

**Why**：企業健身房(biz-gym)跟講座行銷頁是歷史接力棒斷線的任務，教練要求接回；後來教練指定用bymyway-website風格整合成一頁式黑金主題行銷頁，測試版先掛`/bigtree/`（跟正式的`/coach/`分開），效果好再決定要不要替換或並存。

## 關鍵決策

1. **導覽列**：13項（關於教練/創業歷程/創辦理念/五個相信/品牌一致性/經典金句/線上課程/企業演講/學員見證/文章分享/活動快訊/常見問答/乾淨世界/立即聯繫），順序照教練指定的閱讀動線由上往下排列，**服務項目已從導覽拿掉**（只留區塊本身，不放連結，減少擁擠）
2. **Logo**：「大樹教練」四字橫排單行（不可上下堆疊，中文字沒斷詞規則會裁切），英文副標「DA SHU COACH」已從導覽列拿掉（footer保留）
3. **羽毛珍惜條款**：搬進「文章分享」區塊，比照現有4篇文章的彈窗機制呈現，按鈕在文章分享區跟「五件事不做」段落都有入口
4. **活動快訊**：新增3場真實場次（7/1一個下午三個答案-已回顧、7/4零基礎學AI比較快、7/18線上讀書會），舊有6場樣本資料的星期標示已核對2026真實日曆修正

## 自動站SOP驗證（首次零空白零表頭殘留）

嚴格照`knowledges/SOP_bymyway_auto_site.md` v3.4走：iframe用`height:100vh`（不是min-height）、content單行字串+`<div>`包裹防wpautop、`elementor_canvas`模板拿掉bymyway表頭、slug用`bigtree`（curl確認未被佔用）。線上驗證：header/footer出現0次、`<br/>`殘留0個。

## 待辦（下一場接手）

- 分頁標題WordPress自動加了「– 大樹教育顧問」後綴，教練尚未回覆是否要拿掉
- 教練說「如果bigtree效果更好，之後改成COACH」——等教練決定是否要把`/coach/`也換成這個新版，或兩者並存
- 事件卡目前部分場次時間標「時間確認中」，等教練補實際時段
- OG meta（LINE/FB分享卡）+ 這個頁面專屬site_icon尚未設定，若教練要分享連結出去需要照SOP步驟9補上

## 關聯

[[feedback_visual_change_screenshot_not_dom_numbers]]（logo裁切debug血淚教訓）、[[reference_coach_websites]]、`知識庫/SOP_bymyway_auto_site.md`
詳細過程：`試金石/試金石_案例庫.md` 案例38
