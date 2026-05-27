---
name: auto-goal
description: "偵測教練下任務的訊號，自動注入「執行合約」，讓 AI 每次接任務就知道什麼叫完成"
metadata: {"openclaw":{"emoji":"🎯","events":["message:preprocessed"]}}
---

# Auto-Goal Hook（執行合約自動注入）

軍師版（Claude Code）`auto_goal_hook.sh` 的 OpenClaw 對應版本。
教練每發一則帶有任務訊號的訊息，自動注入「執行合約」到 context。

## 觸發事件
`message:preprocessed` — 每次教練發言時觸發

## 觸發邏輯
偵測任務關鍵詞（幫我、請你、去做、去建、去修、做一個、更新、修改等），
命中才注入，閒聊靜默（不炸 token）。

## 注入內容
基於特助場景庫117個場景TOP5痛點的「執行合約」：
- 什麼叫「完成」（有憑證才算）
- 五大執行鐵律（對應最高頻失敗模式）
- 任務失敗定義
- Session 結束必做

## 設計原則
- 防禦性多路徑抽取訊息文字（與 rule-reminder 相同策略）
- 命中才注入，未命中靜默退出
- 與 rule-reminder 互補：rule-reminder 注入守則提醒，auto-goal 注入執行合約
