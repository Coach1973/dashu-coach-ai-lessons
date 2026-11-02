---
name: project-skyteam-unlisted-pool-admin-2026-11-02
description: 「未上架的人才軍火庫」後台 /skyteam/admin：做好的人一律先進未上架，教練勾選上架（顧問師前段／商務團隊／人脈資源團隊）或下架；他區 BNI 會員不放軍火庫
metadata:
  node_type: memory
  type: project
  originSessionId: c984183e-d660-4387-9218-44be25b24f60
  modified: 2026-11-02T15:55:19.476Z
---

教練 11/02 23:46 交辦：做好個人網頁的人**一律先進「未上架的人才軍火庫」**，教練自己進後台勾選上架／下架，不用再問軍師「誰還沒上」。比照策展後台 /curation/admin。

- 網址 https://event.bymyway.com/skyteam/admin（要登入，跟策展後台同一組帳號）；已收進大樹作品集「活動後台」。
- 程式 `event-signup/skyteam_pool.py`（CLI＋後台共用），路由在 app.py、樣板 `templates/skyteam_admin.html`；workspace f7950a1ad。
- 未上架名單存 `~/.openclaw/data/skyteam_pool.json`（不公開、每次寫入前備份到 skyteam_pool_backups/，留 30 份）；`dismissed` 是「不是人才／不放」，自動加入會略過。
- 上架：前段插在前段最後並把 FRONT+1；商務團隊／人脈資源團隊放後段（江宜倫維持最後）。之後自動重產邀請函名單、commit＋push skyteam，失敗就整個退回。
- 自動：curation_process 上架完跑 `skyteam_pool.py auto`，新站標題開頭是常見姓氏且像個人頁才加（沒照片）；第一次跑只記基準（129 站），舊站不回頭加。
- 軍師自己做好個人頁時：`python3 event-signup/skyteam_pool.py add <slug> --name … --role … --image 照片檔`，帶照片放進去，不要直接改 skyteam。

**Why:** 教練原則（11/02 原話整理）：軍火庫是吸引人加入他 BNI 團隊的號召力，只放自己區域在籍、離會、或還沒入會的人；已是他區 BNI 會員的不放（林玟妗移除、蔡佩茹頁尾連結拿掉），怕被說拿別區會員當自己招牌。
**How to apply:** 新做的人不要直接插進 skyteam/index.html，一律 `add` 進未上架；教練口頭點名上架時也可以用 `publish <slug> --to front|商務團隊|人脈資源團隊`。初始未上架 6 位：林士民、李勳婷、陳千禾、Grace、莊哲昀、潛錩（紀宇牧，照片待補）。相關 [[project-skyteam-pending-coach-notice-list-2026-10-26]]、[[feedback-skyteam-insert-command-front-block-24-2026-10-25]]
