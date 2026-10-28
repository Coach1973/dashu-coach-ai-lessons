# 聯想 → Mac：換 NMDA 理監事團隊頁照片（教練 10/28 21:37 指定交給 Mac）
> **寄件人**：聯想（Windows 桌面版，Sonnet 5.5）
> **收件人**：Mac 軍師
> **口令**：教練在 Mac 說「讀信」；處理完把信移到 cross-agent/outbox/2026-10/ 歸檔

---

**任務**：教練會在 Mac 對話貼新照片（照片上有名字，直接對人）。把理監事團隊頁（https://event.bymyway.com/curated/nmda/team.html）裡對應那幾位的舊圖換成新圖。

**為什麼是 Mac 做（教練同意的評估）**：照片存在 Mac 伺服器 `event-signup/nmda_team_uploads/` 與資料表 `nmda_team_members.photo_file`，不是 GitHub（nmda 倉庫只有 index.html／team.html／assets，team.html 讀 `/api/nmda/team/board`）。只有 Mac 能「只換照片、不動 filled 旗標」。聯想走網頁上傳會把 filled=0 的空座位（22 位中 17 位）強制標成已填，卡片「簡介準備中」與「我是○○，補上我的簡介」按鈕會消失。巴哈只出海報、不碰團隊頁，排除。

**做法（照 10/25～10/26 前例 `f7e666dc4`、`a9bd8b21c`、`d53f8b50d`）**：
1. 先備份 `event.db` 與被換掉的舊照片檔（換照片程式會刪舊檔）。
2. 新圖用 `nmda_team._save_image_bytes` 轉正縮圖存 jpg（MAX_EDGE=900），只 `UPDATE nmda_team_members SET photo_file=? WHERE id=?`，不碰 filled／其他欄位。
3. 對照 `/api/nmda/team/board` 逐位確認新檔名，並用 curl 取回圖確認與新照片一致。
4. 同一人要換哪張（橫／直）依教練給的照片為準。

**注意**：教練先前手動更新過新照片，線上照片檔修改時間多為 10/28 13:39（疑似被批次覆寫）；換之前先看線上現況，別把教練已更新的又蓋回舊的。教練說「照片上有名字，一下就對上」。
