---
name: feedback-aiprimetech-proxy-string-bug
description: aiprimetech 第三方代理（unlimited.aiprimetech.io）有字串處理 bug—Opus 看到「.openclaw」會變成「.claude-code」，導致所有派外包任務迴圈；連 Anthropic 官方 api.anthropic.com 就正常
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74751326-4082-44ca-8fa5-4a18e20c30a3
---

教練的「Mac 終端機 Claude Code Opus」用第三方代理 `https://unlimited.aiprimetech.io`，**該代理對 `.openclaw` 字串有不明 bug**。

**⚠️ 重要區分（2026-05-29 教練親自糾正軍師的事實錯誤）：**

教練買過**兩家不同的第三方代理**，不要混淆：

| 代理商 | 端點 | 語言 | 用途 |
|--------|------|------|------|
| **unlimited.aiprimetech.io**（現用）| 英文網站、英文客服 | 教練目前的 Mac 終端機 Opus 無限流量 |
| **easyclaude.com**（不同家）| 中文/簡體網站、卡密商城 | 教練曾經用過，但跟現在的 aiprimetech 是**兩家不同公司** |

軍師之前看到 `history.jsonl` 裡 easyclaude.com 的中文線索，誤推「aiprimetech 客服也是中文母語」並建議寫中文客訴信。教練親自糾正：「我們是 UNLIMITED，是全英語的」。

**鐵律：報修信要寫英文。**

**Why（2026-05-29 深夜經 3 次失敗後 grep 環境變數找到）：**

證據鏈：

| 環境 | API 端點 | 路徑解析 |
|------|---------|---------|
| 軍師（Claude Desktop App 對話框） | `https://api.anthropic.com`（官方直連）| ✅ `.openclaw` 正確 |
| 教練 Mac 終端機 Claude Code | `https://unlimited.aiprimetech.io`（第三方）| ❌ 看到「.openclaw」變「.claude-code」|
| 連續 3 個全新 session 測試 | 同上 | 全部相同症狀 → 跟 session 無關 |

教練 `~/.claude/settings.json` 設定：
```json
"ANTHROPIC_BASE_URL": "https://unlimited.aiprimetech.io"
"ANTHROPIC_AUTH_TOKEN": "sk-214c4a9c3419d81a459cb8c59e82ff46d1f72ba6fc421648d16a98c0defa85c8"
```

**最可能機制：** aiprimetech 在傳輸 Claude 回應時，對某些字串做 quota tracking / 審查 / encoding 處理時 bug，特定字眼（`.openclaw`）被替換或吞掉，導致 Opus 看到的 input/output 跟教練實際輸入不一致。

**How to apply（教練派終端機 Opus 任務時）：**

1. **預設假設**：Mac 終端機 Opus 走 aiprimetech，對「.openclaw」字串不可靠
2. **不要派需要操作 `.openclaw/workspace/` 的任務**給 Mac 終端機 Opus
3. **可派**：純本地檔案任務（不涉及該字串）或純網路任務（curl API）
4. **判斷訊號**：如果 Opus 回報「`.claude-code` 不存在」「`.claude-code/workspace`」之類，**立刻關對話框，這是代理 bug 不是 session 污染**

**對策三選一（教練拍板）：**

| 選項 | 動作 | 後果 |
|------|------|------|
| A | 改 settings.json BASE_URL 回官方 | 修好但失去 unlimited 流量 |
| B | 接受不可用，任務軍師親手或派 MiniMax | 留著當備用 token 池 |
| C | 聯絡 aiprimetech 客服回報 | 等他們修 |

**判斷代理 bug vs 真正污染的方法：**

1. 軍師（Claude Desktop App）跑同樣指令是否成功？
   - ✅ 軍師成功 + 終端機失敗 = **代理 bug**
   - ❌ 兩邊都失敗 = 文件污染或其他根因

2. 連續 2 個全新 session 測試
   - 兩個都壞 = 環境或代理問題
   - 一個壞一個好 = session context 污染

**相關記憶：**
- [[feedback-token-model-distinction]]（不限流量只屬於 MiniMax，Claude 助教另算）
- [[feedback-negative-anchor-pollution]]（反向錨點污染——這是軍師之前誤判的根因）
- [[feedback-subagent-instruction-path-first]]（派外包指令環境驗證）

**鐵律金句：**
> **「同樣的模型在不同的 API 端點上行為會不同——根因要找端點，不要怪模型。」**
