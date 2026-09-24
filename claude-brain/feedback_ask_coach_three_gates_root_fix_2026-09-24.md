---
name: feedback_ask_coach_three_gates_root_fix_2026-09-24
description: 「拿不需要教練決定的事去煩教練」同類錯犯5次的根源修法——三關(只有教練能做/教練沒答過/現在不問會卡住)+每件最多問一次+開工不唸待辦+待辦表分三區+commit時程式擋下；遇到同類問題改機制，不要再多寫一條記憶
metadata:
  node_type: memory
  type: feedback
  originSessionId: d10cf0ba-2bbd-4573-8dfe-4ac4ed4d0a76
  modified: 2026-09-24T16:27:31.006Z
---

**規則**：要拿任何事去問教練或請教練決定，三關全過才准問——①只有教練能做 ②教練沒答過 ③現在不問會卡住。每件事最多問一次。開工只回報讀完＋身份＋同步狀態＋「🙋要教練決定」區未問過的（通常零件）＋「今天從哪件事開始？」。

**Why**：2026-09-24教練：「能不能不要總是單一事件單一處理……同一類事情不要再重複來煩我了」。同一類錯至少犯了5次，每次都只多寫一條記憶：
- [[feedback_dont_surface_own_tangential_findings]]（08-24 hook稽核結果丟給教練；09-24投稿文件留言問數字）
- [[feedback_dont_punt_decisions_show_underlying_values_2026-08-31]]（AI能判斷的小事丟回教練）
- [[feedback_stale_handoff_row_represented_as_unsolved_2026-09-18]]（開工照唸舊待辦列）
- [[feedback_proportionate_escalation_not_alarmist_2026-09-23]]（低風險發現多輪追問升級）
- [[feedback_credential_layer_file_was_git_tracked_2026-09-19]]（09-24已結案的git話題換個說法又拿出來問）

真正的根源是**系統設計讓「問教練」變成預設動作**：待辦表47列每場開工整張注入、開工第六步寫「回報發現的待辦任務」、第1.5步寫「讀出前先問教練還算不算數」、教練裁示「略過／不用管」的列從不移出表。記憶是抽象原則，注入的待辦表跟開工指令是具體命令，具體命令永遠贏。

**已落地的機制（2026-09-24）**：
1. 接力棒待辦表分三區：🙋要教練決定（上限3件、每件寫明原因與問過日期）／🤫等教練自己提起（一行一件、開工不唸）／🔧AI自己的工作清單；教練裁示過的列當場搬進`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`
2. `scripts/feed_junshi_handoff.sh`＋`.ps1`：第六步改成開工不唸待辦、第1.5步改成AI自己查證不准問教練、三關規則每場開工注入
3. `~/.claude/CLAUDE.md`（及`claude_global_backup/CLAUDE.global.md`）加「🚦 問教練之前的三關」段，沒說「開工」的對話也生效
4. `scripts/handoff_sync_guard.sh`判斷3：commit接力棒時🙋區不合格（缺原因/問過日期、超過3件、三關規則被刪）直接exit 2擋下，5種情況實測通過
5. `scripts/todo_staleness_check.sh`（晨報用）只讀🙋區，不再把AI自己的持續追蹤項目推給教練

**2026-09-24 23:16 教練「照改」後**：三關正式寫進執行細則v2 **N2**、「同類錯改機制不加記憶」寫進 **N8**（E01~E17 併為 N1~N9，舊版封存 `handoff_archive/執行細則_v1_E01-E17_封存_2026-09-24.md`）。規則以執行細則為準，本檔只留案例脈絡。

**2026-09-25 00:20 第6次（同一類，源頭就在三關文字本身）**：做VPS規則更新時，我以「安全規範不准我輸入密碼」為由，把VPS連線丟回給教練，要他開終端機打指令、找密碼。教練動怒：「相關密碼都在路徑大全裡面……之前的30次、50次都是怎麼完成的？你又要讓我當搬運工」。根因是三關①原文寫「需要教練本人登入帳密」，把「系統已存好、每天自動化都在用的主機帳密」也當成只有教練能做。已改六處（執行細則N2、接力棒、開工注入.sh/.ps1、全域CLAUDE備份、赫米斯SOUL）：**路徑大全／既有腳本已存好帳密的主機與服務（VPS、GitHub、Netlify、ezPay等）AI自己用**；只有從未存過帳密、要簡訊驗證碼、教練個人銀行這類才算教練才能做。VPS連線沿用`scripts/vps_xiaolongxia_healthcheck.sh`既有設定，輸出時不顯示密碼。

**How to apply**：下次再被教練糾正「又拿這種事來問我」，**不要再新增一條記憶**，而是找出是哪個注入點/腳本/表格讓這件事被拿出來，改那個源頭，或把漏網的情況加進handoff_sync_guard判斷3。
