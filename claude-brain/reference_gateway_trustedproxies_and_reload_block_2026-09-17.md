---
name: reference-gateway-trustedproxies-and-reload-block-2026-09-17
description: bni.bymyway.com/seabiscuit.bymyway.com監控頁404其實是403 proxy_attribution_required——gateway.trustedProxies缺設定+doctor--fix才能解除卡住的config熱重載
metadata:
  type: reference
---

**症狀**：`bni.bymyway.com`、`seabiscuit.bymyway.com`（gateway controlUi的兩個對外網址）回應 HTTP 403，內容 `{"error":{"message":"Proxy client attribution is required. Configure gateway.trustedProxies narrowly..."}}`。

**根因**：`openclaw.json` 的 `gateway.trustedProxies` 從未設定過。這是較新版本 OpenClaw 的安全機制——gateway 要求明確告知「哪個位址是可信任的代理」（cloudflared tunnel 在本機透過 loopback 連進 gateway），沒設定就一律拒絕，回應跟真的斷線/DNS問題完全不同（是403不是502/522/530），容易被誤判成「網頁掛了」。

**修復**：在 `openclaw.json` 的 `gateway` 底下加：
```json
"trustedProxies": ["127.0.0.1", "::1"]
```

**⚠️ 這個修復不會馬上生效，因為同時發現gateway的config熱重載機制被卡住**：只要存檔就在log噴`config reload failed: StartupMaintenanceRequiredError: Legacy workspace setup state requires migration...run openclaw doctor --fix`。這個警報家族跟9/16那次45分鐘當機事故（案例73）同源，但這次版本本身沒有不一致（終端機跟正式服務都確認是同一個新版本），純粹是workspace setup state需要遷移。跑`openclaw doctor --fix`前備份`HEARTBEAT.md`/`TOOLS.md`/`agents/*/TOOLS.md`到`/tmp/`保險（這次`doctor --fix`把TOOLS.md合併進AGENTS.md並封存原檔，不是真的刪除，但備份多一層保障），跑完會自動`Restarted LaunchAgent`+驗證gateway健康，這次全程順利，兩個網址確認200。

**教訓**：
1. 看到`.bymyway.com`類網址回403且內容是JSON錯誤，先讀錯誤內容本身，不要預設是DNS/tunnel斷線——403代表請求真的到了gateway，只是被gateway自己的安全機制擋下，跟"連不上"是完全不同的故障模式。
2. gateway config熱重載卡住時，`openclaw doctor --fix`是官方認可的修復手段，不等於案例73那種「版本不一致貿然重啟」的高風險操作——差別在於：先確認`which openclaw`跟launchd實際執行版本是否一致（一致才能放心跑`doctor --fix`，不一致要先處理版本問題）。

Related: [[reference_curation_sop_2026-09-06]]、日誌位置`/tmp/openclaw/openclaw-<日期>.log`
