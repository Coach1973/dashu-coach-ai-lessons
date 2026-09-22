---
name: feedback-em-voice-correction-means-1m-context-window
description: 教練語音或轉寫出現的「em」=「1M」（1M context window 的「1」被誤寫成英文字母「e」），上下文在討論 context window / token 上限 / 模型大小時直接當 1M 解讀，不要猜成 EM mode / extended mode / enterprise mode
metadata:
  node_type: memory
  type: feedback
  originSessionId: 73705253-e392-56b7-9aa8-b9687aeec642
  modified: 2026-09-22T12:53:00.000Z
---

2026-09-22 教練用 Mac 桌面版跟軍師討論「這個對話框流量走 Claude 還是 MiniMax」時，多次出現「em」一詞。軍師看了直接聯想成「EM mode / Extended Mode / Enterprise Mode」之類的抽象縮寫，整個對話脈絡往錯的方向推（猜「EM mode」是某種 backend 模式）。

教練事後糾正：「em 它是『1234567』的『1』，所以是 1m，結果他寫成英文字母的『e』」——意思是教練原本想講的是 **「1M」（1M context window 的「1」 + 字母 M）**，但因為：
1. 「1」這個數字被某個轉寫機制（語音轉文字／輸入法／OCR）當成英文字母「e」
2. 連在一起的結果就是「em」這個沒有意義的字串

對軍師來說，看到「em」自然會去找某個縮寫（EM mode、Enterprise Mode、Extended Memory...），但其實教練的意思從頭到尾就是 **「1M context window 模式」**——這個專案討論模型 / backend 路由時反覆出現的關鍵指標：
- v223 「B路徑1M通驗證」：教練設計的 B 路徑把 model 改成 `claude-sonnet-5[1m]` 走 MiniMax 透明代理，實測 1M context 真通
- v225 確認 MiniMax-M3 真有 1M context（API 回應 model 欄位驗證）
- settings.json 必開的 `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000`

## Why 這條很重要

這次教練講了「em」+「走 EM 模式」至少 3 次，軍師全部猜成抽象縮寫，沒想到去驗證上下文最直接的解讀（討論 backend 路由時，最常出現的指標就是 context window 大小）。如果當下主動問「您說的『em』是 1M 嗎？」，整個查證方向不會繞彎，也不會給出模糊答案。

守則 #18「語音糾偏必問不猜」明確列舉四種情況主動問：上下文接不上、詞不達意、詞彙陌生、邏輯反常。「em」這種**在討論 backend / 模型路由脈絡下出現、找不到任何已知縮寫能對應、又完全不像中文詞彙**的字串，符合「詞彙陌生 + 邏輯反常」雙重觸發條件，本來就該問。

## How to apply

1. 看到教練訊息出現「em / EM」一字串，**先看上下文是否在討論 context window / token 上限 / 模型大小 / 路由分流**，是的話直接當 **1M** 解讀
2. 如果上下文不清楚「em」指什麼（既不是 context window 話題、也沒有其他明顯對應），**主動問「請問您說的『em』是什麼意思？是 1M context window 嗎？」**，不要自己猜
3. 同類型陷阱：教練其他語音／轉寫字串如果看起來像英文縮寫但意義不明，主動確認，不要硬猜
4. 對應到 MEMORY.md 裡已有的 `feedback_fenhui_not_fenghui_voice_correction.md`（語音「鋒會」vs「鋒慧」），同樣是語音轉寫錯字 → 必須當下確認 → 不要憑印象選一個解釋

## 相關

- `feedback_fenhui_not_fenghui_voice_correction.md`（同類語音糾偏，但那是同音字，這次是數字被誤轉字母）
- `reference_minimax_mystery_resolved_model_name_routing_2026-09-19.md`（教練反覆關心的「這個對話框流量走哪」+ 1M 驗證是核心指標）
- 守則 #18 語音糾偏必問不猜
