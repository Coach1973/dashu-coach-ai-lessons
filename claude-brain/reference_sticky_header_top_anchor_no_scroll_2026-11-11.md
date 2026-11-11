---
name: reference-sticky-header-top-anchor-no-scroll
description: 頁首標題 href="#top" 點了不回頂＝#top 是 sticky 頁首本身；改 JS scrollTo＋instant 保險(bni-story 11/11)
metadata:
  type: reference
---
頁首連結 `href="#top"` 而 `id="top"` 掛在 `position:sticky` 的頁首上 → 瀏覽器認為目標已在畫面內，點了完全不捲。修法：click 時 `preventDefault()`＋`scrollTo({top:0,behavior:"smooth"})`，再 `setTimeout(700)` 檢查 scrollY>2 就 `behavior:"instant"` 補一次（隱藏分頁／部分瀏覽器 smooth 不動）。bni-story 2e63d01。驗證用「先捲到 5000、點、讀 scrollY=0」。相關 [[reference-sticky-header-broken-by-body-overflow-x-hidden-audit-method]]
