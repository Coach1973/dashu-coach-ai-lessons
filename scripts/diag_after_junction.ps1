# 升級 junction 後若打「開」仍無接力棒，跑這個診斷
# 教練暗號：「診斷 hook」
# Win 軍師跑完把輸出全部貼回給 Mac 軍師（5-10 行）

Write-Host "=== Junction 狀態 ==="
$c = "$env:USERPROFILE\.claude"
if (Test-Path $c) {
    $i = Get-Item $c -Force
    $isJ = ($i.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0
    Write-Host "$c | IsJunction=$isJ | Target=$($i.Target)"
} else {
    Write-Host "$c 不存在！"
}

Write-Host ""
Write-Host "=== settings.json hook 註冊 ==="
$sf = "$env:USERPROFILE\.claude\settings.json"
if (Test-Path $sf) {
    Write-Host "檔案大小: $((Get-Item $sf).Length) bytes"
    $s = Get-Content $sf -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($s.hooks.UserPromptSubmit) {
        $count = ($s.hooks.UserPromptSubmit | ForEach-Object { $_.hooks }).Count
        Write-Host "UserPromptSubmit 共 $count 個 hook"
        $s.hooks.UserPromptSubmit | ForEach-Object {
            $_.hooks | ForEach-Object { Write-Host "  - $($_.command)" }
        }
    } else {
        Write-Host "❌ 沒有 UserPromptSubmit hook 註冊"
    }
} else {
    Write-Host "❌ settings.json 不存在"
}

Write-Host ""
Write-Host "=== Hook 腳本檔案 ==="
$h = "E:\Claude-Data\workspace\scripts\feed_junshi_handoff.ps1"
Write-Host "$h | Exists=$(Test-Path $h)"

Write-Host ""
Write-Host "=== 環境變數 ==="
Write-Host "CLAUDE_CONFIG_DIR (User) = $([Environment]::GetEnvironmentVariable('CLAUDE_CONFIG_DIR','User'))"
Write-Host "CLAUDE_CONFIG_DIR (本進程) = $env:CLAUDE_CONFIG_DIR"
Write-Host "JUNSHI_HOOK_ROOT (User) = $([Environment]::GetEnvironmentVariable('JUNSHI_HOOK_ROOT','User'))"

Write-Host ""
Write-Host "=== 模擬 hook 跑一次「開」看會印什麼 ==="
$payload = '{"session_id":"diag","prompt":"開"}'
$out = $payload | & powershell.exe -ExecutionPolicy Bypass -File $h 2>&1
$firstThree = ($out -split "`n" | Select-Object -First 3) -join " | "
Write-Host "Hook 第一行三段: $firstThree"
Write-Host "輸出總行數: $(($out -split "`n").Count)"
Write-Host "含「軍師接力棒」: $($out -match '軍師接力棒')"

Write-Host ""
Write-Host "=== Claude Code 進程 ==="
Get-Process | Where-Object { $_.ProcessName -like "*claude*" -or $_.ProcessName -like "*Claude*" } |
    Select-Object ProcessName, Id, Path | Format-Table -AutoSize
