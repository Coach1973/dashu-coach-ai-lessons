# ACER Junction 回滾腳本（還原到搬移前的狀態）
# 用途：某個軟體搬移後出問題，用本腳本把 junction 拆掉，還原 C 碟原資料
# 建立日期：2026-07-01
#
# 使用方式（以系統管理員身分開 PowerShell）：
#   全部回滾：powershell -ExecutionPolicy Bypass -File "D:\Claude-Data\rollback_junctions_acer.ps1"
#   單個回滾：powershell -ExecutionPolicy Bypass -File "D:\Claude-Data\rollback_junctions_acer.ps1" -Only LINE
#   可選值：LINE, Zoom, Telegram, Chrome, GanJing, Perplexity

param(
    [string]$Only = ""
)

$ErrorActionPreference = 'Continue'

$rollbacks = @(
    @{
        Name = "LINE"
        Links = @(
            @{ Link = "C:\Users\Administrator\AppData\Local\LINE\Data";  Bak = "C:\Users\Administrator\AppData\Local\LINE\Data.bak.20260701" },
            @{ Link = "C:\Users\Administrator\AppData\Local\LINE\Cache"; Bak = "C:\Users\Administrator\AppData\Local\LINE\Cache.bak.20260701" }
        )
        Kill = @("LINE","LineLauncher","LineCall","LineMediaPlayer")
    },
    @{
        Name = "Zoom"
        Links = @(
            @{ Link = "C:\Users\Administrator\AppData\Roaming\Zoom\data";    Bak = "" },
            @{ Link = "C:\Users\Administrator\AppData\Roaming\Zoom\logs";    Bak = "" },
            @{ Link = "C:\Users\Administrator\AppData\Roaming\Zoom\reports"; Bak = "" }
        )
        Kill = @("Zoom")
    },
    @{
        Name = "Telegram"
        Links = @(
            @{ Link = "C:\Users\Administrator\AppData\Roaming\Telegram Desktop"; Bak = "C:\Users\Administrator\AppData\Roaming\Telegram Desktop.bak.20260701" }
        )
        Kill = @("Telegram")
    },
    @{
        Name = "Chrome"
        Links = @(
            @{ Link = "C:\Users\Administrator\AppData\Local\Google"; Bak = "C:\Users\Administrator\AppData\Local\Google.bak.20260701" }
        )
        Kill = @("chrome")
    },
    @{
        Name = "GanJing"
        Links = @(
            @{ Link = "C:\Users\Administrator\AppData\Local\GanJing"; Bak = "C:\Users\Administrator\AppData\Local\GanJing.bak.20260701" }
        )
        Kill = @("Gan Jing Browser")
    },
    @{
        Name = "Perplexity"
        Links = @(
            @{ Link = "C:\Users\Administrator\AppData\Local\Perplexity"; Bak = "C:\Users\Administrator\AppData\Local\Perplexity.bak.20260701" }
        )
        Kill = @("Perplexity")
    }
)

Write-Host "=== ACER Junction 回滾腳本 ===" -ForegroundColor Cyan

if ($Only) {
    $rollbacks = $rollbacks | Where-Object { $_.Name -eq $Only }
    if (-not $rollbacks) {
        Write-Host "找不到 '$Only'，可選：LINE, Zoom, Telegram, Chrome, GanJing, Perplexity" -ForegroundColor Red
        exit 1
    }
    Write-Host "只回滾：$Only" -ForegroundColor Yellow
} else {
    Write-Host "回滾全部軟體" -ForegroundColor Yellow
}
Write-Host ""

foreach ($rb in $rollbacks) {
    Write-Host "--- $($rb.Name) ---"

    # 先關程式
    foreach ($proc in $rb.Kill) {
        Get-Process -Name $proc -ErrorAction SilentlyContinue | Stop-Process -Force
    }
    Start-Sleep 1

    foreach ($item in $rb.Links) {
        # 空 Bak = 純 unlink 模式（如 Zoom data/logs/reports，D 碟是唯一正本，沒有 C 碟副本）
        if ([string]::IsNullOrEmpty($item.Bak)) {
            if (Test-Path $item.Link) {
                $linkItem = Get-Item $item.Link -Force
                if ($linkItem.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                    cmd /c rmdir "$($item.Link)" 2>$null
                    Write-Host "  Removed junction (D 碟資料未受影響): $($item.Link)" -ForegroundColor Green
                } else {
                    Write-Host "  SKIP: 不是 junction，跳過 $($item.Link)" -ForegroundColor Yellow
                }
            } else {
                Write-Host "  SKIP: 路徑不存在 $($item.Link)" -ForegroundColor Yellow
            }
            continue
        }

        # 檢查備份是否存在
        if (-not (Test-Path $item.Bak)) {
            Write-Host "  SKIP: 備份不存在 $($item.Bak)" -ForegroundColor Yellow
            continue
        }

        # 移除 junction（junction 用 cmd /c rmdir 移除，不會刪 D 碟資料）
        if (Test-Path $item.Link) {
            $linkItem = Get-Item $item.Link -Force
            if ($linkItem.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                cmd /c rmdir "$($item.Link)" 2>$null
                Write-Host "  Removed junction: $($item.Link)"
            } else {
                $moved = "$($item.Link).moved.$(Get-Date -Format yyyyMMddHHmmss)"
                Rename-Item $item.Link $moved
                Write-Host "  Moved aside: $moved"
            }
        }

        # 把備份改名回原名
        Rename-Item $item.Bak $item.Link
        Write-Host "  Restored: $($item.Bak) -> $($item.Link)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "=== 回滾完成 ===" -ForegroundColor Green
Write-Host "D 碟的資料沒有被刪除，如果之後要重新搬移，資料還在。"
