---
name: project-bni-dna-attendance-dashboard-2026-07-08
description: coach1973.github.io/bni-dna 大台南南區DnA團隊出缺席戰情儀表板，2026-07-08教練親自維運，全年12個月出席表+滾動式淘汰規則+全勤獎
metadata: 
  node_type: memory
  type: project
  originSessionId: ba466be0-58a7-4f84-a170-be1f5344791a
---

repo：`Coach1973/bni-dna`（GitHub Pages，master 分支根目錄自動部署，非 Netlify）。單一 `index.html`，教練每月開完 DnA 例會後口述出席名單，軍師手動更新表格，commit + push 即上線，不走zip+API。

**2026-07-08 這場的變更**：
- 新增 7月(7/8) 出席資料：16人出席各附鏡頭狀態備註（如「定點開鏡頭」「移動開鏡頭無發言」「前20分鐘沒開鏡頭」），用 `.present-detail` CSS class 顯示（跟純文字「出席」的 `.present` 不同）
- **移除7位夥伴整列紀錄**（不是標記缺席，是整筆刪除）：陳欣佑、張羽家（原本就核准移除）+ 朱正文、康文彬、莊弼翔、張騰文、鄭綉美（教練追加，這5位都是累計達2次缺席門檻）
- **預排全年12個月表頭**：8月(8/12)、9月(9/11)、10月(10/14)、11月(11/11)、12月(12/11)，尚無資料的月份用 `.null-data` 顯示「-」佔位，之後每月逐一補實際出席資料
- **出席政策改版**：淘汰規則從「固定兩次缺席」改為**滾動式計算：任何5週內累計缺席達2次即淘汰**；新增**全勤獎**公告——全年12次月例會全數出席，教練親自頒發
- 已備好 `.perfect-attendance` CSS（金框+金字），等12月有人真的滿12次時套用，目前無人達標不顯示

**設計慣例**：分「原始成員」與「Nyx月份入隊生力軍」兩組，各自依出席次數由高到低排序，用 `divider-row`（`⚡ N月份入隊生力軍 ⚡`）分隔，divider colspan 要跟着欄位數同步更新（本次改為15：排名+姓名+12月+總出席）。新成員入隊前的月份用 `.null-data` 「-」而非「缺席」。

**部署流程**：本機先用 `git clone` 到 `~/Documents/coach-projects/bni-dna`（不在workspace內），改完先起 `.claude/launch.json` 裡的 `bni-dna-preview`（port 8796，static python server）用 `preview_eval` 讀 DOM 文字驗證資料正確（不截圖，遵守截圖鎖），再用 `open -a "Google Chrome" <path>` 開真實瀏覽器讓教練用RustDesk螢幕親眼確認，教練說「推」才 `git push origin master`，用 `gh api repos/Coach1973/bni-dna/pages/builds/latest` 輪詢確認GitHub Pages真的build完成（status: built）才算上線驗證完畢。

**commit**：`8646ef2`（7月資料+移除7人+全年預排+滾動式規則+全勤獎）

Related: [[reference_coach_websites]]（教練作品清單，之後應補上bni-dna）
