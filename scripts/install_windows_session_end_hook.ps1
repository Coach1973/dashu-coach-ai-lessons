# Windows 軍師專用：一鍵安裝 session-end auto-push hook
# 用途：在 Windows 桌面版 Claude Code 註冊 Stop hook → session 結束自動 push 到 GitHub
# 對應：Mac 端 scripts/session_end_auto_push.sh + ~/.claude/settings.json Stop hook
#
# 教練用法（在 Windows 終端機任一視窗貼這一行）：
#   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.openclaw\workspace\scripts\install_windows_session_end_hook.ps1"
#
# 若 workspace 在 E 槽（教練 Claude-Data 結構）：
#   powershell -ExecutionPolicy Bypass -File "E:\Claude-Data\workspace\scripts\install_windows_session_end_hook.ps1"

$ErrorActionPreference = 'Stop'

# ───────── 1. 定位 workspace（與 feed_junshi_handoff.ps1 同邏輯）─────────
if ($env:JUNSHI_HOOK_ROOT) {
    $workspace = Join-Path $env:JUNSHI_HOOK_ROOT "workspace"
} elseif (Test-Path "E:\Claude-Data\workspace") {
    $workspace = "E:\Claude-Data\workspace"
} elseif (Test-Path "E:\junshi-hook\workspace") {
    $workspace = "E:\junshi-hook\workspace"
} else {
    $workspace = Join-Path $env:USERPROFILE ".openclaw\workspace"
}

$hookScript = Join-Path $workspace "scripts\session_end_auto_push.ps1"

if (-not (Test-Path $hookScript)) {
    Write-Host "❌ 找不到 hook 腳本：$hookScript" -ForegroundColor Red
    Write-Host "請先 git pull workspace，再重跑此安裝腳本。" -ForegroundColor Yellow
    exit 1
}

# ───────── 2. 定位 Claude settings.json（會跟 junction 走 E 槽）─────────
$settingsPath = Join-Path $env:USERPROFILE ".claude\settings.json"

if (-not (Test-Path $settingsPath)) {
    # 初次安裝：建空殼
    $settingsDir = Split-Path $settingsPath -Parent
    if (-not (Test-Path $settingsDir)) {
        New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
    }
    @{ hooks = @{} } | ConvertTo-Json -Depth 10 | Set-Content -Path $settingsPath -Encoding UTF8
}

# ───────── 3. 讀 + 改 + 寫 settings.json ─────────
$settings = Get-Content -Path $settingsPath -Encoding UTF8 -Raw | ConvertFrom-Json

# 確保 hooks.Stop 存在
if (-not $settings.hooks) {
    $settings | Add-Member -NotePropertyName "hooks" -NotePropertyValue ([PSCustomObject]@{}) -Force
}
if (-not $settings.hooks.Stop) {
    $settings.hooks | Add-Member -NotePropertyName "Stop" -NotePropertyValue @() -Force
}

# Stop hook 結構：[{matcher:"", hooks:[{command:"...", type:"command"}]}]
$stopArr = @($settings.hooks.Stop)
$targetGroup = $null
foreach ($g in $stopArr) {
    if ($null -eq $g.matcher -or $g.matcher -eq "") {
        $targetGroup = $g; break
    }
}
if ($null -eq $targetGroup) {
    $targetGroup = [PSCustomObject]@{ matcher = ""; hooks = @() }
    $stopArr += $targetGroup
}

# 構造要註冊的 hook command（PowerShell 包裝）
$psCmd = "powershell -ExecutionPolicy Bypass -File `"$hookScript`""

# 去重
$existing = @($targetGroup.hooks) | Where-Object { $_.command -eq $psCmd }
if ($existing) {
    Write-Host "ℹ️ Stop hook 已註冊過，無需重複安裝。" -ForegroundColor Cyan
} else {
    $newHook = [PSCustomObject]@{ command = $psCmd; type = "command" }
    $targetGroup.hooks = @($targetGroup.hooks) + $newHook
    $settings.hooks.Stop = @($stopArr)

    # 寫回（UTF-8 with BOM 不然 Claude Code 可能讀錯）
    $json = $settings | ConvertTo-Json -Depth 10
    [System.IO.File]::WriteAllText($settingsPath, $json, [System.Text.UTF8Encoding]::new($true))

    Write-Host "✅ Windows session-end auto-push hook 已註冊到：$settingsPath" -ForegroundColor Green
}

# ───────── 4. 驗證註冊狀態 ─────────
Write-Host ""
Write-Host "📋 當前 Stop hook 清單：" -ForegroundColor Cyan
$verify = Get-Content -Path $settingsPath -Encoding UTF8 -Raw | ConvertFrom-Json
foreach ($g in @($verify.hooks.Stop)) {
    foreach ($h in @($g.hooks)) {
        Write-Host "  - $($h.command)"
    }
}

Write-Host ""
Write-Host "🎯 下一場 Windows session 結束時，會自動：" -ForegroundColor Yellow
Write-Host "   1. 偵測接力棒/memory/HEARTBEAT/knowledges 是否變動"
Write-Host "   2. 自動 git add + commit + push origin main"
Write-Host "   3. Mac 軍師下次 cron 或 git pull 就拿到 Windows 進度"
Write-Host ""
Write-Host "✅ 安裝完成，教練可以關掉視窗。" -ForegroundColor Green
