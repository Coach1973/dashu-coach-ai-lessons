# 封存：10/16 15:10 追加棒（網站斷線通知＋香檳下午茶頁上架）

## 🟢 本場追加（2026-10-16 15:10 台灣時間，Mac 桌面版 Code 分頁「開工」臨時 worktree，Sonnet 5.5；14:43～15:10）

- **網站斷線通知做完**：`launchagents_guard.sh` 補「13 個公開網站實測連得到」，連不到就電報通知（`4b5bd883f`）。
- **香檳下午茶國際禮儀沙龍頁上架策展中心**：教練給 tava-ai.com/chat/uxna5zb6dv/landing-v2.html，要同樣的網頁、內容照抄、報名走 event.bymyway、封面只放主講者洪繡巒（附學經歷戰績）、理事長林家旭單獨介紹。成品 https://event.bymyway.com/curated/champagne-salon/ （策展 kind=shop、已進大樹作品一覽、GitHub Coach1973/champagne-salon、字 ≥20px、手機桌機皆無橫向捲動）。報名場次 event.db events.id=34 slug `champagne-salon-1109`（改動前備份 /tmp/event.db.bak_champagne），表單 POST /api/register 實測 ok，測試報名已清掉。
- **教練要確認**：①戰績只用原頁寫的（外貿協會歐洲形象訪問團團長、兩本著作、數十年輔導），網路查不到更多；②理事長林家旭網路查無資料，只放姓名職稱＋「敬邀」一句，有資料再補；③照片裡的女士＝洪繡巒、男士＝林家旭是依檔名 hosts 與性別推斷；④策展中心自動把類別分成「食」，要不要改。
- **教練線索**：說「報名機制走 event.bymyway」＝統一用 /api/register 進活動報名群。
