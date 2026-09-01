---
name: reference-css-masonry-flow-vs-manual-row-pairing
description: 多個長短不一的區塊要排成兩欄時，用CSS column-count流式排版取代手動row/col配對；大幅HTML結構重排優先整檔案重寫不要用regex片段替換
metadata: 
  node_type: memory
  type: reference
  originSessionId: d5fe9c18-5091-4fff-8716-7d9c0b806495
  modified: 2026-09-01T11:18:30.168Z
---

## 問題情境
coach888作品總覽表有8個分區(項目數3~17項不等)，原本手動用`.row{display:grid;grid-template-columns:1fr 1fr}`把每2個分區強制配成一排、4排。教練回報「排版壓縮凌亂」——短區塊(5項)配長區塊(10項)同一排時視覺不平衡。

## 解法：CSS多欄流式排版取代手動配對
```css
.wrap { column-count:2; column-gap:48px; }
.section-block { break-inside:avoid; -webkit-column-break-inside:avoid; display:inline-block; width:100%; }
```
把每個分區包一層`.section-block`，直接當作`.wrap`的連續子元素（不再用`.row`/`.col`手動兩兩配對）。瀏覽器像排報紙分欄一樣自動把內容依序往下填滿左欄、再接右欄，任何分區項目數增減都會自動重新平衡，不需要每次手動調整配對關係。`break-inside:avoid`確保單一分區不會被硬生生從欄位中間截斷。

**適用場景**：任何「多個長短不一的內容區塊要排成N欄」的靜態頁面（跟教練說「就是兩欄/兩排就好」但區塊大小差很多時），優先想這個模式而不是手動`grid-template-columns`配對。

## 教訓：大幅HTML結構重排，regex片段替換容易漏算巢狀div，優先整檔案重寫
把`.row`+`.col`兩層巢狀結構改成`.section-block`單層時，第一次嘗試用node/regex做局部字串替換（match「grid關閉+col關閉+col開啟」這類3行連續pattern），因為：
1. 原始檔案是CRLF換行(`\r\n`)，正則沒考慮`\r?`導致完全match不到
2. 巢狀div結構在「第2個分區」跟「換行進新row」兩種transition的實際行數不一致，regex對其中一種pattern少算了一層`</div>`

改用CRLF-tolerant regex後雖然match上了，但因為最初對「該替換掉幾個`</div>`」的心算有誤，替換完後**用`(<div\b/g).length` vs `(<\/div>/g).length`比對總數，發現不平衡(299 vs 298)**，才確認真的有bug。與其繼續在regex上除錯，直接把已知正確的每個分區內容（section-title+grid+可選note）依序組裝成完整檔案用Write工具整篇重寫，重寫後同樣用div開合計數(307/307)+逐分區item數比對(70項)雙重驗證通過才commit。

**教訓**：HTML/程式碼要做「結構性重排」（不是單純改文字/改一兩個屬性）時，若涉及巢狀標籤的開闔關係在不同位置形狀不一致，regex片段替換很容易顧此失彼。判斷標準：如果同一種語意轉換（例如「換到下一個區塊」）在原始檔案裡有兩種以上不同的字面pattern（因為原作者手寫時前後不一致），別硬凹一條regex吃掉所有情況，直接讀懂全部內容後重新組裝整篇檔案更可靠，並且**用機械化的計數比對（div開合數、item總數）驗證，不要只憑肉眼看幾行**。

Related: [[feedback_screenshot_rules_consolidated]]（同一場對話另一個教訓：診斷視覺問題別急著想截圖，先看能不能用結構分析取代）
