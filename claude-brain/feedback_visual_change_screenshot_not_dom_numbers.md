---
name: feedback-visual-change-screenshot-not-dom-numbers
description: 排版/裁切/擠壓/美感類問題，preview_eval讀DOM數字不能替代截圖親眼看——工具本身可能因視窗異常/CSS快取回傳失真但看似精確的數字
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 99c3ea2b-7e18-4617-8ac4-bd4cd1cc69fa
---

# 🔴🔴 視覺類任務唯一可信驗證是截圖，不是 DOM 數字（教練 2026-07-03 罵醒）

**規則**：任何跟「畫面好不好看、有沒有裁切、有沒有擠壓、排版對不對齊」相關的改動，**送出給教練看之前，先用截圖（`mcp__computer-use__screenshot` 或開真的 Chrome）親眼確認**。`preview_eval` 讀 `getBoundingClientRect()`/`getComputedStyle()` 這類 DOM 數字只能輔助，不能當成「已經驗證過畫面」的替代品。

## Why

2026-07-03 講座頁 logo 被切到，軍師連續 5、6 輪只用 `preview_eval` 抓數字判斷有沒有修好，完全沒截圖。後來發現這個特定預覽工具的視窗一度異常（`innerWidth` 變成 1、CSS 版本沒 bust 讀到舊快取），回傳的數字看起來精確（有具體 px 值）但完全不代表真實畫面，軍師被「有數字=有根據」的假象騙過，反覆在錯誤數據上改錯，教練坐在螢幕前人工回報「左邊一點、右邊一點」近一小時。教練罵醒：「你自己去看一看、檢視一下，你自己有沒有美感？」

罵醒後申請截圖權限、真的看一次畫面，一次就準確抓到真問題並給出正確判斷——證明問題不是沒審美，是審美能力全程沒被用上。

## How to apply

1. 遇到排版/裁切/擠壓/對齊/好不好看類任務，**第一時間就申請截圖權限**（`mcp__computer-use__request_access` + 若被 `screenshot_lock.sh` 擋下，直接問教練「這是視覺類改動，可以截圖確認嗎」），不要先用數字工具頂著
2. 同一個 DOM 數字連續 3 次以上量出一樣不合理的結果、且不隨改動變化 → 懷疑工具本身有問題（但更早的正確動作是一開始就用眼睛看，根本不會走到「該不該懷疑工具」這一步）
3. `preview_eval` 的角色是「輔助定量驗證」（例如確認元素寬度、確認沒有溢出），不是「視覺驗收」本身

## 反例（不可再犯）

❌ 只用 `preview_eval` 讀 `getBoundingClientRect()` 就判斷「修好了」，沒有截圖或開 Chrome 給教練/自己看
❌ 數字連續多輪異常還繼續在同一套工具裡打轉，不換驗證方式
❌ 把「截圖需要教練同意」當成「可以先不截圖」的藉口，而不是「該主動申請」的訊號

## 對應機關（待建）

Stop hook 偵測 Edit/Write 觸及 `style.css` 或 HTML 的 `class`/`style` 且涉及 `display`/`flex`/`width`/`gap`/`font-size` 等版面屬性時，提醒「這是視覺類改動，送出前是否已截圖親眼確認？」（尚未實作，見試金石案例38待建機關）。

關聯：[[feedback_screenshot_rules_consolidated]]（截圖鐵律：需教練同意才截圖）、守則#03（作品出來之前自己要先看過）
詳細血淚過程：`試金石/試金石_案例庫.md` 案例38
