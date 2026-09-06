# namecard-db — 名詞對照表

> 目的：讓AI跟教練/軍師/特助講同一種語言，減少每次交接都要重新解釋一次術語。
> 靈感來源：研究 mattpocock/skills 的 `CONTEXT.md` 共享語言做法（2026-07-24建立）。
> 部署細節看 `README.md`（已經寫得很完整），這份文件只補「名詞」跟「架構決策為什麼這樣」。

## 這是什麼

教練的名片搜尋＋產業鏈媒合系統。名片照片（教練/孔大哥/佩佩老師丟進Amber私有雲「名片媒合中心」資料夾）
→ AI直接看懂照片內容（不是傳統OCR）→ 存進SQLite → 手機可查的搜尋網頁 + 產業媒合建議頁。

## 核心名詞

- **卡片（card）**＝`cards`表一筆記錄，一張名片一筆。**不是名片實體**，是AI從照片擷取出的結構化資料。
- **配對（match）**＝`matches`表一筆記錄，代表AI判斷「這兩張名片的產業類別彼此適合互相認識」（上下游或異業合作），顯示在`/matches`頁。跟「重複名片去重」是兩件事，不要混淆——去重是`dedup.py`的工作，配對是`match.py`的工作。
- **watch（監看）**＝`watch_and_extract.py`，偵測名片媒合中心資料夾有新照片就自動觸發擷取。**2026-07-13後已改成真事件觸發**（macOS launchd WatchPaths監看SMB掛載資料夾變更），不是背景輪詢——這是[[feedback_event_driven_not_polling_pattern.md]]這個坑修過的地方，改動這支腳本前先讀那份記憶檔。
- **extract（擷取）**＝`extract.py`/`paddle_extract.py`，把照片轉成`cards`表欄位。`paddle_extract.py`是PaddleOCR備援路徑（有獨立的`paddleocr_venv`），主要路徑是直接餵給AI（Anthropic API）看圖辨識，不是傳統OCR。
- **名片媒合中心**＝Amber私有雲（192.168.0.35）裡的一個共用資料夾，教練/孔大哥/佩佩老師上傳照片的地方，SMB掛載（不是WebDAV，細節見`reference_amber_nas.md`）。
- **通訊錄（directory_contacts表，2026-09-07新增）**＝跟`cards`分開的表，一張照片對應多位聯絡人（獅子會/扶輪社/同濟會等社團的會員名冊），不是「一張名片=一筆」的結構。`extract.py`的`_looks_like_roster()`用「社團關鍵字+3組以上電話樣式」判斷是不是通訊錄，是的話走`ROSTER_SYSTEM_PROMPT`逐人萃取姓名/電話/專業類別/地址，`cards`表只留一筆`status='roster'`的標記列(避免重複處理，不會出現在搜尋結果)。

## 架構決策：為什麼這樣設計

- **事件觸發，不用輪詢**：這是本系統唯一一條被教練親自糾正過4次的鐵律——聽到「多久檢查一次比較好」這種念頭要先反問自己能不能直接事件觸發
- **必須在Mac mini跑，不是聯想/ACER**：因為只有Mac能連到Amber私有雲的SMB掛載，且已裝Python
- **🔴🔴🔴 任何呼叫MiniMax API的地方都必須先過`scripts/minimax_batch_guard.py`的`guard_call()`**：2026-08-26案例65教訓（`chain_matcher.py`批次跑428人沒節流沒快取，一次燒150萬token把帳號5小時4500次額度全部打滿，教練所有服務停擺3小時），教練2026-08-27親口拍板「畫下一條紅線」。這不是建議，是寫死在程式碼裡的硬性上限（批次腳本專屬2000次/5小時，教練拍板的分配是2000留給批次腳本、2500留給三個LINE帳號的即時互動，越線直接拋`MiniMaxBatchGuardError`中止並發Telegram通知，不可用try/except吞掉）。已接上`chain_matcher.py`／`extract.py`／`match.py`三個真正的API呼叫點。**任何新增會呼叫MiniMax的程式碼（不限這個專案，整個workspace都適用同一套規則），第一行動作就是`from minimax_batch_guard import guard_call`並在呼叫`client.messages.create()`前呼叫`guard_call("<呼叫端名稱>")`，沒有例外。**

## 已知狀態（寫給下一場軍師）

- 查名片直接跑 `python3 query.py "<關鍵字>"`，不用自己寫SQL
- 教練/孔大哥/佩佩老師傳照片＋訊息含「名片」二字（LINE或Telegram皆可）→ hook自動處理，不用手動搬檔案，手動複製會造成重複記錄
- 若教練問「怎麼還沒處理」，先查`amber-watch.log`確認有沒有觸發過，或查`namecards.db`的`cards`表筆數變化
