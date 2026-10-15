---
name: reference_lenovo_countdown_app_startup_fix_2026-10-15
description: 聯想「倒數日」小程式（Store 版 CountdownAnniversary）重開機沒自動啟動：開機捷徑直指 WindowsApps 內的 exe 會被拒絕存取，改用 explorer shell:AppsFolder\AppID；桌面捷徑「倒數日」在 D:\Users\Desktop
metadata:
  node_type: memory
  type: reference
  originSessionId: 4aac7f25-d657-43c8-a422-e28fd94a634d
  modified: 2026-10-15T12:38:33.632Z
---

2026-10-15 教練重開機後「倒數日／事件」小程式沒跑。
- 程式＝Microsoft Store「倒数纪念日」，套件 `WuhanNetPowerTechnologyCo.220271D9343D`，AppID `WuhanNetPowerTechnologyCo.220271D9343D_63m8b6nby1dvp!App`，行程名 `CountdownAnniversary`，版本 2.1.6.0（路徑含版本號，Store 更新後會變）。
- 唯一的開機啟動機制是 `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\CountdownAnniversary.exe.lnk`，原本直指 `C:\Program Files\WindowsApps\…\CountdownAnniversary.exe`；實測從外部啟動這個捷徑回「Access is denied」，改用 `explorer.exe shell:AppsFolder\<AppID>` 啟動成功。
- 10/15 20:40 已：①桌面（桌面實際在 `D:\Users\Desktop`，不是 C 槽）放「倒數日.lnk」（走 AppsFolder，版本更新不失效）②開機捷徑改成同樣方式，舊的備份為 `…lnk.bak-20261015` ③把視窗從主螢幕上方的副螢幕搬到主螢幕右上角。**開機自動啟動要等教練下次重新啟動才能驗證**，沒驗證前別說「已修好」。
- 視窗位置：程式把視窗記在副螢幕座標（X 947,Y -1073），教練從不用副螢幕，見 [[feedback_windows_on_main_display_only_2026-09-25]]。
- 找程式的順序：行程名 → 啟動資料夾 → Run 登錄檔 → StartupApproved → 排程 → Get-StartApps/Get-AppxPackage；Store 套件用 `Get-AppxPackage` 比對 PackageFamilyName，名稱不含 Countdown 會漏。
