---
name: feedback-find-maxdepth-false-negative
description: find -maxdepth太淺會漏掉深層檔案，導致誤判「不存在」；有成本的結論（要教練做架構決策）需交叉驗證才能下
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f7125d75-b0da-4c6a-92ba-99012f90285d
  modified: 2026-08-17T20:23:02.301Z
---

用 `find <dir> -maxdepth N -iname "..."` 查檔案時，若沒有先手動數清楚目標路徑相對於搜尋起點有幾層，很容易少算一層，導致明明存在的檔案被判定為「查無結果」。

**Why**：2026-08-17，教練問 coach888 要不要加一個私有後台頁面的連結，我用 `find /Users/bymyway -maxdepth 4 -iname "bni_training_admin.html"` 查無結果，就直接告訴教練「本機沒有這檔案，需要決定架 server 或其他 URL 方案」。教練隨後貼出另一台機器（聯想）的說法「檔案早就存在、git pull 後直接開就好」，兩邊說法對不上，要求釐清。重新查證發現：真實路徑是 `~/.openclaw/workspace/claude-brain/data/bni_training_admin.html`，從 `/Users/bymyway` 起算要 5 層，我的 `-maxdepth 4` 剛好少一層，檔案其實早就存在且已 git 同步，我的結論是查證方法有瑕疵造成的錯誤，不是真的架構問題。已寫入 workspace 試金石案例 59。

**How to apply**：
1. 下 `find -maxdepth` 前先手動數一次目標路徑的層數，抓不準就乾脆不限深度查一次（範圍夠小成本不高）。
2. 「查無結果」不能直接當「不存在」的鐵證——尤其這個結論要拿去支撐一個有成本的建議（重新架設方案、放棄某做法、要用戶做決策）時，一次查詢不夠，要用第二種方法（如逐層 `ls`）交叉驗證後才能下結論。
3. 跨機器協作情境下，「這是另一台機器剛做好的東西」不能自動推論「這台機器還沒有」——若整個工作目錄本身是 git 同步的，「剛做好」跟「還沒同步過來」是兩件要分開查證的事，不能靠直覺合併判斷。

Related: [[feedback_check_master_index_before_claiming_cant_find]]（同屬「說查不到之前要先做窮盡查證」錯誤家族，那條講的是漏查萬用索引檔，這條講的是查詢指令本身的深度/範圍設錯）
