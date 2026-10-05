---
name: reference-chapter-page-glory-hidden-by-spirit-and-gold-medal-section
description: bni-chapters 分會頁「分會之光」數據卡後台新增卻看不到＝因為模板規則是有「分會精神」就不顯示分會之光；金質獎章區另做成獨立資料表，改名單跑 seed_gold_medals
metadata:
  type: reference
---

**為什麼教練在後台「分會之光」新增數據卡，主頁看不到（2026-10-05 查到根因）**：`templates/chapter.html` 是 `{% if spirit %}分會精神{% elif stats %}分會之光{% endif %}`，而 9 個分會都有 9 筆分會精神（chapter_spirit），所以分會之光（chapter_stats）永遠被擋掉。後台存進去沒壞，只是頁面不顯示。要同時顯示得改模板規則，會連動真誠（6 筆）、真AI（5 筆）等分會被隱藏的舊數據卡一起跳出來，所以沒有直接改。

**金質獎章區（教練 10/05 14:24 交辦）**：分會夥伴底下的獨立區塊，資料在 `member_gold_medals`（一人一筆，level 1＝一金、2＝雙金）＋`chapter_gold_section`（有列才顯示該分會的區塊）；獎章照 `static/img/gold-{1,2,series}.jpg`。改得主名單：改 `seed_gold_medals_2026-10-05.py` 的 GOLD 再跑一次（INSERT OR REPLACE）。說明文字寫在 `templates/chapter.html`（6 位一金、12 二金、18 三金、24 四金；台灣紀錄保持人 13 金）。只開了真鑽（10 位）、真誠（鄭綉美一金、陳佩君雙金）、真鑫（沒有得主，只顯示說明）。

**教練口語**：「鄭秀美」＝座位名字「鄭綉美」。簡報頁碼：真鑽 PDF 第 2 頁是一金 6 位、第 4 頁是雙金 3 位，陳淑玲是剛拿到的第 7 位一金（教練口述）。

相關：[[project_business_club_game_design_principles_2026-10-03]]（探測器金質累加規則，目前沒把這批得主寫進探測器，因為只知道等級不知道實際推薦人數）。
