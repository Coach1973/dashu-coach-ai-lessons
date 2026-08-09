# Auto-open Chrome after HTML edit (PostToolUse hook, Windows/PowerShell version)
# Built 2026-08-09 by Lenovo per project_cross_machine_hook_sync_todo_2026-08-08
#
# Mirrors Mac's scripts/auto_chrome_after_html_edit.sh: whenever Edit/Write
# touches an .html file, immediately pop open Chrome on that local file so
# the coach doesn't need to be reminded after the fact.
#
# Kept ASCII-only in string literals: this machine's Windows PowerShell 5.1
# misreads UTF-8 (no-BOM) source under the system codepage, corrupting
# multi-byte characters inside string literals and breaking the parser
# (same issue documented in screenshot_lock.ps1, confirmed again here
# 2026-08-09 via a live test run before this fix).
#
# Limitation: template files (Jinja/Flask) opened via file:// won't render
# server-side logic; still verify against the real server URL separately.
#
# Second encoding gotcha found + fixed 2026-08-09: this machine's console
# defaults to Big5 for [Console]::In, silently corrupting any UTF-8 (e.g.
# Chinese) text in the hook's stdin JSON -- a Chinese file path would parse
# but then fail Test-Path against the mangled string. Fixed by forcing
# [Console]::InputEncoding to UTF8 before reading stdin. This same gotcha
# likely applies to any other Windows PowerShell hook that reads stdin JSON
# and may see Chinese text (e.g. screenshot_lock.ps1's Bash command matching).

$ErrorActionPreference = "Stop"
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

$input_json = [Console]::In.ReadToEnd()

try {
    $data = $input_json | ConvertFrom-Json
} catch {
    exit 0
}

$tool = $data.tool_name
if ($tool -ne "Edit" -and $tool -ne "Write") {
    exit 0
}

$filePath = $data.tool_input.file_path
if (-not $filePath) { exit 0 }
if ($filePath -notmatch '\.html?$') { exit 0 }
if (-not [System.IO.Path]::IsPathRooted($filePath)) { exit 0 }
if (-not (Test-Path $filePath)) { exit 0 }

$uri = "file:///" + ($filePath -replace '\\', '/')

try {
    Start-Process "chrome" $uri -ErrorAction Stop
    [Console]::Error.WriteLine("Auto-opened Chrome: $filePath was edited, opened as a local file for review.")
    [Console]::Error.WriteLine("If this is a template file (Jinja/backend-rendered), the page may look incomplete -- verify against the real server URL too.")
} catch {
    try {
        Start-Process $uri -ErrorAction Stop
        [Console]::Error.WriteLine("Auto-open: chrome executable not found, opened with default browser instead: $filePath")
    } catch {
        [Console]::Error.WriteLine("Auto-open Chrome failed: $_")
    }
}

exit 0
