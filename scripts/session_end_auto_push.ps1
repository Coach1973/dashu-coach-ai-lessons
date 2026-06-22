# Hook: Stop（Windows 桌面版 PowerShell 版）
# 用途: Session 結束時自動把接力棒/記憶/心跳 push 到 GitHub，
#       讓 Mac 軍師下次「開工」/cron 拉取就拿到 Windows 最新進度，教練不當搬運工。
# 對應: scripts/session_end_auto_push.sh（Mac 版）
#
# 設計（v1 教練 2026-06-22 親定 4 件事中的 A 件）：
#   - 只 push 同步相關檔（接力棒、心跳、memory/、knowledges/、試金石/）
#   - 沒實質變動就不 commit（避免 git noise）
#   - 10 秒鎖：同 session 重複 Stop 不重跑
#   - 失敗靜默退出，不阻塞 hook 鏈

$ErrorActionPreference = 'Continue'

# ───────── workspace 位置（與 feed_junshi_handoff.ps1 相同優先序）─────────
if ($env:JUNSHI_HOOK_ROOT) {
    $workspace = Join-Path $env:JUNSHI_HOOK_ROOT "workspace"
} elseif (Test-Path "E:\Claude-Data") {
    $workspace = "E:\Claude-Data\workspace"
} elseif (Test-Path "E:\") {
    $workspace = "E:\junshi-hook\workspace"
} else {
    $workspace = Join-Path $env:USERPROFILE ".openclaw\workspace"
}

if (-not (Test-Path $workspace)) { exit 0 }

# ───────── 10 秒鎖 ─────────
$lockFile = Join-Path $env:TEMP "session_end_push.lock"
if (Test-Path $lockFile) {
    $lockAge = (Get-Date) - (Get-Item $lockFile).LastWriteTime
    if ($lockAge.TotalSeconds -lt 10) { exit 0 }
}
New-Item -ItemType File -Path $lockFile -Force | Out-Null

# ───────── 切到 workspace ─────────
Push-Location $workspace
try {
    # 同步路徑清單
    $syncPaths = @(
        "JUNSHI_HANDOFF_LATEST.md",
        "CLAUDE.md",
        "HEARTBEAT.md",
        "memory/",
        "knowledges/",
        "試金石/"
    )

    # 過濾出真的有變動的路徑（已追蹤的 diff + untracked 新檔）
    $dirty = @()
    foreach ($p in $syncPaths) {
        if (-not (Test-Path $p)) { continue }

        # 已追蹤變動
        & git diff --quiet -- $p 2>$null
        if ($LASTEXITCODE -ne 0) { $dirty += $p; continue }

        # untracked 新檔
        $untracked = & git ls-files --others --exclude-standard -- $p 2>$null
        if ($untracked) { $dirty += $p }
    }

    if ($dirty.Count -eq 0) { exit 0 }

    # stage
    foreach ($p in $dirty) { & git add $p 2>$null }

    # 確認 stage 真有東西
    & git diff --cached --quiet 2>$null
    if ($LASTEXITCODE -eq 0) { exit 0 }

    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $commitMsg = "[Win] session-end 自動同步 $stamp"

    $pushResult = "❓ unknown"
    & git commit -m $commitMsg 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $commitHash = (& git rev-parse --short HEAD 2>$null).Trim()
        & git push origin main 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $pushResult = "✅ pushed $commitHash"
        } else {
            $pushResult = "⚠️ commit $commitHash 本機留底，push 失敗（離線/credential）"
        }
    } else {
        $pushResult = "ℹ️ 沒實質變動"
    }

    # 寫心跳留證
    $hb = Join-Path $workspace "HEARTBEAT.md"
    if (Test-Path $hb) {
        $entry = @"

## 🚀 Session-End 雲端同步 $stamp（Windows）
- $pushResult
- 同步路徑：$($dirty -join ', ')
"@
        try { Add-Content -Path $hb -Value $entry -Encoding UTF8 } catch {}
    }
}
finally {
    Pop-Location
}

exit 0
