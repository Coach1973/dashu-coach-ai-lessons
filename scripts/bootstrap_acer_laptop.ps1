# Bootstrap ACER 筆電軍師據點（v1）
#
# 用途：教練在 ACER 外出筆電一鍵建立軍師據點——裝 git credential、clone workspace 到 D 槽、註冊 hook。
# 適用：教練本人的 ACER 筆電（只有 C+D 槽），不適用助理筆電。
# 不適用情境：助理筆電（一次性任務用 gist 繞道即可）、Mac、聯想 Windows（已建設好）。
#
# 觸發方式（教練動嘴）：
#   1. ACER 上開 PowerShell，跑：iwr "https://gist.githubusercontent.com/<待補>/raw/bootstrap_acer_laptop.ps1" -OutFile $env:TEMP\bootstrap.ps1 ; powershell -ExecutionPolicy Bypass -File $env:TEMP\bootstrap.ps1
#   2. 或：ACER 已有 Claude CLI，動嘴叫軍師「執行 ACER bootstrap」
#
# 設計原則：
#   - workspace 強制在 D 槽（避開 C 槽一鍵還原）
#   - 不在 C 槽留任何 Claude 相關檔案（除了 user-level settings.json 必要）
#   - 每階段獨立呼叫（不合併，案例 27 教訓）
#   - 失敗時詳細回報，不靜默吞錯

$ErrorActionPreference = 'Stop'
$REPO_URL = "https://github.com/Coach1973/mac-openclaw-workflows.git"
$WORKSPACE = "D:\Claude-Data\workspace"

Write-Host "=== ACER 軍師據點 Bootstrap v1 ===" -ForegroundColor Cyan
Write-Host ""

# ───────── 階段 1：環境檢查 ─────────
Write-Host "[階段 1] 環境檢查..." -ForegroundColor Yellow

# D 槽存在嗎
if (-not (Test-Path "D:\")) {
    Write-Host "❌ D 槽不存在，無法在 D 建立 workspace。請先確認硬碟分割。" -ForegroundColor Red
    exit 1
}
$dFree = (Get-PSDrive D).Free / 1GB
Write-Host "  ✅ D 槽剩餘：$([math]::Round($dFree,1)) GB"

# git 裝了嗎
$gitVer = & git --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ⚠️ git 未安裝。請先裝 Git for Windows: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "     或用 winget: winget install Git.Git" -ForegroundColor Yellow
    exit 1
}
Write-Host "  ✅ $gitVer"

# gh CLI 裝了嗎（建議但非必需）
$ghVer = & gh --version 2>$null | Select-Object -First 1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ⚠️ gh CLI 未安裝（建議裝以方便 auth login）: winget install GitHub.cli" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ $ghVer"
}

Write-Host ""

# ───────── 階段 2：GitHub credential ─────────
Write-Host "[階段 2] GitHub credential 確認..." -ForegroundColor Yellow

$authOk = $false
try {
    $authStatus = & gh auth status 2>&1 | Out-String
    if ($authStatus -match 'Logged in to github.com') {
        $authOk = $true
        Write-Host "  ✅ gh 已登入"
    }
} catch {}

if (-not $authOk) {
    Write-Host "  ⚠️ 需要 GitHub credential（repo 是 private）" -ForegroundColor Yellow
    Write-Host "     請手動執行：gh auth login" -ForegroundColor Yellow
    Write-Host "     完成後重跑本 bootstrap。" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "     或：暫時跳過 credential（用 gist 拉單檔 SOP，不 clone 整個 repo）" -ForegroundColor Gray
    $choice = Read-Host "     現在去登入嗎？(y/n)"
    if ($choice -eq 'y') {
        & gh auth login
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ 登入失敗，請手動處理" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "  ⏭️ 跳過 credential，bootstrap 中止。需要時再重跑。" -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""

# ───────── 階段 3：建 workspace + clone repo ─────────
Write-Host "[階段 3] 建立 D 槽 workspace + clone repo..." -ForegroundColor Yellow

$wsParent = Split-Path $WORKSPACE -Parent
if (-not (Test-Path $wsParent)) {
    New-Item -ItemType Directory -Path $wsParent -Force | Out-Null
    Write-Host "  ✅ 建立 $wsParent"
}

if (Test-Path $WORKSPACE) {
    Write-Host "  ⚠️ $WORKSPACE 已存在——改用 git pull 更新"
    Push-Location $WORKSPACE
    & git pull --quiet --rebase 2>&1 | Out-Host
    Pop-Location
} else {
    & git clone --quiet $REPO_URL $WORKSPACE 2>&1 | Out-Host
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ git clone 失敗" -ForegroundColor Red
        exit 1
    }
    Write-Host "  ✅ Clone 完成"
}

$headHash = (& git -C $WORKSPACE rev-parse --short HEAD 2>$null).Trim()
Write-Host "  ✅ HEAD: $headHash"

Write-Host ""

# ───────── 階段 4：設環境變數 + 註冊 hook ─────────
Write-Host "[階段 4] 設環境變數 + 註冊 Claude CLI hook..." -ForegroundColor Yellow

# 持久化 JUNSHI_HOOK_ROOT（user-level）
[Environment]::SetEnvironmentVariable("JUNSHI_HOOK_ROOT", "D:\Claude-Data", "User")
$env:JUNSHI_HOOK_ROOT = "D:\Claude-Data"
Write-Host "  ✅ JUNSHI_HOOK_ROOT=D:\Claude-Data（user-level，永久）"

# 確保 ~/.claude 存在
$claudeDir = Join-Path $env:USERPROFILE ".claude"
if (-not (Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Path $claudeDir -Force | Out-Null
}

$settingsPath = Join-Path $claudeDir "settings.json"
$hookScript = "$WORKSPACE\scripts\feed_junshi_handoff.ps1"
$timeScript = "$WORKSPACE\scripts\session_time_context.ps1"

# 讀現有 settings 或建新的
if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath -Encoding UTF8 -Raw | ConvertFrom-Json
    Write-Host "  ✅ 找到現有 settings.json，合併 hooks"
} else {
    $settings = [PSCustomObject]@{}
    Write-Host "  ✅ 建立新 settings.json"
}

# 確保 hooks.UserPromptSubmit 存在
if (-not $settings.PSObject.Properties['hooks']) {
    $settings | Add-Member -MemberType NoteProperty -Name 'hooks' -Value ([PSCustomObject]@{})
}
if (-not $settings.hooks.PSObject.Properties['UserPromptSubmit']) {
    $settings.hooks | Add-Member -MemberType NoteProperty -Name 'UserPromptSubmit' -Value @()
}

# 加入兩個 hook（接力棒 + 時間覺察）
$hookCmds = @(
    @{ command = "powershell -ExecutionPolicy Bypass -File `"$hookScript`""; type = "command" },
    @{ command = "powershell -ExecutionPolicy Bypass -File `"$timeScript`""; type = "command" }
)
$settings.hooks.UserPromptSubmit = @(@{ hooks = $hookCmds })

# 寫回
$settings | ConvertTo-Json -Depth 10 | Set-Content -Path $settingsPath -Encoding UTF8
Write-Host "  ✅ 寫入 $settingsPath"

Write-Host ""

# ───────── 階段 5：Self-test ─────────
Write-Host "[階段 5] Self-test..." -ForegroundColor Yellow

if (-not (Test-Path $hookScript)) {
    Write-Host "  ❌ Hook 腳本不存在：$hookScript" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Hook 腳本存在"

$handoff = Join-Path $WORKSPACE "JUNSHI_HANDOFF_LATEST.md"
if (-not (Test-Path $handoff)) {
    Write-Host "  ❌ 接力棒不存在：$handoff" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ 接力棒可讀"

Write-Host ""
Write-Host "=== Bootstrap 完成 ===" -ForegroundColor Green
Write-Host ""
Write-Host "下一步："
Write-Host "  1. 開 Claude Code 桌面版 App（或 CLI: claude）"
Write-Host "  2. 喊「開工」——hook 會自動拉雲端最新 + 注入六步驟接力棒"
Write-Host "  3. ACER 軍師上線，跟聯想 Windows 軍師同等發言權"
Write-Host ""
Write-Host "若 LINE 也要從 C 搬到 D：" -ForegroundColor Cyan
Write-Host "  讀 $WORKSPACE\knowledges\SOP_line_migrate_to_d_drive.md"
Write-Host ""
