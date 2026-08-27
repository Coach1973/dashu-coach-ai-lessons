---
name: 三臺終端機並行蒸餾「教練全局理解」計畫
description: Mac/Hermes/聯想三臺終端機分工蒸餾不同層次的教練檔案，最後在 Mac 主控做整合產出「教練全局理解總綱」
type: project
originSessionId: 0d047e5b-f32f-438b-bf9b-ee1440e905b1
---
## 任務目的
動員三臺裝有 Opus 4.7 的終端機並行讀取教練散佈在 Mac/VPS/Windows 同步資料夾的關鍵檔案，蒸餾出對「教練究竟要做什麼」的深度理解，最後由 Mac 主控整合成總綱。

**Why:** 教練的使命、哲學、運作記憶散佈在數十個 .md 檔，單一 session 一次讀完成本太高；三機並行可同時涵蓋「靈魂層」「現況層」「心法層」，再整合。

**How to apply:** 收到「三邊都跑完了」「蒸餾報告好了」「整合一下」這類訊號時，立刻啟動最後一步整合。

## 三機分工

| 終端機 | 負責層次 | 輸出檔/方式 |
|--------|----------|-------------|
| Mac 終端機 | 靈魂、身份、使命 | `/Users/bymyway/Documents/distill_mac_soul.md` |
| Hermes 終端機 | 現況、運作記憶、VPS | `/Users/bymyway/Documents/distill_hermes_state.md` |
| 聯想終端機 | 心法、哲學、方法論 | 文字回貼（聯想不能寫到 Mac）|

## Mac 終端機讀的檔案（靈魂層）
- /Users/bymyway/.claude/CLAUDE.md
- /Users/bymyway/.openclaw/workspace/SOUL.md
- /Users/bymyway/.openclaw/workspace/AGENTS.md
- /Users/bymyway/.openclaw/workspace/CLAUDE.md
- /Users/bymyway/Documents/mac-openclaw-workflows/SOUL.md
- /Users/bymyway/Documents/mac-openclaw-workflows/IDENTITY.md
- /Users/bymyway/Documents/mac-openclaw-workflows/USER.md
- /Users/bymyway/Documents/mac-openclaw-workflows/GRAND_MISSION.md
- /Users/bymyway/Documents/mac-openclaw-workflows/user_grand_mission.md
- /Users/bymyway/.openclaw/agents/kong/SOUL.md
- /Users/bymyway/.openclaw/agents/peipei/SOUL.md

五個蒸餾問題：教練是誰 / 頂級助教長相 / 四助教分工 / 不可違背的鐵律 / 終端機助教成功標準

## Hermes 終端機讀的檔案（現況層）
本機：
- /Users/bymyway/.openclaw/workspace/MEMORY.md
- /Users/bymyway/.openclaw/workspace/shared-context/BOT_MESSAGES.md（最後 300 行）
- /Users/bymyway/.openclaw-kong/workspace/MEMORY.md
- /Users/bymyway/.openclaw-peipei/workspace/MEMORY.md
- /Users/bymyway/.hermes/memories/MEMORY.md
- /Users/bymyway/.hermes/SOUL.md
- /Users/bymyway/.hermes/hermes-agent/AGENTS.md
- /Users/bymyway/Documents/mac-openclaw-workflows/MEMORY.md

VPS（SSH 進去讀）：
- /root/openclaw/data/workspace/SOUL.md
- /root/openclaw/data/workspace/VPS_CORE_RULES.md
- /root/openclaw/data/workspace/VPS_WORK_RULES.md
- /root/openclaw/data/workspace/CLIENT_PROFILE.md
- /root/openclaw/data/workspace/.memsearch/memory/2026-05-{05,06,07}.md

五個問題：Mac 版 vs VPS 版差異 / 近兩週主推專案 / 四機健康狀態 / Hermes 角色 / 3–7 天待辦

## 聯想終端機讀的檔案（心法層）
從同步資料夾 mac-openclaw-workflows 讀：
- sea_biscuit_club.md
- project_haibinggan_philosophy.md
- project_top_assistant_blueprint.md
- project_anti_amnesia_architecture.md
- project_key_decisions.md
- feedback_coach_golden_rules.md
- feedback_working_rules.md
- feedback_top_assistant_ux_standard.md
- feedback_ai_transparency_rule.md
- MASTER_PROMPT_TEMPLATE.md
- HEARTBEAT.md
- project_auto_api_key_blueprint.md

五個問題：海餅乾哲學 / 三大信念落地 / 動嘴執行的實現路徑 / 抗失憶架構 / 好助教 vs 爛助教標準

## 最後整合（Mac 主控執行）

三邊跑完後，把以下三份輸入丟到 Mac 主控這邊：
1. `/Users/bymyway/Documents/distill_mac_soul.md`（Mac 終端機產出）
2. `/Users/bymyway/Documents/distill_hermes_state.md`（Hermes 終端機產出）
3. 聯想電腦文字回貼（用戶貼到對話）

Mac 主控做最後一輪整合，產出：**「教練全局理解總綱」**

整合輸出建議存到：`/Users/bymyway/Documents/教練全局理解總綱.md`

總綱結構建議：
1. 教練是誰（一頁畫像）
2. 終極使命與三大信念（落地版）
3. 系統架構（四助教 + Hermes + VPS）
4. 目前運作現況（近兩週重點）
5. 鐵律與雷區（不可違背清單）
6. 3–30 天路線圖

## 何時觸發整合
教練說以下任何一句，立刻把三份蒸餾合併產出總綱：
- 「三邊都跑完了」「蒸餾報告好了」「整合一下」
- 直接把三份內容貼進來
- 「產出總綱」「給我全局理解」

## 寫指令給三臺終端機時必加段落（15 分鐘最高指導原則）
每一份指令尾巴**必須**加上這段，不能漏：

```
⚠️ 最高指導原則：每讀完 3–5 個檔案（約 15 分鐘）就把當下進度 append 寫到輸出檔一次，
不要等到全部跑完才一次性寫。這樣萬一當機或斷線，最多只損失 15 分鐘的進度。
請不斷提醒自己這條原則。
```
