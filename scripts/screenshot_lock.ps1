# Screenshot lock (PreToolUse hook, Windows/PowerShell version)
# Built 2026-07-13 by Lenovo (Windows) after a Mac cross-machine audit letter
# flagged that the shared screenshot_lock.sh's matcher list was incomplete.
#
# Extra finding specific to this machine: python3 on this Windows box is only
# the Windows Store app-execution-alias stub (exit code 49, no real
# interpreter installed), so the shared .sh script (which shells out to
# python3) would silently fail here even if the matcher were wired up. This
# .ps1 reimplements the same logic in pure PowerShell with no python
# dependency. Kept ASCII-only to avoid PowerShell 5.1 misreading UTF-8
# (no-BOM) source files under the system codepage, which previously broke
# string literals containing Chinese characters.
#
# Token gate: pass = ~/.openclaw/workspace/state/SCREENSHOT_APPROVED
#             no pass -> screenshot-class tool calls are blocked (exit 2)
#             pass is valid for 10 minutes.
#
# Grant pass (only after the coach explicitly says screenshots are OK):
#   New-Item -ItemType File -Force "$HOME\.openclaw\workspace\state\SCREENSHOT_APPROVED"

$ErrorActionPreference = "Stop"

$input_json = [Console]::In.ReadToEnd()

try {
    $data = $input_json | ConvertFrom-Json
} catch {
    exit 0
}

$tool = $data.tool_name
$ti = $data.tool_input
$shotActions = @("screenshot", "zoom")

function Wants-Screenshot {
    if ($tool -in @("mcp__computer-use__screenshot", "mcp__computer-use__zoom", "mcp__Claude_Preview__preview_screenshot")) {
        return $true
    }
    if ($tool -eq "mcp__Claude_Browser__computer") {
        return ($ti.action -in $shotActions)
    }
    if ($tool -eq "mcp__claude-in-chrome__computer") {
        return ($ti.action -in $shotActions)
    }
    if ($tool -eq "mcp__claude-in-chrome__gif_creator") {
        return $true
    }
    if ($tool -in @("mcp__computer-use__computer_batch", "mcp__computer-use__teach_step", "mcp__computer-use__teach_batch")) {
        $items = $ti.actions
        if (-not $items) { $items = $ti.steps }
        foreach ($a in $items) {
            if ($a.action -in $shotActions) { return $true }
            foreach ($sub in $a.actions) {
                if ($sub.action -in $shotActions) { return $true }
            }
        }
        return $false
    }
    if ($tool -eq "mcp__claude-in-chrome__browser_batch") {
        foreach ($a in $ti.actions) {
            if ($a.input.action -in $shotActions) { return $true }
        }
        return $false
    }
    return $false
}

if (-not (Wants-Screenshot)) {
    exit 0
}

$token = Join-Path $HOME ".openclaw\workspace\state\SCREENSHOT_APPROVED"
$maxAgeSeconds = 600

if (Test-Path $token) {
    $age = (Get-Date) - (Get-Item $token).LastWriteTime
    if ($age.TotalSeconds -le $maxAgeSeconds) {
        exit 0
    }
    Remove-Item $token -Force -ErrorAction SilentlyContinue
}

[Console]::Error.WriteLine("")
[Console]::Error.WriteLine("Screenshot lock: this screenshot call was blocked.")
[Console]::Error.WriteLine("")
[Console]::Error.WriteLine("Coach's standing rule: no screenshots without explicit consent (they burn tokens; use a command or file read instead whenever possible).")
[Console]::Error.WriteLine("Did the coach explicitly approve a screenshot just now?")
[Console]::Error.WriteLine("  Yes -> run: New-Item -ItemType File -Force `"$token`" then retry (valid 10 min)")
[Console]::Error.WriteLine("  No  -> use a command or file read instead, or ask the coach first.")
exit 2
