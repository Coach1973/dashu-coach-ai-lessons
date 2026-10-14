---
name: reference-silent-failures-found-in-weekly-audit-2026-10-14
description: 10/14 一週盤點抓到的「默默壞掉」類型與查法：接力棒鏡像防呆擋掉正常棒兩週、MEMORY.md 超 2 萬字被截、點名例外靠錯誤字樣失效、展示版表單收不到；怎麼查、已改成點名出聲
metadata:
  node_type: memory
  type: reference
  originSessionId: a4cae501-0a37-4400-8ff5-f8796bc819ff
  modified: 2026-10-14T01:48:01.771Z
---

10/14 盤點的教訓：最傷的不是會報錯的 bug，是「失敗了沒人聽到」。

- **接力棒鏡像**（workspace/CLAUDE.md）：`sync_handoff_to_claudemd.sh` 防呆要求「新的一棒 vN」，10/01 起標題改用時間 → 每 5 分鐘被擋、失敗 3,257 次、停兩週。查法：`/tmp/openclaw_cron_daemon.log` 的 ⚠️、`/tmp/sync_handoff.log`。已修（`be1f93108`），每日點名有「接力棒鏡像」項（>26 小時亮黃燈）。
- **小龍蝦開機檔字數**：小龍蝦日誌 `bootstrap file MEMORY.md is N chars (limit 20000); truncating` → 尾段讀不到。查法：`grep "bootstrap file" /tmp/openclaw/openclaw-*.log`。SOUL.md 已 19,353 字，下一個會爆。
- **點名例外用錯誤字樣判斷**會隨上游改版失效（Exec blocked → Ls failed）；例外要用穩定的識別（分身名稱）。
- **表單收不到**：`python3 scripts/module_kit.py audit` 應為 0（見 [[project_module_kit_new_project_menu_2026-10-14]]）。
- 活動網站 5xx：`event-signup/webapp.error.log` 的 werkzeug 日期格式是 `[14/Oct/2026 ...]`，用 `\[(0[7-9]|1[0-4])/Oct/2026` 找，別用 ISO 日期 grep（會漏）。

**How to apply:** 新增任何自動化，要問「它失敗時誰會聽到？」——接進 `scripts/daily_team_rollcall.py` 的檢查，不要只寫 log。
