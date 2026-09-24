# ============================================================
# 🗑️🔒 Windows 刪檔鎖 PowerShell 版（2026-06-17 軍師建立）
#
# 起因：試金石案例 24——Windows 桌面版軍師清 TEMP 時 `$temp` 變數
#       跨 shell 跳脫失敗變空字串，Remove-Item -Recurse -Force 從當前
#       目錄遞迴刪，E 槽 636 GB 蒸發。
#
# Mac 版同源：scripts/delete_guard.sh（案例 23 21 GB 血淚而生）
#
# 設計原理：所有不可逆刪除動作必須走這個函式，函式內強制驗證：
#   1. 目標必硬編碼絕對路徑（禁止變數作為唯一來源）
#   2. 必先 Test-Path 確認存在
#   3. 必先計算受影響大小，超過閾值就拒絕
#   4. 必先列出將被刪的內容預覽
#   5. 需要通行證（教練親口同意 10 分鐘內有效）
#
# 通行證發行（教練親口同意刪除之後）：
#   New-Item -ItemType File -Force "$env:USERPROFILE\.openclaw\workspace\state\DELETE_APPROVED"
#
# 使用方式：
#   . "$env:USERPROFILE\.openclaw\workspace\scripts\delete_guard.ps1"
#   Safe-Remove -LiteralPath "C:\some\absolute\path" -MaxGB 1
# ============================================================

function Test-DeleteApproved {
    $token = "$env:USERPROFILE\.openclaw\workspace\state\DELETE_APPROVED"
    if (-not (Test-Path $token)) { return $false }
    $age = (Get-Date) - (Get-Item $token).LastWriteTime
    if ($age.TotalMinutes -gt 10) {
        Remove-Item -LiteralPath $token -Force -ErrorAction SilentlyContinue
        return $false
    }
    return $true
}

function Get-PathSizeGB {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return 0 }
    try {
        $bytes = (Get-ChildItem -LiteralPath $Path -Recurse -Force -ErrorAction SilentlyContinue |
                  Measure-Object -Property Length -Sum).Sum
        if (-not $bytes) { return 0 }
        return [math]::Round($bytes / 1GB, 2)
    } catch { return -1 }
}

function Safe-Remove {
    <#
    .SYNOPSIS
        防呆版的 Remove-Item，強制執行教練鐵律：絕對路徑 + 預驗證 + 通行證。
    .PARAMETER LiteralPath
        必填，目標的完整絕對路徑（禁止用變數作為唯一來源——呼叫前先 echo 顯示出來）
    .PARAMETER MaxGB
        允許刪除的最大 GB 數，超過就拒絕。預設 1 GB。
    .PARAMETER Recurse
        遞迴刪除。
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$LiteralPath,
        [double]$MaxGB = 1,
        [switch]$Recurse
    )

    Write-Host "🗑️🔒 Safe-Remove 驗證流程啟動" -ForegroundColor Yellow

    # 鐵律 1：必須絕對路徑
    if (-not [System.IO.Path]::IsPathRooted($LiteralPath)) {
        Write-Host "❌ 拒絕：目標必須是絕對路徑（你傳的：'$LiteralPath'）" -ForegroundColor Red
        return
    }

    # 鐵律 2：禁止當前工作目錄、家目錄、磁碟根目錄
    $forbidden = @(
        "$env:USERPROFILE",
        "$env:USERPROFILE\Desktop",
        "$env:USERPROFILE\Documents",
        "$env:USERPROFILE\Downloads",
        "C:\", "D:\", "E:\", "F:\", "G:\",
        "C:\Windows", "C:\Program Files", "C:\Program Files (x86)",
        (Get-Location).Path
    )
    foreach ($f in $forbidden) {
        if ($LiteralPath.TrimEnd('\') -ieq $f.TrimEnd('\')) {
            Write-Host "❌ 拒絕：禁止刪除根目錄/家目錄/當前工作目錄：'$LiteralPath'" -ForegroundColor Red
            return
        }
    }

    # 鐵律 3：必須存在
    if (-not (Test-Path -LiteralPath $LiteralPath)) {
        Write-Host "❌ 拒絕：路徑不存在 '$LiteralPath'" -ForegroundColor Red
        return
    }

    # 鐵律 4：計算大小
    $sizeGB = Get-PathSizeGB -Path $LiteralPath
    Write-Host "📊 目標大小：$sizeGB GB" -ForegroundColor Cyan

    if ($sizeGB -gt $MaxGB) {
        Write-Host "❌ 拒絕：受影響大小 $sizeGB GB 超過上限 $MaxGB GB" -ForegroundColor Red
        Write-Host "    若確認要刪，請呼叫時加上 -MaxGB $([math]::Ceiling($sizeGB))" -ForegroundColor Red
        Write-Host "    且必須先取得教練親口通行證：" -ForegroundColor Red
        Write-Host "    New-Item -ItemType File -Force `"$env:USERPROFILE\.openclaw\workspace\state\DELETE_APPROVED`"" -ForegroundColor Red
        return
    }

    # 鐵律 5：超過 100 MB 必須有通行證
    if ($sizeGB -gt 0.1) {
        if (-not (Test-DeleteApproved)) {
            Write-Host "❌ 拒絕：超過 100 MB 的刪除必須有教練通行證（10 分鐘內有效）" -ForegroundColor Red
            Write-Host "    教練同意後執行：" -ForegroundColor Red
            Write-Host "    New-Item -ItemType File -Force `"$env:USERPROFILE\.openclaw\workspace\state\DELETE_APPROVED`"" -ForegroundColor Red
            return
        }
        Write-Host "✅ 通行證有效" -ForegroundColor Green
    }

    # 鐵律 6：列出將被刪的前 10 項預覽
    Write-Host "📋 將刪除（前 10 項預覽）：" -ForegroundColor Yellow
    Get-ChildItem -LiteralPath $LiteralPath -Force -ErrorAction SilentlyContinue |
        Select-Object -First 10 | Format-Table Name, Length, LastWriteTime

    # 執行
    Write-Host "🚮 開始刪除：$LiteralPath" -ForegroundColor Magenta
    if ($Recurse) {
        Remove-Item -LiteralPath $LiteralPath -Recurse -Force
    } else {
        Remove-Item -LiteralPath $LiteralPath -Force
    }
    Write-Host "✅ 刪除完成" -ForegroundColor Green
}

Write-Host "🗑️🔒 delete_guard.ps1 載入完成。所有刪除請改用 Safe-Remove。" -ForegroundColor Green
Write-Host "    禁止直接呼叫 Remove-Item -Recurse -Force（執行細則 N6）。" -ForegroundColor Yellow
