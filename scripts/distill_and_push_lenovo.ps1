# 聯想端：每 2 小時把今日 memory 蒸餾推到雲端
# 對應備忘：knowledges/2026-06-30_跨機verbatim蒸餾備忘.md（交付物 A）
# 作者：Mac 軍師 Sonnet 4.6（2026-06-30 上午）
# 目標讀者：聯想軍師（請依本機 workspace 實際路徑調整 $Workspace）

$ErrorActionPreference = 'Stop'

# === 環境設定（聯想軍師請改成自己 workspace 路徑）===
$Workspace = $env:LENOVO_WORKSPACE
if (-not $Workspace) { $Workspace = 'E:\openclaw\workspace' }  # 預設聯想 E 槽
$AgentTag  = '[聯想]'
$VerbatimDir = Join-Path $Workspace 'memory\verbatim\lenovo'

if (-not (Test-Path $Workspace))   { Write-Host "WORKSPACE_NOT_FOUND: $Workspace"; exit 0 }
if (-not (Test-Path $VerbatimDir)) { New-Item -ItemType Directory -Force -Path $VerbatimDir | Out-Null }

Set-Location $Workspace

# === 台灣時間日期（UTC+8）===
$Today = (Get-Date).ToUniversalTime().AddHours(8).ToString('yyyy-MM-dd')
$Src   = Join-Path $Workspace "memory\$Today.md"
$Dst   = Join-Path $VerbatimDir "$Today.md"

if (-not (Test-Path $Src)) { Write-Host "NO_MEMORY: $Src"; exit 0 }

# === 抽 🦞 小龍蝦 bullet（沿用 Mac 端規則）===
$content = Get-Content $Src -Raw -Encoding UTF8
$entries = New-Object System.Collections.ArrayList
$skip = @(
    'HEARTBEAT_OK','replied with.*HEARTBEAT','cron job status output',
    'async exec.*completed','heartbeat poll','context overflow','session restart'
)
$pattern = [regex]'🦞 小龍蝦：([\s\S]*?)(?=👤 教練：|---|\Z)'
foreach ($m in $pattern.Matches($content)) {
    foreach ($line in $m.Groups[1].Value -split "`n") {
        $t = $line.TrimStart()
        if (-not $t.StartsWith('- ')) { continue }
        $t = $t.Substring(2).Trim()
        if ($t.Length -lt 30) { continue }
        $skipMatch = $false
        foreach ($p in $skip) { if ($t -match $p) { $skipMatch = $true; break } }
        if ($skipMatch) { continue }
        if ($t.Length -gt 300) { $t = $t.Substring(0, 300) }
        [void]$entries.Add("$AgentTag $t")
    }
}

if ($entries.Count -eq 0) { Write-Host 'NO_ENTRIES'; exit 0 }

# === 寫入跨機 verbatim 檔（每次覆寫當日累積）===
$header = "# $AgentTag verbatim · $Today`n`n> 自動蒸餾 · 共 $($entries.Count) 則 · 更新時間 $(Get-Date -Format 'HH:mm') (Asia/Taipei)`n>`n> 試金石候選 marker：🪨 試金石候選：<一句話總結>`n`n"
$body   = ($entries | ForEach-Object { "- $_" }) -join "`n"
Set-Content -Path $Dst -Value "$header$body`n" -Encoding UTF8

# === git add + commit + push ===
git add "memory/verbatim/lenovo/$Today.md" 2>&1 | Out-Null
$staged = git diff --staged --quiet; $ec = $LASTEXITCODE
if ($ec -ne 0) {
    git commit -m "auto: 聯想對話蒸餾 $Today（$($entries.Count) 則）" 2>&1 | Out-Null
    git push origin main 2>&1 | Out-Null
    Write-Host "PUSHED: $($entries.Count) entries"
} else {
    Write-Host 'NO_CHANGE'
}
