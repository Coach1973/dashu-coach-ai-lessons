---
name: project_discord_bot_claude_tezhu_pending_openclaw_2026-10-16
description: Discord 機器人「龍蝦特助」已切成真的 Claude（Mac 上 tmux 視窗 discord-claude 常駐，2026-10-17 00:10 教練實測確認）；「官方 --channels 被旗標關著」的舊結論作廢；小龍蝦 Discord 暫停當備援；怎麼重啟、怎麼退回、容量怎麼算
metadata:
  type: project
---
2026-10-16 夜～10-17 凌晨，教練要「把 Claude 串進 Discord」，全程在教練的 Chrome 做（Chrome 才是教練看得到的瀏覽器，不是內建窗格）。

**現況（10/17 00:10 教練實測：Discord 有回，確實是 Claude）**
- Discord 應用程式 ID `1560673837568233532`（開發者後台的應用程式名稱仍叫「Claude特助」）；機器人顯示名 **10/17 00:02 已改「龍蝦特助」**（用機器人自己的金鑰 `PATCH /users/@me`，教練問「我可以改他的名字嗎」後指定）；伺服器「榮樹下」ID `1560663537527820298`；教練 Discord ID `1560659588297130046`（帳號 dashujiaolian_43576）；Message Content Intent 已開。
- **常駐方式**：tmux 視窗 `discord-claude`，工作資料夾 `~/claude-discord`（內有 `CLAUDE.md` 與 `.claude/settings.json`，後者預先核准 5 個 Discord 工具 reply／react／edit_message／fetch_messages／download_attachment）。啟動指令：`tmux new-session -d -s discord-claude -c ~/claude-discord "env -i HOME=$HOME USER=$USER LOGNAME=$USER PATH=$PATH TERM=xterm-256color LANG=en_US.UTF-8 claude --channels plugin:discord@claude-plugins-official"`；第一次會問「信任資料夾」，用 `tmux send-keys -t discord-claude Down Enter` 選信任。**env -i 一定要留 USER／LOGNAME，否則鑰匙圈讀不到登入，會顯示 Not logged in。**
- 檢查：`tmux capture-pane -t discord-claude -p`；在視窗打 `/status` 要看到 `Channels: Listening for messages from plugin:discord@claude-plugins-official`；`/context` 看容量。首次啟動時 Claude Code 自動從 2.1.278 升到 2.1.301。模型 Sonnet 5（Pro 帳號，用教練的 Pro 用量）。
- 需要核准的動作（改檔、跑指令）：外掛會把權限按鈕傳到教練的 Discord 私訊，教練按核准。只有 `access.json` 白名單裡的教練能傳訊息。
- 限制：Mac 重開機／登出、tmux 被關掉，機器人就不回；**沒有做開機自動啟動**（10/16 的 launchd 設定檔消失事件還沒收尾，先不增加）。
- **備援＝小龍蝦的 Discord 頻道（回話的腦是 MiniMax-M3，不是 Claude）**：`openclaw.json` 的 `channels.discord`（commit `d9d8e2c92` 加入、`c1427db72` 暫停 `enabled:false`）。要退回：先 `tmux kill-session -t discord-claude`，再 `openclaw config patch` 把 `channels.discord.enabled` 設 `true`、`openclaw gateway restart`。**兩邊不能同時開（同一把金鑰會雙重回覆）。** 小龍蝦那邊的金鑰用 SecretRef（file provider `discordfile`）指向 `~/.claude/channels/discord/openclaw-secrets.json`（600，不進 git）；金鑰在 Discord 後台重設時，`.env` 與 `openclaw-secrets.json` 兩處都要改。備份在 `~/.openclaw/backups_manual/openclaw.json.before_discord_20261016`、`…before_claude_switch_20261017`。

**根因更正（舊結論作廢）：** 前一場說「Anthropic 的 `tengu_harbor` 旗標對教練帳號關著」是沒查到底的推論。10/17 00:02 實測：`~/.claude.json` 的 `cachedGrowthBookFeatures.tengu_harbor = true`，`tengu_harbor_ledger` 核准清單含 discord；教練帳號是**個人 Pro**（organizationType claude_pro、角色 admin），官方文件寫個人 Pro／Max 不用任何審核；乾淨環境實測通過閘門，畫面顯示 Listening。旗標是依帳號逐步開放、本機快取最久約 6 小時才更新，前一場（約 23:30）失敗時的值不同，確切何時翻成 true 查不出來，**不要再說「被關著」**。若再看到 `Channels are not currently available`：先看 `cachedGrowthBookFeatures.tengu_harbor`，再開任何新的 claude 讓快取更新，然後在乾淨環境重測。教練朋友的設定沒看過，推論是同一個逐步開放的機制。

**容量（教練 00:12 問）：** Discord 視窗是**一個持續的對話**，所有訊息累積在同一個脈絡。算法與桌面版相同（同一份 `~/.claude/settings.json`：視窗 1,000,000、`CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000`）；開機固定開銷約 55k（系統提示 9.3k＋工具 20.8k＋記憶檔 13.9k＋技能 8.1k…），剛啟動就顯示 8%（`/context`：75.1k/1m）。全域 UserPromptSubmit hook 在 Discord 訊息也會觸發（交易紀錄已確認），所以「約 X%」提醒與 30/35/40/45/50% 提醒理應也會到 Discord 視窗（尚未等到第 5 句實證）。接近上限會自動壓縮；教練習慣 30% 準備、40% 開新對話。**Discord 沒有「新對話」按鈕**：目前做法是重啟 tmux 視窗（上面啟動指令）；「在 Discord 說新對話就自動重開」尚未做，教練決定要不要。

**Why:** 教練要在 Discord 直接跟 Claude 說話，朋友已能做，教練曾被我錯誤告知「帳號被關」。
**How to apply:** 教練問 Discord 沒回 → 先 `tmux ls`、`tmux capture-pane -t discord-claude -p` 看視窗是否活著、有無卡在權限提示；問為何回話不像 Claude → 看是不是退回備援。其他待辦：aiprimetech 的 Claude 線金鑰 401（只有教練能給新金鑰，放 🤫）。

相關：[[feedback_coach_pastes_credentials_on_purpose_2026-10-16]]、[[reference_mac_downloads_on_external_ssd_2026-10-02]]、[[reference_context_percent_reminder_hook_2026-10-14]]
