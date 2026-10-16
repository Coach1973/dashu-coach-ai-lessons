# 小龍蝦（OpenClaw）各分身的技能備份

真正被小龍蝦讀的位置是 `~/.openclaw/agents/<分身>/agent/workshop-skills/<技能>/SKILL.md`（那個資料夾不進 git），這裡是備份＋改版紀錄。
改技能時兩邊一起改；確認有載入：`openclaw skills list --agent <分身> --json`（source 是 openclaw-workshop、狀態 ready）。

2026-10-16 新增（依教練近 31 天對小龍蝦的 385 則交辦盤點）：
- main / `site-down-check`：教練說網站打不開／無法顯示／系統正常嗎 → 實測網址＋跑 system_health_check.py＋白話回報，系統層問題寫信給 Mac 軍師。
- main / `bigtree-publish-site`：上架網站，先分「誰的網站」（教練作品＝creation、不進商圈）。
測試對話（不發訊息）兩題都答對技能名稱與 kind。
