# 全自動診斷 + 徹底修復 Windows 桌面版 Claude Code 開工 hook (v2)
#
# v2 設計核心（教練 2026-06-18 親定）：
#   - 完全不掃 E 槽（教練 E 槽在修復）
#   - 固定走 %USERPROFILE%\.openclaw\workspace（C 槽）
#   - workspace 不存在 → 自動 git clone（一次性）
#   - 用新版 feed_junshi_handoff.ps1（自帶每次 git pull）
#
# 教練暗號：「徹底修 hook」

$ErrorActionPreference = 'Stop'
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔍 Windows 軍師 hook 診斷 + 徹底修復 v2" -ForegroundColor Cyan
Write-Host "  （不碰 E 槽，固定 C 槽，hook 自帶雲端同步）" -ForegroundColor DarkGray
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$REPO_URL  = "https://github.com/Coach1973/mac-openclaw-workflows.git"
$workspace = Join-Path $env:USERPROFILE ".openclaw\workspace"
$hookScript = Join-Path $workspace "scripts\feed_junshi_handoff.ps1"

# ───────── 1. 確保 C 槽 workspace 存在（不存在就 clone）─────────
Write-Host "`n[1/6] 確認 workspace（固定 C 槽位置：$workspace）..." -ForegroundColor Yellow
if (-not (Test-Path $workspace)) {
    Write-Host "  📥 不存在 → 從雲端 clone..." -ForegroundColor Cyan
    $parentDir = Split-Path $workspace -Parent
    if (-not (Test-Path $parentDir)) { New-Item -ItemType Directory -Path $parentDir -Force | Out-Null }
    & git clone --quiet $REPO_URL $workspace
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ❌ Clone 失敗——請檢查 GitHub credential（試 ``gh auth status``）" -ForegroundColor Red
        exit 1
    }
    Write-Host "  ✅ Clone 完成" -ForegroundColor Green
} else {
    Write-Host "  ✅ 已存在 → git pull 取最新..." -ForegroundColor Green
    & git -C $workspace pull --quiet
    $headHash = (& git -C $workspace rev-parse --short HEAD).Trim()
    Write-Host "  ✅ 已拉到 HEAD: $headHash" -ForegroundColor Green
}

if (-not (Test-Path $hookScript)) {
    Write-Host "  ❌ scripts\feed_junshi_handoff.ps1 不存在——repo 結構異常" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Hook 腳本: $hookScript" -ForegroundColor Green

# ───────── 2. 讀現有 settings.json ─────────
Write-Host "`n[2/6] 檢查現有 settings.json..." -ForegroundColor Yellow
$settingsFile = Join-Path $env:USERPROFILE ".claude\settings.json"
if (-not (Test-Path $settingsFile)) {
    Write-Host "  📝 不存在，建新檔" -ForegroundColor Cyan
    $settings = [PSCustomObject]@{}
} else {
    $backup = "$settingsFile.bak.diagfix.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $settingsFile $backup -Force
    Write-Host "  💾 備份: $backup" -ForegroundColor Cyan
    $settings = Get-Content $settingsFile -Raw -Encoding UTF8 | ConvertFrom-Json
}

# ───────── 3. 掃描舊 hook 註冊（包括指向已不存在路徑的殭屍註冊）─────────
Write-Host "`n[3/6] 掃描舊 hook 註冊..." -ForegroundColor Yellow
$brokenHooks = @()
$validHooks  = @()
if ($settings.PSObject.Properties['hooks'] -and $settings.hooks.PSObject.Properties['UserPromptSubmit']) {
    foreach ($entry in $settings.hooks.UserPromptSubmit) {
        foreach ($h in $entry.hooks) {
            if ($h.command -match "feed_junshi_handoff\.ps1") {
                if ($h.command -match '-File\s+"([^"]+)"') { $registeredPath = $matches[1] }
                elseif ($h.command -match '-File\s+(\S+)') { $registeredPath = $matches[1] }
                else { $registeredPath = "(無法解析)" }

                if (Test-Path $registeredPath) {
                    $validHooks += $registeredPath
                    Write-Host "  ✅ 有效: $registeredPath" -ForegroundColor Green
                } else {
                    $brokenHooks += $registeredPath
                    Write-Host "  ❌ 殭屍（檔案不存在）: $registeredPath" -ForegroundColor Red
                }
            }
        }
    }
}

# ───────── 4. 清掉所有 feed_junshi_handoff 註冊，重寫一份指向正確路徑 ─────────
Write-Host "`n[4/6] 重建 hook（清舊註冊 + 寫新指向）..." -ForegroundColor Yellow
if (-not $settings.PSObject.Properties['hooks']) {
    $settings | Add-Member -NotePropertyName hooks -NotePropertyValue ([PSCustomObject]@{}) -Force
}
if (-not $settings.hooks.PSObject.Properties['UserPromptSubmit']) {
    $settings.hooks | Add-Member -NotePropertyName UserPromptSubmit -NotePropertyValue @() -Force
}
$cleanedEntries = @()
foreach ($entry in $settings.hooks.UserPromptSubmit) {
    $remainingHooks = @($entry.hooks | Where-Object { $_.command -notmatch "feed_junshi_handoff\.ps1" })
    if ($remainingHooks.Count -gt 0) {
        $entry.hooks = $remainingHooks
        $cleanedEntries += $entry
    }
}
$hookCmd = "powershell.exe -ExecutionPolicy Bypass -File `"$hookScript`""
$cleanedEntries += [PSCustomObject]@{
    matcher = ""
    hooks   = @([PSCustomObject]@{ type = "command"; command = $hookCmd })
}
$settings.hooks.UserPromptSubmit = $cleanedEntries
Write-Host "  ✅ 清除殭屍註冊 $($brokenHooks.Count) 個" -ForegroundColor Green
Write-Host "  ✅ 重新註冊 1 個 → $hookScript" -ForegroundColor Green

# ───────── 5. 寫回 settings.json（UTF-8 with BOM 避免 PS 5.1 emoji 亂碼）─────────
Write-Host "`n[5/6] 寫回 settings.json..." -ForegroundColor Yellow
$settingsDir = Split-Path $settingsFile -Parent
if (-not (Test-Path $settingsDir)) { New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null }
$json = $settings | ConvertTo-Json -Depth 10
$utf8Bom = New-Object System.Text.UTF8Encoding $true
[System.IO.File]::WriteAllText($settingsFile, $json, $utf8Bom)
Write-Host "  ✅ 已寫入 $settingsFile" -ForegroundColor Green

# ───────── 6. Self-test（真的跑一次 hook + 驗證雲端 git pull 通了）─────────
Write-Host "`n[6/6] Self-test（模擬「開工」+ 驗證雲端 git pull）..." -ForegroundColor Yellow
$testPayload = @{ session_id = "diagfix-$(Get-Date -Format 'HHmmss')"; prompt = "開工" } | ConvertTo-Json -Compress
$testOutput  = $testPayload | & powershell.exe -ExecutionPolicy Bypass -File $hookScript 2>&1
$cloudLine   = ($testOutput | Select-String "已拉雲端最新|首次 clone").Line | Select-Object -First 1
$handoffOK   = ($testOutput -match "軍師接力棒")

if ($handoffOK) {
    Write-Host "  ✅ Self-test 通過——hook 收到「開工」會自動 git pull + 注入接力棒" -ForegroundColor Green
    if ($cloudLine) { Write-Host "  ☁️  $($cloudLine.Trim())" -ForegroundColor Cyan }
} else {
    Write-Host "  ⚠️  Self-test 異常，輸出前 5 行：" -ForegroundColor Yellow
    ($testOutput -split "`n" | Select-Object -First 5) | ForEach-Object { Write-Host "     $_" -ForegroundColor DarkGray }
}

# ───────── 最終報告 ─────────
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ 修復完成（v2 雲端優先設計）" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📁 Workspace: $workspace（**不依賴 E 槽**）"
Write-Host "🪝 Hook 註冊: $hookScript"
Write-Host "☁️  雲端同步: 每次「開工」自動 git pull"
Write-Host "🧹 清除殭屍註冊: $($brokenHooks.Count) 個"
Write-Host ""
Write-Host "🔴 下一步：" -ForegroundColor Red
Write-Host "  1. 完全關閉 Claude Code 桌面版（不是隱藏視窗 — 是退出進程）" -ForegroundColor White
Write-Host "  2. 重新開啟" -ForegroundColor White
Write-Host "  3. 開新對話打「開」或「開工」" -ForegroundColor White
Write-Host "     應該會看到「軍師接力棒（系統自動注入）」+ 雲端 HEAD hash" -ForegroundColor White
Write-Host ""
Write-Host "回報 Mac 軍師：把上面五行報告貼過去就完成驗證" -ForegroundColor Cyan
