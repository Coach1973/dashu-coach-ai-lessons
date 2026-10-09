---
name: feedback-generate-images-myself-via-lk888-guard
description: 教練要圖時我自己用 LK888 出，不要只給提示詞叫他去教別的 AI；Mac 上走 lk888_guard 在程式裡取金鑰，不需要環境變數
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4dc29b4f-38cd-4235-9850-b25ffb8dc8e3
  modified: 2026-10-09T20:41:55.628Z
---

教練 2026-10-10：「其實你自己就可以調用 LK888，我不用再去教別的 AI 做，不是嗎？」——我先前寫完網頁只給了三段「配圖提示詞」，等他拿去做，是多餘的搬運（守則 #12）。

**Why:** 這台 Mac 的 `~/.openclaw/workspace/scripts/lk888_guard.py` 本來就能出圖，金鑰在 `路徑大全_憑證層.md`，沒必要繞一圈。出圖前就能預見「頁面需要配圖」時，直接出。

**How to apply:**
- 腳本裡 `sys.path.insert(0, "<workspace>/scripts"); import lk888_guard`，金鑰用 `lk888_guard._all_keys()[0]`（只在程式裡用，不印出、不寫進任何檔案），請求用 `lk888_guard.urlopen(req, timeout=180)`（收費閘門：重複請求免費回傳、限速）。API：`POST https://api.lk888.ai/v1/images/generations`，`{"model":"gpt-image-2","prompt":…,"size":"1024x1024"}`，回 `b64_json` 或 `url`。
- 先看專案有沒有 `.image-style.md`（bni-chapters 有）；先出一張看過再出其餘；每張只出一次；看到圖才算交付。
- 1024x1024 出圖後，要 4:3／16:9 就在構圖時叫模型「主體放中間橫帶、上下留白」，再用 PIL 裁；它有時會自己畫出上下白邊，裁掉即可。
- 圖裡不要有文字（`No text, no letters…`），中文字另用網頁疊。
- 出完用 `python3 scripts/lk888_guard.py report --hours 1` 查帳。
- 相關：[[reference_lk888_spend_guard_2026-09-26]]、[[project_trust_game_2026-10-10_teams_ranks_cheers_invite]]
