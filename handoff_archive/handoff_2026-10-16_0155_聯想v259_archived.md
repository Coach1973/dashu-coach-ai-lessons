# 封存：10/16 01:55 聯想 v259 棒（2026-10-16 13:06 Mac 收工時封存）

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-16 01:55 台灣時間，**Windows 聯想**桌面版 Code 分頁，Opus 5.5／Sonnet 5.5／Haiku 5.5 來回切；教練說「總結」收工；本段 10/15 13:54～10/16 01:51，對話容量約 35%）

**主軸：聯想記憶體 50%→77% 查出核心漏洞並重開釋放；容量提醒 hook 聯想版；預約頁週四改時段；四個教練網頁小修。**
- **聯想記憶體**：元兇是核心非分頁集區 `NtFC`（ntfs.sys）卡 15GB、1.2 億筆未釋放，工作管理員看不到；重新啟動後歸 0、使用率 77%→40%。**快速啟動開著，「關機」不會清，要「重新啟動」**。誰觸發的**未破案**（WPR 錄製被重開中斷）；NordVPN 已排除（mshield 驅動是停止狀態，教練糾正我「沒開怎麼是嫌疑犯」）。`scripts/ntfc_leak_watch.py` 掛聯想 UserPromptSubmit（教練說話才量 0.1 秒，重啟記新起點、跨 1/2/4/8GB 各提醒一次；已實測重開後自動跳「已放掉」），狀態檔 `E:/Claude-Data/.claude/state/ntfc_watch.json`；跳「又在漲」時用管理員同意跑 `wpr -start %TEMP%\ntfc_trace_20261015\ntfc.wprp!NtFC`。記憶 reference_lenovo_memory_ntfs_nonpaged_pool_leak_2026-10-15。
- **聯想 UAC 原本設成「不詢問」**（ConsentPromptBehaviorAdmin=0），RunAs 不會跳視窗，我叫教練按「是」三次他根本沒看到；教練 14:27 自己調成 5。ChatGPT 桌面版（套件名 **OpenAI.Codex**）我已 `Remove-AppxPackage` 移除，Gemini 教練自己移除；兩者都不是我們的 AI 裝的（9/27 前後裝、10/11 商店自動更新）。
- **容量提醒 hook Python 版**（`scripts/context_percent_hook.py`＋`test_context_percent_hook.py`，聯想 settings.json 已掛，備份 `.bak-20261015-before-context-hook`）；Mac 後來改成 45%＋每5句定期報，本場 30/33/35% 實際有跳。
- **倒數日小程式**（Store 版，套件 `WuhanNetPowerTechnologyCo.220271D9343D`）重開沒啟動：開機捷徑直指 WindowsApps 內 exe 被拒絕存取，已改走 `explorer shell:AppsFolder\<AppID>`，桌面（`D:\Users\Desktop`）放「倒數日.lnk」，視窗從副螢幕搬回主螢幕。**開機自動啟動要等教練下次重新啟動才能驗證**。記憶 reference_lenovo_countdown_app_startup_fix_2026-10-15。
- **預約頁週四**（`5e8a76d61`）：19:30–20:30、21:00–22:00 可約；暖身 19:00–19:30／休息 20:30–21:00 兩筆緩衝寫進總表；週四「線上」開頭行程（線上學習／聚）不擋預約（訪談優先，`_yield_if_online`，用名稱判斷因為 Google 同步會整批重建一次性行程）。**10/16 01:55 實測：資料已生效（線上有 19:30、暖身、休息），但 10/22 缺 21:00＝event-webapp 程式還沒重啟**，已寫信給 Mac 軍師（`cross-agent/inbox/mac/`）。記憶 reference_booking_page_thursday_slots_2026-10-15。
- **四個網頁小修**：lidie 學歷補「國立臺中科技大學 企業管理（大專）1996–2000」`2edcbd1`（教練追問「改 GitHub 為什麼網頁沒換」→新記憶 feedback_github_edit_is_the_web_edit…）；tava-brand-web-playbook 足跡時間軸改上下時間線＋Podcast／部落格寫進規格與檢查 `004fcd1` `2466ca4`（我們這份與 TAVA 原頁文字已不同，README 有註）；榮樹下王大明董事長邀請函短網址 `curated/rongtree/wang-dm.html`（轉址頁，`f0c4e7f`；「通用短網址」仍是教練未拍板的模組化第 3 項，這只是單一轉址頁）；andy-chen 首屏「從受助到助人」卡片從照片上移到照片下（卡片橫向正好蓋住下巴位置，`f33679a`；用 DOM 量測驗證，教練規定不截圖）。
- **踩到的坑**：刪檔鎖會擋 `rm -rf` 暫存夾（改用新資料夾名，不刪）；管理員跑的 PowerShell 腳本要**全英文**（無 BOM 中文會壞）；Windows 沒 `fcntl`，預約頁程式不能直接 import 測試；本機記憶資料夾＝倉庫 `claude-brain`，我的索引壓縮第一次被 Mac 同步蓋回，重做後一起提交；Pages 狀態 errored 時 `gh api -X POST repos/<repo>/pages/builds` 手動重跑。
- **教練原話線索**：「我並沒有開啟它，它也沒有在運行中，為什麼是嫌疑犯」→ 列嫌疑前先查有沒有在執行；「你要確定是跳在 Windows 視窗還是你看得到我看不到的東西」→ 叫教練按東西前先確認真的有跳；「那我剛才就叫你改網頁就好了」→ 教練不分 GitHub 與網頁。

### 📋 下一場開工先做
1. **Mac**：讀 `cross-agent/inbox/mac/` 聯想來信，重啟 `com.coach.event-webapp`（預約頁程式 `coach_schedule_view.py` 已 pull 但未載入），驗證 10/22、10/29 晚上起點＝19:30 與 21:00。
2. 教練下次**重新啟動**電腦後，問他「倒數日」有沒有自動跳出；沒有再查啟動捷徑。
3. 聯想 `ntfc_leak_watch` 若跳「又在漲」：先一句白話告訴教練，再請他在跳出視窗按「是」錄 WPR 追兇手（UAC 已改，會真的跳）。
4. 其餘待辦照上一棒（軍火庫企劃書 4 件待決、新 LINE 群查日誌、雲端花費、志工頁人數）。

🙋 要教練決定：無新增（承上一棒軍火庫企劃書 4 件）｜問過：2026-10-15 企劃書內
🤫 等教練自己提起：TAVA 原頁是否也要改成上下時間線（我們這份已改）；通用短網址模組化；記憶體漏洞追兇。

---

> 📦 10/15 16:30 棒（軍火庫企劃書／雲端分工）與 21:05 棒（榮樹下改版驗收上線／新 LINE 群查行程／張麗蝶站更新機制）已封存：`handoff_archive/handoff_2026-10-15_1630_2105_軍火庫企劃書_榮樹下改版_archived.md`

> 📦 10/15 12:40 棒（榮樹下一週盤點／模組化／常用查詢）已封存：`handoff_archive/handoff_2026-10-15_1240_榮樹下一週盤點_archived.md`

> 📦 10/14 09:20 棒（榮樹下多位來賓／南應大團隊頁）已封存：`handoff_archive/handoff_2026-10-14_0920_榮樹下多位來賓_南應大團隊頁_archived.md`

> 📦 10/14 07:20 棒（榮樹下藍圖）已封存：`handoff_archive/handoff_2026-10-14_0720_榮樹下藍圖_archived.md`

> 📦 10/13 23:33 棒～10/14 02:49 棒、10/12 聯想棒已封存：`handoff_archive/handoff_v258_to_v261_archived_2026-10-14.md`

---

