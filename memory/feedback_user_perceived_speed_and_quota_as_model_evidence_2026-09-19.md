---
name: feedback-user-perceived-speed-and-quota-as-model-evidence-2026-09-19
description: 用戶體感視角的兩條模型身分證據（回應速度 + 額度用量）跟現有三層技術證據鏈互補，技術盲點別忽略用戶活證據。
metadata:
  type: feedback
---

教練 04:44 給出兩條用戶體感視角的鐵證，補完[[feedback-cli-self-described-model-vs-reality-2026-09-19]]三層技術證據鏈沒涵蓋的盲點：

1. **回應速度**：「Claude 在回答問題不會這麼快，他都要想很久，MiniMax 就可以很快」 — Claude Sonnet 5 回應前都有 planning/extended thinking，使用者體感是「慢慢想才講」；MiniMax 系列回應節奏明顯快、幾乎沒有思考停頓
2. **額度用量**：「MiniMax 4,500 次呼叫目前跑到 8%」 — MiniMax provider 的 quota counter 是公開可查，會真實反映「這個對話框跑了多少次 MiniMax backend」。如果跑的是真 Claude（直連 api.anthropic.com），這個 counter 數字不會動；只有走 MiniMax 代理/原生 MiniMax 服務的呼叫才會計入

**Why**：
- 技術證據鏈（ps aux `--model`/`--sdk-url` + env chunk + UI「Unsupported Model」顯示）雖然權威，但要查 ps/env/UI 才有答案，且容易在快速回話時漏查
- 用戶體感證據是**用戶自己即時可觀察**的（不用打指令），在凌晨疲勞/快速對話情境下往往比技術鏈更早被抓到
- 教練 04:44 把這兩條當「鐵證如山」拿出來，是因為這是他不用進終端機打指令就能拿出來的證據，**比技術鏈更貼近用戶實際判斷場景**

**How to apply**：
- 教練任何時候提「這個對話框跑什麼模型」，除了走三層技術證據鏈之外，**主動也提體感線索**：
  - 這台機器過去 1 小時的回應速度有沒有明顯比平常快？
  - 有沒有 quota counter / 用量頁面可以查？（MiniMax provider 有 4,500 次/5hr quota，Anthropic 直連沒這個限制）
  - 教練自己觀察到的速度差異 = 他自己的直覺線索，要認真對待不可忽略
- 教練已經建好的[[reference_minimax_quota_5h_4500_calls]]記憶就是這條 quota counter 的權威來源，未來任何「是不是走 MiniMax」的判斷都先看這個數字有沒有在動
- 跟[[feedback-cli-self-described-model-vs-reality-2026-09-19]]三層證據鏈是**互補兩層**，不是取代：技術鏈給確切答案、體感鏈給即時方向感
- 教練 04:44 明講「我會請 Claude 的助教好好繼續讀你的總結報告」 = 教練開新對話框前要先看總結，這是**開新對話框前的交接 SOP**，未來接力棒開頭要明確標註「教練跨對話框交接情境」

## 教練 04:38 的最終場景釐清（v223 第 3 節需修正）

教練 04:38 講的場景：
> 「開 Mac 終端機本地新對話框 → 永遠 Sonnet 1M、沒在顯示過 200K；200K 出現只有 MiniMax 路徑才有」

這跟 v223 第 3 節寫的「Mac 本地 = 走 MiniMax 代理（B 路徑）」**UI 體感上是一致的** — 因為 Mac 本地新對話吃 settings.json 裡的 `claude-sonnet-5[1m]` model ID，**MiniMax 透明代理到 Claude Sonnet 5 backend**，所以 UI 顯示「1M + Sonnet」。教練看 UI 就是「永遠 1M Sonnet」，跟「走真 Claude」的視覺體驗無法區分。

- v223 第 3 節講的是「啟動方式 → backend 路由」的對應（技術真實）
- 教練講的是「UI 顯示 → 用戶體感」的對應（用戶真實）
- 兩者不矛盾，但 v223 沒講清楚這層差異，造成我跟教練對話時用詞衝突
- **未來跟教練講 model/backend 議題時，要明確分開兩個層次**：UI 體感層 vs 技術 backend 層，不要混用「走 Claude」這個詞（容易造成「直連 Claude」vs「MiniMax 代理到 Claude」兩種解讀的混淆）
