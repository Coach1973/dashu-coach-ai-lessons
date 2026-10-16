## 🔴 給跨對話框軍師讀的總結摘要（2026-10-16 19:45 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Sonnet 5.5→Opus 5.5；教練說「要總結嗎」收工；本段 13:09～19:45，對話容量約 49%）

**主軸：15:00 workspace 被本機另一個 AI 對話框拉錯分支換掉，教練在外面 3.5 小時下不了任何指令、/curated/ 全部 404（重大疏失，試金石123）→ 全部救回並從源頭封住；全面盤查救回 7 月以來 52 筆自動暫存默默弄丟的東西；Claude 新增 7 個技能、小龍蝦新增 2 個技能；背景工作失敗改成當下通知。收工前健康檢查 🟢 全部正常。**
- **兇手與原因**：對話框 960f614e（做香檳下午茶網頁）在 workspace 憑印象寫 `origin master`（workspace 是 main），整個資料夾被換成 ~/.openclaw 的檔；python 檢查程式不見→回 2→教練每句話（含手機）被擋 16 次。9/10 同坑已發生過，當時只寫記憶。還原後 4,172 檔全回（`2538fe817`）。
- **源頭機制**：①8 支 python hook「檔案不在就放行」②`scripts/git_wrong_branch_guard.py`（PreToolUse）：寫錯分支名或指到毫無共同歷史的線就擋並給正確名稱，所有資料夾適用，1,525 筆真實指令回測誤擋 0（`6ef61e757` `aab134d12`）③兩個資料夾都裝 pre-rebase。
- **盤查救回**（`c1eb5ede6`）：5 個整份檔（Plaud主題整理.md 等）、13 條記憶索引、3 份 SOP 段落；遺失行封存 `handoff_archive/stash_rescue_2026-10-16/README.md`；三支自動同步改用 `scripts/safe_stash_restore.py` 逐檔放回。守門員擴大到 38 個自動服務含小龍蝦 gateway（`00886b78d`）；接力棒鏡像格式檢查改查全文（`69d1d3ad6`）；背景排程失敗當下通知 `scripts/cron_fail_notify.sh`（30 分鐘同工作 3 次→電報＋信到 inbox/mac，`de8266088`，daemon 19:22 已重啟）。
- **技能**（`9d6041215` `7502acedf`）：Claude＝健康檢查 system-health-check（`scripts/system_health_check.py`）、總結、改網頁、上架、加上報名、BNI 開票、原話報告書；小龍蝦 main＝site-down-check、bigtree-publish-site（備份 `ops/xiaolongxia_workshop_skills/`）。都實測新對話看得到／答對。報告 https://claude.ai/artifact/GF4ueUwADRQtzeaeQko2JK
- **教練原話線索**：「寫一個指令，寫到我連主人親自下命令都不行，那要你何用？」「憑什麼你們可以憑印象？」「我又不懂電腦」→ 會造成損失的動作一律「系統先查、不符就擋」，不靠 AI 自覺；做得到的事不叫教練點、不叫教練動手。

### 📋 下一場開工先做
1. 教練回應軍火庫設計稿（https://claude.ai/artifact/VvLFrV8He1qA3fnScPTSm3 ）後照做（企劃書 4 件＋雲端另 3 件；點數剩 US$36、週用量預警）；不主動追問。
2. 志工頁有人加入後教練報人數 → 改 `volunteer.html` 的 `JOINED`。
3. 🔧 下次真實登入後看 `~/Library/Logs/openclaw/launchagents_guard.log` 有沒有登入時那筆；跑一次 `system_health_check.py`。
4. 🔧 承接：gateway 啟動的 `providers.nvidia.models[17].input` 設定驗證錯誤；新 LINE 群歡迎詞沒送出原因；策展 GitHub 化收尾；聯想 `/api/mytools/state` 放行 8765 建議拿掉；worktree 分支 `claude/kaigong-424fd5` 兩個 commit 要不要搬進 master；52 筆舊 stash 留在清單（內容已封存）；`namecard-db/namecards.db.backup-…20260712` 含個資只留本機；`memory/` 有 2 個記憶檔放錯位置（應在 claude-brain/）；angel-sister 頁 10.6MB（圖片內嵌），手機慢可考慮壓。

🙋 要教練決定：軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）｜問過：2026-10-15 企劃書內
🤫 等教練自己提起：香檳下午茶頁 4 點確認（戰績只用原頁、理事長林家旭查無資料、照片人物依檔名推斷、類別被分成「食」）；social-club 頁尾寫「TAVA AI 設計」不是「製作」；吳錦昌沒有個人頁；預約頁「只開固定時段」；南應大 /tut/team 要不要加入口；真貴 5 位要不要從真鑽拿掉；Podcast 快取改 1 分鐘；TAVA 備份頁放哪一類；GitHub 404 三個（joseph-cloth／social-good 私有倉庫不能開 Pages、Business.gym 沒有倉庫，event 上的版本正常）。

---
