---
name: feedback_check_existing_naming_convention_before_new_subdomain_2026-09-01
description: 新建BNI分會相關子網域前，必須先查chapters.bymyway.com/admin既有的英文代號對照表，不能自己音譯或猜命名
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 529f493d-3a80-43be-815c-8e4a5987a014
  modified: 2026-09-01T09:45:38.825Z
---

部署真鑽(邀約來賓戰情儀表板)跟真貴(邀約來賓戰情儀表板)的正式網址時，沒有先去查`chapters.bymyway.com`分會一覽表裡教練已經設定好的英文代號，自己用拼音音譯成`zhenzuan.bymyway.com`/`zhengui.bymyway.com`，跟教練既有系統脫節。教練當場糾正：真鑫=zhenxin是唯一用拼音的，真鑽=real-diamonds、真貴=real-wealth，這些代號早就存在（`chapters.bymyway.com`底下的`/real-diamonds`、`/real-wealth`路徑），部署前完全可以查得到。

**Why**：教練已經為9個分會建立過一套完整的英文代號系統（`chapters.bymyway.com`的路由slug），新的相關服務理應延用同一套代號，維持跨系統一致性；憑印象/音譯自創命名，會讓同一個分會在不同系統下有兩套不同英文名字，長期造成混淆與維護負擔。

**How to apply**：往後任何要幫BNI大台南南區分會建立新子網域/repo/服務時，第一步永遠是`curl chapters.bymyway.com/`列出既有連結，或直接查`chapters.bymyway.com/admin`後台的分會清單，取得該分會的官方英文slug，再拿來用，不得自己音譯或另創新名字。已修正：`real-diamonds.bymyway.com`(真鑽)、`real-wealth.bymyway.com`(真貴)，舊的錯誤DNS紀錄`zhenzuan.bymyway.com`/`zhengui.bymyway.com`已刪除。

Related: [[feedback_url_given_open_it_dont_guess_2026-09-01]]（同一種「查證前先查」的教訓，那次是查URL本身，這次是查命名規則）
