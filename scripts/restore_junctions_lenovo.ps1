# 聯想筆電（TREE）一鍵還原後重建 Junction 腳本
# 用途：一鍵還原把 C 碟清空後，用系統管理員身分執行本腳本，重建所有 junction
# 建立日期：2026-07-11（比照 ACER restore_junctions_acer.ps1 驗證過的架構撰寫）
#
# 使用方式：以系統管理員身分開 PowerShell，執行：
#   powershell -ExecutionPolicy Bypass -File "E:\Claude-Data\restore_junctions_lenovo.ps1"

$ErrorActionPreference = 'Continue'

Write-Host "=== 聯想筆電 Junction 重建腳本 ===" -ForegroundColor Cyan
Write-Host ""

$junctions = @(
    @{
        Link   = "C:\Users\bymyw\AppData\Local\LINE\Data"
        Target = "E:\Claude-Data\LINE-Data"
        Note   = "LINE 聊天記錄（新版 bin 留 C 碟）"
    },
    @{
        Link   = "C:\Users\bymyw\AppData\Local\LINE\Cache"
        Target = "E:\Claude-Data\LINE-Cache"
        Note   = "LINE 暫存圖片"
    },
    @{
        Link   = "C:\Users\bymyw\AppData\Local\Google\Chrome\User Data"
        Target = "E:\Claude-Data\AppData\Chrome-User-Data"
        Note   = "Chrome 書籤/密碼/擴充/瀏覽記錄（只 junction User Data，Application 程式本體留 C 碟，絕不整包搬——2026-07-11 搬移驗證）"
    },
    @{
        Link   = "C:\Users\bymyw\AppData\Local\GanJing\User Data"
        Target = "E:\Claude-Data\AppData\GanJing-User-Data"
        Note   = "乾淨世界瀏覽器（只 junction User Data，程式本體在 AppData\Roaming\Gan Jing Browser，不搬——跟 ACER 同款架構）"
    },
    @{
        Link   = "C:\Users\bymyw\AppData\Roaming\Signal"
        Target = "E:\Claude-Data\AppData\Signal"
        Note   = "Signal（無路徑驗證問題，整包 junction 沒問題）"
    },
    @{
        Link   = "C:\Users\bymyw\AppData\Roaming\Zoom"
        Target = "E:\Claude-Data\AppData\Zoom"
        Note   = "Zoom（目前是整包搬，非ACER的data/logs/reports分拆版；還原後若瀏覽器點會議連結偵測不到已安裝，直接去 zoom.us 重裝一次即可，見 feedback_zoom_junction_reinstall.md）"
    },
    @{
        Link   = "C:\Users\bymyw\AppData\Roaming\Claude\vm_bundles"
        Target = "E:\Claude-Data\AppData\Claude-vm_bundles"
        Note   = "Claude 桌面版沙盒環境資料"
    },
    @{
        Link   = "C:\Users\bymyw\.claude\projects\E--Claude-Data\memory"
        Target = "E:\Claude-Data\mac-openclaw-workflows\claude-brain"
        Note   = "三機共用大腦記憶（最優先，其他步驟失敗也要確保這條先接回）"
    }
)

$ok = 0
$fail = 0

foreach ($j in $junctions) {
    Write-Host "--- $($j.Note) ---"

    if (-not (Test-Path $j.Target)) {
        Write-Host "  SKIP: E 碟來源不存在 $($j.Target)" -ForegroundColor Yellow
        $fail++
        continue
    }

    $parent = Split-Path $j.Link -Parent
    if (-not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
        Write-Host "  Created parent: $parent"
    }

    if (Test-Path $j.Link) {
        $item = Get-Item $j.Link -Force
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            Write-Host "  SKIP: Junction already exists" -ForegroundColor Green
            $ok++
            continue
        }
        $bak = "$($j.Link).bak.restored.$(Get-Date -Format yyyyMMdd)"
        Rename-Item $j.Link $bak -ErrorAction SilentlyContinue
        Write-Host "  Renamed existing folder -> $bak"
    }

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
Write-Host "  - Zoom 目前是整包 junction，還原後若會議連結偵測不到已安裝，去 zoom.us 重裝一次即可，不用花時間診斷"
Write-Host "  - Comet（Perplexity）瀏覽器目前尚未啟用 junction，還原後是全新資料，不受影響（E 碟上的舊備份是測試期殘留，非現役資料）"
Write-Host "  - Chrome/GanJing：絕對不要整包 junction AppData\Local\<瀏覽器>，只能 junction User Data 子資料夾，教訓見 acer-post-restore-todo.md 的慘痛經驗（整包搬移遺失過帳號設定）"
Write-Host "  - 還原後務必請教練親自打開每套軟體，肉眼確認資料還在，不是只看程式能不能開"
