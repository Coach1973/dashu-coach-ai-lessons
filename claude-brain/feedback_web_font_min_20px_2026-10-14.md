---
name: feedback-web-font-min-20px
description: 教練 10/14 定：我們做的任何網頁字最小 20px；module_kit check 會擋 px 寫法；既有 43 站小字多數是 rem/em，全面改要教練定範圍
metadata:
  node_type: memory
  type: feedback
  originSessionId: ba79a2ec-9970-45c6-82fc-a131cdcda823
  modified: 2026-10-14T03:23:42.671Z
---

教練 2026-10-14 原話：「我們做的任何網頁，字體大小最少都要 20px，如果沒有的話要調整一下。」

**Why:** 教練與來賓多半用手機看，字小看不清（同一場也要求邀請函「陽光多一點、亮堂一點」，重視好讀）。

**How to apply:**
- 新做／修改的網頁：所有字（含小註、按鈕、表單說明、<small>）計算後 ≥20px。交付前跑 `python3 scripts/module_kit.py check <slug>`，會列出 CSS 裡 font／font-size 小於 20px 的寫法（只抓 px，rem/em/瀏覽器預設小字抓不到，要用瀏覽器量 getComputedStyle）。
- 坑：`font:500 19px/1 inherit` 這種簡寫加 inherit 整條失效，按鈕會掉回瀏覽器預設 13px（榮樹下來賓資料表踩過）。
- 10/14 盤點：event.bymyway.com 策展 57 站有 43 站有小字，每頁小字元素 40～530 個，多數是 rem/em 不是 px；EDM／og 分享圖頁（1080/1200 寬）是出圖用，不適用。全面改會大改夥伴網站版面，範圍等教練裁示（見 [[project-rongtree-guest-form-card-prep-section]]）。
