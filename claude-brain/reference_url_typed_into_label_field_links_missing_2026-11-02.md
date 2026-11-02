---
name: reference_url_typed_into_label_field_links_missing_2026-11-02
description: 簡介視窗連結不顯示＝網址被貼進「修改標籤」欄存進 *_label 欄；bni-chapters 已加防呆，team-bymyway 尚無
metadata:
  type: reference
---

真聚籌備會（real-center）陳晏綜補資料後簡介沒連結，根因是 FB／Threads 網址存進 `*_label` 欄，`db.member_links` 只讀 `*_url`。張育慈同樣中招。修法：補資料＋ `_extract_member_links` 標籤欄是 http 網址就搬回網址欄（bni-chapters 3f9e2e2）。

**Why:** 表單有「修改標籤」欄，使用者誤貼網址。
**How to apply:** 以後「連結填了不顯示」先查 *_label 是否是網址；team-bymyway 有同樣未防呆的函式，需要時補。教練語音「彥仲」＝陳晏綜（未確認）、「證券／真劇籌備會」＝真聚。
