---
name: reference-peipei-dm-allowlist-dmscope-and-openclaw-nvm-copy-2026-10-26
description: 巴哈機器人私訊開通（allowlist＋獨立對話）、Telegram 要對方先按 Start；英文錯誤訊息改中文且小龍蝦實際在跑 nvm 那份；寫入失敗自動換新對話規則
metadata:
  node_type: memory
  type: reference
  originSessionId: 36eddc83-dbc1-4766-a862-fef378a60de5
  modified: 2026-10-25T17:51:22.094Z
---

**私訊**：openclaw.json `channels.telegram.accounts.bot_peipei` 加 `dmPolicy:"allowlist"`、`allowFrom:["8786886419"(佩佩老師), "6124913915"(教練)]`；巴哈那條 binding 加 `session.dmScope:"per-channel-peer"`（預設 main＝所有人私訊共用 `agent:peipei:main`，會跟教練的私訊混在一起）。教練 10/26 01:28 私訊 @coachwu_lenovo_bot 實測收發通。**Telegram 規定機器人不能先對沒開過對話的人傳訊息（403）**，佩佩老師要先按一次 Start。outer repo `01098ca95`、`58f1de197`。binding 改動小龍蝦會等工作做完才套用，等滿 5 分鐘就強制重連 Telegram（所以當下巴哈會斷線幾秒）。

**教練為什麼留在群組（他 10/26 原話）**：本來就想夥伴習慣後讓他們自理；他在裡面是因為小龍蝦問題多、他看到問題就知道怎麼處理、能第一時間知道。專案（如台鐵）才開單獨一段對話。

**英文錯誤訊息改中文**：「Something went wrong while processing your request…」是小龍蝦內建固定字串。**實際在跑的是 `~/.nvm/versions/node/v24.21.0/lib/node_modules/openclaw/dist`（不是 /opt/homebrew 那份）**；補丁腳本 `scripts/openclaw_zh_errmsg_patch.py`（冪等、先備份），小龍蝦更新後要重跑再重啟。`worker/worker.mjs` 的 `node --check` 本來就會失敗，不是補丁造成。

**寫入失敗自動換新對話**：日誌 `SessionTranscriptWriterClaimReboundError`（對話寫入壞掉，每則訊息立刻失敗）；`openclaw_stall_watchdog.py` 新增 CLAIM_RE，同一對話 10 分鐘內 2 次就 `sessions delete` 並通知教練（workspace `4214cc182`，未真實觸發過；根因為何壞掉仍不明）。

**重啟 gateway 前**：先確認用 nvm 的 openclaw（`2026.9.4`），與服務是同一版（案例73）。
