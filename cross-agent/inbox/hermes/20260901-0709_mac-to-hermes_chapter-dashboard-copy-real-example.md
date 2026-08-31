# 更正+接手：來賓戰情儀表板，直接複製真實範例，不要照描述重新設計

> **寄件人**：Mac 終端機（軍師，Sonnet 5，克勞德）
> **收件人**：Hermes
> **時間**：2026-09-01 07:09 台灣時間
> **教練是否在場**：是，教練親口問「可以交給Hermes了嗎」，軍師確認方向已明確，可以交
> **關聯信件**：取代前三封（`20260901-0640`分會CRUD版、`20260901-0648`後台CRUD更正版）——那兩封的設計方向整個是錯的，請忽略，不用讀

## 教訓（軍師這邊已經因此挨罵，寫進試金石案例68，你不用重蹈）

教練一開始就貼了明確網址`sincere.bymyway.com`要求「照抄」，軍師沒有先打開看，憑印象猜成別的系統，設計了一堆不對的東西，被教練連續糾正3次、浪費30分鐘。**這次不要再犯同樣的錯**：任何時候教練給具體URL/檔案路徑要你「照抄」「參考」，第一件事是直接去讀那個東西本身，不要憑名字或描述聯想。

## 現在的正確狀態（軍師已經查證+動手到這裡，你直接接手）

`sincere.bymyway.com`背後是獨立的repo：**`~/github_repos/zhencheng-guests`**（跟`bni-chapters`完全無關），是「邀約來賓戰情儀表板」系統，Flask+SQLite，零登入，會員自己在網頁上直接改自己的121/咖啡會議數字，教練/軍師提供來賓跟早鳥資料。

軍師已經**複製出真鑫分會版本**：**`~/github_repos/zhenxin-guests`**（已commit `0e1d7ec`），做了：
- 完整複製`db.py`/`app.py`/`schema.sql`/`templates/index.html`
- `weekly_data`表新增`early_bird`欄位（真鑫比真誠多一個「早鳥」維度，教練提供，會員不可自填，邏輯跟`guests`一樣）
- `db.py`的`METRICS`/`METRIC_LABELS`/`METRIC_UNITS`加入`early_bird`（`compute_member_stats`是用`for m in METRICS`動態遍歷算totals/streaks，不用改邏輯）
- `templates/index.html`兩處表格區塊都加了早鳥欄位顯示（表頭「總早鳥」「連續無早鳥」+ 每週明細早鳥行），`colspan`數字也同步調整過
- 標題/說明文字改「真鑫分會」、四項指標；「真誠翻轉計劃－大事紀」跟「統計範圍為真誠分會14位在籍會員...」這類寫死的真誠專屬內容已清空/改通用文字
- 用假資料（借用原本真誠的種子資料）跑過Flask test_client + 本機Chrome驗證過畫面正常，早鳥欄位有出現、無「真誠」字樣殘留（測試完已關閉本機服務，`.db`不進git）

## 你接手要做的事

1. **複製`~/github_repos/zhenxin-guests`同樣的模式，再建`~/github_repos/zhengui-guests`（真貴）跟`~/github_repos/zhenzuan-guests`（真鑽）兩份**——這兩個分會不用早鳥欄位（教練只說真鑫要多這個），直接複製`zhencheng-guests`原始架構即可，不用加`early_bird`那些改動。
2. **改`seed.py`寫入真實資料**——這是唯一還沒到位的部分：
   - **真鑫**：軍師手上有Hermes你自己之前整理的21場真鑫例會資料（`~/.hermes/workspace/bni-attendance-summary.txt`，含來賓+早鳥），可以直接拿來寫`seed.py`的`GUEST_DATA`跟早鳥資料。**但缺少真鑫分會的完整會員名單+team分組**（原始`zhencheng-guests`的`TEAMS`/`MEMBERS`是「王者飛翔／百聖維尼／羽宙奇蹟」三組14人，這是真誠分會專屬的，真鑫的組名/成員教練還沒給）——**這個資訊你我都沒有，等教練提供**，不要瞎猜套用真誠的組名。
   - **真貴、真鑽**：目前完全沒有種子資料（會員名單、分組、來賓紀錄都沒有），先把repo骨架/schema建好，`seed.py`留空或最小示範資料，等教練提供再匯入，不用因為沒資料就卡住其他部分不做。
3. **部署交給軍師**——DNS+Cloudflare Tunnel+launchd這塊涉及對外網域設定，軍師來把關（跟`team.bymyway.com`那次的分工一樣）。你把三個repo的程式/資料庫準備好、本機能跑起來即可，完成後寫信告知，軍師接手部署。建議網址：`zhenxin.bymyway.com`、`zhengui.bymyway.com`、`zhenzuan.bymyway.com`（教練還沒最終確認，若他有不同想法軍師會再通知你）。

## 完成後請做
- [ ] 回信告知三個repo的本機測試結果（Flask test_client渲染是否正常、有沒有殘留錯誤分會名稱）
- [ ] 明確列出「還缺哪些資料才能真正上線」（真鑫的組名/會員名單、真貴/真鑽的全部資料），軍師會轉問教練
- [ ] 不要自己編造會員名單或分組，寧可留空等資料，也不要用假資料充當正式內容

—Mac 軍師
2026-09-01 07:09 台灣時間
