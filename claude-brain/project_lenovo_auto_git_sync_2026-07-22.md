---
name: project-lenovo-auto-git-sync-2026-07-22
description: 聯想機LenovoBrainSync排程(每2小時拉雲端大腦)已於2026-07-23應教練要求關閉，因每次開工自然會同步，不需要輪詢
metadata: 
  node_type: memory
  type: project
  originSessionId: 7f58ea38-aeee-46d4-9937-f9db3d365b35
  modified: 2026-07-23T14:26:31.889Z
---

2026-07-22 教練體檢時發現:聯想機兩個主倉庫(`mac-openclaw-workflows`、`workspace`)昨晚同步後幾小時內又落後遠端76個commit,而本該負責自動同步的舊排程`ClaudeMemorySync`、`ClaudeHeartbeat`從2026-06-14就是Disabled狀態(五週沒動),且它們指向的`E:\Claude-Data\scripts\`裡是4月/6月的老腳本,屬於舊架構遺物(倉庫早已改用mac-openclaw-workflows)。這是[[project_windows_workspace_git_sync_gap_2026-07-17]]那次落後17天/1711commit的真正結構性根源——不是偶發疏忽,是這台機器根本沒有在運作的自動同步。

**已建的治本機制**:
- 腳本:`E:\Claude-Data\scripts\auto_git_sync.ps1`(純英文避免ps1編碼陷阱),對兩個倉庫做`git pull --ff-only`,工作區有未提交變更就跳過(絕不覆蓋本機),絕不自動push,結果寫進`auto_git_sync.log`
- 排程:`LenovoBrainSync`(schtasks建立,每2小時觸發+已開StartWhenAvailable開機補跑)。註冊時ONLOGON觸發需要管理員權限失敗,改用HOURLY/MO 2成功(使用者context免權限)。已實測排程器能正確呼叫、拉取、記錄。

**How to apply:**
- 以後這台機器最多落後遠端2小時(開機狀態),久沒開機也會在開機後自動補跑一次。開工前若仍想保險可手動`git pull`,但不再是必要動作。
- 舊的`ClaudeMemorySync`/`ClaudeHeartbeat`排程是死的,可忽略;真正在跑的是`LenovoBrainSync`。
- 若哪天又發現落後很多,先查`auto_git_sync.log`看排程有沒有在跑、有沒有因為工作區不乾淨一直跳過。
- 這是時間型排程(每2小時)不是純事件驅動,原因是「遠端有更新」在Windows沒有原生事件可掛,登入觸發又需管理員權限;折衷用登入痛點最相關的短間隔+開機補跑,已是免權限前提下的最佳解。

**2026-07-23更新:此排程已停用。** 教練當天22:16看到PowerShell視窗閃一下(就是排程22:15:02觸發的sync),查證後教練說「每次勾選的時候，它自然而然會把雲端同步，所以不需要這個每兩個小時跑一次」——已執行`Disable-ScheduledTask -TaskName 'LenovoBrainSync'`,狀態改為Disabled(沒刪除,腳本`E:\Claude-Data\scripts\auto_git_sync.ps1`還在,要恢復可再Enable)。
**How to apply(更新):** 以後聯想機不再每2小時自動同步,同步時機回到「開工六步驟」第一步的手動`git pull`。若未來又發現久沒開機導致落後遠端很多,那是預期中的行為(不是bug),等下次開工自然補齊即可,不要又主動重建輪詢排程。

Related: [[project_windows_workspace_git_sync_gap_2026-07-17]]、[[feedback_event_driven_not_polling_pattern]]
