---
name: feedback_departed_members_removed_from_training_guests_overview_2026-10-13
description: 培訓總覽、來賓總覽不留離會的人；以三個戰情表在籍名單為準，補信用證時順便做；程式 BNI-Training/departed.py
metadata:
  type: feedback
---
教練 2026-10-13 定：**離會的人不要留在培訓總覽（Top10、未參加名單）和來賓總覽（邀約排行）**。補開信用證資料時，同一輪一起處理。

- 判斷：三個戰情表（zhenzuan／zhenxin／zhencheng-guests 的 members，left_chapter=0）的在籍名單；**不在名單上＝離會**。戰情表還沒標、但教練已說離會的（柯朝陽、徐偉倫…）寫進 `~/github_repos/BNI-Training/departed.py` 的 EXPLICIT_DEPARTED。
- 做法：新增離會者 → 改 EXPLICIT_DEPARTED → `cd ~/github_repos/BNI-Training && python3 departed.py && python3 region_build_html.py && python3 guests_build_html.py` → commit/push。chapters.bymyway.com/training、/guests 讀本機檔，推完立刻生效。`region_build_data.py`、`guests_build_data.py` 寫檔前也會自動套用。
- 🔴 同一個人在不同報表寫法不同（連晧宇＝連皓宇、楊為凱＝楊凱為、林尹渟＝林尹渰、姵彤蔡／蔡珮彤＝蔡姵彤），要放 ALIASES，否則在籍的人會被誤刪（10/13 我第一次就誤刪了三人，核對出席日期才抓到）。
- 沒處理（原本就有）：「林佳伶」與「林佳伶 Lavi」在培訓總覽被當兩個人。
- 信用證手工補登記錄見 `knowledges/2026-08-27_BNI信用証清查進度與續作方法.md`（10/13 補登第三批：范郁琪、薛如媛、徐偉倫）。

**Why:** 教練看近 6 個月培訓 Top10 發現已離會的柯朝陽排第五。
**How to apply:** 任何一次補信用證／得知有人離會，同輪更新 EXPLICIT_DEPARTED 並重建兩個總覽。

## 2026-10-13 補充：戰情表在籍以教練貼的名單為準（教練糾正）
- 我照資料庫的在籍旗標寫真鑫 10/01、10/08 出席，漏了徐偉倫已於 10/08 離會；教練貼 14 人名單才發現，當時我以為他還在。
- 規則：寫戰情表前，先請教練貼「目前在籍名單」逐一比對資料庫，不要只信資料庫旗標；離會、人數不對就先問，不要猜。
- 同一晚的做法：楊凱為、徐偉倫都標成離會（依教練名單），備份在 zhenxin_guests.db.bak-20261013-2333-before-roster-14。
- 副作用：下次重建培訓總覽、來賓總覽時，楊凱為會被 departed.py 當成離會者拿掉。
- **Why:** 名單不對，週報人數就對不上，教練要靠人數核對才信。
- **How to apply:** 寫週報前列出「應到＝在籍名單」給教練核對一次，數字對不上就停下來問。
