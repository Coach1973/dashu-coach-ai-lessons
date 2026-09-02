---
name: feedback-cap-retries-report-when-stuck
description: 卡在同一個技術死角時最多試3次就要停手回報，不能悶頭死磕燒教練的時間/金錢/token；跟feedback_exhaust_own_tools_before_asking_coach是互補的兩面
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f2c9facb-b15d-4dc5-a667-c1efd909155b
  modified: 2026-09-02T18:12:09.169Z
---

同一個技術路徑卡關，最多嘗試約3次就要停手，主動回報「這個做法行不通」，不能悶著頭一直換花招硬幹到底。

**Why**：2026-09-03教練委託複製一份Google表單（南應大校友會入會申請）並接Telegram通知，AI在Google表單編輯器的「必填」自訂開關上，換了六七種點擊/鍵盤/JS事件模擬手法死磕十幾分鐘都點不動；换成Google Apps Script想直接寫程式建表單，又踩到編輯器中文+程式碼混打時吃掉所有標點符號的怪異行為，仍然沒有停下來評估、繼續往下試。教練直接點名：「你會不會效率太慢了」「浪費我這麼多時間」「浪費我的token、金錢、生命」。教練事後定調的具體規則：**同一個問題試差不多3次不行，就趕緊回報**，不要等到搞了半天徹底失敗才承認。

**How to apply**：
- 遇到UI自動化/API呼叫/任何具體技術操作卡住時，內心默記已經換了幾種手法（不同的點擊方式、不同的事件模擬、不同的選取器都算「一種嘗試」），第3次還是不行，立刻停手回報現況，不要想著「再換個方法應該就通了」。
- 回報時要誠實講清楚卡在哪、已經試過什麼、為什麼判斷這條路走不通，然後**主動提出替代方案**讓教練選（不是丟回一句「做不到」就結束）——參考[[feedback_exhaust_own_tools_before_asking_coach]]的精神，停手不等於放棄，是換一條更務實的路。
- 這條規則跟「窮盡自己工具再問教練」不衝突：那條是說「你能自己做的事不要推給教練做」，這條是說「你在同一個死胡同裡狂試不會變出新結果時，要有停損點」——兩者合起來是「該自己扛的扛，扛不動的要儘早講」。
- 典型會踩線的場景：客製化UI元件（如Material Design切換開關）用合成滑鼠事件點不動、程式碼編輯器的IME/自動配對括號吃掉字元、第三方系統的隱藏驗證擋住操作流程——這類「怎麼換手法都一樣結果」的情況，就是該回報的訊號，不是該加碼嘗試的訊號。

Related: [[feedback_exhaust_own_tools_before_asking_coach]]、[[feedback_dont_surface_own_tangential_findings]]
