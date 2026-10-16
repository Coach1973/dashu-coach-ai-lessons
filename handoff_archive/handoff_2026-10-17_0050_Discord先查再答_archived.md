## 🔴 給跨對話框軍師讀的總結摘要（2026-10-17 00:50 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Sonnet 5.5→Opus 5.5；教練說「總結」收工；本段 10/16 23:51～10/17 00:50，對話容量約 42%）

**主軸：Discord 機器人「龍蝦特助」兩種腦都通，平常用 MiniMax 省用量；教練要的「先查再答」標準已接進系統（每次提醒＋回話擋下）。收工前健康檢查 🟢 全部正常。**
- **Discord**：先接小龍蝦（金鑰不進 git，SecretRef 指到 `~/.claude/channels/discord/openclaw-secrets.json`；`plugins.allow` 要補 discord 否則一直 stopped；`d9d8e2c92`）→ 教練追問「為什麼朋友可以我不可以」→ 查本機 `cachedGrowthBookFeatures.tengu_harbor=true`、帳號個人 Pro、乾淨環境實測 Listening → 切真的 Claude（tmux `discord-claude`、資料夾 `~/claude-discord`），00:10 教練實測「確實是 Claude」→ 00:30 教練要省流量，切回 MiniMax（`c482276a2`）。換腦一行：`bash scripts/discord_brain_switch.sh minimax|claude|status`（Telegram／LINE 會斷約 20 秒）。機器人已改名「龍蝦特助」（開發者後台的應用程式名仍叫「Claude特助」）。細節在記憶 project_discord_bot_claude_tezhu_pending_openclaw_2026-10-16。
- **先查再答**（`80b8a1a80`）：反射 R-VERIFY-BEFORE-ANSWER（教練問原因／能不能／是不是／對嗎，每次都提醒；路由新增 `repeat`；歷史回測 4,092 句中 1,073 句觸發）；`stop_rules_master.py` E2（判斷題這輪 0 次查證就下結論→擋下要求補查，記錄在 `distill/rule03_verify_violations.log`）；24 項迴歸全過。極限：有用工具卻仍把推論講成結論，程式抓不到，靠「查到的／推論／沒查的」三分法。試金石125。
- **其他**：「BB＝MiniMax」反射＋語音對照（Claude 與小龍蝦都吃）；Hook 稽核紅字＝舊 `scripts/context_percent_hook.sh`，已拿掉宣告；Discord Claude 視窗容量算法與桌面版相同（開機即 8%，沒有新對話鈕，要重啟 tmux）。
- **教練原話線索**：「為什麼你都不能說「我先去了解一下真實情況」，不要著急回答我吧？」「這種反反覆覆，你不覺得很煩嗎？」「不是今天晚上而已，之前也多次發生過這種情況」→ 判斷題先查第一手證據，話分「查到的／推論／沒查的」，不夠就說「我先去了解」（三大信念一「真誠：說真話，辦真事，一切歸於真實。」）。「我現在還不確定我 Discord 要怎麼用，所以也不想浪費我的流量」→ 平常 MiniMax，要用才切 Claude。

### 📋 下一場開工先做（以本棒為準）
1. 🔧 看「先查再答」E2 有沒有誤擋：`grep -A2 "E2 判斷題零查證" distill/rule03_verify_violations.log`；誤擋就改反射索引 R-VERIFY-BEFORE-ANSWER 的 match（E2 讀同一條）。
2. 🔧 修憑證層「Claude（主力 UNLIMITED）」過時（aiprimetech 金鑰 401）：先查有沒有換過金鑰；查不到就放 🤫（只有教練能給新金鑰）。
3. 承接新一棒 📋 第 2 項（19:45 棒的清單已併入、該棒已封存）。

🙋 要教練決定：軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）｜問過：2026-10-15 企劃書內
🤫 等教練自己提起：（「榮樹下」伺服器頻道已於 01:19 開通並經教練實測，本項移出）；其餘見新一棒 🤫 清單。

---


