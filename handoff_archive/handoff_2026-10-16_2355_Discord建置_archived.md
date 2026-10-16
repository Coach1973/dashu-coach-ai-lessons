## 🔴 給跨對話框軍師讀的總結摘要（2026-10-16 23:55 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Sonnet 5.5；教練說「總結」收工；本段 20:14～23:55，對話容量約 37%）

**主軸：教練要把 Claude 串進 Discord。機器人建好了、在教練的伺服器裡，但「接上 Claude」沒成功（Anthropic 對教練帳號的功能旗標關著）；下一步改接小龍蝦，尚未動手。同一晚被教練當場糾正兩個低級錯，都已從源頭修掉。**
- **Discord 已做好**（全在教練的 Chrome 操作；教練本人輸了密碼、點了授權）：應用程式「Claude特助」ID `1560673837568233532`、伺服器「榮樹下」ID `1560663537527820298`（擁有者＝教練 `1560659588297130046`）、Message Content Intent 已開、機器人已在伺服器內（API 驗證）。金鑰在 `~/.claude/channels/discord/.env`（600）與 `路徑大全_憑證層.md` 的 Discord 段（git 忽略，驗證有效）。Bun 1.4.3 已裝；外掛 `discord@claude-plugins-official` v0.0.4 已裝；`access.json` 已寫成只有教練可私訊。
- **卡點**：`claude --channels plugin:discord@claude-plugins-official` 顯示「Channels are not currently available」。查 Claude Code 2.1.278 程式碼：閘門是 `P("tengu_harbor", false)`＝Anthropic 伺服器端、依帳號逐步開放的旗標；拿掉桌面版環境變數重試結果相同，教練電腦上改不了。教練朋友能接＝他的帳號被開了旗標（推論，沒看到朋友設定）。
- **小龍蝦路（教練 23:35「如果是的話，那你就做吧」，尚未動手）**：OpenClaw 2026.9.4 原生支援 Discord（`openclaw channels add --channel discord`）。查到：所有 agent 的腦都是 `minimax/MiniMax-M3`；aiprimetech 的 Claude 線金鑰實測 401 INVALID_API_KEY，憑證層寫「使用中」已過時。已向教練說明「回話的會是 MiniMax，不是 Claude」，教練沒有反對。
- **被糾正的兩個低級錯（試金石124）**：①下載資料夾是指向外接 SSD 的捷徑，反射提示寫 `ls ~/Downloads` 看不到圖→改反射 `55465d9d8`；②用了教練看不到的內建瀏覽器窗格→新反射 R-BUILTIN-BROWSER-EXTERNAL-BLOCK（擋下，通行證 `state/BUILTIN_BROWSER_APPROVED` 10 分鐘）、路由器支援 `unless_fresh_file`、settings.json PreToolUse 觸發範圍加 `mcp__Claude_Browser__.*`，`30c573f7f`，真實呼叫被擋已驗證。
- **金鑰防護**：教練貼的金鑰曾被 `log_junshi_activity_to_echo.sh` 寫進 `state/inbound_echo`（會被自動同步推上 GitHub）→已遮掉並讓程式寫入前自動遮蔽 Discord／Telegram／sk-／GitHub 金鑰 `c8076a774`；新反射 R-COACH-PASTED-CREDENTIAL `b829cdd59`；記憶 feedback_coach_pastes_credentials_on_purpose／project_discord_bot_claude_tezhu_pending_openclaw `3444a1d99`。
- **教練原話線索**：「我是一定要把金鑰貼給你…你自己去做好防護，就不要再來煩我了」→貼密碼是刻意的，收進憑證層、做防護、一句話回報；「為什麼你思考了這麼久？…我什麼都不知道，也看不到」→長時間做事要主動簡短報進度；「我一直都在使用chrome且登入好了，你怎麼不用呢」→網頁操作預設用教練的 Chrome（先 list_connected_browsers 確認 Mac 本機）；「超過 30% 就要開始準備，差不多 40% 就要開新對話框」→主動看容量。

### 📋 下一場開工先做（以本棒為準）
1. **Discord 改接小龍蝦**（完整步驟在記憶 project_discord_bot_claude_tezhu_pending_openclaw_2026-10-16）：備份 `~/.openclaw/openclaw.json` → `openclaw channels add --channel discord`（金鑰用腳本從 `.env` 讀、不貼出來）→ 只允許教練 ID 私訊、伺服器頻道先不開 → `openclaw config validate` → 重啟閘道 → 確認 Telegram／LINE 沒壞 → 請教練私訊機器人實測。回報要講清楚：回話的是 MiniMax-M3，不是 Claude。同一把金鑰不要同時給 Claude Code 外掛與 OpenClaw。
2. 🔧 修憑證層「Claude（主力 UNLIMITED）」過時（aiprimetech 金鑰 401）：先查有沒有換過金鑰；查不到就放 🤫（只有教練能給新金鑰）。
3. 🔧 查新工作資料夾啟動時 SessionStart 紅字「Hook稽核：宣告是hook但沒註冊進settings.json的腳本」是哪一支（`scripts/audit_claude_hooks_registered.sh`）。
4. 承接上一棒（下方 19:45 棒）：軍火庫設計稿教練回應後照做、志工頁 `JOINED`、下次登入看 `launchagents_guard.log`、gateway `providers.nvidia.models[17].input` 驗證錯誤等。

🙋 要教練決定：軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）｜問過：2026-10-15 企劃書內
🤫 等教練自己提起：朋友的 Discord 用哪種方法接 Claude；Claude 線（aiprimetech）新金鑰；等 Anthropic 開 tengu_harbor 後改用官方 `--channels`（一行指令即通）；及下方 19:45 棒的 🤫 清單。

