---
name: reference-tailscale-rustdesk-direct-network-2026-10-01
description: RustDesk官方中繼站21117壞掉(10-01)，改Tailscale三台+iPhone入網，RustDesk輸入100.x位址直連；在家同網路ID仍可用，「就緒」不等於中繼站正常
metadata:
  type: reference
---

RustDesk官方公用伺服器 rs-ny.rustdesk.com(209.250.254.15)：21115/21116(櫃台)正常，**21117(中繼站)從全球多地都被拒**(2026-10-01查，check-host.net)。App顯示「就緒」只代表連上櫃台，不代表中繼站正常。

**解法**：Tailscale，帳號 bymyway7@gmail.com 三台+手機同一帳號。位址：Mac mini 100.91.228.91、聯想(tree) 100.95.122.29、宏碁 100.78.106.14、iPhone 15 Pro Max 已入網。每台 RustDesk 開「IP 直接存取」(21118)，Windows 端防火牆只放行 100.64.0.0/10。連線時在 RustDesk「遠端 ID」欄直接輸入 100.x 位址(連一次後按星星存最愛)。

**行為**：同一區網(192.168.0.x)用ID直連本來就通，不需中繼站(手機在家連Mac用ID成功)；出門(行動網路)才需輸入100.x。ID與IP兩條路不會自動切換，只走IP最穩。佩佩老師電腦未入網，仍走ID。

**Why**：教練「聯想連得上、手機連不上」的疑惑根源是區網直連 vs 跨網路需中繼。
**How to apply**：遠端連線題先問「誰連誰」(同案例90，10-01又犯第二次)；Mac RustDesk 直連選項要教練本人解鎖(要管理員密碼)；Windows 提升權限教練按「是」；不要叫教練找設定欄位，能建捷徑就建。見 [[reference_move_to_cloud_this_repo_2026-09-25]] 無關，勿混。
