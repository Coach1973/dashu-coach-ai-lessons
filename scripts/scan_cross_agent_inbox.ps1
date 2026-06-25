# Hook: UserPromptSubmit (Windows 聯想/ACER 版)
# 用途：每次教練講話時掃 cross-agent/inbox/{自己}/，有新信主動報告
# 設計：有信才注入，沒信靜默退出（不干擾正常對話）
# 對應：教練 2026-06-26 0:17 親口「以後跨機統一路徑，叫他們自己去讀」
#
# 安裝步驟（聯想或 ACER 軍師讀完照做）：
#   1. $env:AGENT_INBOX_NAME 設成 "lenovo" 或 "acer"
#      [Environment]::SetEnvironmentVariable("AGENT_INBOX_NAME","lenovo","User")   # 聯想
#      [Environment]::SetEnvironmentVariable("AGENT_INBOX_NAME","acer","User")     # ACER
#   2. 在 ~/.claude/settings.json 的 hooks.UserPromptSubmit 加一條：
#      { "command": "powershell -ExecutionPolicy Bypass -File D:\\Claude-Data\\mac-openclaw-workflows\\scripts\\scan_cross_agent_inbox.ps1", "type": "command" }
#      （路徑依實際 repo 位置調整）

$ErrorActionPreference = "SilentlyContinue"

# 找 workspace 根（以本檔案位置往上一層）
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Workspace = Split-Path -Parent $ScriptDir

# 機器名（必須設環境變數）
$AgentName = $env:AGENT_INBOX_NAME
if (-not $AgentName) { exit 0 }   # 沒設就靜默

$InboxDir = Join-Path $Workspace "cross-agent\inbox\$AgentName"
if (-not (Test-Path $InboxDir)) { exit 0 }

$Letters = Get-ChildItem -Path $InboxDir -Filter "*.md" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
if (-not $Letters -or $Letters.Count -eq 0) { exit 0 }

$Count = $Letters.Count
$YearMonth = Get-Date -Format "yyyy-MM"

$output = @"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📬 跨機軍師信箱（$AgentName 收件匣有 $Count 封未讀）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

未讀清單（新→舊）：
"@

foreach ($l in $Letters) {
    $output += "`n  📨 $($l.Name)"
}

$output += @"


🎯 教練口令字典：
  • 「讀信」「跨機有信」「{機器}有事交代」 → $AgentName 軍師自動讀取最新封並執行/回報
  • 處理完務必 Move-Item 到 cross-agent\outbox\$YearMonth\ 歸檔，不留在 inbox

📁 完整路徑：$InboxDir
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"@

Write-Output $output
exit 0
