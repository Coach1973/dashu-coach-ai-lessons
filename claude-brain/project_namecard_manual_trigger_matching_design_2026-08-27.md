---
name: project-namecard-manual-trigger-matching-design
description: 名片系統產業鏈媒合永久改成手動點按鈕觸發，教練拍板不再批次自動跑，含/find搜尋頁+guest媒合入口設計
metadata:
  node_type: memory
  type: project
  originSessionId: 454fbcb4-70a8-4a88-832e-8ef2cbc35b65
  modified: 2026-09-02T09:03:36.764Z
---

2026-08-26案例65（MiniMax額度事故）後，教練親口拍板永久架構：「不要再把我的額度占完...重新製作一個按鈕，叫媒合，改成手動觸發，誰需要時再媒合。需要預先媒合的就是現有的92個會員」。

**設計定案**：
- 現任會員92人（唯一預先批次媒合的例外）：`namecard-db/bni_connect_import/run_chain_match.py`已改成只鎖`bni_note LIKE '%現任%'`，不會再掃到前會員。
- 前會員336人＋來賓3216人：一律靠網頁手動按鈕觸發，AI不主動批次跑。
- `/find`（`namecard-db/templates/find.html`+`app.py`的`find_page()`）：統一搜尋`cards`+`guests`兩表，結果卡片含身分標籤+聯絡方式+媒合按鈕，純瀏覽/搜尋零AI呼叫。
- `/guest/<id>/match`（`guest_match()`）：來賓版媒合入口，首次點擊才把該來賓轉一筆`cards`(用`source_guest_id`欄位+partial unique index防重複轉入)，接著沿用既有`/card/<id>/match`+`chain_matcher.py`邏輯，不重造一套。

**Why**：批次自動媒合的系統提示詞含905項分類詞庫(~5140 token)，300多次呼叫燒了150萬token，打到教練全部服務(小龍蝦/BNI小幫手/教練都在想什麼/VPS)共用的唯一MiniMax帳號額度上限。

**How to apply**：往後任何要幫`cards`或`guests`表新增/擴充媒合相關功能，一律遵守「瀏覽零AI呼叫、按鈕才觸發」原則，不要建議或恢復批次自動跑的機制，除非教練親口再次授權（且要限定範圍，例如這次的92人現任會員）。若要加新的資料來源進媒合系統（例如guests之外的另一張表），優先仿照guest_match()的「lazy-convert成一筆card再導去既有media流程」模式，複用既有infrastructure。

Related: [[feedback_insert_or_ignore_silent_failure_2026-08-27]]（同一批修復裡發現的資料寫入bug）、[[reference_bni_connect_guest_report_navigation_2026-08-27]]（來賓資料的正確抓取方法）、[[project_namecard_login_gate_and_guest_history_2026-09-02]]（2026-09-02存取控制改版，「瀏覽零AI呼叫」這條AI呼叫原則不變，但瀏覽本身現在需要登入）

**2026-09-02更新（不推翻上述設計，只是疊加一層）**：這篇寫的「純瀏覽/搜尋零AI呼叫」在AI呼叫層面依然成立不變，但**存取層面已改變**——教練這天要求全站（含`/find`搜尋、`/`首頁、`/card/<id>/match`、`/upload`）一律要登入才能用，不再對外公開瀏覽。詳見新記憶[[project_namecard_login_gate_and_guest_history_2026-09-02]]。
