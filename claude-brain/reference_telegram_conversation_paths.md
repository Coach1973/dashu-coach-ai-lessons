---
name: Telegram 對話紀錄固定路徑
description: 三機對話紀錄的固定存放位置，直接讀取不需搜尋
type: reference
originSessionId: 8fc287b4-68a6-415b-9454-1df736e9c1fc
---
## 1號機（教練與學長的對話）

**最重要、最常用的：**
```
/Users/bymyway/.openclaw/workspace/BOT_MESSAGES.md
```
- 包含教練與1號機的所有對話（私訊 + 群組）
- 群組 chatId：`-1003877502911`（三機+教練的頂級特助分工群）
- 讀最後 100–200 行即可看到最新對話：`tail -200 /Users/bymyway/.openclaw/workspace/BOT_MESSAGES.md`

**Session 詳細紀錄（含工具呼叫）：**
```
/Users/bymyway/.openclaw/agents/main/sessions/
```
- 最新 session = `ls -lt` 第一個 `.jsonl` 檔

## 2號機（孔大哥的對話）

```
/Users/bymyway/.openclaw-peipei/agents/main/sessions/sessions.json
/Users/bymyway/.openclaw-peipei/agents/main/sessions/  （各 .jsonl）
```

## 3號機（佩佩老師的對話）

```
/Users/bymyway/.openclaw-kong/agents/main/sessions/sessions.json
/Users/bymyway/.openclaw-kong/agents/main/sessions/  （各 .jsonl）
```

## 使用原則
- 找「最新對話內容」→ 直接 `tail` BOT_MESSAGES.md（1號機）
- 找「某個特定對話細節/工具呼叫」→ 進 sessions/ 找最新 .jsonl
- 2/3號機沒有獨立 BOT_MESSAGES.md，對話在 sessions/ 裡
