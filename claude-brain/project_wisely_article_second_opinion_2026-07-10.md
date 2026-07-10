---
name: project_wisely_article_second_opinion_2026-07-10
description: 教練要軍師(Sonnet 5)重跑小龍蝦(MiniMax-M3)已做過的文章分析當第二意見，抓到3個實質誤判並當場修好
metadata: 
  node_type: memory
  type: project
  originSessionId: e8f1ec4f-d181-48a7-92cd-2d066d484656
---

教練 2026-07-10 早上請軍師（桌面版 Sonnet 5）獨立重新分析同一篇文章
（wiselychen 的 OpenClaw 記憶架構剖析），對照小龍蝦（MiniMax-M3）已完成的初版，
明確說「不知道 MiniMax 深度思考能力怎麼樣」，要看差異。

**Why**：教練對非 Opus/Sonnet 模型做深度技術分析的可靠度有疑慮，這次是實測驗證。

**結果（有 commit 憑證，`e7db2cb43`→`3a6e885db`→`a2a7ce7d1`→`7d678b429`）**：
軍師親自抓文章原文 + 查 `openclaw.json`/`AGENTS.md`/實測檔案大小，抓到小龍蝦
3 個沒查證就下結論的錯：①memorySearch 向量搜尋其實已在跑，小龍蝦「我們不用RAG」
判斷錯；②熱啟動小龍蝦說「比文章聰明」但沒實測，軍師實測反而比文章講的上限還高；
③完全沒發現自訂 `feed_junshi_handoff.sh` Hook 無字數上限，把 memory 檔裡的
Dreaming 雜訊整包灌進對話（43KB），這是文章跟小龍蝦都沒抓到的自製新黑洞。

軍師執行修復後，過程中又發現自己第一輪查證也查錯了地方（查了軍師自己的
`.claude/projects/*.jsonl` 而非小龍蝦真正在跑的 `~/.openclaw/agents/main/sessions/*.trajectory.jsonl`），
修正後確認 memorySearch 確實有在用（8次呼叫）；另外 2 項建議動作（記憶檔警告cron、
cc-switch說明）查證後發現小龍蝦當天稍早已經做完，避免重工。

**How to apply**：
- 涉及「查證後才能下結論」的深度技術分析，值得用高階模型（軍師/Opus）做二輪驗證，
  非高階模型容易用印象打勾而非實測——這次是具體反例證據，可支撐 [[feedback_model_choice_quality_first]]
- 執行分析報告裡的「建議行動」前，一定要重新查證現況（cron 清單、SOUL.md 現有內容等），
  不能拿分析當下的結論直接動手——尤其小龍蝦跟軍師是併行工作，狀態隨時在變
- 完整技術細節見 `knowledges/2026-07-10_文章剖析_軍師版_對照小龍蝦初版.md`
