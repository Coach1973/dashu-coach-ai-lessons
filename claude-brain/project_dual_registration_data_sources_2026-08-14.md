---
name: project-dual-registration-data-sources-2026-08-14
description: 教練活動報名資料其實有兩套不同意義的資料源(現場簽到vs線上報名)，後者完全沒有資料庫落地，已backfill 30筆真實資料並在USER.md記錄查詢SOP
metadata: 
  node_type: memory
  type: project
  originSessionId: 7c3bfad2-6f16-4c09-ab1c-23bcf3e61ae2
  modified: 2026-08-13T18:30:27.393Z
---

教練問「幫我統計各場次報名幾人」，一開始我只查了`event-signup/event.db`的`events`+`signups`表，回報一批數字（如AI微論壇7/29=56人）。教練點破這只是**現場數位簽到**（簽到加輪盤系統，掃碼/填手機才算）的人數，跟他真正在意的**網站線上報名**（填表單當下就算，不用到場）是兩回事，後者完全查不到。

**查證確認的架構真相**：多個獨立網站（大樹小講bigtree-tw、AI微論壇ai-talk、mentor100等，至少6個repo有引用）的報名表單，全部共用同一支中樞Netlify function `https://sme-register-fn.netlify.app/.netlify/functions/register`，這支function**純轉發LINE/Telegram通知、完全不落地任何資料庫**——這不是猜測，是之前session已查證過的事實（見`feedback_cannot_delete_coach_line_messages`同一次查證）。所以這批「線上報名」資料原本100%只活在教練LINE/Telegram收到的「📋新報名通知」訊息裡，AI完全讀不到，教練得自己人工翻訊息數。

**已處理**：教練直接把30筆真實通知文字貼給我，已解析並insert進`event.db`新建的`advance_registrations`表（欄位：session_label/name/company/phone/email/registered_at）。正規化後統計：AI微論壇嘉義場(8/28)=12人、大樹小講8/26=7人、8/21=3人、8/25=3人，其餘個位數。查詢SOP已寫進`USER.md`。

**已知缺口，尚未解決**：`sme-register-fn`本身還沒修復成會自動寫入資料庫，代表這張表目前是**一次性backfill**，之後新的線上報名不會自動出現，除非①教練繼續手動貼通知文字來backfill，或②找時間依教練既有Netlify部署SOP（本機測試給教練看→教練說「推」才上線）修好這支function本身——但它是6+個網站共用的中樞，貿然改動風險高，這件事故意沒有在這場深夜對話裡衝動去做。

**Why**：教練的核心訴求「記住用戶的話才叫在乎」延伸到這裡就是「別讓我為系統本該做的事做人工苦工」——跟[[project_line_per_user_memory_standardization_2026-08-14]]同一條精神脈絡，只是這次的缺口在資料落地層，不是agent記憶層。

**How to apply**：下次教練問「報名/簽到統計」，先確認他要的是「現場簽到」還是「線上報名」，兩套資料完全不同來源不能混算。若教練提到`sme-register-fn`要修復成自動落地，記得那是共用6+網站的中樞function，改動前務必走完整Netlify部署三步驟，不能因為「順手」就跳過確認直接推。
