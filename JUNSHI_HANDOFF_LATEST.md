# 軍師接力棒 · 2026-06-11 v17（Sonnet 4.6 終端機 session）

> 建立時間：2026-06-11 凌晨 3:57 台灣時間
> 本棒執行者：Sonnet 4.6
> 上一棒：v16 Favicon SOP + jiesheng-leadership 按鈕修改

---

## 🎯 本場最重要成果

### 1. jiesheng-leadership 早鳥按鈕還原（commit e7833b7）
- 移除「搶限量早鳥名額」按鈕，回到只有「報名線上座談會」+「立即報名工作坊」
- 早鳥版備份存於 `_backup/index_含早鳥名額版.html`（commit e7833b7）
- **暗號已寫入記憶**：教練說「恢復早鳥名額」→ cp 備份蓋回 → 預覽 → 教練說推才推

### 2. 試金石案例 H 補入（commit c8456491）
- 案例 H-2026-06-11：jiesheng-leadership 分批 push 再扣 15 點
- 同案例 G 根因，守則 #07 再犯紀錄
- 路徑：`workspace/試金石/試金石_案例庫.md`

### 3. 結繩領導學收單策略報告 → GitHub Pages（commit d31681e）
- 新建 `Coach1973/teamwork` repo（gh-pages 分支）
- 上線網址：https://coach1973.github.io/teamwork/rpl/
- 補充內容（對照 DOCX + SOP）：
  - 7場座談會（修正「新書發表會」→「座談會（與作者有約）」）
  - 「傘繩」（修正「閃神」）
  - 雙人搭接模式 + 兩次 CTA 時機
  - 互惠槓桿重點鎖定區域（高雄中區、台南市區、台中市區、台中南區）
  - 毛利防禦戰略說明（$1,000 贈品 vs $1,000 折扣）
  - 關鍵字洗版腳本（「我也要領傘繩」「+1」「已匯」）
  - QR Code 立牌（醫療展）
  - 佩君老師拆出獨立欄位（新職責描述）
  - 新增時間軸表格
  - 新增異常排除對照表

---

## 📋 下一棒待辦

| 優先 | 任務 | 說明 |
|------|------|------|
| 🔴 | 全自動蒸餾系統 | 地基已查清，是最高優先任務 |
| 🟡 | bymyway.com 搬移 | 超限戰、cool-case 搬進 bymyway 主站（教練之前提到） |
| 🟡 | jiesheng-leadership 金流就緒時 | 說「恢復早鳥名額」立刻執行備份還原 |

---

## 🔑 重要 commit hash 索引

| commit | 內容 |
|--------|------|
| e7833b7 | jiesheng-leadership 移除早鳥按鈕 + 備份 |
| c8456491 | 試金石案例 H（workspace repo） |
| d31681e | teamwork/rpl GitHub Pages 首次推送 |

---

## 📌 常用路徑提醒

- jiesheng-leadership repo：`/Users/bymyway/github_repos/jiesheng-leadership/`
- 早鳥備份：`_backup/index_含早鳥名額版.html`
- 試金石：`~/.openclaw/workspace/試金石/試金石_案例庫.md`
- 網頁推 SOP：`~/.openclaw/workspace/knowledges/SOP_netlify_website_edit.md`


---

## 🔒 v17.1 增補（2026-06-11 凌晨 4:15，Fable 5 軍師）

### 教練拍板的新方向：「規則太多、機關太少」→ 重複犯錯改用物理鎖
1. **推送鎖（pre-push）已裝**：jiesheng-leadership / cool-case / theunrestrictedwar 三個資料夾。
   - 沒有通行證 `.git/PUSH_APPROVED` → git push 直接被擋（案例 G+H 永久止血）
   - 教練說「推」→ `touch .git/PUSH_APPROVED && git push`，單次有效、30 分鐘過期
   - 安裝器：`scripts/install-push-lock.sh`
   - 教練補充：只有 Netlify（jiesheng-leadership）扣點，另外兩個不扣
2. **截圖鎖（PreToolUse hook）已裝**：`scripts/screenshot_lock.sh`，掛在 `~/.claude/settings.json`
   - 沒有通行證 `state/SCREENSHOT_APPROVED` → 所有截圖/zoom 工具（含批次夾帶）直接被擋
   - 教練同意 → `touch ~/.openclaw/workspace/state/SCREENSHOT_APPROVED`，10 分鐘有效
   - 永久測試套件：`scripts/test_screenshot_lock.sh`（11 項全過才能改 hook，案例 F 教訓）
   - ⚠️ 限制：只管終端機 CLI；桌面版 Claude.app 是否吃這個 hook 未驗證；小龍蝦（OpenClaw）另一套系統不在範圍
3. **教練待決事項**：另外三個建議（就地放規則紙條 / 查話工具 / 基礎建設封頂）尚未拍板

---

## 🔎 v17.2 增補（2026-06-11 凌晨 4:50，Fable 5 軍師）：查話系統上線

### 教練最重視的「記憶力」問題，三層解法已全部落地
1. **逐字保險箱**：`memory/verbatim/YYYY-MM.jsonl`（只加不刪）
   - 🔴 重大發現：OpenClaw sessions 在 Context Overflow 重啟會被清掉，「原文100%都在」對小龍蝦不成立！
   - 每 30 分鐘 crontab 自動收割（小龍蝦三群 + 終端機備份），從此原文永不蒸發
2. **自動索引**：`state/recall_index.jsonl`，885 句真人的話，0.7 秒重建，過濾 cron/心跳/作夢噪音
3. **查話入口**：`scripts/recall.py 關鍵詞` → 台灣時間+出處+原句，只回前10筆（省 Context）
   - 同義詞自動展開：`state/recall_synonyms.json`（語音糾偏對映表的落地）
   - 小龍蝦接線：TOOLS.md 已加「教練問舊話→跑 recall」段落
   - crontab 已註冊並當場驗證（E09）：`*/30 * * * * recall.py --harvest --build`

### 下一棒注意
- 同義詞表發現新諧音就補
- verbatim/ 會隨 workspace 的 git 自動備份上雲
