---
name: project_discord_bot_claude_tezhu_pending_openclaw_2026-10-16
description: Discord 機器人「Claude特助」已建好、在榮樹下伺服器，但官方 Claude Code Channels 對教練帳號被 Anthropic 旗標關著；下一步改接小龍蝦 OpenClaw（尚未做）
metadata:
  type: project
---
2026-10-16 夜，教練要「把 Claude 串進 Discord」，在教練的 Chrome 做完（Chrome 才是教練看得到的瀏覽器，不是內建窗格）：
- Discord 應用程式「Claude特助」ID `1560673837568233532`；伺服器「榮樹下」ID `1560663537527820298`（擁有者＝教練 `1560659588297130046`，帳號 dashujiaolian_43576）；Message Content Intent 已開；機器人已在伺服器內（API 驗證）。
- 金鑰在 `~/.claude/channels/discord/.env`（600）與 `路徑大全_憑證層.md` 的 Discord 段（git 忽略）。外掛 `discord@claude-plugins-official` v0.0.4 已裝（user scope），`~/.claude/channels/discord/access.json` 已寫成 allowlist 只有教練。
- **卡點**：`claude --channels plugin:discord@claude-plugins-official` 顯示「Channels are not currently available」。查 Claude Code 2.1.278 程式：閘門是 `P("tengu_harbor", false)`＝Anthropic 伺服器端旗標，依帳號逐步開放；拿掉桌面版環境變數重試結果相同。教練朋友能接＝他的帳號被開了旗標，教練機器上無法改。
- 教練同意改走小龍蝦（OpenClaw 2026.9.4 原生支援 Discord）：「如果是的話，那你就做吧」，**尚未動手**。

**How to apply（新對話框第一件事）：** ①備份 `~/.openclaw/openclaw.json` ②用腳本從 `.env` 讀金鑰，`openclaw channels add --channel discord --token …`（金鑰不要貼出來）③只允許教練 user ID 私訊、伺服器頻道先不開；`openclaw config validate` ④重啟閘道、確認 Telegram／LINE 沒壞 ⑤請教練私訊機器人實測。⑥注意：小龍蝦目前能用的腦只有 minimax/MiniMax-M3；aiprimetech 的 Claude 金鑰 2026-10-16 實測 401 INVALID_API_KEY，憑證層寫「使用中」已過時，要告訴教練並修正。⑦同一把金鑰不要同時給 Claude Code 外掛與 OpenClaw 兩邊跑。等 Anthropic 開旗標後，才改用 `--channels`。

相關：[[feedback_coach_pastes_credentials_on_purpose_2026-10-16]]、[[reference_mac_downloads_on_external_ssd_2026-10-02]]
