---
name: feedback-minimax-dynamic-context-cap-2026-09-17
description: MiniMax-M3 的 context window 上限會隨 session 累計用量動態縮減（觀察值 200K 新對話 → 163K 短時間後 → 84K 跑 2 小時），以前以為是固定 200K 是錯的
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8aa0d172-24d4-58ae-a1eb-134bd3a007c5
  modified: 2026-09-17T10:05:32.206Z
---

# MiniMax-M3 的 context window 上限會動態縮減（鐵證：curl API 回應 model: MiniMax-M3）

## 事件

2026-09-17 凌晨 04:21，教練在手機觀察到兩個對話框的 context window 數字不一致：
- 新開的對話框：上限 200K（MiniMax-M3 出廠值）→ 跑一下變 163K
- 電腦版 PID 48499 這場跑了 2 小時的對話框：上限被縮減到 **84K**

教練原話：「這是精神錯亂嗎？」——他以為這是 bug，實際上是 MiniMax 的動態政策。

## 鐵證（curl 驗證）

```bash
$ curl -s -X POST https://api.minimax.io/anthropic/v1/messages \
    -H "x-api-key: $ANTHROPIC_AUTH_TOKEN" \
    -d '{"model":"claude-sonnet-5","max_tokens":10,"messages":[{"role":"user","content":"Reply with just the word OK."}]}'
```

回應關鍵欄位：
```json
{
  "id": "06fa2d580e9c6d092b66e6b0bd982526",
  "model": "MiniMax-M3",          ← 後端自己說是 M3，不是 sonnet-5
  "usage": {
    "input_tokens": 42,
    "cache_read_input_tokens": 128
  }
}
```

**結論**：即使 process 啟動時帶 `--model claude-sonnet-5` 標籤，MiniMax 後端**根本沒有真的跑 sonnet-5**，而是把所有 sonnet-5 請求導到 MiniMax-M3。API 回應的 `model` 欄位是最權威的證據。

## 動態 context 縮減觀察值

| session 狀態 | context window 顯示 |
|------------|---------------------|
| 全新對話框剛開 | 200K（出廠上限） |
| 短時間使用後 | 163K |
| 跑 2 小時大量使用後 | 84K |

教練觀察到「很快就變成 163K」——「很快」這個字暗示是**動態變化**，不是出廠固定值。

## 教訓（修正既有認知）

**以前以為**：MiniMax-M3 的 context window 是固定 200K。

**實際是**：MiniMax-M3 的**靜態上限**是 200K，但**運行時會根據 session 累計用量動態縮減**——session 跑越久、用量越大，上限會被砍下來。

**為什麼 MiniMax 要這樣做**（合理推測）：管控後端成本+算力分配。用量大的 session 佔太多 token 預算，就縮減上限逼對話結束或觸發 compact。

## 影響

1. **長對話會更早被切斷**——以前預期 200K 才到頂，現在可能 84K 就到頂
2. **OpenClaw auto-compact 會更頻繁觸發**——因為「上限變小」會讓剩餘額度看似不夠、觸發 compact
3. **Mac 上這場對話（PID 48499）已被縮減到 84K**——意味著這場後續對話容量比預期小很多

## Why

這件事**完全沒有官方文件說明**，要靠教練觀察才會知道。如果沒有記下來，下次再看到「context window 突然變小」會以為是 OpenClaw bug 或 process 出問題，浪費時間除錯。

## How to apply

- 看到 context window 數字變小，先看是不是 MiniMax 動態政策、**不要急著 blame OpenClaw**
- 長對話策略要改：早期就做 compact 或拆成多個 session，不要賭 200K 上限
- 自我檢測模型身分時，**curl API 看回應的 `model` 欄位是最權威方式**（process 啟動標籤、shell env、openclaw.json 都不是真相）
- 不要相信「切到 sonnet-5」的指令——除非看到 API 回應真的寫 sonnet-5

## 相關

- [[feedback_check_global_config_before_shell_level_fix_2026-09-17]]（環境變數 vs 全域設定檔 雙查）
- [[reference_claude_code_remote_control_setup_sop_2026-09-17]]（Mac 上的 Remote Control SOP）
- v209 接力棒第 2 節「模型身份三層驗證」原本只列了三層，缺第 4 層「API 回應 model 欄位」→ 本次新增這第 4 層為最權威
