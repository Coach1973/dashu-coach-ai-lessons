---
name: existence-verification-voice-correction
description: Use whenever 教練 mentions an unfamiliar filename, term, or phrase — especially via voice input — or when context doesn't logically connect. Verify existence before acting; ask for confirmation on transcription anomalies rather than guessing.
---

# 存在性驗證 + 語音糾偏必問不猜（執行細則 N3）

對應守則 #03、#15、#18。

## 存在性驗證

聽到陌生檔名/術語/專案名：
1. 先搜尋驗證（grep、find、WebSearch）
2. 找不到就明說「找不到」，不假裝存在、不照字面瞎猜著執行

## 語音糾偏四情況（守則#18）

以下四種情況之一出現，主動問「您說的是『XXXX』嗎？」，確認後才執行：
1. **上下文接不上**——這句話跟前後文邏輯兜不起來
2. **詞不達意**——聽起來像在講別的事
3. **詞彙陌生**——過去對話從未出現過的字眼
4. **邏輯反常**——教練平常不會這樣講/這樣要求

## 常見語音變體對照（持續累積）

中文語音辨識常見諧音錯誤，聽到近似詞先對映再確認：
- 「特助心法」「頂級特助」等核心詞的語音變體
- 數字/日期矛盾（同段訊息出現兩個不一致數字，例如「四」↔「十」）必須用 AskUserQuestion 問清楚，不能自己選一個

## 鐵律

不確定就問，問完再做；絕不把「聽起來像」當「教練說過」處理。
