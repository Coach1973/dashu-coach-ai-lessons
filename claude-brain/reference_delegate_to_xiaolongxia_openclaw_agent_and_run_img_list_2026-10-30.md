---
name: reference-delegate-to-xiaolongxia-openclaw-agent-and-run-img-list-2026-10-30
description: 出圖清單（教練的出圖指令表 JSON）預設我自己用 scripts/run_img_list.py 一行跑（LK888 出圖不佔我 token，看圖才佔）；要交辦小龍蝦才用 nvm 的 openclaw agent；coachwu 4 張 AI 示意圖案
metadata:
  type: reference
---

教練 10/30 03:36 說「你能自己交辦給小龍蝦就省得我去貼」。做法（實測通，101 秒 4 張圖）：
`/Users/bymyway/.nvm/versions/node/v24.21.0/bin/openclaw agent --agent main --session-id <新id> --message "<一行指令交辦>" --deliver --channel telegram --reply-to 6124913915 --reply-account bot_main --timeout 900 --json`
**要用 nvm 那份（2026.9.4），/opt/homebrew 那份是 2026.6.34 不是實際在跑的**（見 [[reference_peipei_dm_allowlist_dmscope_and_openclaw_nvm_copy_2026-10-26]]）。用新 session-id 不污染教練私訊對話；交辦內容寫成「執行這一行指令、不自己改、失敗不重試」，照 [[feedback_bot_instructions_must_block_old_path_and_measure_tokens_2026-10-25]]。

出圖清單（教練的 ai-go/biz-web-inject「出圖指令表」格式）：`scripts/run_img_list.py <清單.json> <輸出夾> [--dry-run]`，走 lk888_guard、概念類才做、已存在不重出、上限 12 張、完成用 notify_coach.sh 回報；輸出夾放 /tmp（workspace 的未追蹤檔會被 stash -u 收走，見 [[reference_workspace_stash_u_clobbers_background_outputs_2026-10-26]]）。

coachwu 頁（event.bymyway.com/curated/coachwu/）真正的 AI 示意圖只有「學經歷時間軸」4 個 SVG（143 張圖其餘全是真照片）；已換成 LK888 出的 4 張（倉庫 51c588a，圖說「AI 繪製示意插畫」，原始 PNG 在 ~/Pictures/coachwu_AI插畫_20261030/，清單在 workspace/reports/img_lists/）。

**教練 10/30 03:41 糾正（繞遠路）：** 「交給小龍蝦跑、跑完你再上」多繞一圈。小龍蝦只在「20～30 張工作量大」才有意義；我自己用 run_img_list.py 出圖，圖直接存硬碟、回到我對話的只有十幾行文字，**生成本身不佔我 token，佔的是我逐張「看圖」驗收**（大批量就拼成聯絡表看一張）。LK888 點數不論誰跑都一樣。

**Why:** 教練不當搬運工、也不要多繞一圈；**How to apply:** 教練在 Claude 對話框交辦出圖＝我自己跑 run_img_list.py（≤12 張一次）→逐張看（無文字、無真人臉）→換進網頁；只有教練明說交小龍蝦、或一次 20～30 張以上才交辦（用上面 openclaw agent 那條）。沒量過每張圖的精確 token 數。
