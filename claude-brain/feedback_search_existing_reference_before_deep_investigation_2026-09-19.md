---
name: feedback-search-existing-reference-before-deep-investigation-2026-09-19
description: "手機Remote Control重啟卡死問題，v220+v221兩場session花數小時重新排查，最後才發現09-17首次設定時reference_claude_code_remote_control_setup_sop_2026-09-17.md早就完整記錄同一根因跟解法"
metadata:
  type: feedback
---

# 深入技術排查前先grep claude-brain全文搜關鍵字，不能只靠記憶判斷「查過了」

v220、v221兩場session（跨兩個對話框，累積數小時）反覆排查「手機`claude rc`重啟卡死」，
v220排除10處設定來源仍查不到根因；v221才真正查明根因是`~/.claude/settings.json`的
全域`env`區塊（MiniMax路由）污染每個claude呼叫。**修好之後才發現**：
`claude-brain/reference_claude_code_remote_control_setup_sop_2026-09-17.md`——這是
2026-09-17第一次設定`claude rc`時寫的SOP，裡面**逐字記錄了完全同一個根因**
（settings.json的env區塊、四道卡關的第三關）跟**完全同一個解法**（暫時移除env區塊、
process啟動後跟檔案是否存在無關可以放心還原），連「收工後設定檔復原」章節都寫了
「env var不是process啟動後還會被檔案變動即時覆寫的東西」——這正是v221花大把時間
親自實測才驗證出來的同一個結論。

## Why 這條反覆發作值得記

- E07/守則#07「不要在同一個地方跌倒兩次」在這裡的落地方式，不該只靠「記得住自己以前
  查過什麼」，因為隔了兩個對話框、跨了兩場session，沒有人天生記得住上一場對話裡
  查過的細節——**必須靠機械式動作（grep claude-brain全文）補足記憶力的落差**，
  不能只憑印象覺得「這個問題應該是第一次遇到」就直接動手深入排查。
- 這次問題本身有明顯的關鍵字可以搜（`claude rc`、`remote control`、`ANTHROPIC_BASE_URL`），
  但v220/v221都沒有先做`grep -rl "remote.control\|claude rc" claude-brain/`這個最基本
  的動作，而是直接進入逐一排除設定來源的實測流程。

## How to apply

**任何技術類排查任務動手前，先做一次**：
```bash
grep -rli "<問題關鍵字1>\|<關鍵字2>" /Users/bymyway/.openclaw/workspace/claude-brain/
```
確認沒有既有reference檔案已經記錄過同一個問題，再決定要不要投入時間重新排查。
如果找到，直接讀完既有記錄再判斷「這次的症狀是不是同一個根因的重複發作」，
不要因為「這次的症狀敘述看起來不完全一樣」就跳過既有記錄直接重新查起
（本案例中v220的症狀描述跟09-17 SOP講的其實是同一件事，只是措辭不同）。

## 相關

- [[reference_remote_control_relaunch_blocked_mystery_2026-09-19]]（本次真正查明的根因+修復記錄）
- [[reference_claude_code_remote_control_setup_sop_2026-09-17]]（09-17首次設定時就已寫好的原始SOP，早就有答案）
- [[feedback_check_master_index_before_claiming_cant_find]]（同類型「查證前先查既有索引」教訓，這次是claude-brain技術參考檔的版本）
