---
name: feedback-model-tier-advisor-opus-vs-sonnet-2026-09-25
description: 【v3三燈號，2026-10-09】每則交辦回覆第一行亮燈🔵Haiku(已有SOP的固定動作)/🟢Sonnet/🟣Opus；模型不夠先建議切換不動手、卡關往上切、高模型做低級任務做完提醒切下；「目前模型」以系統提示為準(hook剛/model切換會看到舊的)；注入+Stop hook雙機制
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7dfd3491-32da-49ec-be24-a2c0d54e850c
  modified: 2026-10-09T04:24:38.330Z
---

教練：「重大決策時我會請 Opus 出來，平常一般的庶務類雜事我還是讓 Sonnet 解決……如果你覺得需要調動 Opus 出來，就主動提醒我……如果是 Sonnet 就能解決的，就不用提醒我。該用 Opus 就用，該省就省。」

**Why:** 教練流量有限（週三13:00重算，到週五04:13已用50%），但他認為 Opus 值得——2026-09-25 同一個赫米斯問題，Sonnet 5 繞了約1小時（推給系統、叫教練自己關、搞出副螢幕），切 Opus 5.5 後約30分鐘找到真因並補上防呆機制。教練原話：「Sonnet 那邊想半天、花了很長時間，卻沒有解決問題的根源；Opus 5.5 思考的時間更短，但非常有效率，而且直擊痛點。」

**How to apply:**
- 🔵 **v3（2026-10-09 教練親定，取代下面 v2 的兩燈號）**：多一個藍燈 🔵＝Haiku 就能做，範圍是「已寫成 SOP 的常態動作」——更新戰報／戰情儀表板、簡報套版、策展 SOP 與大樹作品上架、新增籌備會／例會名單、控制電腦查行事曆、開發票。前提是照 SOP 走得通，SOP 出錯升 🟢、要找原因或多系統升 🟣。完整對照表（目前模型×任務等級要做什麼）在規則檔。
- **「目前模型」以系統提示為準**：2026-10-09 查證，教練送出前剛用 /model 切換時，切換紀錄寫進對話檔比 hook 晚，hook 會看到上一個模型；hook 輸入欄位存 `state/model_tier_advisor_last_input.json`，目前只有 prompt／transcript_path 等，沒有 model。
- 規則全文：`knowledges/模型分工規則_Opus與Sonnet.md`（Opus級六條：找根因／多系統／不可逆／設計機制／教練不滿／重要對外）
- **v2（同日教練追問「我不知道你的提醒什麼時候才會出現」）：每則≥15字的交辦，不管哪個模型，回覆第一行都標「🟢 這件 Sonnet 就能做」或「🟣 這件是 Opus 等級（理由）」**——看得見、可預期，比只在不對盤時才出聲好
- 注入端 `scripts/model_tier_advisor.sh`（UserPromptSubmit，看對話紀錄 model 欄位＋最後一次 /model）；檢查端 `stop_rules_master.py` A3，沒標示就擋
- 在 Sonnet 標🟣：一句建議切 Opus，先不動手；教練回「直接做」就照做
- 在 Sonnet 卡關（兩種方法都沒解決／教練說還是不行）：停下說「我卡關了，建議切換到 Opus 5.5 接手」
- 在 Opus 標🟢：照常做完，第一行提醒下一件可切回 Sonnet
- **手機版切不到 Opus（教練2026-09-26親口）**：在手機碰到🟣事件，只做止血（叫停、安撫、不替教練做決定），根因與機制的結論先標「待電腦版Opus查證」，不要寫成定論——9/26 LK888事故手機版Sonnet先回信下了兩個錯結論（「軍師端擋不了」「60秒鎖可信」），教練回電腦後由Opus查原始紀錄更正（案例85）
- 相關：[[feedback_junshi_threshold_sonnet5_and_above_2026-09-24]]、[[feedback_model_choice_quality_first]]
