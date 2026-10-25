---
name: project-peipei-poster-only-tra-research-to-junshi-2026-10-26
description: 教練10/26定：巴哈(peipei)只出中華新媒體橫＋直版海報；台鐵標案研究由軍師統籌；巴哈上網／瀏覽器／小幫手已用程式禁用，台鐵訊息追加到 state/tra_research_inbox.md
metadata:
  type: project
---

**教練原話（10/26 00:52 台灣時間）**：「跟台鐵研究案有關的東西接手回來，由你這邊統籌。小龍蝦現在這個階段，讓他單純跑單一任務就好，就是出中華新媒體的直式跟橫式圖片。」另：「佩佩老師處理不了的，你這邊都來處理，處理完再把圖片推回去」。

**怎麼落地**：openclaw.json `agents.entries.peipei.tools.toolsBySender` 三種身分都 deny `group:web`、`browser`、`sessions_spawn`、`subagents`（da22958c9）；巴哈 AGENTS.md 最上方加最優先指令（備份 state/peipei_AGENTS_20261026_poster_only.md）；台鐵訊息→巴哈追加到 `state/tra_research_inbox.md` 並回「軍師統籌」，已實測成功。

**Why:** 10/25 台鐵研究讓巴哈派小幫手燒到 898 步／1.29 億 token，連帶限流冷卻→罷工（見 [[feedback-bot-instructions-must-block-old-path-and-measure-tokens-2026-10-25]]、[[feedback-lk888-hourly-cap-raised-and-minimax-quota-burner-2026-10-25]]）。

**How to apply:** 開工先讀 tra_research_inbox.md；做完用巴哈 bot token（channels.telegram.accounts.bot_peipei）推回群組 -5115910257；要重新開放研究工具要教練明說。講「額度」必附時間點與現況（案例134 ef69f9fc4）。圖文報告：event.bymyway.com/curated/tra-taitung/。
