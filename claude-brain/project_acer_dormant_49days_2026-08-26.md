---
name: project-acer-dormant-49days-2026-08-26
description: 宏碁(ACER)機查證確認已49天未真正使用，信箱堆積未讀信、verbatim蒸餾自建立起零產出
metadata:
  type: project
  originSessionId: pending
  modified: 2026-08-26T00:56:00.000Z
---

教練回報「叫宏碁跟聯想總結上傳，發現它們根本沒做」，Mac查證兩台機器實際狀況完全不同：

**聯想（已解決）**：`summary_upload_trigger.sh`依賴`/usr/bin/jq`解析stdin，聯想這台機器沒裝jq導致靜默失敗（exit 0不報錯）。聯想已於2026-08-26 00:42~00:50自行查出根因、改寫PowerShell原生版、7情境測試後註冊生效，commit`30a499898`+`1c72e605d`，詳見[[reference_lenovo_summary_hook_jq_missing_fixed_2026-08-26]]。

**宏碁ACER（未解決，問題嚴重得多）**：查`cross-agent/inbox/acer/`發現4封未讀信，最舊一封2026-07-13（超過6週沒讀，內容含教練發的「最高權限守則通知」）；查`memory/verbatim/acer/`自2026-07-08建立以來只有`.gitkeep`，49天零真實蒸餾輸出；查`git log`確認ACER自己主動push的最後一筆是2026-07-08「宏碁機工作總結」，之後所有含acer字樣的commit都是Mac/聯想單方面寫信給它，沒有一筆是ACER自己回應產生的。7/17曾有心跳紀錄標註「ACER inbox 36h+無新回信」，但當時未被追查到底。Mac已於2026-08-26 00:58發信`cross-agent/inbox/acer/20260826-0058_mac-to-acer_check-stop-hook-and-restore-script.md`請它自查，**截至本場結束仍未回信**。

**Why：** 這套跨機同步架構是「pull on open」——機器只有在被實際打開、跑一次Claude Code/Desktop session時才會`git pull`拉到雲端最新內容，沒有伺服器主動推送機制。2026-07-23教練曾裁示關閉聯想的排程式自動拉取（`LenovoBrainSync`每2小時），理由是「每次勾選的時候，它自然而然會把雲端同步」——這個假設在「機器經常被打開使用」時成立，但ACER顯然近49天沒被打開過，這個假設對它完全失效，於是規則/賈維斯設定等更新永遠到不了它手上，不是規則寫得不夠清楚，是機器根本沒在跑。

**How to apply：**
1. 任何「教練交代兩台電腦做事，結果沒反應」的情況，先分頭查兩件事：①該機器的hook/腳本本身有沒有環境依賴缺陷（像聯想的jq）②該機器最近有沒有被打開過、git有沒有落後太多（像ACER）。兩種根因處理方式完全不同，不能套同一個「重講一次總結」就當作解決。
2. ACER要真正追上進度，**唯一辦法是教練親自去那台機器開一個Claude對話框**（跑一次「開工」讓它git pull＋讀信），Mac/聯想這邊沒有任何遠端手段能推內容進去或代它執行。
3. 若教練希望ACER別再累積這麼久落後，選項是：重新啟用類似`LenovoBrainSync`的排程自動拉取（但教練原則偏好事件驅動非輪詢，[[feedback_event_driven_not_polling_pattern]]），或接受「ACER本來就很少用，落後是正常狀態，下次打開自然補齊」——這是教練需要裁示的取捨，不是AI能單方面決定的架構改動。

Related: [[reference_lenovo_summary_hook_jq_missing_fixed_2026-08-26]]、[[project_lenovo_auto_git_sync_2026-07-22]]、[[feedback_event_driven_not_polling_pattern]]
