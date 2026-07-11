---
name: project-namecard-db-2026-07-12
description: 教練要把Amber私有雲名片資料夾裡1000~2000張名片建成可搜尋資料庫+產業鏈媒合系統，2026-07-12已寫好程式碼推上雲端共用大腦但尚未實機測試
metadata:
  node_type: memory
  type: project
  originSessionId: 836b136b-e6ce-4296-a039-b22d27e1b827
---

教練的工作團隊隨時拍照上傳名片到Amber私有雲的專屬資料夾，教練想要AI接手做三件事：
① 自動辨識欄位（姓名/電話/Email/LINE/公司/地址）② 搜尋介面（姓名/公司/地區/產品服務/專業類別）
③ 自動媒合名片之間的產業鏈關聯性。

**查證結果（2026-07-12）：** GitHub上查過一輪，沒有現成完整方案可直接引進。既有公開專案
（BizCardX系列等）幾乎都是英文OCR課程作業等級，不支援繁體中文/LINE ID，也沒有搜尋介面
跟產業鏈媒合功能。判斷自建比改別人的半成品划算。

**已建置（尚未實機測試，聯想這台Windows機器沒裝Python，無法執行驗證）：**
- 位置：`mac-openclaw-workflows/namecard-db/`（已commit+push，commit `966a618f`）
- 架構：Claude視覺直接讀名片照片抓欄位（非傳統OCR）→ SQLite(`namecards.db`) → Flask搜尋網頁
  → 產業鏈媒合（先把類別去重、一次AI呼叫判斷哪些類別彼此該互相認識，再回頭批次配對名片，
  避免對2000張名片做O(n²)全量AI比對）
- 部署目標是Mac mini（已有Python、且SMB連得到Amber私有雲），對外查詢建議比照現有
  「小龍蝦專線」cloudflared tunnel技術另開一條路由，讓教練出門用手機也能查
- 完整部署步驟見`namecard-db/README.md`

**教練已確認的兩個關鍵決定：**
1. 使用情境選「外出時手機也要能查」（非只在家用電腦查）
2. 名片上「不少有印產品/服務標語」，代表產業鏈媒合可以同時參考公司名稱+名片上的標語文字，
   不是只能靠公司名稱瞎猜

**尚待進行：**
- 教練提供Amber私有雲裡名片資料夾的實際路徑/名稱（README裡目前是佔位路徑）
- 第一次部署務必先用10~20張名片小量測試辨識品質，再處理全部1000~2000張
- 需要在有Python 3.10+的機器（建議Mac mini）安裝`requirements.txt`後才能真正驗證程式碼是否正確

Related: [[reference_amber_nas]], [[project_media_resource_center_2026-07-09]], [[reference_xiaolongxia_line_tunnel_cloudflared]]
