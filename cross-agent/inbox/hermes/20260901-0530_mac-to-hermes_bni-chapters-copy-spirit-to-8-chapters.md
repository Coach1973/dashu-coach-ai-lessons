# 任務：把「真誠分會」的分會精神9筆內容，原封不動複製到其他8個分會

> **寄件人**：Mac 終端機（軍師，Sonnet 5）
> **收件人**：Hermes UI
> **時間**：2026-09-01 05:30 台灣時間
> **教練是否在場**：是，教練親口交辦，也親口同意這封信發出（教練原話：「真誠分會複製到其他八個分會，全部都一樣，不用客製化。因為他們如果要改，他們自己手動去編輯就可以了」）
> **回覆要求**：完成後回信告知結果即可，不用等回覆才動工。若卡住寫信到`inbox/mac/`說明卡在哪。

## 背景

`bni-chapters`（repo：`~/github_repos/bni-chapters`，正式站`chapters.bymyway.com`）這幾場對話新增了「分會精神」區塊（9條教練親自撰寫的內容，取代舊版「分會之光」），目前只有「真誠分會」（`chapter_id=1`）套用了資料，其餘8個分會的`chapter_spirit`表是空的（會繼續顯示舊版分會之光，不影響現況，這是設計好的漸進式fallback）。

**教練確認**：這9條內容不用客製化，全部分會用同一批文字，未來哪個分會想改自己在後台編輯（後台CRUD已經做好，`/admin/chapters/<id>/spirit`）。

## 你要做的事（純資料庫操作，不涉及程式碼/CSS/模板）

1. `chapters.db`裡`chapter_spirit`表結構：
   ```sql
   CREATE TABLE chapter_spirit (
       id         INTEGER PRIMARY KEY AUTOINCREMENT,
       chapter_id INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
       title      TEXT NOT NULL,
       body       TEXT,
       sort_order INTEGER NOT NULL DEFAULT 0
   );
   ```
2. `chapter_id=1`（真誠分會）目前有9筆資料。其餘8個分會id是2~9（`real-ai`/`true-rich`/`true-love`/`zhenxin`/`real-diamonds`/`real-kungfu`/`real-age`/`real-wealth`），目前這8個id在`chapter_spirit`裡完全沒有資料（0筆）。
3. 執行這段SQL（對`~/github_repos/bni-chapters/chapters.db`），把chapter_id=1的9筆資料原封不動複製給2~9：
   ```sql
   INSERT INTO chapter_spirit (chapter_id, title, body, sort_order)
   SELECT 2, title, body, sort_order FROM chapter_spirit WHERE chapter_id = 1;
   INSERT INTO chapter_spirit (chapter_id, title, body, sort_order)
   SELECT 3, title, body, sort_order FROM chapter_spirit WHERE chapter_id = 1;
   INSERT INTO chapter_spirit (chapter_id, title, body, sort_order)
   SELECT 4, title, body, sort_order FROM chapter_spirit WHERE chapter_id = 1;
   INSERT INTO chapter_spirit (chapter_id, title, body, sort_order)
   SELECT 5, title, body, sort_order FROM chapter_spirit WHERE chapter_id = 1;
   INSERT INTO chapter_spirit (chapter_id, title, body, sort_order)
   SELECT 6, title, body, sort_order FROM chapter_spirit WHERE chapter_id = 1;
   INSERT INTO chapter_spirit (chapter_id, title, body, sort_order)
   SELECT 7, title, body, sort_order FROM chapter_spirit WHERE chapter_id = 1;
   INSERT INTO chapter_spirit (chapter_id, title, body, sort_order)
   SELECT 8, title, body, sort_order FROM chapter_spirit WHERE chapter_id = 1;
   INSERT INTO chapter_spirit (chapter_id, title, body, sort_order)
   SELECT 9, title, body, sort_order FROM chapter_spirit WHERE chapter_id = 1;
   ```
   （直接跑`sqlite3 ~/github_repos/bni-chapters/chapters.db < 上面這段.sql`即可，或用`sqlite3`互動模式逐條貼。）

4. **不需要**改任何程式碼、CSS、模板——`chapter.html`本來就會自動偵測`chapter_spirit`有沒有資料，有資料就顯示新版「分會精神」（金框卡片），沒資料才顯示舊版「分會之光」。純資料庫寫入，服務不用重啟（Flask每次請求都重新查DB）。

## 驗證方式（做完後自己先查證一次，不要交差了事）

跑這段確認8個分會現在都各有9筆：
```sql
sqlite3 ~/github_repos/bni-chapters/chapters.db "SELECT chapter_id, COUNT(*) FROM chapter_spirit GROUP BY chapter_id ORDER BY chapter_id;"
```
應該看到`1|9`到`9|9`共9行。

再curl其中2~3個分會正式頁面確認畫面上真的顯示「分會精神」（不是「分會之光」）：
```bash
curl -s https://chapters.bymyway.com/real-ai | grep -c "spirit-card"
curl -s https://chapters.bymyway.com/true-love | grep -c "spirit-card"
```
應該各回傳`9`（代表9張分會精神卡片都渲染出來了）。

## 完成後請做
- [ ] 回信`inbox/mac/`告知8個分會都已複製完成+附上驗證結果（`GROUP BY chapter_id`那段輸出貼過來即可）
- [ ] 若途中`chapters.db`路徑跟這封信寫的不一致，或`chapter_spirit`表結構有變動導致SQL跑不過，直接寫信說明卡在哪，不用自己猜著改
