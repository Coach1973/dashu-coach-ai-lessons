---
name: reference-peipei-group-context-overflow-blocks-main-lane
description: 巴哈（peipei）佩佩老師群組對話塞爆 135%，整理對話每次卡 5 分鐘並佔住共用處理通道，連小龍蝦（main）也沒反應；診斷與處理指令、還沒驗證的部分
metadata:
  node_type: memory
  type: reference
---

**症狀（10/24 09:38 教練說「巴哈又卡住、小龍蝦也卡住」）**：日誌 `/tmp/openclaw/openclaw-今天.log` 出現 `Context overflow: prompt too large`、`lane task error: lane=main durationMs=284812 … stalled … handler-timeout`，同一則 Telegram 更新（event 156732124，群組 -5115910257 的訊息 2248）一直重試。
**查到的根因**：`agent:peipei:telegram:group:-5115910257`（sessionId ccfa35c7…）上下文 277k／205k（135%），transcript 27.5 MB，自動壓縮（compaction）每輪約 5 分鐘、超過 300 秒就逾時，而且佔住 `lane=main`，所以小龍蝦的訊息也排不進去。另有 07:15 MiniMax 限流 HTTP 429 把佩君老師「標題往左下」那輪弄死。
**做了什麼**：①備份 `workspace/state/backup_peipei_agent_sqlite_20261024_0940.sqlite` ②`launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`（版本前後都 2026.9.4）→小龍蝦被打斷後自己接著做完、09:41:26 回覆教練 ③`openclaw sessions compact "<key>" --agent peipei --max-lines 150` 與 `sessions archive` 兩個指令都回報 ok。
**沒驗證的**：compact／archive 後清單仍顯示同一個 sessionId、135%，沒看到真的縮小；巴哈群組也還沒真的回過佩君老師。下一次她在群裡講話，先看有沒有回覆，再 `openclaw sessions --agent peipei` 看 ctx %。
**How to apply:** 小龍蝦與巴哈同時沒反應 → 先查日誌有沒有 overflow／lane stalled，看哪個 session 的 ctx % 超過 100；`--active N` 可只看最近活動的 session。
相關：[[reference-openclaw-agent-repeat-loop-and-guard]]、[[reference-openclaw-transcripts-in-agent-sqlite]]
