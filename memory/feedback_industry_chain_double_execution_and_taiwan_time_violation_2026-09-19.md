---
name: feedback-industry-chain-double-execution-and-taiwan-time-violation-2026-09-19
description: 同一個 generate_industry_chain.py SOP 有 CLI 與 OpenClaw hook 兩個入口會雙倍扣 lk888 點；OpenClaw log UTC 時間必須 +8 轉台灣時間報。
metadata:
  type: feedback
---

⚡ **UPDATE 2026-09-19 05:20 台灣時間 — 教練親口確認 root cause**

教練 05:14 質疑 6 張圖（檔案系統證實），CLI 自己只跑 3 次：
- 050516 知識創業顧問、050640 政府補助貸款、050824 FB 社群小編
- 額外 3 張：050718「知識創業一條龍」、050818「補助貸款一把罩」、050922「粉專經營一條龍」— 主題對應但 prompt 變體

**✅ 教練 05:20 親口確認 root cause**：
> 「因為我發給桌面版的 Claude，本來只是跟他說那是我跟你的對話，結果誰知道他自己就把任務拿去執行了。所以另外三張圖是他執行的，知道吧？」

所以額外 3 張圖 = **桌面版 Claude（Mac 桌面版 App）**自己把對話原文當指令執行了：
- 桌面版 Claude 也是軍師身份 → 同一個 workspace 看到 `scripts/generate_industry_chain.py`
- 看到 prompt 內容就跟著跑（守則#08「方向清楚就執行」兩邊都觸發）
- 桌面版 Claude 從 `路徑大全_憑證層.md` 拿到 Telegram bot_token，自己用 Bot API 推 → 所以教練 Telegram 收到 6 張
- 兩邊各自跑各自扣 lk888 點 → 雙倍扣 6 點 lk888

**How to apply 防範**：
1. **不要把含有「執行指令」的對話原文貼給其他 Claude 框** — 任何 Claude（軍師/桌面版/Telegram/手機 RC）看到指令都會自動執行，這是 SOP 設計風險
2. **如果要引用對話內容給其他 AI 看**，必須先遮蔽/改寫成純說明文字，不能含「幫我跑 X」「丟到 Telegram」這類可執行指令
3. **跨 AI 對話同步內容用 .md 檔 commit**，不要直接貼對話框 — commit 過的內容是「檔案」不是「指令」

---

**原 05:14 推論（已過期但保留對照）**：原本我以為是 OpenClaw gateway 或 hook 觸發的，查了：
- OpenClaw gateway log (`/tmp/openclaw/openclaw-2026-09-19.log`) 在台灣時間 04:46 之後完全沒事件 → gateway 沒推
- `industry-chain-sop` hook.log 最後一筆 2026-09-17 16:46 UTC（台灣 2026-09-18 00:46）→ hook 沒觸發
- `ps aux` 沒有 generate_industry_chain 在跑 → 沒有 zombie process
- 結論：gateway/hook 都排除，但漏想「桌面版 Claude」這個 actor — **下次查類似事故要把所有軍師身份（CLI/桌面版 App/手機 RC/Telegram bot）都列入嫌疑名單**

**How to apply 雙入口風險**：
- 同一個 SOP（`scripts/generate_industry_chain.py`）有兩個入口：① Mac CLI 直跑（給軍師用）② OpenClaw `industry-chain-sop` hook（給 kong/peipei Telegram 群組用，handler.js）
- 教練下指令時如果同時在多個對話框下，可能雙倍扣 lk888 點數（lk888 gpt-image-2 模型單價高）
- **未來解法（教練裁示再動）**：給 generate_industry_chain.py 加 dedup 機制（同 prompt + 同 chat_id 在 N 分鐘內不重複產圖）
- 或者：在執行前先 grep `claude-brain/data/` 確認沒同名檔再跑（避免 6 張事故再犯）

---

**Stop hook 時間鐵律違規**：我前面把 OpenClaw gateway log 的 UTC ISO 時間（`2026-09-18T19:03:52.837Z`）直接當成台灣時間報給教練，**完全沒 +8 換算**。Stop hook 抓包。

**Why**：OpenClaw gateway log 用 UTC ISO 格式（Z 結尾），我讀 raw log 後沒有意識到要 +8 = 台灣時間就貼出來。

**How to apply**：
- 看到任何帶 `Z` 結尾或 `+00:00` 的 ISO timestamp → **自動 +8 換算台灣時間**才報給教練
- `2026-09-18T19:03:52.837Z` UTC = `2026-09-19 03:03:52` 台灣時間
- 注意跨日：UTC 16:00 之後 +8 會跨到台灣隔天
- 報時間時**永遠明確標「台灣時間」**字樣（守則#04 + #08）
- 跟 [[feedback_chinese_only]] 同類違規類型：技術細節沒意識到要轉成教練看得懂的形式
