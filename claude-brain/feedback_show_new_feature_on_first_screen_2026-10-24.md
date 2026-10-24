---
name: feedback-show-new-feature-on-first-screen
description: 做預覽頁要教練看新功能時，新功能必須落在第一屏；按鈕在頁面第 1788px、螢幕只有 958px，教練滑不到就說「看都沒看到」，我卻連問兩次 OK 不 OK
metadata:
  node_type: memory
  type: feedback
---

人才軍火庫「你想解決什麼？」12 顆需求按鈕放在名錄區上方，離頁首 1788px；教練螢幕一屏約 958px，要滑兩屏。他沒看到按鈕，也就不知道要看什麼；我隔夜開工還在問「OK 不 OK」，他很不耐（10/24 02:43、02:41）。

**Why:** 教練是用眼睛驗收，不會主動往下找；我用 `getBoundingClientRect` 一量就知道在不在第一屏，卻沒量。
**How to apply:**
- 交預覽頁給教練看新功能前，用 Chrome 的 javascript_tool 量新功能的 top 是否 < innerHeight；不在就讓頁面一打開自動捲到那裡（`scrollIntoView`，已用在 skyteam preview-need.html，skyteam 5983ecf）。
- 教練說「我沒看到」＝先重現他看到的畫面，不要再問同一個問題。
- 同場另有：用 `scripts/deliver_open.sh` 開頁面有時沒開成（這次輸出看不出），要再讀回分頁網址確認；Chrome 讀 JS 要走 claude-in-chrome 的 javascript_tool，osascript 的 execute javascript 被 Chrome 設定關著。
相關：[[feedback-opened-on-mac-is-not-delivery-phone-coach]]
