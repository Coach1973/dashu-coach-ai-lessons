---
name: feedback-opus-token-economy
description: Opus 軍師模式下，兼顧品質的前提下永遠要考慮怎麼節省 token 完成任務。教練親定 2026-05-29
metadata: 
  node_type: memory
  type: feedback
  originSessionId: caaed8f5-91fa-46aa-a8d5-29b6517b52cc
---

# Opus 軍師模式：兼顧品質下永遠省 token

## 規則

在 Opus 模式下，軍師執行任何任務時，**先想「能不能更省 token」**，再動手。

順序是：① 品質達標（不能降）② 省 token（永遠想） ③ 速度快（順便）。

## Why

教練的「不限流量」只屬於小龍蝦/MiniMax（無限），**Opus 軍師走的是教練的 Claude 額度**——5 小時內用完要等 3 小時才回滿。

教練每給軍師一個任務，本質上是在用「教練的生命額度」。軍師若揮霍 token，等同於：
- 教練此刻的工作被切斷
- 或者要重啟視窗、補context、重建脈絡
- 都是雙倍燒生命

這跟 [[feedback-scarce-resource-workflow]]「稀缺資源用在思考、執行外包」同源——但這條更進一步：**Opus 軍師自己做事時也要省，不只是分工層面省。**

## How to apply（軍師省 token 標準技巧清單）

### 一、分工層面（最高優先）
- **判斷類**（複審、品管、撈真實對話、視覺品質判斷）→ Opus 親手，不可外包
- **執行類**（寫腳本、改檔、重生 HTML、跑測試）→ 派 MiniMax / 終端機 Haiku
- 派外包用 [[feedback-subagent-instruction-no-questions]] 標準格式，禁問鐵律

### 二、讀檔層面（高頻省 token）
- **Edit 優先於 Write**——9 段改動用 9 個 Edit 比重寫整檔省 80% output token
- **Python/awk/grep 精準萃取，不要 cat 全檔**——21 條故事檔 31KB 全讀 vs 萃取三段 16KB，差一半
- **不要 Read 已在 context 的檔**——一旦 Write/Edit 過，內容已在 context，重 Read 浪費
- **過濾 jsonl 用 Python script，輸出含時間戳+前 400 字**——不要整段 dump

### 三、驗收層面（容易忽略）
- **現場活證據優先於另派驗收**——hook 已在這場 session 觸發，就不必派學長重跑
- **抽查 1-2 個樣本而非全跑**——驗收 21 條時跑 3 條代表性即可

### 四、互動層面
- **一次性指令完整給出**，不要分段問教練「OK 嗎」「下一步嗎」
- **方向清楚就直接執行**（守則#08 + E06）——不問「要不要做」
- **必問三情境例外**（[[feedback-subagent-instruction-no-questions]]）：方向不確定、不可逆、重大決策

### 五、回報層面
- **表格化勝過長段落**——同樣資訊，table 比 prose 省 30% token
- **不要重複報告已給過的 commit hash**——一次給清，後續引用
- **驗收完直接給結論**（✅/⚠️），不要重複「結論：通過」+「我覺得通過」

## 實戰範本（2026-05-29 下午場軍師親跑）

| 任務 | 普通做法 | 軍師省 token 做法 | 節省 |
|------|---------|----------------|------|
| 撈 5 條 C 類真實對話 | 每條派 Explore agent | Python 一次過濾 83 jsonl | 約 60% |
| 21 條故事檔總覽 HTML | Read 21 檔 + Write | Python 萃取三段 + Write 一次 | 約 50% |
| 9 段 HTML 改錯字 | Write 重寫整檔 | 9 個 Edit 精準改 | 約 70% |
| hook 階段 3 驗收 | 派學長 git pull + 跑測試 | 現場活證據（hook 就在這場觸發） | 約 90% |

**總結：本場下午場原預估 50-60K token，實際約 30-40K，省了三分之一。**

## 紅線（不可為了省 token 犧牲的事）

- ❌ 引用守則一字不差（#21）——不能因為省 token 就「大概意思對」
- ❌ 教練原話查證（#15）——不能因為省 token 就用記憶硬編
- ❌ 視覺交付物親自看過（#03）——不能因為省 token 就跳過驗收
- ❌ 完美交接接力棒（#06）——不能因為省 token 就敷衍接力棒
- ❌ 教練的話神聖收錄（[[feedback-coach-words-are-sacred]]）——不能因為省 token 就漏記
