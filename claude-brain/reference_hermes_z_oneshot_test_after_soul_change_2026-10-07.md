---
name: reference-hermes-z-oneshot-test-after-soul-change
description: 改了桌面版 Hermes 的 ~/.hermes/SOUL.md 後，用 hermes -z 一次性提問開新對話實測；已開著的舊對話沿用舊規則
metadata:
  type: reference
---

桌面版 Hermes（Hermes.app）每次對話都把 `~/.hermes/SOUL.md` 全文放進系統提示（state.db 的 system_prompts 查得到）。**改規則的源頭就是這個檔**，不在 workspace git 裡，改前自己備份（`SOUL.md.bak.日期_說明`）。

**實測法（10/07 用過，成功）**：`/Users/bymyway/.local/bin/hermes -z "<教練會說的那句話>，只回答…不要執行任何動作"`——這會開一個全新對話，用最新的 SOUL.md 回答；Mac 沒有 `timeout` 指令，不要加。已經開著的舊對話不會重讀，所以要請教練開新對話。

**Why**：10/06 教練叫 Hermes「大樹作品上架 SOP」它說對不上（SOUL.md 沒有口令對照）；修完用這招實測才算交付（N4）。同一類錯（SOP 沒寫口語別名）9/24、10/06 已兩次，見 [[feedback_sop_must_alias_spoken_trigger_phrase_2026-09-24]]、試金石案例108。

**How to apply**：教練抱怨某個 AI「不懂我說的話」→ 先找該 AI 的注入檔（Hermes＝SOUL.md；小龍蝦＝專案卡 projects/cards/*.md、reflex 外掛）補口令對照，再用實際對話實測，不要只改檔就報完成。
