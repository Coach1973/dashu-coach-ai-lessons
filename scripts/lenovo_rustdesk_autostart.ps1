# ⛔ 2026-10-19 作廢：請改用 scripts/lenovo_rustdesk_guard.ps1。
# 原因：本檔用 --tray 啟動，實測 --tray 只開托盤、不會開 21118（直連口）；且要管理員權限、從沒在聯想實跑。
# 真正根因是 RustDesk2.toml 的 stop-service='Y'（RustDesk 自己的『停止服務』動作寫入）。
# 聯想 Windows：登入時自動開 RustDesk，被關掉會自動再開（2026-10-18，起因：手機連不上聯想，RustDesk 沒在跑）
# 用法：在聯想上「開始→PowerShell→系統管理員身分執行」，執行本檔
$exe = "D:\Program Files\RustDesk\rustdesk.exe"
if (-not (Test-Path $exe)) { Write-Host "找不到 $exe"; exit 1 }
$name = "RustDesk-AutoStart"
$action   = New-ScheduledTaskAction -Execute $exe -Argument "--tray"
$trigger  = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
            -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit (New-TimeSpan -Seconds 0)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction SilentlyContinue
Register-ScheduledTask -TaskName $name -Action $action -Trigger $trigger -Settings $settings -Principal $principal | Out-Null
# 直連（用 IP 連、21118 口）要開著：先關掉舊的、補設定、再啟動
Get-Process rustdesk -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 2
$cfg = Join-Path $env:APPDATA "RustDesk\config\RustDesk2.toml"
if (Test-Path $cfg) {
  $t = Get-Content $cfg -Raw -Encoding UTF8
  if ($t -notmatch "direct-server") {
    if ($t -match "\[options\]") { $t = $t -replace "\[options\]", "[options]`r`ndirect-server = 'Y'" } else { $t += "`r`n[options]`r`ndirect-server = 'Y'`r`n" }
    Set-Content $cfg $t -Encoding UTF8
  } elseif ($t -notmatch "direct-server\s*=\s*'Y'") {
    $t = $t -replace "direct-server\s*=\s*'[^']*'", "direct-server = 'Y'"
    Set-Content $cfg $t -Encoding UTF8
  }
}
Start-Process $exe -ArgumentList "--tray"
Start-Sleep 8
$p = Get-Process rustdesk -ErrorAction SilentlyContinue
$l = Get-NetTCPConnection -LocalPort 21118 -State Listen -ErrorAction SilentlyContinue
if ($p -and $l) { Write-Host "OK：RustDesk 在執行、21118 口已開，之後登入會自動開" }
elseif ($p) { Write-Host "RustDesk 在跑但 21118 沒開：請到 RustDesk 設定→安全性→勾選「啟用直接 IP 存取」" ; exit 1 }
else { Write-Host "失敗：RustDesk 沒起來" ; exit 1 }
