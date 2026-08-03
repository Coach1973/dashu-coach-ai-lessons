---
name: project-claude-md-health-check-2026-07-31
description: 教練看完CLAUDE.md規則過期文章後要求對照健檢，2026-07-31~08-03實測揪出並修好~/.claude/CLAUDE.md兩個真過期案例，逐條證據型健檢執行細則E01~E16並合併一組重複規則
metadata: 
  node_type: memory
  type: project
  originSessionId: 7c99dd26-4c2c-4250-8fef-c87f9d9487a8
  modified: 2026-08-03T06:11:25.041Z
---

教練分享一篇講「CLAUDE.md 規則只進不出、悄悄過期」的文章（Anthropic 自己砍掉系統提示詞 80% 舊規則的故事），要求對照 `~/.claude/CLAUDE.md` 做**實測**而非空談分析。

**Why：** 文章核心論點——規則寫了之後沒人回頭看，AI 每次都把可能過期的規則從頭啃一遍，會悄悄變笨；刪規則前要有證據，不是憑感覺。

**實測揪出的兩個真過期案例：**
1. 「特助心法」段落是手動貼上去的，沒有像 E01~E15 那樣的自動同步機制，已跟源頭 `特助心法.md` 出現格式/日期標籤飄移（跟 E10~E12 當年分岔一個半月是同一種病）——新增 [[reference_deterministic_hooks_over_docs_pattern]] 提到的 `scripts/sync_xinfa_to_claude_global.sh` 根治
2. Netlify 部署鐵律段落停在 2026-05-30 版本，沒收錄 2026-07-25 才發生的 `_headers` 萬用字元蓋掉圖片 Content-Type 教訓（案例54，教練當時要求全機通報）——已補上三條具體規則

**教練後續授權範圍擴大**：「你去評估哪些是必要的、有用的、可執行的，就留著；沒用的、過時的，就想辦法移到歷史備忘紀錄」——逐條查證執行細則 E01~E16 是否有專屬 skill 或 Stop/PreToolUse hook 撐著（不是憑印象猜），發現 **E02跟E10幾乎逐字重複**（都在講「教練說的話自動記錄不用想」），且兩者都沒有專屬 hook，判定為真過期，原文完整併入 E02，E10 編號保留空缺不重用。其餘 14 條（E01/03~09/11~16）逐一查證都有專屬 skill 或 hook 撐著，判定持續有積極作用，保留不動。

**How to apply：** 下次教練問「CLAUDE.md 是不是又累積很多過期規則」，可以直接引用這次的健檢方法論——查 skill/hook 是否存在當作「這條規則還有沒有積極作用」的證據，而不是靠主觀判斷。commit `0f54af6b2`（封存過時副本）、`0d1cc9755`（E10併入E02）。

相關：[[project_ai_go_xinfa_system]]（同場順手處理的另一件事）
