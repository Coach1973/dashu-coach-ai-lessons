---
name: reference-line-oa-chat-plan-monthly-and-send-limit
description: LINE 官方帳號「標籤」要買聊天進階方案（月租 NT$100 未稅，會自動續扣）、怎麼看預定付款與取消；後台手動一對一聊天「短時間上限」的官方數字
metadata:
  node_type: memory
  type: reference
  originSessionId: 886a007e-d9a7-4ddf-8646-c9cd9970e016
  modified: 2026-11-02T05:40:04.978Z
---

**聊天進階方案（標籤功能）**：2026-11-02 教練在大樹教育顧問（@qaw8118h）開通標籤，付 NT$105（含稅，未稅 100）。這是**月租、會自動續扣**，不是單次：後台「帳務專區 → 總覽頁面」的「預定付款」會列出下月（當時 12/01 NT$100）。取消＝總覽頁「變更方案」把聊天方案改回免費；教練 11/02 自己按了，我讀回「尚無預定付款資料」。已扣當月費用退不退後台沒寫，要問 LINE 客服。官方公告 10/28–11/2 暫停方案變更與付款功能。帳務頁用 get_page_text 讀（read_page 常回空）；截圖被截圖鎖擋，不用截圖。未確認：chat.line.biz 路徑裡的 `U995…` 對應哪個帳號。

**後台手動一對一聊天上限**（官方 FAQ tw.linebiz.com/faq/oa-chat/chattinglimit/）：1 小時內對超過 200 個不同聊天室發訊息→暫時限制，提示「已達短時間內可發送的訊息數量上限，請稍後再試」；暫停多久官方沒寫，建議等 1 小時以上。未認證帳號另有：7 天以上沒回覆的聊天室，每日最多 200 則。第三方網站的「每分鐘 17 則」「24 小時」互相矛盾、沒官方出處，不採用。教練說發約 100 則就被擋，低於門檻，原因沒查明。

相關：[[reference-line-quota-push-counts-per-member-registration-forward]]、[[feedback-line-push-needs-coach-approval-standing-order]]。
