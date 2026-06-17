# Windows 桌面版 Claude Code 開工 hook 安裝/還原腳本 v3
#
# v3 設計核心（教練 2026-06-18 親定）：
#   - workspace + hook 腳本固定放 E 槽（E:\junshi-hook\workspace）
#   - 永久設環境變數 JUNSHI_HOOK_ROOT
#   - settings.json 在 C 槽（Claude Code 規定），但被一鍵還原洗掉後，
#     只要 E 槽工具箱還在 → 重跑本腳本一次就能完整重建
#
# 教練暗號：「裝 E 槽 hook」或「還原 hook」
# 兩種情境都跑同一支腳本：
#   情境 A：首次安裝 → 自動 clone workspace 到 E 槽 + 寫 settings.json
#   情境 B：一鍵還原後 → workspace 還在 E 槽，重寫 settings.json

param(
    [string]$Root = "E:\Claude-Data"
)

$ErrorActionPreference = 'Stop'
$REPO_URL = "https://github.com/Coach1973/mac-openclaw-workflows.git"

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🛠️  Windows Hook 安裝/還原 v3" -ForegroundColor Cyan
Write-Host "  根目錄: $Root" -ForegroundColor DarkGray
Write-Host "  設計: E 槽工具箱 + C 槽連接線 + 雲端真相" -ForegroundColor DarkGray
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$workspace  = Join-Path $Root "workspace"
$hookScript = Join-Path $workspace "scripts\feed_junshi_handoff.ps1"

# ───────── 1. 確認 E 槽可寫 ─────────
Write-Host "`n[1/6] 確認 $Root 可寫..." -ForegroundColor Yellow
$rootDrive = (Split-Path $Root -Qualifier)
if (-not (Test-Path $rootDrive)) {
    Write-Host "  ❌ $rootDrive 不存在，請插入 / 掛載再跑一次" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $Root)) {
    New-Item -ItemType Directory -Path $Root -Force | Out-Null
    Write-Host "  📁 建立 $Root" -ForegroundColor Cyan
}
$testFile = Join-Path $Root ".write_test"
try {
    Set-Content -Path $testFile -Value "ok" -ErrorAction Stop
    Remove-Item $testFile -Force
    Write-Host "  ✅ $Root 可寫" -ForegroundColor Green
} catch {
    Write-Host "  ❌ $Root 不可寫：$_" -ForegroundColor Red
    exit 1
}

# ───────── 2. clone 或 pull workspace ─────────
Write-Host "`n[2/6] 拉雲端 workspace 到 $workspace..." -ForegroundColor Yellow
if (-not (Test-Path $workspace)) {
    Write-Host "  📥 不存在 → git clone..." -ForegroundColor Cyan
    & git clone --quiet $REPO_URL $workspace
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ❌ Clone 失敗——請檢查 gh auth status" -ForegroundColor Red
        exit 1
    }
    Write-Host "  ✅ Clone 完成" -ForegroundColor Green
} else {
    & git -C $workspace pull --quiet
    $headHash = (& git -C $workspace rev-parse --short HEAD).Trim()
    Write-Host "  ✅ 已 pull 到 HEAD: $headHash" -ForegroundColor Green
}

if (-not (Test-Path $hookScript)) {
    Write-Host "  ❌ feed_junshi_handoff.ps1 不存在於 repo" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Hook 腳本就位: $hookScript" -ForegroundColor Green

# ───────── 3. 永久設環境變數 JUNSHI_HOOK_ROOT ─────────
Write-Host "`n[3/6] 永久設 JUNSHI_HOOK_ROOT 環境變數..." -ForegroundColor Yellow
[Environment]::SetEnvironmentVariable("JUNSHI_HOOK_ROOT", $Root, "User")
$env:JUNSHI_HOOK_ROOT = $Root
Write-Host "  ✅ 已設 JUNSHI_HOOK_ROOT = $Root（永久，登入時自動載入）" -ForegroundColor Green

# ───────── 4. 自動偵測 settings.json 位置（教練若把 .claude 搬到 E 槽就用 E 槽，不再被一鍵還原威脅）─────────
Write-Host "`n[4/6] 偵測 settings.json 位置..." -ForegroundColor Yellow

# 優先序：
#   1. $env:CLAUDE_CONFIG_DIR（Claude Code 官方自訂變數）
#   2. E:\Claude-Data\.claude（教練既有目錄，若存在則代表已搬到 E 槽）
#   3. %USERPROFILE%\.claude（Claude Code 預設，C 槽，會被一鍵還原洗掉）
$settingsLocations = @()
if ($env:CLAUDE_CONFIG_DIR) {
    $settingsLocations += [PSCustomObject]@{ Path = (Join-Path $env:CLAUDE_CONFIG_DIR "settings.json"); Source = "CLAUDE_CONFIG_DIR 環境變數" }
}
if (Test-Path "E:\Claude-Data\.claude") {
    $settingsLocations += [PSCustomObject]@{ Path = "E:\Claude-Data\.claude\settings.json"; Source = "E:\Claude-Data\.claude 既有目錄（教練既有）" }
}
$settingsLocations += [PSCustomObject]@{ Path = (Join-Path $env:USERPROFILE ".claude\settings.json"); Source = "%USERPROFILE%\.claude（C 槽預設，會被一鍵還原）" }

# 列所有候選給 Windows 軍師看（透明）
Write-Host "  偵測到的候選位置：" -ForegroundColor Cyan
foreach ($loc in $settingsLocations) {
    $exists = if (Test-Path $loc.Path) { "✅存在" } else { "—" }
    Write-Host "    [$exists] $($loc.Path)" -ForegroundColor DarkGray
    Write-Host "          來源：$($loc.Source)" -ForegroundColor DarkGray
}

# 優先用第一個存在的 .claude 目錄；都不存在就用最後一個（C 槽）建新
$settingsFile = $settingsLocations[0].Path
foreach ($loc in $settingsLocations) {
    $dir = Split-Path $loc.Path -Parent
    if (Test-Path $dir) {
        $settingsFile = $loc.Path
        Write-Host "  ✅ 選用: $settingsFile" -ForegroundColor Green
        if ($settingsFile -like "E:\*") {
            Write-Host "  🎉 settings.json 在 E 槽，連接線也免疫一鍵還原！" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  settings.json 仍在 C 槽，一鍵還原後需重跑本腳本" -ForegroundColor Yellow
        }
        break
    }
}

$settingsDir = Split-Path $settingsFile -Parent
if (-not (Test-Path $settingsDir)) { New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null }
Write-Host "" -ForegroundColor DarkGray
Write-Host "  重建 hook 註冊..." -ForegroundColor Yellow

if (Test-Path $settingsFile) {
    $backup = "$settingsFile.bak.v3.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $settingsFile $backup -Force
    Write-Host "  💾 備份舊 settings: $backup" -ForegroundColor Cyan
    $settings = Get-Content $settingsFile -Raw -Encoding UTF8 | ConvertFrom-Json
} else {
    Write-Host "  📝 settings.json 不存在（可能剛被一鍵還原洗掉），建新檔" -ForegroundColor Cyan
    $settings = [PSCustomObject]@{}
}

if (-not $settings.PSObject.Properties['hooks']) {
    $settings | Add-Member -NotePropertyName hooks -NotePropertyValue ([PSCustomObject]@{}) -Force
}
if (-not $settings.hooks.PSObject.Properties['UserPromptSubmit']) {
    $settings.hooks | Add-Member -NotePropertyName UserPromptSubmit -NotePropertyValue @() -Force
}

# 清掉所有 feed_junshi_handoff 舊註冊（包括殭屍指向 C 槽 / 舊路徑）
$brokenCount = 0
$cleanedEntries = @()
foreach ($entry in $settings.hooks.UserPromptSubmit) {
    $filtered = @($entry.hooks | Where-Object {
        if ($_.command -match "feed_junshi_handoff\.ps1") { $brokenCount++; return $false }
        return $true
    })
    if ($filtered.Count -gt 0) {
        $entry.hooks = $filtered
        $cleanedEntries += $entry
    }
}

# 加新註冊指向 E 槽
$hookCmd = "powershell.exe -ExecutionPolicy Bypass -File `"$hookScript`""
$cleanedEntries += [PSCustomObject]@{
    matcher = ""
    hooks   = @([PSCustomObject]@{ type = "command"; command = $hookCmd })
}
$settings.hooks.UserPromptSubmit = $cleanedEntries

# UTF-8 with BOM 寫回（PS 5.1 emoji 安全）
$json = $settings | ConvertTo-Json -Depth 10
$utf8Bom = New-Object System.Text.UTF8Encoding $true
[System.IO.File]::WriteAllText($settingsFile, $json, $utf8Bom)
Write-Host "  ✅ 清掉舊註冊 $brokenCount 個，重新註冊 1 個 → E 槽" -ForegroundColor Green

# ───────── 5. Self-test ─────────
Write-Host "`n[5/6] Self-test（模擬「開工」+ 驗證雲端 pull）..." -ForegroundColor Yellow
$testPayload = @{ session_id = "v3-$(Get-Date -Format 'HHmmss')"; prompt = "開工" } | ConvertTo-Json -Compress
$testOutput  = $testPayload | & powershell.exe -ExecutionPolicy Bypass -File $hookScript 2>&1
$cloudLine   = ($testOutput | Select-String "已拉雲端最新|首次 clone").Line | Select-Object -First 1
if ($testOutput -match "軍師接力棒") {
    Write-Host "  ✅ Self-test 通過——hook 收到「開工」會自動 git pull + 注入接力棒" -ForegroundColor Green
    if ($cloudLine) { Write-Host "  ☁️  $($cloudLine.Trim())" -ForegroundColor Cyan }
} else {
    Write-Host "  ⚠️  Self-test 異常，輸出前 5 行：" -ForegroundColor Yellow
    ($testOutput -split "`n" | Select-Object -First 5) | ForEach-Object { Write-Host "     $_" -ForegroundColor DarkGray }
}

# ───────── 6. 留還原暗號便條到 E 槽 ─────────
Write-Host "`n[6/6] 寫還原便條到 $Root\一鍵還原後怎麼修.txt..." -ForegroundColor Yellow
$noteContent = @"
🛠️ Windows Hook 一鍵還原後的修復步驟
=========================================

如果某天用了「易數一鍵還原」洗掉 C 槽，Claude Code 桌面版打「開工」沒反應，
不要慌，按下面三步驟做就會完全恢復：

【步驟 1】開 PowerShell

【步驟 2】跑這一行（從 E 槽工具箱重新安裝 hook）：
  powershell -ExecutionPolicy Bypass -File "$Root\workspace\scripts\install_or_restore_windows_hook.ps1"

【步驟 3】完全關閉 Claude Code 重開，打「開」測試。

設計原理：
- 工具箱在 E 槽：$Root\workspace
- 連接線在 C 槽 settings.json：被一鍵還原洗掉
- 真相在雲端 GitHub：永遠最新

只要 E 槽工具箱沒被刪，重跑一次安裝腳本就能把 C 槽連接線接回去。

最後安裝時間：$(Get-Date -Format 'yyyy-MM-dd HH:mm') 台灣時間
"@
$notePath = Join-Path $Root "一鍵還原後怎麼修.txt"
Set-Content -Path $notePath -Value $noteContent -Encoding UTF8
Write-Host "  ✅ 已寫: $notePath" -ForegroundColor Green

# ───────── 最終報告 ─────────
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ 安裝/還原完成（v3 E 槽工具箱設計）" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📁 工具箱（E 槽，不被一鍵還原）: $workspace"
$connLocation = if ($settingsFile -like "E:\*") { "🎉 連接線（E 槽，也免疫一鍵還原）" } else { "🔗 連接線（C 槽，一鍵還原會洗掉，需重跑本腳本）" }
Write-Host "${connLocation}: $settingsFile"
Write-Host "☁️  真相源（雲端）: $REPO_URL"
Write-Host "🌐 環境變數: JUNSHI_HOOK_ROOT = $Root"
Write-Host "🧹 清掉殭屍註冊: $brokenCount 個"
Write-Host "📝 還原便條: $notePath"
Write-Host ""
Write-Host "🔴 下一步：" -ForegroundColor Red
Write-Host "  1. 完全關閉 Claude Code 桌面版（退出進程）" -ForegroundColor White
Write-Host "  2. 重新開啟" -ForegroundColor White
Write-Host "  3. 開新對話打「開」或「開工」→ 看到雲端 HEAD hash + 接力棒" -ForegroundColor White
Write-Host ""
Write-Host "回報 Mac 軍師：把上面五行報告貼過去就完成驗證" -ForegroundColor Cyan
