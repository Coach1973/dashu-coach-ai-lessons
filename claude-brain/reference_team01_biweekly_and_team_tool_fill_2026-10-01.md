---
name: reference-team01-biweekly-and-team-tool-fill-2026-10-01
description: 第一分會戰情表改雙週(8/9~11/11)＋team_tool新增填121/填咖啡/填來賓，怡靜群可口頭更正數字
metadata:
  type: reference
---

team01(第一分會) weeks 表：8/9、8/19、9/2、9/16、9/30、10/14、10/28、11/11 為雙週開會日，11/18 起每週三到12/30(8/9是星期天，教練裁示照寫)。weeks表在 `~/github_repos/team01-guests/team01_guests.db`(不進git，改前先備份)。

`workspace/scripts/team_tool.py`：`填121 <姓名> <週> <次數>`、`填咖啡 …`、`填來賓 …`(來賓網站不開放會員填，工具直接寫DB；重填新數字=更正)。週可寫 9/16、第四週。第一分會限定。

**How to apply**：怡靜群說「X 9/16 做了 2 次一對一」→ 執行對應指令；若怡靜回「沒有此功能」是 session 還記舊規則，封存 session 重來。

**未來週次不開放填寫**（10-03）：`db.list_occurred_active_weeks` 只給日期<=今天的週，未到的週格子沒有四項指標，只顯示「尚未到」；教練問「第十週按了沒出現」＝第十週是 11/25。若怡靜要提前填，要改 `compute_member_stats`／模板的 `entry` 判斷（教練說要再改）。
