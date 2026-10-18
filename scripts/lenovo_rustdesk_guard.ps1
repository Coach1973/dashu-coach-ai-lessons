# Lenovo RustDesk guard (2026-10-19). Keeps this PC reachable from other machines / phone.
# Why: RustDesk's own "Stop service" action (log line "Uninstalling service...") deleted the service
#      and wrote stop-service='Y' into RustDesk2.toml at least 9 times since April (last: 09-05 03:09, 10-14 22:56).
#      While stop-service='Y', RustDesk neither listens on 21118 nor registers with the rendezvous server.
# How: event driven, NO polling. Blocks on (a) RustDesk process exit, (b) RustDesk2.toml change.
#      On either event: remove stop-service line, make sure direct-server='Y', start RustDesk (normal start,
#      NOT --tray: tray-only does not open 21118), verify 21118, write a log + a "last repair" note.
# Install: runs at logon via HKCU\...\Run (no admin needed). Installed copy:
#      %APPDATA%\RustDesk\guard\rustdesk_guard.ps1 ; log: %APPDATA%\RustDesk\guard\guard.log
# ASCII only on purpose (Windows PowerShell 5 misreads BOM-less UTF-8).

$exe   = 'D:\Program Files\RustDesk\rustdesk.exe'
$dir   = Join-Path $env:APPDATA 'RustDesk\config'
$cfg   = Join-Path $dir 'RustDesk2.toml'
$gdir  = Join-Path $env:APPDATA 'RustDesk\guard'
$log   = Join-Path $gdir 'guard.log'
$note  = Join-Path $gdir 'last_repair.txt'
New-Item -ItemType Directory -Force -Path $gdir | Out-Null

# single instance
$mutex = New-Object System.Threading.Mutex($false, 'Global\LenovoRustDeskGuard')
if (-not $mutex.WaitOne(0)) { exit 0 }

function Log($m) { Add-Content -Path $log -Value ('[{0}] {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $m) }

function Fix-Config {
  # returns $true if the file had to be changed
  if (-not (Test-Path $cfg)) { return $false }
  $t = [IO.File]::ReadAllText($cfg)
  $o = $t
  $t = [regex]::Replace($t, "(?m)^\s*stop-service\s*=\s*'Y'\s*\r?\n?", '')
  if ($t -notmatch "(?m)^\s*direct-server\s*=\s*'Y'") {
    if ($t -match "(?m)^\s*direct-server\s*=") { $t = [regex]::Replace($t, "(?m)^(\s*)direct-server\s*=.*$", "`$1direct-server = 'Y'") }
    elseif ($t -match '\[options\]') { $t = $t -replace '\[options\]', "[options]`r`ndirect-server = 'Y'" }
    else { $t += "`r`n[options]`r`ndirect-server = 'Y'`r`n" }
  }
  if ($t -ne $o) { [IO.File]::WriteAllText($cfg, $t); return $true }
  return $false
}

function Listening21118 { return [bool](Get-NetTCPConnection -State Listen -LocalPort 21118 -ErrorAction SilentlyContinue) }

function Repair($why) {
  Log "repair start: $why"
  Get-Process rustdesk -ErrorAction SilentlyContinue | Stop-Process -Force
  Start-Sleep -Seconds 3
  $changed = Fix-Config
  $r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = ('"' + $exe + '"') }
  Start-Sleep -Seconds 12
  $ok = Listening21118
  Log ("repair done: config_changed={0} start_rc={1} listening_21118={2}" -f $changed, $r.ReturnValue, $ok)
  Set-Content -Path $note -Value ('{0} | {1} | config_changed={2} | listening_21118={3}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $why, $changed, $ok)
}

$fsw = New-Object System.IO.FileSystemWatcher $dir, 'RustDesk2.toml'
$fsw.NotifyFilter = [IO.NotifyFilters]'LastWrite,Size'
$fsw.EnableRaisingEvents = $true
Register-ObjectEvent $fsw Changed -SourceIdentifier cfgchg | Out-Null
Log 'guard started'

while ($true) {
  $p = Get-Process rustdesk -ErrorAction SilentlyContinue | Select-Object -First 1
  $stopY = (Test-Path $cfg) -and ([IO.File]::ReadAllText($cfg) -match "(?m)^\s*stop-service\s*=\s*'Y'")
  if (-not $p)        { Repair 'rustdesk not running' ; $p = Get-Process rustdesk -ErrorAction SilentlyContinue | Select-Object -First 1 }
  elseif ($stopY)     { Repair "stop-service=Y found in config" ; $p = Get-Process rustdesk -ErrorAction SilentlyContinue | Select-Object -First 1 }
  elseif (-not (Listening21118)) {
    # running but not accepting direct connections: give it a moment, then repair
    Start-Sleep -Seconds 20
    if (-not (Listening21118)) { Repair 'running but 21118 not listening' ; $p = Get-Process rustdesk -ErrorAction SilentlyContinue | Select-Object -First 1 }
  }
  if ($p) {
    $p.EnableRaisingEvents = $true
    Register-ObjectEvent $p Exited -SourceIdentifier pexit | Out-Null
  }
  Get-Event | Remove-Event -ErrorAction SilentlyContinue
  # block here until the process exits or the config file changes (no timer, no polling)
  $null = Wait-Event
  Start-Sleep -Seconds 2
  Unregister-Event -SourceIdentifier pexit -ErrorAction SilentlyContinue
  Get-Event | Remove-Event -ErrorAction SilentlyContinue
}
