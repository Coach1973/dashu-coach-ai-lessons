---
name: reference_dock_extra_app_icons_are_recent_apps_2026-10-23
description: Dock 上同一個 App（例如 Chrome）圖示變多個＝多半是 Dock「最近使用」區記了好幾筆，不是真的開了好幾個程式；怎麼查、怎麼讓它消失、哪些開法已測過不會增加
metadata:
  node_type: memory
  type: reference
  originSessionId: 0d9a0596-c5e4-4098-a53c-c959434a309a
  modified: 2026-10-22T22:24:30.015Z
---

2026-10-23 教練抱怨「你幫我開網頁，每開一次 Dock 就多一個 Chrome 圖示」。

**查到的（有指令輸出為證）**
- Dock 實際有 4 個「Google Chrome」：1 個釘著、3 個在分隔線後（`osascript -e 'tell application "System Events" to tell process "Dock" to return name of every UI element of list 1'`）。
- 系統只登記 1 個前景 Chrome（`lsappinfo list`，只有 pid 98526 是 Foreground）；`ps` 也只有 1 個 Chrome 主程序；重啟 Dock（`killall Dock`）後仍 4 個 → 不是殘影。
- `defaults read com.apple.dock recent-apps` 裡有 3 筆 `com.google.Chrome`（路徑都是 /Applications/Google Chrome.app）→ 多出的 3 個就是「最近使用」區。`show-recents` 沒設定過＝預設開著。
- 已實測「不會」增加 Dock 圖示：`open -a "Google Chrome" <網址>`（deliver_open.sh 用的）、`Chrome --headless=new` 加臨時設定檔截圖、除錯用 `start_debug_chrome.sh`（系統登記成 BackgroundOnly）。
- 教練自己關掉系統設定的「在Dock中顯示建議的和最近使用過的App」後，Dock 的 Chrome 圖示 4→1。

**沒查出的**：為什麼 Chrome 會被記進最近使用 3 次（我的推論：每次 Chrome 被重新啟動記一筆，未證實）。

**怎麼辦**：同類問題（Dock 同一 App 圖示重複）先看 `recent-apps`；解法是關掉上面那個開關。這是系統設定，我不能代按，但要把設定頁開好、導到位置、讀出開關位置，只留最後一下給教練（`open "x-apple.systempreferences:com.apple.Desktop-Settings.extension"` 開「桌面與 Dock」，視窗名稱「桌面與Dock」）；不准丟「系統設定 → …」路徑叫他自己找，見 [[feedback_dont_ask_obvious_yes_and_never_hand_commands_2026-09-30]]。

附：教練設有截圖鎖（`state/SCREENSHOT_APPROVED`，沒同意不能截圖）與內建瀏覽器鎖（外部網站要用 claude-in-chrome），查畫面狀態改用 AppleScript／AX 讀取，不要自己解鎖。
