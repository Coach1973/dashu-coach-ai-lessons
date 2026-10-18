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
Start-Process $exe -ArgumentList "--tray"
Start-Sleep 5
if (Get-Process rustdesk -ErrorAction SilentlyContinue) { Write-Host "OK：RustDesk 已在執行，之後登入會自動開" } else { Write-Host "失敗：RustDesk 沒起來" ; exit 1 }
