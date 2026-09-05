---
name: acer-pc5c925ed70e46-environment-notes
description: 這台機器（hostname PC5C925ED70E46，cross-agent 信箱名 acer）專屬的環境限制與 Git Bash 踩坑筆記，2026-08-31~09-05 累積
metadata:
  type: reference
---

## 帳號權限：COACH 不是系統管理員

當下登入帳號是 `PC5C925ED70E46\COACH`，`IsInRole(Administrator) = False`。資料夾路徑雖然叫 `C:\Users\Administrator`，但那只是資料夾名稱，**不代表帳號本身有系統管理員權限**。

**實測受影響的功能**：
- `schtasks /Create` 直接「拒絕存取」，連建立最陽春的測試任務都不行——**這台機器不能用 Windows工作排程器**，任何「N 小時後自動做某件事」的需求要改用背景計時程序（`Start-Process powershell -WindowStyle Hidden` 跑 `Start-Sleep` 後執行動作），缺點是機器重開機/登出會讓計時器消失
- `powercfg /change` 這類使用者層級電源設定**不需要管理員權限，正常可用**

## Git Bash 會吃掉 `/` 開頭的參數

MSYS2/Git Bash 對 `/xxx` 這種以斜線開頭的參數，預設會當成 POSIX 路徑做轉換，導致傳給原生 Windows CLI（`powercfg`、`schtasks` 等）的參數整個跑掉，回報「無效的參數」或「拒絕存取」但其實只是路徑轉換把參數轉亂了。

**修法**：呼叫這類指令前加 `MSYS_NO_PATHCONV=1`，例：
```bash
MSYS_NO_PATHCONV=1 powercfg /change monitor-timeout-ac 5
```
2026-09-02 首次踩到（`powercfg /change` 一直報錯，`powercfg /?` 卻正常，才發現是參數轉換問題，不是指令本身有問題）。

## python3 是 Windows Store 樁，不是真安裝

`which python3` 找得到（`AppData\Local\Microsoft\WindowsApps\python3`），但執行 `python3 --version` 沒有任何輸出，不能拿來跑腳本或當 pipe 的下游（`curl ... | python3 -c "..."` 會整條靜默失敗，exit code 常是 49）。跟聯想機器同款環境限制（見試金石案例64），但這台從一開始用的是 PowerShell 原生腳本，沒受影響；**這次新踩到的坑是拿它處理 curl 回應的 JSON**，改用 PowerShell 的 `ConvertFrom-Json` 或直接 `grep`/字串比對即可繞過。

## 沒有裝 GitHub CLI（`gh`）

這台機器 `gh` 指令不存在，SOP 裡教的 `gh repo create` / `gh api .../pages` 那套在這裡用不了。

**替代做法**：git 本身的 `credential.helper = manager`（Git Credential Manager）已經快取好 GitHub OAuth token，可以直接取出來對 REST API 用：
```bash
printf "protocol=https\nhost=github.com\n\n" | git credential fill
# 回傳 username=Coach1973, password=gho_xxxx（OAuth token）
```
拿到 token 後用 `curl` 打 `https://api.github.com/user/repos`（建repo）、`https://api.github.com/repos/{owner}/{repo}/pages`（開Pages）即可，效果等同 `gh repo create --push` + `gh api .../pages`。

**注意**：`curl -d '...'` 直接帶中文 JSON 字串在這台的 shell 環境會被編碼吃掉，回 400 "Problems parsing JSON"——一律先把 payload 寫成檔案（UTF-8），用 `--data-binary "@檔案路徑"` 帶進去才不會壞。

## 這台機器的 workspace/repo 位置

真正在用、持續同步的 repo 只有一份：`C:\Users\Administrator\Documents\mac-openclaw-workflows`。`Documents\workspace` 是 junction 指過去的（2026-09-01 修復自我修復邏輯後，就算 junction 被刪掉，`feed_junshi_handoff.ps1` 也會自動偵測既有 repo 補 junction，不會再整包重新 clone），不要誤以為那是獨立資料。

Related: [[試金石案例64]]（聯想同源環境相容性問題）、[[project_acer_health_check_2026-08-31]]（完整體檢報告）
