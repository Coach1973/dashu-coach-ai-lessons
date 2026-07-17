---
name: openclaw-polling-restart-loop
description: VPS 小龍蝦 Telegram polling 持續 health-monitor restart loop 的診斷與修復方法（與 .processing 阻塞不同）
metadata: 
  node_type: memory
  type: project
  originSessionId: f9a18d7e-b1b9-4efb-a82d-7c2e3a4c8e91
---

## VPS 小龍蝦 Telegram polling 卡在 health-monitor restart loop — 診斷與修復 SOP

**⚠️ 跟 `.processing` 卡住是不同的問題，症狀、診斷、修法都不同。**

---

### 跟 `.processing` SOP 怎麼分？

| 現象 | `.processing` 阻塞（舊 SOP） | **health-monitor restart loop（本 SOP）** |
|------|----------------------|--------------------------|
| 用戶訊息 | 卡住不消化，spool 堆一堆 | 大部分沒問題，polling 啟動又立刻停 |
| container log | 沒看到 Inbound | 看到 **每 15 分鐘一行** `[health-monitor] restarting (reason: stopped)` |
| gateway /health | `{"ok":true}` | `{"ok":true}` |
| ingress-spool | **非空**，有 `.processing` 殘留 | **空**，沒有 .processing |
| 真正 root cause | MiniMax M3 過載 → LLM 超時 → processor 不消化 | Telegram API 短暫 502/deleteWebhook timeout → polling 啟動後立刻停 |

---

### Why（為什麼會發生，2026-07-17 教訓）

`api.telegram.org` 短暫 502 Bad Gateway，或 Telegram Bot API IP 在某些網段被 timeout 時：
1. openclaw 啟動 Telegram provider，第一步呼叫 `deleteWebhook`
2. deleteWebhook 失敗 → channel exit code 1
3. health-monitor 看到 polling `stopped` → 觸發 restart
4. 重啟又遇到同樣網路問題（或 polling child 內部狀態髒了）→ 立刻又 stop
5. 進入 30 秒 → 5 分鐘 → 15 分鐘無限循環
6. 即使後來 Telegram API 恢復了，polling child process 的內部狀態可能髒了，**只重啟 child 不夠**

---

### 怎麼辨認這個問題（4 個訊號全對才是）

```bash
ssh root@43.245.60.200 "docker logs --tail 100 openclaw 2>&1 | grep health-monitor"
```
**訊號 1**：看到 `[health-monitor] restarting (reason: stopped)` 或 `(reason: disconnected)` 每 15 分鐘循環

```bash
ssh root@43.245.60.200 "docker exec openclaw ls /home/node/.openclaw/telegram/ingress-spool-default/"
```
**訊號 2**：`ingress-spool-default` **是空的**（沒有 .processing 殘留）

```bash
ssh root@43.245.60.200 "docker logs --tail 200 openclaw 2>&1 | grep -E 'getMe|deleteWebhook'"
```
**訊號 3**：曾經看到 `fetch timeout`、`502 Bad Gateway`、`deleteWebhook failed`

```bash
ssh root@43.245.60.200 "curl -s --max-time 5 'https://api.telegram.org/bot<TOKEN>/getMe'"
```
**訊號 4**：現在直連測 `getMe` 已經 ✅ 通，但容器內 polling 還是壞的

**4 個全對 = 本 SOP 適用，只看訊號 2 但沒訊號 1 = 走 `.processing` 舊 SOP。**

---

### 為什麼自動 force-restart 救不了？

Mac mini 上的 `launchctl kickstart -k ai.openclaw.gateway` 是 macOS LaunchAgent，**無法觸及 VPS container 內 systemd unit**（VPS container 沒 systemd），所以對容器內的 health-monitor 完全沒作用。

這是 2026-07-09 到 2026-07-17 反覆發生同樣症狀、自動 force-restart 都沒清乾淨的原因。

---

### How to apply（推薦修法）

**✅ 推薦：直接重啟整個 Docker container（2026-07-17 驗證有效，2026-06-23 同款）**

```bash
sshpass -p '9kdxvQN2' ssh root@43.245.60.200 'docker restart openclaw'
```

**然後等 15 秒驗證：**
```bash
sshpass -p '9kdxvQN2' ssh root@43.245.60.200 '
curl -s --max-time 5 http://127.0.0.1:18789/health
echo
docker ps --format "{{.Names}}\t{{.Status}}"
docker logs --tail 30 openclaw 2>&1 | grep -E "health-monitor|telegram|isolated polling ingress" | tail -10
'
```

**期望看到：**
- `{"ok":true,"status":"live"}` ✅
- `Up <N> seconds (healthy)`
- `[health-monitor] started (interval: 300s)` ← 全新
- `[telegram] isolated polling ingress started` ← polling 復活
- 沒有再出現 `[health-monitor] restarting (reason: stopped)` 字樣

**⚠️ 不要用 `openclaw gateway restart` 在容器內跑**：會踩到「Gateway service disabled」陷阱（容器無 systemd），這個 CLI 在 container 環境只會 disable service 不會啟動。

---

### 副作用 & 注意事項

- `docker restart openclaw` 會中斷所有運行中的 session 5-10 秒（gateway 重啟時間）
- 但這台 VPS 對外版主要給外部朋友體驗用，目前沒人在跑 session，影響低
- 重啟後會自動跑 state-migrations，把 legacy 狀態遷到 SQLite（正常現象）
- 重啟後 last_inbound_age 可能從頭計算（state 重置）

---

### 何時該用 `.processing` 舊 SOP，何時用本 SOP？

| 狀況 | 用哪個 |
|------|--------|
| spool 有 .processing 殘留檔 | 舊 SOP（清 .processing） |
| spool 為空 + log 一直 restart loop + getMe 現在通 | **本 SOP**（docker restart） |
| spool 為空 + 不見得重啟 loop + getMe 也失敗 | 兩個都不能用，先修 Telegram API 連線 |

Related: [[openclaw-spool-stuck-fix]], [[vps-connection]]
