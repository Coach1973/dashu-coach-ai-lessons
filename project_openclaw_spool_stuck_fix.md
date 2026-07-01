---
name: openclaw-spool-stuck-fix
description: VPS 小龍蝦 Telegram 訊息卡住的診斷與修復方法（ingress spool .processing 檔案阻塞）
metadata: 
  node_type: memory
  type: project
  originSessionId: a4314073-04dc-4cea-ae43-48543d5ca592
---

## VPS 小龍蝦 Telegram 用戶訊息卡住 — 診斷與修復 SOP

當 MiniMax M3（或其他模型）發生過載/超時，會導致 ingress spool 裡的 `.processing` 檔案卡死，阻塞同一用戶後續所有訊息。

**Why:** 2026-07-01 MiniMax M3 整天過載（503 overloaded + 408 timeout），最早開通的用戶（Lin Yu Ju、CHIU YuJung、教練）的第一則訊息被 claim 後 LLM 超時，`.processing` 檔案永遠不會被清除，導致該用戶後續所有訊息都堆在 spool 裡無法處理。其他後來開通的用戶因為 MiniMax 恢復後才發訊息，所以正常。

**How to apply:**

### 症狀判斷
- 用戶發訊息但完全沒有回應
- `docker logs openclaw` 看不到該用戶的 Inbound 記錄（或只看到 Inbound 沒有回覆）
- 其他用戶正常

### 診斷步驟
```bash
# 1. 確認 Gateway 運作正常
ssh root@43.245.60.200 "curl -s http://127.0.0.1:18789/health"
# 應回傳 {"ok":true,"status":"live"}

# 2. 檢查是否有卡住的 .processing 檔案（這是關鍵！）
ssh root@43.245.60.200 "docker exec openclaw find /home/node/.openclaw/telegram/ingress-spool-default/ -name '*.processing'"

# 3. 查看卡住的是哪個用戶
ssh root@43.245.60.200 "docker exec openclaw cat /home/node/.openclaw/telegram/ingress-spool-default/<檔名>.processing"
```

### 修復方法
```bash
# 方法一：只清除 .processing 檔案（溫和，保留未處理訊息）
ssh root@43.245.60.200 "docker exec openclaw rm /home/node/.openclaw/telegram/ingress-spool-default/*.processing"

# 方法二：清除特定用戶的所有積壓（徹底，用於大量堆積時）
ssh root@43.245.60.200 "docker exec openclaw sh -c 'cd /home/node/.openclaw/telegram/ingress-spool-default && rm -f *.processing && for f in *.json; do grep -q <用戶ID> \"\$f\" && rm \"\$f\"; done'"

# 清除後讓用戶重新發一則訊息即可
```

### 注意事項
- 不需要重啟 Gateway 或 Docker container
- 清除 `.processing` 檔案不會影響已建立的 session
- 如果模型仍在過載，新訊息會再次卡住，需等模型恢復或換模型
- `openclaw doctor` 和 `openclaw status --deep` 不會顯示 spool 阻塞問題，必須手動檢查 `.processing` 檔案

Related: [[minimax-m3-overload-pattern]]
