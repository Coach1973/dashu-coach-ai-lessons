---
name: feedback-always-name-the-group-bot-site-in-full
description: 回報裡提到群組、機器人、網站，一律寫完整名稱；寫「那個群組」讓教練猜會被罵（2026-10-18）
metadata:
  type: feedback
---

回報時寫「電報那個有多個機器人的群組」，教練回：「下次明確說哪個群組？讓我猜嗎？訓練我的記憶力？還是叫我去做事？」

**Why:** 教練管很多群組（活動報名即時通知、佩佩老師的巴哈助理、榮樹下談公益…），代稱逼他自己猜，等於把查證工作丟回給他（守則 #12 精神）。我當時還講錯：以為是同一群組兩個機器人都回，實際是佩君老師把同一句貼進「活動報名即時通知」與「佩佩老師的巴哈助理」兩個不同群組。

**How to apply:**
- 提到群組寫全名；提到機器人寫「主機器人」「巴哈助理」這類教練叫得出的名字；提到網站寫網址或網站名。
- 查群組名：各分身資料庫 `~/.openclaw/agents/<agent>/agent/openclaw-agent.sqlite` 的 `session_windows.display_name`（例如 `telegram:g-活動報名即時通知`）。
- 同類錯第二次出現就做成 reply 時機的反射（N8），不再加記憶。與 [[feedback-chat-written-prompts-may-be-detour-ask-coach-first]] 同日。
