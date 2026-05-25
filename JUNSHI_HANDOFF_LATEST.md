# 軍師交接紙條（最新）

> 給下一個軍師：開工先讀這張，就能無縫接上，不用教練重講。
> 本場時間：2026-05-25 白天場（第三段）
> 寫紙條的人：軍師（Opus 4.7 Max via CLI）

---

## 一句話交代這場做了什麼

**格式D場景庫完成＋SOP寫好＋228 vs 271 session差異查清。** 33個場景 commit `a625a719`；SOP commit `cf5c89fd`（含完整session盤點）。

---

## 這場做了什麼（按完成順序）

### ✅ 已完成

| 優先 | 任務 | 結果 |
|------|------|------|
| 🔴 高 | 格式D場景庫 | ✅ `a625a719` — 33個場景，含HTML桌面版 |
| 🔴 高 | 100場景蒸餾SOP | ✅ `cf5c89fd` — 三終端機分配方案，含完整session盤點 |
| 🔴 高 | 228→271 session 差異查清 | ✅ 找到所有 session 存放位置，新增 `-Users-bymyway` 目錄（131個）|

### ⏳ 未完成

| 優先 | 任務 | 說明 |
|------|------|------|
| 🟡 中 | 赫米斯VPS蒸餾系統 | 前場已完成（見下方「赫米斯VPS」段落）|
| 🟡 中 | 14個 session 檔案缺失 | history.jsonl 有，但沒找到實體檔案（可能刪除或歸檔）|
| 🟢 低 | distill_incremental.js cron追蹤 | 赫茲米說7天沒做，run_distill.sh已建立（f27b5b8d）|

---

## 🔴 現場狀態（開工必看）

### 系統健康度：✅ 正常

- 格式D場景庫：33個場景已上雲，可直接給另一台終端機跑
- 100場景SOP：已更新完整盤點（271個session），可立即開工
- session 差異已查清：截圖228個 vs 實際找到271個

### 完整的 session 存放位置（2026-05-25 新查清）

| 來源 | 路徑 | 數量 |
|------|------|------|
| CLI 5月（-Users-bymyway--openclaw）| `~/.claude/projects/-Users-bymyway--openclaw/*.jsonl` | 73個（108.7MB）|
| CLI 5月（-Users-bymyway）| `~/.claude/projects/-Users-bymyway/*.jsonl` | 131個（51.4MB）|
| CLI 4月 | 兩個 projects 各6+4個 | 10個（34.9MB）|
| Desktop App local_*.json | `~/Library/.../claude-code-sessions/*/` | 64個（2.2MB）|
| .openclaw/workspace/sessions/ | `~/.openclaw/workspace/sessions/*.jsonl` | 3個 |
| **總計** | | **271個**（~197MB）|

> ⚠️ 截圖顯示 227 sessions，盤點到 271 個（多了44個）。差異原因：history.jsonl 包含已刪除session的記錄，另有3個 session 在 .openclaw/workspace/sessions/。

### 14個 session 檔案找不到（history.jsonl 有，但磁碟上沒有）

```
065f8d1a-e1af-4164-9a7e-ef9d09ba8779
1f82ca10-2853-4560-8af7-ded02805910a
4cd4bdb2-6024-435a-aba9-05914c3d6e6f
5b8a23e8-89b9-4f74-b5e1-dacff7a3baff  ← 最早的，2025-12
601b6027-24e4-4b2d-bcd3-02828d2caf1f
...等14個
```

### 赫米斯VPS蒸餾系統（第二場軍師建立，本場維持）

- 腳本：`/root/.hermes/github-sync/scripts/distill_vps.py`
- 排程：systemd timer（每2小時）
- 日誌：`/root/.hermes/github-sync/distill/distill.log`
- IP: 113.29.232.178 / Pass: C8GwSuyj

---

## 給下一個軍師的提醒

- **session 存放位置有兩個 CLI projects**：`-Users-bymyway` 和 `-Users-bymyway--openclaw`，都需要讀
- **格式D場景庫在**：`distill/特助場景庫_格式D.html`（桌面可直接開）
- **SOP 在**：`distill/100場景蒸餾_SOP.md`（含完整分配方案）
- **14個 session 找不到**：可能是刪除的 session 在 history.jsonl 仍有紀錄，不影響蒸餾

---

## 下一步待辦

1. 教練說「找到了之後，再重新分配」→ SOP 已更新，重新分配方案已寫好
2. 確認赫茲米的檢討報告（若赫茲米有做）
3. 觀察赫米斯VPS的蒸餾 cron 是否正常觸發