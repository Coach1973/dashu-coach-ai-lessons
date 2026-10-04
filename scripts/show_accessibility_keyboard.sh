#!/bin/bash
# 教練說「輔助鍵盤／輔助使用鍵盤」→ 把螢幕上的虛擬鍵盤叫出來（用滑鼠點字母，不經實體鍵盤）
# 教練習慣縮到最小（螢幕上一個小方塊），按叉才會消失。已在螢幕上就什麼都不動。
has_panel() { osascript -e 'tell application "System Events" to tell process "Assistive Control" to get count of windows' 2>/dev/null | grep -qE '^[1-9]'; }
if has_panel; then echo "輔助使用鍵盤已在螢幕上（縮小的小方塊，點一下展開）"; exit 0; fi
defaults write com.apple.universalaccess virtualKeyboardOnOff -bool true
killall "Assistive Control" 2>/dev/null
sleep 3
has_panel && echo "輔助使用鍵盤已叫出" || { echo "沒叫出來"; exit 1; }
