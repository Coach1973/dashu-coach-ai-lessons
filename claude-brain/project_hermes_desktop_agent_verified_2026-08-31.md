---
name: project_hermes_desktop_agent_verified_2026-08-31
description: Hermes是教練Mac上真實存在且在跑的獨立桌面AI代理(Nous Research出品，非Claude)，workspace跟軍師共用同一份大腦檔案，可作為Claude額度不足時的備援執行者
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-31T06:11:08.857Z
  originSessionId: 3253f534-e643-448c-a692-d2b09e411371
---

教練2026-08-31要求查證「Hermes是不是真的在Mac上」，用`ps aux`+`osascript`+讀取安裝目錄查證屬實，非教練誇大或誤會：

**Hermes是什麼**：`com.nousresearch.hermes`，Nous Research出品的獨立桌面AI代理App，版本0.15.1，安裝於`/Users/bymyway/.hermes/`，2026-04-22建立（SOUL.md/CURRENT_TASK.md皆為此日期）。有自己的gateway process（`hermes_cli.main gateway run`，長駐從週六18:50就在跑）、menubar狀態列程式、CLI dashboard(127.0.0.1:9120)、cron、skills、sessions等完整獨立架構，**不是Claude Code也不是OpenClaw，是第三套完全獨立的AI agent框架**。

**關鍵事實一：Hermes預設模型是MiniMax，不吃Claude額度**——`~/.hermes/config.yaml`的`model.provider: minimax`。這代表教練擔心「Claude流量用完」時，Hermes本來就不受這個瓶頸限制，是真正意義上的備援（前提是MiniMax那邊的量還夠，見[[feedback_token_model_distinction]]「不限流量只屬於小龍蝦/MiniMax」）。

**關鍵事實二：Hermes的workspace跟軍師(Claude Code終端機/桌面版)共用同一份大腦**——`~/.hermes/workspace/`底下`CLAUDE.md`/`HEARTBEAT.md`/`JUNSHI_HANDOFF_LATEST.md`/`MEMORY.md`/`SOUL.md`/`USER.md`/`memory/`/`distill/`/`執行細則.md`/`特助心法.md`/`路徑大全.md`全部是symlink指向`/Users/bymyway/.openclaw/workspace/`底下的同名檔案。代表**寫進`~/.openclaw/workspace/`的任何交接文件（例如給Hermes的SOP指令），Hermes原生就讀得到，不需要額外搬運或轉貼**——`knowledges/2026-08-31_大樹小講四場活動維運SOP_備援指令給Hermes.md`就是放在這個共用路徑下。

**Hermes自己的角色定位**（`~/.hermes/SOUL.md`，2026-05-16建立）：「大樹教練的重型任務代理＋認知骨幹」，定位是「當OpenClaw Bot團隊各自服務不同人類時，Hermes維持對教練全局視角的理解，負責跑Bot做不到的複雜任務」，且明確寫「與終端機（Claude Code CLI）協作，各司其職」——這個分工關係在2026-05-16就已經定義好，不是本次臨時安排。

**Hermes有自己獨立的接力棒/試金石**：`H_HANDOFF_LATEST.md`/`H_試金石.md`/`H_HOOKS_PLAN.md`（H_開頭，非symlink，是Hermes專屬檔案），跟軍師的`JUNSHI_HANDOFF_LATEST.md`分開維護，查Hermes上次做到哪要讀這幾份。

**CURRENT_TASK.md內容已過期**（停在2026-04-22的VPS TTS對接任務），不代表Hermes現在在做這件事，只是「每次重啟必讀」的檔案還沒被後續任務覆蓋，查Hermes近況應優先看`H_HANDOFF_LATEST.md`。

**Why**：教練想把Claude額度不夠時的工作無縫轉給Hermes，這不是空想——Hermes是真實運作中的獨立agent，且技術上完全具備接手條件（同一份workspace大腦+不吃Claude額度）。

**How to apply**：往後教練提到「Hermes」，直接當成一個真實存在、隨時可能被開啟的協作者看待，不用每次重新查證存在與否。交辦Hermes的任務/SOP文件，寫進`~/.openclaw/workspace/`底下任何路徑即可（Hermes workspace會透過symlink自動讀到），不需要額外複製一份到`~/.hermes/workspace/`。若要查Hermes上一次做了什麼，讀`~/.hermes/workspace/H_HANDOFF_LATEST.md`。

Related: [[feedback_token_model_distinction]]（不限流量只屬於小龍蝦/MiniMax，Claude助教不適用——Hermes吃的正是這個不限流量的池子）
