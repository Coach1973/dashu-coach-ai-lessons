---
name: openclaw-gateway-hooks-not-per-machine
description: OpenClaw gateway hooks(如line-user-memory)只跑在Mac mini單一gateway，不像Claude Code settings.json hooks需要三機各自移植；別把兩種「hook」混為一談自動加註「Windows/ACER待處理」
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d4e7866e-b3e7-4d0e-a441-cc55c9c119e3
  modified: 2026-08-14T00:03:15.498Z
---

2026-08-14 v108接力棒把`hooks/line-user-memory`（OpenClaw湖道hook，修main/default頻道LINE個人記憶）誤標「三機同步：Windows/ACER待處理」。查`openclaw.json`確認三個LINE帳號（default/bni_tainan/jiaolian_thoughts）全部只在這台Mac mini單一gateway設定裡——[[project_team_structure]]早就記載學長/學弟/學妹三個LINE帳號都在同一台Mac mini，Windows/ACER（聯想/教練外出筆電）只是教練自己另外開Claude Code的工作機，並未各自跑一份OpenClaw LINE gateway，見[[reference_coach_machines_naming]]。

**Why：** 系統裡有兩種完全不同的「hook」，容易被同一個詞混淆：
1. **OpenClaw gateway hooks**（`hooks/*/handler.js`，如line-user-memory、namecard-inbound）——只在實際跑gateway的機器（目前僅Mac mini）有作用，git push就是唯一同步動作，不需要各機移植。
2. **Claude Code hooks**（`~/.claude/settings.json`的PostToolUse/UserPromptSubmit等）——這才是[[project_cross_machine_hook_sync_todo_2026-08-08]]講的「三機各自需要移植PowerShell版本並手動註冊settings.json」，因為每台機器的Claude Code特助/軍師是各自獨立運行、設定檔不隨git同步。

**How to apply：** 修完任何hook要標記「待三機同步」之前，先問這支hook屬於上面哪一種——是gateway hook（服務LINE/Telegram用戶）就只需git push，不用另外加Windows/ACER待辦；是Claude Code的settings.json hook才需要真的排三機同步待辦。
