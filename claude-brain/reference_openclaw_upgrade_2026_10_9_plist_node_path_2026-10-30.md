---
name: reference-openclaw-upgrade-2026-10-9-plist-node-path-2026-10-30
description: 小龍蝦 10/30 升到 2026.10.9：主服務 plist 寫死舊 Node 24.21.0 導致升級卡 20 分鐘、全分身沒反應；改 Node 24.22.2 修好；升級後現況（版本、Node、閘門、補丁、日誌字樣改變）與升級超過 5 分鐘先看什麼
metadata:
  node_type: memory
  type: reference
  originSessionId: 972c1bc8-aa67-4f97-a8bc-39bd61222b6a
  modified: 2026-10-30T05:26:30.396Z
---

**現況（10/30 13:00 查證）**：OpenClaw 2026.10.9；主服務由 `~/Library/LaunchAgents/ai.openclaw.gateway.plist` 啟動，第 3 個參數現在是 `~/.nvm/versions/node/v24.22.2/bin/node`（舊的寫死 v24.21.0，新版要求 Node ≥24.22.1 <25 或 ≥26.12.1）；程式本體仍在 `~/.nvm/versions/node/v24.21.0/lib/node_modules/openclaw/`（套件原地更新）；`nvm default` 改成 24.22.2。plist 備份：`workspace/state/ai.openclaw.gateway.plist.bak-20261030-1255`。**這取代舊記憶裡「實際在跑 2026.9.4」的說法**（見 [[reference_peipei_dm_allowlist_dmscope_and_openclaw_nvm_copy_2026-10-26]]、[[reference_delegate_to_xiaolongxia_openclaw_agent_and_run_img_list_2026-10-30]]）。

**事件**：12:35 另一對話框啟動升級，12:39 停主服務；新版不支援舊 Node，主服務每 10 秒重開失敗 61 次（`~/Library/Logs/openclaw/gateway.log` 寫「Node 24.21.0: openclaw requires Node >=24.22.1」），升級收尾等它起來而卡住，全分身沒反應。我前面乾等通知，教練嫌「升級哪有 12 分鐘」才查。12:55 改 plist 後恢復，12:56 升級程式自己結束。巴哈真訊息 34 秒回、鎖沒觸發。案例 140、反射 `R-OPENCLAW-UPDATE-NODE-PATH`。

**升級後要記得**：①LINE 推播閘門 V2 升級後仍在（`line_push_gate_patch.py --check`）；②英文錯誤訊息中文補丁 `scripts/openclaw_zh_errmsg_patch.py <新版 dist 路徑>`，下次重啟主服務才生效；③日誌送出訊息字樣新版改成 `telegram text delivery ok`（舊的 `outbound send ok` 只偶爾出現）——寫盯梢程式別只比對舊字樣（我 13:04 因此誤報）；④升級程式自己警告 plist 指向 nvm 版本資料夾「升級後可能再壞」，還沒穩定化；⑤升級程式 `openclaw-update` 超過 5 分鐘沒結束＝有問題，先 `launchctl print gui/$(id -u)/ai.openclaw.gateway`（runs、last exit code）＋看 `gateway.log` 尾巴，不要等。

**Why:** 教練 12:54 要求「升級哪有這麼久」要自己看出異常；**How to apply:** 任何升級／安裝跑超過預期，先查服務狀態與錯誤紀錄，不設通知乾等。
