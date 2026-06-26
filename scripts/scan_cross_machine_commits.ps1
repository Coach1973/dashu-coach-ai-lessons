# Hook: UserPromptSubmit (Windows 版)
# 用途：開工時自動掃描 git log 最近 24 小時其他機器的 commit，
#       防止跨機交接任務漏接（不依賴寄信，系統自動抓）
# 起因：2026-06-26 聯想交接講座行銷頁給 ACER，但沒寄信，
#       ACER 和 Mac 都漏接，教練自己提醒 = 搬運工（守則 #12 違規）
# 對應 Mac 版: scan_cross_machine_commits.sh

$ErrorActionPreference = "SilentlyContinue"

# 讀 stdin JSON
$raw = [Console]::In.ReadToEnd()
try { $payload = $raw | ConvertFrom-Json -ErrorAction Stop } catch { exit 0 }
$sessionId = if ($payload.session_id) { [string]$payload.session_id } else { "" }

# 同 session 只跑一次
$markerDir = Join-Path $env:TEMP "cross_machine_markers"
if (-not (Test-Path $markerDir)) { New-Item -ItemType Directory -Path $markerDir -Force | Out-Null }
$marker = Join-Path $markerDir "scanned_$sessionId"
if (Test-Path $marker) { exit 0 }

# 找 workspace
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Workspace = Split-Path -Parent $ScriptDir
if (-not (Test-Path (Join-Path $Workspace ".git"))) {
    $parent = Split-Path -Parent $Workspace
    if (Test-Path (Join-Path $parent ".git")) { $Workspace = $parent }
    else { exit 0 }
}

Push-Location $Workspace

# 先 git pull 確保看到其他機器的最新 commit（節流：5 分鐘內不重複）
$pullLock = Join-Path $env:TEMP "cross_commit_git_pull.lock"
$needPull = $true
if (Test-Path $pullLock) {
    $lockAge = (Get-Date) - (Get-Item $pullLock).LastWriteTime
    if ($lockAge.TotalSeconds -lt 300) { $needPull = $false }
}
if ($needPull) {
    & git pull --quiet 2>$null
    New-Item -Path $pullLock -ItemType File -Force | Out-Null
}

# 判斷自己是哪台（排除自己的 commit）
$machineName = $env:AGENT_INBOX_NAME
if (-not $machineName) { $machineName = "windows" }

# 自己的 prefix（用來排除）
$myPrefixes = @()
if ($machineName -eq "lenovo") { $myPrefixes = @("[Win]", "[Lenovo]", "聯想") }
elseif ($machineName -eq "acer") { $myPrefixes = @("[ACER]", "[Acer]", "ACER") }
else { $myPrefixes = @("[Win]") }

# 掃最近 24 小時 commit
$since = (Get-Date).AddHours(-24).ToString("yyyy-MM-dd HH:mm:ss")
$logLines = & git log --all --oneline --since="$since" --format="%h|%ai|%s" 2>$null

if (-not $logLines) { New-Item -Path $marker -ItemType File -Force | Out-Null; Pop-Location; exit 0 }

$relevant = @()
foreach ($line in $logLines) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    if ($line -match "auto-backup|auto:|Merge branch") { continue }

    # 排除自己的 commit
    $isOwn = $false
    foreach ($prefix in $myPrefixes) {
        if ($line -match [regex]::Escape($prefix)) { $isOwn = $true; break }
    }
    if ($isOwn) { continue }

    $parts = $line -split '\|', 3
    if ($parts.Count -lt 3) { continue }

    $hash = $parts[0]
    $datetime = $parts[1].Trim()
    $msg = $parts[2].Trim()

    # 簡化時間顯示
    try {
        $dt = [DateTime]::Parse($datetime)
        $timeStr = $dt.ToString("MM/dd HH:mm")
    } catch {
        $timeStr = $datetime.Substring(5, 11)
    }

    $relevant += "  * $timeStr ``$hash`` $msg"
    if ($relevant.Count -ge 15) { break }
}

Pop-Location

if ($relevant.Count -eq 0) { New-Item -Path $marker -ItemType File -Force | Out-Null; exit 0 }

$count = $relevant.Count
$body = $relevant -join "`n"

$output = @"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 跨機動態（最近 24 小時其他機器的 $count 筆 commit）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$body

⚠️ 如有「交接」「handoff」相關 commit，請主動讀取並回報教練。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"@

Write-Output $output
New-Item -Path $marker -ItemType File -Force | Out-Null
exit 0
