# Session 時間覺察工具——每次回應前呼叫一次
# 用法：powershell -ExecutionPolicy Bypass -File scripts\session_time_context.ps1

$ErrorActionPreference = "SilentlyContinue"

$now = Get-Date
$projectDir = "E:\Claude-Data\.claude\projects\E--Claude-Data"
$latestJsonl = Get-ChildItem $projectDir -Filter "*.jsonl" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $latestJsonl) {
    Write-Host "[時間覺察] 現在：$($now.ToString('yyyy-MM-dd HH:mm:ss'))（無 jsonl）"
    exit
}

$lines = Get-Content $latestJsonl.FullName -Encoding UTF8
$firstTs = $null
$lastUserTs = $null
$lastUserMsg = $null

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match '"timestamp"\s*:\s*"([^"]+)"') {
        if (-not $firstTs) { $firstTs = $matches[1] }
        if ($line -match '"role"\s*:\s*"user"' -or $line -match '"type"\s*:\s*"user"') {
            $lastUserTs = $matches[1]
        }
    }
}

if ($firstTs) {
    $first = [DateTime]::Parse($firstTs).ToLocalTime()
    $dur = $now - $first
    Write-Host ("[時間覺察]")
    Write-Host ("  現在：{0} 星期{1}" -f $now.ToString('yyyy-MM-dd HH:mm:ss'), @('日','一','二','三','四','五','六')[[int]$now.DayOfWeek])
    Write-Host ("  Session 開始：{0}" -f $first.ToString('yyyy-MM-dd HH:mm:ss'))
    Write-Host ("  Session 已跑：{0:N1} 小時" -f $dur.TotalHours)
    if ($lastUserTs) {
        $lastUser = [DateTime]::Parse($lastUserTs).ToLocalTime()
        $sinceUser = ($now - $lastUser).TotalMinutes
        Write-Host ("  教練上次說話：{0}（{1:N1} 分鐘前）" -f $lastUser.ToString('HH:mm:ss'), $sinceUser)
    }
}
