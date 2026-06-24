---
name: minimax-m3-api-parser
description: "MiniMax-M3 API 回應結構是 [{thinking}, {text}]，解析要遍歷找 type==\"text\"，不能讀 content[0]"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b701cc5f-5498-4a6e-b723-0cd90da952c9
---

呼叫 MiniMax-M3 的 Anthropic 相容端點時，`content` 陣列**至少有兩塊**：
1. `{"thinking": "...", "signature": "...", "type": "thinking"}` — 推理過程，**沒有 text 欄位**
2. `{"text": "...", "type": "text"}` — 真正的回應

**Why:** 2026-06-03 軍師建全自動蒸餾系統時踩雷——`distill_terminal_llm.py` 用 `content[0].get("text", "")` 拿到空字串（thinking 塊沒 text），結果蒸餾出 6 個 session 全部空白還誤以為成功。M2.7 沒這個現象，M3 才有。

**How to apply:** 任何呼叫 MiniMax-M3（或會吐 thinking 的模型）的 Python 腳本，解析時要遍歷找 `type=="text"`：

```python
# ❌ 錯（會拿到空字串）
result = data.get("content", [])
return result[0].get("text", "")

# ✅ 對
result = data.get("content", [])
if isinstance(result, list):
    for block in result:
        if block.get("type") == "text" and block.get("text"):
            return block["text"]
return None
```

**踩過的腳本：** `~/.openclaw/workspace/scripts/distill_terminal_llm.py`（已修，commit `1e703d8a`）

**Why M3 比 M2.7 多 thinking 塊：** M3 是「思考型」模型（類似 o1/Claude thinking），預設會吐推理過程。如果不想要 thinking，可在 payload 加 `"thinking": {"type": "disabled"}`，但目前保留 thinking 對蒸餾品質更好（讓模型先想再寫）。

相關記憶：[[project-auto-distill-mission]]
