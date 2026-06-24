---
name: feedback-model-choice-quality-first
description: 教練親定模型選擇鐵律——「複審念頭=訊號=該直接用 Opus」，禁止 Haiku 開工+Opus 複審（雙重消費假省真貴）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74751326-4082-44ca-8fa5-4a18e20c30a3
---

教練 2026-05-29 親定模型選擇鐵律：**品質優先，禁止混用 Haiku/Opus 開工**

**Why:** 2026-05-29 教練用 Haiku 4.5 做品管想省 token，跑完心裡不放心又叫 Opus 複審——當場發現 Haiku 品管不及格（軍師 Opus 隨機抽 3 條 2 條判錯）。軍師估算成本：
- 混用（Haiku 開頭+Opus 複審）：~$2.62
- 純 Opus 一次到位：~$2.85
- **只省 $0.23**，但 Opus 還要花心力修 Haiku 沒做好的部分（這場 Haiku 品管 50% 抽中率錯誤），實際 ROI 為負。

教練聽完軍師分析後親口拍板：「品質優先，那我們就開始新的對話框吧」。

**How to apply:**

| 情境 | 應該用 | 理由 |
|------|--------|------|
| 心裡冒出「Haiku 做的我得再看一眼」 | **直接 Opus 開工** | 複審念頭=訊號=該直接用最強模型 |
| 任務需要判斷力（品管、複審、策略、抓細節） | **純 Opus** | Sonnet/Haiku 容易過度信任「自評」，會放水 |
| 任務純執行（讀檔、grep、commit、固定流程） | **純 Haiku** | Haiku token 是 Opus 的 1/15，純執行勝任 |
| ❌ Haiku 開頭 + Opus 複審 | **永遠不要** | 雙重消費（兩次都付 token）+ Opus 還要修補 |

**核心鐵律（教練同意的軍師金句）：**
> 「**複審是訊號——說明你不該用低階模型做這件事。**」

**反例（已驗證為錯）：**
- 2026-05-29 早上：Haiku 做守則故事庫品管 → 報告「全綠燈」→ Opus 複審 → 抓出 #03/#14 兩條誤標 → 必須重派 MiniMax 重判

相關記憶：[[feedback-model-split-strategy]]、[[feedback-token-model-distinction]]
