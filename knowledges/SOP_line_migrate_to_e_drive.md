# LINE Windows 桌面版對話紀錄搬到 E 槽 SOP

> 教練親口（2026-06-18 凌晨 5:16）：
> 「LINE 的對話一直是我的痛點，每次一鍵還原，對話記錄都會不見」
>
> Mac 軍師親寫（凌晨 5:18），交給 Windows 軍師明天執行。
> 教練暗號：「請執行 LINE 搬家研究」

---

## ⚠️ 首要警告（不可跳）

LINE 桌面版不是「文字檔」這麼單純——它有：
1. **對話資料庫**（SQLite 加密）
2. **媒體快取**（照片、語音、影片）
3. **登入 token / 加密金鑰**（搬錯位置可能整個帳號被登出）
4. **設定檔**（聊天室順序、訊息已讀狀態）

**動錯一個，全部對話可能不見、帳號可能要重新登入掃描手機 QR code**。
所以本 SOP **強制三階段**，每階段教練親口確認才能下一步。

---

## 🎯 三階段執行（不可跳）

### 階段 1：發現 LINE 真實位置（不動任何檔）

Windows 軍師跑這個診斷：

```powershell
# 找 LINE 在 AppData 的所有相關目錄
$paths = @(
    "$env:APPDATA\LINE",
    "$env:LOCALAPPDATA\LINE",
    "$env:APPDATA\line.bnr.NEW_LINE_DESKTOP_NATIVE",
    "$env:LOCALAPPDATA\LINE Corporation"
)
foreach ($p in $paths) {
    if (Test-Path $p) {
        $size = (Get-ChildItem $p -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
        Write-Host "✅ $p"
        Write-Host "   大小：$([math]::Round($size,1)) MB"
        Get-ChildItem $p | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
    }
}
# 額外掃 LINE 進程，看它真的在用哪個目錄
Get-Process | Where-Object { $_.ProcessName -like "*line*" } | Select-Object ProcessName, Id, Path
```

**回報給教練**：
- LINE 對話檔在哪個位置
- 大小多少（GB？這影響搬移時間）
- LINE 目前在運作嗎

教練看完，**親口說「下一步」**才進階段 2。

---

### 階段 2：Dry-Run 備份測試（複製不刪）

**前提：LINE 完全關閉**（連系統匣 LINE 圖示都右鍵退出）

```powershell
# 1. 確認 LINE 已關閉
Get-Process | Where-Object { $_.ProcessName -like "*line*" }
# 應該沒輸出。有就先教練手動關掉。

# 2. 完整複製到 E 槽（不刪原本）
$src = "C:\Users\$env:USERNAME\AppData\Local\LINE"  # 階段 1 確認過真實位置才用這個
$dst = "E:\Claude-Data\LINE-AppData-Local"
robocopy "$src" "$dst" /E /R:3 /W:5 /COPY:DAT /DCOPY:T /XJ /LOG:"E:\Claude-Data\line-migrate-log.txt"

# 3. 驗證：原檔與複製檔大小一致
$srcSize = (Get-ChildItem $src -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$dstSize = (Get-ChildItem $dst -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
Write-Host "原檔大小: $([math]::Round($srcSize/1MB,1)) MB"
Write-Host "複製檔大小: $([math]::Round($dstSize/1MB,1)) MB"
Write-Host "差異: $([math]::Round(($srcSize-$dstSize)/1MB,1)) MB"
```

**規則**：
- 用 `robocopy /XJ` 避開 junction loops
- `/COPY:DAT /DCOPY:T` 保留檔案時間、屬性（LINE 可能用 timestamp 判斷快取有效性）
- 大小差距 > 10 MB → 停下查 log，不進階段 3

**回報給教練**：
- 複製成功 / 失敗
- 大小差距

教練看完，**親口說「進階段 3」**才動原檔。

---

### 階段 3：建 Junction（這步動真檔）

**前提**：
- 階段 2 大小驗證通過
- LINE 仍然關閉
- 教練親口確認

```powershell
# 1. 重命名原 C 槽 LINE 為 .bak（不是刪，可逆）
$src = "C:\Users\$env:USERNAME\AppData\Local\LINE"
$bak = "$src.bak.beforejunction.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Rename-Item -Path $src -NewName ([System.IO.Path]::GetFileName($bak))
Write-Host "✅ 原檔已 rename 為 $bak（保留 7 天再刪）"

# 2. 建 junction：原位置 → 指向 E 槽複製檔
cmd /c mklink /J "$src" "E:\Claude-Data\LINE-AppData-Local"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Junction 建失敗，rename 回來復原"
    Rename-Item -Path $bak -NewName "LINE"
    exit 1
}

# 3. 驗證 junction
Get-Item $src -Force | Format-List Name, Target, Attributes

# 4. 寫還原便條
$noteContent = @"
LINE 對話檔位置：E:\Claude-Data\LINE-AppData-Local
C 槽 junction：$src
建立時間：$(Get-Date -Format 'yyyy-MM-dd HH:mm')

【一鍵還原後修復步驟】
1. 確認 LINE 是關閉狀態
2. 跑：cmd /c mklink /J "$src" "E:\Claude-Data\LINE-AppData-Local"
3. 開 LINE，對話檔應該完整還在

【7 天觀察期內若 LINE 出問題】
1. 完全關閉 LINE
2. 刪掉 junction：Remove-Item $src -Force
3. rename 回來：Rename-Item $bak LINE
4. 開 LINE 確認復原
"@
Set-Content -Path "E:\Claude-Data\LINE-junction-紀錄.txt" -Value $noteContent -Encoding UTF8
```

**測試**：開 LINE，看：
- ✅ 是否要重新登入？（應該不用）
- ✅ 對話列表完整？
- ✅ 點開任一聊天室，歷史訊息在？
- ✅ 照片 / 媒體預覽正常？
- ✅ 傳一個新訊息出去能收到嗎？

**全部 OK → 教練確認後**，**7 天後再刪 .bak**（給觀察期）。
**任一不 OK** → 立刻復原（關 LINE → 刪 junction → rename .bak 回來）。

---

## 🚫 絕對不做的事

1. 不用 `Remove-Item -Recurse -Force` 刪 C 槽 LINE 目錄（用 Rename 才可逆）
2. 不在 LINE 運作中動目錄（資料庫鎖住會壞檔）
3. 不在階段 2 大小驗證沒過就跳階段 3
4. 不未經教練親口確認跳階段

## ❓ 如果 junction 不被 LINE 接受怎麼辦

LINE 桌面版有可能（雖然少見）拒絕從 junction 路徑讀取。
若階段 3 測試失敗：

**Plan B：用 LINE Keep 雲端備份**（LINE 內建功能）：
- LINE 設定 → 聊天記錄 → 備份到 LINE Keep（每個聊天室分別備份）
- 一鍵還原後重新登入 → 從 LINE Keep 還原

**Plan C：定期 robocopy 同步**（折衷方案）：
- 不動 C 槽 LINE 原始位置
- 寫 Windows 排程：每天凌晨 3 點 robocopy C 槽 LINE → E 槽備份
- 一鍵還原後從 E 槽備份覆蓋回 C 槽
- 缺點：恢復時聊天室順序、登入狀態可能要重設

---

## 給 Windows 軍師的硬性提醒

- **本 SOP 強制三階段，不可合併**
- 階段間必須回報教練 + 等親口指示
- 階段 3 如果有任何不確定 → **不要動**，跟教練說「Plan B/C 怎麼選」
- 一切以「**對話不丟、帳號不掉**」為最高優先

教練親口最痛點：「LINE 對話是我的痛點」——這份檔案不能在凌晨瞎搞，要白天精神好 + Windows 軍師清醒時做。

---

> Mac 軍師 Opus 4.7 親寫於 2026-06-18 凌晨 5:18 台灣時間。
> 寫完去睡。
