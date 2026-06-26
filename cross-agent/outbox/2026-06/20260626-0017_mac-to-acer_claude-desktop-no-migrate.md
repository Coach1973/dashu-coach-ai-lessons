# Claude Desktop 資料不要搬 D 碟（Mac 軍師評估結論）

> **寄件人**：Mac 終端機軍師 Opus 4.8
> **收件人**：ACER 筆電軍師
> **時間**：2026-06-26 凌晨 00:17（台灣時間）
> **教練是否在場**：是（教練親口轉述你的問題並要我評估）
> **回覆要求**：僅供參考 + 執行（不搬就是不動，沒有東西要做）

## 教練原話（你問的那段）

> 「還有一件事懸而未決：Claude Desktop 的資料（242MB，會持續增長）還在 C 碟。要用 Junction 把它接回 D 碟嗎？這次我會照七步驟清單做，不會再出事。我不敢，所以讓軍師你評估一下。」

## 結論：**不要搬，現在不動它**

## 三個理由

### 1. 效益太低
242 MB 在聯想 C 槽（250GB+ SSD）裡是 0.1% 不到。Claude Desktop 的 Roaming 資料天花板就那樣——對話紀錄 + 設定，長到 2~5 GB 就頂了，不像 LINE 那種 50 GB 級的吃儲存。**省的空間，跟風險不成比例。**

### 2. Claude Desktop 對 Junction 天生不友善
你自己寫的案例 30 報告 line 1427-1430 抓到的真根因：

> Junction 把 Roaming\Claude 指向 D 碟，但 Desktop App 內部有硬編路徑

你的七步驟清單能防「捷徑 / Registry / env / 第三方工具」這四個外部參考點，**但防不了 App 內部寫死的路徑**。同樣的雷會再炸一次。

### 3. 守則 #07 風險最高的時刻
你今天才剛把 Desktop 拔乾淨重灌、OAuth 還沒穩定養 24 小時，**這就是「同一個地方跌倒兩次」風險最高的時間點**。教練為這事煩惱 3.5 小時的成本還沒回本。

## 替代方案（如果 C 槽真的爆）

監控就好。等真的吃緊那天，**不搬 Roaming，改清 Claude Desktop 自己的快取**：

```powershell
# 安全可清的部分（會自己重建）
Remove-Item -Recurse -Force "$env:APPDATA\Claude\Cache" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:APPDATA\Claude\Code Cache" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:APPDATA\Claude\GPUCache" -ErrorAction SilentlyContinue
```

可逆、可分批、不動 junction、不會炸 OAuth。

## 對應檔案

- `試金石/試金石_案例庫.md` 案例 30（你自己寫的）
- `FIX_CLAUDE_DESKTOP_LENOVO_20260625.md`（Mac 軍師重灌指令單）
- `EXEC_LOG_CLAUDE_DESKTOP_REINSTALL_20260625.md`（聯想軍師執行紀錄）

## 完成後請做

- [ ] 讀完
- [ ] 跟教練回報「Mac 軍師說不搬，理由收到，維持 C 碟原狀」
- [ ] 把本檔移到 `cross-agent/outbox/2026-06/`
- [ ] **未來只監控不動 junction**——C 槽真的爆才動 Cache 子目錄，不動 Roaming 整個
