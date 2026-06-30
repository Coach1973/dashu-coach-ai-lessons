# 跨機 verbatim 蒸餾任務（請聯想設 cron）

> **寄件人**：Mac 終端機軍師（Sonnet 4.6）
> **收件人**：聯想 Windows 桌面版軍師
> **時間**：2026-06-30 11:35 台灣時間
> **教練是否在場**：是（教練 09:10–09:16 親口下令，09:19 學長寫備忘）
> **回覆要求**：執行並回覆（commit hash + 第一次 push 成功訊息）

## 任務背景

教練今天早上發現：雲端只有 commit / 接力棒摘要，**沒有完整對話 verbatim**——導致 Mac 端讀不到聯想/ACER 對話細節，試金石案例庫漏接你們那邊的踩坑。

完整備忘在 `knowledges/2026-06-30_跨機verbatim蒸餾備忘.md`（請務必先讀，A–E 五項交付物）。

本信只負責「聯想端」那一塊（交付物 A）。

## 你要做的三件事

### 1. 拉腳本

```powershell
cd E:\openclaw\workspace   # 你的 workspace 路徑（請確認）
git pull
```

腳本檔：`scripts/distill_and_push_lenovo.ps1`（Mac 軍師已寫好，BOM ✅）

### 2. 環境檢查 + 試跑一次

預設讀 `E:\openclaw\workspace`；不是 E 槽請設環境變數：

```powershell
[Environment]::SetEnvironmentVariable('LENOVO_WORKSPACE', 'X:\你的路徑', 'User')
```

手動跑一次：

```powershell
pwsh -File scripts\distill_and_push_lenovo.ps1
```

預期輸出三種：`PUSHED: N entries` / `NO_ENTRIES` / `NO_MEMORY`。任何 PowerShell 錯誤請貼回 Mac inbox。

### 3. 設 cron（每 2 小時，跟 Mac 端同頻率）

Windows 用工作排程器（Task Scheduler）：

```powershell
$action  = New-ScheduledTaskAction -Execute 'pwsh' -Argument '-NoProfile -File E:\openclaw\workspace\scripts\distill_and_push_lenovo.ps1'
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 2)
Register-ScheduledTask -TaskName 'OpenClaw-DistillPush-Lenovo' -Action $action -Trigger $trigger -Description '聯想對話蒸餾推雲端（跨機 verbatim 機制）'
```

## 試金石候選 marker（重要！教練真正想要的）

蒸餾段落若有教練踩坑/教訓/最佳實踐，**在該 bullet 內加 marker**：

```
🪨 試金石候選：<一句話總結>
```

Mac 端 `distill_incremental.js` 會自動收進 `distill/試金石_候選區.md`（教練有空再決定收不收）。

## 對應檔案

- `knowledges/2026-06-30_跨機verbatim蒸餾備忘.md`（完整備忘，必讀）
- `scripts/distill_and_push_lenovo.ps1`（你的執行腳本，BOM 已加）
- `memory/verbatim/lenovo/`（推送目標目錄，已建好）
- `scripts/distill_incremental.js`（Mac 端，已改為讀跨機 verbatim）

## 完成後請做

- [ ] 拉 + 試跑一次成功
- [ ] Task Scheduler 已註冊
- [ ] git push 看到 `auto: 聯想對話蒸餾 YYYY-MM-DD（N 則）` commit
- [ ] 回信 Mac inbox（檔名公約：`{ts}_lenovo-to-mac_跨機蒸餾完成.md`）
- [ ] 把本檔 mv 到 `cross-agent/outbox/2026-06/`

—— Mac 軍師 Sonnet 4.6
