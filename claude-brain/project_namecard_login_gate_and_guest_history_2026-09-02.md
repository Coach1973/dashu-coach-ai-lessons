---
name: project-namecard-login-gate-and-guest-history
description: namecard-db 2026-09-02兩項架構變更：全站改需登入(含瀏覽/搜尋)+guest_visits表記錄來賓完整分會訪問歷程，取代之前公開瀏覽的設計
metadata:
  node_type: memory
  type: project
  originSessionId: 8413cc54-aeab-49dc-81d8-2b7c18c27451
  modified: 2026-09-02T09:04:00.108Z
---

**變更一：guests表新增`guest_visits`子表，記錄完整訪問歷程**

原本`guests`表每人只留「最新一次」訪問的分會，沒有日期欄位，教練反映「看不到他之前是哪個分會的來賓、什麼時候來過」。已從BNI Connect完整歷史報表（涵蓋2018-08-08~2026-09-01全部訪問紀錄）重建`guest_visits`表（guest_id/chapter/visit_date/company/profession/invited_by），`/find`搜尋結果會列出每位來賓的完整分會+日期清單。目前3222位不重複來賓（依電話去重），其中320人有多筆歷史紀錄。commit`db21d10a5`。

**變更二：全站改成需登入才能用（不再公開瀏覽）**

教練先要求「只有跟進功能要登入」（自助申請：姓名+行動電話，密碼統一預設88888，教練`/admin/team`審核），上線後教練又推翻改成**整個系統都要登入**，理由：「如果他們上傳名片，我才知道是誰上傳的」。最終定案：
- `/`、`/find`、`/chains`、`/matches`、`/card/<id>/match`、`/guest/<id>/match`、`/upload`全部加`@team_login_required`。
- `cards`表新增`uploaded_by`欄位，上傳成功時寫入登入者`display_name`，首頁卡片顯示「👤 OOO 上傳」。
- `team_members`表新增`status`(pending/approved/rejected)+`applied_at`，既有帳號（教練bymyway、佩君老師）透過schema遷移自動標記approved，不受影響。
- `team_login_required`裝飾器必須定義在所有使用它的路由**之前**（原本定義在檔案中段，`@app.route("/")`在前面用會報`NameError`，已把裝飾器搬到檔案最前面`app.config`設定之後）。

commit`bb25684eb`（跟進限定版，已被推翻）→`1aa5ddfba`（全站需登入最終版）。

**Why**：教練把系統開放給BNI領導團隊/DNA使用後，需要問責制——知道誰查詢、誰上傳、誰跟進了誰。原本「瀏覽不耗AI額度所以公開」的設計目標（省MiniMax token）跟「需要知道是誰在操作」的新目標互相衝突，教練選擇後者優先。

**How to apply**：
- 往後任何人問「namecard-db/`namecard.bymyway.com`要不要帳號」，答案是**要**，不再是公開瀏覽系統。
- 新增/擴充查詢功能時，資料模型優先考慮「保留完整歷史」而非「只留最新一筆」，尤其是像guest訪問記錄這種天生會重複發生的事件型資料。
- 教練對「存取範圍該多寬」這類設計決策容易在看到實際畫面後反覆調整（這裡改了兩次），先做最簡單可行版本讓他試用，比一次寫到位更有效率，不用一開始就設計得極盡完美。

Related: [[project_namecard_manual_trigger_matching_design_2026-08-27]]（AI呼叫觸發原則，本次未變動）
