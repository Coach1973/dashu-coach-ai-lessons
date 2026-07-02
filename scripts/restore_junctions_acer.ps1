# ACER 一鍵還原後重建 Junction 腳本
# 用途：一鍵還原把 C 碟清空後，用系統管理員身分執行本腳本，重建所有 junction
# 建立日期：2026-07-01
#
# 使用方式：以系統管理員身分開 PowerShell，執行：
#   powershell -ExecutionPolicy Bypass -File "D:\Claude-Data\restore_junctions_acer.ps1"

$ErrorActionPreference = 'Continue'

Write-Host "=== ACER Junction 重建腳本 ===" -ForegroundColor Cyan
Write-Host ""

$junctions = @(
    @{
        Link   = "C:\Users\Administrator\AppData\Local\LINE\Data"
        Target = "D:\Claude-Data\LINE-Data"
        Note   = "LINE 聊天記錄（26.x 新版 bin 留 C 碟）"
    },
    @{
        Link   = "C:\Users\Administrator\AppData\Local\LINE\Cache"
        Target = "D:\Claude-Data\LINE-Cache"
        Note   = "LINE 暫存圖片"
    },
    @{
        Link   = "C:\Users\Administrator\AppData\Roaming\Zoom\data"
        Target = "D:\Claude-Data\Zoom-Roaming\data"
        Note   = "Zoom 使用者資料（2026-07-02 改法：bin 留 C 碟，只 junction 增量資料，不用整包重搬）"
    },
    @{
        Link   = "C:\Users\Administrator\AppData\Roaming\Zoom\logs"
        Target = "D:\Claude-Data\Zoom-Roaming\logs"
        Note   = "Zoom 日誌"
    },
    @{
        Link   = "C:\Users\Administrator\AppData\Roaming\Zoom\reports"
        Target = "D:\Claude-Data\Zoom-Roaming\reports"
        Note   = "Zoom 報告"
    },
    @{
        Link   = "C:\Users\Administrator\AppData\Roaming\Telegram Desktop"
        Target = "D:\Claude-Data\Telegram-Desktop"
        Note   = "Telegram 聊天記錄"
    },
    @{
        Link   = "C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
        Target = "D:\Claude-Data\Google-Chrome-UserData"
        Note   = "Chrome 書籤/密碼/擴充/瀏覽記錄（只 junction User Data，Application 程式本體留 C 碟，絕不整包搬——見 feedback_browser_no_full_junction.md）"
    },
    @{
        Link   = "C:\Users\Administrator\AppData\Local\GanJing\User Data"
        Target = "D:\Claude-Data\GanJing-Local"
        Note   = "GanJing 乾淨世界瀏覽器（2026-07-02 改法：比照 Chrome，只 junction User Data，程式本體在 AppData\Roaming\Gan Jing Browser，不搬）"
    },
    @{
        Link   = "C:\Users\Administrator\AppData\Local\Perplexity\Comet\User Data"
        Target = "D:\Claude-Data\Perplexity-UserData"
        Note   = "Perplexity Comet 瀏覽器（尚未實際搬移，D 碟來源不存在會自動 SKIP，之後要搬比照 GanJing 做法）"
    }
)

$ok = 0
$fail = 0

foreach ($j in $junctions) {
    Write-Host "--- $($j.Note) ---"

    # 檢查 D 碟來源是否存在
    if (-not (Test-Path $j.Target)) {
        Write-Host "  SKIP: D 碟來源不存在 $($j.Target)" -ForegroundColor Yellow
        $fail++
        continue
    }

    # 確保父目錄存在
    $parent = Split-Path $j.Link -Parent
    if (-not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
        Write-Host "  Created parent: $parent"
    }

    # 如果 Link 位置已經是 junction，跳過
    if (Test-Path $j.Link) {
        $item = Get-Item $j.Link -Force
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            Write-Host "  SKIP: Junction already exists" -ForegroundColor Green
            $ok++
            continue
        }
        # 如果是普通資料夾（還原後新建的），改名備份
        $bak = "$($j.Link).bak.restored.$(Get-Date -Format yyyyMMdd)"
        Rename-Item $j.Link $bak -ErrorAction SilentlyContinue
        Write-Host "  Renamed existing folder -> $bak"
    }

    # 建 junction
    $result = cmd /c mklink /J "$($j.Link)" "$($j.Target)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK: $result" -ForegroundColor Green
        $ok++
    } else {
        Write-Host "  FAIL: $result" -ForegroundColor Red
        $fail++
    }
}

Write-Host ""
Write-Host "=== 完成：$ok 成功 / $fail 失敗 ===" -ForegroundColor $(if ($fail -eq 0) { 'Green' } else { 'Yellow' })
Write-Host ""
Write-Host "提醒：" -ForegroundColor Cyan
Write-Host "  - Zoom 的 bin/程式本體沒有 junction，C 碟被清空後仍需重新安裝（zoom.us 下載）"
Write-Host "    重裝完成後直接跑本腳本，data/logs/reports 會自動接回 D 碟舊資料，不必再手動搬一次"
Write-Host "  - LINE 如果版本升級到新版，bin 可能需要重裝"
Write-Host "  - Chrome/GanJing/Perplexity：絕對不要整包 junction AppData\Local\<瀏覽器>，只能 junction User Data 子資料夾，教訓見 feedback_browser_no_full_junction.md（已因整包搬移遺失過兩次帳號）"
