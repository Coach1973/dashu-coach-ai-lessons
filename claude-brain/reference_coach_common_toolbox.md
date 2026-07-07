---
name: reference-coach-common-toolbox
description: 教練常用工具箱——反覆被要求的設定/指令/流程集中索引，新機器或忘記時直接來這裡查
metadata:
  type: reference
  originSessionId: a8416d87-73e6-474e-98f8-1a099e9b1ad3
  updated: 2026-07-08
---

# 教練常用工具箱

> 這份清單收錄「教練反覆提過好幾次、每次都要重新想一遍」的設定/指令，目的是不用每次都重新查證或問教練，直接來這裡複製貼上。

## 1. Claude Code 不要一直問 yes/no

**背景**：教練至少提過 3 次以上（更早一次的程式後來因為系統還原被洗掉、2026-06-25 ACER、2026-06-26 聯想機），根因是這個設定存在 `~/.claude/settings.json`（純本機 C 槽檔案），不在 E 槽工具箱的「免疫一鍵還原」保護範圍內，每次系統還原就會消失，必須重新設定。詳細查證過程見試金石案例 42（禁止問教練記不記得，一律查記錄）。

**安全版（官方建議，只自動通過檔案編輯，終端機指令仍會確認一次）：**

Windows PowerShell：
```powershell
$settingsPath = "$env:USERPROFILE\.claude\settings.json"
New-Item -ItemType Directory -Path (Split-Path $settingsPath) -Force -ErrorAction SilentlyContinue | Out-Null
if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
} else {
    $settings = [PSCustomObject]@{}
}
if (-not $settings.PSObject.Properties['permissions']) {
    $settings | Add-Member -NotePropertyName permissions -NotePropertyValue ([PSCustomObject]@{})
}
if (-not $settings.permissions.PSObject.Properties['defaultMode']) {
    $settings.permissions | Add-Member -NotePropertyName defaultMode -NotePropertyValue "acceptEdits"
} else {
    $settings.permissions.defaultMode = "acceptEdits"
}
$json = $settings | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($settingsPath, $json, [System.Text.Encoding]::UTF8)
```

Mac / Linux：
```bash
mkdir -p ~/.claude
python3 -c "
import json, os
path = os.path.expanduser('~/.claude/settings.json')
data = json.load(open(path)) if os.path.exists(path) else {}
data.setdefault('permissions', {})['defaultMode'] = 'acceptEdits'
json.dump(data, open(path, 'w'), indent=2, ensure_ascii=False)
"
```

**完全版（連終端機指令都不問，官方警告只建議在隔離環境用，一般電腦要三思）**：把上面的 `acceptEdits` 換成 `bypassPermissions`。

跑完都要**重開 Claude Code 才生效**。

## 2. 部署詞彙字典（避免誤解要不要上線）

- 「自動站」＝部署到 bymyway（自動觸發）
- 「網頁推」＝git push GitHub（手動觸發部署）
- 「推」＝Netlify zip+API 直接上傳
三者不可混，詳見 `feedback_coach_deploy_vocabulary.md`。

## 3. 本機 HTML 預覽唯一指定 Chrome

禁止用 Safari／file://／預覽面板，格式固定：`open -a "Google Chrome" <path>`。詳見 `feedback_html_preview_chrome_only.md`。

## 4. 危險指令五道閘門（刪除/搬移大型資料前）

① 絕對路徑硬編碼 ② 目標 echo 給教練看 ③ 大小驗證 ④ 超過 100MB 必須通行證 ⑤ 超過 1GB 任何身份不得自主執行。Windows 用 `scripts/delete_guard.ps1` 的 `Safe-Remove`，禁止直接呼叫 `Remove-Item -Recurse -Force`。

## 5. 查證方向七層系統（禁止問教練記不記得）

git log --grep → 試金石案例庫 → memory 記憶檔 → HEARTBEAT/接力棒 → 每日蒸餾摘要 → 原始對話 jsonl → 即時系統現況。詳見試金石案例 42、`feedback_never_ask_coach_recall_self_verify.md`。

## 6. App 搬家到 E/D 槽的正確做法

只 junction 該 App 的「使用者資料/Profile」子資料夾，絕對不要整個 `AppData\Local\<App>` 資料夾搬（會混到程式本體，曾導致三個瀏覽器帳號全部遺失）。搬家前先檢查目標資料夾內部有沒有巢狀 Junction，避免重複處理。詳見試金石案例 W03、39、41，`feedback_browser_no_full_junction.md`。

## Why / How to apply

**Why:** 教練的工作習慣是「凡走過必留痕跡」，每件事都會走 git commit + GitHub，不想每次都要重新提醒或讓 AI 重新查一輪。這份工具箱把已經反覆驗證過的固定答案集中放一起，省下重複查證的時間。

**How to apply:** 教練提到「工具箱」「常用指令」「以前那個設定」時，先來這份清單找，找不到才啟動查證方向七層系統。這份清單也要持續更新——每次發現教練重複要求同一件事三次以上，就該把最終解法補進來。
