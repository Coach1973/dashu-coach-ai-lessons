# Session 時間覺察工具——每次回應前呼叫一次（Windows 通用版）
# v2: 動態路徑，不再寫死 E:\Claude-Data（ACER/聯想通用）
# 對應 Mac 版: session_time_context.sh

$ErrorActionPreference = "SilentlyContinue"

$now = Get-Date

# 動態找 Claude 專案目錄下最新的 jsonl
$projectRoot = Join-Path $env:USERPROFILE ".claude\projects"
if (-not (Test-Path $projectRoot)) {
    Write-Host "[時間覺察] 現在：$($now.ToString('yyyy-MM-dd HH:mm:ss'))（無專案目錄）"
    exit
}

$latestJsonl = Get-ChildItem $projectRoot -Recurse -Filter "*.jsonl" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $latestJsonl) {
    Write-Host "[時間覺察] 現在：$($now.ToString('yyyy-MM-dd HH:mm:ss'))（無 jsonl）"
    exit
}

$lines = Get-Content $latestJsonl.FullName -Encoding UTF8
$firstTs = $null
$lastUserTs = $null
$lastUserPreview = $null

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match '"timestamp"\s*:\s*"([^"]+)"') {
        $ts = $matches[1]
        if (-not $firstTs) { $firstTs = $ts }
        if ($line -match '"role"\s*:\s*"user"' -or $line -match '"type"\s*:\s*"user"') {
            $lastUserTs = $ts
            if ($line -match '"message"\s*:\s*"([^"]{1,50})') {
                $lastUserPreview = $matches[1]
            }
        }
    }
}

$dayNames = @('日','一','二','三','四','五','六')

if ($firstTs) {
    $first = [DateTime]::Parse($firstTs).ToLocalTime()
    $dur = $now - $first
    $dayName = $dayNames[[int]$now.DayOfWeek]

    Write-Host "[時間覺察 · 台灣時間 GMT+8]"
    Write-Host ("  現在：{0} 星期{1}" -f $now.ToString('yyyy-MM-dd HH:mm:ss'), $dayName)
    Write-Host ("  Session 開始：{0}（{1:N1} 小時前）" -f $first.ToString('yyyy-MM-dd HH:mm:ss'), $dur.TotalHours)
    if ($lastUserTs) {
        $lastUser = [DateTime]::Parse($lastUserTs).ToLocalTime()
        $sinceUser = ($now - $lastUser).TotalMinutes
        $sinceHours = ($now - $lastUser).TotalHours
        if ($sinceHours -ge 1) {
            $sinceText = "{0:N1} 小時前" -f $sinceHours
        } else {
            $sinceText = "{0:N1} 分鐘前" -f $sinceUser
        }
        $previewText = if ($lastUserPreview) { "「$lastUserPreview…」" } else { "" }
        Write-Host ("  教練上次說話：{0}（{1}）{2}" -f $lastUser.ToString('HH:mm:ss'), $sinceText, $previewText)
    }
}
