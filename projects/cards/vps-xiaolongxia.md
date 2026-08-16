# 專案卡：VPS 小龍蝦（外部朋友版）

- **主機**：43.245.60.200（3.8GB RAM／100GB／1 CPU）｜對外入口：coach.bymyway.com（🔴 這筆 DNS A 紀錄絕不能刪——曾差點被 PicSee 設定指示誤刪）
- **用途**：服務教練的外部朋友（9 個用戶，記憶已隔離，client-memory hook）
- **一鍵開通新用戶**：`/root/provision_new_vps_user.sh`（詳見記憶 reference_vps_provision_script）
- **備份**：VPS 有自己的 GitHub 憑證可自主備份（commit 驗證過）
- **健康檢查**：Mac 每日 08:00 LaunchAgent 測 SSH/Docker，異常才報
- **更新 SOP**：教練說「VPS更新/升級」→ 直接跑四步 SOP 不用問（記憶 feedback_vps_update_sop_trigger）
- **模型**：VPS 小龍蝦用 MiniMax（不限流量的是它，Claude 助教額度另計不可混談）
- **注意**：查 VPS 的事先讀 VPS 上的路徑大全再下結論（案例55：沒查萬用索引就回報查不到，教練糾正）
