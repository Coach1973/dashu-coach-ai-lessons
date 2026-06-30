---
name: junshi-token-economy-outsource
description: 軍師流量稀缺，耗 token 的執行動作寫成腳本丟給終端機（MiniMax M3 無限流量）執行
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3a789871-76e2-40e0-a248-c93ee820ec05
---

# 軍師流量分配鐵律（2026-06-30 19:00 教練親口）

**規則**：軍師（Opus）每 5 小時限流——本場聊不到幾段就用了 50%。**深層思考+判斷**才是軍師價值，**耗 token 的執行動作要外包給終端機（MiniMax M3 無限流量）**。

**Why（教練原話）：**
> 「我們這個高級的模型非常消耗流量，我們每 5 個小時都有資訊限流⋯⋯你最佳的價值在於深層次的思考與判斷。至於那些很耗 Token 的執行工作，你完全可以寫一段程式碼，我會交給『終端機』處理。終端機裡面跑的是 MiniMax-M3 無限流量的方案，你儘可能把消耗流量的程式修復或具體執行動作，全部丟給它去執行⋯⋯這也是我強調過很多次的分工方式。」

本場血淚：
- 一輪不到幾段 → token 已用 303.9K（context 30%）+ 流量 50%
- 軍師反覆做 grep gateway.log / tail BOT_MESSAGES.md / launchctl list / find 等大檔操作
- 這些**全可以寫成 shell 腳本**，外包給終端機跑，軍師只讀結果

**How to apply：**

| 動作類型 | 軍師做 | 外包終端機做 |
|---|---|---|
| 寫腳本/想根源/評估方案/設計 | ✅ 軍師核心價值 | ❌ |
| 跑診斷指令掃 log | ⚠️ 限 1 次小範圍探查 | ✅ 後續批次掃描寫腳本丟出去 |
| 多輪 grep / cat / find / tail 大檔 | ❌ 嚴禁反覆 | ✅ 統一寫成 diagnose.sh 跑一次 |
| 跑 cron 修改 / launchctl 操作 | ❌ | ✅ 寫成 fix.sh 外包 |
| 高密度推理（守則對照、案例分析、架構決策）| ✅ 唯一價值 | ❌ MiniMax 做不到深度 |

**分工模式範例：**
- ❌ 錯：軍師 5 次 grep gateway.log → 每次幾十 KB 進 context
- ✅ 對：軍師寫 `diagnose_peipei.sh`（一檔含 grep+awk+結論），輸出 200 字以內摘要 → 教練拿給終端機跑 → 軍師只看 200 字摘要決策

**外包格式：**
- 軍師交付：一段獨立 code block 的 bash/python 腳本（教練可一鍵複製）
- 結尾必輸出**簡短結論**（不超過 30 行），不要 raw log
- 教練貼進終端機 → MiniMax 跑 → 結果回報軍師 → 軍師做判斷

關聯：[[feedback_scarce_resource_workflow]]、[[feedback_opus_token_economy]]、[[feedback_model_split_strategy]]、[[feedback_junshi_role_decide_not_ask]]
