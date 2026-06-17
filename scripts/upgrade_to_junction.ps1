# Windows .claude 目錄 Junction 升級腳本 v1
#
# 目的：把 C:\Users\<user>\.claude → 變成 junction 指向 E:\Claude-Data\.claude
#       讓 Claude Code 永遠讀 C 槽路徑、但實際讀寫 E 槽真檔
#       一鍵還原洗 C 槽 → junction 沒了 → 真檔還在 E 槽 → 重做 junction 一行搞定
#
# 教練親口（2026-06-18 凌晨 4 點半）：
#   「其實之前 windows 早就寫過同樣的指令，所有讀取 C 時都會指向 E
#    只是我前幾天一鍵還原，然後 E 又被整個清除，所以現在才會這麼麻煩」
#
# 教練暗號：「裝 junction」

param(
    [string]$TargetReal = "E:\Claude-Data\.claude",
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$cClaude = Join-Path $env:USERPROFILE ".claude"
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔗 .claude Junction 升級 v1" -ForegroundColor Cyan
Write-Host "  C 槽路徑 → E 槽真檔 (Junction Point)" -ForegroundColor DarkGray
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "C 槽路徑: $cClaude"
Write-Host "E 槽真檔: $TargetReal"
if ($DryRun) { Write-Host "🧪 DRY-RUN 模式：只看不做" -ForegroundColor Yellow }
Write-Host ""

# ───────── 0. 預檢 ─────────
Write-Host "[0/6] 預檢..." -ForegroundColor Yellow
$cExists = Test-Path $cClaude
$cIsJunction = $false
if ($cExists) {
    $item = Get-Item $cClaude -Force
    $cIsJunction = ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0
}
if ($cIsJunction) {
    $targetCurrent = (Get-Item $cClaude -Force).Target
    if ($targetCurrent -eq $TargetReal) {
        Write-Host "  ✅ $cClaude 已經是 junction 指向 $TargetReal——免升級" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "  ⚠️  $cClaude 是 junction 但指向 $targetCurrent，將重建" -ForegroundColor Yellow
    }
}
if (-not (Test-Path $TargetReal)) {
    if ($DryRun) {
        Write-Host "  [Dry-run] 會建立 $TargetReal" -ForegroundColor Cyan
    } else {
        New-Item -ItemType Directory -Path $TargetReal -Force | Out-Null
        Write-Host "  📁 建立 $TargetReal" -ForegroundColor Cyan
    }
}

# ───────── 1. 列 C 槽 .claude 內容（讓教練看有什麼會被合併）─────────
Write-Host "`n[1/6] 掃描 C 槽 .claude 內容..." -ForegroundColor Yellow
if ($cExists -and -not $cIsJunction) {
    $cContents = Get-ChildItem $cClaude -Force -ErrorAction SilentlyContinue
    if ($cContents) {
        Write-Host "  C 槽 .claude 包含：" -ForegroundColor Cyan
        $cContents | ForEach-Object {
            $size = if ($_.PSIsContainer) { "(目錄)" } else { "$([math]::Round($_.Length/1KB,1)) KB" }
            Write-Host "    - $($_.Name) $size" -ForegroundColor DarkGray
        }
    } else {
        Write-Host "  C 槽 .claude 是空目錄" -ForegroundColor DarkGray
    }
} else {
    Write-Host "  C 槽 .claude 不存在或已是 junction，跳過掃描" -ForegroundColor DarkGray
}

# ───────── 2. 合併 C 槽內容到 E 槽（保留兩邊資料）─────────
Write-Host "`n[2/6] 合併 C 槽 → E 槽（不覆蓋 E 槽 newer 的）..." -ForegroundColor Yellow
if ($cExists -and -not $cIsJunction) {
    $mergeCount = 0
    Get-ChildItem $cClaude -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {
        $relativePath = $_.FullName.Substring($cClaude.Length).TrimStart('\')
        $destPath = Join-Path $TargetReal $relativePath
        if ($_.PSIsContainer) {
            if (-not (Test-Path $destPath)) {
                if (-not $DryRun) { New-Item -ItemType Directory -Path $destPath -Force | Out-Null }
                $mergeCount++
            }
        } else {
            $shouldCopy = $true
            if (Test-Path $destPath) {
                $destItem = Get-Item $destPath -Force
                if ($destItem.LastWriteTime -ge $_.LastWriteTime) {
                    $shouldCopy = $false
                    Write-Host "    ⏭️  跳過（E 槽較新）: $relativePath" -ForegroundColor DarkGray
                }
            }
            if ($shouldCopy) {
                if (-not $DryRun) { Copy-Item $_.FullName $destPath -Force }
                Write-Host "    📥 $relativePath" -ForegroundColor DarkGray
                $mergeCount++
            }
        }
    }
    Write-Host "  ✅ 合併 $mergeCount 個項目（C → E）" -ForegroundColor Green
} else {
    Write-Host "  跳過合併（C 槽不存在或已是 junction）" -ForegroundColor DarkGray
}

# ───────── 3. 重命名 C 槽 .claude 為 .bak（可逆 backup，不直接刪）─────────
Write-Host "`n[3/6] 重命名 C 槽 .claude 為 .bak（可逆）..." -ForegroundColor Yellow
$bakPath = "$cClaude.bak.junctionupgrade.$timestamp"
if ($cExists -and -not $cIsJunction) {
    if ($DryRun) {
        Write-Host "  [Dry-run] 會 rename $cClaude → $bakPath" -ForegroundColor Cyan
    } else {
        Rename-Item -Path $cClaude -NewName ".claude.bak.junctionupgrade.$timestamp"
        Write-Host "  ✅ 已備份: $bakPath" -ForegroundColor Green
        Write-Host "  （確認 junction 運作正常後可手動刪除）" -ForegroundColor DarkGray
    }
} elseif ($cIsJunction) {
    if ($DryRun) {
        Write-Host "  [Dry-run] 會移除舊 junction $cClaude（不是真實目錄，移除安全）" -ForegroundColor Cyan
    } else {
        # junction 用 Remove-Item 只刪連結，不刪目標——安全
        Remove-Item $cClaude -Force
        Write-Host "  ✅ 已移除舊 junction（E 槽真檔不受影響）" -ForegroundColor Green
    }
} else {
    Write-Host "  C 槽 .claude 不存在，跳過備份" -ForegroundColor DarkGray
}

# ───────── 4. 建 Junction：C → E ─────────
Write-Host "`n[4/6] 建立 Junction Point..." -ForegroundColor Yellow
if ($DryRun) {
    Write-Host "  [Dry-run] 會執行: cmd /c mklink /J `"$cClaude`" `"$TargetReal`"" -ForegroundColor Cyan
} else {
    $mklinkResult = & cmd /c mklink /J "$cClaude" "$TargetReal" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Junction 建立成功：$mklinkResult" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Junction 建立失敗：$mklinkResult" -ForegroundColor Red
        Write-Host "  ⚠️  C 槽 .claude.bak 還在，可手動 rename 回 .claude 復原" -ForegroundColor Yellow
        exit 1
    }
}

# ───────── 5. 驗證 Junction 運作 ─────────
Write-Host "`n[5/6] 驗證 Junction..." -ForegroundColor Yellow
if (-not $DryRun) {
    $newItem = Get-Item $cClaude -Force
    $isJunctionNow = ($newItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0
    $targetNow = $newItem.Target
    if ($isJunctionNow -and ($targetNow -contains $TargetReal -or $targetNow -eq $TargetReal)) {
        Write-Host "  ✅ Junction 驗證通過" -ForegroundColor Green
        Write-Host "     $cClaude → $targetNow" -ForegroundColor DarkGray
    } else {
        Write-Host "  ⚠️  Junction 驗證異常" -ForegroundColor Yellow
        Write-Host "     IsJunction: $isJunctionNow / Target: $targetNow" -ForegroundColor DarkGray
    }

    # 測試讀寫穿透
    $settingsTest = Join-Path $cClaude "settings.json"
    if (Test-Path $settingsTest) {
        $realPath = Join-Path $TargetReal "settings.json"
        Write-Host "  ✅ 從 C 槽路徑可讀 settings.json，實際檔在 E 槽" -ForegroundColor Green
    }
} else {
    Write-Host "  [Dry-run] 略過驗證" -ForegroundColor DarkGray
}

# ───────── 6. 寫還原便條到 E 槽 ─────────
Write-Host "`n[6/6] 寫升級便條..." -ForegroundColor Yellow
$noteContent = @"
🔗 Windows .claude Junction 升級紀錄
========================================

升級時間：$(Get-Date -Format 'yyyy-MM-dd HH:mm') 台灣時間

【架構】
$cClaude  ← Claude Code 看到的路徑（junction）
    ↓ 解析到
$TargetReal  ← 真實檔案位置（E 槽）

【一鍵還原後怎麼修】
C 槽 .claude junction 會被洗掉，但 E 槽真檔還在。重建一行指令：
  cmd /c mklink /J "$cClaude" "$TargetReal"

或者直接重跑：
  powershell -ExecutionPolicy Bypass -File "$TargetReal\..\workspace\scripts\upgrade_to_junction.ps1"

【備份】
舊 C 槽 .claude 內容已 rename 為：
  $bakPath
確認 junction 運作正常後可手動刪除。
"@
$notePath = "E:\Claude-Data\一鍵還原後怎麼修.txt"
if (-not $DryRun) {
    Set-Content -Path $notePath -Value $noteContent -Encoding UTF8
    Write-Host "  ✅ 已寫: $notePath" -ForegroundColor Green
} else {
    Write-Host "  [Dry-run] 會寫便條到 $notePath" -ForegroundColor Cyan
}

# ───────── 最終報告 ─────────
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "🧪 Dry-run 完成——沒有實際變動，移除 -DryRun 才會真正執行" -ForegroundColor Yellow
} else {
    Write-Host "✅ Junction 升級完成" -ForegroundColor Green
}
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔗 Junction: $cClaude → $TargetReal"
Write-Host "💾 舊 C 槽備份: $bakPath（確認沒問題後可手動刪）"
Write-Host "📝 升級便條: E:\Claude-Data\一鍵還原後怎麼修.txt"
Write-Host ""
Write-Host "🔴 下一步：" -ForegroundColor Red
Write-Host "  1. 完全關閉 Claude Code 桌面版（退出進程）" -ForegroundColor White
Write-Host "  2. 重新開啟" -ForegroundColor White
Write-Host "  3. 開新對話打「開」→ 看到接力棒注入" -ForegroundColor White
Write-Host ""
Write-Host "從此以後 Claude Code 讀 C 槽路徑，實際讀寫 E 槽真檔，一鍵還原免疫。" -ForegroundColor Cyan
