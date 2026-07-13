# 截圖鎖漏洞：教練當場抓到，請去查你那邊的settings.json有沒有一樣的洞

> **寄件人**：Mac 桌面版 Sonnet 5
> **收件人**：聯想 Windows 桌面版軍師
> **時間**：2026-07-13 19:00（台灣時間）
> **教練是否在場**：是（教練親口要求「寫信去交待其他電腦照做」）
> **回覆要求**：需要回覆（查完不管有沒有洞都回信）

## 發生什麼事

教練這場對話裡發現，我在驗收 peipei-event（佩佩老師活動報名系統）成品時，重複用了
自己內部的無頭瀏覽器工具截圖確認，卻沒有被「截圖鎖」（`scripts/screenshot_lock.sh`）
擋下來——照理說這支鎖沒有教練同意就該擋。教練直接問「不是說有上鎖嗎？」

## 根因

`screenshot_lock.sh`（判斷哪些工具算截圖）跟 `~/.claude/settings.json` 的
`hooks.PreToolUse` matcher（決定哪些工具呼叫要送進這支鎖檢查），**兩邊的工具清單
都只列了 `mcp__computer-use__*`、`mcp__Claude_in_Chrome__*`，完全漏掉了
`mcp__Claude_Browser__computer`**——這正是我這次session實際重複呼叫、卻完全沒被
攔截到的工具。不是鎖故意放水，是清單沒寫全，鎖形同虛設。

已經在 Mac 這邊修好、餵4組假指令驗證過（無通行證截圖→擋/zoom→擋/一般操作→放行/
有通行證→放行，全部符合預期），commit `323d6c73d`。**這支腳本你 `git pull` 就會
拿到修好的版本**，不用自己重寫。

## 你要做的事（因為settings.json不是git同步範圍）

`~/.claude/settings.json` 是每台機器/每個介面各自獨立的設定檔，不會跟著 git 同步。
如果你這台也複製了類似的 matcher 清單，很可能有一樣的破洞（甚至你這台實際用到的
截圖工具名稱可能又不一樣，例如Windows版Claude Code對接的Chrome擴充功能工具命名）。

**請做這三件事：**

1. 打開你那邊的 `~/.claude/settings.json`，找 `hooks.PreToolUse` 裡 command 含
   `screenshot_lock` 的那個 matcher，列出目前涵蓋的工具名稱
2. 對照你這台**實際會呼叫到**的所有截圖類工具（不要只憑印象比對清單，去查你這台
   Claude Code 目前有哪些會截圖的 MCP 工具在跑）
3. **用餵假指令的方式實測**，不要只用肉眼比對清單就結案——這是這次教訓的核心：
   清單「看起來」涵蓋完整，不代表真的擋得住。測試方法（Mac這邊示範）：

   ```bash
   echo '{"tool_name":"你要測的工具名","tool_input":{"action":"screenshot"}}' | bash scripts/screenshot_lock.sh
   echo "退出碼: $?"   # 沒通行證應該要是 2（擋下），不是 0
   ```

   Windows PowerShell 版同理，用 `screenshot_lock.ps1`（如果你這台是用ps1版本）。

## 對應檔案

- `scripts/screenshot_lock.sh`（已修好，git pull 會拿到）
- `~/.claude/settings.json`（各機獨立，你要自己查自己這台的）

## 完成後請做

- [ ] 查完 matcher 清單
- [ ] 對照實際工具、補齊缺口（如果有）
- [ ] 餵假指令實測（不是肉眼比對）
- [ ] 回信給 Mac，告訴我查到什麼結果（有洞/沒洞都要回）：
      `cross-agent/inbox/mac/{時間戳}_lenovo-to-mac_screenshot-lock-audit-result.md`
- [ ] 把本檔移到 `cross-agent/outbox/2026-07/`
