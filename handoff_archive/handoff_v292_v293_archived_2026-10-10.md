# 接力棒 v292、v293 封存（2026-10-10 v295 收工時搬出）

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-09 12:40 台灣時間，Mac 桌面版 Code 分頁，Haiku 5.5→Opus 5.5→Sonnet 5.5（教練 10/09 用 /model 切換），v293，教練說「總結」收工；對話 10/08 17:23～10/09 12:30）

**主軸：四件事——BNI 套版《商戰破局的終極外掛》滿版並讓聯想也做對；替換 inventor（像瘋子的發明家）網站內容；模型分工改三燈號；教練稱讚語音糾錯。另有一次被糾正（案例112）。**

### 1. 《商戰破局的終極外掛》PDF 套 BNI 底圖（滿版）
- 主檔 `/Volumes/953-SSD/下載/商戰破局的終極外掛_BNI版.pptx`（14 張，1450×817），走 BNI PPT SOP `pdf_to_branded_pptx.py` 預設遮罩，不縮小；縮圖總覽親眼看過。第 2、9、13、14 張底部字幕最左幾字被左下 LOGO 遮罩蓋到（舊成品也有）。暫存試過遮罩右界 0.296→0.252：第 9 張修好、第 13 張「這」仍有點被蓋，**沒套用到主檔**（會動 SOP 固定座標），已告知教練，教練沒回。
- 教練說「打開資料夾，不要打開檔案」→ 已開資料夾。10/09 12:27 他說明原因：**直接開檔案他只看得到內容、沒有路徑，沒辦法傳到 LINE；開資料夾他要看就點、要傳就直接拉進 LINE（教練習慣的方式）**。所以 `scripts/deliver_open.sh` 對**所有檔案**（簡報、PDF、Word、Excel、圖片、zip…）預設改成「開所在資料夾並選取該檔、開完把 Finder 拉到最前面」，教練明說要開內容才加 `--open`；網頁／網址仍開 Chrome。反射 `R-DELIVER-POP-OPEN`、記憶 `feedback_opened_on_mac_is_not_delivery…` 同步（commit `3eebbe6c6`）。

### 2. 聯想跑出來不是滿版 → 更新指令
- 查證：我這台用通用工具 auto 模式在 BNI 底圖上選的是 mask（滿版），**看不到聯想的畫面，無法確認它為什麼縮小**，最可能是沒指定模式或用了 safe。處理＝把指令寫死 `--mode mask`、禁止 safe／`--fill contain`、加驗收步驟。
- 改了：`knowledges/SKILL_簡報套底圖_通用版.md` BNI 段、新檔 `knowledges/給聯想_BNI滿版指令.md`（commit `a67830a90`）；大樹作品一鍵套版入口 `ai-go` 的 `ppt-prompt.md`＋`ppt-inject.html`（commit `189fbf8`，線上已換新，手機寬度 375px 無溢出）。

### 3. inventor（像瘋子的發明家）網站內容替換（10/09 01:49）
- 教練給 `huang-kuo-chang-site(1).zip`（只有 index.html＋2 張圖，公開專利局資料版），要取代原頁、網址不變、舊檔留歷史。網址 `https://event.bymyway.com/curated/inventor/` 不變；舊資料夾整個搬到 `~/github_repos/_archive_inventor_v1`（含 plan.html 商業計劃書，**沒有公開網址**），新內容逐檔比對一致；線上 plan.html 已 404、圖片 200 image/jpeg、375px 無溢出。`inventor` 不是 git repo，無 hash。
- ⚠️ 名字：教練訊息寫「黃國璋」，檔案／登記表／專利連結都是「黃國彰」；照檔案發布，**沒改名**，已告知，教練沒回。registry 的 `source_package` 還是舊 zip 名（沒動）。

### 4. 模型分工改三燈號（教練親定，commit `b4dbe3e1a`）
- 🔵 Haiku＝已有 SOP 的固定動作（戰報／儀表板、簡報套版、策展與大樹作品上架、新增籌備會／例會名單、查行事曆、開發票）、🟢 Sonnet、🟣 Opus。改了 `knowledges/模型分工規則_Opus與Sonnet.md`、`scripts/model_tier_advisor.sh`、`stop_rules_master.py` A3（認 🔵），補教練不滿關鍵字（不滿意／偷工減料／不是我要的／問那麼多）。
- 發現：教練送出前剛 `/model` 切換，hook 讀對話檔會看到舊模型（切換紀錄寫入比 hook 晚）→ 提示改成「以系統提示的模型為準」。
- 教練稱讚語音糾錯（「Haiku 3.5」＝5.5、「檔期作品」＝大樹作品），已加進 `feedback_coach_chinese_file_mapping`。

### 5. 教練糾正與源頭修復（案例112）
- 教練問「要修改…指令嗎？」我查完答「要改」卻回問「要我現在改嗎？」→「我叫你改，就是要改，怎麼問那麼多」。同類 09-30 已有記憶，依 N8 不再加記憶，改源頭：新反射 `R-COACH-YN-QUESTION-IS-ORDER`（prompt 時刻；2042 句教練真實發言回測只命中那 1 句，寬鬆版會誤抓 2 句）。試金石案例 112。

### 📋 下一場開工先做
**目前沒有教練交辦未完成。** 開工回報 5 行內，問「今天要從哪件事開始？」。
🔧AI 自己的（不問）：①教練丟簡報套 BNI 底圖：走 `pdf_to_branded_pptx.py` 預設、不縮小；交付任何檔案用 `deliver_open.sh <檔>`（預設開資料夾並選取、不開內容；原因：教練要拖進 LINE 傳）；②教練的短問句「要不要改 X 嗎」＝交辦，查完直接做；③每則交辦第一行亮燈 🔵／🟢／🟣；④聯想那邊是否真的修好沒看到結果，有人貼聯想回報再查。
🤫等教練自己提起：inventor 名字「璋」vs「彰」、舊版是否要有公開網址；套版底部字幕被 LOGO 蓋到的 0.252 版本（沒套用）；Run for Future／百人導師真送測試與 Plaud 主題對照（見前棒）。
**commit**：workspace `b4dbe3e1a`（三燈號）、`a67830a90`（聯想指令）、`6dd879251`（收工主體）、`3eebbe6c6`（檔案開資料夾）；ai-go `189fbf8`。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-08 17:12 台灣時間，Mac 桌面版 Code 分頁，Sonnet 5.5（中途教練手動切 Haiku 5.5 約 1 小時再切回），v292，教練說「總結」收工；對話 10/08 13:33～17:08）

**主軸：教練當天丟了五件事——Run for Future 頁改數字＋報名通知、百人導師申請通知加群、找「全世界最優秀團隊計畫」逐字稿（做成網頁登記作品一覽）、PDF 簡報套 BNI 底圖；最後一件我做錯被教練火大糾正（案例110）。**

### 1. Run for Future 2027 頁（https://event.bymyway.com/curated/runforfuture/）
- 席次 40→**88/100**（圖示、進度條、剩餘 12、FAQ「約 88 個」全同步）。**教練裁示**：刻意營造快滿額氛圍；FAQ 那句「100 家額滿即截止」**不改**（「只有限額，報名才會踴躍」）——不再提。
- 預約席次表單原本只是 mailto，改成送 `/api/register` → 入庫＋推「活動報名即時通知」群（`event.db` events 新增 id 33、slug `runforfuture`、site `curated`）。前端攔截送出內容＋後端用假通知測過，**沒有真的送一筆吵群**。測試時誤用了教練舊測試手機 0912345678（attendee 182）被我覆蓋，已從備份 `event.db.bak-before-runforfuture-20261008` 還原。
- commit：網站 repo `runforfuture` `aa7138c`；workspace `3f05cba92`。

### 2. 百人導師申請通知（mentor100）
- 原本只發教練私訊（chat 6124913915），現在**私訊＋活動報名即時通知群（-5349981085）兩邊都發**，任一邊失敗仍會寫 `notify_failures.log`。假通知測過、網站已重啟；**沒有真送**。commit `mentor100` `e588fb1`。

### 3. 三缺經典對話 → 網頁＋作品一覽（✅ 10/08 17:21 已上架，教練說「你選就好，趕快結案」）
- 教練找的「全世界最優秀團隊計畫｜客戶、人才、伯樂」＝作品 `three-lacks`（作品一覽已有，但只是行銷網頁，沒逐字稿）；逐字稿原稿＝雲端對話的 `bni-chapters/docs/classic_dialogue_three_lacks_2026-10-06.md`（私有倉庫，雲端 AI 整理，內容為「缺客戶／人才／資金」，10/06 糾正為「天使投資人」，池塘與魚比喻）。**「伯樂」一詞不在這份對話裡**；NotebookLM「真實AI團隊計劃」另有 47 份投影片（教練說那是口誤，不管）。
- 已把這份做成 game-1004 同格式網頁，26 段教練原話與原檔逐字比對 0 缺漏、375px 無溢出；檔案存 `knowledges/三缺經典對話_網頁待上架/`（index.html、zip、build_dialogue.py）。**上架結果**：短網址我選 `lacks-1006`（沿用 `ema1017` 日期式命名；原三個候選都超過 SOP 規定的 10 字，所以改選 10 字內的），網址 https://event.bymyway.com/curated/lacks-1006/ ；`kind=creation` 上傳 → `curation_check_result.py` 回 success_creation、線上 200；線上網頁原話與原檔比對 26 段缺漏 0；已自動登記 coach888「最新作品」第一筆（教練個人創作）；已用 `deliver_open.sh` 在 Chrome 跳出。**未移進「全世界最優秀團隊系列」分類**（教練只說登記作品一覽；要移他說一聲，改伺服器狀態 coach888_layout 先 GET 再 POST）。

### 4. 《96小時引爆億級商業宇宙》PDF 套 BNI 底圖（教練火大，案例110）
- 我先用通用技能＋手動 `--mode safe` 縮小成 94%×89% → 被罵偷工減料。教練要的是「**全部覆蓋**」滿版（跟 9/21 驗收通過的《建構高效商務系統的建築師》BNI 版同做法）。已用 BNI PPT SOP 腳本重做，**主檔**：`/Volumes/953-SSD/下載/96小時引爆億級商業宇宙_BNI版.pptx`（15 張，1450×817）；其他版本（縮小版、滿版v2、文字完整）在 `96小時_其他版本備份/`。底部有字被 LOGO／弧形蓋住（第4、13、15張最明顯），已告知。**沒在 PowerPoint／Keynote 實際開過（截圖被鎖）**。
- **源頭已修**：`reference_notebooklm_cli_pipeline` 的錯誤建議（用 safe）、`reference_bni_ppt_sop_alias` 補標準、MEMORY 索引、新反射 `R-BNI-PPT-FULLBLEED-NO-SHRINK`、試金石案例110。
- 順手：技能腳本存 `~/tools/brand_pptx.py`＋獨立 venv `~/tools/brandpptx-venv/`。

### 5. 其他
- 給教練一段貼給小龍蝦的指令（列出 Plaud 175 筆主題整理），教練說這種簡單的事交給小龍蝦跑省 token；我誤說「讀不到我來整理」被糾正，已收回——**Plaud 主題整理由小龍蝦做，AI 不代做**；若小龍蝦讀不到 SSD，我只負責把 `local_text`（16 MB）複製到它讀得到的位置。
- 「釋放」＝跑 `scripts/rustdesk_free_memory.sh`（782M→133M）。
- Stop hook「叫教練自己動手」對描述性的「您打開」誤判一次，已向教練澄清。

### 📋 下一場開工先做
**目前沒有教練交辦未完成。** 開工回報 5 行內，問「今天要從哪件事開始？」。（三缺經典對話已於 10/08 17:21 上架完成。）
🔧AI 自己的（不問）：①教練丟簡報套 BNI 底圖時，先看舊成品，走 `pdf_to_branded_pptx.py` 預設，不縮小（反射已掛）；②有人提 PowerPoint／Keynote 驗證要截圖時，才請教練同意截圖。③🔴 **交付任何檔案／網址，最後一步一律跑 `scripts/deliver_open.sh <主檔或網址>` 直接跳出**（教練 10/08 17:15 令；案例111；多版本只留一個主檔）。
🤫等教練自己提起：Run for Future 與百人導師的**真送一筆測試**（會吵群、佩佩老師會看到，教練說可以才做）；Plaud 主題對照表與刪雲端（見上一棒）。
**commit**：runforfuture `aa7138c`；event-signup/workspace `3f05cba92`；mentor100 `e588fb1`；本棒總結另計（見開工注入）。

---

> 📦 v291完整內容已封存：`handoff_archive/handoff_v291_archived_2026-10-09.md`（兩個一鍵注入技能頁＋Plaud 175 筆備份轉繁中＋NotebookLM 自動化 nlm）

> 📦 v290完整內容（發明家頁表單、信任遊戲小上癮機制；含 v288 指標）已封存：`handoff_archive/handoff_v290_archived_2026-10-08.md`
