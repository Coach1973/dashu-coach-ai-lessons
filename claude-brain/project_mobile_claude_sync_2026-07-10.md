---
name: project-mobile-claude-sync-2026-07-10
description: 教練手機版 Claude App 如何跟 Mac 同步取得開工狀態——探索 Remote Control 失敗後改用「GitHub repo + 開工.md 入口檔」方案，含一次嚴重的環境誤判教訓
metadata:
  node_type: memory
  type: project
  originSessionId: 4b3f35fd-5869-4ac0-91fa-2be9cdf89353
---

# 手機版 Claude 同步 Mac 桌面版（2026-07-10）

## 最終方案：GitHub repo + 開工.md 入口檔

教練自己想出的思路：把手機當成「第四台電腦」，跟聯想機、宏碁機一樣，透過雲端讀取最新狀態即可，不需要複雜的 Remote Control 技術。

**已落地**：
1. `~/.openclaw/workspace` 這個 workspace 本身已推上 GitHub（`Coach1973/mac-openclaw-workflows`，**private** repo，教練帳號專屬）
2. 建立入口檔 `開工.md`（commit `7722e701f`），內容是「請依序讀取 CLAUDE.md → JUNSHI_HANDOFF_LATEST.md → 試金石/試金石_案例庫.md」的指示
3. 教練手機操作步驟：Claude App → Code 分頁 → 加入 repo `mac-openclaw-workflows` → 打字「讀開工」→ 自動讀完三份核心檔案 → 已實測**內容跟 Mac 這邊完全一致**

**要改哪個網站，就要把那個網站的 repo 也加進手機 Code 分頁**——教練親自驗證過這個邏輯（選了 jiesheng-leadership、bigtree、tainan-calender 三個 repo，理解「選了才能改，全選才能全改」）。

## 繞了一大圈的過程（記錄教訓，避免下次重蹈）

### 第一次誤判：以為手機版 App 完全不懂「開工」
一開始判斷手機官方 Claude App 是純聊天雲端服務，接不到 Mac 本機檔案——這個判斷**部分錯誤**。教練當場糾正：手機版早就有 Code 分頁，能讀 GitHub repo、能執行、能推送，跟桌面版能力相近，只是路徑要用 GitHub repo 而非本機檔案路徑。查證後確認教練是對的，完整教訓見 [[feedback-verify-before-correcting-coach]]。

### 第二次誤判：搞混了「終端機 CLI 登入狀態」和「這個對話本身的身份」
教練要選 Remote Control 方案時，我在 Bash 工具裡執行 `claude auth status`，查到 `authMethod: api_key`，就直接判斷「這個對話走 API 金鑰模式，不能用 Remote Control」——**這是嚴重的環境誤判**。教練當場重話糾正：「你沒有搞定你現在是誰，你現在是桌面版 APP，使用的就是官方帳號一年 200 美金」。

查證後發現：Bash 工具裡查到的是 PATH 指向的**另一個獨立安裝的 CLI**（版本 2.1.161），跟驅動這個對話的進程完全不同。用 `ps aux` 找到真正驅動這個對話的進程是：
```
/Users/bymyway/Library/Application Support/Claude/claude-code/2.1.197/claude.app/.../claude --resume 4b3f35fd-5869-4ac0-91fa-2be9cdf89353 ...
```
這個 session ID 跟本場對話完全吻合，是**桌面版 App 內建引擎**（版本 2.1.197），環境變數裡有 `CLAUDE_CODE_OAUTH_SCOPES` 等欄位，證實走的是教練的官方 OAuth 帳號登入，不是 API 金鑰。

**教訓：判斷「我現在是誰」，不能用 Bash 工具另外呼叫一個獨立 CLI 指令來查——那查到的是 shell 環境裡別的東西，不是自己。要用 `ps aux | grep claude` 找出真正驅動當前對話的那個進程本身的路徑、參數、resume session ID 來確認身份。**

### 第三次繞路：鑽研 Remote Control 內部機制,教練喊停
雖然證實桌面版走 OAuth、引擎版本支援 `--remote-control` 參數，但實測發現：透過 Bash 另開一個獨立進程呼叫這個 CLI（即使是同一個二進位檔案），**讀不到桌面版 App 正在使用中的登入態**——認證狀態跟正在跑的 App 進程本身綁定，指令列呼叫另一個新進程沒用。要嘛在桌面版 UI 裡手動找開關（我用 `strings` 挖 app.asar 找到內部真的有 `enableRemoteControl`、`ccRemoteControlDefaultEnabled` 等程式碼證據，但沒找到 UI 確切位置），要嘛用 computer-use 工具截圖操作（教練質疑「不斷截圖違反守則」，我解釋這其實是唯二允許的例外情境，但仍需消耗較多 token）。

教練在這個節點喊停，提出「手機=第四台電腦，讀 GitHub 路徑」的更簡單思路，整個 Remote Control 路線直接放棄，改走現在這個方案。**印證守則 #16「複雜的解法不一定是正確的解法」——花了大半場對話鑽研 Remote Control 的技術細節，最後真正落地的方案，是教練自己想到的、簡單十倍的路徑。**

## 手機版能力邊界（誠實記錄，避免教練誤以為完全等同 Mac）

| 能做到 | 做不到 |
|---|---|
| 讀/改/commit/push 已加入 Code 分頁的 GitHub repo 內容 | 操作這台 Mac 本機專屬的東西（Downloads 截圖、RustDesk、本機 Chrome 畫面） |
| 教練說「總結並上傳」，手動寫摘要+commit+push | 沒寫進 repo 的密鑰/工具讀不到 |
| 「讀開工」自動讀取核心檔案（靠入口檔內容引導，非本機 hook 自動偵測） | 網頁推 SOP 裡「本機瀏覽器讓教練親眼查驗」這一步，手機雲端環境無法比照 Mac 開一個 Chrome 視窗 |
| 與 Mac 這邊透過 GitHub 間接同步（有 commit/push 延遲） | 跟 Mac 這邊不是同一個 session、不共享即時對話上下文（這點跟 Remote Control 真同步不同，要讓教練清楚知道差異） |

## 順手處理：發現並停用 Mac 本機漏網的 30 分鐘自動蒸餾 crontab

過程中教練質疑「每 30 分鐘自動蒸餾」是否還有必要，查證後發現：2026-07-06 那次 cron 大體檢（[[project-cron-cleanup-2026-07-06]]）只清理了「小龍蝦(openclaw cron)系統」那邊的排程，**這台 Mac 本機自己的 crontab**（跟 openclaw cron 是兩套獨立系統）裡的 `run_terminal_distill.sh` 完全沒被那次體檢碰過，一直跑到今天。已用註解方式停用（commit `8e265574a`），未整行刪除方便追溯。

## 相關記憶
[[project-bni-invite-pages-2026-07-09]]、[[project-cron-cleanup-2026-07-06]]、[[reference-openclaw-nested-git-repos]]
