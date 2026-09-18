---
name: reference-remote-control-relaunch-blocked-mystery-2026-09-19
description: "claude rc手機Remote Control host process被關掉後無法重啟，卡在Claude Code自己判定「API金鑰存在」，來源查不到，已exhaust所有已知config位置"
metadata:
  type: reference
---

# 手機Remote Control (`claude rc`) 重啟卡死，根因未查明

2026-09-18深夜，因診斷「手機MiniMax context window沒吃到1M設定」問題，發現手機Remote Control所連的`claude rc` host process（PID 97294，tmux session `remote-control`）從**2026-09-17 03:47就一直沒重啟過**——比當晚做的settings.json MiniMax修復還早一天多，導致手機那端一直吃不到新設定。教練同意後關掉重啟，結果**卡死，至今未修復**。

**症狀**：任何方式重啟`claude rc`（含`.zshrc`裡9/17就寫好的專用別名`claude-remote`：`env -u ANTHROPIC_BASE_URL -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC claude rc --setting-sources=project,local`）都回報：
```
Error: Remote Control is only available when using Claude via api.anthropic.com.
ANTHROPIC_BASE_URL is set and does not point at api.anthropic.com...
```
`claude rc --debug`額外顯示`ANTHROPIC_API_KEY=set`/`ANTHROPIC_AUTH_TOKEN=set`，即使該次呼叫已用`env -u`清空這些變數。

**已排除的來源（逐一實測排除，非猜測）**：
1. `~/.claude/settings.json`的`env`區塊——臨時整個拔掉ANTHROPIC_BASE_URL/API_KEY/AUTH_TOKEN/CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC後仍同樣報錯，已還原
2. `~/.claude/settings.local.json`（user層級）——env區塊是空的`{}`
3. `/Users/bymyway/.openclaw/.claude/settings.local.json`（project層級）——env區塊是空的`{}`
4. `~/.zshrc`——用純`bash`(非zsh，不會source .zshrc)直接跑同樣失敗，排除shell rc檔案
5. macOS Keychain「Claude Code-credentials」——結構只有`claudeAiOauth`(accessToken/refreshToken/expiresAt等OAuth欄位)，沒有apiKey/baseUrl欄位
6. macOS Keychain「Claude Safe Storage」——推測是Electron safeStorage加密金鑰(桌面版App用來加密本機資料)，非CLI憑證來源
7. `launchctl getenv`全域環境——ANTHROPIC_BASE_URL/CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC皆為空
8. 背景daemon/router process——`ps aux`全機掃描無任何claude gateway/daemon/router/ccr-bridge類process在跑，也無相關unix socket檔案
9. `~/.claude.json`（Claude Code主設定檔，非settings.json）——搜尋baseUrl/apiKey/authToken相關欄位，只找到`customApiKeyResponses`(記錄使用者曾核准過的API金鑰指紋清單，非目前生效設定)
10. `claude auth logout` + `claude auth login`重新走一次真OAuth登入——確認`auth status`回報帳號正確(bymyway7@gmail.com/CoachWu)，但`claude rc`症狀完全沒變

**已確認正常/乾淨的部分**：
- 真OAuth登入狀態乾淨(這部分修復成功且已驗證)
- 本場對話所在的桌面版Desktop App session全程未受影響(logout/login過程中持續正常回應)

**懷疑方向（未驗證）**：`claude rc --debug`輸出裡有一行`tengu_ccr_bridge=true`（tengu是Claude Code內部代號），懷疑跟某種GrowthBook feature-flag控制的「CCR(Claude Code Router?)橋接」機制有關，這類內部功能旗標的判斷邏輯不在任何本機可查的設定檔裡，可能是SDK/CLI內部程式邏輯直接綁定、或透過某個尚未找到的快取檔案生效。

**下一場診斷建議**：
1. 先查`claude --version`是否有更新版本修復此問題（`claude update`）
2. 嘗試完全移除`~/.local/share/claude/`下的CLI快取重裝（風險：會清掉更多狀態，執行前跟教練確認）
3. 直接查Anthropic官方Claude Code GitHub issues搜尋`tengu_ccr_bridge`或這段錯誤訊息全文
4. 若教練想要的其實只是「手機能連上跑任務的入口」而非精確復原原本那個process，可評估改用`mcp__ccd_session_mgmt__set_remote_control`(Desktop App原生Remote Control機制，讓手機直接follow/steer現有桌面版session)是否能滿足需求，跟原本`claude rc`+MiniMax lobby的定位不同(前者是跟拍桌面版昂貴session，後者是獨立MiniMax輕量任務入口)，兩者不是直接替代關係，教練要先想清楚要哪一種

**教練當場裁示**：先總結收工，這個問題留到下一個對話框繼續查，不繼續耗當前對話框的context。
