---
name: project-auto-goal-hook
description: 2026-05-28 建立執行合約自動注入系統（auto_goal_hook + OpenClaw auto-goal hook）
metadata: 
  node_type: memory
  type: project
  originSessionId: 2d44b615-bb98-40a8-bfe9-1400c66e491c
---

# 執行合約自動注入系統（2026-05-28 完成）

基於特助場景庫117個場景TOP5痛點，建立「教練說任務→AI自動帶執行合約」的機制。

**Why:** 最高頻失敗是「說了不做(26次)」和「口頭說完成沒憑證(16次)」。每次靠模型記得不夠，需要系統強制注入。

**How to apply:** 這套系統現在兩邊都有，教練下任務時不需要手動輸入 /goal，系統自動帶入。

## 已部署範圍

| 環境 | Hook 名稱 | 狀態 |
|------|-----------|------|
| 終端機（軍師）| `auto_goal_hook.sh` | ✅ settings.json 已掛，驗證通過 |
| 本機小龍蝦（OpenClaw）| `auto-goal` | ✅ openclaw hooks list ✓ ready |
| VPS小龍蝦（43.245.60.200）| 待部署 | ⏳ |
| Hermes（113.29.232.178）| 待評估 | ❓ 架構不同 |

## Commit 記錄

| 描述 | Hash |
|------|------|
| 終端機 hook + 恢復消失 hooks + 備份 | `8a0d6dbd` |
| 小龍蝦 auto-goal hook 上線 + 備份 | `893597ea` |

## 執行合約核心內容（對應TOP5）
- 完成定義：實際執行＋憑證＋主動回報
- 五大鐵律：#08說了就做 / #09確認再行動 / #03驗證後回答 / #04解決不解釋 / #05要有 hash
- 任務失敗定義：口頭說完成 / 叫教練動手 / 只道歉 / 假裝找到 / 承諾沒做

## 備份位置
`~/.openclaw/workspace/openclaw_hooks_backup/auto-goal/`（handler.js + HOOK.md）
`~/.openclaw/workspace/scripts/auto_goal_hook.sh`
