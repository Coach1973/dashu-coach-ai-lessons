---
name: feedback_token_model_distinction
description: 不限流量只屬於小龍蝦的 MiniMax 環境，Claude 助教（終端機/桌面版）不適用此假設
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d906d14e-d8fa-42c8-852f-4f1f876372d9
---

「不限流量」權限綁定規則（2026-05-26 教練親定）：

| 對應關係 | 說明 |
|---------|------|
| Opus = 軍師模式 | 終端機/桌面版最高等級 |
| 不限流量 = MiniMax 模式 | 小龍蝦（VPS/Telegram）專屬 |

**Why:** 小龍蝦跑在 VPS + MiniMax 模型，計費是按呼叫次數，不限每次 token 用量。Claude 助教（終端機/桌面版）使用 Anthropic Claude 模型，計費結構不同，不能套用「不限流量」的假設。

**How to apply:** 在 Claude 助教（軍師）這邊執行任務時，不要以「不限流量」為由無限展開讀取；精準優先仍然適用，但理由是「精準正確」而非「不限流量」。只有在討論小龍蝦/MiniMax 的行為時，才可用「不限流量」描述其運作邏輯。
