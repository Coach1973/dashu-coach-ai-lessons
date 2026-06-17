# 全自動診斷 + 徹底修復 Windows 桌面版 Claude Code 開工 hook
# 適用情境：跑了 install_windows_hook.ps1 顯示「已註冊跳過」，但實際打「開工」毫無反應
# 根因：E 槽 636 GB 蒸發災難後，舊 hook 路徑指向已不存在的腳本，silent fail
# 教練暗號：「徹底修 Windows hook」

$ErrorActionPreference = 'Stop'
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔍 Windows 軍師 hook 診斷 + 徹底修復" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# ───────── 1. 找 workspace 真實位置 ─────────
Write-Host "`n[1/7] 找 workspace 真實位置..." -ForegroundColor Yellow
$candidates = @(
    $env:OPENCLAW_WORKSPACE,
    (Join-Path $env:USERPROFILE ".openclaw\workspace"),
    "C:\Users\$env:USERNAME\.openclaw\workspace",
    "E:\Claude-Data\.openclaw\workspace",
    "E:\.openclaw\workspace",
    "D:\.openclaw\workspace"
) | Where-Object { $_ -and (Test-Path (Join-Path $_ "JUNSHI_HANDOFF_LATEST.md")) }

if (-not $candidates) {
    Write-Host "  ❌ 找不到任何含 JUNSHI_HANDOFF_LATEST.md 的 workspace" -ForegroundColor Red
    Write-Host "  請先 git clone 到 `$env:USERPROFILE\.openclaw\workspace" -ForegroundColor Yellow
    exit 1
}
$workspace = $candidates[0]
$hookScript = Join-Path $workspace "scripts\feed_junshi_handoff.ps1"
Write-Host "  ✅ Workspace: $workspace" -ForegroundColor Green
Write-Host "  ✅ Hook 腳本: $hookScript" -ForegroundColor Green

if (-not (Test-Path $hookScript)) {
    Write-Host "  ❌ feed_junshi_handoff.ps1 不存在！請 git pull" -ForegroundColor Red
    exit 1
}

# ───────── 2. 列出現有 settings.json 內容 ─────────
Write-Host "`n[2/7] 檢查現有 settings.json..." -ForegroundColor Yellow
$settingsFile = Join-Path $env:USERPROFILE ".claude\settings.json"
if (-not (Test-Path $settingsFile)) {
    Write-Host "  📝 settings.json 不存在，建新檔" -ForegroundColor Cyan
    $settings = [PSCustomObject]@{}
} else {
    $backup = "$settingsFile.bak.diagfix.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item $settingsFile $backup -Force
    Write-Host "  💾 備份: $backup" -ForegroundColor Cyan
    $settings = Get-Content $settingsFile -Raw -Encoding UTF8 | ConvertFrom-Json
}

# ───────── 3. 掃描所有 hook 註冊，找出壞掉的舊註冊 ─────────
Write-Host "`n[3/7] 掃描舊 hook 註冊..." -ForegroundColor Yellow
$brokenHooks = @()
$validHooks  = @()

if ($settings.PSObject.Properties['hooks'] -and $settings.hooks.PSObject.Properties['UserPromptSubmit']) {
    foreach ($entry in $settings.hooks.UserPromptSubmit) {
        foreach ($h in $entry.hooks) {
            if ($h.command -match "feed_junshi_handoff\.ps1") {
                # 取出 -File 後的路徑
                if ($h.command -match '-File\s+"([^"]+)"') {
                    $registeredPath = $matches[1]
                } elseif ($h.command -match '-File\s+(\S+)') {
                    $registeredPath = $matches[1]
                } else {
                    $registeredPath = "(無法解析)"
                }

                if (Test-Path $registeredPath) {
                    $validHooks += $registeredPath
                    Write-Host "  ✅ 有效: $registeredPath" -ForegroundColor Green
                } else {
                    $brokenHooks += $registeredPath
                    Write-Host "  ❌ 壞掉（檔案不存在）: $registeredPath" -ForegroundColor Red
                }
            }
        }
    }
}

if ($brokenHooks.Count -eq 0 -and $validHooks.Count -eq 0) {
    Write-Host "  ℹ️  沒有任何 feed_junshi_handoff.ps1 註冊（全新安裝）" -ForegroundColor Cyan
}

# ───────── 4. 重建 hooks.UserPromptSubmit：清掉所有 feed_junshi_handoff 註冊，重新寫一份 ─────────
Write-Host "`n[4/7] 清除壞掉/舊註冊，重建 hook..." -ForegroundColor Yellow

if (-not $settings.PSObject.Properties['hooks']) {
    $settings | Add-Member -NotePropertyName hooks -NotePropertyValue ([PSCustomObject]@{}) -Force
}
if (-not $settings.hooks.PSObject.Properties['UserPromptSubmit']) {
    $settings.hooks | Add-Member -NotePropertyName UserPromptSubmit -NotePropertyValue @() -Force
}

# 過濾掉所有 feed_junshi_handoff 相關 entry（會用乾淨新版重新加）
$cleanedEntries = @()
foreach ($entry in $settings.hooks.UserPromptSubmit) {
    $remainingHooks = @($entry.hooks | Where-Object { $_.command -notmatch "feed_junshi_handoff\.ps1" })
    if ($remainingHooks.Count -gt 0) {
        $entry.hooks = $remainingHooks
        $cleanedEntries += $entry
    }
}

# 加入乾淨的新 entry
$hookCmd = "powershell.exe -ExecutionPolicy Bypass -File `"$hookScript`""
$newEntry = [PSCustomObject]@{
    matcher = ""
    hooks   = @([PSCustomObject]@{
        type    = "command"
        command = $hookCmd
    })
}
$cleanedEntries += $newEntry
$settings.hooks.UserPromptSubmit = $cleanedEntries

Write-Host "  ✅ 已清除 $($brokenHooks.Count) 個壞掉註冊" -ForegroundColor Green
Write-Host "  ✅ 已重新註冊指向: $hookScript" -ForegroundColor Green

# ───────── 5. 寫回 settings.json ─────────
Write-Host "`n[5/7] 寫回 settings.json..." -ForegroundColor Yellow
$settingsDir = Split-Path $settingsFile -Parent
if (-not (Test-Path $settingsDir)) { New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null }
$json = $settings | ConvertTo-Json -Depth 10
# 寫成 UTF-8 with BOM（避免 PowerShell 5.1 讀取 emoji 崩潰）
$utf8Bom = New-Object System.Text.UTF8Encoding $true
[System.IO.File]::WriteAllText($settingsFile, $json, $utf8Bom)
Write-Host "  ✅ 已寫入 $settingsFile（UTF-8 with BOM）" -ForegroundColor Green

# ───────── 6. Self-test（真的跑一次 hook 看注入內容）─────────
Write-Host "`n[6/7] Self-test（模擬教練說「開工」）..." -ForegroundColor Yellow
$testPayload = @{ session_id = "diagfix-$(Get-Date -Format 'HHmmss')"; prompt = "開工" } | ConvertTo-Json -Compress
$testOutput  = $testPayload | & powershell.exe -ExecutionPolicy Bypass -File $hookScript 2>&1
$firstLines  = ($testOutput -split "`n" | Select-Object -First 5) -join "`n"

if ($testOutput -match "軍師接力棒") {
    Write-Host "  ✅ Self-test 通過——hook 收到「開工」會注入接力棒" -ForegroundColor Green
    Write-Host "  注入第一行: $($testOutput -split "`n" | Select-Object -First 1)" -ForegroundColor DarkGray
} else {
    Write-Host "  ⚠️  Self-test 異常，輸出前 5 行：" -ForegroundColor Yellow
    Write-Host $firstLines -ForegroundColor DarkGray
}

# ───────── 7. 最終診斷報告 ─────────
Write-Host "`n[7/7] 最終診斷報告" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ workspace 真實位置: $workspace" -ForegroundColor Green
Write-Host "✅ hook 腳本: $hookScript ($(if(Test-Path $hookScript){'存在'}else{'❌不存在'}))" -ForegroundColor Green
Write-Host "✅ settings.json: $settingsFile" -ForegroundColor Green
Write-Host "✅ 清除壞掉舊註冊: $($brokenHooks.Count) 個" -ForegroundColor Green
Write-Host "✅ 重新註冊: 1 個（指向上述存在的腳本）" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔴 關鍵下一步：" -ForegroundColor Red
Write-Host "  Claude Code 啟動時讀 settings.json，所以必須【完全關閉重開】才會載入新的 hook 路徑。" -ForegroundColor Yellow
Write-Host "  在當前 session 打「開工」不會有反應，這正常——hook 是啟動時 register 的。" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. 完全關閉 Claude Code（不是隱藏視窗——是退出進程）" -ForegroundColor White
Write-Host "  2. 確認 cwd：開啟時切到 workspace 目錄，不要從 E:\ 開（E 槽被清光，沒 CLAUDE.md）" -ForegroundColor White
Write-Host "     建議：cd $workspace ; 然後啟動 Claude Code" -ForegroundColor White
Write-Host "  3. 開新對話打「開工」——應該會看到接力棒自動注入" -ForegroundColor White
Write-Host ""
Write-Host "回報 Mac 軍師：把上面整段【最終診斷報告】貼過去就完成驗證" -ForegroundColor Cyan
