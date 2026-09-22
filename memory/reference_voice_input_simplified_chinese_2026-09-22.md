---
name: reference_voice_input_simplified_chinese_2026-09-22
description: 教練用手機麥克風按鈕語音輸入會轉成簡體字，待測試如何直接出繁體
metadata:
  type: reference
---

教練 2026-09-22 23:23 親口回報：
> 「我確實是用手機版的麥克風按鈕，結果我說出來的話都變成簡體字。所以這個問題我到時候再測試看看，要怎麼樣才能讓我說出來的字直接變成繁體字。」

## 現象
手機麥克風按鈕 → 轉錄結果為**簡體中文**（圖片→图片，現在→现在，語音→语音 等典型對照）

## 待辦（教練未來處理）
- 測試不同語音輸入法/引擎能否直接出繁體
- 探索方向：
  1. 手機輸入法：Google 注音/小米輸入法/原生鍵盤，各切換語音辨識引擎看哪個會出繁體
  2. Telegram 語音訊息：bot_main 收到後用 whisper 轉繁體（whisper 支援 zh 參數，繁簡需後處理 s2tw）
  3. 各 APP 比較：找出哪個的語音輸入會直接出繁體中文

## 同場已完成
- ☕ 膠囊咖啡機產業服務鏈（20節點）`claude-brain/data/industry_chain_咖啡機膠囊.png`，Telegram 已推 chat_id=6124913915，教練親眼確認完成

Related: [[feedback_voice_correction_not_self_verified_handling_2026-09-19]]（同系列語音輸入教訓——凌晨 5:04 誤判 5:07 案例）