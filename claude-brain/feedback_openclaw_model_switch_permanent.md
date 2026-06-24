---
name: feedback_openclaw_model_switch_permanent
description: 切換 openclaw.json 模型必須直接改設定檔，UI 切換是臨時狀態，重啟就消失——血淚教訓：損失 $60 美金
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4fc91aea-4bac-4b6d-a75f-799b21425b4e
---

UI 手動切換模型 ≠ 永久設定，必須直接修改 `~/.openclaw/openclaw.json` 的 `agents.list[].model` 欄位，才能在 gateway 重啟後持續生效。

**Why:** 2026-05-25 教練手動切換 main 機器人到 MiniMax，UI 切換只改執行期狀態，不寫入 openclaw.json。三天內 gateway 多次重啟，main 每次都彈回 kimi/kimi-k2.6。無任何助教主動警告，導致損失約 $60 USD Kimi API 費用。教練原話：「60 塊美金不少錢啊。」

**How to apply:**
1. 開工必查：確認 main model 是否為 `minimax/MiniMax-M2.7`
   ```
   cat ~/.openclaw/openclaw.json | python3 -c "import json,sys; [print(a['id'],a['model']) for a in json.load(sys.stdin)['agents']['list']]"
   ```
2. 模型切換後：直接改 openclaw.json → 重啟 gateway → cat 驗證 → 回報結果
3. UI 切換不算數，永遠以 openclaw.json 為準
4. 已永久設定：main → `minimax/MiniMax-M2.7`（2026-05-27，commit f7298df3）

Related: [[project_hermes_minimax_switchback]], [[feedback_openclaw_json_forbidden]]
