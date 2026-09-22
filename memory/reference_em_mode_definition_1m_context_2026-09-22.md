---
name: em-mode-definition-1m-context
description: EM 模式 = 1M context window（教練內部簡寫，e = 1 = 1M），不是 Extended Mode / Enterprise Mode。對應 model name 字串 [1m] 後綴、`--print` 測試 CTX=1000000、CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000 設定。v227 完整機制：claude-sonnet-5[1m] 走 Anthropic 原生 OAuth → 1M 真有效。
metadata:
  type: reference
---

# EM 模式 = 1M context window

## 精確定義（一字不差）

EM 模式 = **1M context window**（一百萬 token context window）。

教練內部簡寫，**「e」是數字「1」的代號**（教練 2026-09-22 20:52 台灣時間親口講：「em它是『1234567』的『1』，所以是 1m 結果他寫成英文字母的『e』」）。

**不是 Extended Mode / Extended Model / Enterprise Mode**——之前搜尋方向完全錯誤，一直找不到就是因為去找這些技術術語。

## 三種驗證 EM（1M context）的依據

| 驗證方式 | 輸出 | 意義 |
|---|---|---|
| **model name 字串** | `claude-sonnet-5[1m]`（帶 `[1m]` 後綴）| 1M context 啟用標記 |
| **`--print` 測試** | `MODEL=Sonnet 5 (claude-sonnet-5[1m]) CTX=1000000` | 模型自報 1M context |
| **環境變數** | `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` | CLI 1M compact window 設定 |

## v227 完整機制（教練 9/19 凌晨 5:53~6:25 解出）

Claude Code CLI 按 **model 名稱字串是否為「Anthropic 辨識的合法 id」**決定連線目的地，**不是看 `ANTHROPIC_BASE_URL`**：

| Model 字串 | Anthropic 是否認得 | 路由 | Context |
|---|---|---|---|
| `claude-sonnet-5[1m]` | ✅ 真認得 | 原生 Claude Pro OAuth → 160.79.104.10 | **1M context（EM 模式）** |
| `MiniMax-M3[1m]` | ❌ 不認得 | 退回 BASE_URL → 175.99.116.25 | 200K（MiniMax 預設）|

推測機制細節：MiniMax 金鑰格式 `sk-cp-0_` 開頭不符合 Anthropic API key 格式驗證，CLI 偵測後自動 fallback 回原生 OAuth → `ANTHROPIC_BASE_URL`/`API_KEY`/`AUTH_TOKEN` 在 `claude-sonnet-5[1m]` 路徑下形同虛設。

## v225 手機 session 硬證據（MiniMax 32.35MB > Anthropic 12.94MB）

- PID 51719（04:06 啟動，session id 尾碼 `Crf`）
- nettop 量測：MiniMax 175.99.116.25 流出 32.35MB / 流入 2.11MB；Anthropic 160.79.104.10 流出 12.94MB / 流入 1.25MB
- MiniMax 是 Anthropic 的 **2.5 倍**
- TLS 憑證驗證：`curl --resolve api.minimax.io:443:175.99.116.25` 確認 `CN=www.minimax.io`，排除 CDN 共用節點誤判

## 教練 9/22 14:51 新規（跟這個定義的關係）

「手機開工 = minimax 模型 = 特助身份」——這個是「**身份判定**」層次，意思是教練說「手機開工」時整個 session 視為 minimax + 特助。

但**「實際跑什麼 model」** 仍由 v227 機制決定：
- 如果手機 session model 是 `claude-sonnet-5[1m]`（Anthropic 認得）→ Sonnet 主線走 Anthropic 真 1M
- 如果手機 session model 是 `MiniMax-M3[1m]`（Anthropic 不認得）→ 退回 BASE_URL 走 MiniMax

兩個判定是不同維度：身份（教練宣告）vs 流量（model 字串機制）。

## 怎麼應用

- 聽到「EM 模式」「走 EM」「EM」→ 直接理解為 1M context window，不要再去找 Extended Mode 那些
- 問當前 session 走不走 EM → 看 `--model` 啟動參數有沒有 `[1m]` 後綴，或跑 `--print "..."` 看 `CTX=` 數字
- 問當前 session 走 MiniMax 還是 Anthropic → 看 lsof 有沒有 175.99.116.25 連線 + 看 model 字串
- 教練說「200K」「200k context」→ MiniMax 路徑（不是 EM 模式）

## 相關

- [[reference_minimax_mystery_resolved_model_name_routing_2026-09-19]]（v227 完整機制原文）
- [[reference_mobile_session_minimax_traffic_unresolved_mystery_2026-09-19]]（v225 案例 78 懸案原文）
- [[feedback_phone_kai_gong_means_minimax_model_2026-09-22]]（9/22 14:51 教練手機開工新規）
- 試金石案例 78 第 3642~3692 行
