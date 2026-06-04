# Feature Requests

教練交辦但尚未做到的能力請求。每次有「我想要 X 能做到」的需求就寫這裡。

**提升路徑**：FEATURE_REQUESTS.md → distill/future-capabilities.md → 排入任務清單

---

## [FEAT-20260605-001] 主動學習機制（已被 LRN-20260605-002 涵蓋）

**Logged**: 2026-06-05T04:25:00+08:00
**Priority**: high
**Status**: resolved
**Complexity**: simple

### 請求
- 教練 #7521：「主動學習，請執行」
- 想要：我每次任務結束自動觸發 self-improving-agent，把學習寫進 `.learnings/`

### 解法
- 已落實 LRN-20260605-002 的「硬規則」
- 每次任務結束自我檢查 → 有就寫、沒有就標記
- 配套：capability-evolver 等 `.learnings/` 有料後自動產出 mutation 建議

### Resolution
- Resolved: 2026-06-05T04:30:00+08:00
- Notes: 已建立本檔 + 新增 3 條 LEARNINGS + 1 條 ERRORS

---

（之後教練新的功能請求請加在這下面）
