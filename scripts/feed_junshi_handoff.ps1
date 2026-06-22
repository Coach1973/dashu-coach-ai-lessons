# Hook: UserPromptSubmit (Windows PowerShell 版 · v2 雲端優先)
# 用途: 教練在 Windows 桌面版 Claude Code 喊「開」「開工」等暗號時，
#       自動 git pull 拉雲端最新接力棒 → 注入 context。
#
# 設計核心（v2 教練 2026-06-18 親定）：
#   - 完全不依賴本機 workspace 預先存在
#   - 完全不碰 E 槽（教練 E 槽在修復）
#   - 固定用 %USERPROFILE%\.openclaw\workspace 當 cache
#   - workspace 不存在 → 自動 git clone（一次性）
#   - workspace 存在 → git pull --quiet 永遠拉雲端最新（不會過期）
#
# 對應 Mac 版: feed_junshi_handoff.sh

$ErrorActionPreference = 'Continue'

# ───────── 雲端真相源（固定，不需動）─────────
$REPO_URL  = "https://github.com/Coach1973/mac-openclaw-workflows.git"

# ───────── workspace 位置（v3.1 教練親定：對齊既有 E:\Claude-Data）─────────
# 優先序：
#   1. $env:JUNSHI_HOOK_ROOT 環境變數（由 install 腳本永久設定）
#   2. E:\Claude-Data\workspace（教練既有 Claude-Data 目錄結構）
#   3. E:\junshi-hook\workspace（fallback 若 Claude-Data 不存在）
#   4. C 槽（最後手段，會被一鍵還原洗掉）
if ($env:JUNSHI_HOOK_ROOT) {
    $workspace = Join-Path $env:JUNSHI_HOOK_ROOT "workspace"
} elseif (Test-Path "E:\Claude-Data") {
    $workspace = "E:\Claude-Data\workspace"
} elseif (Test-Path "E:\") {
    $workspace = "E:\junshi-hook\workspace"
} else {
    $workspace = Join-Path $env:USERPROFILE ".openclaw\workspace"
}

$handoff       = Join-Path $workspace "JUNSHI_HANDOFF_LATEST.md"
$identityCard  = Join-Path $workspace "knowledges\IDENTITY_windows_desktop.md"
$sessionDump   = Join-Path $workspace "claude-sessions"
$heartbeatPath = Join-Path $workspace "HEARTBEAT.md"

# ───────── 讀 stdin JSON ─────────
$raw = [Console]::In.ReadToEnd()
try { $payload = $raw | ConvertFrom-Json -ErrorAction Stop } catch { exit 0 }

$sessionId = if ($payload.session_id) { [string]$payload.session_id } else { "" }
$prompt    = if ($payload.prompt)     { [string]$payload.prompt }     else { "" }
if ([string]::IsNullOrWhiteSpace($prompt)) { exit 0 }

# ───────── Marker（同 session 只餵一次）─────────
$markerDir = Join-Path $env:TEMP "junshi_markers"
if (-not (Test-Path $markerDir)) { New-Item -ItemType Directory -Path $markerDir -Force | Out-Null }
$marker = Join-Path $markerDir "fed_$sessionId"

# ───────── 觸發詞偵測 ─────────
$forceRefeed = $false
if ($prompt -match '^[\s]*開工[\s。！!]*$' -or $prompt -match '開工了' -or $prompt -match '開工幹活') {
    $forceRefeed = $true
}
$triggerPattern = '^[\s]*(開|開工|工作|幹活|開始工作)[\s。！!]*$|軍師|接續指揮所|JunShi|junshi|Claude\s*軍師'
$triggered = ($prompt -match $triggerPattern) -or $forceRefeed
if (-not $triggered) { exit 0 }

if ((-not $forceRefeed) -and $sessionId -and (Test-Path $marker)) { exit 0 }

# ───────── 🌐 雲端優先：先確保 workspace 是最新版 ─────────
$pullStatus = ""
try {
    if (-not (Test-Path $workspace)) {
        # 首次：自動 clone 雲端 repo 到固定位置（用 git credential，不問 token）
        $parentDir = Split-Path $workspace -Parent
        if (-not (Test-Path $parentDir)) { New-Item -ItemType Directory -Path $parentDir -Force | Out-Null }
        $cloneResult = & git clone --quiet $REPO_URL $workspace 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pullStatus = "✅ 首次 clone 雲端 repo 成功"
        } else {
            $pullStatus = "❌ Clone 失敗: $cloneResult"
        }
    } else {
        # 已存在：git pull 拉雲端最新（每次「開工」都拉，保證永遠不過期）
        # 2026-06-22 修：HEARTBEAT.md/log 類經常被 hook 寫入會卡 pull，先 stash 包裝再 pop
        $dirty = & git -C $workspace status --porcelain 2>$null
        $stashed = $false
        if ($dirty) {
            & git -C $workspace stash push -u -m "auto-pull-stash-$(Get-Date -Format yyyyMMddHHmmss)" --quiet 2>$null | Out-Null
            if ($LASTEXITCODE -eq 0) { $stashed = $true }
        }
        $pullResult = & git -C $workspace pull --quiet --rebase 2>&1
        $pullOk = ($LASTEXITCODE -eq 0)
        if ($stashed) {
            & git -C $workspace stash pop --quiet 2>$null | Out-Null
        }
        if ($pullOk) {
            $headHash = (& git -C $workspace rev-parse --short HEAD 2>&1).Trim()
            $pullStatus = "✅ 已拉雲端最新（HEAD: $headHash$(if($stashed){'，本地改動已 stash/pop'}else{''})）"
        } else {
            $pullStatus = "⚠️ Pull 警告: $pullResult"
        }
    }
} catch {
    $pullStatus = "❌ Git 操作失敗: $_"
}

# ───────── 接力棒不存在 → 印雲端狀態給教練看 ─────────
if (-not (Test-Path $handoff)) {
    Write-Output "# ⚠️ 軍師接力棒從雲端拉不下來"
    Write-Output ""
    Write-Output "雲端狀態：$pullStatus"
    Write-Output ""
    Write-Output "預期位置：$handoff"
    Write-Output ""
    Write-Output "可能原因："
    Write-Output "- GitHub credential 失效（請跑 ``gh auth login`` 重新登入）"
    Write-Output "- 網路問題"
    Write-Output "- repo URL 變更（目前指向：$REPO_URL）"
    exit 0
}

# ───────── 找最新 SESSION 總結 ─────────
$latestSession = $null
if (Test-Path $sessionDump) {
    $latestSession = Get-ChildItem -Path $sessionDump -Filter "SESSION_*.md" -ErrorAction SilentlyContinue |
                     Sort-Object Name | Select-Object -Last 1
}

# ───────── 輸出注入內容 ─────────
Write-Output "# 🔴 軍師接力棒（系統自動注入，本場 session 僅注入一次）"
Write-Output ""
Write-Output "## 🌐 雲端同步狀態（v2 設計：每次「開工」自動 git pull）"
Write-Output ""
Write-Output "- $pullStatus"
Write-Output "- 來源：$REPO_URL"
Write-Output "- 本機 cache：$workspace（**E 槽不被一鍵還原洗掉**，C 槽 settings.json 失效後可一鍵重建）"
Write-Output ""
Write-Output "## 🪪 身份硬性告知（教練 2026-06-17 親口定稿）"
Write-Output ""
Write-Output "- **平台**：Windows 桌面版（GUI App，非終端機 CLI）"
Write-Output "- **軟體**：Claude Code Desktop App for Windows"
Write-Output "- **工具能力**：✅ 跟 Mac CLI / 終端機 **完全同等**——Bash、Read、Edit、Write、TaskCreate、Agent、Skill 全部都有"
Write-Output "- **底層 shell**：Bash 工具在 Windows 跑 PowerShell（不是 macOS bash），語法要對應"
Write-Output "- **工作目錄**：``\`$env:USERPROFILE\.openclaw\workspace``（**不是 E 槽**）"
Write-Output "- **身份等級**：軍師（Opus），跟 Mac 軍師同等發言權"
Write-Output "- **稱呼教練**：**大樹教練**"
Write-Output "- **commit 前綴**：``[Win]``（區分 Mac 軍師的 ``[Mac]``）"
Write-Output ""
Write-Output "🔴 **三件最容易搞錯的事**："
Write-Output "1. **「我是桌面版，沒有 shell」← 錯**。你有完整 Bash/Read/Edit/Write 工具，能力同 CLI。"
Write-Output "2. **「我是 Mac 環境」← 錯**。路徑 ``/tmp/`` → ``\`$env:TEMP``；指令 ``open -a Chrome`` → ``Start-Process chrome.exe``。"
Write-Output "3. **跨 shell 跳脫災難（案例 24，636 GB 學費）**——危險指令一律走 ``scripts\delete_guard.ps1`` 的 ``Safe-Remove``，**禁止直接寫 ``Remove-Item -Recurse -Force``**。"
Write-Output ""
Write-Output "📖 **完整身份卡 + 網頁推 SOP Mac↔Windows 對照表**：``knowledges\IDENTITY_windows_desktop.md`` ——本場必讀。"
Write-Output ""
Write-Output "---"
Write-Output ""
Write-Output "教練說「開工/開/工作/幹活」=暗號觸發。讀完本段即可無縫接續。"
Write-Output ""
Write-Output "## 📜 JUNSHI_HANDOFF_LATEST.md 完整內容（剛從雲端拉的）"
Write-Output ""
Get-Content -Path $handoff -Encoding UTF8 | ForEach-Object { Write-Output $_ }

if ($latestSession) {
    Write-Output ""
    Write-Output "---"
    Write-Output ""
    Write-Output "## 📂 最新一場 session 總結（$($latestSession.Name)）"
    Write-Output ""
    Get-Content -Path $latestSession.FullName -Encoding UTF8 | ForEach-Object { Write-Output $_ }
}

Write-Output ""
Write-Output "---"
Write-Output ""
Write-Output "## ✅ 上線回應要求"
Write-Output "讀完本段後，第一句回應**必須**包含："
Write-Output "- 「我已讀完接力棒」字樣"
Write-Output "- 雲端同步 HEAD hash 前 7 碼"
Write-Output "- 當下主軸名稱（從 JUNSHI_HANDOFF_LATEST.md「本棒主軸」段挑最優先一條）"
Write-Output "- 身份核對（模型版本 + 平台：Windows 桌面版 GUI）"
Write-Output ""

# 寫 self-test 到 HEARTBEAT（如果存在）
if (Test-Path $heartbeatPath) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm"
    $triggerPreview = if ($prompt.Length -gt 40) { $prompt.Substring(0, 40) } else { $prompt }
    $selfTest = @"

## 🩺 軍師 Hook 自檢 $ts（Windows v2 雲端優先）
- ✅ Hook 觸發 + git pull 完成
- 觸發詞：$triggerPreview
- 雲端狀態：$pullStatus
- Session: $sessionId
"@
    try { Add-Content -Path $heartbeatPath -Value $selfTest -Encoding UTF8 } catch {}
}

if ($sessionId) { New-Item -ItemType File -Path $marker -Force | Out-Null }
exit 0
