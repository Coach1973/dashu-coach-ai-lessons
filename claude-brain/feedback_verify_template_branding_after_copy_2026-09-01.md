---
name: feedback_verify_template_branding_after_copy_2026-09-01
description: 複製既有repo模板建新分會網站時，只改title標籤不夠，要grep全檔案搜尋來源分會名稱確認沒有殘留品牌文字
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 529f493d-3a80-43be-815c-8e4a5987a014
  modified: 2026-09-01T10:21:57.742Z
---

真鑽(zhenzuan-guests)、真貴(zhengui-guests)兩個網站是複製真鑫(zhenxin-guests)的程式碼建立的，之前只驗證了`<title>`標籤跟curl抓到的title正確就回報完成，實際上模板內文（h1標題、大事紀標題、規則說明段落）都還殘留著「真鑫分會」字樣，教練實際點進網站才發現。

**Why**：curl只抓`<title>`標籤的驗證方式不夠全面，網頁內文任何地方都可能殘留來源模板的品牌文字，尤其是像h1、規則說明這種容易被忽略的區塊。教練直接使用產品發現這個問題，證明「查title」跟「教練實際體驗」是兩件不同的事。

**How to apply**：複製既有repo當模板建立新的分會/專案網站時，交付前必須：
1. `grep -rn "<來源分會名稱>" templates/ *.py` 全檔案搜尋來源名稱，逐一確認替換乾淨
2. 不只看title標籤，用`get_page_text`或Chrome實際看過整頁內容
3. 若模板有「統計期間」「特殊例外規則」這類寫死的具體日期/事件文字（例如真鑫的「8/20當週改為內訓」），也要一併確認新專案是否適用，不能連同品牌名稱一起照抄過去卻内容不符

Related: [[feedback_check_existing_naming_convention_before_new_subdomain_2026-09-01]]（同一場任務，另一種「複製模板沒改乾淨」的教訓）
