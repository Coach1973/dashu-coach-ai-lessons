---
name: reference-accessibility-keyboard-trigger-2026-10-04
description: 教練說「輔助鍵盤／輔助使用鍵盤」＝跑 scripts/show_accessibility_keyboard.sh 把螢幕虛擬鍵盤叫出來（教練實體鍵盤 E、M 常打不出，密碼靠點螢幕鍵盤或複製貼上）
metadata:
  node_type: memory
  type: reference
  originSessionId: 0376f33d-338c-47b4-bc98-224fc7e01b30
---

教練 2026-10-04 15:09 要求：只要他說「輔助鍵盤」或「輔助使用鍵盤」，AI 直接把 macOS 輔助使用鍵盤叫出來，不要問、不要叫他去設定裡找。

- 指令：`/Users/bymyway/.openclaw/workspace/scripts/show_accessibility_keyboard.sh`
- 教練習慣把它縮到最小（螢幕上一個小方塊，約 70x62），按叉才會消失。腳本先看 Assistive Control 程序有沒有視窗：有＝已在螢幕上，不動；沒有＝`defaults write com.apple.universalaccess virtualKeyboardOnOff -bool true` ＋ `killall "Assistive Control"` 重啟。
- 驗證狀態：「已在螢幕上」分支實跑過；「被叉掉後叫回」分支只觀察到重啟後 Panel 視窗出現，沒有從關閉狀態完整測過（教練說不用測，怕干擾）。
- 走過的死路：用 AppleScript 點系統設定的開關，第二次起讀不到元素；`screencapture` 會跳螢幕錄製授權窗，不要用。
- 背景：教練實體鍵盤 E、M 常打不出（原因未確認，Typeless 設定沒綁 E、M，輸入法是 ABC）；AI 不能代輸入密碼，教練用螢幕鍵盤或複製貼上。

**Why:** 教練不想每次都自己去系統設定找。
**How to apply:** 聽到「輔助鍵盤」→ 跑腳本 → 一行回報「已叫出／已在螢幕上」。
