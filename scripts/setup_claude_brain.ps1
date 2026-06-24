# ============================================================
# setup_claude_brain.ps1 — Windows 端「共用大腦」一鍵橋接
# 用途：把本機 Claude 桌面版記憶 (%USERPROFILE%\.claude\projects\<encoded>\memory)
#       接到雲端同步的 claude-brain（git repo 內），三機共用一份大腦。
# 機制：用 Junction（mklink /J 等效），不需系統管理員權限、可跨磁碟。
# 安全：原記憶資料夾一律先備份成 memory.bak.<時間>，可逆。
# 冪等：已經是 Junction 就直接結束。
# 用法：在 Windows 軍師端 PowerShell 執行：
#   powershell -ExecutionPolicy Bypass -File <repo>\scripts\setup_claude_brain.ps1
#   （若自動偵測的 repo 位置不對，可加 -RepoRoot "E:\Claude-Data\workspace"）
# ============================================================
param([string]$RepoRoot = "")

$ErrorActionPreference = "Stop"

# 1) 找到 brain repo root（預設 = 本腳本所在的上一層）
if ([string]::IsNullOrEmpty($RepoRoot)) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
$Brain    = Join-Path $RepoRoot "claude-brain"
$Registry = Join-Path $Brain "machines.json"

Write-Host "Brain repo:" $RepoRoot
Write-Host "Brain dir :" $Brain

if (-not (Test-Path $Brain)) {
    Write-Host "❌ 找不到 claude-brain，請先 git pull 取得最新 repo（或用 -RepoRoot 指定正確位置）" -ForegroundColor Red
    exit 1
}

# 2) 自動偵測本機 encoded_path：比對 machines.json 與 ~/.claude/projects/
$Projects = Join-Path $env:USERPROFILE ".claude\projects"
if (-not (Test-Path $Projects)) {
    Write-Host "❌ 找不到 $Projects（Claude 桌面版尚未在此機產生資料）" -ForegroundColor Red
    exit 1
}
$localDirs = Get-ChildItem $Projects -Directory | Select-Object -ExpandProperty Name
$encoded = $null
if (Test-Path $Registry) {
    $reg = Get-Content $Registry -Raw | ConvertFrom-Json
    foreach ($p in $reg.machines.PSObject.Properties) {
        $cfg = $p.Value
        if ($cfg.os -eq "windows" -and ($localDirs -contains $cfg.encoded_path)) {
            $encoded = $cfg.encoded_path; break
        }
    }
}
if (-not $encoded) {
    # 後備：取最近使用、含 memory 的資料夾
    $encoded = (Get-ChildItem $Projects -Directory | Sort-Object LastWriteTime -Descending |
                Select-Object -First 1).Name
    Write-Host "⚠️  registry 未比對到本機，後備採用最近使用的：$encoded" -ForegroundColor Yellow
}

$Link = Join-Path $Projects "$encoded\memory"
Write-Host "本機 encoded:" $encoded
Write-Host "memory 路徑 :" $Link

# 3) 已是 reparse point(Junction/symlink) → 結束
$item = Get-Item $Link -ErrorAction SilentlyContinue
if ($item -and $item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    Write-Host "✅ 已橋接（Junction 已存在），無需處理" -ForegroundColor Green
    exit 0
}

# 4) 真實資料夾 → 先備份（存檔不刪）
if (Test-Path $Link) {
    $ts = Get-Date -Format "yyyyMMdd-HHmmss"
    Move-Item $Link "$Link.bak.$ts"
    Write-Host "📦 原記憶已備份 → memory.bak.$ts（可日後比對合併獨有記憶，確認無誤再刪）"
}

# 5) 建立 Junction（不需管理員）
$parent = Split-Path $Link -Parent
if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
New-Item -ItemType Junction -Path $Link -Target $Brain | Out-Null

# 6) 驗證
$count = (Get-ChildItem $Link -Filter *.md).Count
if (Test-Path (Join-Path $Link "MEMORY.md")) {
    Write-Host "✅ 完成：本機已接上共用大腦，MEMORY.md 讀得到，共 $count 個事實檔。" -ForegroundColor Green
    Write-Host "   下次開工 git pull 會自動拉到其他機器寫的記憶。"
} else {
    Write-Host "⚠️  Junction 已建，但讀不到 MEMORY.md，請檢查 brain 是否已 git pull。" -ForegroundColor Yellow
}
