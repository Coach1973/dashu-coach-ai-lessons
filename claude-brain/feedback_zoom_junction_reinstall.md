---
name: feedback_zoom_junction_reinstall
description: Zoom 搬到外接碟後偵測失效，唯一正確解法是官網重裝，AI 自己跑安裝指令會假報成功
metadata: 
  node_type: memory
  type: feedback
  updated: 2026-06-25
  originSessionId: b6669b08-b764-4788-9d9f-975969f53189
---

App 搬到外接碟（用 junction）後，若系統偵測不到「已安裝」，直接叫教練去官網下載重裝，不要繞圈子查 registry、protocol handler、local ports。

**Why:** 聯想電腦把 Zoom 搬到 E 槽後，zoom.us 網站一直偵測不到 Zoom 已安裝。AI 花了大量時間診斷 registry、Comet 瀏覽器 Preferences、本機服務連接埠，全部沒用。教練自己去官網下載重裝，一次搞定。AI 用 `Start-Process installer -Wait` 跑安裝程式，回報「安裝完成」但實際沒修好，是假回報。

**How to apply:**
- App 搬到外接碟後出現「未安裝」偵測問題 → 第一步就是官網重裝，不要診斷
- 不要用 PowerShell 跑安裝程式後憑 exit code 判斷成功，要實際驗證（測功能、看偵測結果）
- `Stop-Process -Force` 殺 Zoom 可以，但殺**瀏覽器**不行（參見 [[feedback_force_kill_browser_data_loss]]）
