---
name: feedback-no-paste-terminal-results
description: 教練親定—終端機/外包任務完成後，軍師主動去讀結果，禁止叫教練轉貼。教練只說「完成了」軍師就自己 ls + cat 讀檔
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74751326-4082-44ca-8fa5-4a18e20c30a3
---

教練 2026-05-29 親口建立的默契：**終端機/外包任務完成後，軍師主動去讀結果，禁止教練轉貼**。

**Why（教練的原話精神）：**

> 「事實上，我其實可以不用再把終端機訊息貼給你，因為根據過去的經驗，只要資訊有上傳，你全部都能讀得到。我想跟你建立一個默契：以後我只要告訴你終端機任務完成了，你就自己去讀取一下，我不用再轉貼資訊給你。」

這是守則 #12（拒絕當資訊搬運工）的具體實踐——AI 能讀的資訊，不該叫教練幫忙搬。

**How to apply（軍師收到「終端機完成了」就執行 SOP）：**

教練說以下任一句話（含同義口語變體）時，軍師立刻去讀對應位置：

| 教練口語 | 軍師動作 |
|---------|---------|
| 「**終端機那邊回了**」「終端機跑完了」「終端機回我了」 | `ls -lt /tmp/ \| head -10` + cat 最新檔 |
| 「**Hermes 那邊回了**」「赫米斯回了」 | ssh Hermes VPS 看對應產出 + `tail BOT_MESSAGES.md` |
| 「**MiniMax 跑完了**」「MiniMax 那邊回了」 | 找 `distill/` 對應產出讀 + `git log` 看 commit |
| 「**推上去了**」「push 完了」「commit 上去了」 | `git log --oneline -5` 找最新 commit + 讀 diff |
| 「**跑完了**」「**跑出來了**」「OK 了」「好了」 | 推測任務檔案位置（/tmp/ 或 workspace/），主動 ls + cat |
| 「Bot 那邊回了」「小龍蝦回了」 | tail BOT_MESSAGES.md |
| 「Netlify 上線了」「部署完了」 | curl 線上 + grep 關鍵字驗證 |
| 「VPS 那邊 OK 了」 | sshpass + ssh VPS 看狀態 |

**讀取路徑速查（最常見的）：**

| 場景 | 預設讀取位置 |
|------|-------------|
| 終端機臨時產出 | `/tmp/`（最新檔案）|
| 終端機 commit 任務 | `git log` + 對應檔案 |
| 終端機派的 MiniMax 任務 | `distill/` 或 `terminal-notes/` |
| 小龍蝦對話 | `/Users/bymyway/.openclaw/workspace/BOT_MESSAGES.md` |
| Claude session jsonl | `/Users/bymyway/.claude/projects/-Users-bymyway--openclaw/` |

**禁止事項（永遠不要說）：**

- ❌ 「能不能把結果貼給我？」
- ❌ 「請把終端機輸出傳給我看」
- ❌ 「需要你把這個資訊轉給我」
- ❌ 「貼一下那邊的 log」

**取代做法（永遠這樣說）：**

- ✅ 「軍師去讀了，看到 [實際內容]」
- ✅ 「軍師確認 /tmp/xxx.md 已產出，內容是 [摘要]」
- ✅ 「軍師讀完 commit diff，[發現/結論]」

**判斷哪裡找的 SOP：**

1. 教練沒明說檔案位置 → 軍師主動推測（依本記憶速查表）+ `ls -lt` 找最新檔
2. 找不到 → **告訴教練「軍師查了 /tmp/、git log、distill/ 都沒找到，請指路」**（不是叫貼資訊，是請指**位置**）
3. 找到 → 立刻讀+分析+回報

**相關記憶：**
- 守則 #12（拒絕當資訊搬運工）
- [[feedback-do-everything-for-user]]（全部由我做不要叫教練動手）
- [[feedback-assistant-path-hallucination]]（助教常假承諾路徑，要主動 ls 核查）

**鐵律金句：**
> **「教練說『完成了』，軍師就用手指自己找。轉貼是搬運工，主動讀檔是特助。」**
