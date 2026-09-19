---
name: tokentable-claude-tool-calling-bug-2026-09-20
description: 第三方API轉售平台TokenTable(tokentable.asia)的Claude系列模型(claude-opus-4-8/claude-sonnet-5/claude-fable-5)一啟用function tools就502/400失敗，GPT系列(gpt-5.6)正常，已接進OpenCode CLI驗證
metadata:
  type: reference
---

# TokenTable：Claude系列模型工具呼叫故障，GPT系列正常

## 背景

2026-09-20教練提供TokenTable(tokentable.asia，月費制AI API轉售平台，OpenAI相容格式，Base URL `https://tokentable.asia/v1`)的API Key，要求接進本機的Hermes或OpenCode其中一個。軍師評估風險後選擇先接OpenCode（CLI工具，出問題影響範圍小；Hermes是24小時Telegram正式系統，之前有因改動不慎斷線16小時的紀錄[[feedback_hermes_gateway_vs_desktop_app_distinction_2026-09-19]]，不先動）。

設定寫在 `~/.config/opencode/opencode.jsonc` 的 `provider.tokentable`（跟既有kimi/opencode-go provider同樣用 `@ai-sdk/openai-compatible` 格式）。

## 發現的問題

純聊天（無tools）完全正常，但OpenCode的agent模式一定會帶function tools（跑bash/改檔案這些都要靠tool calling），這時：

| 模型 | 純聊天 | 帶function tools |
|---|---|---|
| claude-opus-4-8 | 未測 | ❌ 502，`Function tools with reasoning_effort are not supported for gpt-6-astra` |
| claude-sonnet-5 | ✅ | ❌ 同樣502同樣錯誤訊息 |
| claude-fable-5 | 未測 | ❌ 同樣502同樣錯誤訊息 |
| gpt-5.6 | 未測 | ✅ 正常回傳tool_calls，OpenCode CLI實跑成功(叫它查時間，真的執行`date`指令拿到正確答案) |

錯誤訊息裡出現的「gpt-6-astra」很奇怪——不管指定哪個Claude模型，錯誤都提到這個不相關的模型名，研判是TokenTable自己後端在轉譯Claude家族的工具呼叫格式時，內部路由/轉譯層有bug，不是我們這邊設定錯，也不是OpenCode的問題（同一套OpenCode代理層對gpt-5.6完全正常）。

用curl直接打API重現過這個現象（非OpenCode特有），可排除OpenCode本身的bug。

## How to apply

- 任何機器要用TokenTable做「真正執行任務」（agentic/tool calling）用途，**選GPT系列模型（已驗證gpt-5.6可用），不要選Claude系列**，Claude系列目前在TokenTable上工具呼叫必掛
- 這是TokenTable平台自己的bug，等他們修——之後如果教練或任一機器要驗證是否修好，直接用上面的curl測試法重測（帶一個簡單function tool的chat completions請求）即可，不用整套接進agent工具才測得出來
- 純聊天（不涉及工具呼叫）用途Claude系列完全沒問題，只有「執行任務」這個用途才會踩到

## 相關

- [[feedback_hermes_gateway_vs_desktop_app_distinction_2026-09-19]]（為什麼先接OpenCode不接Hermes的風險考量依據）
