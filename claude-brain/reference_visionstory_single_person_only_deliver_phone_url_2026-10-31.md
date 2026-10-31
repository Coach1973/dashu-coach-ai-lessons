---
name: reference-visionstory-single-person-only-deliver-phone-url-2026-10-31
description: VisionStory API 只能單人說話（雙人同框做不到，用 ffmpeg 並排輪流）；教練在手機時影片要放臨時網址、SendUserFile 送不出
metadata:
  type: reference
---

VisionStory API（scripts/visionstory_api.py）只有單一人像說話；公開資料也找不到雙人同框，網頁版 Podcast 工具才有雙人鏡頭。教練要「我們兩個同框一起講」時：把照片裁成左右兩人各建 avatar（create-avatar --file，會自動抓畫面主要那張臉，先看 head 縮圖確認）、各生一句，ffmpeg hstack 並排、沒說話的定格，成品 1440×720。計點每 4 秒 1 點無條件進位（見 SOP_visionstory_影片生成_2026-10-31）。

**Why:** 10/31 我把「兩個年輕人的聲音」誤讀成單人換聲音被糾正；教練在手機，說「沒看到影片，給我路徑」，Mac 桌面他看不到，SendUserFile 在這種對話回「not on a project thread」。
**How to apply:** 教練說「我們兩個／同框」先想雙人；影片給手機看＝放 event-signup/static/_tmp_<隨機碼>/（加進 .git/info/exclude、確認後刪），回報寫完整網址一行一個；對外前提醒影片裡第三人要同意；聲音沒聽過要明說。
