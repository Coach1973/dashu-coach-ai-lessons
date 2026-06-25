# ============================================================
# restore_junctions.ps1 — C 槽一鍵還原後重建所有 Junction
# 放置位置：D:\Claude-Data\restore_junctions.ps1
# 執行方式：用系統管理員身分開 PowerShell，貼這行：
#   powershell -ExecutionPolicy Bypass -File D:\Claude-Data\restore_junctions.ps1
# ============================================================

$ErrorActionPreference = "Stop"
$user = $env:USERPROFILE   # C:\Users\Administrator

function Make-Junction($link, $target) {
    if (-not (Test-Path $target)) {
        Write-Host "  ⚠️  目標不在 D 槽，跳過：$target" -ForegroundColor Yellow
        return
    }
    $item = Get-Item $link -ErrorAction SilentlyContinue
    if ($item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        Write-Host "  ✅ 已存在 Junction：$link" -ForegroundColor Green
        return
    }
    if (Test-Path $link) {
        $ts = Get-Date -Format "yyyyMMdd-HHmmss"
        Rename-Item $link "$link.bak.$ts"
        Write-Host "  📦 原資料夾改名 .bak：$link"
    }
    $parent = Split-Path $link -Parent
    if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    New-Item -ItemType Junction -Path $link -Target $target | Out-Null
    Write-Host "  ✅ Junction 建立：$link → $target" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== 還原 Junction 開始 ===" -ForegroundColor Cyan

# 1. Claude 共用大腦記憶
Write-Host ""
Write-Host "① Claude 共用大腦記憶"
$brainRepo = "D:\Claude-Data\mac-openclaw-workflows"
if (-not (Test-Path $brainRepo)) {
    Write-Host "  ⬇️  Repo 不在 D 槽，從 GitHub clone..."
    git clone https://github.com/Coach1973/mac-openclaw-workflows.git $brainRepo
}
# 找最近使用的 Claude project 目錄（encoded_path）
$projects = Join-Path $user ".claude\projects"
$encoded = (Get-ChildItem $projects -Directory -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1).Name
if (-not $encoded) { $encoded = "C--Users-Administrator--claude" }
Make-Junction (Join-Path $projects "$encoded\memory") "$brainRepo\claude-brain"

# 2. LINE
Write-Host ""
Write-Host "② LINE"
Make-Junction "$user\AppData\Local\LINE" "D:\Claude-Data\LINE-AppData-Local"

# 3. Chrome User Data
Write-Host ""
Write-Host "③ Chrome User Data"
Make-Junction "$user\AppData\Local\Google\Chrome\User Data" "D:\Claude-Data\Google-Chrome-UserData"

# 4. Perplexity
Write-Host ""
Write-Host "④ Perplexity"
Make-Junction "$user\AppData\Local\Perplexity" "D:\Claude-Data\Perplexity"

# 5. GanJing
Write-Host ""
Write-Host "⑤ GanJing"
Make-Junction "$user\AppData\Local\GanJing" "D:\Claude-Data\GanJing"

Write-Host ""
Write-Host "=== 完成！以下是 D 槽資料總覽 ===" -ForegroundColor Cyan
Get-ChildItem "D:\Claude-Data" | Select-Object Name, LastWriteTime | Format-Table -AutoSize
