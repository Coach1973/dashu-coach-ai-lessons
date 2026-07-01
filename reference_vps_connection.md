---
name: vps-connection
description: VPS 連線資訊與指令，任何電腦的 Claude Code 都能直接 SSH 上去操作
metadata:
  type: reference
---

## VPS 連線資訊

教練說「連 VPS」「開 VPS」「上線」時，直接用以下資訊 SSH 連線，不要再問。

### 小龍蝦 VPS（對外體驗版）
- **IP:** `43.245.60.200`
- **User:** `root`
- **Password:** `9kdxvQN2`
- **用途:** 外部朋友體驗版（coach.bymyway.com / Telegram）
- **連線指令:**
  ```
  sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200
  ```
- **Docker 指令:**
  ```
  sshpass -p '9kdxvQN2' ssh root@43.245.60.200 "docker exec openclaw openclaw [指令]"
  ```

### 赫茲米 VPS（Hermes）
- **IP:** `113.29.232.178`
- **User:** `root`
- **Password:** `C8GwSuyj`
- **Port:** 8642 對外
- **用途:** 跑 Hermes Agent
- **連線指令:**
  ```
  sshpass -p 'C8GwSuyj' ssh -o StrictHostKeyChecking=no root@113.29.232.178
  ```

**How to apply:** 任何電腦上的 Claude Code 只要 pull 了 mac-openclaw-workflows repo，就能直接讀取這份檔案並連線操作 VPS，不需要額外設定 SSH Key。

Related: [[acer-post-restore-todo]], [[openclaw-spool-stuck-fix]]
