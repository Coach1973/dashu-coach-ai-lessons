# Periodic rule-text reload (UserPromptSubmit hook, Windows/PowerShell version)
# Built 2026-08-09 by Lenovo per project_cross_machine_hook_sync_todo_2026-08-08
#
# Mirrors Mac's scripts/periodic_xinfa_reload_hook.sh: every 10 turns after
# turn 20, re-inject the full text of the 21 rules (特助21守則) so it
# doesn't silently fall out of context on long sessions -- CLAUDE.md is
# only loaded once at session start.
#
# Encoding gotchas found + fixed 2026-08-09 (both confirmed via live test runs
# before the fixes, not just reasoned about):
#   1. This file itself has a UTF-8 BOM prepended. Without it, this machine's
#      Windows PowerShell 5.1 misreads UTF-8 (no-BOM) source under the system
#      codepage (Big5), corrupting the Chinese literal path on line ~26
#      (Xinfa) enough that Test-Path against it silently failed -- the whole
#      hook exited 0 every time with zero output, no error. Same root cause
#      documented in screenshot_lock.ps1's own header comment, but that one
#      worked around it by staying ASCII-only; this script needs a literal
#      Chinese filename, so BOM is the fix here instead.
#   2. [Console]::InputEncoding defaults to Big5 on this machine, corrupting
#      any UTF-8 (Chinese) text arriving via stdin JSON before it's even
#      parsed. Forced to UTF8 below. Likely affects any other Windows
#      PowerShell hook that reads stdin JSON containing Chinese text.
#
# No jq, no python3 dependency: this machine's python3 is a Windows Store
# app-execution-alias stub (exit code 49, no real interpreter), so this is
# a pure PowerShell reimplementation of the turn-counting + band logic.

$ErrorActionPreference = "Stop"
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$THRESHOLD = 20
$BAND = 10
$ProjectDir = "E:\Claude-Data\.claude\projects\E--Claude-Data"
$Xinfa = "E:\Claude-Data\mac-openclaw-workflows\特助心法.md"

$input_json = [Console]::In.ReadToEnd()

try {
    $data = $input_json | ConvertFrom-Json
} catch {
    exit 0
}

$sessionId = $data.session_id
if (-not $sessionId) { exit 0 }
if (-not (Test-Path $Xinfa)) { exit 0 }

$jsonlPath = Join-Path $ProjectDir "$sessionId.jsonl"
if (-not (Test-Path $jsonlPath)) { exit 0 }

$turns = 0
Get-Content $jsonlPath -Encoding UTF8 | ForEach-Object {
    $line = $_
    if (-not $line) { return }
    try { $o = $line | ConvertFrom-Json } catch { return }
    if ($o.type -ne "user") { return }
    $content = $o.message.content
    if ($content -is [string]) {
        if ($content.Trim().Length -gt 0) { $turns++ }
    } elseif ($content -is [System.Array]) {
        $hasText = $false
        $hasToolResult = $false
        foreach ($block in $content) {
            if ($block.type -eq "text") { $hasText = $true }
            if ($block.type -eq "tool_result") { $hasToolResult = $true }
        }
        if ($hasText -and -not $hasToolResult) { $turns++ }
    }
}

if ($turns -lt $THRESHOLD) { exit 0 }

$curBand = [Math]::Floor($turns / $BAND) * $BAND

$marker = Join-Path $env:TEMP "xinfa_reload_band_$sessionId"
$lastBand = 0
if (Test-Path $marker) {
    $lastBand = [int](Get-Content $marker -Raw -ErrorAction SilentlyContinue)
}

if ($curBand -le $lastBand) { exit 0 }

Set-Content -Path $marker -Value $curBand -NoNewline

$lines = Get-Content $Xinfa -Encoding UTF8
$excerpt = ($lines[53..164]) -join "`n"

$sep = "----------------------------------------"
Write-Output ""
Write-Output $sep
Write-Output "[auto-reload at turn $curBand -- not requested by the coach]"
Write-Output $sep
Write-Output "This session has passed turn $curBand. The rule text loaded from CLAUDE.md at"
Write-Output "session start may have been compressed out of context by now. Below is the full"
Write-Output "original text of the 21 rules -- reference this text directly, do not rely on memory."
Write-Output ""
Write-Output $excerpt
Write-Output ""
Write-Output "(source: $Xinfa, auto-reloaded at turn $curBand)"
Write-Output $sep

exit 0
