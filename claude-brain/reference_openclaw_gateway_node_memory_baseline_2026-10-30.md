---
name: reference-openclaw-gateway-node-memory-baseline-2026-10-30
description: 教練說「node 佔 2.15G」＝小龍蝦主程式 ai.openclaw.gateway（pid 5462→重啟後 93627）；重啟後開機就回到約 1.7～1.9G（V8 堆積約 1.3G），重啟只能省約 0.3～0.4G；Mac mini 16G、可用 63%
metadata:
  node_type: memory
  type: reference
  originSessionId: 19560b24-fe5c-400f-8d97-05a71e2c8f34
  modified: 2026-10-30T15:22:43.703Z
---

10/30 23:19（台灣時間）教練問「那個 node 佔 2.15G，可以解決嗎」。查到：
- 該 node ＝ `ai.openclaw.gateway`（小龍蝦），啟動 12:58 台灣時間（10/30 升 2026.10.9 之後），跑 10 小時 24 分時 Activity Monitor「記憶體」2231M（其中壓縮 735M）。其他 node（rea mcp、Claude Helper）都只有 5～60MB。
- 23:20:18 用 `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway` 重啟：新 pid 93627，LINE／Telegram（bot_main、bot_kong、bot_peipei）／cron（48 個）都重新起來。但剛開機 50 秒就 RSS 1.7～1.8G，Activity Monitor 約 1.8～2.0G。vmmap：V8 堆積（Memory Tag 255）約 1.3G ＋ malloc 小區 250MB。所以「跑久才變大」只佔約 0.4G／10 小時，大頭是開機就載入的東西，重啟沒法解決。
- 系統：16GB、可用 63%、swap 用 661MB／2GB，沒有記憶體壓力。V8 堆積上限預設 4288MB。

**How to apply:** 教練再問 node 吃記憶體，先 `ps` 排序確認是不是 gateway，不要再當成「重啟就好」。要真的降低要查開機載入什麼（8 個分身的 sqlite／外掛／暫停中的 Discord 等），那是另一件事，沒做、沒有任何根因結論。相關：[[reference_llama_server_memory_ubatch_wrapper_2026-10-12]]。
