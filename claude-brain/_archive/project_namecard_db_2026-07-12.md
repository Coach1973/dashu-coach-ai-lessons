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

**2026-07-12 Mac已完成實機部署與驗證：**
- Amber SMB連線debug波折：教練Amber帳號`bymyway7`的Finder連線多次「跳出登入視窗又立刻消失」，
  查系統log證實是`smb_iod_start_reconnect`/逾時(`iod is dead`)真實網路層問題，不是教練操作或
  AI指令的錯；同時發現AI自動觸發`open smb://`指令會跟教練手動操作互相干擾，最後改成AI完全
  不碰、教練自己從頭操作Finder才穩定連上。教訓寫入[[feedback_password_boundary_vs_courier_resolution]]
  同系列：即使AI技術上能從Keychain取出明文密碼（已實測`security find-internet-password -w`可行），
  仍堅持不用它做登入，界線不因技術可行性鬆動。
- 名片資料夾實際路徑：教練手機App上傳的10張測試名片落在`/Volumes/home/名片媒合中心`
  （不是Photos分享），Amber帳號密碼需教練自己在Finder登入一次並勾選記住密碼。
- API金鑰：程式原寫死`claude-sonnet-5`(Anthropic官方)，實測cc-switch裡的ET(echotoken,404)、
  aiprimetech(Permission Denied)兩組都連不上，改用**MiniMax-M3**（無限Token，文字+視覺辨識
  皆實測通過），`extract.py`/`match.py`改讀`NAMECARD_MODEL`環境變數而非寫死。
- 小量測試(10張)結果：全數成功辨識，2張status=ok、8張status=needs_review(設計上會標記
  不確定欄位如傳真號碼/模糊字跡，非辨識失敗)。
- 產業媒合(match.py)：10種類別跑出14組候選配對，寫入matches表成功。
- 搜尋網頁：port 5000被macOS AirPlay佔用，改用**5050**，`http://localhost:5050`正常運作。
- 背景常駐：`~/Library/LaunchAgents/com.coach.namecard-watch.plist`已裝載運行(launchctl load)，
  每60秒自動掃新名片，教練丟名片免開終端機。
- **未完成**：手機外部查詢路由（cloudflared加一條指到localhost:5050的路由）——這條通道是
  小龍蝦LINE命脈(見[[reference_xiaolongxia_line_tunnel_cloudflared]])，設定在Cloudflare雲端
  非本機檔案，AI沒有API Token/後台存取權限，故意不碰，留給教練自己在Cloudflare後台加，
  或提供API Token後再處理。
- SS(synterolink)金鑰：教練原key回傳「GROUP_DELETED」(帳號分組已刪除)，教練已自行換新key
  並確認連上；cc-switch裡的synterolink設定已同步改成內嵌api_key格式(比照echotoken)。

**2026-07-12 追加：正反面名片自動合併(dedup.py)**
教練發現「鄭勝光/TFS」兩張照片是同一張名片的正反面，卻被拆成兩筆獨立紀錄。新增
`dedup.py`：用公司名稱關鍵字重疊比對抓正反面配對（先排除「有限公司」「股份」等
通用字），自動合併進同一筆、背面照片記進新增的`extra_images`欄位。已整合進
`watch_and_extract.py`每次掃描後自動執行，非一次性手動修正。**技術教訓**：原本
照教練指示用AI(MiniMax-M3)做yes/no合理性判斷，實測同一組資料重複問三次答案
不一致(2否1是)，不夠可靠，改用純關鍵字重疊的確定性判斷。commit `974c5e036`。

**2026-07-12 待辦（教練指定下一場新對話框執行，今晚太累不做）：**
教練要「雙通道」——LINE跟Telegram(小龍蝦)都要能傳名片/查詢名片，不是只做Telegram
單邊。技術背景：
- 查詢名片：簡單，小龍蝦本來就能讀這台Mac的檔案，直接查`namecards.db`即可，
  Telegram/LINE兩邊都適用同一套邏輯（因為都是同一個OpenClaw agent在回應）
- 上傳照片變名片：教練傳照片到小龍蝦（不論LINE或Telegram）會先落地
  `~/.openclaw/media/inbound/`，這裡是所有訊息類型混放的共用資料夾，需要寫一段
  串接邏輯：偵測到教練傳照片+觸發詞（例如「上傳名片」）→ 把該照片複製到Amber
  SMB掛載的`/Volumes/home/名片媒合中心`資料夾 → 現有背景服務會在60秒內自動接手
  處理，不需要額外碰AI辨識這塊
- 這件事完全不需要cloudflared/LINE tunnel路由，是完全不同的技術路徑（直接用
  OpenClaw既有的訊息接收機制），比原本規劃的「開網頁對外路由」更簡單、風險更低

**釐清：LINE tunnel(cloudflared)跟名片系統本來就沒有任何關聯**——上一輪對話教練
一度誤會兩者有關，已澄清：cloudflared只在「想用手機瀏覽器連進localhost:5050搜尋頁」
這個附加功能才用得到，教練決定改用小龍蝦雙通道後，這條路線已經不需要了，
cloudflared/LINE tunnel維持原樣不用動（它的既定用途是LINE官方帳號訊息進小龍蝦）。

Related: [[reference_amber_nas]], [[project_media_resource_center_2026-07-09]], [[reference_xiaolongxia_line_tunnel_cloudflared]], [[feedback_password_boundary_vs_courier_resolution]]
