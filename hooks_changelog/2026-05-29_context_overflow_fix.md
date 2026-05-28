# 小龍蝦對話兩句就滿 — 根治紀錄

**日期**：2026-05-29
**軍師**：Opus 4.7（終端機）
**教練症狀**：貼五場《超限戰》電影場次資料時，小龍蝦讀一則就說「對話記錄已滿」，等下一場又問「要做什麼」，反覆貼又反覆滿。
**教練拍板**：A + B + C 三方案全做（信念三「對的事就是長期有好處的事」）。

---

## 根因（三層）

| 層 | 病灶 | 浪費量 |
|----|------|--------|
| 1. 每則訊息注入 | `auto-goal/handler.js` 的 `TASK_PATTERNS` 含「幫我\|請你\|幫忙\|麻煩你」太寬，每則任務訊息都注入 850 字「執行合約」 | 5 則 ≈ 4250 字 |
| 2. 每則訊息注入 | `rule-reminder/handler.js` 關鍵字命中時注入提醒 | 50–200 字／則 |
| 3. 開工注入 | `client-memory/handler.js` 把 `CLIENT_PROFILE.md` 13.6KB 全文塞入，大半是 cron 蒸餾雜訊 | 13.6KB |

**佐證**：
- 小龍蝦自己 5/28 03:50 已診斷過（見 BOT_MESSAGES.md msgId 6578）
- 本場對話我親眼見 hook 每句都注入「🎯 執行合約」全文

---

## 修法

### A. auto-goal/handler.js → session-once 鎖

- 新增 `SESSION_MARKER = ~/.openclaw/workspace/state/auto_goal_session_marker.json`
- 以 `session_counter.json` 的 `bootstrapTime` 為 session 識別
- 同一場 session 命中任務訊號只注入第一次；新 session（counter 重建）才會再注入

### B. auto-goal/handler.js → TASK_PATTERNS 收窄

刪除：
```
/幫我|請你|幫忙|麻煩你/
/修改|更新|修正|修復|檢查|確認|驗證|測試一下|跑一下|執行一下/
```

保留（明確動作動詞）：
```
/你去|去讀|去寫|去建|去修|去查|去跑|去搜|去設|去確認|去測|去執行|去處理|去上傳|去部署|去更新|去刪/
/做一個|建一個|寫一個|設一個|建立|新增|產生|生成/
/開始做|繼續做|繼續執行|把.{1,20}做完|把.{1,20}完成|完成.{1,10}任務/
```

### C. client-memory/handler.js → CLIENT_PROFILE 截首 3500 字

- 舊：全文 13.6KB
- 新：檔首 3500 字（最新 1-2 天蒸餾），其餘提示「完整檔在 `~/.openclaw/workspace/CLIENT_PROFILE.md` 自行讀取」

---

## 驗證

- `node -c` 兩個 handler 語法 OK
- `launchctl unload && load ai.openclaw.gateway.plist` → 新 PID
- A+B 重啟 PID: 10877
- C 重啟 PID: 11177

---

## 預期效果

| 指標 | 改前 | 改後 |
|------|------|------|
| 開工注入 | 約 16KB | 約 5KB |
| 每則任務訊息 | 850 字合約 + 守則提醒 | 守則提醒（合約只本場第一次） |
| 教練貼 5 則資料 | 多塞 4250 字合約 | 多塞 850 字合約（首則） |

---

## 教練待測

下一場 session 跟小龍蝦對話：
1. 貼大量內容試試是否還會兩句就滿
2. 若仍滿 → 把當時的 chatId + 訊息序列回報，軍師繼續查
