---
name: reference_per_user_memory_three_systems_2026-09-25
description: 教練要求「每位朋友對話單獨記憶」在三套系統各自怎麼實作、怎麼驗證；2026-09-25修好LINE記憶被巡檢指令灌爆+200KB上限停寫的bug
metadata:
  node_type: memory
  type: reference
  originSessionId: d10cf0ba-2bbd-4573-8dfe-4ac4ed4d0a76
  modified: 2026-09-24T16:58:59.401Z
---

教練的要求：VPS版、「教練都在想什麼」、「大台南小幫手」每一位朋友的對話都要單獨記憶，才能記得住對方說過什麼。三套實作方式不同：

**Mac LINE 三帳號（龍蝦小助教 main／bni_tainan／jiaolian_thoughts）**
- 對話分開：openclaw.json 的 line 路由 `session.dmScope: per-channel-peer`
- 記得住：`~/.openclaw/hooks/line-user-memory/handler.js`（伺服器端 hook，不靠 AI 自己寫），每則訊息 append 到 `~/.openclaw/agents/<帳號>/clients/<userId>.md`，每則訊息注入該檔最後 3000 字
- 驗證方法：比對 `workspace/state/inbound_echo/*.jsonl` 每個人最後一則訊息時間 vs 他的 clients 檔最後寫入時間

**2026-09-25 修好的兩個 bug**：①小龍蝦2.0每30分鐘巡檢指令（開頭 `Follow the heartbeat monitor scratch context`，OpenClaw 原始碼常數 HEARTBEAT_CONTEXT_PROMPT）掛在教練 LINE 對話底下，9/22 起被當成教練說的話寫進記憶，佔檔案 96%，回想時只讀到巡檢文字 ②`MAX_FILE_BYTES` 200KB 上限原本寫成「超過就停止寫入」（註解卻說續記），教練的檔案 9/24 06:20 起完全不記。已改成巡檢不記、超過上限整份搬進 `clients/_archive/` 後續記；教練的檔案原檔封存為 `_archive/…polluted-heartbeat-20260925.md`，新檔只留 13 筆真話。外層 repo commit `e4cc4209c`。

**VPS 體驗版（Telegram 朋友）**
- 對話分開：每位朋友開通時就是獨立 agent `trial-<telegramId>` + 獨立 workspace `workspace-trial-<id>`
- 記得住：OpenClaw 內建記憶——AI 當天寫 `memory/YYYY-MM-DD.md` → 每晚 dreaming 整理（`memory/dreaming/light/`）→ `memory-core.autoRecall` 下次自動帶出。不是伺服器端逐字記錄，靠 AI 自己寫每日記憶
- 朋友空間**沒有** `CLIENT_PROFILE.md`（那是主帳號給教練用的，`hooks/client-memory` 只對教練 6124913915 注入；外部朋友讀 `workspace/clients/<id>.md`，只有 3 份 7/1 手寫檔）。規則要寫「寫進每日記憶」，不能寫 CLIENT_PROFILE（09-25 已改正，VPS commit `856342502`）
- 連 VPS：沿用 `scripts/vps_xiaolongxia_healthcheck.sh` 既有的連線設定，輸出不顯示密碼

Related: [[feedback_ask_coach_three_gates_root_fix_2026-09-24]]
