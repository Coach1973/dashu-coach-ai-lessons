---
name: feedback-coach-chinese-file-mapping
description: 教練中文詞彙與實際檔案路徑的對照表，聽到這些詞直接對應到正確檔案
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 216aaa42-ba45-4ef4-9218-6fa9b5ae428c
  modified: 2026-08-27T18:01:36.667Z
---

教練說中文詞，AI 必須直接對應到正確的英文檔案或目錄，不需要再問確認。

| 教練說的中文 | 對應的實際檔案/目錄 |
|------------|------------------|
| 路徑大全 | `/Users/bymyway/.openclaw/workspace/路徑大全.md`（功能上等同 INDEX） |
| 靈魂檔案 | `SOUL.md` |
| 記憶檔 | `memory/` 目錄（或 `memory/YYYY-MM-DD.md`） |
| 接力棒 | `JUNSHI_HANDOFF_LATEST.md` |
| 特助心法 | `特助心法.md` |
| 試金石 | `試金石/試金石_案例庫.md` |
| 心跳檔 | `HEARTBEAT.md` |
| 網頁推 | 啟動「網頁推 SOP」→ 見 [[feedback-web-push-sop]] |
| 香草／嘸蝦米 | 教練慣用輸入法 OpenVanilla／嘸蝦米，絕不可移除否則無法打中文 |
| Telegram 快取（Mac，教練傳照片） | `~/Library/Group Containers/`（Telegram Mac 的照片快取路徑） |

**Why:** 教練用中文說話，AI 要自動翻譯到技術檔名，不應讓教練說「我是說那個叫 XXX 的英文檔」——那就是逼教練當搬運工（守則 #12）。

**How to apply:** 聽到上方任何中文詞，直接操作對應檔案，不問「您說的是哪個檔」。有新詞不確定時才問，確認後立刻加進這張表。

[[feedback_voice_typo_shixing_shouze]] — 語音糾偏對映表，同類型記憶

**2026-10-04 語音誤聽（教練自己更正）**：「教練原畫組織報告書」＝**教練原話報告書**（form 同 game-1004 原話逐字報告書）；「大富作品總覽」＝**大樹作品總覽**（coach888，教練 10-04 23:44 親口：「語音輸入法錯誤，教練原話　大樹作品」）。「全世界最優秀團隊系列」是 coach888 伺服器狀態裡的自訂分類（key `custom1791122483432`），新作品放第一項。
**2026-10-04 23:51 教練確認的語音諧音**：「倭軍／倭郡健身房」＝**World Gym**；「網會」＝**網頁**；「Windows count／Windows Content」＝**context window**。

**2026-10-07 教練對照**：①「真貴分會」＝**真貴籌備會**（chapters.slug `real-wealth`，status forming；教練當場糾正「真貴籌備會」）②分會名單上的「吳大樹」＝**教練本人**，遊戲裡已是「大樹教練」#1，不要入第二個座位（`seed_game_players.py` 的 `NAME_ALIASES` 已處理）③「官網」＝**www.bymyway.com**；大樹小講網站＝bigtree-tw.netlify.app，不叫官網（試金石案例108）。
