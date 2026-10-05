---
name: bni-tainan-db-first-and-rank-ladder
description: 大台南小幫手(bni_tainan LINE)必須「BNI 資訊資料庫優先、不上網頂替」；位階順序檔 knowledge/bni_rank_ladder.md 是教練口述；改人設後要封存舊對話並用新對話實測
metadata:
  type: reference
---

教練 2026-10-05 04:04～04:08 在 LINE 問小幫手「BNI 職務職稱從領導幹部往上、自助理大使開始到國家董事」，小幫手混了網路資料；教練糾正：「資料庫裡面的是官方，第一手來源；沒有特別指示上網，BNI 任何資訊以資料庫為優先」。

**修在源頭（外層 repo `4c8f02640`、`70e2536b1`）**：
- `agents/bni_tainan/SOUL.md` 最上層（小檔，不會被 2 萬字上限截斷；AGENTS.md 已 4.7 萬字超限）加規則：資料庫優先於網路，查不到就說「資料庫沒有」；問位階先讀 `knowledge/bni_rank_ladder.md`。
- 新檔 `agents/bni_tainan/knowledge/bni_rank_ladder.md`：教練口述順序（領導團隊→助理大使→大使→董顧[啟動董事／支持與增長董事]→區域董事），區域董事以上資料庫沒有（AGENTS.md 的 13 個董事職稱是字母順序不是階層），回答時說沒有、別自己排。
- 封存教練舊 LINE 對話 `openclaw sessions archive --agent bni_tainan "agent:bni_tainan:line:direct:u895a0ad8e49d75f8303dc3d067282dc0"`（可還原）；用 `openclaw agent --agent bni_tainan --session-id test-xxx --message "【系統測試】…"` 新對話實測，答對（測完封存測試 session）。

**Why:** 教練要小幫手以他提供的資料庫為準；位階資料庫原本沒有階層圖，所以才會去上網找。
**How to apply:** 小幫手再答錯 BNI 事實時，先查是不是資料庫缺資料（補進 `knowledge/`），再查 SOUL.md 規則；改完一定封存舊對話＋新對話實測，沒實測不說好了。相關：[[reference_agent_session_keeps_old_rules_archive_after_edit_2026-10-01]]、[[project_business_club_game_design_principles_2026-10-03]]。
