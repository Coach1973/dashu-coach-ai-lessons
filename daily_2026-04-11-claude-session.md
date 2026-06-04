# 2026-04-11 Claude 助教工作總結（完整版）

> 這份文件記錄 Claude Code 助教今日建立的所有機制與邏輯
> 小龍蝦助教請必讀，這是你的「進化日誌」
> 最後更新：2026-04-11 13:10

---

## 🏆 今日完成的重大進化

### 進化 1：五條備援模型線路（上午）

**問題**：主模型（Gemini）限流 → 小龍蝦完全癱瘓

**解決方案**：建立 5 層備援鏈
```
Primary:    google/gemini-3.1-pro-preview（繁體中文穩定，100萬 ctx）
Fallback 1: openrouter/nvidia/nemotron-3-super-120b-a12b:free
Fallback 2: openrouter/google/gemma-4-31b-it:free
Fallback 3: sambanova/Meta-Llama-3.3-70B-Instruct
Fallback 4: cerebras/qwen-3-235b-a22b-instruct-2507
Fallback 5: anthropic/claude-sonnet-4-6
```

**每個 Provider 的接入重點**：
- OpenRouter：endpoint `https://openrouter.ai/api/v1`，apiKey 存 models.json + auth-profiles 都要設
- SambaNova：endpoint `https://fast-api.snova.ai/v1`（注意！`api.sambanova.ai` DNS 不通）
- Cerebras：apiKey **必須直接寫進 models.json**，auth-profiles 方式無效

**永久結論**：Groq 不能當 Primary（57k token 系統提示 > 12k TPM 上限）

---

### 進化 2：Session Lock 自動修復

**問題**：Primary 失敗後，fallback 被拒絕接管（Session 啟動時鎖定了 Primary 到 JSONL）

**正確修復步驟**：
1. 刪掉鎖死的 JSONL 檔案（只清 sessions.json 不夠！gateway 會從 JSONL 恢復）
2. 清空 sessions.json 所有條目
3. 清空 auth-profiles.json 的 usageStats（cooldown）
4. `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`

**自動化**：`ai.openclaw.session-fix` LaunchAgent 每 2 分鐘執行一次

---

### 進化 3：記憶體系從零建立（今日最重要發現）

**問題**：`memory/` 目錄從未被建立 → 小龍蝦每次啟動都是完全失憶狀態

**AGENTS.md 要求**（第 3 步）：讀 `memory/YYYY-MM-DD.md`，但目錄不存在，所以它每次說「今日記憶不存在」是真的

**修復**：
```bash
mkdir -p /Users/bymyway/.openclaw/workspace/memory/
```

**現在建立的記憶文件**：
- `memory/2026-04-10.md` — 昨日歷史
- `memory/2026-04-11.md` — 今日完整日誌（含所有踩坑記錄）
- `memory/2026-04-11-morning.md` — 早上 session 的補充
- `memory/2026-04-11-claude-session.md` — 本文件

---

### 進化 4：Telegram 對話自動同步機制

**問題**：Claude 助教不知道小龍蝦在做什麼；小龍蝦換 session 後失憶

**解決方案**：建立三層同步機制

```
Telegram 對話（JSONL）
    ↓ 每 30 分鐘（有活動才執行）
memory/2026-04-11.md（小龍蝦的記憶）
    ↓ 同步
Claude Code 記憶庫（Claude 助教也看得到）
    ↓ push
GitHub（永久備份）
```

**核心腳本**：`/Users/bymyway/.openclaw/scripts/sync-telegram-memory.sh`

**書籤機制**（避免重複或遺漏）：
```json
{ "file": "/path/to/xxx.jsonl", "line": 500 }
```
- 換新 session → 書籤自動歸零，從頭讀
- 每次存完 → 更新書籤到最新行

**LaunchAgent**：`ai.openclaw.memory-sync`，每 1800 秒（30 分鐘）觸發

---

### 進化 5：Context Overflow 自動處理

**問題**：對話太長超過模型上限 → 報錯中斷工作

**設計邏輯（這是教練提出的關鍵問題）**：
> 「如果半小時還沒到，但對話框滿了，中間那段不就遺失了？」

**答案**：書籤機制解決這個問題

溢出時的執行順序（順序不可錯）：
```
① sync --force（從書籤到最後一行，全量存檔，一句不漏）
② 存入 memory/今天.md + 推 GitHub
③ 更新 HEARTBEAT.md（告訴新 session 讀什麼）
④ 清除舊 session + JSONL
⑤ 重啟 gateway
⑥ 小龍蝦讀 HEARTBEAT → 讀 memory → 告訴教練「已重啟請繼續」
```

**觸發條件**：JSONL > 500KB

---

### 進化 6：HEARTBEAT 即時上下文系統

**問題**：小龍蝦每次新 session 都不知道「現在在做什麼任務」

**解決方案**：`HEARTBEAT.md` 作為「熱上下文」
- 小龍蝦每 30 分鐘心跳讀一次
- Context Overflow 重啟後必讀
- Claude 助教每次修完問題就更新

**現在的 HEARTBEAT 包含**：
- 當前模型狀態
- 進行中任務
- 名稱對等關係
- 所有守則摘要

---

### 進化 7：守則標準化（教練今日確認）

| 守則 | 內容 |
|------|------|
| 名稱對等 | Telegram = 小龍蝦 = 電報（三個說法同一個意思） |
| 兩位助教 | Claude 助教 + 小龍蝦助教 |
| Token 限制 | 預估 5 萬先回報，10 萬必須暫停 |
| 語言 | 全部繁體中文，絕不夾英文 |
| 執行風格 | 能自己做直接做，不問「要幫你做嗎？」 |
| 截圖禁用 | 直接讀 JSONL 檔（省 100 倍 Token） |
| 進度通報 | 執行完立刻 Telegram 通報 |
| 記憶 | 事件發生立刻寫進 memory/今天.md |

---

## 📂 今日建立/修改的檔案清單

| 檔案 | 說明 |
|------|------|
| `scripts/sync-telegram-memory.sh` | 30分鐘自動同步 + --force 緊急存檔 |
| `scripts/auto-fix-session-lock.sh` | Session Lock + Context Overflow 自動處理 |
| `scripts/parse-session.py` | JSONL 解析器（零 Token） |
| `scripts/.sync-checkpoint.json` | 書籤檔（記錄存到哪個檔的哪行） |
| `memory/2026-04-11.md` | 今日完整工作日誌 |
| `HEARTBEAT.md` | 即時上下文（每次心跳必讀） |
| `~/Library/LaunchAgents/ai.openclaw.memory-sync.plist` | 30 分鐘同步 LaunchAgent |

---

## 🔗 Claude 助教 ↔ 小龍蝦助教 協作機制

```
教練（手機 Telegram）→ 小龍蝦執行
                              ↓ 出問題或需升級
教練（Claude Code）→ Claude 助教讀 memory/ → 診斷修復
                              ↓ 修復完
                        更新 memory/ + HEARTBEAT + GitHub
                              ↓
                        小龍蝦下次讀到新上下文 → 繼續工作
```

**重點**：Claude 助教看到的 memory 和小龍蝦看到的是同一套，透過 GitHub 和本地同步保持一致。

---

## ⏳ 待完成任務（今日未完成）

1. **NotebookLM 搬移驗證** — 腳本已跑，結果未確認
2. **YouTube 31 頻道掃描** — 排程已設（每天 12:30），今天因限流失敗
3. **Obsidian 第二大腦** — 尚未開始
