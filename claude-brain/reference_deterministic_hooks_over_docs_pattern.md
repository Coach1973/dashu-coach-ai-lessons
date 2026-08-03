---
name: reference-deterministic-hooks-over-docs-pattern
description: 教練要求「規則要保持新鮮/自動觸發」時的標準做法——寫成腳本(自動同步或UserPromptSubmit關鍵字hook)驗證後才算數，不能只靠文件宣告或模型記憶，2026-08-03新增「總結」收工暗號時確立
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7c99dd26-4c2c-4250-8fef-c87f9d9487a8
  modified: 2026-08-03T06:11:18.696Z
---

這個系統裡凡是「規則該怎麼被落實」的問題，答案一律是**寫成腳本、pipe-test驗證、再接進 `~/.claude/settings.json` 的 hook**，不是把規則寫進文件就算數。兩個已驗證的具體範式：

**範式一：來源文件自動鏡像（mtime-marker sync script）**
用途：某份「正式版」文件（如 `執行細則.md`、`特助心法.md`）內容要即時反映到另一份給 AI 讀取的檔案（如 `~/.claude/CLAUDE.md`），避免手動複製貼上後兩邊慢慢飄移。
做法：`scripts/sync_zhixingxize_to_claude_global.sh` / `scripts/sync_xinfa_to_claude_global.sh` 是範本——比對來源檔 mtime 跟上次同步時間，用 marker 標記包住目標區段，每次跑只在來源真的變動時才重寫。掛進 openclaw cron 每 30 分鐘跑一次，不靠人記得手動跑。

**範式二：關鍵字觸發 hook（UserPromptSubmit keyword detection）**
用途：教練說「從今以後我說 X，就代表要做 Y」這種指令。
做法：比照既有的「開工」機制（`scripts/feed_junshi_handoff.sh`，偵測開工類關鍵字、session 開始時注入六步驟內容）做對稱設計。2026-08-03 新增「總結」收工暗號（`scripts/summary_upload_trigger.sh`）就是同一個範式的第二個實例：偵測「總結」類短語 pattern（用錨定寫法避免長句子順口提到關鍵字被誤觸發）、命中就注入一段提醒文字，讓 Claude 讀到後執行對應步驟。

**共通驗證標準（缺一不算完成）：**
1. Pipe-test：合成真實情境的 stdin JSON，直接餵給腳本，確認觸發/不觸發都符合預期（尤其要測「不該觸發的長句子」，避免關鍵字誤觸發）
2. JSON schema 驗證：`jq -e` 確認 hook 正確掛進 settings.json 對應區段
3. 寫進正式規則文件（`執行細則.md` 新增對應 E 編號），讓這個機制有文字說明可查，不是只有一支沒人知道存在的腳本

**Why：** 教練多次強調「不想當監工」「都是很基本的問題卻要人工發現」——文件宣告的規則會被新 session 忽略或飄移，只有寫成 hook 才能保證每次都真的觸發，不靠模型記不記得。

**How to apply：** 下次教練提出任何「以後聽到 X 就要 Y」或「這個規則要保持最新」的需求，先問「有沒有既有的對稱範式可以抄」，不要重新發明；用 Skill(`update-config`) 取得 hook 正確配置格式後照著上面兩個範式做，做完才算數。

相關：[[project_claude_md_health_check_2026-07-31]]
