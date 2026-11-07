---
name: reference_phone_claude_rc_dies_on_reboot_autostart_2026-11-03
description: 教練手機連不上 Claude＝Mac 重開機後 tmux 裡的 claude rc 沒回來；11/03 加開機自動啟動 com.coach.claude-remote-control；重啟中的 rc 會被雲端記號擋「already served」約3分鐘
metadata:
  node_type: memory
  type: reference
  originSessionId: 8f583093-6086-42e2-8bfa-75232ec6f5d3
  modified: 2026-11-07T04:22:32.669Z
---

**症狀**：教練出門用手機連不上 Claude（Claude App／claude.ai/code 看不到 Mac）。

**11/03 根因（查到的）**：Mac 在 11/02 01:41 重開機（`sysctl kern.boottime`），手機那條路是 tmux session `remote-control` 裡的 `claude rc`，重開機就沒了，之前沒有任何開機自動啟動。Mac 本身醒著、網路通、Claude App 在跑都不是問題。
- 桌面 App 的 `~/Library/Logs/Claude/remote-control.log` 從 10/17 起一直是 off／polls:0，那是桌面 App 自己的「讓這台 Mac 可被遠端使用」，**不是**教練用的那條，別被它誤導。

**修法**：
- 立刻恢復：`bash ~/.openclaw/workspace/scripts/restart_remote_control.sh`，看到 `✅ Remote Control 已成功啟動並連線`。
- 防再犯：`~/Library/LaunchAgents/com.coach.claude-remote-control.plist`（RunAtLoad、不 KeepAlive、不輪詢；log 在 `~/.openclaw/logs/claude_remote_control_boot.log`）。登入時跑上面那支腳本。launchd 環境下 tmux＋claude rc 實測會啟動（14:04:29 那次有跑到 claude）。
- **坑**：rc 正在跑時再重啟（腳本會先殺 tmux），雲端還記著舊連線，新的會報 `This folder is already served by a terminal claude remote-control on this device`，本機找不到任何鎖檔；**等約 3 分鐘再跑就好**（14:04 撞到、14:07:59 成功）。所以不要拿 `launchctl kickstart` 去「測試」正在連線的 rc。
- 腳本「等舊 rc 真的退出」的改良沒改成（worktree 對話 Edit 被 hook 擋），記在 AI 自己的清單。

**11/07 第二次發生（查到的）**：11/06 12:24 重開機，開機自啟有跑，但撞 already served，v4 腳本直接 exit 1，tmux 空殼留著、rc 沒起來，教練手機一整天只看到雲端。11/07 12:2x 手動重跑一次就 Connected。腳本已改 v5：撞 already served 每 60 秒重試、最多 6 次（commit 2194e5cb0）。v5 重試那段還沒在真的重開機時驗證過。手機只看到「雲端」、看不到 Mac＝先查 `tmux capture-pane -t remote-control -p` 有沒有 Connected。

**沒驗證**：真的重開機一次看會不會自己連上；教練手機端實際連入。

相關：[[reference_claude_desktop_worktree_quota_2026-10-26]] [[reference_launchagents_plists_deleted_outage_2026-10-16]]
