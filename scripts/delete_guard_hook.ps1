# ============================================================
# 🗑️🔒 delete_guard_hook.ps1 — Windows PreToolUse 刪檔鎖（真 hook）
#
# 案例 29（2026-06-25 LINE 4GB 永久丟失）後建立。
# 取代 delete_guard.ps1 的 opt-in 函式 Safe-Remove——那是「規矩」，
# AI 不呼叫就等於沒鎖。本檔是「機關」：註冊成 PreToolUse hook 後，
# AI 打任何指令都先過這關，攔得住 Remove-Item / rmdir /s 等危險刪除。
#
# 與 Mac scripts/delete_guard.sh 同源邏輯。
#
# 註冊（寫進 ~/.claude/settings.json 的 hooks.PreToolUse）：
#   {"matcher":"Bash","hooks":[{"type":"command",
#     "command":"powershell -NoProfile -ExecutionPolicy Bypass -File \"%USERPROFILE%\\.openclaw\\workspace\\scripts\\delete_guard_hook.ps1\""}]}
#
# 註冊後必跑：scripts\verify_delete_guard.ps1 證明它真的會擋（檔案存在 ≠ 鎖有效）。
# ============================================================
$ErrorActionPreference = 'Stop'

# stdin 編碼鐵律（2026-08-26 聯想，同 feed_junshi_handoff.ps1）：
# PS 5.1 -File 模式下 InputEncoding 預設 Big5，含中文檔名的刪除指令會讀壞而漏擋
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 讀 PreToolUse 傳入的 JSON（stdin）
try {
    $raw  = [Console]::In.ReadToEnd()
    $data = $raw | ConvertFrom-Json
} catch { exit 0 }

$cmd = ''
try { if ($data.tool_input -and $data.tool_input.command) { $cmd = [string]$data.tool_input.command } } catch { $cmd = '' }
if ([string]::IsNullOrWhiteSpace($cmd)) { exit 0 }

# 先剝掉引號字面字串（避免 grep "Remove-Item" 之類被誤判）
$stripped = $cmd -replace '"[^"]*"', '""'
$stripped = $stripped -replace "'[^']*'", "''"

# 危險刪除特徵
$danger = @(
    '(?i)\bRemove-Item\b[^|;\r\n]*-(Recurse|Force)\b',
    '(?i)\bri\b[^|;\r\n]*-(Recurse|Force)\b',
    '(?i)\b(rmdir|rd)\b[^\r\n]*/s\b',
    '(?i)\b(del|erase)\b[^\r\n]*/[sq]\b',
    '\brm\s+(-[a-zA-Z]*r[a-zA-Z]*\b|--recursive)'
)
# 暫存/快取白名單：只動這些的刪除不擋
$safe = '(?i)([\\/]AppData[\\/]Local[\\/]Temp[\\/]|[\\/]Windows[\\/]Temp[\\/]|[\\/]tmp[\\/]|node_modules)'

# 2026-11-11 聯想體檢修：Git Bash 裡 Remove-Item 只能寫成 powershell -Command "..."，
# 上面剝引號會把整句刪除指令剝掉→永遠漏擋。-Command／-c 後面引號裡的內容一律也要檢查。
$targets = @($stripped)
foreach ($m in [regex]::Matches($cmd, '(?i)(?:-Command|-c)\s+(["''])(.*?)\1')) { $targets += $m.Groups[2].Value }

$hit = $false
foreach ($t in $targets) { foreach ($p in $danger) { if ([regex]::IsMatch($t, $p)) { $hit = $true; break } }; if ($hit) { break } }
if (-not $hit) { exit 0 }
if ([regex]::IsMatch($cmd, $safe)) { exit 0 }

# 通行證（教練親口同意，10 分鐘有效）
$token = Join-Path $env:USERPROFILE ".openclaw\workspace\state\DELETE_APPROVED"
if (Test-Path $token) {
    $age = (Get-Date) - (Get-Item $token).LastWriteTime
    if ($age.TotalMinutes -le 10) { exit 0 }
    Remove-Item -LiteralPath $token -Force -ErrorAction SilentlyContinue
}

$e = [Console]::Error
$e.WriteLine("")
$e.WriteLine("DELETE-GUARD 刪檔鎖：這個刪除指令已被擋下（案例 29：LINE 4GB 永久丟失）。")
$e.WriteLine("教練鐵律：珍貴資料只搬不刪；備份 .bak/.old 七天內絕對不刪。")
$e.WriteLine("教練親口同意這次刪除了嗎？")
$e.WriteLine("  是 -> New-Item -ItemType File -Force `"$token`" 後重試（10 分鐘有效）")
$e.WriteLine("  否 -> 改用搬到存檔區，或先問教練。")
exit 2
