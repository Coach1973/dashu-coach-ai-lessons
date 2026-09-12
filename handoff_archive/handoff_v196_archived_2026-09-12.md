# 軍師接力棒 · 2026-09-11 v196（Mac桌面版 Sonnet 5，FB App Review精簡權限+示範錄影兩次失敗+關鍵發現pages_read_engagement審核前完全不可用）

> 建立時間：2026-09-11 15:55 ~ 16:34（台灣時間）
> 上一棒：v195（Mac桌面版，FB App Review表單填寫：圖示透明背景修復+權限精簡建議）
> 本棒主軸：**教練同意移除3個沒用到的權限，軍師直接操作Meta App Dashboard完成移除；教練要求軍師教他錄示範影片，過程中軍師直接控制教練已登入的真實Chrome示範`pages_show_list`(查粉專清單)+`pages_manage_posts`(真實發文+刪除測試貼文)，但意外發現`pages_read_engagement`在App通過審核前，即使是粉專管理員本人也完全無法呼叫，這解釋了「同一份申請裡有些權限錄得出示範、有些錄不出來」的根因。教練兩次錄影都沒錄好，已將失敗檔案移到垃圾桶(非永久刪除)，晚點再重錄。**

## 🎯 本場戰果

### 1. 移除3個未使用的App Review申請權限
教練同意v195建議，軍師直接操作`developers.facebook.com/apps/1050871501278089/app-review/submissions/`頁面（教練口頭同意截圖後才能精準定位垃圾桶圖示），逐一移除`pages_manage_metadata`／`pages_messaging`／`business_management`，確認清單剩下`pages_manage_posts`／`pages_show_list`／`pages_read_engagement`／`public_profile`四項真正有用到的權限。

### 2. 錄影示範分工模式確立：AI操作教練錄影
教練提出「我不會錄影，要你教」，軍師說明Mac內建`⌘+Shift+5`錄影操作步驟，並提出由AI直接控制教練已登入的真實Chrome示範功能、教練只需按錄製/停止的分工——經教練確認「畫面上看不出是誰操作，用的是真實帳號真實資料，不算造假」後，教練同意採用此模式。

### 3. 兩次示範錄影，中途發現關鍵技術限制
用Graph API測試工具(`developers.facebook.com/tools/explorer`)實際示範：`pages_show_list`(呼叫`me/accounts`，成功列出教練管理的所有真實粉專)、`pages_manage_posts`(POST到「大樹教練」粉專`me/feed`，成功發布真實測試貼文並取得貼文ID)。**過程中發現`pages_read_engagement`(查詢貼文按讚/留言數)不管用「用戶權杖」或「粉專權杖」呼叫，都固定回傳OAuthException「此端點需要pages_read_engagement權限」**——這代表這個權限在App通過審核前，連粉專管理員自己都無法測試，屬於Facebook對「讀取互動數據」類權限的既定嚴格限制，不是操作錯誤，也解釋了為何同一份申請裡各權限的可示範程度不一致。示範用的測試貼文透過API的DELETE呼叫失敗(`error_subcode 33`)，改用Facebook Page後台「切換為粉專身分」→貼文選單「移到垃圾桶」的一般UI操作成功刪除。

### 4. 兩次錄影皆失敗，錄影檔已移至垃圾桶
教練回報兩次錄影「都沒錄好」，要求刪除。查明桌面兩個`.mov`檔(97MB+138MB)，依安全原則**用`mv`移到`~/.Trash/`而非`rm`永久刪除**(可復原)，已驗證桌面已清空，教練晚點會再重新錄製。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **`pages_read_engagement`等讀取互動數據類權限，在App通過審核前即使管理員本人也完全無法呼叫**——不同於`pages_manage_posts`/`pages_show_list`這類「發文/列清單」權限在Standard Access下對管理員自己開放。已補進`reference_fb_graph_api_app_review_required_for_public_visibility_2026-09-11`，往後遇到App Review示範影片「某個權限怎麼測都失敗」，先用Graph API測試工具跑一次真實呼叫確認是Access Level門檻問題還是操作問題，不要在同一個死角反覆嘗試。
2. **App Review示範影片可由AI操作教練的真實登入瀏覽器完成，教練只需負責錄製/停止**——畫面錄影看不出操作者是誰，只要是真實帳號真實資料的真實功能展示，不算造假示範，此分工模式已寫入同一則記憶供未來類似任務參考。
3. **危險指令鐵律的「刪除」原則同樣適用於教練個人檔案**——教練要求刪除失敗錄影檔，遵照系統規則不做永久刪除(`rm`)，改用`mv`到`~/.Trash/`(等同拖進垃圾桶)，保留復原可能性。

## 📋 下一場開工先做
1. **教練重新錄製App Review示範影片**：`pages_show_list`+`pages_manage_posts`用Graph API測試工具示範法已驗證可行，`pages_read_engagement`改用文字說明取代影片(教練尚未確認要不要，軍師已提議代寫)。
2. 續寫`pages_show_list`+`pages_read_engagement`的使用說明文字（v195遺留待辦）。
3. 大台南策展中心15篇店家上線通知是否要重貼、BNI Connect打勾出席、更新BNI培訓總覽資料庫、Amber TimeMachine清理、MEMORY.md索引瘦身、後台帳密清單、materials系統42份教材待勾選（沿用多場舊待辦）。
4. E16接力棒瘦身：本次已把v192+v193搬進`handoff_archive/`，主檔維持v194+v195+v196三棒。

## 🔑 本場commit
本場為Meta App Dashboard表單操作+Graph API示範+本機檔案清理，未產生git commit（App Review設定變更不在版控範圍；記憶檔更新見下）。記憶：`reference_fb_graph_api_app_review_required_for_public_visibility_2026-09-11`(更新，補充pages_read_engagement審核前限制+錄影分工模式)。
