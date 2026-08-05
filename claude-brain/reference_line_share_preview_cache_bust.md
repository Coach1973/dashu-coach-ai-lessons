---
name: reference-line-share-preview-cache-bust
description: LINE分享連結預覽卡舊內容的處理方式——官方Page Poker工具已停用，唯一解法是網址加?v=參數（2026-08-05查證）
metadata:
  type: reference
---

# 🔴 LINE 分享連結預覽卡住舊內容，怎麼修

## 症狀
網頁內容已經改了（例如活動從台南場換成嘉義場），但貼到 LINE 分享出去，預覽的標題/圖片還是顯示舊的。

## 根因（2026-08-05 AI微論壇嘉義場實測發現）
1. 網頁本身可能**從未設過 `og:title`／`og:description`／`og:image` 標籤**，LINE 只能退而求其次去猜 `<title>`
2. 就算補上了 og 標籤，**LINE 會把第一次抓到的結果快取住**，同一個網址之後分享都直接拿快取，不會重讀

## 修法
1. **先確認網頁本身有沒有 og: 標籤**——用 `curl -s <網址> | grep 'og:'` 檢查，沒有就先補上（title/description/image 都要指定絕對網址，image 建議另外補 `og:image:width`／`og:image:height`／`og:image:type`）
2. **官方除錯工具 LINE Page Poker（`poker.line.naver.jp`）已停用**——2026-08-05 實測 DNS 查無此網域，不要浪費時間去試
3. **唯一可行的繞過法：網址後面加查詢參數**，例如原本 `https://ai-talk-tw.netlify.app/` 改貼 `https://ai-talk-tw.netlify.app/?v=2`——LINE 會當成新網址重新抓一次

## 限制（要跟教練講清楚，避免期待錯誤）
- **已經分享出去的舊訊息不會自動更新**，快取是綁在那則訊息上的，要教練自己刪掉重貼新網址版本
- LINE／Slack／Telegram 都沒公布快取多久會過期，無法精準預估「等幾天會自己好」

## How to apply
往後任何新建/大改的活動頁、行銷頁，**上線前就先補好完整 og: 標籤**，不要等分享出去才發現預覽是錯的——og 標籤本身沒有快取問題，快取是分享之後才產生的，越早補越不會踩到「已經分享出去改不了」的坑。

Related: [[project_ai_talk_jiayi_launch_2026-08-03]]
