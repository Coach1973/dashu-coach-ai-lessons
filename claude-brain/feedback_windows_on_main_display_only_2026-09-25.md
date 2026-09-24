---
name: feedback-windows-on-main-display-only-2026-09-25
description: 教練Mac接了第二台螢幕(1280x720，系統標示Wokyis)但從不使用、一直關著；AI開任何視窗都要搬到主螢幕(1920x1080)並截圖確認，不能只看process有沒有在跑就說「已經跳出來了」
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7dfd3491-32da-49ec-be24-a2c0d54e850c
  modified: 2026-09-24T20:01:17.285Z
---

教練的 Mac 有兩台螢幕：主螢幕 1920×1080（有桌面，教練在用）、第二台 1280×720（`system_profiler` 顯示 Online，computer-use 標示為「Wokyis」，教練說「沒有在用，而且一直都是關閉的狀態」）。macOS 仍把第二台當成開著，所以 `open` 開出來的視窗可能落在那台，教練完全看不到。

**Why:** 2026-09-25 我用 `open` 開系統設定→登入項目，只確認 process 在跑就說「已經跳出來了」，教練兩次說沒看到，還要求「截張圖來證明」。實際上視窗開在第二台螢幕。這是「工具說 OK 不算，親眼看過才算」（執行細則 N4）的又一次違反。

**教練不拔線的原因**：那台是擴充塢附的螢幕，上面接著 953GB SSD 跟很多連接埠，絕對不能叫教練拔線、也不要叫他去系統設定改（教練：「你就簡單幫我解決問題，不要把問題丟回來給我」）。副螢幕在主螢幕左邊（x -1280~0）。

**查證（2026-09-25）：螢幕設定沒有跑掉**。教練以為「之前設定過、今天跑掉」。用 Time Machine 本機快照（02:05，登出前）比對 `/Library/Preferences/com.apple.windowserver.displays.plist`，跟登入後完全一樣：Wokyis 至少從 9/21 07:36（那次登出登入）起就一直是延伸螢幕、排在 HP 左邊。系統紀錄（最早到 9/15）只有 9/21、9/25 兩次登入時偵測到 Wokyis；9/11 後沒重開機，6/16 後沒系統更新。今天會「跑出來」是因為我用 `open` 開的系統設定視窗落在那台上，不是設定壞了。9/21 以前的狀態沒有紀錄可查。

**已有自動機制（2026-09-25 裝好並實測）**：PostToolUse hook `scripts/main_display_guard_hook.sh` —— Bash 指令含 `open`／`osascript`、Edit/Write 改 .html（會自動開 Chrome）、computer-use `open_application` 之後，背景 2 秒、5 秒各跑一次 `scripts/move_windows_to_main_display.sh`，把副螢幕上的視窗全部搬回主螢幕，有搬才寫 `logs/main_display_guard.log`。手動掃：`move_windows_to_main_display.sh [--dry-run]`。

**How to apply:**
- 要給教練看的視窗，還是要用 `app_list_windows`（bounds x 在 0~1920）或截圖親眼確認，才說「跳出來了」。
- 如果教練又說沒看到，先查 log 跟 hook 有沒有註冊（開工的 `audit_claude_hooks_registered.sh` 會檢查），不要叫教練動手。
- 相關：[[feedback_screenshot_rules_consolidated]]、[[feedback_hermes_gateway_vs_desktop_app_distinction_2026-09-19]]
