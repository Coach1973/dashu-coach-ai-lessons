# organize_downloads.ps1
# 用途：自動整理下載資料夾
# 建立：2026-07-02
# 用法：
#   powershell -ExecutionPolicy Bypass -File .\organize_downloads.ps1                 (預覽，預設)
#   powershell -ExecutionPolicy Bypass -File .\organize_downloads.ps1 -Execute      (實際移動)

[CmdletBinding()]
param(
    [switch]$Execute,
    [string]$SourcePath = "D:\Users\Downloads"
)

# ===== 規則表 =====

# 檔名關鍵字規則（優先於副檔名）
$nameRules = @(
    @{ Pattern = '燈號|紅綠燈'; Folder = '燈號資料倉庫'; Description = 'BNI 燈號相關' }
    @{ Pattern = '^__-palms-___'; Folder = '燈號資料倉庫'; Description = 'Palms 系統匯出（推測燈號）' }
    @{ Pattern = '預算書|預算表'; Folder = 'Excel'; Description = '預算相關' }
)

# 副檔名規則
$extRules = @(
    @{ Exts = @('jpg','jpeg','png','gif','bmp','webp'); Folder = '圖片' }
    @{ Exts = @('pdf'); Folder = 'PDF' }
    @{ Exts = @('pptx','ppt'); Folder = 'PPT' }
    @{ Exts = @('docx','doc'); Folder = 'Word' }
    @{ Exts = @('xlsx','xls','csv'); Folder = 'Excel' }
    @{ Exts = @('mp4','mov','avi','mkv','m4v'); Folder = '影音資料' }
    @{ Exts = @('aac','m4a','wav','mp3','flac'); Folder = '會議音樂' }
    @{ Exts = @('exe','msi','rar','zip','7z'); Folder = '軟體安裝' }
)

# 跳過的檔案（檔名剛好是這些，不處理）
$skipPatterns = @('^123$')

# ===== 掃描並分類 =====
$plan = New-Object System.Collections.Generic.List[Object]

if (-not (Test-Path -LiteralPath $SourcePath)) {
    Write-Host "❌ 來源路徑不存在：$SourcePath" -ForegroundColor Red
    exit 1
}

Get-ChildItem -LiteralPath $SourcePath -File | ForEach-Object {
    $file = $_
    $name = $file.Name

    # 跳過特定檔案
    foreach ($skip in $skipPatterns) {
        if ($name -match $skip) { return }
    }

    # 檔名規則
    foreach ($rule in $nameRules) {
        if ($name -match $rule.Pattern) {
            $plan.Add([PSCustomObject]@{
                File   = $name
                Size   = $file.Length
                Target = $rule.Folder
                Reason = $rule.Description
            })
            return
        }
    }

    # 副檔名規則
    $ext = $file.Extension.ToLower().TrimStart('.')
    foreach ($rule in $extRules) {
        if ($rule.Exts -contains $ext) {
            $plan.Add([PSCustomObject]@{
                File   = $name
                Size   = $file.Length
                Target = $rule.Folder
                Reason = ".$ext 副檔名"
            })
            return
        }
    }

    # 沒分類到
    $plan.Add([PSCustomObject]@{
        File   = $name
        Size   = $file.Length
        Target = "⚠️ 未分類"
        Reason = "不符合任何規則"
    })
}

# ===== 顯示計劃 =====
Write-Host "`n📂 整理計劃" -ForegroundColor Cyan
Write-Host "來源：$SourcePath`n"

$totalSize = ($plan | Measure-Object -Property Size -Sum).Sum
Write-Host "共 $($plan.Count) 個檔案，總大小 $([math]::Round($totalSize/1MB, 2)) MB`n"

$grouped = $plan | Group-Object -Property Target | Sort-Object Name
foreach ($group in $grouped) {
    $color = if ($group.Name -eq "⚠️ 未分類") { "Red" } else { "Yellow" }
    Write-Host "[$($group.Name)] $($group.Count) 個檔案" -ForegroundColor $color
    $group.Group | Sort-Object File | ForEach-Object {
        $sizeMB = [math]::Round($_.Size / 1MB, 2)
        Write-Host "  $($_.File) ($sizeMB MB) — $($_.Reason)"
    }
    Write-Host ""
}

# 找出未分類的
$uncategorized = $plan | Where-Object { $_.Target -eq "⚠️ 未分類" }
if ($uncategorized) {
    Write-Host "⚠️  以上未分類的檔案「不會被移動」，請手動處理" -ForegroundColor Red
}

# 大檔警告
$bigFiles = $plan | Where-Object { $_.Size -gt 100MB -and $_.Target -ne "⚠️ 未分類" }
if ($bigFiles) {
    Write-Host "`n⚠️  超過 100MB 的大檔：" -ForegroundColor Magenta
    $bigFiles | ForEach-Object { Write-Host "  $($_.File) $([math]::Round($_.Size/1MB,2)) MB" }
}

# ===== 執行 =====
# 雙擊/右鍵「使用 PowerShell 執行」時 $Execute 不會被設定，改用互動詢問；
# 命令列已明確加 -Execute 的情況（例如排程或其他腳本呼叫）就不再重複詢問。
$doExecute = $Execute
if (-not $doExecute -and $plan.Count -gt 0) {
    Write-Host "`n💡 這是預覽模式，尚未搬動任何檔案。" -ForegroundColor Cyan
    $answer = Read-Host "要照上面的計劃實際搬移嗎？輸入 Y 執行，其他任意鍵取消"
    if ($answer -match '^[Yy]$') {
        $doExecute = $true
    }
}

if ($doExecute) {
    Write-Host "`n🚀 開始移動..." -ForegroundColor Green
    $moved = 0
    $failed = 0
    foreach ($item in $plan) {
        if ($item.Target -eq "⚠️ 未分類") { continue }
        $src = Join-Path $SourcePath $item.File
        $dstDir = Join-Path $SourcePath $item.Target
        $dst = Join-Path $dstDir $item.File
        try {
            if (-not (Test-Path -LiteralPath $dstDir)) {
                New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
                Write-Host "  📁 建立資料夾：$item.Target" -ForegroundColor DarkGray
            }
            if (Test-Path -LiteralPath $dst) {
                Write-Host "  ⚠️  跳過（目標已存在）：$($item.File)" -ForegroundColor Yellow
                continue
            }
            Move-Item -LiteralPath $src -Destination $dstDir
            $moved++
        } catch {
            Write-Host "  ❌ 失敗：$($item.File) — $_" -ForegroundColor Red
            $failed++
        }
    }
    Write-Host "`n✅ 完成！移動 $moved 個檔案，失敗 $failed 個" -ForegroundColor Green
} else {
    Write-Host "`n💡 已取消，沒有搬動任何檔案。" -ForegroundColor Cyan
}

# 雙擊/右鍵執行時視窗跑完會直接關掉，加暫停讓結果看得到
if ($Host.Name -eq 'ConsoleHost') {
    Write-Host ""
    Read-Host "按 Enter 鍵結束"
}
