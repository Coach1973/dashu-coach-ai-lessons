# Hook: UserPromptSubmit (Windows PowerShell 版)
# 用途：每次教練說話，自動注入「當下台灣時間」+「永遠台灣時間鐵律」
# 教練 2026-06-09 親罵：UTC/Z 時間講了 N 次違反，從此寫死系統
# 對應 Mac 版: inject_taiwan_time.sh

$ErrorActionPreference = "SilentlyContinue"

try {
    $tz = [System.TimeZoneInfo]::FindSystemTimeZoneById('Taipei Standard Time')
    $twNow = [System.TimeZoneInfo]::ConvertTime((Get-Date), $tz)
} catch {
    $twNow = (Get-Date).ToUniversalTime().AddHours(8)
}

$dayNames = @('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
$dayEn = $dayNames[[int]$twNow.DayOfWeek]
$formatted = $twNow.ToString('yyyy-MM-dd') + " $dayEn " + $twNow.ToString('HH:mm:ss')

$output = @"
`u{1f550} **當下台灣時間：${formatted}（GMT+8）**

`u{1f534} **時間鐵律（教練 2026-06-09 親罵後寫死，違反 = 守則 #07 同處跌倒）**：
- 跟教練講時間 → **永遠先換算成台灣時間**（Asia/Taipei，UTC+8）
- 看到 ISO 字串「``2026-06-09T06:25:36.752Z``」→ Z = UTC → **+8 變 14:25:36（下午 2:25）**
- 禁止口語講「06:24」「06:25」等 Z 時間——這是 UTC，不是台灣時間
- 對教練講「上午 6 點半」「下午 2 點半」用白話，不用 24 小時制更好
"@

Write-Output $output
exit 0
