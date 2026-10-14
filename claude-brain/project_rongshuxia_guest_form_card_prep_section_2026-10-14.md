---
name: project-rongshuxia-guest-form-card-prep-section-2026-10-14
description: 榮樹下來賓資料表＋AI來賓卡＋樹蔭席承諾牆＋「訪談嘉賓前置作業」公開區怎麼運作、公開範圍、維護指令（教練10/14構想）
metadata:
  type: project
---

2026-10-14 教練讀完吳董 ChatGPT 的分工建議後定案：大樹只做主訪＋舞台＋系統，剪輯發稿交邱裕榮，每週四場（預約頁固定時段先按下）。藍圖在 `knowledges/榮樹下_營運藍圖與公益轉身席_2026-10-14.md`。接 [[project-rongshuxia-group-interview-scheduler-2026-10-12]]。

**運作**：LINE 榮樹下群組登記訪談對象（set-guest）→ 回覆附 `/rongtree/guest/<代碼>` → 來賓填 → MiniMax 做來賓卡（`event-signup/rongtree_guest.py`，金鑰 `state/minimax_api_key` 不進 git）→ 巴哈群組通知簽章網址，**同時也發教練私人電報**（10/14 傍晚教練說「平常找不到路徑」，`start_card(coach_notify=)`；公開「已交資料」頁只放姓名職稱照片一句話，完整資料只在簽章來賓卡）。榮樹下網頁最下方 `#prep`「訪談嘉賓前置作業」讀 `/api/rongtree/prep`，列出接下來訪談與已交資料來賓。`coach_schedule.py ensure-forms` 幫每場配網址。樹蔭席承諾牆：`scripts/rongtree_pledge.py add／done／list`。後台短網址 `/rongtree/a/<12字>` 已收進大樹作品集。

**Why**：教練工作量太大；要讓誰交了資料公開一目了然，但來賓個資要保護。
**How to apply**：公開只給姓名、職稱、照片、一句話介紹；電話、不談話題、AI 訪綱與提醒只在簽章來賓卡。給吳董與裕榮的回覆信**只存草稿、跳網頁給教練看，教練自己傳，AI 不代寄**。公益企業家俱樂部（tava-ai.com/chat/dn3wyx5ini/）是同一計畫的行銷工具，之後收進 event.bymyway.com。
