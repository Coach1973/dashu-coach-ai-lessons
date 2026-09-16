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
