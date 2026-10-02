---
name: feedback-open-settings-to-exact-spot-only-password-left-2026-10-02
description: 只有教練能做的步驟（密碼、系統設定）也不准列「設定 → A → B」叫教練找；AI 先打開到那一格、要 sudo 的放 App 終端機分頁停在輸入密碼，教練只打密碼
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9df2876c-7681-432c-88e0-2fa87d0e2702
  modified: 2026-10-02T03:29:01.768Z
---

教練 2026-10-02 11:12 原話：「每次看到這個就麻煩，我希望的是直接幫我開到備份頻率，甚至選好手動，只留我輸密碼，這才叫真的省事，不然我光是找你講的這些步驟，就花不少時間。」

起因：我寫「只剩一步只有您能做：到系統設定 → 時光機 → 選項，把備份頻率改成手動」。舊的守則#12 檢查看到「只有您能做＋密碼」就放行，所以沒擋。

**Why:** 「只有教練能做」只代表最後那一下（打密碼、按允許）是他的；找畫面、點進去、開好指令，都是 AI 能做的搬運。叫他自己照路徑找，等於把工作丟回去（守則#12）。

**How to apply:**
- 系統設定：`open 'x-apple.systempreferences:<面板代號>'` 直接打開（時光機＝`com.apple.Time-Machine-Settings.extension`；代號查 `/System/Library/ExtensionKit/Extensions/*.appex` 的 CFBundleIdentifier）。
- 要管理員權限的指令：**用跳到畫面最前面的密碼視窗**：`SUDO_ASKPASS=~/.openclaw/workspace/scripts/coach_password_dialog.sh COACH_PW_MSG='要做什麼' sudo -A <指令>`（Bash 工具背景跑）。10/02 實測：App 終端機面板（run_in_terminal＋show_pane）教練兩次都說看不到；這個視窗教練一看到就輸入成功。多件事合成一支腳本，只輸入一次密碼。osascript 的 administrator privileges 視窗會失去完整磁碟取用，tmutil 看不到備份，別用。
- 回覆寫「我已經打開到 X，只剩輸入密碼」，不列路徑。
- 機制：反射 `R-SUDO-SHOW-TERMINAL`（下 sudo 沒帶 -A 就提醒改用密碼視窗）；`scripts/stop_rules_master.py` A2b（回覆有「設定 → A → B」兩段箭頭、卻沒寫「已幫您打開」就擋；回測 2461 則歷史回覆命中 6 則，全是真的）。

相關：[[feedback_dont_ask_obvious_yes_and_never_hand_commands_2026-09-30]]、[[feedback_remote_connect_do_it_for_coach_no_jargon_2026-10-01]]
