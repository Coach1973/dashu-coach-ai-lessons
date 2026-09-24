# Hook: UserPromptSubmit (Windows/聯想版)
# 用途：教練說「總結」時，自動注入「收工動作清單」，觸發總結+更新接力棒+commit+push。
# 對稱腳本：summary_upload_trigger.sh（Mac版，用jq解析stdin）。
# 起因：聯想這台機器沒有安裝jq(/usr/bin/jq不存在)，Mac版腳本在這裡會靜默失敗
#       （jq指令找不到→PROMPT變數變空字串→grep永遠比對不到→hook永遠不觸發，且不會報錯，
#       跟periodic_xinfa_reload_hook.ps1當初遇到的python3/jq環境限制是同一種坑）。
#       改用PowerShell原生ConvertFrom-Json解析，不依賴任何外部指令。
# 2026-08-26 教練親口糾正：發現「總結」在聯想這台機器上從未真正觸發過收工流程。

$ErrorActionPreference = 'SilentlyContinue'
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$rawInput = [Console]::In.ReadToEnd()
try {
    $json = $rawInput | ConvertFrom-Json
    $prompt = $json.prompt
} catch {
    exit 0
}

if ([string]::IsNullOrWhiteSpace($prompt)) { exit 0 }

$trimmed = $prompt.Trim()

# 觸發條件：整句主要是「總結」類指令才觸發，避免長句子裡順口提到「總結」誤觸發
# （例如「幫我寫一份年度總結報告」不該觸發收工流程），對稱Mac版.sh的判定邏輯
$isTrigger = $false
if ($trimmed -match '^總結[\s。！!，,]*$') { $isTrigger = $true }
elseif ($trimmed -match '^總結[，,]') { $isTrigger = $true }
elseif ($prompt -match '總結上傳') { $isTrigger = $true }
elseif ($prompt -match '總結一下') { $isTrigger = $true }

if (-not $isTrigger) { exit 0 }

@"
🔴 教練說「總結」＝收工暗號（比照「開工」對稱設計，2026-08-03教練親定）。
讀到這句話，立即依序執行以下步驟，不用再問「要不要」：

1. 【總結本場】守則#14——把這場對話濃縮成300~500字重點：做了什麼、卡在哪、下一步是什麼
2. 【更新接力棒】N9交接鐵律——把總結寫進 JUNSHI_HANDOFF_LATEST.md 開頭「現在真正待辦」表 + 新增一棒敘述
3. 【判斷是否寫記憶】N8記憶鐵律六種情況——本場若有教訓/發現符合清單任一條，寫進 memory/試金石
4. 【commit + push】N1鐵律——完成以上更新後，commit + push，附上 commit hash 給教練
5. 教練這句話同時代表他即將開新對話框——不用問「還有其他事嗎」，完成上述四步驟收尾即可回報
"@

exit 0
