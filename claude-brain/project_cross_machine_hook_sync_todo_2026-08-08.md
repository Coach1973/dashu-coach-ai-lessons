---
name: cross-machine-hook-sync-todo-2026-08-08
description: 2026-08-08 Mac新增三支重要hook(截圖鎖修復/自動跳Chrome/守則定期重載)，Windows(聯想/ACER)需要各自PowerShell版本並在當地settings.json註冊，教練要求優先處理
metadata: 
  node_type: memory
  type: project
  originSessionId: 56947c71-51f1-4f4b-be4e-2ffdbfc779dc
  modified: 2026-08-07T23:02:50.720Z
---

# 三台機器hook同步待辦（2026-08-08教練親口要求「每台電腦都要知道這個優先順序」）

Mac終端機這場對話修了三個問題，全部已commit推上`mac-openclaw-workflows`(workspace repo)雲端：

1. **截圖鎖工具名稱修復**（commit `b52934ad9`）：`scripts/screenshot_lock.sh`裡claude-in-chrome的工具名稱寫錯（`Claude_in_Chrome`應為`claude-in-chrome`），修正後截圖鎖才真正生效。**Windows已有`screenshot_lock.ps1`，需要同樣檢查裡面的工具名稱有沒有同款拼字bug。**
2. **改完HTML自動跳Chrome**（commit `17147771f`）：新增`scripts/auto_chrome_after_html_edit.sh`（PostToolUse hook，Edit/Write碰`.html`就自動`open -a "Google Chrome" file://...`）。**Windows需要PowerShell版本，用`start chrome`取代`open -a`（參考[[feedback_html_preview_chrome_only]]既有的Windows對應寫法）。**
3. **長對話每10輪自動重載21條守則全文**（commit `6ae54fd6c`）：新增`scripts/periodic_xinfa_reload_hook.sh`（UserPromptSubmit hook），根因是Claude Code的CLAUDE.md只在session開始載入一次，隨對話變長可能被系統壓縮掉。**這支是純bash+python3，理論上Windows能直接用（Windows也有python3+git bash環境），但要實測過jq/python3路徑在該機器上是否正確才能上。**

## Why
教練當場質問：「如果不能讀守則，那我花費心思寫出來的守則意義是什麼？」查證發現這是Claude Code CLI架構性問題（單一長對話會被context壓縮），已修復Mac端，但`~/.claude/settings.json`是**每台機器各自的本機設定檔，不隨git同步**——即使腳本檔案本身已經推上雲端、其他機器`git pull`能拿到檔案，**hook的註冊（matcher/PostToolUse/UserPromptSubmit區塊）仍要各機自己動手改`~/.claude/settings.json`**，不會自動生效。

## How to apply
Windows(聯想/ACER)下次開工，這是優先任務：
1. `git pull`更新到`mac-openclaw-workflows`最新版，確認拿到上述三支腳本
2. 檢查Windows端`screenshot_lock.ps1`是否也有工具名稱拼字問題（比對`mcp__claude-in-chrome__`vs可能寫錯的`mcp__Claude_in_Chrome__`）
3. 仿照Mac的`auto_chrome_after_html_edit.sh`邏輯寫`auto_chrome_after_html_edit.ps1`（用`start chrome`），在Windows的`~/.claude/settings.json`加PostToolUse註冊(matcher: Edit|Write)
4. `periodic_xinfa_reload_hook.sh`若Windows環境有bash/git-bash可直接執行，在該機的`~/.claude/settings.json`的UserPromptSubmit區塊補上這行；若環境不支援bash，需要改寫PowerShell版本
5. 每支改完都要用模擬輸入測試過（`echo '{...}' | script.sh`這種方式），不能只憑寫完就當作生效，比照Mac這場的驗證方式

Related: [[feedback_html_preview_chrome_only]]、[[feedback_screenshot_rules_consolidated]]、[[reference_claude_code_long_session_rule_decay]]
