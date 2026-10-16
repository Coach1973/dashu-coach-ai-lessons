---
name: project_skills_catalog_2026-10-16
description: 🧰 技能清單（10/16 教練要「常做的事寫成技能，說一句就好」）：Claude 7 個＋小龍蝦 2 個新技能的口令、位置、怎麼加新技能、怎麼驗證有載入
metadata:
  type: project
---

2026-10-16 教練（朋友建議）要求：經常重複的工作寫成技能，下次說「走某個技能」就不用重交代；Claude 與小龍蝦兩邊都要。依 3,003 則 Claude 交辦＋385 則小龍蝦交辦盤點後建立。

**Claude（Mac）**：檔案在 `workspace/claude-code-skills/<名>/SKILL.md`，連到 `~/.claude/skills/<名>`，副本 `cloud_sync/skills/<名>/`（雲端用）。
- 「健康檢查」system-health-check → `scripts/system_health_check.py`（只讀，⚠️ 要先驗證再講，程式本身會誤報）
- 「總結」junshi-shutdown-summary；「改網頁」bigtree-web-edit；「上架」bigtree-publish-site；「加上報名」bigtree-event-signup；「開過票沒」bni-training-invoice；「原話報告書」coach-verbatim-report
- 驗證：新開 `claude -p` 問口令對應哪個技能（10/16 實測 7 個都看得到）。

**小龍蝦**：真正讀的位置 `~/.openclaw/agents/<分身>/agent/workshop-skills/<名>/SKILL.md`（不進 git），備份 `workspace/ops/xiaolongxia_workshop_skills/`。main 新增 site-down-check（網站打不開／健康檢查）、bigtree-publish-site（上架，先分誰的網站）；原有出圖 5 個＋bni_tainan 產業鏈圖 1 個＋kong 派工 1 個。驗證：`openclaw skills list --agent <分身> --json` 看 source=openclaw-workshop、ready；再用 `openclaw agent --agent main --session-id <測試> -m ...`（不加 --deliver 不會發訊息）問一次。

**Why:** 教練是電腦小白、每天語音交代大量重複流程，「沒腦子再去一一點出有哪些事」。
**How to apply:** 新的重複工作出現第 3 次就寫成技能；技能裡引用的路徑先確認存在（不憑印象）；改小龍蝦技能後用新對話測。相關：[[feedback_hooks_must_fail_open_never_block_coach_2026-10-16]]
