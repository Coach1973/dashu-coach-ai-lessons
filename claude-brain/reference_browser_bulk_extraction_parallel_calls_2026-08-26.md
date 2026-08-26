---
name: reference-browser-bulk-extraction-parallel-calls
description: 如何用javascript_tool高效爬取瀏覽器頁面上的大量資料(千筆以上)，含response截斷限制、失敗過的下載路徑、完整性驗證方法
metadata: 
  node_type: memory
  type: reference
  originSessionId: bae7c68e-400f-478f-a3d8-5d27eb6b1211
  modified: 2026-08-26T05:33:15.456Z
---

2026-08-26收集BNI Connect來賓資料時，需要從瀏覽器記憶體(`window.__bniGuestsMini`陣列)取出3712筆資料存進本機檔案。過程踩出一套可複用的技巧。

**核心限制**：javascript_tool的回傳值有硬性截斷，純ASCII約1000~1200字元、含中文的TSV格式(姓名/電話/email三欄)約25筆記錄後就會被截斷，跟輸入的JS程式碼長度無關(輸入可以很長，例如把3000+筆已收集電話清單塞進JS當比對用的Set，44KB照樣正常執行)。

**失敗過的下載路徑，不用再試**：
- `Blob`+`createObjectURL`+`<a download>`.click()——Chrome認定這不是真人手勢觸發，靜默不下載，不報錯
- `window.open(blobUrl)`——被彈出視窗攔截器擋掉
- `location.href = 'data:...'`——Chrome自Chrome 82起禁止頂層導覽到data: URI(防釣魚)，靜默失敗
- AppleScript `execute javascript`控制Chrome——需要開啟「允許Apple事件的JavaScript」，但claude-in-chrome擴充功能已連接該分頁時這個選項在選單上顯示為disabled(灰字點不動)，猜測是Chrome刻意避免跟自動化擴充功能衝突

**真正有效率的做法**：既然每次呼叫只能拿到~25筆，就別用單一cursor靠上一次呼叫結果算下一批(容易累計計數失誤)，改成：
1. 直接用固定索引`array.slice(start, start+25)`取值，start由自己算好，不依賴任何前一輪的回傳
2. 因為每個索引範圍互不依賴，可以在同一輪對話回合內一次送出10個(甚至更多)獨立的javascript_tool呼叫——工具支援多個獨立呼叫並行執行，這樣單一回合就能拿到250筆，把原本要跑150輪的工作壓縮到15輪左右
3. 資料落地時用「每個索引範圍一個檔案」(如`r1000_1250.tsv`)取代不斷append同一個檔案，檔名本身就是完整性的證據，不會有「這個flush到底寫到第幾筆」的計數混亂

**完整性驗證，不要用人工算行數**：光數wc -l很容易被「這批我到底收了幾筆」搞混（這次就因為手滑漏algo了一個25筆區間，靠肉眼對不出來）。正確做法：
1. 把已收集資料的某個唯一鍵(這次用電話號碼)全部撈出，用Python轉成JSON陣列
2. 把這個JSON陣列直接餵進javascript_tool的輸入(當成JS的`Set`字面量)——輸入沒有截斷限制，塞3000多筆也沒問題
3. 在頁面裡跑`sourceArray.forEach((item,i)=>{ if(!collectedSet.has(item.key)) missing.push(i) })`，只回傳「還缺哪些index」，這個回傳很小、不會被截斷
4. 抓到缺口後直接用同樣的`slice(missingIndex, missingIndex+1)`點對點補齊，最後再跑一次同樣的diff確認`missingCount===0`才算真的做完

這套「輸入不限、輸出限縮、用程式diff代替人工計數」的模式，適用於任何「要把瀏覽器頁面裡幾百筆以上資料轉存到本機」的任務(名片系統/BNI Connect還有其他分會來賓、其他大量清單抓取)，下次遇到類似需求直接套用，不用重新摸索下載路徑或被截斷卡住。
