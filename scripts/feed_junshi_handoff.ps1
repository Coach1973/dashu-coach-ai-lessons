# Hook: UserPromptSubmit (Windows PowerShell 版 · v4 心法＋最新一棒)
# 用途: 教練在 Windows 桌面版 Claude Code 喊「開」「開工」等暗號時，
#       自動 git pull 拉雲端最新接力棒 → 注入六步驟全部內容到 context。
#
# v4 改動 (2026-10-05，對齊 Mac feed_junshi_handoff.sh v3 的瘦身，注入 42KB→約 10KB)：
#   - 只注入：🎯教練交辦、雲端同步、身份、最新一棒摘要＋🙋區、第6步回報要求＋三關
#   - 拿掉：接力棒全文、JUNSHI_RULES 全文、HEARTBEAT 尾50行、試金石2案例、knowledges 清單、memory 最新日、
#           舊 session 總結（實測當天內容多半是舊自檢紀錄／空標題／7月舊檔，試金石已變反射）。
#   - 需要時各檔原地 Read；KAIGONG_SELFTEST=1 可只產生內容、不拉雲端不寫紀錄不設 marker（反覆實測用）。
#
# v3 改動 (2026-06-23 教練親口「對長期有好處的事不問直接做」):
#   - 不只注入接力棒，連同 HEARTBEAT / 試金石最新 3 案 / memory 最新日 / knowledges 近 7 天清單全部一次注入
#   - 對應 Mac feed_junshi_handoff.sh，雙邊邏輯對等
#   - 保留 v2 雲端優先設計（git pull 永遠拉最新）
#
# 對應 Mac 版: feed_junshi_handoff.sh

$ErrorActionPreference = 'Continue'
$selfTest = ($env:KAIGONG_SELFTEST -eq '1')

# ───────── stdin 編碼鐵律（2026-08-26 聯想查出，跟案例 64 同源）─────────
# PS 5.1 在 -File 模式下 [Console]::InputEncoding 預設是系統 codepage（Big5），
# stdin JSON 裡的中文會被讀壞（實測「開工」958B,5DE5 → 003F,F55D,6975），
# 觸發詞永遠比對不到 → 整支 hook 靜默不觸發、不報錯。
# 對稱寫法見 summary_upload_trigger.ps1 / periodic_xinfa_reload_hook.ps1。
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ───────── 雲端真相源（固定，不需動）─────────
$REPO_URL = "https://github.com/Coach1973/mac-openclaw-workflows.git"

# ───────── workspace 位置（v3.1 教練親定：對齊既有 E:\Claude-Data）─────────
if ($env:JUNSHI_HOOK_ROOT) {
    $workspace = Join-Path $env:JUNSHI_HOOK_ROOT "workspace"
} elseif (Test-Path "E:\Claude-Data") {
    $workspace = "E:\Claude-Data\workspace"
} elseif (Test-Path "E:\") {
    $workspace = "E:\junshi-hook\workspace"
} else {
    $workspace = Join-Path $env:USERPROFILE ".openclaw\workspace"
}

$handoff       = Join-Path $workspace "JUNSHI_HANDOFF_LATEST.md"
$identityCard  = Join-Path $workspace "knowledges\IDENTITY_windows_desktop.md"
$sessionDump   = Join-Path $workspace "claude-sessions"
$heartbeatPath = Join-Path $workspace "HEARTBEAT.md"
$stonePath     = Join-Path $workspace "試金石\試金石_案例庫.md"
$top10IndexPath = Join-Path $workspace "distill\top10_errors_index.md"
$memoryDir     = Join-Path $workspace "memory"
$knowledgesDir = Join-Path $workspace "knowledges"

# ───────── 讀 stdin JSON ─────────
$raw = [Console]::In.ReadToEnd()
try { $payload = $raw | ConvertFrom-Json -ErrorAction Stop } catch { exit 0 }

$sessionId = if ($payload.session_id) { [string]$payload.session_id } else { "" }
$prompt    = if ($payload.prompt)     { [string]$payload.prompt }     else { "" }
if ([string]::IsNullOrWhiteSpace($prompt)) { exit 0 }

# ───────── Marker（同 session 只餵一次）─────────
$markerDir = Join-Path $env:TEMP "junshi_markers"
if (-not (Test-Path $markerDir)) { New-Item -ItemType Directory -Path $markerDir -Force | Out-Null }
$marker = Join-Path $markerDir "fed_$sessionId"

# ───────── 觸發詞偵測 ─────────
$forceRefeed = $false
if ($prompt -match '^[\s]*開工[\s。！!]*$' -or $prompt -match '開工了' -or $prompt -match '開工幹活') {
    $forceRefeed = $true
}
$triggerPattern = '^[\s]*(開|開工|工作|幹活|開始工作)[\s。！!]*$|軍師|接續指揮所|JunShi|junshi|Claude\s*軍師'
$triggered = ($prompt -match $triggerPattern) -or $forceRefeed
if (-not $triggered) { exit 0 }

if ((-not $forceRefeed) -and $sessionId -and (Test-Path $marker)) { exit 0 }

# ───────── 🌐 雲端優先：先確保 workspace 是最新版 ─────────
$pullStatus = ""
try {
    if ($selfTest) {
        $pullStatus = "（自我測試，略過 pull）"
    } elseif (-not (Test-Path $workspace)) {
        # 2026-09-01 修復：先找有沒有同一份 repo 已經存在別的資料夾名稱（例如
        # mac-openclaw-workflows），有就補 junction 過去，不要盲目重新 clone
        # 整包 1GB+ 資料。這支腳本以前每次遇到 $workspace 對不上真正的 repo
        # 資料夾名稱，就會無限重新 clone，見 claude-brain/project_acer_health_check_2026-08-31.md
        $parentDir = Split-Path $workspace -Parent
        $normalizedTarget = $REPO_URL.TrimEnd('/') -replace '\.git$', ''
        $existingRepo = $null
        if (Test-Path $parentDir) {
            $existingRepo = Get-ChildItem -Path $parentDir -Directory -ErrorAction SilentlyContinue |
                Where-Object {
                    $gitDir = Join-Path $_.FullName ".git"
                    if (-not (Test-Path $gitDir)) { return $false }
                    $remoteUrl = (& git -C $_.FullName remote get-url origin 2>$null)
                    if (-not $remoteUrl) { return $false }
                    $normalizedRemote = $remoteUrl.Trim().TrimEnd('/') -replace '\.git$', ''
                    return ($normalizedRemote -eq $normalizedTarget)
                } | Select-Object -First 1
        }
        if ($existingRepo) {
            New-Item -ItemType Junction -Path $workspace -Target $existingRepo.FullName -Force | Out-Null
            $pullResult = & git -C $workspace pull --quiet --rebase 2>&1
            $headHash = (& git -C $workspace rev-parse --short HEAD 2>&1).Trim()
            $pullStatus = "✅ 找到既有 repo（$($existingRepo.Name)）已補 junction，HEAD: $headHash"
        } else {
            if (-not (Test-Path $parentDir)) { New-Item -ItemType Directory -Path $parentDir -Force | Out-Null }
            $cloneResult = & git clone --quiet $REPO_URL $workspace 2>&1
            if ($LASTEXITCODE -eq 0) {
                $pullStatus = "✅ 首次 clone 雲端 repo 成功"
            } else {
                $pullStatus = "❌ Clone 失敗: $cloneResult"
            }
        }
    } else {
        # 2026-09-05 修復（ACER來信+本場實測皆撞到同一個坑）：原本不論工作區乾不乾淨
        # 都跑 stash→pull --rebase→pop，比 Mac 版本更容易撞到「pop 時跟雲端剛推上來的
        # 內容衝突」——且 pop 失敗/衝突時原本完全靜默吞掉，衝突標記會被直接寫進檔案。
        # 改成跟 Mac 版對齊：先試 ff-only（不動工作區，最安全），失敗才退回 stash+rebase，
        # 且 stash pop 後一定檢查有沒有殘留衝突標記，有就大聲警告不能悶著。
        $branch = (& git -C $workspace rev-parse --abbrev-ref HEAD 2>$null).Trim()
        & git -C $workspace fetch --quiet 2>$null | Out-Null
        $ffOk = $false
        if ($branch) {
            & git -C $workspace merge --quiet --ff-only "origin/$branch" 2>$null | Out-Null
            $ffOk = ($LASTEXITCODE -eq 0)
        }
        if ($ffOk) {
            $headHash = (& git -C $workspace rev-parse --short HEAD 2>&1).Trim()
            $pullStatus = "✅ 已拉雲端最新（HEAD: $headHash，ff-only未動工作區）"
        } else {
            $dirty = & git -C $workspace status --porcelain 2>$null
            $stashed = $false
            if ($dirty) {
                & git -C $workspace stash push -u -m "auto-pull-stash-$(Get-Date -Format yyyyMMddHHmmss)" --quiet 2>$null | Out-Null
                if ($LASTEXITCODE -eq 0) { $stashed = $true }
            }
            $pullResult = & git -C $workspace pull --quiet --rebase 2>&1
            $pullOk = ($LASTEXITCODE -eq 0)
            $popConflict = $false
            if ($stashed) {
                & git -C $workspace stash pop --quiet 2>$null | Out-Null
                if ($LASTEXITCODE -ne 0) { $popConflict = $true }
            }
            # 2026-09-05補強（聯想同日實測撞到的邊界情況）：不論 pop 有沒有回報非零
            # exit code，都再親自掃一次工作區有沒有殘留衝突標記（曾實際發生 pop 回報
            # 成功但檔案裡仍留有 <<<<<<< 的案例），跟 Mac 版本一樣列出受影響檔案。
            if (-not $popConflict) {
                $unmerged = & git -C $workspace status --porcelain 2>$null | Where-Object { $_ -match '^(UU|AA|DD|AU|UA|UD|DU) ' }
                if ($unmerged) { $popConflict = $true }
            }
            if ($popConflict) {
                $conflictFiles = (& git -C $workspace diff --name-only --diff-filter=U 2>$null) -join ', '
                $pullStatus = "🔴 stash pop 衝突未解決！受影響檔案：$conflictFiles ——本次不算真正同步成功，需要人工檢查 $workspace 後手動解決衝突，不要直接commit"
            } elseif ($pullOk) {
                $headHash = (& git -C $workspace rev-parse --short HEAD 2>&1).Trim()
                $pullStatus = "✅ 已拉雲端最新（HEAD: $headHash$(if($stashed){'，本地改動已 stash/pop（無衝突）'}else{''})）"
            } else {
                $pullStatus = "⚠️ Pull 警告: $pullResult"
            }
        }
    }
} catch {
    $pullStatus = "❌ Git 操作失敗: $_"
}

# ───────── 🩺 同步健康狀態落地（2026-08-26，讓Mac那邊能查這台機器多久沒真正同步過）─────────
# 這台機器沒有直接發Telegram的管道(bot只跑在Mac mini上)，所以這裡只負責老實記錄
# 「我剛才有沒有真的拉到雲端最新」，Mac那邊的feed_junshi_handoff.sh開工時會讀取
# 所有機器這份紀錄，超過72小時沒更新就會主動用Telegram通知教練。
# 教練若想確認這台機器的識別名稱是否正確，可直接看下面 machineKey 的值。
try {
    if ($selfTest) { throw "selftest" }
    $machineKey = ($env:COMPUTERNAME).ToLower()
    if (-not $machineKey) { $machineKey = "windows-unknown" }
    $syncHealthDir = Join-Path $workspace "state\sync_health"
    if (-not (Test-Path $syncHealthDir)) { New-Item -ItemType Directory -Path $syncHealthDir -Force | Out-Null }
    $syncHealthFile = Join-Path $syncHealthDir "$machineKey.json"
    $pullOkForJson = $pullStatus.StartsWith("✅")
    $healthData = @{
        machine       = $machineKey
        last_attempt  = (Get-Date).ToString("yyyy-MM-ddTHH:mm:sszzz")
        pull_ok       = $pullOkForJson
        status_text   = $pullStatus
    }
    $healthData | ConvertTo-Json | Set-Content -Path $syncHealthFile -Encoding UTF8
} catch {
    # 這只是輔助紀錄，寫失敗不該擋到主流程繼續注入接力棒內容
}

# ───────── 接力棒不存在 → 印雲端狀態給教練看 ─────────
if (-not (Test-Path $handoff)) {
    Write-Output "# ⚠️ 軍師接力棒從雲端拉不下來"
    Write-Output ""
    Write-Output "雲端狀態：$pullStatus"
    Write-Output ""
    Write-Output "預期位置：$handoff"
    Write-Output ""
    Write-Output "可能原因："
    Write-Output "- GitHub credential 失效（請跑 ``gh auth login`` 重新登入）"
    Write-Output "- 網路問題"
    Write-Output "- repo URL 變更（目前指向：$REPO_URL）"
    exit 0
}

# ───────── 輸出注入內容（v4：心法＋最新一棒）─────────
Write-Output "# 🔴 軍師接力棒 v4（心法＋最新一棒；本場 session 僅一次）"
Write-Output ""

# 2026-10-02 Mac軍師交辦（教練授權）：最新一棒的「教練上一場交辦」置頂注入，挑時間最新的一段（同Mac feed_junshi_handoff.sh）
$nextTask = ""
try {
    $pyExe = $null
    foreach ($c in @("python", "py")) { if (Get-Command $c -ErrorAction SilentlyContinue) { $pyExe = $c; break } }
    if ($pyExe -and (Test-Path $handoff)) {
        $tmpPy = Join-Path $PSScriptRoot "pick_next_task.py"
        $prevEnc = [Console]::OutputEncoding
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        $nextTask = ((& $pyExe $tmpPy $handoff) -join "`n").Trim()
        [Console]::OutputEncoding = $prevEnc
    }
} catch { $nextTask = "" }
if ($nextTask) {
    Write-Output "## 🎯 教練上一場交辦：這一場第一件要做的事（開工回報第一行就要講，講完直接開始做）"
    Write-Output ""
    Write-Output $nextTask
    Write-Output ""
}
Write-Output "## 🌐 雲端同步狀態"
Write-Output ""
Write-Output "- $pullStatus"
Write-Output "- 本機 cache：$workspace"
Write-Output ""
Write-Output "## 🪪 身份硬性告知（教練 2026-06-17 親口定稿）"
Write-Output ""
Write-Output "- **平台**：Windows 桌面版（GUI App，非終端機 CLI）；工具能力跟 Mac CLI 完全同等（Bash、Read、Edit、Write、Agent、Skill 全都有）"
Write-Output "- **工作目錄**：``$workspace``（**不是 C 槽 .openclaw**）｜**稱呼教練**：**大樹教練**｜**commit 前綴**：``[Win]``（Mac 軍師是 ``[Mac]``）"
Write-Output "- 🔴 **三件最容易搞錯的事**：①「我是桌面版，沒有 shell」← 錯，你有完整工具。②「我是 Mac 環境」← 錯，路徑 ``/tmp/`` → ``\`$env:TEMP``、``open -a Chrome`` → ``Start-Process chrome.exe``。③ 危險指令一律走 ``scripts\delete_guard.ps1`` 的 ``Safe-Remove``，**禁止直接寫 ``Remove-Item -Recurse -Force``**（案例 24，636 GB 學費）。"
Write-Output "- 完整身份卡＋網頁推 SOP Mac↔Windows 對照表：``knowledges\IDENTITY_windows_desktop.md``（需要才讀）"
Write-Output ""
Write-Output "---"
Write-Output ""

# ───────── 第 1 步：最新一棒摘要＋🙋區（對齊 Mac v3；前一棒／🤫／🔧區／封存索引需要才讀原檔）─────────
Write-Output "## 📜 第 1 步：接力棒（精簡注入：只貼最新一棒摘要＋🙋區；前一棒／🤫／🔧區／封存索引請讀 ``JUNSHI_HANDOFF_LATEST.md`` 原檔，需要才讀）"
Write-Output ""
$hLines = @(Get-Content -Path $handoff -Encoding UTF8)
$hdrIdx = @()
for ($i = 0; $i -lt $hLines.Count; $i++) {
    if ($hLines[$i].StartsWith('## 🔴 給跨對話框軍師讀的總結摘要')) { $hdrIdx += $i }
}
if ($hdrIdx.Count -ge 2) {
    # 找不到第二個標記就整份貼上（安全優先）；找得到就只貼最新一棒
    $hLines[$hdrIdx[0]..($hdrIdx[1] - 1)] | ForEach-Object { Write-Output $_ }
    $askIdx = -1
    for ($i = 0; $i -lt $hLines.Count; $i++) { if ($hLines[$i].StartsWith('### 🙋')) { $askIdx = $i; break } }
    if ($askIdx -ge 0) {
        $j = $askIdx + 1
        while ($j -lt $hLines.Count -and -not $hLines[$j].StartsWith('### ')) { $j++ }
        Write-Output ""
        $hLines[$askIdx..($j - 1)] | ForEach-Object { Write-Output $_ }
    }
} else {
    $hLines | ForEach-Object { Write-Output $_ }
}
Write-Output ""
Write-Output "> 需要才讀（原地 Read）：``HEARTBEAT.md``、``試金石\試金石_案例庫.md``（已變反射，會在對的時刻自己跳出來）、``knowledges\``、``memory\``、``JUNSHI_RULES.md``（軍師鐵律正典）。"

# ───────── 第 6 步：上線回應要求 ─────────
Write-Output ""
Write-Output "---"
Write-Output ""
Write-Output "## ✅ 第 6 步：上線回應要求（2026-09-24根源改版：開工不唸待辦）"
Write-Output "讀完本段後，回應**不超過5行**，只包含："
Write-Output "- 「我已讀完接力棒」＋身份核對（模型版本 + Windows 桌面版 GUI）＋雲端同步 HEAD hash 前 7 碼，一行講完"
Write-Output "- 待辦表「🙋要教練決定」區裡**還沒問過**的項目（通常是零件；零件就完全不提待辦）"
Write-Output "- 詢問教練「今天從哪件事開始？」"
Write-Output "- 若最上方有「🎯 教練上一場交辦」：第二行就講這件事，並說「現在開始做」，回報完直接動手，不問「今天從哪件事開始」"
Write-Output "**禁止**：唸「🤫等教練自己提起」區、唸「🔧AI自己的工作清單」、列舉上一棒戰果、自己發現的系統異常。這些是AI自己的事，自己處理。"
Write-Output ""
Write-Output "## 🚦 本場全程適用：問教練之前的三關（2026-09-24教練：「同一類事情不要再重複來煩我了」）"
Write-Output "任何時候（開工、健檢、全都釋放、總結、任務中途）要拿一件事去問教練或請教練決定，必須三關全過，少一關就不准問："
Write-Output "① **只有教練能做**：花錢、代表教練對外發言、不可逆操作、教練自己的內容與喜好、需要教練本人親自登入（例如要手機簡訊驗證碼、教練個人銀行等系統從未存過帳密的帳號）。路徑大全／既有腳本裡已存好帳密的主機與服務（VPS、GitHub、Netlify、ezPay等），AI 自己用，不算這一關。AI查得到、做得到、判斷得了的，自己處理。"
Write-Output "② **教練沒答過**：先查待辦表、封存檔、記憶檔。教練裁示過的（含「不用管」「略過」「到此為止」「保留就好」），換任何說法都不准再問。"
Write-Output "③ **現在不問會卡住**：教練正在等結果，或幾天內有期限。不急的寫進「🤫等教練自己提起」區，不主動提。"
Write-Output "**每件事最多問一次**：問過沒回應＝教練現在不想處理，移到🤫區，不追問。"
Write-Output "過不了三關的事：AI自己做完（不用報告細節，最多一行帶過），或安靜寫進🤫區。"
Write-Output ""

# 寫 self-test 到本機log，不寫HEARTBEAT.md（小龍蝦開機必讀檔，且會跨機同步；2026-09-25查到軍師日誌佔它78%）
$automationLog = Join-Path $workspace "state\junshi_automation.log"
if ((-not $selfTest) -and (Test-Path (Split-Path $automationLog))) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm"
    $triggerPreview = if ($prompt.Length -gt 40) { $prompt.Substring(0, 40) } else { $prompt }
    $selfTest = @"

## 🩺 軍師 Hook 自檢 $ts（Windows v4 心法＋最新一棒注入）
- ✅ Hook 觸發 + git pull + 注入完成
- 觸發詞：$triggerPreview
- 雲端狀態：$pullStatus
- Session: $sessionId
"@
    try { Add-Content -Path $automationLog -Value $selfTest -Encoding UTF8 } catch {}
}

if ($sessionId -and -not $selfTest) { New-Item -ItemType File -Path $marker -Force | Out-Null }
exit 0
