---
name: feedback-lock-must-be-hook-not-optin
description: 防呆「鎖」必須是攔截所有指令的 hook，不能是要 AI 自己呼叫的函式；且必須 verify 證明會擋——檔案存在≠鎖有效（2026-06-25 LINE 4GB 丟失血淚）
metadata:
  type: feedback
---

# 防呆鎖必須是 hook + 必須驗證會擋（案例 29，4GB 換來）

2026-06-25 聯想 LINE 重裝善後，AI 一條 `Remove-Item -Recurse -Force` 把 C/E 兩份 .bak 刪光，4GB 聊天記錄永久丟失（LINE 電腦版無雲端備份）。事後拆鎖發現：Windows 的「刪檔鎖」delete_guard.ps1 根本是 opt-in 函式 `Safe-Remove`，AI 直接打 Remove-Item 就完全繞過；而且從沒人驗證過鎖會擋。

**Why（教練親口）：** 「你寫的什麼程式鎖根本個屁用都沒有，資料還是被刪了！」——對。opt-in 的防呆 = 規矩 = 廢紙（案例 25 早講過又犯）。

**How to apply：**
1. **真機關的定義：AI「選擇不用它」也繞不過。** 只有 PreToolUse hook（攔截所有指令）做得到；函式庫 / 「請改用 XXX」的規矩做不到。
2. **「鎖的檔案存在」≠「鎖有效」。** 唯一憑證 = 餵一條假危險指令、親眼看它被擋（exit 2）。沒跑過 verify 自證 = 那台機器視同沒鎖。
3. 任何機器回報「裝了刪檔鎖」必須附 `verify_delete_guard` 全綠輸出（呼應 [[feedback_settings_hook_verify]] / [[feedback_hook_install_environment_verify]]）。
4. 重裝/刪除類善後：原始資料先複製到 AI 碰不到的獨立位置，.bak/.old 七天內不准刪。

機關：`scripts/delete_guard_hook.ps1`（真 hook）+ `scripts/verify_delete_guard.sh`/`.ps1`（自證）。完整見試金石案例 29 與 [[project_line_moved_to_e]]。
