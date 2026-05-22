---
name: 白話文鐵律——教練是電腦小白
description: 跟教練講話禁用工程術語、檔名、cron/git/relay 等行話，先翻成日常人話
type: feedback
originSessionId: e036e714-6919-49b9-8691-6afa49800e13
---
教練是電腦小白，講話用「日常人話」，不用工程術語、不講 cron/git/relay/repo/commit 這類字、不引用檔名（如 MAC_MIGRATION_PLAN.md）當名詞。CORE_RULES R02 早寫了，是我反覆違反。

**Why:** 2026-05-16 04:50 我給教練一段「5/13 主線那條『修 cron 路徑 + 你 claude /login』這 3 天沒人做」「MAC_MIGRATION_PLAN 已經消滅 relay cron 的核心用途」「整個指揮所考古結案」——教練直接回「你在講什麼，我聽不懂」。我把報告寫得像給工程同事看，忘了報告對象是教練。「全中文」（feedback_chinese_only）只是表象，真正鐵律是「**白話文**」——所有技術概念要轉成生活譬喻或具體動作描述。

**How to apply:**
- 講「git commit」→ 改說「存個版本」「留個記號」
- 講「cron job」→ 改說「定時任務」或「自動排程」
- 講「relay 系統」→ 改說「傳訊小工具」「轉信機制」
- 講「repo / workspace」→ 改說「資料夾」
- 引用內部檔名（OPUS_HANDOFF_20260513.md）→ 改說「5/13 那份交接文件」
- 講「MAC_MIGRATION_PLAN 消滅了這步」→ 改說「軍師搬到 Mac 之後，這件事就用不到了」
- 寫每一段給教練看的字，先自問：「我媽看得懂嗎？」看不懂就重寫
- 不確定要不要解釋的詞，**一律解釋**——成本低，誤會成本高
