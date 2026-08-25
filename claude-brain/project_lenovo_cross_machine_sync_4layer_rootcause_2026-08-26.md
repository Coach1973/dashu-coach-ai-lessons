---
name: project-lenovo-cross-machine-sync-4layer-rootcause-2026-08-26
description: 教練問「三台Claude桌面版怎麼變各自為政」的完整答案——聯想這端有四層獨立根因疊在一起，全部已修並推雲端(6b121713)，含驗證方法
metadata: 
  node_type: memory
  type: project
  originSessionId: 4e652b8a-8bea-4bf1-bb10-68f6594c133b
  modified: 2026-08-25T17:36:54.619Z
---

2026-08-26 凌晨教練質問「我早就講過三臺電腦有什麼進度全部都要上傳更新、互通有無，怎麼會搞到現在變成三臺電腦又各自為政」。查證後聯想這端有**四層互相獨立的根因**，任何一層沒修都會讓同步整體失效，而且全部是靜默的（不報錯、教練看不出異狀）：

**第一層：七支對齊 hook 一支都沒註冊。** `setup_windows_hooks.ps1` 定義的標準七支（時間鐵律×2／開工六步驟注入／跨機信箱掃描／跨機commit掃描／刪除防護鎖／**收工自動push**）在聯想 `~/.claude/settings.json` 完全不存在，只有另外 5 支本機自建的。ACER 2026-08-25 已重裝這七支，聯想沒有——這就是兩台落差的來源。

**第二層：`E:\Claude-Data\workspace` 是卡在 7/23 的第二份 clone。** 所有 hook 靠 `JUNSHI_HOOK_ROOT\workspace` 定位，但那個路徑指向一份 34 天沒更新的舊 clone（691MB，有自己的 .git、同一個 remote）；真正活的 repo 是 `E:\Claude-Data\mac-openclaw-workflows`。**就算 hook 裝上也會讀到 7/23 的接力棒。** 已確認舊 clone 無任何未推送內容（`origin/main..HEAD` 空、工作區 0 異動、HEAD `99c05e1b` 已存在於 origin/main），改名封存為 `workspace.stale-20260723-archived-20260826`（**未刪**），原路徑改建 junction 指向活 repo，一次修好全部七支的路徑。

**第三層：PS 5.1 `-File` 模式下 stdin 中文被 Big5 讀壞。** `feed_junshi_handoff.ps1` 用中文觸發詞比對，實測「開工」的 code point 從 `958B,5DE5` 變成 `003F,F55D,6975` → 永遠比對不到 → exit 0 靜默。**腳本檔案本身的中文是好的（有 BOM），壞的只有 stdin**，所以光看程式碼看不出問題。修法照抄已驗證的 `summary_upload_trigger.ps1`：`ReadToEnd` 之前加 `[Console]::InputEncoding = [System.Text.Encoding]::UTF8`。同批修了 `scan_cross_machine_commits.ps1`、`delete_guard_hook.ps1`（後者關係到含中文檔名的刪除指令會不會漏擋）。

**第四層：`session_end_auto_push.ps1` commit 後直接 push，沒先 pull。** Mac 每 15 分鐘就自動 commit 一次接力棒，所以聯想的 push 幾乎必然被 `! [rejected] (fetch first)` 擋掉，東西永遠留本機。已補 stash→`pull --rebase`→push→stash pop（pop 衝突時不丟 stash）。**Mac 端 HEARTBEAT 也看得到同款失敗紀錄（「commit 437a99c5c 已留本機，但 push 失敗」），Mac 版是 .sh，未受本次修復涵蓋。**

**順手做的瘦身**：開工注入從 174,260 → 60,494 bytes（省 114KB）。Mac 版早有「CLAUDE.md 已鏡像接力棒就不重複貼」的設計，但它比對 `.sync_markers` 時間戳，而 git pull 會把檔案 mtime 改成 pull 當下時間 → 在聯想/ACER 上永遠判定「非最新」、瘦身永遠不生效。改成比對內容指紋（接力棒尾端 300 字是否出現在 CLAUDE.md 裡），跨機通用。

**驗證方法（下次懷疑同步斷掉時照這個順序查）：**
1. `powershell -NoProfile -Command "(Get-Content $env:USERPROFILE\.claude\settings.json -Raw|ConvertFrom-Json).hooks"` 數 hook 支數（聯想現在應該是 12 支）
2. 確認 `E:\Claude-Data\workspace` 是 junction 且 `git -C 該路徑 log -1` 是今天的
3. pipe-test：`echo '{"session_id":"t","prompt":"開工"}' | powershell -NoProfile -ExecutionPolicy Bypass -File scripts\feed_junshi_handoff.ps1` 應輸出約 60KB，不是 0
4. `git rev-parse --short HEAD` 要等於 `git rev-parse --short origin/main`

commit `b8c294dc`→`5828b1b8`→`91ffefd7`→`6b121713`（全部已推 origin/main）。

相關：[[reference_lenovo_summary_hook_jq_missing_fixed_2026-08-26]]（同一天前一場，同型的靜默失效但根因是缺 jq）、[[project_cross_machine_hook_sync_todo_2026-08-08]]（那份記錄的「聯想已完成」只涵蓋 2 支自建 hook，不含這七支）、[[feedback_lock_must_be_hook_not_optin]]（檔案存在≠鎖有效，同一種驗證精神）
