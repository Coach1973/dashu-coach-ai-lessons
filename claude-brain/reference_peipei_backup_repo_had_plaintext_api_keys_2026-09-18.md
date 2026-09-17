---
name: reference-peipei-backup-repo-plaintext-keys
description: peipei-ai-backup(private repo) git歷史裡曾有MiniMax共用金鑰+Google API金鑰明文，現況已清空但舊commit仍在
metadata:
  type: reference
---

清理peipei-ai-backup 10週積壓時發現：`agent/models.json`跟`agent/auth-profiles.json`過去的git commit裡含明文`sk-cp-...`(全系統共用的MiniMax金鑰，同一把[[reference_minimax_quota_5h_4500_calls]])+一組Google API Key(`AIzaSyDFLv...`)。

當下工作目錄裡這兩個檔案已經是空/被刪除狀態(不確定是誰、何時清空的，非本次操作)，2026-09-18已將現況commit(`d4034d4`)並把這兩個檔名加進`.gitignore`防止未來再度含明文金鑰入庫。

**未處理**：金鑰本體仍留在較舊的git commit歷史裡，只要有人執行`git log -p`翻到那幾個commit就看得到明文。repo已確認是private(`gh repo view`驗證`isPrivate:true`)，曝光範圍侷限在教練自己的GitHub帳號協作者，風險比照[[reference_terminal_notes_raw_sessions_no_gitignore_2026-09-14]]那次Telegram token洩漏的判斷邏輯(private+風險可接受，不主動輪替)。

**How to apply**：教練若想徹底清除歷史紀錄裡的金鑰，需要`git filter-repo`或BFG改寫歷史+強制推送，這是不可逆操作，要教練親口確認才能動手；若只是要防止未來再犯，現有`.gitignore`修法已經足夠。之後任何agent的獨立備份repo(kong-ai-backup同理)，清理積壓commit前都應該順手grep一次`models.json`/`auth-profiles.json`這類含embedded apiKey欄位的設定檔，這類檔案的結構性風險比一般文字檔案高。
