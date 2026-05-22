---
name: Hook/設定類任務必須在教練實際使用環境驗證
description: ~/.claude/settings.json 的 hook 對桌面版 Claude Code（Code 分頁）有效（2026-05-20 實證更正）；但跨檔任務仍須在真實環境驗證，不能 selftest 結案
type: feedback
originSessionId: c69b4269-ecb6-42e2-bbb1-7d5bca4352e0
---
裝設定檔、註冊 hook、改 cron 這類「跨檔/跨系統」任務，**完工驗證必須在教練真實使用的環境跑一次**，不能只在腳本作者的環境跑 self-test 就回報完成。

## 🔴 2026-05-20 實證更正：桌面版 Code 分頁「會讀」~/.claude/settings.json

舊版本檔斷言「`~/.claude/settings.json` 只有終端機 CLI 會讀、對桌面版完全沒效」——**這是錯的，今天當場推翻：**
- 軍師（桌面版，`__CFBundleIdentifier=com.anthropic.claudefordesktop`）的運行進程啟動參數帶 `--setting-sources=user,project,local`，user 層就是 `~/.claude/settings.json`
- PreToolUse hook（dangerous_cmd_check.sh）在桌面版**實測攔截成功**

正確理解 Claude Desktop 三個分頁的設定來源：
- **Code 分頁**（軍師）＝ 跑 Claude Code 引擎 → 讀 `~/.claude/settings.json`（hook 有效）
- **Chat / MCP 設定** → 才在 `~/Library/Application Support/Claude/claude_desktop_config.json`
- 兩者是不同分頁的不同配置，不是「桌面版一律不讀 settings.json」

**所以：要給桌面版軍師裝 hook，就裝 `~/.claude/settings.json`，有效。** 2026-05-16 那次「hook 沒發動」是當時配置或版本問題，不是路徑根本不通。

**Why:** 2026-05-16 連續兩場 Opus 軍師回報「第一招 Hook 已完工」，第一場根本沒註冊到 settings.json、第二場註冊了但裝錯位置——教練全程用桌面版 Claude.app，那支 hook 在他的使用場景**從未發動過任何一次**。HEARTBEAT.md 裡的「Hook 自檢通過」是腳本作者在終端機自己跑 `selftest-002`，看起來像驗收實際是假驗收。教練 12:00 開工沒觸發當場抓包，整套「機制取代自律」目標到該刻實現 0%。第三場（本次）改用 CLAUDE.md 自動鏡像才真正解決桌面版的「強制餵」需求。

**How to apply:**
- 改 `~/.claude/settings.json` 前先問：教練主要在哪種視窗用？桌面版 App / 終端機 CLI / 其他？
- 任何「裝完了」回報必須附：(1) 教練在他**自己日常開的視窗**測過 (2) 系統留證（HEARTBEAT.md 紀錄 / cron log / 檔案 mtime）
- Self-test 的 Session ID 不能是 `selftest-*`，必須是教練實際打開工那場的真實 session id
- 桌面版要做「強制餵接力棒」的標準做法：把接力棒鏡像到 CLAUDE.md 標記區段，桌面版啟動讀 CLAUDE.md 一定看得到；腳本：`workspace/scripts/sync_handoff_to_claudemd.sh`
