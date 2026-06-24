---
name: feedback-subagent-instruction-path-first
description: 軍師派任何外包 AI（終端機/Hermes/MiniMax）跑任務前，指令第一句永遠是「cd 絕對路徑 + git pull + ls 三大檔案」，禁止假設 AI 知道路徑
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74751326-4082-44ca-8fa5-4a18e20c30a3
---

軍師派任何外包 AI（Mac/Windows 終端機、Hermes、MiniMax 等）跑任務時，指令**第一句永遠**是「環境驗證三件套」。

**Why:** 2026-05-29 教練派終端機 Opus 跑任務時三度踩雷：
1. **Windows 終端機 Opus**：被 Claude Code auto mode classifier 封網，連 git pull 都跑不了
2. **Mac 終端機 Opus（下了開工指令還是錯）**：去找 `~/.claude-code/workspace/`（不存在的目錄）
3. **教練親口確認**：「我有先打開 Opus 再下開工開工的指令」但它還是錯

根因（軍師深挖出來的）：
- 每個新 session 的外包 AI = **零 context**
- 開工 hook 只注入「接力棒+心法+memory」，**不教路徑**
- 接力棒寫「做了什麼+待辦」，沒寫 workspace 絕對路徑在哪
- AI 看到舊對話片段（可能有人打錯字）→ **直接記成事實**

**How to apply（鐵律三句不可省）:**

軍師派外包指令必含「三段式」，順序不可換：

### 第一段：環境驗證三件套（永遠是指令的第一句）

```bash
cd /Users/bymyway/.openclaw/workspace && git pull origin main
ls 路徑大全.md JUNSHI_HANDOFF_LATEST.md 特助心法.md
sed -n '1,90p' 路徑大全.md   # 先讀第〇節「絕對路徑速查」
```

- 三個都 `ls` 到 = ✅ 環境正確，繼續往下做
- 任何一個報「No such file」= ❌ 環境錯，**立刻停手回報軍師**，不要瞎找

### 第二段：必要 context 直接餵（禁止假設 AI 能找到）

- **Netlify Token / Site ID / API Key 直接寫在指令裡**（不要叫它「自己去找 token」）
- **路徑全部寫絕對路徑**（`/Users/bymyway/...`），禁止寫 `~/...` 或相對路徑
- **範本格式直接複製進指令**，不要叫它「自己找範本」
- 預先列已知的「禁止假設清單」（例：「禁止找 `.claude-code` 那是錯的」）

### 第三段：任務 SOP（步驟編號 + 每步明確憑證）

每步寫清楚：要跑什麼指令、產出什麼、commit 哪個檔。

---

## 標準範本（派外包時直接套用）

```
從現在開始進入「自跑模式」。鐵律：教練不催、自己跑完、不問問題。

【第一步：環境驗證（不過不准動手）】

cd /Users/bymyway/.openclaw/workspace && git pull origin main
ls 路徑大全.md JUNSHI_HANDOFF_LATEST.md 特助心法.md
sed -n '1,90p' 路徑大全.md

三個 ls 都過 = 環境正確，繼續第二步。
任何一個失敗 = 立刻停手回報「環境不對」，不要瞎找其他路徑。

【第二步：必要 context（已餵好，不要再找）】

- Netlify Token: nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838
- Site ID（正式）: 86406013-6cdf-4bec-90e3-cdc9655bf124
- 範本格式: 看路徑大全「## 九、《超限戰》」段
- 禁止假設的錯路徑: `.claude-code/` / `claude/workspace/`（都是錯的，正確是 `.openclaw/workspace/`）

【第三步：任務 SOP】

1. [具體步驟]
2. [具體步驟]
...

【自跑鐵律（教練親定）】
- 不要回「好的」「收到」「我來看看」，直接幹活
- 中途不問教練、不等指令、不分批報告
- 遇到判斷模糊 → 標🟡寫進報告，繼續下一步
- 全部跑完才停，停的時候給 commit hash + 完工時間
```

---

## 反例（過去 AI 踩雷的爛指令）

❌ 「請幫我修改超限戰網站的時刻表」（沒 cd、沒 token、沒範本）
❌ 「去看一下 memory 然後整理」（沒絕對路徑，AI 會找 `~/memory` 然後找不到）
❌ 「按之前的部署流程跑」（什麼流程？哪裡寫？）

✅ 上面標準範本——三段式齊全，AI 照表抄就會做對。

**相關記憶：**
- [[feedback-subagent-instruction-no-questions]]（派外包禁問）
- [[feedback-opus-token-economy]]（Opus 省 token 鐵律）
- [[feedback-model-choice-quality-first]]（品質優先，禁止 Haiku+Opus 混用）

**鐵律金句：**
> **「外包 AI 不是讀心術師——你不寫的它都當不存在。」**

---

## 🔴 補充鐵律：迴圈病防護（2026-05-29 晚間血淚）

派外包 AI 的指令**必須含「迴圈自停條款」**，否則它會在錯誤指令上耗到爆 token。

**範本（加進每個派外包指令的「自跑鐵律」段）：**
```
連續三次同樣的 Bash 錯誤 → 立刻停手回報軍師，不要再迴圈。
「重複跑同一個失敗指令超過 2 次」= 必須停止+回報「我陷入迴圈了，請軍師救援」。
```

**Why（迴圈病的真實案例）：**
- 2026-05-29 晚間 Mac 終端機 Opus 跑任務 1，被 `~/.claude-code/workspace/`（不存在的目錄）卡住
- 它甚至自己說「.claude-code 不存在，正確應該是 .claude-code」（同一個錯誤路徑說兩遍）
- 連跑 8 分鐘+反覆同樣的 Bash error 而不自停
- 教練暫停才止血

**🔴 進階病例（同晚二次發作）：**
- 教練第二次派 Opus，指令裡明確寫「禁止找 .claude-code」「正確是 .openclaw」
- Opus 仍然在「.openclaw」和「.claude-code」之間迴圈，**自我矛盾還能自圓其說**
- 它回報：「實際 workspace 在 .claude-code/workspace/，但 .claude-code/workspace/ 不存在」（兩個 .claude-code 字面上一樣！）
- 軍師同步在另一個對話框 `cd .openclaw` 完全正常 → 證明**不是介面 bug，是該 session 的 context 已徹底污染**

**判斷「session 已污染」的訊號（看到任一就立刻關對話框）：**
1. 同一個 Bash 指令連續報同樣 error 2 次以上
2. AI 的回報出現「自我矛盾」（如「X 不存在，正確應該是 X」）
3. AI 不執行 ls 但回報「ls 三個都成功」（純幻覺）
4. AI 把指令裡明確寫的路徑（`.openclaw`）「自動解讀」成別的（`.claude-code`）

**止血 SOP：**
1. ❌ 不要試圖糾正污染的 session（指令蓋不過記憶）
2. ✅ 立刻關掉對話框（不是刷新，是直接關）
3. ✅ 開新對話框 + 重貼指令
4. ✅ 如果新對話框也壞 → 軍師親手接手（不要再耗 token）

**根因：** Claude Code 的 session 一旦 context 被某個錯誤事實污染，**指令蓋不過記憶**——它會「忠實執行軍師指令」但用它自己記憶裡（污染後）的路徑。

**解法：** 派外包指令裡寫死「自停條款」+ 教練看到迴圈直接關對話框換新的（不要試圖糾正污染的 session）。
