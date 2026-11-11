---
name: feedback-realscene-without-ref-photo-generate-as-concept
description: 出圖清單標「實景修飾」但參考照片欄是空的＝沒有底圖可修，直接當概念圖用 LK888 出，不准停下來跟教練要真實照片
metadata:
  type: feedback
---

TAVA prompts 清單裡「實景修飾」類型，若 ref 欄空白（金門 kinmen-1205 的 13 張美食物產），代表根本沒有真實照片；run_img_list.py 會跳過它，我就停下跟教練要照片，教練 11/11 火大：「明明是創造的圖片，為什麼還要真實照片？我哪來的真實照片？」

**Why:** 教練不可能有照片，問了只是讓他當搬運工（守則 #12）；先前 [[feedback-real-scene-slots-find-reference-yourself-not-ask-coach-2026-11-06]] 的前提是「倉庫裡找得到本人照」，沒有照片時不適用。
**How to apply:** 被跳過的實景修飾項，先查倉庫有沒有照片；沒有就把 type 改成「概念」、file 設 <id>.png，分批（每批≤12 張）用 run_img_list.py 跑完，同一輪交圖，不問。
