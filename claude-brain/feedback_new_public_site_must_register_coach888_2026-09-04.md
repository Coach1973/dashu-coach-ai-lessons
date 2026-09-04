---
name: feedback-new-public-site-must-register-coach888
description: 每個新建的公開網站(gh repo create --public)一律要收錄進coach888作品一覽，已做成deterministic Stop hook強制檢查
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 89e4937c-c840-4c0c-bc46-68785a6d6bbf
  modified: 2026-09-04T14:42:33.527Z
---

每次用`gh repo create <repo> --public`建立新的對外網站repo，收工前一定要把它加進`~/github_repos/coach888/index.html`作品一覽（通常放「大樹常用」分類第一項，依既有`feedback_coach888_new_items_go_first`SOP），不能等教練發現「怎麼看不到」才補。

**Why**：2026-09-04同一天內連續發生兩次同款疏漏——v179「7新站+1後台工具全漏」查證後補齊，v181新建`tainan-shangquan`站又漏放，教練當場糾正「請寫入SOP...不要再讓我提醒」。純文字SOP靠AI自己記得會再忘第三次（呼應更早的教訓「防呆鎖必須是hook不能opt-in」——文件寫得再清楚，AI在忙著做正事時還是會漏看）。

**How to apply**：已做成`scripts/stop_rules_master.py`規則L（deterministic check，非自稱）——只要這輪對話執行過`gh repo create ... --public`，Stop hook就會掃描該repo名稱是否出現在本機`coach888/index.html`裡，沒有就擋下收工（exit 2），逼自己補完才能結束對話。這條鎖只認`--public`，用`--private`建的備份/工具型repo（如`true-ai-team`）不會被誤攔。已用合成transcript測試正反兩案例（缺收錄→擋下；已收錄/私有repo→放行）驗證邏輯正確。

真正給教練看的網站永遠用`--public`建repo，這樣才會被這條鎖保護到；如果之後有其他不經過`gh repo create --public`就上線的管道（例如純掛在event-signup底下的repo-served路由，沒有另外建GitHub repo），這條鎖看不到，仍要靠人工記得補coach888。

相關：[[feedback_coach888_new_items_go_first]]
