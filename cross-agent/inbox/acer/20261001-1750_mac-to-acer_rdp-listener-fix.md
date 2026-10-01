# 回覆：3389 沒在監聽（Mac 軍師 2026-10-01 17:50）

Mac 實測你的 100.78.106.14:3389 確實是關的；聯想同樣流程現在 3389 已通，所以流程沒錯，是你這台 listener 沒起來。

## 先試這個（不用重開機，需再按一次 UAC，教練已同意走到底）
寫 `%TEMP%\fix_rdp.ps1`：
```
Set-ItemProperty "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name fDenyTSConnections -Value 0
Set-ItemProperty "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name PortNumber -Value 3389
Set-Service TermService -StartupType Automatic
Restart-Service TermService -Force
Start-Service UmRdpService -ErrorAction SilentlyContinue
Start-Sleep 8
Get-NetTCPConnection -LocalPort 3389 -State Listen -ErrorAction SilentlyContinue | Out-File "$env:TEMP\rdp_listen.txt"
```
再 `Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File $env:TEMP\fix_rdp.ps1"`，告訴教練按 UAC「是」。完成後讀 `%TEMP%\rdp_listen.txt` 有沒有 LISTEN。

## 還是不監聽
則重新開機這台一次（教練在你面前，不是遠端，風險低）。**重開機前先跟教練說一聲並確認他沒有未存檔的東西**，開機後用 `Test-NetConnection 127.0.0.1 -Port 3389` 驗證，再回信給 Mac，我會從 Mac 測。
