---
name: rule-reminder
description: "每次收到教練訊息時偵測關鍵字，自動注入相關特助守則提醒，讓守則對照不靠模型記得、靠系統強制"
metadata: {"openclaw":{"emoji":"🌱","events":["message:preprocessed"]}}
---

# Rule Reminder Hook（守則自動對照）

軍師版（Claude Code）`pre_task_hook.sh` 的 OpenClaw 對應版本。教練每發一則訊息，
自動掃描關鍵字，命中高頻痛點就注入對應的特助守則提醒到 context。

## 觸發事件
`message:preprocessed` — 每次教練發言時觸發

## 對照邏輯
依據 `~/.openclaw/workspace/knowledges/01_knowledge_base/trigger_index.md` 的關鍵字對照表，
涵蓋守則 #01 #02 #04 #05 #08 #09 #12 #13 #16 #17。命中才注入，不命中靜默（不炸 token）。

## 注入格式
```
🌱 守則提醒（系統自動對照 trigger_index）：
• 守則#XX（...）：...行動指引...
```

## 偵測 log
`~/.openclaw/logs/rule-reminder-probe.log` — 記錄 event 結構與命中文字，供事後精準化訊息欄位。

## 設計原則
- 防禦性多路徑抽取訊息文字（OpenClaw 未明確暴露欄位，故嘗試 context.text / messages[] / context.message.text 等）
- 抓不到文字或未命中 → 靜默退出，不影響對話
