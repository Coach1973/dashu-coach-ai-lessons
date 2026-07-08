# 任務：Discord / GanJing / Microsoft 三項 C 槽搬家指示（給佩佩老師電腦）

> 設計者：聯想機軍師 Sonnet 5 ｜ 2026-07-08
> 起因：教練決定這三項也要搬，不只是「跳過寫報告」

---

## 總原則（三項都要遵守，來自案例 30/41 血淚教訓）

1. **只搬「使用者資料/Profile」子資料夾，絕對不要整個 App 資料夾搬**——程式本體跟使用者資料常常混在一起，整包搬會讓程式壞掉（案例 30：Comet 瀏覽器帳號全部遺失）
2. **搬家前先檢查目標子資料夾內部有沒有巢狀 Junction**（案例 41 教訓）：
   ```powershell
   Get-ChildItem "<目標路徑>" -Recurse -Force -Directory -ErrorAction SilentlyContinue |
     Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint } |
     ForEach-Object { Write-Output "$($_.FullName) -> $((Get-Item $_.FullName).Target)" }
   ```
   查到有東西 → 代表已經搬過，不用重搬，回報教練即可。查到空的才繼續下面步驟。
3. **標準七步驟**（跟 LINE/Perplexity 同一套）：關閉程式 → robocopy 第一次複製 → robocopy /MIR 鏡射 → 比對來源/目的地檔案數與大小 → 完全一致才繼續 → 原始資料夾改名成 `.bak.YYYYMMDD-HHmmss`（保留 7 天）→ 建立 Junction

---

## 一、Discord（低風險，建議優先做）

**關鍵事實**（已查證 Discord 官方資料夾慣例）：Discord 的使用者資料（登入 token、快取、Local Storage）**只放在 `%APPDATA%\discord`（Roaming）**，跟程式執行檔完全分開放在 `%LOCALAPPDATA%\Discord`（Local）。這個分離是 Windows 系統本身的慣例，不用像瀏覽器那樣擔心兩者混在一起。

Discord 沒有「書籤/瀏覽紀錄」這類本地端唯一資料——所有訊息都在 Discord 伺服器端，本機只有登入 token 和顯示快取，**風險是三項裡最低的，就算搬壞了，最多重新登入一次**。

```powershell
$src = "$env:APPDATA\discord"
$dst = "E:\Claude-Data\AppData\Discord"   # 依佩佩電腦實際外接碟代號調整路徑

# 先查巢狀 Junction（若已搬過會查到，查到就跳過不用重做）
Get-ChildItem $src -Recurse -Force -Directory -ErrorAction SilentlyContinue |
  Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }

Stop-Process -Name "Discord" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

robocopy $src $dst /E /COPY:DAT /R:1 /W:1 /NFL /NDL /NJH | Out-Null
robocopy $src $dst /MIR /COPY:DAT /R:1 /W:1 /NFL /NDL /NJH | Out-Null

$srcCount = (Get-ChildItem $src -Recurse -Force -File -ErrorAction SilentlyContinue).Count
$dstCount = (Get-ChildItem $dst -Recurse -Force -File -ErrorAction SilentlyContinue).Count
$srcSize  = (Get-ChildItem $src -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
$dstSize  = (Get-ChildItem $dst -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
Write-Output "來源: $srcCount 檔案 $([math]::Round($srcSize/1MB,1))MB | 目的地: $dstCount 檔案 $([math]::Round($dstSize/1MB,1))MB"

if ($srcCount -eq $dstCount -and $srcSize -eq $dstSize) {
    $ts = Get-Date -Format "yyyyMMdd-HHmmss"
    Rename-Item -LiteralPath $src -NewName "discord.bak.$ts"
    New-Item -ItemType Junction -Path $src -Target $dst | Out-Null
    Write-Output "完成，原始資料留底 discord.bak.$ts（保留7天）"
} else {
    Write-Output "數量或大小不一致，先不要搬家，回報教練"
}
```

---

## 二、GanJing 乾淨世界瀏覽器（已有現成驗證過的做法，直接套用）

**這套做法已經在聯想機驗證過，是穩定的**（commit `737bd140`）：只 junction `User Data`，**程式本體在 `AppData\Roaming\Gan Jing Browser`，完全不要動**。

```powershell
$src = "$env:LOCALAPPDATA\GanJing\User Data"
$dst = "E:\Claude-Data\AppData\GanJing-User-Data"   # 依佩佩電腦實際外接碟代號調整

# 先查巢狀 Junction
Get-ChildItem $src -Recurse -Force -Directory -ErrorAction SilentlyContinue |
  Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }

Stop-Process -Name "Gan Jing Browser" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

robocopy $src $dst /E /COPY:DAT /R:1 /W:1 /NFL /NDL /NJH | Out-Null
robocopy $src $dst /MIR /COPY:DAT /R:1 /W:1 /NFL /NDL /NJH | Out-Null

$srcCount = (Get-ChildItem $src -Recurse -Force -File -ErrorAction SilentlyContinue).Count
$dstCount = (Get-ChildItem $dst -Recurse -Force -File -ErrorAction SilentlyContinue).Count
$srcSize  = (Get-ChildItem $src -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
$dstSize  = (Get-ChildItem $dst -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
Write-Output "來源: $srcCount 檔案 $([math]::Round($srcSize/1MB,1))MB | 目的地: $dstCount 檔案 $([math]::Round($dstSize/1MB,1))MB"

if ($srcCount -eq $dstCount -and $srcSize -eq $dstSize) {
    $ts = Get-Date -Format "yyyyMMdd-HHmmss"
    Rename-Item -LiteralPath $src -NewName "User Data.bak.$ts"
    New-Item -ItemType Junction -Path $src -Target $dst | Out-Null
    Write-Output "完成，原始資料留底 User Data.bak.$ts（保留7天）"
} else {
    Write-Output "數量或大小不一致，先不要搬家，回報教練"
}
```

---

## 三、Microsoft 資料夾（🔴 不要直接搬家，先查清楚再說）

**這一項跟前兩項性質完全不同，不能套同一個做法。**

`AppData\Local\Microsoft` **不是單一 App 的資料夾**，是 Windows 系統本身跟多個 Microsoft 元件共用的位置（可能同時裝著 Edge 殘留、Windows 搜尋索引、WebView2、認證快取、Windows Copilot 等等）。聯想機軍師今天自己做 C 槽檢查時，也查到同名資料夾（3.24GB），**當時的判斷是「系統/Store 相依，不建議動」**——這不是隨便講的，是實測過的保守結論。

你判斷「Edge 已移除，可能是殘骸」的方向是對的，但**在確認之前，不要對整個 `Microsoft` 資料夾做 Junction 搬家**。正確做法：

```powershell
# 第一步：列出裡面的子資料夾跟大小，找出真正佔空間的是誰
Get-ChildItem "$env:LOCALAPPDATA\Microsoft" -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
  $s = (Get-ChildItem $_.FullName -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
  [PSCustomObject]@{Name=$_.Name; SizeMB=[math]::Round($s/1MB,1)}
} | Sort-Object SizeMB -Descending
```

找出最大的那幾個子資料夾名稱後，**個別判斷**：
- 如果名稱明確是 `Edge`、`EdgeCore`、`EdgeUpdate` 這類，且教練確認 Edge 真的不用了 → 可以考慮**直接刪除**（不是搬家，因為用不到的瀏覽器資料沒有保留價值）
- 如果是 `WebView2`、`WindowsApps`、`CLR_v4.0_32`、`Windows`、`CryptnetUrlCache` 這類系統元件相關 → **不要動**，這些通常是其他程式依賴的共用元件
- 拿不準的子資料夾，回報教練列出名單，不要自己猜測後就刪或搬

**這一項先做完「列清單」這一步，回報教練看過名單再決定，不要直接執行搬家或刪除。**

---

## 執行順序

1. Discord（風險最低，先做）
2. GanJing（現成驗證過的做法，直接套用）
3. Microsoft（先列清單回報，等教練看過名單再決定，不要自己搬或刪）

每做完一項都跟教練回報一次，不要三項都做完才一次回報。
