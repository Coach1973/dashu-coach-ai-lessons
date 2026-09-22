---
name: reference-claude-code-remote-control-setup-sop-2026-09-17
description: Claude Code Remote Control在這台Mac的完整可行SOP+四道卡關與修法，教練人在外面時用手機/claude.ai/code直接操控這台Mac的正式解法
metadata:
  type: reference
---

# Claude Code Remote Control：這台Mac的完整可行SOP（2026-09-17首次跑通）

## 背景

教練人在外面時，手機版Claude只能讀雲端資料、無法操控Mac；小龍蝦派工機制(`junshi_dispatch_worker.py`)只能做3種預設唯讀查詢，且要等有人在Mac喊「開工」才會執行，不是即時。Anthropic官方2026年2月推出的「Remote Control」功能才是真正解法：手機/claude.ai/code直接連上這台Mac本機正在跑的Claude Code session，session本身留在本機（fs/exec/git權限完整），手機只是遠端窗口，可以雙向下指令、批准權限請求。

## 正確指令（不是網路文章猜的那幾種）

```bash
claude rc
```

**必須在乾淨的shell提示字元下執行**（`%`結尾那種，不是Claude對話裡的`❯`提示字元），不能打在已經進入的Claude對話裡當成一句話送出，也不是`/remote-control`斜線指令、也不是`--remote-control`當成啟動旗標（這幾種都在這台機器實測失敗過）。

## 四道卡關+修法（照順序會依次跳出，逐一解決）

這台機器因為「軍師」平常為了省錢，透過`~/.claude/settings.json`的`env`區塊把整個Claude Code CLI導去MiniMax API，這四道卡關全部跟這個設定有關：

1. **CLI版本太舊**：`claude --version`確認版本，舊版可能連`/remote-control`指令字串都還沒收錄。`claude update`更新到最新版。
2. **`Error: You must be logged in to use Remote Control`**：這台終端機是用API key在跑，不是claude.ai帳號登入。解法：`claude` 進session → `/login` → 選「1. Claude account with subscription」→瀏覽器完成OAuth。**必須是Pro/Max/Team/Enterprise訂閱帳號，API key或Console帳單帳號都不算**。
3. **`Error: ...ANTHROPIC_BASE_URL is set and does not point at api.anthropic.com`** + **`Error: ...ANTHROPIC_API_KEY is set`**：根因是`~/.claude/settings.json`的`env`區塊寫死`ANTHROPIC_BASE_URL`(指向MiniMax)+`ANTHROPIC_API_KEY`+`ANTHROPIC_AUTH_TOKEN`——**這是全域設定檔，在shell層級`unset`完全沒用，因為Claude Code每次啟動都會重新從這個檔案注入**。解法：直接編輯`~/.claude/settings.json`，暫時移除這4個key（`ANTHROPIC_BASE_URL`/`ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`/`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`，第4個是下一關）。
4. **`Error: ...CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC is set`**：這個變數本體藏在`~/.zshrc`第36行的`export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`，跟settings.json是兩個獨立來源，settings.json修好了這關還是會卡。解法：**這個可以單純用shell層級`unset CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`解決**（不用動`.zshrc`本身），因為這個特定變數在settings.json裡的複本已經清掉，剩下`.zshrc`匯出的那份可以直接`unset`蓋掉。

四關全過後`claude rc`會問：
- `Enable Remote Control? (y/n)` → `y`
- `Spawn mode: [1] same-dir [2] worktree` → 選**1（預設）**，跟平常操作習慣一致

成功後終端機顯示「Connected」，手機Claude App的「Code」分頁會即時出現這台Mac的session，直接點進去操控。**終端機視窗不能關，關掉=斷線**（App畫面本身寫"Press Ctrl+C to stop"）。

## 收工後的設定檔復原

Remote Control連線成功後，session的環境變數已經在process啟動當下固定，**可以放心把`~/.claude/settings.json`改回原本MiniMax設定**，不會影響已連線的session（env var不是process啟動後還會被檔案變動即時覆寫的東西）。`.zshrc`那行沒有動過，維持原樣。

## 下次直接可用的懶人包（教練或其他機器要重跑這套SOP時）

```bash
# 1. 確認版本夠新
claude update

# 2. 進session登入claude.ai帳號（只需做一次，登入後會記住）
claude
/login    # 選 1. Claude account with subscription

# 3. /exit 退出，回到 % 提示字元

# 4. 檢查 ~/.claude/settings.json 的 env 區塊有沒有 ANTHROPIC_BASE_URL /
#    ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN / CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC，
#    有就暫時移除（備份原檔）

# 5. 同一個 % 畫面：
unset CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC
claude rc
# y → 1（same-dir）→ 完成

# 6. 手機開Claude App「Code」分頁應該看得到這個session

# 7. 復原 settings.json（可選，不影響已連線的session）
```

## Why（這條記憶的核心價值）

這解決了教練最根本的痛點：**「非得坐在電腦前才能用AI」完全違反Jarvis理念**。Remote Control是Anthropic官方給的正解，不是小龍蝦派工那種要等「開工」觸發、只能做3種預設查詢的間接方案——連上之後就是這台Mac本機的完整session，跟坐在電腦前操作沒有本質差異。

## How to apply

教練往後只要人在外面需要操作Mac，先確認Remote Control連線還在（終端機視窗有沒有還開著），沒有的話照上面懶人包重跑一次即可，全程約2分鐘（多數情況四關都已經解過，只剩`claude rc`+`y`+`1`三個動作）。

## 相關

- [[feedback_check_global_config_before_shell_level_fix_2026-09-17]]（這次繞遠路的診斷教訓）

## 🔴 2026-09-17 03:41 追加：改用tmux背景session，關終端機視窗不再斷線

**起因**：教練照SOP連上後，聽軍師說「設定檔可以放心改回去」就順手把終端機視窗也關了——連線斷了，教練當場動怒（合理，是軍師沒把「設定檔」跟「視窗」講清楚分開）。教練授權軍師自行嘗試把連線改成放進`tmux`背景session，這樣關視窗不會再斷線。

**做法**：
```bash
tmux new-session -d -s remote-control -c ~/.openclaw
tmux send-keys -t remote-control "env -u CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC claude rc" Enter
```
（暫時清空`~/.claude/settings.json`的4個卡點設定，跑完再還原，做法跟前面章節一致）

**結果**：tmux session名稱`remote-control`，內含process「claude rc」(PID視每次啟動而定，父行程是tmux pane)，畫面顯示：
```
·✔︎· Ready · mac-openclaw-workflows · master
Code anywhere with the Claude mobile app or https://claude.ai/code?environment=env_01WK5Qo84HdaxXo5WxirnAi5
```
這個狀態畫面看起來跟教練稍早手機端確認成功那次一致（有Ready標示+environment URL），判斷是成功連線。

**⚠️ 誠實記錄一個尚未100%排除的殘留警告**：啟動log裡出現過：
```
Session failed: claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set and takes precedence over your claude.ai login
Couldn't verify your organization's policy for remote control. Check your network connection and try again.
```
用`ps eww -p <claude rc PID>`直接查這個process本身的環境變數，確認`ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`(MiniMax金鑰值)**仍然存在**——即使settings.json已經在啟動前清空，process執行後這兩個值還是出現了，懷疑Claude Code CLI有自己的憑證解析順序(env→settings.json→macOS Keychain「Claude Code-credentials」條目→...)，Keychain裡可能也存了一份同樣的MiniMax憑證，settings.json清空後CLI退而求其次讀到Keychain的。**沒有動Keychain**（風險太高，教練已經去休息無法即時確認，不該在他睡覺時動系統憑證庫）。這個警告訊息本身講的是「claude.ai connectors被停用」，跟Remote Control核心連線是否成功可能是兩件事(獨立功能)，但沒有100%證據排除它會不會間接影響Remote Control穩定性。

**How to apply**：教練醒來後第一件事**務必用手機確認這個tmux版本的連線是否真的顯示正常/能操作**，不能只信這份記錄「看起來成功」。如果手機端出現異常(例如能連上但操作會報錯)，下一步該查的方向是macOS Keychain「Claude Code-credentials」條目，而非重複前面已經測過的settings.json/.zshrc路徑。

**已知限制**：`tmux`session能撐過「關閉終端機視窗」，但**撐不過Mac重開機/登出**——重開機後這個session會消失，需要重新跑一次`tmux new-session`+`claude rc`那套流程（可以考慮之後寫成launchd開機自動執行，但這超出本次範圍，教練沒有要求，不擅自加）。

## 🟢 2026-09-17 03:47 最終結案：殘留警告的真正原因是軍師自己重複測試時忘記重清settings.json，非Keychain問題

教練收到手機「Can't reach wudashudeMac-mini...may be asleep or offline」，軍師緊張回頭排查，過程中發現：**上一節記錄的「connectors disabled」警告，真正原因很可能只是單純的settings.json在教練休息前已經被還原、而軍師沒有在下一次測試前重新清空**（自己的操作疏失，不是Keychain殘留憑證的問題）。已用最乾淨的方式重新驗證：

```bash
tmux kill-session -t remote-control
tmux new-session -d -s remote-control -c ~/.openclaw
tmux send-keys -t remote-control "env -u ANTHROPIC_BASE_URL -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC claude rc" Enter
```

這次settings.json確實清空的情況下，畫面乾淨顯示`·✔︎· Connected`（不是模糊的`Ready`）+ `Capacity: 1/32`（真的有裝置連上），**完全沒有再出現任何connectors/policy警告**。教練隨後在Mac終端機打字、手機Code分頁同步看到，雙向即時同步驗證通過，比單看連線狀態文字更可靠。

**結論修正**：上一節「懷疑跟macOS Keychain快取憑證有關」是過度推論，沒有直接證據，**不需要進一步調查Keychain**。真正的坑純粹是「每次要清`~/.claude/settings.json`的4個key，一定要在啟動`claude rc`**前**確認乾淨，不能沿用上一輪的記憶假設已經清過」——這條併入前面`feedback_check_global_config_before_shell_level_fix_2026-09-17`的教訓範疇：改一次性config前，動手前先當場查證目前狀態，不要憑記憶假設。

設定檔已還原回MiniMax設定，tmux session `remote-control`持續在背景執行，教練已用雙向打字同步確認連線正常。

## 🔴 2026-09-22 23:50 永久定案：不再「用完復原」，改成手機這條線永久拔除MiniMax

**背景**：09-17當初「用完把設定檔改回MiniMax」是為了保留桌面版/終端機的MiniMax省錢路徑，但這個「暫時清空、之後復原」的模式導致MiniMax金鑰在`~/.claude/settings.json`反覆復活，教練最終在09-22深夜用「Claude帳單88%不動+MiniMax呼叫0%→4%」的雙帳單交叉比對，當場抓到手機Remote Control真的在算MiniMax的錢（詳見[[feedback_settings_json_minimax_leak_not_cleared_2026-09-22]]）。教練明確裁示：**手機這條線永久只准走Claude，不要再「暫時清、之後復原」這種會反覆漏回去的模式**。

**新發現的關鍵坑（09-17沒抓到）**：`~/.claude/settings.json`編輯後，**已經在跑的process/shell不會自動吃到新內容**——包括從「桌面版/終端機這個Claude Code session自己的Bash工具」開的shell，也帶著這個session啟動當下就注入好的舊環境變數（`ANTHROPIC_API_KEY`/`ANTHROPIC_DEFAULT_HAIKU_MODEL`等），**就算改完settings.json，用這個shell開的新tmux session還是會繼承到舊值**，跟settings.json當下寫什麼無關。`env -u`單獨清單一變數在這個繼承鏈下也不夠乾淨。

**真正有效的做法**：改用 `env -i`（完全清空環境變數表，不繼承任何東西）只留最基本的`HOME`/`USER`/`PATH`/`TERM`/`SHELL`+明確`ANTHROPIC_MODEL="claude-sonnet-5[1m]"`/`ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-5[1m]"`兩個必要值來啟動`claude rc`：

```bash
tmux kill-session -t remote-control 2>/dev/null || true
tmux new-session -d -s remote-control -c ~/.openclaw -x 200 -y 50
tmux send-keys -t remote-control 'env -i HOME="$HOME" USER="$USER" PATH="$PATH" TERM="$TERM" SHELL="$SHELL" ANTHROPIC_MODEL="claude-sonnet-5[1m]" ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-5[1m]" claude rc' C-m
```

用`ps eww -p <claude rc PID>`驗證，這次環境變數表裡**完全沒有**`ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_BASE_URL`/`ANTHROPIC_DEFAULT_HAIKU_MODEL`/`ANTHROPIC_DEFAULT_OPUS_MODEL`任何一個，只有明確設定的兩個Sonnet相關key——這代表**就算未來手機端又生出一個要求`MiniMax-M3`的對話串，這個process樹裡也沒有任何MiniMax金鑰/URL可以讓它成功連線**，物理上斷了退路，不是靠「祈禱不要選到」。

**同步永久移除**`~/.claude/settings.json`的`ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_BASE_URL`（連同稍早已移除的`DEFAULT_HAIKU_MODEL`/`DEFAULT_OPUS_MODEL`），**這次不再復原**——因為終端機/桌面版的session本來就一路都用`claude-sonnet-5`原生model走OAuth，從未依賴這幾個fallback變數，拔掉對它們沒有實質影響（[[reference_minimax_mystery_resolved_model_name_routing_2026-09-19]]已驗證：原生model id會走OAuth，完全繞過BASE_URL/API_KEY，只有non-native字串才會退回用這幾個變數當fallback）。OpenClaw閘道(Telegram/LINE/VPS)走的是`~/.openclaw/openclaw.json`完全獨立的設定，不受這次異動影響。

**下次要重啟這個RC bridge**，直接用上面`env -i`版指令，不要再用單純`unset`或依賴settings.json「應該已經清乾淨」的假設——env繼承鏈這個坑（不是settings.json本身，是已存在process的繼承環境）才是這次真正卡了教練一整晚的根因。

## 相關

- [[feedback_settings_json_minimax_leak_not_cleared_2026-09-22]]（教練用雙帳單交叉比對抓到真相的完整過程）

## 🔴🔴🔴 2026-09-23 00:20 當晚真正卡住教練超過1小時的根因：bridge-pointer.json指標檔卡死舊session

**背景**：MiniMax金鑰問題(上面兩段)修好之後，教練手機端連續開好幾次「新對話」——23:53、00:05、00:08——全部都卡住不回應，教練力氣用盡，逐字稿裡明確說「哪怕它吐一個字出來都好，什麼都沒有」。中途一度誤判是env變數殘留/是locale缺失/是慢（heavy hook injection），都不是。

**真正根因**：`~/.claude/projects/-Users-bymyway--openclaw/bridge-pointer.json` 這個檔案記著上一次的 `environmentId`(`env_01VPC6JamuENoF5VDHkX58j3`)。**每次`claude rc`重啟，都會讀這個指標檔案，試著reuse同一個environment**——debug log證據：`Found prior environment env_01VPC6JamuENoF5VDHkX58j3 in pointer (ageMs=461597...); requesting reuse on registration`。而這個environment底下卡著一個從23:47:51就`state: queued`、從未被正常`started_at`的殭屍session(`cse_01PCsAeoy6JFFa8UvXo5j8dN`)——**教練不管在手機上按幾次「開新對話」，同一個environment/機制底下都只會被導回這個永遠queued、永遠不會真正處理訊息的舊session**，這就是為什麼連環開新對話都沒用、連桌面版打字也沒反應的真正原因。

**修復**：直接刪除`bridge-pointer.json`(先備份)，強迫下次`claude rc`啟動時不再嘗試reuse舊environment，改為向server重新註冊一個全新的environment_id。刪除後立即重啟，debug log證實拿到全新`environment_id`(`env_019DNSVrxibV7PvgHRsBBipm`)，教練手機端當下自動連上全新session(`cse_017inbZ7ugfQHiKcZJUq8kiY`)，實測送出訊息成功收到回應。

**關鍵診斷工具**：`claude rc --debug-file <path> -v` 這個旗標平常沒人用過，但這次是**唯一真正看得到「reuse哪個environment」「session卡在queued多久」這些內部狀態的方法**——單看終端機畫面顯示`Connected`完全看不出底層在reuse一個殭屍session，這是這次繞了一大圈才找到根因的關鍵教訓。

**如何應用**：以後Remote Control連線「表面顯示Connected但完全沒有任何回應」，**不要照案例78/v227那套查nettop流量的方法論**（那是查「走哪個model」，這次的病灶完全不同），先直接：
1. `cat ~/.claude/projects/-Users-bymyway--openclaw/bridge-pointer.json` 看有沒有在reuse一個很舊的environment(`ageMs`很大)
2. 用`claude rc --debug-file /tmp/xxx.log -v`重啟，`grep -E "Found prior|state.*queued|Adopted session"`該log，確認是不是卡在reuse舊session
3. 確認是的話，直接刪掉`bridge-pointer.json`(備份後)強制重新註冊，不用再懷疑env變數/locale/MiniMax那些已經在稍早排除掉的可能性

**教訓**：教練被迫連續開4次新對話、逐字稿裡出現「我真的跟笨蛋一樣」這種話，根本原因是軍師把「連線設定問題」(MiniMax殘留，已經真的修好)跟「卡住不回應問題」(bridge-pointer.json殭屍session，完全不同的病灶)混為一談，一直在同一個錯誤方向上反覆重啟/换env策略，卻沒有先去看`--debug-file`這種能直接看到底層真相的工具。**下次遇到「感覺修好了，但教練說沒用」，要先假設是不同的根因，不要在同一個假設上加碼修第二次、第三次**，改用能看到底層狀態的診斷工具重新定位問題，而不是憑更激進的手段(`env -i`)硬猜。

## 相關（補充）

- 這次的完整血淚過程建議蒸餾進試金石案例庫（下次E05接力棒更新時一併補上）
