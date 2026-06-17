# Hook: UserPromptSubmit (Windows PowerShell 版)
# 用途: 教練在 Windows 桌面版 Claude Code 新 session 喊「開」「開工」「工作」「幹活」等暗號時，
#       自動把 JUNSHI_HANDOFF_LATEST.md 餵進 context。
# 對應檔: scripts/feed_junshi_handoff.sh (Mac 版)
# 設計: 同 session 只餵一次（marker 防重複）；「開工」可強制重餵。
# 安裝: 由 scripts\install_windows_hook.ps1 自動掛到 %USERPROFILE%\.claude\settings.json

$ErrorActionPreference = 'Continue'

# ───────── 路徑解析 ─────────
# 優先吃環境變數 OPENCLAW_WORKSPACE；沒設就 fallback 到 ~/.openclaw/workspace
$workspace = $env:OPENCLAW_WORKSPACE
if (-not $workspace) {
    $workspace = Join-Path $env:USERPROFILE ".openclaw\workspace"
}
$handoff       = Join-Path $workspace "JUNSHI_HANDOFF_LATEST.md"
$sessionDump   = Join-Path $workspace "claude-sessions"
$heartbeatPath = Join-Path $workspace "HEARTBEAT.md"

# ───────── 讀 stdin JSON ─────────
$raw = [Console]::In.ReadToEnd()
try {
    $payload = $raw | ConvertFrom-Json -ErrorAction Stop
} catch {
    exit 0
}

$sessionId = if ($payload.session_id) { [string]$payload.session_id } else { "" }
$prompt    = if ($payload.prompt)     { [string]$payload.prompt }     else { "" }

if ([string]::IsNullOrWhiteSpace($prompt)) { exit 0 }

# ───────── Marker（同 session 只餵一次）─────────
$markerDir = Join-Path $env:TEMP "junshi_markers"
if (-not (Test-Path $markerDir)) { New-Item -ItemType Directory -Path $markerDir -Force | Out-Null }
$marker = Join-Path $markerDir "fed_$sessionId"

# ───────── 觸發詞偵測 ─────────
# 強制重餵：整句僅「開工」（含全形標點 / 換行 / 空白）→ /clear 後仍可重新觸發
$forceRefeed = $false
if ($prompt -match '^[\s]*開工[\s。！!]*$' -or $prompt -match '開工了' -or $prompt -match '開工幹活') {
    $forceRefeed = $true
}

# 一般暗號：整句只有「開」「開工」「工作」「幹活」單一動詞，或含「軍師」「JunShi」字眼
# 注意：「開」單字易誤觸發（如「打開瀏覽器」），所以僅當整句=「開」才觸發
$triggerPattern = '^[\s]*(開|開工|工作|幹活|開始工作)[\s。！!]*$|軍師|接續指揮所|JunShi|junshi|Claude\s*軍師'
$triggered = ($prompt -match $triggerPattern) -or $forceRefeed

if (-not $triggered) { exit 0 }

# 非強制 + marker 已存在 → 靜默退出（避免每句話都炸 token）
if ((-not $forceRefeed) -and $sessionId -and (Test-Path $marker)) { exit 0 }

# ───────── 注入接力棒 ─────────
if (-not (Test-Path $handoff)) {
    Write-Output "# ⚠️ 軍師接力棒檔案不存在"
    Write-Output ""
    Write-Output "預期路徑：``$handoff``"
    Write-Output "可能原因：workspace 還沒 clone，或 ``OPENCLAW_WORKSPACE`` 環境變數沒設。"
    Write-Output "請執行：``git clone <repo> `$env:USERPROFILE\.openclaw\workspace``"
    exit 0
}

# 找最新一場 SESSION 總結（依檔名排序取最後）
$latestSession = $null
if (Test-Path $sessionDump) {
    $latestSession = Get-ChildItem -Path $sessionDump -Filter "SESSION_*.md" -ErrorAction SilentlyContinue |
                     Sort-Object Name | Select-Object -Last 1
}

# Self-test：寫進 HEARTBEAT 證明 hook 真的被觸發（防假回報）
if (Test-Path $heartbeatPath) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm"
    $triggerPreview = if ($prompt.Length -gt 40) { $prompt.Substring(0, 40) } else { $prompt }
    $selfTest = @"

## 🩺 軍師 Hook 自檢 $ts（Windows）
- ✅ Hook 自檢通過（settings.json 含 hooks.UserPromptSubmit、本 ps1 被觸發）
- 觸發詞：$triggerPreview
- Session: $sessionId
- 平台：Windows PowerShell
"@
    try { Add-Content -Path $heartbeatPath -Value $selfTest -Encoding UTF8 } catch {}
}

# 輸出注入內容（→ Claude Code 會把 stdout 當作 context 注入）
Write-Output "# 🔴 軍師接力棒（系統自動注入，本場 session 僅注入一次）"
Write-Output ""
Write-Output "你是 **Claude 軍師**（Windows 桌面版）。教練說「開工/開/工作/幹活」=暗號觸發。讀完本段即可無縫接續。"
Write-Output ""
Write-Output "## 📜 JUNSHI_HANDOFF_LATEST.md 完整內容"
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
Write-Output "- 當下主軸名稱（從 JUNSHI_HANDOFF_LATEST.md「本棒主軸」段挑最優先一條）"
Write-Output "- 身份核對（模型版本 + 平台：Windows 桌面版）"
Write-Output "- 雲端同步狀態（commit hash 前 7 碼）"
Write-Output ""
Write-Output "## ⚠️ Windows 軍師硬性提醒（案例 24 後新增）"
Write-Output "- 任何 ``Remove-Item -Recurse -Force`` 必須走 ``scripts\delete_guard.ps1`` 的 ``Safe-Remove`` 函式"
Write-Output "- 超過 1 GB 任何身份不得自主刪除"
Write-Output "- 開工六步驟第三步「讀血淚試金石」必讀案例 24（E 槽 636 GB 蒸發）"

# 設 marker（本 session 不再注入）
if ($sessionId) { New-Item -ItemType File -Path $marker -Force | Out-Null }

exit 0
