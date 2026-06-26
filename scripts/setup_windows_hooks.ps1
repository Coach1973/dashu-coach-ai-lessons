#!/usr/bin/env pwsh
# ============================================================
# setup_windows_hooks.ps1 — Windows 一鍵對齊（聯想/ACER 通用）
#
# 讓 Windows 機器的 Claude 開工體驗跟 Mac 完全一致。
# 教練只要說一句「git pull，然後跑 scripts/setup_windows_hooks.ps1」
#
# 做四件事：
#   1. 偵測機器（聯想/ACER）+ 找 repo 路徑
#   2. 設環境變數（AGENT_INBOX_NAME / JUNSHI_HOOK_ROOT）
#   3. 把所有 hook 一次性寫進 settings.json
#   4. 自測
#
# 2026-06-26 Mac 終端機軍師 Opus 4.6 建立
# ============================================================

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Windows Hook 一鍵對齊（Mac 同步版）" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ───────── 1. 偵測機器 + 找 repo ─────────

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent $ScriptDir
$Workspace = $RepoRoot

# 偵測機器名（用電腦名稱 + 已設環境變數判斷）
$computerName = $env:COMPUTERNAME
$existingName = $env:AGENT_INBOX_NAME

if ($existingName) {
    $machineName = $existingName
    Write-Host "[1/4] 機器名偵測：$machineName（已有環境變數）" -ForegroundColor Green
} elseif ($computerName -match 'LENOVO|THINK') {
    $machineName = "lenovo"
    Write-Host "[1/4] 機器名偵測：lenovo（依電腦名稱 $computerName）" -ForegroundColor Green
} elseif ($computerName -match 'ACER') {
    $machineName = "acer"
    Write-Host "[1/4] 機器名偵測：acer（依電腦名稱 $computerName）" -ForegroundColor Green
} else {
    Write-Host "[1/4] 無法自動偵測機器名（電腦名稱：$computerName）" -ForegroundColor Yellow
    Write-Host "  請輸入你的機器名（lenovo / acer）：" -ForegroundColor Yellow -NoNewline
    $machineName = Read-Host
    if ($machineName -notin @('lenovo', 'acer')) {
        Write-Host "  不認得的名字，預設用 '$machineName'" -ForegroundColor Yellow
    }
}

Write-Host "  Repo 路徑：$RepoRoot" -ForegroundColor Gray
Write-Host "  Scripts 路徑：$ScriptDir" -ForegroundColor Gray
Write-Host ""

# ───────── 2. 設環境變數 ─────────

Write-Host "[2/4] 設定環境變數..." -ForegroundColor Cyan

# AGENT_INBOX_NAME
$currentInbox = [Environment]::GetEnvironmentVariable("AGENT_INBOX_NAME", "User")
if ($currentInbox -ne $machineName) {
    [Environment]::SetEnvironmentVariable("AGENT_INBOX_NAME", $machineName, "User")
    $env:AGENT_INBOX_NAME = $machineName
    Write-Host "  AGENT_INBOX_NAME = $machineName（已設定）" -ForegroundColor Green
} else {
    Write-Host "  AGENT_INBOX_NAME = $machineName（已存在，跳過）" -ForegroundColor Gray
}

# JUNSHI_HOOK_ROOT（指向 repo 上一層，讓 feed_junshi_handoff.ps1 能找到 workspace）
$repoParent = Split-Path -Parent $RepoRoot
$currentRoot = [Environment]::GetEnvironmentVariable("JUNSHI_HOOK_ROOT", "User")

# 判斷 repo 結構：如果 repo 本身就是 workspace（裡面有 JUNSHI_HANDOFF_LATEST.md）
if (Test-Path (Join-Path $RepoRoot "JUNSHI_HANDOFF_LATEST.md")) {
    $hookRoot = $repoParent
} else {
    $hookRoot = $RepoRoot
}

if ($currentRoot -ne $hookRoot) {
    [Environment]::SetEnvironmentVariable("JUNSHI_HOOK_ROOT", $hookRoot, "User")
    $env:JUNSHI_HOOK_ROOT = $hookRoot
    Write-Host "  JUNSHI_HOOK_ROOT = $hookRoot（已設定）" -ForegroundColor Green
} else {
    Write-Host "  JUNSHI_HOOK_ROOT = $hookRoot（已存在，跳過）" -ForegroundColor Gray
}

Write-Host ""

# ───────── 3. 寫入 settings.json ─────────

Write-Host "[3/4] 對齊 Claude hooks（settings.json）..." -ForegroundColor Cyan

$settingsPath = Join-Path $env:USERPROFILE ".claude\settings.json"
$settingsDir  = Split-Path -Parent $settingsPath

if (-not (Test-Path $settingsDir)) {
    New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
}

# 讀現有 settings（或建空的）
$settings = @{}
if (Test-Path $settingsPath) {
    try {
        $settings = Get-Content $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable
    } catch {
        $backupPath = "$settingsPath.bak.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item $settingsPath $backupPath
        Write-Host "  原 settings.json 格式錯誤，已備份到 $backupPath" -ForegroundColor Yellow
        $settings = @{}
    }
}

# 用反斜線路徑（Windows 標準）
$escapedScriptDir = $ScriptDir -replace '\\', '\\'

# 定義所有要掛的 hook（對齊 Mac 版）
$pwshPrefix = "powershell -NoProfile -ExecutionPolicy Bypass -File"

$userPromptHooks = @(
    @{ command = "$pwshPrefix `"$ScriptDir\inject_taiwan_time.ps1`""; type = "command" },
    @{ command = "$pwshPrefix `"$ScriptDir\session_time_context.ps1`""; type = "command" },
    @{ command = "$pwshPrefix `"$ScriptDir\feed_junshi_handoff.ps1`""; type = "command" },
    @{ command = "$pwshPrefix `"$ScriptDir\scan_cross_agent_inbox.ps1`""; type = "command" }
)

$preToolUseHooks = @(
    @{
        matcher = "Bash"
        hooks = @(
            @{ command = "$pwshPrefix `"$ScriptDir\delete_guard_hook.ps1`""; type = "command" }
        )
    }
)

$stopHooks = @(
    @{ command = "$pwshPrefix `"$ScriptDir\session_end_auto_push.ps1`""; type = "command" }
)

# 建構完整 hooks 結構
$newHooks = @{
    UserPromptSubmit = @(
        @{
            hooks   = $userPromptHooks
            matcher = ""
        }
    )
    PreToolUse = $preToolUseHooks
    Stop = @(
        @{
            hooks   = $stopHooks
            matcher = ""
        }
    )
}

# 寫入（保留 settings 裡 hooks 以外的設定）
if (-not $settings.ContainsKey('hooks')) {
    $settings['hooks'] = @{}
}
$settings['hooks'] = $newHooks

# 備份後寫入
if (Test-Path $settingsPath) {
    $backupPath = "$settingsPath.bak.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $settingsPath $backupPath
    Write-Host "  原 settings.json 已備份：$backupPath" -ForegroundColor Gray
}

$jsonOutput = $settings | ConvertTo-Json -Depth 10
# 確保 UTF-8 with BOM（Windows PowerShell 預設 + 案例 25 慣例）
[System.IO.File]::WriteAllText($settingsPath, $jsonOutput, [System.Text.UTF8Encoding]::new($true))

# 列出已安裝的 hook
Write-Host ""
Write-Host "  已安裝 hook 清單：" -ForegroundColor Green
Write-Host "  ── UserPromptSubmit（教練每說一句話就跑）──" -ForegroundColor White
Write-Host "    1. inject_taiwan_time.ps1    台灣時間鐵律" -ForegroundColor Gray
Write-Host "    2. session_time_context.ps1  Session 時間覺察" -ForegroundColor Gray
Write-Host "    3. feed_junshi_handoff.ps1   開工六步驟全注入（接力棒）" -ForegroundColor Gray
Write-Host "    4. scan_cross_agent_inbox.ps1 跨機信箱掃描" -ForegroundColor Gray
Write-Host "  ── PreToolUse（執行指令前攔截）──" -ForegroundColor White
Write-Host "    5. delete_guard_hook.ps1     刪除防護鎖" -ForegroundColor Gray
Write-Host "  ── Stop（Session 結束時）──" -ForegroundColor White
Write-Host "    6. session_end_auto_push.ps1 自動 git push 同步" -ForegroundColor Gray
Write-Host ""

# ───────── 4. 自測 ─────────

Write-Host "[4/4] 自測..." -ForegroundColor Cyan

$allPass = $true

# 檢查每個 .ps1 是否存在
$scripts = @(
    "inject_taiwan_time.ps1",
    "session_time_context.ps1",
    "feed_junshi_handoff.ps1",
    "scan_cross_agent_inbox.ps1",
    "delete_guard_hook.ps1",
    "session_end_auto_push.ps1"
)

foreach ($s in $scripts) {
    $p = Join-Path $ScriptDir $s
    if (Test-Path $p) {
        Write-Host "  ✅ $s" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $s（檔案不存在！）" -ForegroundColor Red
        $allPass = $false
    }
}

# 檢查 settings.json 寫入成功
if (Test-Path $settingsPath) {
    try {
        $verify = Get-Content $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $hookCount = 0
        if ($verify.hooks.UserPromptSubmit) { $hookCount += $verify.hooks.UserPromptSubmit[0].hooks.Count }
        if ($verify.hooks.PreToolUse)       { $hookCount += $verify.hooks.PreToolUse[0].hooks.Count }
        if ($verify.hooks.Stop)             { $hookCount += $verify.hooks.Stop[0].hooks.Count }
        Write-Host "  ✅ settings.json 已寫入（$hookCount 個 hook）" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ settings.json 格式驗證失敗" -ForegroundColor Red
        $allPass = $false
    }
} else {
    Write-Host "  ❌ settings.json 不存在" -ForegroundColor Red
    $allPass = $false
}

# 檢查環境變數
if ($env:AGENT_INBOX_NAME) {
    Write-Host "  ✅ AGENT_INBOX_NAME = $env:AGENT_INBOX_NAME" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ AGENT_INBOX_NAME 需重開 PowerShell 才生效" -ForegroundColor Yellow
}

Write-Host ""

if ($allPass) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  全部完成！重開 Claude 就生效。" -ForegroundColor Green
    Write-Host "  下次開工會跟 Mac 一樣自動注入。" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  部分項目有問題，請檢查上面的 ❌" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
}

Write-Host ""
