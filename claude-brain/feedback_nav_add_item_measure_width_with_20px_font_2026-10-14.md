---
name: feedback-nav-add-item-measure-width-with-20px-font-2026-10-14
description: 頂部選單加一個項目前先量寬度；字最小 20px 時多一項就會讓整排折成兩行（公益路跑 10/14 被教練截圖抓到）；手機窄螢幕選單消失＝要用共用漢堡選單
metadata:
  type: feedback
---

2026-10-14 我在公益路跑頂部選單加第 7 項「志工團隊」，加上「網頁字最小 20px」規定，整排選單與品牌名全折成兩行（「為什麼參與」被拆成「為什麼參／與」），教練截圖說「表頭字太大、太擁擠」。接 [[feedback-web-font-min-20px-2026-10-14]]。

**Why**：20px 下每多一項約 +100px，原本剛好放得下的版面就爆；而且各站窄螢幕時選單是整個 `display:none`，手機上根本沒導覽。
**How to apply**：①改頂部選單（加／改字）之後，用 1440／1280／1210／手機寬度量「每項高度是不是單行、`.wrap` 有沒有 overflow」再交；②寬度不夠先拿掉頂部列次要文字、`white-space:nowrap`、調整收合寬度，不要縮字（20px 是死規則）；③手機／平板導覽統一用共用模組 `event-signup/static/nav-burger.js`（模組庫第 11 項，連結複製頂部選單），不要每站自己寫；改共用檔要把各站 `?v=` 加一。已接：rongtree、runforfuture、social-club、social-good。
