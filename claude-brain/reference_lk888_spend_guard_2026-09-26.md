---
name: reference-lk888-spend-guard-2026-09-26
description: LK888出圖一律走scripts/lk888_guard.py收費閘門（重複免費回傳/重畫限速/每小時煞車），兩端都有繞過鎖；測付費API必須先封網，Homebrew Python的sitecustomize會被同名檔蓋掉
metadata:
  node_type: memory
  type: reference
  originSessionId: b5333cd5-14c9-4b0c-89c7-506d62e34a17
  modified: 2026-09-26T07:42:23.687Z
---

**機制（試金石案例85，2026-09-26）**：小龍蝦一句話重跑21次，28張出成96張燒光教練LK888額度。
- 閘門：`workspace/scripts/lk888_guard.py`，腳本把打LK888的 `urllib.request.urlopen` 換成 `lk888_guard.urlopen`。同樣請求24h只付一次；`LK888_REDO=1` 才准重畫（同張5分鐘內不准連續、一天3次）；一小時40次煞車+Telegram通知教練。帳本 `state/lk888_ledger.jsonl`，查帳 `python3 scripts/lk888_guard.py report`。
- 小龍蝦端：`~/.openclaw/extensions/safety-locks/index.js`（before_tool_call，改完要 `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`，重啟前照[[check-openclaw-version-before-gateway-restart]]比版本）。同檔另有「紀錄檔覆寫鎖」：工作區>10KB的.md被write縮到一半以下就擋。
- 軍師端：`workspace/scripts/lk888_bypass_guard.sh`（PreToolUse Bash）。
- 多組金鑰（09-26教練開第二帳戶）：憑證層lk888段落「API Key：sk-」依序＝1號線(新帳戶，主要)、2號線(原帳戶，備援)。所有腳本先用第一行；閘門遇401/402/403/429且訊息含額度/餘額/quota字樣，同一張自動換下一條線，不重跑。LK888查不到餘額API(billing端點404)，餘額只能看控制台。只讀查詢寫成腳本走`lk888_guard.urlopen`的GET，直接curl會被軍師端收費鎖擋。

**How to apply**：
- 自己寫新的出圖腳本一定 import lk888_guard，不然兩端都會擋。
- 測任何會花錢的API：先在連線層封死網路（monkeypatch socket.connect）並自我檢查才跑目標腳本。不要用自製 `sitecustomize.py`——會蓋掉Homebrew Python自己的同名檔，Pillow等套件路徑消失、mock裝不上卻照樣放行（本案因此真的燒了1張）。
- 小龍蝦（MiniMax）的自我檢討與「已執行」回報不可直接採信，查 `~/.openclaw/agents/main/agent/openclaw-agent.sqlite` 的 `transcript_events`。
