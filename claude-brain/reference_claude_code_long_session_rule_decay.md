---
name: claude-code-long-session-rule-decay
description: Claude Code(終端機/桌面版)長對話裡CLAUDE.md守則可能被context壓縮掉，跟VPS小龍蝦每次心跳重讀SOUL.md的架構落差，已補periodic重載hook
metadata: 
  node_type: memory
  type: reference
  originSessionId: 56947c71-51f1-4f4b-be4e-2ffdbfc779dc
  modified: 2026-08-07T22:53:46.532Z
---

# Claude Code長對話守則流失問題（2026-08-08教練當場質問後查證+修復）

教練質問：「如果不能讀守則，那我花費心思寫出來的守則意義是什麼？VPS版的小龍蝦都知道，為何claude卻不能讀完守則再做事？」

## 查證出的真根因

`~/.claude/CLAUDE.md`（含特助21守則全文）只在Claude Code session**開始那一刻載入一次**，之後隨著對話輪數增加，系統可能把最早的context壓縮/摘要掉（本場對話到第20輪時，系統自己的`session_length_hook.sh`才第一次提醒「該開新視窗」——這代表20輪前的原始context極可能已經被動過壓縮）。既有機制只提醒換視窗，完全沒有補回守則文字這個動作。

VPS版小龍蝦（OpenClaw agent）架構不同：每次心跳/每則訊息處理都重新讀取`SOUL.md`/`IDENTITY.md`，天生不會有「跑久了守則從context消失」這個問題，因為它根本不是靠一次性載入撐一整場長對話。

## Why
兩套系統的「守則是否持續在AI眼前」這件事，底層機制本來就不一樣，教練誤以為是能力落差，實際是架構落差——但這不代表可以拿架構當藉口，該補的補。

## How to apply
已新增`scripts/periodic_xinfa_reload_hook.sh`（UserPromptSubmit hook），複用`session_length_hook.sh`同一套「20輪起、每10輪一個band」節流設計，每個新band第一次觸發時把`特助心法.md`21條守則完整原文重新貼進context（不是連結、不是摘要）。已模擬20輪input測試通過、commit `6ae54fd6c`。

**誠實的殘留限制**：這解決的是「守則文字有沒有確實還在context裡」這個可驗證的前提，**不解決**「AI有沒有真的照著文字去做判斷」——後者仍然是行為層面的事，跟[[feedback_html_preview_chrome_only]]、[[feedback_screenshot_rules_consolidated]]這類「把具體行為轉成outcome-verification hook」的做法是互補而非取代關係：文字重載確保素材還在，outcome hook確保具體行為對了，兩層都要有。

Related: [[feedback_html_preview_chrome_only]]、[[feedback_screenshot_rules_consolidated]]
