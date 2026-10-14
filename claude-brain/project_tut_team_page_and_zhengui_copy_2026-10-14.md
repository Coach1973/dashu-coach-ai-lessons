---
name: project-tut-team-page-and-zhengui-copy-2026-10-14
description: 南應大校友會台南分會「理監事與顧問團隊」頁 /tut/team 怎麼運作、資料放哪、哪些不在 git；以及真鑽 5 位助理大使「複製」進真貴籌備會（只在資料庫、有備份）
metadata:
  node_type: memory
  type: project
  originSessionId: 1120f135-e197-43d6-997f-bdcf7a93f84a
  modified: 2026-10-14T01:17:50.279Z
---

**南應大校友會理監事與顧問團隊頁**（教練 2026-10-14 交辦，比照 BNI 分會自助簡介）
- 公開頁 https://event.bymyway.com/tut/team ；程式 `workspace/event-signup/tut_team.py`＋路由在 `app.py`（「南應大校友會台南分會」區塊）；測試 `test_tut_team.py`（用暫時資料庫，`venv/bin/python` 跑）。
- 按「我要建立檔案」→ 送出立刻上架（不審核）→ 拿專屬修改連結 `/tut/team/edit/<token>`；顧問 17 位（記憶牆 `tut-memory` 的 `BIZ_TEAM`）先放空座位，本人點名字補照片簡介。理監事名單教練還沒給，目前空。
- 色系：南應大官網主色紫 `#854D92`（2026-10-14 從 tut.edu.tw 樣式表與校徽實測；官網文字沒寫色碼）。
- 後台 `/tut/team/a/<簽章短碼>` 已收進大樹作品集（活動後台），可隱藏／刪除／新增座位／一鍵複製專屬連結；公開頁收進「bymyway自架版」。
- 預放的介紹來源：4 個網頁（鄭儷絲 CICA、陳彥玲 northern-tw、謝志賓 nmda——網頁沒他本人只放協會介紹、林丁禾）、「為你轉身」（李中閔、施正益）、百人導師資料庫（林丁禾簡介、江睿翔、林士民照片）。全部標「待本人補充」，本人存檔後自動拿掉。
- 名字確認：**施正益**（教練親口；記憶牆原寫「施正義」已改，程式有自動改名）。
- 🔴 **本人上傳的照片存在 `event-signup/tut_team_uploads/`，已 .gitignore、不在 git**——要備份時別漏。資料表 `tut_team_members` 在 `event.db`。

**教練說「移植」＝複製過來、原處保留**（顧問團、百人導師、為你轉身都是這個用法）。

**真貴籌備會 5 位助理大使**（楊仁豪、康文彬、楊智帆、黃智宏、李孟哲）
- 他們是真鑽分會的，楊仁豪是真鑽現任**主席**、康文彬導師協調人，所以我**複製**進真貴（chapter 9），真鑽原處保留；連同簡介、大頭照、一頁式簡報圖（`ppt_filename`）、新的專屬連結。沒複製他們的真鑽職務、金牌、燈號分數。
- 只改了 `bni-chapters/chapters.db`（不在 git）；備份 `chapters.db.bak-before-zhengui-ambassadors-20261014`。教練若要從真鑽拿掉，要另外處理（職務與金牌資料會跟著失去，先問清楚）。

**Why:** 下次有人問「他們怎麼在兩個分會」「南應大頁資料放哪」，不用重查。
**How to apply:** 動南應大頁先讀 `tut_team.py` 檔頭；真貴／真鑽成員異動前先看上面的備份名。相關：[[reference-bni-member-personal-edit-link-two-repos-2026-10-14]]
