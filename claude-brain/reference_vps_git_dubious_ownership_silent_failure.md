---
name: reference-vps-git-dubious-ownership-silent-failure
description: VPS(43.245.60.200)自主git備份靜默失敗35天，根因是Docker容器更新後觸發git「dubious ownership」安全機制，所有push被拒但沒人發現
metadata:
  type: reference
  originSessionId: 84150fda-42bc-4356-acc0-ad3d3b4a8c7a
  modified: 2026-08-25T14:18:15.342Z
---

2026-08-25 VPS全面體檢時發現：`reference_vps_github_credentials.md`聲稱VPS能自主備份workspace，但實測`git push origin master`直接失敗（`fatal: could not read Username for 'https://github.com'`），查`git log -1`發現最後一次成功推送是7/20，代表這個機制已經靜默失敗了35天，累積65個未commit的檔案異動（含教練不知道的即時對話記憶）。

**根因分兩層：**
1. **host跟容器路徑不對等**：git的`credential.helper`設定指向容器內路徑`/home/node/.openclaw/.git-credentials`，若在host（VPS本機，不進容器）直接跑git指令，這個路徑在host上根本不存在（host的真實路徑是`/root/openclaw/data/`），必須用`docker exec`進容器內操作，git指令才能正確找到憑證檔案。
2. **git安全目錄檢查(dubious ownership)**：在容器內用`docker exec -u root`執行git指令時，因為repo檔案owner是`node`(uid 1000)而非`root`，較新版git會拒絕操作並要求明確加入`safe.directory`例外，否則`git push`/`git pull`全部會被擋（`fatal: detected dubious ownership in repository`）。這個安全機制很可能是某次容器更新/重建後新引入生效的，觸發後沒有任何主動通知，錯誤只會在下次手動嘗試git操作時才會看到。

**Why：** 這是「靜默失敗沒人發現」這一類系統性問題的又一個實例（同類案例：LINE 429配額被`except:pass`吞掉、報名通知失敗被吞掉），差別是這次連錯誤log都沒有主動被檢視，純粹是這次體檢主動去跑`git push`才發現。

**How to apply：**
1. 診斷VPS的git相關操作，永遠先`docker exec -u root <容器名> sh -c '...'`在容器內執行，不要在host直接跑，兩者的檔案系統視角不同。
2. 遇到`dubious ownership`錯誤，修法是`git config --global --add safe.directory <repo路徑>`（容器內路徑），這是一次性設定，加過就不會再擋。
3. 遇到分支分岔（本地有未同步異動+遠端也有新commit）時，先`git add -A && git commit`把本地異動保住，再`git merge origin/<branch>`（不要用`git pull`預設模式，會卡在要求指定rebase/merge/ff-only），衝突逐一解決（若衝突檔案其中一版本內容自己標記「已棄用/DEPRECATED」，直接判斷保留另一版本，不需要每次都問教練這類明顯可判斷的技術取捨）。
4. 建議：VPS這類「有自主備份機制」的環境，應該定期（例如每次體檢/每月）主動跑一次`git status`+`git push`測試，不能只信任「設定過了就會一直work」，這次35天沒人發現正是最好的例子。

Related: [[reference_vps_github_credentials]]（原始設定記錄，需要更新標注此坑）、[[feedback_false_success_report_pattern]]
