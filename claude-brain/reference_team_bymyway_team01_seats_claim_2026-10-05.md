---
name: reference-team-bymyway-team01-seats-claim
description: team.bymyway.com（第一～五分會 team-01～05）夥伴座位怎麼建、認座位補資料；名單規則（戰情表姓名為主、重複以戰情表為主）；第一二分會是信任遊戲的友好夥伴；chapters.bymyway.com 分會列表順序
metadata:
  type: reference
---

**網站**：team.bymyway.com ＝ repo `~/github_repos/team-bymyway`（資料庫 `team.db`，不進 git；launchd `com.coach.team-webapp` 用 bni-chapters 的 venv 跑 port 5073），分會 team-01～team-05。跟 team01.bymyway.com（戰情表，repo `team01-guests`）是兩個獨立網站。

**第一分會座位（教練 2026-10-05 14:52 交辦）**：名單＝戰情表（`team01-guests/team01_guests.db` members）的姓名，**扣掉陳佩君（啟動董顧）、陳宜璟（支持與成長董顧）**——兩位等分會正式立會才寫上去。專業類別只寫「教練給的名單跟戰情表姓名對得上」的；對不上的是新增夥伴，類別留給本人自補。教練 14:54：「以戰情表上的姓名為主」，所以教練名單的「陳漳豪（產險）」用戰情表的「謝漳濠」。腳本 `seed_team01_members_2026-10-05.py`（重跑安全）。目前 11 座：陳晏綜、鄭季顓、謝漳濠、簡美惠、林芸安、黃乙純、李星慕、王天賜、廖丞威＋名單上戰情表沒有的陳迎薰、王純藝（類別空白，教練名單寫投資型保單、行動美容，待教練確認）。

**認座位**（10/05 從 bni-chapters 真鑽那套搬來）：分會頁座位卡「我是○○・補上照片」→ `/<slug>/claim` 選名字 → 專屬編輯頁（名字唯讀、不能前台刪除；公司／專業類別／簡介／照片／連結本人補；每次儲存先存舊資料到 `member_edit_log`）。座位標記＝`chapter_members.claim_phones` 不是 NULL（本站存空字串）。其他分會（team-02～05）要建座位照 seed 腳本改名單即可。

相關：[[reference_team01_biweekly_and_team_tool_fill_2026-10-01]]（戰情表）

**重複人名規則（教練 15:01）**：教練名單裡的人如果同時在別的名單／戰情表，「以戰情表為主」——陳晏綜在第一分會戰情表，也在教練給的第二分會名單（勞資顧問），只留第一分會，類別取教練名單的勞資顧問。第二分會座位：鄧智文大圖輸出、廖允菁會計師、何琬菁人壽保險、翁郁琇電子針灸儀（`seed_team02_members_2026-10-05.py`）。

**信任遊戲＝友好夥伴（教練 14:58）**：第一分會（後來照辦第二分會）類似還不在 BNI 系統內的友好單位／外部玩家，一樣能玩遊戲（最高到「被相信」第 10 級），成為 BNI 會員才進玩家俱樂部（`game_db.link_member`）。排座位：`bni-chapters/seed_team01_players_2026-10-05.py team-0N`（source=team-0N，identity=friend）。

**chapters.bymyway.com 分會列表順序（教練 14:32）**：照成立先後——真鑽、真誠、真鑫、真愛、真富，後面才是籌備會：真貴、真AI、真功夫、真樂齡。存在 `chapters.sort_order` 和 `bni-chapters/seed.py`（新增分會要照這個規則排）。
