---
name: mac-bot-relay-retired
description: 學長/學弟/學妹三機協作退役土法煉鋼bot-relay機制，改用官方sessions_send/agentToAgent（該功能其實已啟用只是沒人告知教練）
metadata: 
  node_type: memory
  type: project
  originSessionId: e800e341-3d04-4ed4-bf2a-f43e799bb9e4
---

2026-07-02凌晨，教練要求對Mac端學長(main)/學弟(kong)/學妹(peipei)三個Telegram bot在同一群組協作的機制做大盤查，並依信念二查OPE最新做法。

**大盤查發現**：
1. 現有架構：main/kong/peipei各自獨立agent，各自綁定專屬Telegram bot帳號（bot_main/bot_kong/bot_peipei），三個bot都是同一個supergroup（-1003877502911）成員，靠mention機制輪流發言——這層Telegram群組運作正常，不用動。
2. **意外發現**：官方內建的`sessions_send`工具（讓agent間直接互傳訊息討論，不透過Telegram）搭配`tools.agentToAgent.enabled:true`其實**已經設定好且啟用**，allow清單正是`["main","kong","peipei"]`——這代表4月`project_multiagent_2026-04-23.md`記錄的待辦「還差sessions_send接線」，後來已經有人補上了，只是沒有留下明確記錄讓教練/後續軍師知道已經完成。
3. **同時發現重複**：舊的土法煉鋼機制`bot-relay`（發言寫入共用日誌`BOT_MESSAGES.md`）+ `bot-relay-inbound`（收到人類訊息時讀日誌，注入其他Bot最近發言）**同時在跑**，跟官方機制疊床架屋。

**OPE查證結果**：2026年OpenClaw官方推薦的多bot同群組協作做法，就是用`sessions_send`+`tools.agentToAgent`做agent間內部討論（可靠、可稽核、不受Telegram傳遞怪癖影響），只把最終共識貼回可見群組——這正是Mac已經配好但沒充分利用的機制。

**已執行的簡化**：
- 關閉`bot-relay`與`bot-relay-inbound`兩個hook（`openclaw.json`的`hooks.internal.entries`，兩者`enabled`改為`false`）
- 備份：`~/.openclaw/openclaw.json.bak-before-relay-retire-20260702-020543`
- `openclaw gateway restart`重啟生效，`openclaw hooks list`確認兩者顯示`disabled`
- `openclaw agents list --bindings`確認main/kong/peipei路由規則不受影響，main仍是default
- `tools.agentToAgent`設定確認未被動到，維持`enabled:true, allow:["main","kong","peipei"]`

**Why**：教練要求「結果簡單一點」——兩套機制同時存在是不必要的複雜度，官方機制更穩定（內建`maxPingPongTurns`上限避免無限來回、`REPLY_SKIP`可提早結束），且已經設定正確，退役舊的DIY機制是最簡單的路。

**How to apply**：以後若三機需要互相討論協調，agent應主動呼叫`sessions_send`工具，而不是依賴被動的共用日誌注入。若退役後發現三機彼此感知變差（例如沒被mention到的bot對群組近況一無所知），可以考慮重新評估——但這是需要教練實際觀察一段時間才能判斷的事，非本次工程範圍。

Related: [[project_multiagent_2026-04-23]]（原始4月架構記錄，已部分過時）
