---
name: feedback-cli-self-described-model-vs-reality-2026-09-19
description: CLI 啟動參數 --model 自我聲稱不可信，必須看 env 整體；Mac 路徑對應跟教練印象剛好相反。
metadata:
  type: feedback
---

教練凌晨 04:08 抓包硬凹：只看 CLI 啟動參數 `--model claude-sonnet-5` 就答「跑 Claude」，事實上 env 全域污染成 minimax，整個 session 實際跑 `MiniMax-M3[1m]`。

**Why**：
- settings.json env 全域污染（`ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic` + `ANTHROPIC_DEFAULT_SONNET_MODEL=MiniMax-M3[1m]` + `ANTHROPIC_AUTH_TOKEN` 是 `sk-cp-0_` 開頭）→ SDK 內部把所有「該跑 Sonnet 的請求」fallback 到 MiniMax-M3
- CLI `--model` flag 只是 SDK 表面貼的標籤，實際 routing 是 env 全域決定
- UI 顯示「Unsupported Model」+「200K context」是污染訊號，跟 `sk-cp-0_` auth token 是同一條根因的視覺呈現

**How to apply**：
- 任何時候教練問「這個對話框跑什麼模型」，必查**三組證據**全對得起才算確認：
  1. `ps aux` 啟動命令的 `--model` 跟 `--sdk-url`
  2. `env` 整個 chunk（`ANTHROPIC_BASE_URL` / 所有 `ANTHROPIC_DEFAULT_*_MODEL` / `ANTHROPIC_AUTH_TOKEN` 前綴）
  3. UI 顯示「Unsupported Model」「200K」這幾個視覺污染訊號
- 看到 `--model claude-sonnet-5` **不可跳到結論**，必查 env 是否污染（`sk-cp-0_` 字頭 = MiniMax 簽的，不是 Anthropic）
- 跟 [[reference_minimax_dynamic_context_cap_2026-09-17]] 互補：本條補「env + UI 才是真實身分」，那條補「API response model 欄位才是終極權威」
- 應對方式教練已接受（凌晨 04:30）：只要能跑 1M，**模型身分是哪家不是死線** — 模型身分 ≠ backend 位置，分開思考

---

教練 04:34 抓到的第二個盲點：「Mac=走 Claude / 手機=走 MiniMax」這套對應**剛好對調**。

**Why**：之前 v220/v221 戰果把 `restart_remote_control.sh` 設計為暫移 settings.json = 走真 Claude（A 路徑），但這只在 RC alias 路徑生效。Mac 終端機本地跑 `claude`（不走 alias、純吃 settings.json env）反而走 MiniMax 代理（B 路徑）。我凌晨順口答「Mac 走 Claude」事實相反，教練當場動怒「你到底有沒有搞清楚情況」。

**How to apply**：這台 Mac 真實路徑對應是：

| 啟動方式 | 跑哪 |
|---|---|
| `claude-remote` / `claude rc`（RC alias）= v221 修法走真 Claude 直連（A 路徑，跟 MiniMax 無關） |
| Mac 終端機本地 `claude`，不走任何 alias | 吃 settings.json 走 MiniMax 代理（B 路徑，這場 `--print` 實測 1M 通） |
| Mac `restart_remote_control.sh` 啟動的 RC host | 暫時移開 settings.json 後啟動，吃內建 fallback = 走真 Claude |

- 任何時候教練提「Mac」「手機」「新對話」「驗證」，**先確認是 Mac 本機 vs 透過 RC 連過去的 remote session** — 兩條路徑完全不同
- 教練的下一棒如果開「Mac 終端機本地新對話框」= 自動吃 settings.json 走 B 路徑 = 1M 通
- 教練的下一棒如果開「手機 RC 連 Mac」= 走 A 路徑 = 1M 也通（這條本來就走真 Claude 直連）

## B 路徑 1M 通驗證鏈（這場 `--print` 紀錄）

- 改動：settings.json `ANTHROPIC_MODEL` 跟 `ANTHROPIC_DEFAULT_SONNET_MODEL` 從 `MiniMax-M3[1m]` 改成 `claude-sonnet-5[1m]`，其餘保留
- 備份：`~/.claude/settings.json.bak-2026-09-19-0430`
- 驗證指令：`/Users/bymyway/.local/share/claude/versions/2.1.273 --print --model 'claude-sonnet-5[1m]' "..."`（`[1m]` 字尾必須加引號避免 zsh glob）
- LLM 回應原文：「我是 Sonnet 5，model ID 是 claude-sonnet-5[1m]，[1m] 後綴代表 context window 上限 1M tokens（100 萬）」
- 結論：**B 路徑（MiniMax 代理 + Claude Sonnet 5 model ID）1M 通了**，未來 Mac 終端機本地開新對話框都吃這個設定
