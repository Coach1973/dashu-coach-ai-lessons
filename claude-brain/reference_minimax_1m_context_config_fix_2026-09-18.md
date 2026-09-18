---
name: reference-minimax-1m-context-config-fix-2026-09-18
description: "~/.claude/settings.json的MiniMax模型字串大小寫寫錯([1M]應為[1m])+缺CLAUDE_CODE_AUTO_COMPACT_WINDOW，導致手機Remote Control context window被鎖死在200K而非MiniMax-M3真正支援的1M，已依官方文件修正"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 915e272e-7a9b-4c59-b1ae-7377bdea7f62
  modified: 2026-09-18T11:04:34.179Z
---

教練問「MiniMax最高等級是1M不是200K，能不能研究一下改參數」，查證屬實並修復。

## 根因（直接fetch MiniMax官方文件`platform.minimax.io/docs/token-plan/claude-code`原始JSON驗證，非猜測）

官方建議的Claude Code設定：
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimax.io/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "<MINIMAX_API_KEY>",
    "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000",
    "ANTHROPIC_MODEL": "MiniMax-M3[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M3[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M3[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M3[1m]"
  }
}
```

這台Mac`~/.claude/settings.json`原本的設定有兩處跟官方文件不符：
1. **大小寫錯誤**：`MiniMax-M3[1M]`(大寫M)，官方要求`MiniMax-M3[1m]`(小寫m)——Claude Code對模型字串是大小寫敏感比對，這正是稍早tmux log看到`[claude-code:unrecognized_model] {"model":"MiniMax-M3[1M]"...}`錯誤的根因，模型字串沒被辨識成「1M變體」，退回預設(繼承Sonnet的200K)context window估算
2. **Haiku完全沒加`[1m]`後綴**（純`MiniMax-M3`）
3. **完全缺少`ANTHROPIC_MODEL`跟`CLAUDE_CODE_AUTO_COMPACT_WINDOW`兩個key**——後者是明確告訴Claude Code「auto-compact的門檻是100萬token」，沒設就算模型字串對了，Claude Code可能還是用內建的較小預設值觸發compact

## 已知關聯的官方bug（仍open未修復）

GitHub issue `MiniMax-AI/MiniMax-M2.7#46`(open狀態，官方尚未修復)：用**純**`ANTHROPIC_MODEL: MiniMax-M3`(無`[1m]`後綴)時，`/anthropic` endpoint回傳的model metadata會讓Claude Code誤判成200K(疑似繼承Claude Sonnet的context_window值)。`[1m]`後綴正是MiniMax官方提供的workaround——讓Claude Code的模型字串驗證邏輯辨識出這是「1M變體」而套用正確的大額度，繞過這個未修復的metadata bug。

## 已修復+已驗證

1. 修正`~/.claude/settings.json`的`env`區塊：4個模型變數全部改小寫`[1m]`後綴+補上`ANTHROPIC_MODEL`+補上`CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000`，逐字比對官方文件JSON無誤
2. 用curl直接呼叫`https://api.minimax.io/anthropic/v1/messages`帶`"model":"MiniMax-M3[1m]"`測試，API正常回應(非400/未知模型錯誤)，證實字串本身有效
3. 原始值已備份於`/tmp/settings_backup/claude_settings_env_before_2026-09-18.json`供回退

## 限制：只對「新啟動」的session生效

settings.json的`env`是process啟動時讀取寫入子行程環境，**已經在跑的`claude rc` host process(教練手機Remote Control的host)跟其下已存在的子session不會回溯套用**，要等下次重啟`claude rc`或開全新session才會吃到新設定。教練若想讓「現在」的手機host立即套用，需要重啟`claude rc`(會中斷目前手機上開著的對話)，這是教練自己的取捨，非軍師擅自決定。

## Why 這值得記

`ANTHROPIC_DEFAULT_*`這組變數表面上看起來「隨便打都行」，實際上Claude Code對其字串內容做精確比對來決定功能開關(這裡是context window額度)，一個大小寫之差就讓月費/額度花在200K假設上，實際上帳單早就付了1M的服務。往後任何provider的Claude Code整合設定，**改完一定要直接fetch該provider官方文件的原始設定範例逐字比對**，不能只憑第三方摘要或憑印象猜測大小寫/底線/連字號這類細節。

## 相關

- [[feedback_minimax_dynamic_context_cap_2026-09-17]]（同一個現象：context window顯示會變小，但那篇記錄的是「動態縮減」現象，本篇找到的是「一開始上限就被鎖死在200K」的設定錯誤，兩者疊加）
- [[feedback_hook_hardcoded_identity_assumption_2026-09-18]]（同一場對話發現的另一個ANTHROPIC_*環境變數相關bug）
