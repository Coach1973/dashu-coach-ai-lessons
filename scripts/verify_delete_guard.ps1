# ============================================================
# verify_delete_guard.ps1 — 證明 Windows 刪檔鎖會擋（案例 29 後建立）
# 用法：powershell -NoProfile -ExecutionPolicy Bypass -File scripts\verify_delete_guard.ps1
# 全綠 exit 0 = 這台機器的鎖有效；任何紅 exit 1 = 鎖是擺設，立刻修。
# ============================================================
$ErrorActionPreference = 'Stop'
$hook  = Join-Path $PSScriptRoot "delete_guard_hook.ps1"
$token = Join-Path $env:USERPROFILE ".openclaw\workspace\state\DELETE_APPROVED"
if (Test-Path $token) { Remove-Item $token -Force -ErrorAction SilentlyContinue }

if (-not (Test-Path $hook)) { Write-Host "找不到 $hook" -ForegroundColor Red; exit 1 }

$script:pass = 0; $script:fail = 0
function Check([string]$desc, [string]$command, [int]$expect) {
    $json = @{ tool_name = "Bash"; tool_input = @{ command = $command } } | ConvertTo-Json -Compress
    $json | & powershell -NoProfile -ExecutionPolicy Bypass -File $hook 2>$null | Out-Null
    $rc = $LASTEXITCODE
    if ($rc -eq $expect) { Write-Host "  OK  $desc (rc=$rc)" -ForegroundColor Green; $script:pass++ }
    else { Write-Host "  XX  $desc 期望 rc=$expect 實得 rc=$rc" -ForegroundColor Red; $script:fail++ }
}

Write-Host "刪檔鎖自證測試 (Windows)"
Check "Remove-Item -Recurse -Force 被擋" 'Remove-Item -Recurse -Force E:\Claude-Data\LINE.bak' 2
Check "rmdir /s 被擋"                   'rmdir /s /q C:\data'                                 2
Check "一般 dir 放行"                   'dir C:\'                                             0
Check "Temp 暫存刪除放行"               'Remove-Item -Recurse -Force C:\Users\x\AppData\Local\Temp\cache' 0
Write-Host "通過 $script:pass 失敗 $script:fail"
if ($script:fail -eq 0) { Write-Host "OK 本機刪檔鎖【有效】" -ForegroundColor Green; exit 0 }
else { Write-Host "XX 本機刪檔鎖【無效】——它是擺設，立刻修，別相信它" -ForegroundColor Red; exit 1 }
