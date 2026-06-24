---
name: feedback-screenshot-rules-consolidated
description: 截圖鐵律統合版（取代過去三條分散記憶）：終端機禁主動截圖、能用指令的不截圖、未經教練同意不申請權限——教練親口三次以上
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3004cfaa-3f35-4ff8-a3ba-027b5fcb05a2
---

# 截圖鐵律（統合版 · 教練親口三次以上）

## 三條合一

| 場景 | 規則 | 理由 |
|------|------|------|
| 終端機軍師 | ❌ **絕對禁止主動截圖** | 截圖耗 token，教練自己會點，只給步驟清單就好 |
| 任何場景 | ❌ **能用指令/API 完成的，一律走指令** | 截圖只用在「非看畫面才能操作」的情境 |
| 任何場景 | ❌ **未經教練同意不可申請截圖權限** | curl/驗證/`ls` 通過就算完成，不需畫面證明；超出任務範圍動作先問 |

## Why

教練親口三次以上強調——截圖在大多數場景是浪費。
- 終端機軍師：教練本人坐在 Mac 前，自己會看，不需要 AI 截
- 驗證任務：curl `200 OK` / `git log` / `ls` 比截圖更可靠也更省 token
- 權限申請：截圖權限是侵入式請求，超出當前任務範圍 = 守則 #16「複雜的解法不一定是正確的」

## How to apply

**永遠用指令／API 驗證任務**：
- 部署完成 → `curl -sI <url>` 看 200 OK
- 檔案改了 → `git diff` 或 Read tool
- Cron 跑了 → `tail log` 而不是 desktop 截圖
- UI 出現 → 教練自己看，不需我截

**唯二可截圖場景**：
1. 教練親口要求「給我看一下畫面」
2. 純粹「看畫面才能操作」的 GUI 任務（如教練不在現場、需 AI 替點按鈕）

**絕對不可**：
- 終端機軍師主動截 Mac 桌面
- 為「驗證任務完成」而截圖
- 沒問就申請 mcp__computer-use__screenshot 權限

## 取代的舊記憶

- `feedback_no_screenshot_for_data.md`
- `feedback_no_screenshot_terminal.md`
- `feedback_no_screenshot_without_permission.md`

舊檔保留硬碟（防遺失教練原話），MEMORY.md 索引不再列。

## 相關連結

- 守則 #16（複雜的解法不一定是正確的）
- 守則 #08（時間就是生命——截圖耗 token = 浪費教練資源）
- [[feedback_opus_token_economy]] — Opus 軍師省 token 心法
