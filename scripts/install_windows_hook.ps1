# 一鍵安裝 Windows 桌面版 Claude Code 的「開工」暗號 hook
# 執行方式（在 Windows PowerShell 跑一次即可）：
#   cd $env:USERPROFILE\.openclaw\workspace
#   powershell -ExecutionPolicy Bypass -File scripts\install_windows_hook.ps1
#
# 作用：
#   1. 確認 scripts\feed_junshi_handoff.ps1 存在
#   2. 安全 merge 到 %USERPROFILE%\.claude\settings.json 的 hooks.UserPromptSubmit
#   3. 已存在則跳過（不重複註冊）；舊 settings.json 自動備份
#   4. 完成後跑一次 self-test 驗證能跑

$ErrorActionPreference = 'Stop'

$workspace = $env:OPENCLAW_WORKSPACE
if (-not $workspace) {
    $workspace = Join-Path $env:USERPROFILE ".openclaw\workspace"
}
$hookScript   = Join-Path $workspace "scripts\feed_junshi_handoff.ps1"
$settingsDir  = Join-Path $env:USERPROFILE ".claude"
$settingsFile = Join-Path $settingsDir "settings.json"

# ───────── 1. 確認 hook 腳本存在 ─────────
if (-not (Test-Path $hookScript)) {
    Write-Host "❌ 找不到 hook 腳本：$hookScript" -ForegroundColor Red
    Write-Host "請先 git pull 確保 workspace 是最新版" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Hook 腳本存在：$hookScript" -ForegroundColor Green

# ───────── 2. 確認 .claude 目錄存在 ─────────
if (-not (Test-Path $settingsDir)) {
    New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
    Write-Host "📂 建立 $settingsDir" -ForegroundColor Cyan
}

# ───────── 3. 讀現有 settings.json（沒有就建空的）─────────
if (Test-Path $settingsFile) {
    $backup = "$settingsFile.bak.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $settingsFile $backup -Force
    Write-Host "💾 備份舊 settings：$backup" -ForegroundColor Cyan
    $settings = Get-Content $settingsFile -Raw -Encoding UTF8 | ConvertFrom-Json
} else {
    $settings = [PSCustomObject]@{}
    Write-Host "📝 settings.json 不存在，建立新檔" -ForegroundColor Cyan
}

# ───────── 4. 確保 hooks.UserPromptSubmit 結構存在 ─────────
if (-not $settings.PSObject.Properties['hooks']) {
    $settings | Add-Member -NotePropertyName hooks -NotePropertyValue ([PSCustomObject]@{}) -Force
}
if (-not $settings.hooks.PSObject.Properties['UserPromptSubmit']) {
    $settings.hooks | Add-Member -NotePropertyName UserPromptSubmit -NotePropertyValue @() -Force
}

# ───────── 5. 構造 hook 指令（PowerShell 走 -File）─────────
# Claude Code hook 規格：執行檔吃 stdin JSON、stdout 注入 context
$hookCmd = "powershell.exe -ExecutionPolicy Bypass -File `"$hookScript`""

# ───────── 6. 檢查是否已註冊（避免重複）─────────
$alreadyRegistered = $false
foreach ($entry in $settings.hooks.UserPromptSubmit) {
    foreach ($h in $entry.hooks) {
        if ($h.command -like "*feed_junshi_handoff.ps1*") {
            $alreadyRegistered = $true
            break
        }
    }
    if ($alreadyRegistered) { break }
}

if ($alreadyRegistered) {
    Write-Host "⚠️  feed_junshi_handoff.ps1 已註冊，跳過" -ForegroundColor Yellow
} else {
    # 新增一筆 hook entry
    $newEntry = [PSCustomObject]@{
        matcher = ""
        hooks   = @(
            [PSCustomObject]@{
                type    = "command"
                command = $hookCmd
            }
        )
    }
    $settings.hooks.UserPromptSubmit = @($settings.hooks.UserPromptSubmit) + $newEntry
    Write-Host "✅ 已註冊 feed_junshi_handoff.ps1 到 UserPromptSubmit" -ForegroundColor Green
}

# ───────── 7. 寫回 settings.json ─────────
$json = $settings | ConvertTo-Json -Depth 10
Set-Content -Path $settingsFile -Value $json -Encoding UTF8
Write-Host "💾 已寫入 $settingsFile" -ForegroundColor Green

# ───────── 8. Self-test（模擬「開工」觸發）─────────
Write-Host ""
Write-Host "🩺 跑 self-test（模擬教練說「開工」）..." -ForegroundColor Cyan
$testPayload = @{ session_id = "selftest-$(Get-Date -Format 'HHmmss')"; prompt = "開工" } | ConvertTo-Json -Compress
$testOutput  = $testPayload | & powershell.exe -ExecutionPolicy Bypass -File $hookScript 2>&1
$firstLine   = ($testOutput -split "`n" | Select-Object -First 1)
if ($firstLine -match "軍師接力棒") {
    Write-Host "✅ Self-test 通過——hook 收到「開工」會注入接力棒" -ForegroundColor Green
} else {
    Write-Host "⚠️  Self-test 異常，第一行輸出：$firstLine" -ForegroundColor Yellow
    Write-Host "（如果 JUNSHI_HANDOFF_LATEST.md 不存在會跑出警告訊息，這正常）" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🎉 安裝完成。下一步：" -ForegroundColor Green
Write-Host "  1. 完全關閉 Claude Code 桌面版" -ForegroundColor White
Write-Host "  2. 重新開啟" -ForegroundColor White
Write-Host "  3. 開新對話，第一句打「開」或「開工」" -ForegroundColor White
Write-Host "  4. 軍師會自動讀完接力棒並回報「我已讀完接力棒」" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
