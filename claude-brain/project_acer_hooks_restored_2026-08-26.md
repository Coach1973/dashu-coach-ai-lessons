---
name: project-acer-hooks-restored-2026-08-26
description: ACER機49天未開機導致settings.json全部hooks遺失，本場重新安裝七支hook+跟進聯想總結上傳修復，過程中發現setup_windows_hooks.ps1在PowerShell 5.1會吃掉原有設定的bug
metadata:
  type: project
---

延續[[project_acer_dormant_49days_2026-08-26]]，教練要求ACER跟進聯想的「總結」收工hook修復。查證確認ACER的`~/.claude/settings.json`完全沒有`hooks`區塊（不只是總結hook缺，開工六步驟/截圖鎖/跨機信箱掃描全部沒註冊），推測跟這台機器沒被打開49天期間可能經歷過的還原/重裝事件有關，非單一腳本bug。

**已執行**：跑`scripts/setup_windows_hooks.ps1`（原本就是為聯想/ACER寫的通用一鍵安裝腳本），但**發現這支腳本在Windows PowerShell 5.1上有真的bug**：`ConvertFrom-Json -AsHashtable`這個參數是PowerShell 6+才有，5.1會拋例外，觸發腳本的catch分支，導致`$settings`被重置成空物件，寫回settings.json時把原本的`env`/`permissions`/`model`等既有設定全部蓋掉，只剩新寫入的`hooks`。這台機器`powershell`指令解析到的就是5.1（`$PSVersionTable.PSVersion`實測5.1.26100.9168），不是pwsh 7。

**Why**：這是「腳本假設環境版本，實際環境不符」的同一種坑（跟[[reference_lenovo_summary_hook_jq_missing_fixed_2026-08-26]]的jq依賴問題同屬一個模式），差別是這次不是靜默失敗，而是**靜默損毀既有設定**，風險更高——好在腳本本身有先備份一份(`settings.json.bak.{timestamp}`)，從備份救回原始`env`/`permissions`/`model`，手動合併寫回，沒有真的遺失資料。

**已完成**：
1. 手動合併settings.json：保留原有`env`(MiniMax API key等)/`permissions`/`model`/`includeCoAuthoredBy`/`skipDangerousModePermissionPrompt`，加回7支hook（PreToolUse: delete_guard_hook；Stop: session_end_auto_push；UserPromptSubmit: inject_taiwan_time/session_time_context/feed_junshi_handoff/scan_cross_agent_inbox/scan_cross_machine_commits）
2. 額外把聯想2026-08-26新寫的`summary_upload_trigger.ps1`（總結收工hook）也加進UserPromptSubmit——這是`setup_windows_hooks.ps1`本身沒有涵蓋的部分，因為那支hook比安裝腳本本身還新
3. 用假指令逐一實測：`summary_upload_trigger.ps1`四情境全過（"總結"/"總結上傳"觸發，"年度總結報告"/"今天天氣如何"不誤觸發）；其餘5支UserPromptSubmit hook做基本煙霧測試(exit 0無例外)

**How to apply**：
- `setup_windows_hooks.ps1`日後在任何機器上執行前，**先確認該機器`powershell`版本**（`$PSVersionTable.PSVersion`），5.1會觸發這個bug。理想修法是把腳本的`ConvertFrom-Json -AsHashtable`改成不依賴AsHashtable的相容寫法（例如手動用`[ordered]@{}`合併PSCustomObject屬性），這次因為教練只要求先跟進聯想的總結修復，腳本本身的bug只做了記錄沒有回頭改，下次有人要在別台機器跑這支installer前，記得先讀這篇
- 任何機器如果出現「hooks全部消失但git歷史看起來一切正常」，優先懷疑本機`settings.json`被非git事件（重裝/還原/手動誤操作）動過，不要只查git log，因為settings.json本來就不在git同步範圍
- 完整的7支hook清單+對應腳本路徑，見`scripts/setup_windows_hooks.ps1`本身的清單（第178~189行）

Related: [[project_acer_dormant_49days_2026-08-26]]、[[reference_lenovo_summary_hook_jq_missing_fixed_2026-08-26]]
