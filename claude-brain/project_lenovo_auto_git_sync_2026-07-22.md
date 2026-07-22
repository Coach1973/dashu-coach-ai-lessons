---
name: project-lenovo-auto-git-sync-2026-07-22
description: 聯想機已建LenovoBrainSync排程自動拉取雲端大腦(每2小時+開機補跑)，治本解決「久沒用就落後遠端十幾天」的結構性問題
metadata: 
  node_type: memory
  type: project
  originSessionId: 7f58ea38-aeee-46d4-9937-f9db3d365b35
  modified: 2026-07-22T02:18:59.868Z
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

Related: [[project_windows_workspace_git_sync_gap_2026-07-17]]、[[feedback_event_driven_not_polling_pattern]]
