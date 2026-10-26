# Claude 額度燒光主因：Claude Desktop 內建 worktree 分身（2026-10-26 查明結案）

<!-- project: github.com/Coach1973/mac-openclaw-workflows -->

## 一句話

教練 Claude 帳號 10/23～10/25 燒掉的額度，**94.9% 來自教練自己在 Claude Desktop 打字「開工＋時分」所開的分身**。
**沒有任何排程器、沒有任何 hook 在背後自發**——Claude Desktop 的內建 worktree 功能就是那個「launcher」。

## 完整因果鏈

1. 教練在 Claude Desktop 開新對話，輸入「開工1437」「開工1543」「開工」這類字串。
2. Claude Desktop **自己**執行 `git worktree add`：
   - `baseRepo=/Users/bymyway/.openclaw`
   - `branch=claude/kaigyo-1437-7ba0b0`（`kaigyo` ＝ 開工的羅馬拼音，`1437` ＝ 打字當下的分鐘）
   - `sourceBranch=main`
   - 寫進自己的租約檔 `~/Library/Application Support/Claude/git-worktrees.json`（欄位 `leasedBy`、`createdAt`）
3. Claude Code 在該 worktree 啟動，`~/.claude/sessions/*.json` 的 `hostSessionId` 與 `leasedBy` **完全相符**
   （`entrypoint=claude-desktop`、`kind=interactive`）。
4. 提示以**真人輸入**落地 → 這之後才輪到 `SessionStart` / `UserPromptSubmit` hook 注入
   `JUNSHI_HANDOFF_LATEST.md` 與 worktree 自己的 `CLAUDE.md` 鏡像 → cache read 暴增。
5. 場次一路拖到跨夜 → 額度燒完。

## 「這是真人輸入」的簽章（下次查直接照抄）

| 欄位 | 真人 GUI 輸入 | hook 注入 |
|---|---|---|
| `userType` | `external` | — |
| `isSidechain` | `false` | — |
| `isMeta` | `null` | `true` |
| `hookEventName` | `null` | `Stop` / `UserPromptSubmit` / `SessionStart`… |

**`isMeta=null` 且 `hookEventName=null` ＝ 真人從 GUI 輸入。** 這是判定「誰發起」的黃金訊號。

## 三層人類筆跡佐證（排程器模仿不來）

- `開工2O31` — 把數字 0 打成英文字母 O
- `開工 12 點 52 分` — 口語時間寫法
- `只回覆兩個字：測試` — 真人測試訊息

## 時分後綴 = 打字當下的分鐘（與 worktree 建立時間對得上）

| 提示 | worktree 建立 | 第一則真人輸入 |
|---|---|---|
| `開工1437` | 10-25 14:38:31 | 10-25 14:38:34 |
| `開工1543` | 10-25 15:44:24 | 10-25 15:44:26 |
| `開工0019` | 10-25 00:19 區間 | 10-25 00:20:26 |
| `開工` | 10-26 01:17:18 | 10-26 01:17:20 |

## 排除 hook／排程的必查清單

- `SessionStart`／`UserPromptSubmit` hook **時序上跑在提示落地之後**
  （實測：01:17:20 提示 → 01:18:21 SessionStart → 01:18:27 UserPromptSubmit）
- `git worktree add` 搜尋範圍：`~/.openclaw/workspace/scripts/`、`~/.openclaw/scripts/`、`~/.claude/hooks/`
- `/tmp/cc-socks/*.sock`：OpenClaw 訊息工具的**外部注入通道**（收件人寫法 `uds:/tmp/cc-socks/<pid>.sock`），有審批閘門。**腳本層零命中**（唯一 `socket.connect` 是 Playwright 內部 CDP socket）；命中全在資料／記錄檔，狀態只有「擋住待核准」「逾期未核准」「未投遞」三種，**無一筆成功投遞**；uds 收件只有 9 月的 2 個 pid，與三場「開工」分身無關；10/26 當天 uds 紀錄為 0 → 與本案無關
- `~/Library/LaunchAgents/`、crontab、`osascript`／`cliclick`：無驅動 Claude Desktop 者
- Claude Desktop 自身日誌（`main.log`、`coworkd.log`、`cowork_vm_*.log`、`app-cu-helper.log`）：無自動觸發痕跡

## 「程序比提示晚 3.5 小時」＝執行程序換代，不是時鐘跳動

`開工1437` 第一則提示 10-25 14:38:34，活著的 Claude Code 程序 18:13:49 起。
該場 assistant 訊息從 14:38:51 連續到 10-26 01:14:01（815 個），唯一空檔 19:55→00:12 ＝ 教練休息。
→ Claude Desktop 會中途重新拉起 runtime，但 session 記錄／worktree／分身對象全程同一份，額度是整段累計。

## 省額度三招

1. **別讓分身跨夜**（10/25 00:19、10/26 01:17 開的都跑到隔天）
2. **離開就關分身**
3. **縮上下文**（cache 佔加權量 87.6%，cache_read 61.0% + cache_creation 26.6%）

## 相關

- 報告全文：`cross-agent/inbox/mac/20261026-0930_xiaolongxia-to-mac_claude-quota-burn-10-23-to-10-25-report.md`
- 軍師 08:55 調查信（已回覆並歸檔）：`cross-agent/outbox/2026-10/done_20261026-0855_mac-to-xiaolongxia_investigate-claude-quota-burn-10-23-to-10-25.md`
- 結案 commit：`33823d2f1d0de95c67c2eeae3a0e446ff6a293d7`
