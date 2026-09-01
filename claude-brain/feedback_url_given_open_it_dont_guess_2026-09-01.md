---
name: feedback-url-given-open-it-dont-guess-2026-09-01
description: 教練貼出具體URL要求「照抄」時，第一件事是curl/打開查看，不能憑名稱相似度聯想到別的系統就開始設計
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9b6d5e7c-c63c-44c9-ba78-b15d5ff918bb
  modified: 2026-08-31T22:52:25.863Z
---

教練貼`sincere.bymyway.com`要求「照抄這個網址」做來賓戰情儀表板，因為前幾棒剛做完`bni-chapters`的「真誠分會」(`chapters.bymyway.com/sincere`)，看到「sincere」就直接聯想過去、沒有打開網址查看，開始自行設計一套五維度資料庫+後台CRUD+公開表單防灌水機制。教練連續糾正3次（「想太複雜了」「跟後臺沒關係」「到底講的是不是同一回事」）才真正去curl查看，發現是完全獨立的系統（`~/github_repos/zhencheng-guests`，跟bni-chapters無關），浪費教練至少30分鐘，教練整晚沒睡在溝通、情緒嚴重受損。詳見[[試金石案例68]]。

**Why：** URL本身就是最強的規格來源，查一次的成本（幾秒curl）遠低於自己設計系統再被糾正重來的成本。名字相似不代表是同一個系統，這種情況下更需要查證，不是更不需要。

**How to apply：** 教練貼出具體URL/檔案路徑要求「照抄」「參考」「比照」時，收到當下第一件事就是打開查看實際內容，不得憑名稱相似度或過往經驗聯想跳過查證。連續被糾正超過1次還沒解決，就該停下手上的猜測方向，做最基礎的存在性查證，而不是在原本錯誤的方向上小幅修正。對應守則#09「先確認清楚再行動，不瞎猜」（執行合約最高頻痛點第二名）。
