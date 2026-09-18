---
name: minimax-mystery-resolved-model-name-routing
description: 手機Remote Control「身份驗證是真Anthropic但流量流向MiniMax」懸案真正根因查明：SDK按model名稱字串是否被Anthropic辨識來決定路由，不是看BASE_URL設定本身
metadata:
  type: reference
---

延續 [[reference_mobile_session_minimax_traffic_unresolved_mystery_2026-09-19]]（案例78，nettop測到手機session對MiniMax真實IP有32MB流量但JWT驗證是真Anthropic的矛盾未解）。2026-09-19 05:53~06:20 教練親自給出解釋方向後，實測查證出真正完整根因，懸案結案。

## 真正根因：Claude Code CLI 按 model 名稱字串是否為「Anthropic辨識的合法模型id」來決定連線目的地，不是單純看 `ANTHROPIC_BASE_URL`

實測證據鏈（2026-09-19 05:54~06:15，`ps aux` + `lsof -p <pid> -i -n` + `nettop -p <pid>`）：

1. **settings.json 全域 env 區塊**（`~/.claude/settings.json`）：
   - `ANTHROPIC_DEFAULT_SONNET_MODEL = claude-sonnet-5[1m]`（Anthropic真實model id + 1M後綴）
   - `ANTHROPIC_DEFAULT_HAIKU_MODEL = MiniMax-M3[1m]`、`ANTHROPIC_DEFAULT_OPUS_MODEL = MiniMax-M3[1m]`（MiniMax自家model id，Anthropic後端不認得這個名字）
   - `ANTHROPIC_BASE_URL = https://api.minimax.io/anthropic`（全部session共用同一個BASE_URL設定，不分Sonnet/Haiku/Opus）

2. **主要互動模型（Sonnet-tier，`--model claude-sonnet-5[1m]`）**：無論是`--print`直測還是實際`claude rc`重啟的RC session，`lsof`實測連線**只打到 160.79.104.10（真Anthropic）**，從未連到MiniMax真實IP。`/status`顯示`Login method: Claude Pro account`、`Anthropic base URL: https://api.anthropic.com`——因為 `claude-sonnet-5` 是Anthropic後端真實認得的model id，CLI優先用已登入的原生Claude Pro OAuth連線處理，`ANTHROPIC_BASE_URL`/`API_KEY`/`AUTH_TOKEN`這幾個env在這個路徑下形同虛設（推測：MiniMax金鑰格式`sk-cp-0_`開頭不符合Anthropic API key格式驗證，CLI偵測到格式不對後自動fallback回原生OAuth，這條路徑徹底忽略BASE_URL）。`--print`直接問模型自報：`MODEL=Sonnet 5 (claude-sonnet-5[1m]) CTX=1000000`，配合網路層鐵證（真連到160.79.104.10），這次自報可信，1M context window對主要互動模型是真的。

3. **背景/低階任務model slot（Haiku/Opus-tier，實際觀察到`--model MiniMax-M3[1m]`）**：2026-09-19 06:16重啟RC後教練手機端立刻spawn了一個新子session（PID 99778，父行程是剛重啟的`claude rc` PID 99751），這個子行程的啟動指令明確帶`--model MiniMax-M3[1m]`——**這個字串不是Anthropic認得的model id**，於是CLI换了一條路徑：`lsof`實測這個PID真的有一條連線打到 **175.99.116.25**（MiniMax真實IP，`api.minimax.io`透過Akamai CDN解析出的位址，跟案例78 v225用TLS憑證`CN=www.minimax.io`驗證過的是同一個真實伺服器），旁邊還有8條連線是160.79.104.10（這個子session混合處理，可能是同一個agent在不同tool call間切換model tier）。

## 結論：兩邊都是真的，不是矛盾，是「按model名稱分流」

- Sonnet主線互動 → model名稱是真Anthropic id → 原生OAuth → 真連Anthropic → 真1M
- Haiku/Opus背景任務 → model名稱是`MiniMax-M3[1m]`（Anthropic不認得）→ CLI找不到對應原生model，退回用`ANTHROPIC_BASE_URL`+`ANTHROPIC_API_KEY`打MiniMax → 真連MiniMax

這剛好跟教練2026-09-19 05:53親口給的解釋方向一致：「底層架構規定除了Claude以外，所有模型鐵律強制走MiniMax，這是我下的指令」——`ANTHROPIC_DEFAULT_HAIKU_MODEL`/`ANTHROPIC_DEFAULT_OPUS_MODEL`維持`MiniMax-M3[1m]`就是這個政策的具體實作，只是機制細節（按model名稱字串判斷路由，不是單純BASE_URL開關）教練原本不知道，AI也是這次才用網路層證據挖出來。

## 教練最終裁示（2026-09-19 05:53，優先權排序）
1. 手機版RC有沒有走MiniMax不是重點——「它不是思考的料，是幹活的料」，手機只拿來下簡單指令/叫Mac桌面版或小龍蝦做事，不會拿來討論思考類任務
2. 唯一在乎的是「200K能不能變1M」——已確認：主要互動的Sonnet model走真Anthropic時，1M是真的（見上方[[reference_remote_control_relaunch_blocked_mystery_2026-09-19]]/[[feedback_cli_self_described_model_unreliable_and_path_reversal_2026-09-19]]的B路徑驗證，這次用真實RC session再次交叉確認）
3. 教練明確指示：「自己想辦法解決問題，不要再等我決定」——這條記憶連同RC重啟腳本v2修復都是教練睡覺期間自主完成，未等待授權

## 伴隨修復
1. `~/.claude/settings.json`永久移除`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`這個key（唯一真正擋住`claude rc`啟動的變數，不影響其他既有session，因為env只在process啟動當下讀取一次）
2. `~/.zshrc`的`claude-remote`alias + `scripts/restart_remote_control.sh`都改版（v2）：不再需要暫時搬移整份settings.json這種粗暴解法，只要unset這一個key即可
3. **反直覺的新坑，寫進[[feedback_claude_rc_never_unset_base_url_2026-09-19]]**：明確`unset ANTHROPIC_BASE_URL`（即使目標是清空它）反而會觸發`claude rc`自己的硬性檢查噴錯「is set and does not point at api.anthropic.com」，正確做法是完全不要去動這個變數，讓它保持原狀（settings.json裡的MiniMax值）即可正常連線——已用4輪tmux實測交叉確認這個結論
4. 手機端正式重啟RC並驗證：`bash scripts/restart_remote_control.sh`跑出`✅ Remote Control 已成功啟動並連線`，教練手機App應可正常使用，且主要對話走1M Sonnet
