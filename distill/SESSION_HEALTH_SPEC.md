# Session 健康度自我監測系統

> 設計者：軍師（Opus 4.7 Max via CLI）
> 日期：2026-05-25
> 目標：三端通用（終端機 / 小龍蝦 / VPS赫茲米）

---

## 一、問題定義

### 現況痛點
| 症狀 | 後果 |
|------|------|
| AI不知道context何時快滿 | 滿了才知道，已經來不及 |
| 15分鐘commit但從不主動reload | commit只是寫，沒讀等於白寫 |
| 舊內容被壓縮但AI不知道 | 教練問「你忘了嗎」，AI才發現 |
| 小龍蝦/VPS沒有CLI的API | 沒有直接token計數 |

### 三端差異
| 終端 | 監測方式 | reload方式 |
|------|---------|-----------|
| **終端機 CLI** | message count / rolling window | `/compact` 或重新開工 |
| **小龍蝦 Telegram** | 對話輪數 / 訊息量估算 | heartbeat機制 / 重新對話 |
| **VPS赫茲米** | 訊息輪數 / 檔案蒸餾頻率 | 自動蒸餾後reload |

---

## 二、健康度等級（核心演算法）

```
健康度 🟢  輪數  0-15  → 正常，不干擾
警戒度 🟡  輪數 16-25  → 主動告知「session已過半」
警告度 🟠  輪數 26-35  → 明確告知「session快滿，準備reload」
危急度 🔴  輪數 36-50  → 立即reload，告知教練
重置線   50+    → 已經太晚，告知教練「有些內容可能已壓縮」
```

> 為什麼是50輪？基於Claude Code CLI實測，約50輪對話後context開始不穩定。

### 進階演算法（終端機用）

```
tokens_estimated ≈ turns × avg_turn_size
context_ratio = tokens_estimated / context_limit (100萬)

🟢 < 60%  → 正常
🟡 60-75% → 即將進入警戒
🟠 75-90% → 立即reload
🔴 > 90%  → 已經壓縮，來不及了
```

### 進階演算法（小龍蝦Telegram用）

小龍蝦沒有直接token計數，改用「對話段落密度」：

```
段落長度 = 最近N個來回的教練發言總字數
密度比 = 段落長度 / 段落長度上限（2000字）

🟢 密度比 < 50% → 正常
🟡 密度比 50-70% → 即將進入警戒
🟠 密度比 70-85% → 立即reload
🔴 密度比 > 85% → 已經壓縮
```

---

## 三、輸出格式（通用警告訊息）

### 🟢 健康（不說話）
```
（正常，不干擾）
```

### 🟡 警戒
```
━━━ 健康度 🟡 輪 #N | 估 ~XK tokens | 距離刷新線：Y輪
💡 小提醒：session已運行 {N} 輪，隨時可以 /compact 或重新開工。
```

### 🟠 警告
```
━━━ 健康度 🟠 輪 #N | 估 ~XK tokens | 距離刷新線：Y輪
⚠️ 教練，session快滿了。建議 /compact 或重新開工。
```

### 🔴 危急
```
━━━ 健康度 🔴 輪 #N | 估 ~XK tokens | 上下文已壓縮
🚨 教練，session已超載，已經開始壓縮內容了！
建議立即 /compact 或重新開工，舊內容由接力棒銜接。
```

---

## 四、觸發時機

每次教練發言後，AI自動做一次健康度檢查：

```
教練發言
  → [執行任務]
  → [健康度檢查]  ← 每次必做
  → [回報教練]
```

不主動打斷教練。健康度資訊可以附在回覆最後。

---

## 五、實作方式

### 終端機 CLI（Python script）
- `scripts/session_health.py` — 健康度計算
- 內嵌在 AGENTS.md / CLAUDE.md 作為行為準則

### 小龍蝦 Telegram（MD格式）
- 在 heartbeat 流程中加入健康度檢查
- 透過 relay 訊息格式傳遞健康度

### VPS赫茲米（Python script）
- `scripts/session_health_vps.py` — 適用於 memory蒸餾後的session
- 自動reload机制

---

## 六、接力棒銜接機制

當session reload後，下一個視窗開工時：

1. git pull → 恢復雲端最新狀態
2. 讀取 `HEARTBEAT.md` → 知道上一個session的最後狀態
3. 讀取 `JUNSHI_HANDOFF_LATEST.md` → 知道未完成的任務
4. 回報教練：「上一個session最後做到了⋯，現在銜接⋯」

---

## 七、Commit Hash追蹤

| 日期 | Commit | 更新內容 |
|------|--------|---------|
| 2026-05-25 | `本檔新建` | Session健康度自我監測系統規格 |
