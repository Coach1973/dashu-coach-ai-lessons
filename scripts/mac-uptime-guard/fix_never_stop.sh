#!/bin/bash
# Mac 永不停機根治腳本
# 建立：2026-07-01 軍師 Opus 4.7
# 起因：07-01 03:10 pmset repeat 觸發重啟 → 停在 login screen → 停工 16.5 小時
# 教練親口：「除非停電或停網，永遠不要再出現」

set -e
echo "🔧 Mac 永不停機根治開始..."
echo ""

echo "① 刪掉每週三凌晨 3:00 排程重啟（禍首）"
sudo pmset repeat cancel
echo "   ✅ 已取消"
echo ""

echo "② 斷電後自動重啟（停電恢復就自動醒）"
sudo pmset -a autorestart 1
echo "   ✅ 已設定"
echo ""

echo "③ 睡眠設定確認（sleep=0 已設，加固）"
sudo pmset -a sleep 0
sudo pmset -a disksleep 0
sudo pmset -a displaysleep 0
sudo pmset -a powernap 1
sudo pmset -a womp 1
sudo pmset -a standby 0
sudo pmset -a hibernatemode 0
echo "   ✅ 所有睡眠關閉"
echo ""

echo "④ 關閉 macOS 自動更新的自動重啟（不再半夜偷偷重啟）"
sudo softwareupdate --schedule off 2>/dev/null || true
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticallyInstallMacOSUpdates -bool false
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate CriticalUpdateInstall -bool false
echo "   ✅ 自動更新關閉（仍會下載，但不會自動安裝重啟）"
echo ""

echo "⑤ 啟用自動登入（萬一重啟，開機就進 user session）"
echo "   ⚠️ 需要輸入你的登入密碼"
sudo sysadminctl -autologin set -userName bymyway -password - 2>&1 || true
echo ""

echo "===== 最終驗證 ====="
echo ""
echo "▸ pmset 排程（應該顯示 No scheduled events.）："
pmset -g sched
echo ""
echo "▸ pmset 睡眠設定："
pmset -g custom | grep -E "sleep|autorestart|disksleep|powernap|womp"
echo ""
echo "▸ auto login 狀態："
sudo defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser 2>&1 || echo "  未設定"
echo ""
echo "✅ 完成！Mac 從此不會自己重啟。"
