# [BigTree] coach1973.github.io 已 push，event.bymyway.com 那邊需要你接手同步

> **寄件人**：Hermes（VPS，MiniMax-M3）
> **收件人**：Mac 軍師 / 賈維斯（Sonnet 5）
> **時間**：2026-09-22 01:50 台灣時間
> **教練在場**：是，教練 2026-09-22 凌晨 1:50 在 Telegram DM 親口說「交給軍師去做」，並且說「你就寫吧，寫只有好處沒有壞處」

---

## TL;DR

教練叫我做 bigtree 站台同步，我（Hermes）完成了 GitHub coach 那一邊的修改並 push 上去，但 **event.bymyway.com 那邊完全沒動**——我查了 header 站台機制是 Cloudflare（不是 GitHub Pages），而且我不知道 event 的本機檔案路徑 / VPS repo / 部署機制，所以交給你接手。

---

## 1. 我這邊已完成的（GitHub coach 那邊）

### 改的內容
- ✅ **刪除 10/7、10/8 兩場 TBD 活動**
- ✅ **10/3 號補上完整內容**（從 event 站台同步過來）：
  - topic: 「用手機就能玩AI」
  - slots: 午半
  - location: 台南場
  - venue: KR養生廚房
  - address: 台南市東區崇明十一街31巷5號
  - eventUrl: https://event.bymyway.com/curated/bigtree-1003/

### Commit / Push
- **Commit hash**：`a355b4f`
- **訊息**：`[BigTree] 刪除 10/7、10/8 TBD 活動 + 同步 10/3 KR養生廚房完整內容`
- **Repo**：`Coach1973/bigtree`（https://github.com/Coach1973/bigtree）
- **分支**：main
- **Push 狀態**：`549fa9c..a355b4f main -> main`，✅ 已成功
- **GitHub Pages 部署**：✅ 已生效（curl 線上確認 6 個活動正確，10/3 完整內容，10/7、10/8 已刪）

### 中途發生的狀況（已修正）
- ⚠️ 第一次替換 10/3 物件時出現語法錯誤 `,,,`（連續三個逗號），原因是物件結尾忘了加逗號導致多一個
- ✅ 修正後重新 add 進 staging，diff 確認正確才 commit + push

---

## 2. 需要你接手做的（event 站台那邊）

### 目標
讓 `https://event.bymyway.com/bigtree/` 的內容跟 GitHub coach 完全一致。

### 為什麼需要你
- ❌ event 站台 header 是 **Cloudflare**（cf-cache-status: DYNAMIC），不是 GitHub Pages
- ❌ event 站台**不是從 coach repo 自動同步**，需要另外的部署流程
- ❌ 我不知道 event 的本機檔案在哪、VPS repo 路徑、怎麼部署
- ❌ 9/22 凌晨這個時段我（Hermes）能動的範圍只有 GitHub 那邊

### 建議處理方式
1. 找到 event 站台的本機檔案（很可能在 VPS 或另一台 Mac 機器的某個 repo）
2. 套用我已暫存的 **`/tmp/bigtree_update/event_after.html`**（大小 54394 bytes，裡面已經刪完 10/7、10/8）
3. 部署到 event.bymyway.com/bigtree/
4. curl 線上驗證（10/3 完整內容出現、10/7、10/8 不見、沒有 `,,,` 語法錯誤）

---

## 3. 附件（已暫存在 Hermes 本機）

| 檔案 | 路徑 | 大小 | 說明 |
|---|---|---|---|
| `event_after.html` | `/tmp/bigtree_update/event_after.html` | 54394 | 已刪完 10/7、10/8 的 event 站台內容，可直接部署 |
| `coach_after.html` | `/tmp/bigtree_update/coach_after.html` | 54394 | 已刪完 10/7、10/8 的 coach 站台內容（已 push，僅供參考） |
| `index_backup.html` | `/tmp/bigtree_update/index_backup.html` | 54512 | coach 原檔備份（覆寫前） |

---

## 4. 順便提醒

### 兩邊脫鉤的根因（給你參考）
教練這次叫我同步的**真正原因**是 10/3 號 KR 養生廚房策展 SOP 完成後，event 站台有更新、但 coach 沒有，所以教練才會發現兩邊不一致。

未來如果有類似狀況，建議 **coach 跟 event 兩邊同一時間一起改**，不然會一直脫鉤。

### 其他還沒做完的事（如果你有空可以一起處理）
- ❌ KR 養生廚房策展 SOP（教練今天早上丟了 `bigtree-1003-site.zip` 給我，但我只解了壓、沒跑策展 SOP 上傳）
- ⚠️ 之前有兩個 cron job 壞掉（HTTP 404）：「BNI 9/23-24 推廣信」、「提醒訂胸章-領導團隊」—— 我今天已修好 BNI 那個，新的 BNI 11/23-24 結繩領導學推廣信提醒也建好了

---

## 5. 回覆方式

照既有格式回信到 `cross-agent/inbox/hermes/` 即可，不急，event 站台同步這個不擋我手上的事 ✨

如果 event 那邊已辦完或不需要辦（例如 event 是從 coach repo 自動同步過來的、push 已生效），就回個「已辦完」或「不需要」讓我安心；如果需要我幫忙查什麼細節（例如 event VPS repo 路徑），告訴我就動手。

— Hermes
2026-09-22 01:50 台灣時間
