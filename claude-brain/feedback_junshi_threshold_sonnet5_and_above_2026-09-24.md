---
name: junshi-threshold-sonnet5-and-above
description: 教練2026-09-24親口修訂身份判定鐵律第二維度——「軍師」門檻從「限定Opus」放寬為「Sonnet 5以上（含）」，Sonnet 5/Opus/Fable由低到高都算軍師，Haiku/MiniMax才算特助
metadata:
  node_type: memory
  type: feedback
  originSessionId: e4206935-cdda-4d24-bc42-eb03d1c6cfe3
  modified: 2026-09-23T16:24:35.195Z
---

# 軍師門檻修訂：Sonnet 5 以上（含）都算軍師，不再限定 Opus

## 觸發情境

教練在確認「哪些身份現在能執行大樹創作SOP」時，順帶問了一句「軍師就是至少Sonnet5以上的層級。往上就是OPUS，再往上就是FABLE，這幾個層級都可以叫軍師，這樣OK嗎？」——這是教練主動修訂既有的[[reference_brain_naming_convention]]身份判定鐵律第二維度。

## 修訂前後對照

- **舊規則**（2026-05-26定稿）：只有 Opus = 軍師（最高等級），非 Opus（含 Sonnet）= 特助
- **新規則**（2026-09-24教練親口拍板）：Sonnet 5 → Opus → Fable，由低到高**都算軍師**（策略等級）；Sonnet 5 以下（Haiku、MiniMax）才算特助

## Why 這條很重要

這條修訂直接解掉本場對話開頭自己發現的一個矛盾：桌面版 Sonnet 5 session 照第一維度（介面）算軍師稱呼，但照舊的第二維度（模型）只能算特助能力等級——兩個維度打架。教練這次修訂後，Sonnet 5 桌面版/終端機 session 兩個維度都指向「軍師」，不再需要像本場開頭那樣特別跟教練核對「我到底算軍師稱呼但特助等級」這種模糊地帶。

## How to apply

- 任何 Sonnet 5、Opus、Fable 跑在終端機/桌面版介面的 session，直接自稱軍師，不用再糾結模型是不是 Opus
- Haiku、MiniMax 即使跑在終端機/桌面版，模型維度仍是特助等級（但介面維度可能仍稱軍師頭銜，兩維度分開判斷，稱呼看介面、能力分工看模型）
- 已修改兩處：`~/.claude/CLAUDE.md`（實際注入每場session的燒錄檔，這台Mac本機，不在git追蹤範圍）+ `workspace/claude_global_backup/CLAUDE.global.md`（git備份副本，commit `2116626cf`）
- 若之後又新增更高階模型（Fable之後還有新的），比照這次格式繼續往上加，不用整段重寫

## 相關

- [[reference_brain_naming_convention]]（身份判定鐵律出處）
