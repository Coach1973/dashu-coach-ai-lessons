---
name: project-2026-07-02-guardrail-expansion
description: 一場75輪對話內建立機關生命週期SOP+4個新機關（HTML預覽查證/#03/#08/主動提醒開新視窗），並在cool-case上線案例33-37
metadata:
  type: project
  originSessionId: e800e341-3d04-4ed4-bf2a-f43e799bb9e4
---

2026-07-02（延續自前一晚VPS體檢/長期記憶修復），教練把重點從「單一問題修復」轉向「系統化防止重複犯錯」，一場對話內完成：

**1. cool-case上線案例33-37**：教練重申鐵律「沒有上傳到cool-case網站之前的，就不要跟我說是已經定案的案例」，5個案例（VPS體檢/先斬後奏鎖兩難/VPS長期記憶修復/輪詢第三次糾正/HTML預覽查證鎖）全部轉HTML、本機Chrome預覽驗證、教練確認後推上GitHub Pages。

**2. 機關生命週期SOP建立**（`機關SOP.md`）：機關分Block/Warn/Allow三級、建機關的觸發條件（違反2次以上或教練生氣過）、每3個月定期審計「這個鎖還有意義嗎」——回應教練昨天提的「上鎖越多會不會把自己鎖死」的疑慮（OPE查證業界共識已在案例34記錄）。

**3. 4個新機關，全部當場合成測試通過才commit**：
- `web_preview_verify_guard.sh`（Block）：git push網站前查對話紀錄裡有無真的開過Chrome的證據，不採信AI自稱通行證——回應教練「一個月6次沒給看HTML」的質問（見[[feedback_html_preview_chrome_only]]延伸）
- `rule03_verify_before_answer_check.sh`（Warn，本場擴充2次）：從單純猜測語言，擴大到肯定式誤判（沒hedge詞卻宣稱發現問題）、瞎猜/亂猜自承語言
- `rule08_ask_when_clear_check.sh`（Warn）：方向已清楚卻還多問「要不要我」
- `rule_proactive_session_reminder_check.sh`（Warn）：輪數過門檻後檢查回覆有沒有真的主動提「開新視窗」

**4. 過程中連續兩次抓到自己的方法論錯誤**（詳見[[feedback_verify_via_real_transcript_not_case_count]]）：用案例庫筆數估算頻率被教練點破不精準；重查後給的「2次」答案本身又是沒徹底查證的產物，最終正確數字是8次。

**5. 過程中抓到2個真實bug並當場修復**：
- `web_preview_verify_guard.sh`比對整條指令自由文字，被commit message內文誤觸（提到「government-grow」四字就誤判要推該網站）——改成只認cwd/cd路徑型比對
- `rule03`白名單「已經/之前」太籠統，導致「我已經找到問題，要不要我修改」這種該被抓的句子被誤放行——收窄白名單重測

**How to apply**：
1. 下次教練問「這值不值得建機關」，直接用查真實transcript的方法（見[[feedback_verify_via_real_transcript_not_case_count]]），不要再用案例庫筆數估算。
2. 新建的Warn級機關都只跑過合成測試，還沒在真實對話中驗證過噪音率——運作幾天後要回頭檢查 `distill/rule*_violations.log` 有沒有誤報。
3. 完整機關清單見 `機關SOP.md` 第五節，目前共9個（5 Block在PreToolUse + 4 Warn在Stop）。

Related: [[feedback_verify_via_real_transcript_not_case_count]], [[project_vps_local_embedding_fix_2026-07-02]]
