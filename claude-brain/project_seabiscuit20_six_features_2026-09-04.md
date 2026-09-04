---
name: project-seabiscuit20-six-features
description: 海餅乾俱樂部20週年官網(Coach1973/seabiscuit20)六項新功能建置完成，含頁面結構+頁尾連結全貌
metadata: 
  node_type: memory
  type: project
  originSessionId: 65a4f974-3ac9-474c-8683-dbde5d132d06
  modified: 2026-09-04T08:19:50.721Z
---

seabiscuit20（https://coach1973.github.io/seabiscuit20/）是單頁式(SPA)靜態網站，用JS的`navigate(pageId)`切換`.page`區塊，本場（2026-09-04）在既有的首頁/傳奇/俱樂部/信念/紀念冊/願景基礎上新增：

- **時光足跡**（`#trail`）：180+1張教練提供的俱樂部歷史照片，CSS多欄masonry照片牆+獨立lightbox，圖檔存於`assets/trail/`。
- **見證**（`#testimonials`）：從bymyway-website（大樹教育官網）移植的20則真實學員見證，獨立成頁（原本誤放在「俱樂部」頁裡，教練找不到入口後才移出）。
- **語錄**（`#quotes`）：30張教練提供的海餅乾語錄卡圖片（`assets/quotes/`），單張淡入輪播。
- **信念與守則頁**內建的「智慧之言」語錄輪播：從4則擴充到22則，一字不差移植bymyway-website的「經典金句」全部內容。
- **信念與守則頁**新增「完整守則」發光連結+彈窗：教練提供的守則卡圖片（`assets/rules-card.jpg`）+團隊使命/三大信念/十大守則完整文字+2支YouTube影片（海餅乾15週年慶9fAWItpusJU／海餅乾守則PT7Ue8iQgIw）。
- **全站9個頁面頁尾**統一新增三欄快速連結（logo在上→近期活動/聯繫方式/快速連結三欄→版權宣告）：
  - 近期活動：大樹小講(event.bymyway.com/bigtree/)、AI微論壇台南場9/22(event.bymyway.com/ai-talk/)、AI轉念台南場9/22晚上(coach1973.github.io/ai-fit/)、AI微論壇台中場(event.bymyway.com/ai-forum/)、AI微論壇台南場10/7–8(同ai-forum，日期到了會直接覆蓋內容不用改連結)、高雄音樂流水席(event.bymyway.com/ai-art/)
  - 聯繫方式：LINE(lin.ee/o5pODV8)、Facebook(facebook.com/seabiscuitclub)、乾淨世界頻道(ganjingworld.com/@bymyway)、電子信箱(bymyway7@gmail.com)
  - 快速連結：大樹教育官方網站(www.bymyway.com)

**Why:** 教練把seabiscuit20當作大樹教育官網生態系的一環在經營，密集要求把bymyway-website既有內容（見證/語錄/官方連結）+近期活動微站全部匯集進來，希望訪客從這個20週年紀念站也能一路連到教練其他所有對外服務。

**How to apply:** 之後若教練要在seabiscuit20新增頁面，記得：①桌機`.nav-links`+手機`.mobile-menu ul`兩處都要加連結 ②`navigate()`函式裡的`valid`陣列要加新頁面id ③新頁面若有輪播/lightbox，優先抄既有的`quote-carousel`(單張淡入)或`testi-carousel`(多張橫移)模式，不要重造輪子 ④大範圍HTML替換一律用exact字串`.replace()`+`.count()`驗證，不要用regex非貪婪`.*?`跨越巢狀`<div>`（會切錯邊界，見[[reference_search_image_files_include_webp_2026-09-04]]同場踩過的div平衡bug）⑤每次push前先跑`open div`/`close div`計數腳本確認平衡。
