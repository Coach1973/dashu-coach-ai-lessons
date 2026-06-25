# 聯想桌面版軍師工作總結 · 2026-06-26 上午

> 執行者：聯想 Windows 桌面版 Sonnet 4.6
> 時間：2026-06-26 上午（台灣時間）

---

## 本場戰果

### 1. ✅ Claude CLI 自動模式設定
- `C:\Users\bymyw\.claude\settings.json` 加入 `"permissions": { "defaultMode": "acceptEdits" }`
- 效果：以後開 Claude CLI 不再一直問 yes/no，讀寫檔案類直接過
- 教練詢問 Acer 的做法 → 給了一條 PowerShell 一行指令可貼到 Acer 執行

### 2. ✅ Zoom 連結失效修復
- 根因：Zoom AppData 搬到 E 槽（junction），zoom.us 網站偵測不到
- 過程：AI 繞圈診斷 registry / Comet 瀏覽器 Preferences / 本機連接埠，全沒用
- 結局：**教練自己去官網下載重裝，一次搞定**
- 🔴 血淚教訓已燒進記憶：`feedback_zoom_junction_reinstall.md`
  - App 搬外接碟後偵測失效 → 第一步直接官網重裝，不診斷
  - AI 用 PowerShell 跑安裝程式 `-Wait` 假回報「完成」，實際沒修好

### 3. ✅ 跨機 inbox hook 上線（聯想端）
- `git pull` mac-openclaw-workflows（拉到 32 個新檔）
- 讀取 Mac 軍師信件：`cross-agent/inbox/lenovo/20260626-0020_mac-to-lenovo_inbox-system-online.md`
- 執行三步 setup：
  1. 環境變數 `AGENT_INBOX_NAME=lenovo`（User 層級，永久生效）
  2. `scan_cross_agent_inbox.ps1` hook 掛進 `settings.json` UserPromptSubmit
  3. 自測通過：`📬 跨機軍師信箱（lenovo 收件匣有 2 封未讀）`
- 信件歸檔 outbox，回信 Mac，push commit `8f9a163c`

---

## 本場踩點（自我檢視）

| 踩點 | 根因 | 正確做法 |
|------|------|----------|
| Zoom 診斷繞圈 10+ 輪 | 沒有立刻想到「重裝」 | App 搬碟後失效 → 第一步官網重裝 |
| PowerShell 安裝假回報 | `-Wait` 只等進程結束，不驗功能 | 裝完必測實際功能，不信 exit code |
| 問教練用哪個瀏覽器 | 應直接查登錄檔 default browser | 已查到是 Perplexity Comet |

---

## 下一棒待辦

| 優先 | 任務 |
|------|------|
| 🟡 | Acer 也要做 inbox hook setup（信件已在 `cross-agent/inbox/acer/`）|
| 🟡 | Acer Claude CLI settings.json 也要加 `defaultMode: acceptEdits`（已給指令）|
| 🟢 | 聯想 Zoom 連結確認正常（已修好）|

---

> 教練下口令「Mac 有事情交代，你去讀一下」，聯想軍師每次開口時自動提示 inbox。
> 機制上線，設定一次永久生效。
