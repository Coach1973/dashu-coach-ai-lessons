---
name: feedback-model-tier-advisor-opus-vs-sonnet-2026-09-25
description: 教練親定模型分工默契：重大決策/找根因/設計機制用Opus，庶務用Sonnet；Sonnet碰到Opus級任務要先一句話提醒切換、先不動手，Opus碰到庶務做完提醒可切回；已由UserPromptSubmit hook自動評估
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7dfd3491-32da-49ec-be24-a2c0d54e850c
  modified: 2026-09-24T20:22:02.141Z
---

教練：「重大決策時我會請 Opus 出來，平常一般的庶務類雜事我還是讓 Sonnet 解決……如果你覺得需要調動 Opus 出來，就主動提醒我……如果是 Sonnet 就能解決的，就不用提醒我。該用 Opus 就用，該省就省。」

**Why:** 教練流量有限（週三13:00重算，到週五04:13已用50%），但他認為 Opus 值得——2026-09-25 同一個赫米斯問題，Sonnet 5 繞了約1小時（推給系統、叫教練自己關、搞出副螢幕），切 Opus 5.5 後約30分鐘找到真因並補上防呆機制。教練原話：「Sonnet 那邊想半天、花了很長時間，卻沒有解決問題的根源；Opus 5.5 思考的時間更短，但非常有效率，而且直擊痛點。」

**How to apply:**
- 規則全文：`knowledges/模型分工規則_Opus與Sonnet.md`（Opus級六條：找根因／多系統／不可逆／設計機制／教練不滿／重要對外）
- **v2（同日教練追問「我不知道你的提醒什麼時候才會出現」）：每則≥15字的交辦，不管哪個模型，回覆第一行都標「🟢 這件 Sonnet 就能做」或「🟣 這件是 Opus 等級（理由）」**——看得見、可預期，比只在不對盤時才出聲好
- 注入端 `scripts/model_tier_advisor.sh`（UserPromptSubmit，看對話紀錄 model 欄位＋最後一次 /model）；檢查端 `stop_rules_master.py` A3，沒標示就擋
- 在 Sonnet 標🟣：一句建議切 Opus，先不動手；教練回「直接做」就照做
- 在 Sonnet 卡關（兩種方法都沒解決／教練說還是不行）：停下說「我卡關了，建議切換到 Opus 5.5 接手」
- 在 Opus 標🟢：照常做完，第一行提醒下一件可切回 Sonnet
- 相關：[[feedback_junshi_threshold_sonnet5_and_above_2026-09-24]]、[[feedback_model_choice_quality_first]]
