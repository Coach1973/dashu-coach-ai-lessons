---
name: reference-lenovo-summary-hook-jq-missing-fixed-2026-08-26
description: 聯想「總結」收工hook因缺jq指令靜默失效近一個月，2026-08-26改PowerShell版修復並註冊
metadata: 
  node_type: memory
  type: reference
  originSessionId: ed12b5f3-f2d9-405b-9e5f-f674db4b6e9d
  modified: 2026-08-25T16:47:04.961Z
---

教練習慣每次工作完說「總結」讓AI收工（總結本場+更新接力棒+判斷寫記憶+commit push），跟「開工」對稱設計，2026-08-03教練親定，腳本`summary_upload_trigger.sh`早就寫好。但聯想這台機器一直沒有真正生效——教練質疑「我每次都有講總結上傳，怎麼可能沒紀錄」，查證後發現這支.sh腳本靠`/usr/bin/jq`解析stdin JSON，**這台機器根本沒裝jq**，指令找不到導致PROMPT變數變空字串，grep永遠比對不到觸發詞，整支hook靜默不觸發（不報錯、UserPromptSubmit exit 0），教練完全看不出異狀。

**Why：** 跟`periodic_xinfa_reload_hook.ps1`當初遇到的python3/jq環境限制是同一種坑（這台python3只是Windows Store樁、jq完全沒裝），Mac寫的.sh腳本假設Unix工具鏈存在，直接搬到Windows會靜默失敗而非報錯，最難察覺。

**How to apply：** 已寫`scripts/summary_upload_trigger.ps1`（PowerShell原生`ConvertFrom-Json`解析，不依賴jq/python3），並已在`~/.claude/settings.json`的UserPromptSubmit註冊生效，7情境模擬測試全過（4觸發：純總結/總結上傳/總結一下/總結+逗號；3防呆：年度總結報告類長句不誤觸發/無關訊息/空字串）。**任何從Mac(.sh)搬到聯想的hook，動手前先查腳本依賴哪些指令（jq/python3/whisper等Unix慣例工具），聯想這台機器能確定沒有的至少有jq跟正常python3**，寫Windows版一律用PowerShell原生能力，不要假設Unix工具鏈存在。commit`30a49989`(scripts)。

同場也查出另一支「開工」對應機制`feed_junshi_handoff.sh`在聯想也未被hook直接觸發，但因CLAUDE.md靜態指令已完整涵蓋六步驟效果一致，暫不需額外處理，此為「總結」專屬的缺口修復。
