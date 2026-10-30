---
name: reference-nmda-team-photos-live-in-mac-db-not-github
description: NMDA 理監事團隊頁的照片存 Mac 伺服器資料庫與上傳資料夾，不在 GitHub；換照片交 Mac 只改 photo_file；聯想網頁上傳會把空座位標成已填(2026-10-28)
metadata:
  type: reference
---

- 公開頁 `team.html`（GitHub `nmda` 倉庫，只有 index.html／team.html／assets）載入時讀 `/api/nmda/team/board`，照片網址是 `/nmda/team/photo/<檔名>`，檔案在 Mac `event-signup/nmda_team_uploads/`、欄位 `nmda_team_members.photo_file`。**只改 GitHub 不會換照片。**
- 網頁編輯網址上傳（建置模式 `/nmda/b/<碼>` 取得每人編輯連結）會呼叫 `update()`：強制 `filled=1`、重寫所有欄位、刪舊照片檔。22 位只有 5 位 filled=1，其餘 17 位會失去「簡介準備中」與「我是○○，補上我的簡介」按鈕。→ 換照片交 Mac，只 `UPDATE ... SET photo_file`，先備份 event.db。
- 巴哈只出海報（`poster_new_person.py` 印出 jpg 路徑為止），沒有自動放進團隊頁的步驟；歷來都是軍師手動放（`f7e666dc4`、`a9bd8b21c`、`d53f8b50d`）。
- 10/28 教練決定交給 Mac，聯想寫信；Mac 22:10 已換 21 位新海報（`0bdf9dabf`，只動 photo_file）。

**How to apply:** 教練再說換團隊頁照片＝Mac 做；聯想只寫信（放 inbox/mac，見 [[feedback-letters-to-junshi-go-to-inbox-not-outbox]]）。基礎機制見 [[project-nmda-board-team-page-2026-10-23]]。
