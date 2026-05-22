---
name: VPS 配對批准正確方式
description: 批准 Telegram 用戶配對到 VPS Bot 的正確指令
type: feedback
originSessionId: a78e6713-45fe-4963-a1f5-8d9909176c56
---
OpenClaw 在 VPS 上跑在 Docker 容器內，不能直接用 `openclaw` 指令，必須透過 `docker exec`。

正確指令：
```bash
sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200 \
  "docker exec openclaw openclaw pairing approve telegram [CODE]"
```

**Why:** 直接在 VPS host 跑 `openclaw` 會報 `command not found`，因為 openclaw 只存在於容器內部。

**How to apply:** 每次教練要批准新用戶配對時，一律用這個格式，不要在 Mac 本機或 VPS host 直接跑。
