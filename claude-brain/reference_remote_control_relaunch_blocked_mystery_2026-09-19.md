---
name: reference-remote-control-relaunch-blocked-mystery-2026-09-19
description: "claude rc手機Remote Control重啟卡死，根因已查明並修復：~/.claude/settings.json全域env區塊(MiniMax路由)被無條件套用到每個claude呼叫，擋下api.anthropic.com檢查+feature-flag評估"
metadata:
  type: reference
---

# 手機Remote Control (`claude rc`) 重啟卡死——根因已查明並修復（2026-09-19）

## 根因（實測驗證，非推測）

`~/.claude/settings.json`的**user層級**`env`區塊（為了MiniMax路由設定的
`ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_MODEL`/
`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`）會被claude CLI**無條件套用**到
**每一個**claude呼叫的process環境，不管呼叫端有沒有用`env -u`刻意清掉這些變數，
也不管`--setting-sources`flag想不想排除user層級設定——這個flag在目前CLI版本
(2.1.273/2.1.274)對`rc`子指令根本是無效參數，直接報`Error: Unknown argument`
(舊alias`claude-remote`裡的`--setting-sources=project,local`從一開始語法就是錯的，
大概率是CLI某次更新把這個flag拿掉了，`autoUpdatesChannel: latest`這台機器又是自動更新)。

`claude rc`啟動當下需要兩個條件都成立：①真正連到api.anthropic.com（不是MiniMax的
`api.minimax.io/anthropic`）②feature-flag評估沒被`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
停用。settings.json全域env區塊剛好同時把這兩個條件都破壞掉，這才是真正卡住的原因，
跟settings.json三層/shell rc檔/Keychain/launchd/`~/.claude.json`這些先前排除的10個來源
完全無關——**先前的排除清單方向就沒對準真正的變因**：settings.json的env區塊當時**有**
被檢查過（見下方「先前排除清單」#1），但檢查方式是「臨時拔掉又還原」，沒有搭配同一次
測試把`--setting-sources`那個已失效的flag也拿掉，兩個問題疊在一起互相遮蔽——先觸發
BASE_URL檢查失敗，永遠看不到後面flag解析失敗，所以誤判成「拔掉env區塊仍同樣報錯」。

## 修復方式（已測試2次成功）

實測證實：claude process只在**啟動當下**讀取一次env，process啟動、把值讀進自己的記憶體
之後，跟settings.json檔案之後存不存在完全無關（已用diff驗證：process還在跑、檔案內容
還原後跟備份一致）。

`scripts/restart_remote_control.sh`：啟動當下暫時把settings.json移開（整個時間窗口
不到10秒）、用tmux起一個新的`claude rc`、輪詢看到「Connected」字樣代表成功、立即
（用bash trap確保就算腳本中途失敗也一定會執行）把settings.json還原。已跑過2次，
每次都成功連線+檔案完整還原。

`.zshrc`的`claude-remote`alias已同步修正：拿掉失效的`--setting-sources`flag，
但**這個alias單獨使用仍然無法解決settings.json污染問題**（因為它只能清掉呼叫這一刻
shell層級的env，清不掉claude CLI自己內部重新讀settings.json這件事），平常重啟一律
用上面的腳本，alias只留著給settings.json本身乾淨時的簡易手動測試用。

## 額外發現：官方內建Desktop App Remote Control機制也被同一根因擋下

`mcp__ccd_session_mgmt__set_remote_control`（教練要求的「兩套同時都做」的第二條路）
呼叫後回報「Remote Control initialization failed」——跟`claude rc`是同一個
`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`全域污染問題，但**這個session自己的process
早在很久以前就啟動完成，env早就讀進去了**，現在才移開settings.json時間點已經來不及，
必須**重啟這個桌面版session本身**，讓它在一個沒有污染的settings.json狀態下重新啟動，
才能真正修好。這是2026-09-19教練「兩套同時做」的裁示還沒完成的部分，需要教練決定
要不要現在重啟這個對話框。

## 尚待評估的架構性問題（未動手，僅記錄）

`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`原意（`.zshrc`2026-05-16註解：
「aiprimetech Claude代理設定」）應該是只在**真的用MiniMax當後端**時才需要（避免
Claude Code打一些MiniMax不支援的非必要API，如遙測/feature-flag查詢），但它被寫進
`~/.claude/settings.json`的**全域**env區塊後，變成連「這台Mac桌面版本身走真正
api.anthropic.com的session」都被連帶影響——這是跟`claude rc`同一種「本來該是條件式
的設定被全域套用，波及不相干session」的架構問題。**要不要把這個變數從全域settings.json
的env區塊移出、改成只在真正呼叫MiniMax的地方才設**，教練還沒有明確裁示，先只記錄
不動手，因為移除它涉及所有依賴MiniMax路由的session（手機/test2），影響範圍需要教練
一起評估。

## 先前排除清單（保留當技術檔案，但方向已被上面的根因取代，之後不用再照這份清單排查）

1. `~/.claude/settings.json`的`env`區塊——當時臨時拔掉env區塊後仍同樣報錯，判斷方向錯誤，
   已被上面「疊加兩個問題互相遮蔽」的分析取代
2. `~/.claude/settings.local.json`（user層級）——env區塊是空的`{}`，這部分排除有效，跟真正根因無關
3. `/Users/bymyway/.openclaw/.claude/settings.local.json`（project層級）——env區塊是空的`{}`，排除有效
4. `~/.zshrc`——用純bash直接跑排除shell rc檔案，排除有效但不完整（沒測zsh登入shell的export邏輯，
   後來證實.zshrc本身也沒有直接export這些變數，值全部來自settings.json）
5-9. Keychain/launchd/背景daemon/`~/.claude.json`——排除皆有效，跟真正根因無關
10. `claude auth logout`+`claude auth login`——確認帳號乾淨，跟這次的根因無關，是另一個獨立健康的部分
