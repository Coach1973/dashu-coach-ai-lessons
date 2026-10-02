---
name: reference-openclaw-bootstrap-20k-char-limit
description: OpenClaw每個bootstrap檔(AGENTS.md/SOUL.md/HEARTBEAT.md/MEMORY.md等)有DEFAULT_BOOTSTRAP_MAX_CHARS=20000字上限，超過會被硬切斷、可能切在多位元組中文字中間造成UTF-8亂碼；不要把自動化日誌寫進這些檔案，改寫state/*.log
metadata:
  node_type: memory
  type: reference
  originSessionId: b9d35266-2d17-4f5f-8412-f41e7726a492
  modified: 2026-09-25T16:26:42.203Z
---

# OpenClaw bootstrap 檔案有 2 萬字硬上限，超過會被切斷出亂碼

## 核心事實（2026-09-25 查證，試金石案例83）

OpenClaw 安裝目錄的原始碼裡寫死 `DEFAULT_BOOTSTRAP_MAX_CHARS = 2e4`（2 萬字），小龍蝦每次開機讀取
`AGENTS.md`／`SOUL.md`／`HEARTBEAT.md`／`MEMORY.md`／`USER.md`／`TOOLS.md`／`IDENTITY.md` 這些
bootstrap 檔時，超過這個字數的部分會被截斷。截斷點不看字元邊界，**可能剛好切在一個多位元組中文字
中間**，讀出來直接是 UTF-8 decode error / 亂碼（實測 `HEARTBEAT.md` 25,769 字時切出 2 處亂碼，
`MEMORY.md` 20,717 字時切出 1 處）。

## 起因

軍師端 5 支程式（`feed_junshi_handoff.sh`／`.ps1`、`sync_handoff_to_claudemd.sh`、
`sync_xinfa_to_claude_global.sh`、`sync_zhixingxize_to_claude_global.sh`、
`session_end_auto_push.ps1`）長期把「Hook 自檢」「自動同步結果」這類軍師自己的執行日誌
`>>` append 進 `HEARTBEAT.md`——這是小龍蝦（OpenClaw agent）的開機必讀檔，不是軍師的日誌本。
累積到 167 段裡有 155 段（78% 字數）都是軍師寫的，把檔案撐爆上限。

## How to apply

1. **任何要記錄「這個 hook/腳本執行過」的自我測試/留證，一律寫進 `state/*.log`**
   （`*.log` 已在 `.gitignore`，不會跨機同步造成雜訊），不要寫進 `AGENTS.md`／`SOUL.md`／
   `HEARTBEAT.md`／`MEMORY.md` 這些 bootstrap 檔。
2. **定期用 `wc -c` 檢查這幾個檔案字數**，接近或超過 2 萬字就要瘦身：找出佔比最大的段落
   搬去 `handoff_archive/` 或 `distill/`，原檔先備份再覆寫，寫完用 python
   `open(f,'rb').read().decode('utf-8')` 驗證沒有拋錯（沒有殘留亂碼）。
3. **`Get-Content -Tail N` / `tail -N` 這類「最近N行」的hook注入邏輯只是treat symptom**——
   就算只注入最後 50 行給教練看，檔案本體還是會超過 2 萬字被小龍蝦自己的 bootstrap 讀取截斷，
   兩件事要分開處理。

## 相關
- 試金石案例83（軍師自己的自動化拖垮小龍蝦的完整事故）
- [[reference_openclaw2_heartbeat_message_failed_bug_2026-09-14]]（同一場事故的另一半根因：心跳排程重開機復活）
