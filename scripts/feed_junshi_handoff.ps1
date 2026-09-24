# Hook: UserPromptSubmit (Windows PowerShell 版 · v3 六步驟全注入)
# 用途: 教練在 Windows 桌面版 Claude Code 喊「開」「開工」等暗號時，
#       自動 git pull 拉雲端最新接力棒 → 注入六步驟全部內容到 context。
#
# v3 改動 (2026-06-23 教練親口「對長期有好處的事不問直接做」):
#   - 不只注入接力棒，連同 HEARTBEAT / 試金石最新 3 案 / memory 最新日 / knowledges 近 7 天清單全部一次注入
#   - 對應 Mac feed_junshi_handoff.sh，雙邊邏輯對等
#   - 保留 v2 雲端優先設計（git pull 永遠拉最新）
#
# 對應 Mac 版: feed_junshi_handoff.sh

$ErrorActionPreference = 'Continue'

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
    if (-not (Test-Path $workspace)) {
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

# ───────── 找最新 SESSION 總結 ─────────
$latestSession = $null
if (Test-Path $sessionDump) {
    $latestSession = Get-ChildItem -Path $sessionDump -Filter "SESSION_*.md" -ErrorAction SilentlyContinue |
                     Sort-Object Name | Select-Object -Last 1
}

# ───────── 輸出注入內容 ─────────
Write-Output "# 🔴 軍師接力棒 v3（六步驟全注入，本場 session 僅一次）"
Write-Output ""
Write-Output "## 🌐 雲端同步狀態（v3 設計：每次「開工」自動 git pull）"
Write-Output ""
Write-Output "- $pullStatus"
Write-Output "- 來源：$REPO_URL"
Write-Output "- 本機 cache：$workspace"
Write-Output ""
Write-Output "## 🪪 身份硬性告知（教練 2026-06-17 親口定稿）"
Write-Output ""
Write-Output "- **平台**：Windows 桌面版（GUI App，非終端機 CLI）"
Write-Output "- **軟體**：Claude Code Desktop App for Windows"
Write-Output "- **工具能力**：✅ 跟 Mac CLI / 終端機 **完全同等**——Bash、Read、Edit、Write、TaskCreate、Agent、Skill 全部都有"
Write-Output "- **底層 shell**：Bash 工具在 Windows 跑 PowerShell（不是 macOS bash），語法要對應"
Write-Output "- **工作目錄**：``$workspace`` (**不是 C 槽 .openclaw**)"
Write-Output "- **身份等級**：軍師（Opus），跟 Mac 軍師同等發言權"
Write-Output "- **稱呼教練**：**大樹教練**"
Write-Output "- **commit 前綴**：``[Win]``（區分 Mac 軍師的 ``[Mac]``）"
Write-Output ""
Write-Output "🔴 **三件最容易搞錯的事**："
Write-Output "1. **「我是桌面版，沒有 shell」← 錯**。你有完整 Bash/Read/Edit/Write 工具，能力同 CLI。"
Write-Output "2. **「我是 Mac 環境」← 錯**。路徑 ``/tmp/`` → ``\`$env:TEMP``；指令 ``open -a Chrome`` → ``Start-Process chrome.exe``。"
Write-Output "3. **跨 shell 跳脫災難（案例 24，636 GB 學費）**——危險指令一律走 ``scripts\delete_guard.ps1`` 的 ``Safe-Remove``，**禁止直接寫 ``Remove-Item -Recurse -Force``**。"
Write-Output ""
Write-Output "📖 **完整身份卡 + 網頁推 SOP Mac↔Windows 對照表**：``knowledges\IDENTITY_windows_desktop.md`` ——本場必讀。"
Write-Output ""
Write-Output "---"
Write-Output ""
Write-Output "教練說「開工/開/工作/幹活」=暗號觸發。讀完本段即可無縫接續。"

# ───────── 第 1 步：接力棒 ─────────
# 2026-08-26 聯想補（對齊 Mac 版 feed_junshi_handoff.sh 第 192~210 行的既有設計）：
# workspace/CLAUDE.md 已由 scripts/sync_handoff_to_claudemd.sh 自動鏡像接力棒全文，
# 桌面版讀 CLAUDE.md 時本來就會看到。鏡像若是最新的（sync marker >= HANDOFF mtime）
# 就不重複貼一次全文，省下約 114KB；鏡像不是最新（sync 掛掉/沒跑過）才照舊完整貼上，安全優先。
Write-Output ""
Write-Output "## 📜 第 1 步：接力棒"
Write-Output ""
# 判斷方式刻意跟 Mac 版不同：Mac 比對 .sync_markers 時間戳，但 git pull 會把檔案 mtime
# 改成 pull 當下時間，在聯想/ACER 上永遠比 Mac 寫的 marker 新 → 瘦身永遠不會生效。
# 改成直接比對內容指紋（接力棒尾端 300 字是否出現在 CLAUDE.md 鏡像裡），跨機通用且更準。
$mirrorFresh = $false
$claudeMdPath = Join-Path $workspace "CLAUDE.md"
if ((Test-Path $claudeMdPath) -and (Test-Path $handoff)) {
    try {
        $handoffRaw = Get-Content $handoff -Raw -Encoding UTF8
        if ($handoffRaw.Length -gt 400) {
            $probe = $handoffRaw.Substring($handoffRaw.Length - 300).Trim()
            $claudeMdRaw = Get-Content $claudeMdPath -Raw -Encoding UTF8
            if ($probe -and $claudeMdRaw.Contains($probe)) { $mirrorFresh = $true }
        }
    } catch { $mirrorFresh = $false }
}
if ($mirrorFresh) {
    Write-Output "（接力棒全文已透過 workspace/CLAUDE.md 自動鏡像注入，內容與 JUNSHI_HANDOFF_LATEST.md 一致，不重複貼上。若這是這場對話第一則訊息卻沒看到 CLAUDE.md 內容，代表鏡像沒生效，請直接讀 ``JUNSHI_HANDOFF_LATEST.md`` 原檔。）"
} else {
    Write-Output "⚠️（CLAUDE.md 鏡像非最新，改為完整貼上，確保接力棒不漏接）"
    Write-Output ""
    Get-Content -Path $handoff -Encoding UTF8 | ForEach-Object { Write-Output $_ }
}

# ───────── 注入 JUNSHI_RULES.md（三機共讀軍師鐵律正典）─────────
$junshiRules = if ($env:JUNSHI_HOOK_ROOT) {
    Join-Path $env:JUNSHI_HOOK_ROOT "mac-openclaw-workflows\JUNSHI_RULES.md"
} else {
    Join-Path (Split-Path $workspace -Parent) "mac-openclaw-workflows\JUNSHI_RULES.md"
}
if (Test-Path $junshiRules) {
    Write-Output ""
    Write-Output "---"
    Write-Output ""
    Write-Output "## 🔴 軍師鐵律正典（雲端三機共讀，本場開工注入）"
    Write-Output ""
    Get-Content $junshiRules -Raw -Encoding UTF8
}

# ───────── 第 2 步：HEARTBEAT 熱上下文 ─────────
if (Test-Path $heartbeatPath) {
    Write-Output ""
    Write-Output "---"
    Write-Output ""
    Write-Output "## 🩺 第 2 步：HEARTBEAT.md（最近 50 行熱上下文）"
    Write-Output ""
    Get-Content -Path $heartbeatPath -Encoding UTF8 -Tail 50 | ForEach-Object { Write-Output $_ }
}

# ───────── 第 3 步：血淚試金石 ─────────
# 3a：Top10高頻模式一句話摘要（2026-08-31新增，避免只看「最新案例」漏接3個月前但還沒解決的舊模式，跟Mac版對等）
if (Test-Path $top10IndexPath) {
    Write-Output ""
    Write-Output "---"
    Write-Output ""
    Write-Output "## 🔴 第 3 步 (3a)：Top10 高頻失敗模式一句話比對（開工當下先掃過，命中就照做法走）"
    Write-Output ""
    $top10Lines = Get-Content -Path $top10IndexPath -Encoding UTF8
    $header = ""
    foreach ($line in $top10Lines) {
        if ($line -match '^## 🔴 模式') { $header = $line }
        if ($line -match '^\*\*觸發詞\*\*' -and $header -ne "") {
            Write-Output $header
            Write-Output $line
            Write-Output ""
        }
    }
    Write-Output "（完整版含涉及案例編號/自動化防護狀態，見 distill/top10_errors_index.md）"
}

# 3b：最新2案例全文
if (Test-Path $stonePath) {
    Write-Output ""
    Write-Output "---"
    Write-Output ""
    Write-Output "## 🔴 第 3 步 (3b)：血淚試金石最新 2 案例全文（守則 #07 同處跌倒鐵律）"
    Write-Output ""
    $stoneLines = Get-Content -Path $stonePath -Encoding UTF8
    $caseIdx = @()
    for ($i = 0; $i -lt $stoneLines.Count; $i++) {
        if ($stoneLines[$i] -match '^## 案例') { $caseIdx += $i }
    }
    if ($caseIdx.Count -ge 3) {
        $startLine = $caseIdx[$caseIdx.Count - 3]
        $stoneLines[$startLine..($stoneLines.Count - 1)] | ForEach-Object { Write-Output $_ }
    } elseif ($caseIdx.Count -gt 0) {
        $startLine = $caseIdx[0]
        $stoneLines[$startLine..($stoneLines.Count - 1)] | ForEach-Object { Write-Output $_ }
    } else {
        Write-Output "（無法定位案例段落，請手動查閱 試金石\試金石_案例庫.md）"
    }
}

# ───────── 第 4 步：knowledges 近 7 天新檔清單 ─────────
if (Test-Path $knowledgesDir) {
    Write-Output ""
    Write-Output "---"
    Write-Output ""
    Write-Output "## 📚 第 4 步：knowledges/ 最近 7 天新建/修改檔案清單"
    Write-Output ""
    $weekAgo = (Get-Date).AddDays(-7)
    $recentFiles = Get-ChildItem -Path $knowledgesDir -Filter "*.md" -File -ErrorAction SilentlyContinue |
                   Where-Object { $_.LastWriteTime -gt $weekAgo } |
                   Sort-Object Name
    if ($recentFiles.Count -gt 0) {
        foreach ($f in $recentFiles) {
            $firstLine = ""
            try {
                $firstLine = (Get-Content -Path $f.FullName -Encoding UTF8 -TotalCount 1) -replace '^# ', ''
            } catch {}
            Write-Output "- ``$($f.Name)``：$firstLine"
        }
    } else {
        Write-Output "（過去 7 天無新檔）"
    }
}

# ───────── 第 5 步：memory 最新日 ─────────
if (Test-Path $memoryDir) {
    $latestMemory = Get-ChildItem -Path $memoryDir -Filter "20*.md" -File -ErrorAction SilentlyContinue |
                    Where-Object { $_.Name -match '^\d{4}-\d{2}-\d{2}\.md$' } |
                    Sort-Object Name | Select-Object -Last 1
    if ($latestMemory) {
        Write-Output ""
        Write-Output "---"
        Write-Output ""
        Write-Output "## 🧠 第 5 步：memory 最新日（$($latestMemory.Name)）"
        Write-Output ""
        Get-Content -Path $latestMemory.FullName -Encoding UTF8 | ForEach-Object { Write-Output $_ }
    }
}

# ───────── 最新一場 SESSION 總結（保留原行為）─────────
if ($latestSession) {
    Write-Output ""
    Write-Output "---"
    Write-Output ""
    Write-Output "## 📂 最新一場 session 總結（$($latestSession.Name)）"
    Write-Output ""
    Get-Content -Path $latestSession.FullName -Encoding UTF8 | ForEach-Object { Write-Output $_ }
}

# ───────── 第 6 步：上線回應要求 ─────────
Write-Output ""
Write-Output "---"
Write-Output ""
Write-Output "## ✅ 第 6 步：上線回應要求（2026-09-24根源改版：開工不唸待辦）"
Write-Output "讀完本段後，回應**不超過5行**，只包含："
Write-Output "- 「我已讀完接力棒」＋身份核對（模型版本 + Windows 桌面版 GUI）＋雲端同步 HEAD hash 前 7 碼，一行講完"
Write-Output "- 待辦表「🙋要教練決定」區裡**還沒問過**的項目（通常是零件；零件就完全不提待辦）"
Write-Output "- 詢問教練「今天從哪件事開始？」"
Write-Output "**禁止**：唸「🤫等教練自己提起」區、唸「🔧AI自己的工作清單」、列舉上一棒戰果、自己發現的系統異常。這些是AI自己的事，自己處理。"
Write-Output ""
Write-Output "## 🚦 本場全程適用：問教練之前的三關（2026-09-24教練：「同一類事情不要再重複來煩我了」）"
Write-Output "任何時候（開工、健檢、全都釋放、總結、任務中途）要拿一件事去問教練或請教練決定，必須三關全過，少一關就不准問："
Write-Output "① **只有教練能做**：花錢、代表教練對外發言、不可逆操作、教練自己的內容與喜好、需要教練本人登入帳密。AI查得到、做得到、判斷得了的，自己處理。"
Write-Output "② **教練沒答過**：先查待辦表、封存檔、記憶檔。教練裁示過的（含「不用管」「略過」「到此為止」「保留就好」），換任何說法都不准再問。"
Write-Output "③ **現在不問會卡住**：教練正在等結果，或幾天內有期限。不急的寫進「🤫等教練自己提起」區，不主動提。"
Write-Output "**每件事最多問一次**：問過沒回應＝教練現在不想處理，移到🤫區，不追問。"
Write-Output "過不了三關的事：AI自己做完（不用報告細節，最多一行帶過），或安靜寫進🤫區。"
Write-Output ""

# 寫 self-test 到 HEARTBEAT（如果存在）
if (Test-Path $heartbeatPath) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm"
    $triggerPreview = if ($prompt.Length -gt 40) { $prompt.Substring(0, 40) } else { $prompt }
    $selfTest = @"

## 🩺 軍師 Hook 自檢 $ts（Windows v3 六步驟注入）
- ✅ Hook 觸發 + git pull + 六步驟內容注入完成
- 觸發詞：$triggerPreview
- 雲端狀態：$pullStatus
- Session: $sessionId
"@
    try { Add-Content -Path $heartbeatPath -Value $selfTest -Encoding UTF8 } catch {}
}

if ($sessionId) { New-Item -ItemType File -Path $marker -Force | Out-Null }
exit 0
