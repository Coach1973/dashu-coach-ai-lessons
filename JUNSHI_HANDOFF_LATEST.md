## 🔴 給跨對話框軍師讀的總結摘要（2026-10-09 12:40 台灣時間，Mac 桌面版 Code 分頁，Haiku 5.5→Opus 5.5→Sonnet 5.5（教練 10/09 用 /model 切換），v293，教練說「總結」收工；對話 10/08 17:23～10/09 12:30）

**主軸：四件事——BNI 套版《商戰破局的終極外掛》滿版並讓聯想也做對；替換 inventor（像瘋子的發明家）網站內容；模型分工改三燈號；教練稱讚語音糾錯。另有一次被糾正（案例112）。**

### 1. 《商戰破局的終極外掛》PDF 套 BNI 底圖（滿版）
- 主檔 `/Volumes/953-SSD/下載/商戰破局的終極外掛_BNI版.pptx`（14 張，1450×817），走 BNI PPT SOP `pdf_to_branded_pptx.py` 預設遮罩，不縮小；縮圖總覽親眼看過。第 2、9、13、14 張底部字幕最左幾字被左下 LOGO 遮罩蓋到（舊成品也有）。暫存試過遮罩右界 0.296→0.252：第 9 張修好、第 13 張「這」仍有點被蓋，**沒套用到主檔**（會動 SOP 固定座標），已告知教練，教練沒回。
- 教練說「打開資料夾，不要打開檔案」→ 已開資料夾；`scripts/deliver_open.sh` 簡報預設改成開資料夾並選取檔案（`--open` 才開 Keynote），反射 `R-DELIVER-POP-OPEN` 同步。

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
🔧AI 自己的（不問）：①教練丟簡報套 BNI 底圖：走 `pdf_to_branded_pptx.py` 預設、不縮小；交付簡報用 `deliver_open.sh <檔>`（預設開資料夾）；②教練的短問句「要不要改 X 嗎」＝交辦，查完直接做；③每則交辦第一行亮燈 🔵／🟢／🟣；④聯想那邊是否真的修好沒看到結果，有人貼聯想回報再查。
🤫等教練自己提起：inventor 名字「璋」vs「彰」、舊版是否要有公開網址；套版底部字幕被 LOGO 蓋到的 0.252 版本（沒套用）；Run for Future／百人導師真送測試與 Plaud 主題對照（見前棒）。
**commit**：workspace `b4dbe3e1a`（三燈號）、`a67830a90`（聯想指令）；ai-go `189fbf8`；本棒總結另計（見回報）。

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

## 🎯 「賈維斯成長計畫」（簡稱「反射條件」）進度（2026-10-02 07:10 瘦身版；詳細交辦段與第 1~3 步經過已封存 `handoff_archive/handoff_v266_to_v267_and_goal_section_archived_2026-10-02.md`）

教練 02:30 原話：教練訓練出來的每個 AI 都要有條件反射；三種標準＝有智慧的反應、聽懂人話的反應、準確做事情的反應；對外服務再加「讓人備受禮遇、被尊重，惦記用戶說的話，不把問題丟回給用戶」。已全權授權，**不准再拿細項問教練**。

| 對象 | 狀態 |
|---|---|
| ① 教練自己的 AI | 小龍蝦端外掛 reflex-prompt／member-context／coach-context 上線；Mac 軍師 hook 85 條反射；**聯想 10-02 07:45 已接上並回信（Mac 驗收過：commit `bee1a7653` 存在、`pick_next_task.py` 在 Mac 接力棒實跑輸出正確、ps1 有 BOM 且呼叫它；聯想自己的反射／擋下是用管線模擬，要等教練在聯想開新對話框才算真實驗收）；宏碁 10-02 09:15 已接線並回信（裝了 Python 3.12、加 5 個 hook，用模擬事件測過反射與擋下；開工置頂🎯等聯想推上去後會自動帶到，真實新對話框畫面待教練下次開新對話框才算驗收）** |
| ② 四位夥伴分身 | ✅ 10-02 04:20 SOUL.md「三種標準（夥伴版）」＋群組 session 封存＋真實路徑測過（見 v269） |
| ③ LINE 對外帳號（禮遇版） | ✅ 人設上線（v268）；**真實 LINE 會員流量還沒驗證**（看 `state/member_context.log` 第 4 欄 `sender:u…`） |
| 試金石 97 案／記憶 171 條 | ✅ 全部有去向，`python3 scripts/reflex_coverage.py` 未處理 0、斷鏈 0 |

✅ 開工已改成「心法＋最新一棒」（10-02 14:2x，注入 30KB→9.7KB，全域與 workspace CLAUDE.md 開工鐵律同步改 v3）；之後：Stop hook 只留行為檢查、拿掉字眼檢查。待查：`handoff_sync_guard.sh` 判斷1 用 PreToolUse＋stderr＋exit 0 提醒，AI 可能看不到。量尺：教練訊息「重講」比例 5月19%／6月13%／7月14%／8月12%／9月16%，重跑 `python3 scripts/render_top30_report.py` 看 10 月有沒有降。

> 📦 v264（Mac 10-01 22:20，小龍蝦卡核准修好、第一分會雙週＋口頭填數據、Tailscale 三台＋手機入網）完整內容已封存：`handoff_archive/handoff_v264_archived_2026-10-02.md`

---

> 📦 v262（聯想 10-01 18:50，RustDesk 中繼故障→Tailscale、BNI 簡報 3 份）＋v263 宏碁（10-01 21:50，真鑫戰情表、宏碁 Tailscale＋RustDesk 直連）完整內容已封存：`handoff_archive/handoff_v262_v263acer_archived_2026-10-02.md`

## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立；2026-09-24教練要求根源改版）

> 🔴 **2026-09-24根源改版（教練：「同一類事情不要再重複來煩我了」）**：這張表是**AI自己的工作筆記，不是要唸給教練聽的清單**。任何事要拿去問教練，必須同時過三關，少一關就不准問：
> ① **只有教練能做**：花錢、代表教練對外發言、不可逆操作、教練自己的內容與喜好、需要教練本人親自登入（例如要手機簡訊驗證碼、教練個人銀行等系統從未存過帳密的帳號）。路徑大全／既有腳本裡已存好帳密的主機與服務（VPS、GitHub、Netlify、ezPay等），AI 自己用，不算這一關。AI自己查得到、做得到、判斷得了的，一律自己處理。
> ② **教練沒答過**：先查本表、封存檔、記憶檔。教練裁示過的（含「不用管」「略過」「到此為止」「保留就好」），換任何說法都不准再問。
> ③ **現在不問會卡住**：教練正在等結果，或幾天內有期限。不急的放「等教練自己提起」，不主動提。
> **每件事最多問一次**：問過沒回應＝教練現在不想處理，移到「等教練自己提起」，不准追問、不准開工重唸。
> **開工回報不唸待辦**：只講「🙋要教練決定」裡還沒問過的（通常是零件），然後問「今天從哪件事開始？」
> 教練裁示「不用管／不做／略過」的列，當場搬去封存檔，不准留在這裡。

### 🙋 要教練決定（三關全過才能放；格式：標題｜只有教練能做的原因｜卡住什麼｜問過：日期或「未問」）
（目前沒有。10/06 教練糾正：轉述雲端／其他 AI 寫的「待決定」前，每項各自過 N2 三關，不准整段搬進來——案例106）


### 🤫 等教練自己提起（AI不主動問、開工不唸；教練提到時才去封存檔查詳情）
- **Run for Future／百人導師通知的真送測試**：會吵「活動報名即時通知」群，教練說可以才做（10/08）。FAQ「100 家額滿即截止」教練已裁示不改，不再提。
> 詳情全文：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`
- **inventor 網站**：教練訊息寫「黃國璋」、檔案內是「黃國彰」（10/09 已告知，教練沒回）；舊版（含商業計劃書）目前只存本機 `~/github_repos/_archive_inventor_v1`，沒有公開網址，教練要才登記新網址。
- **套版底部字幕被 LOGO 蓋到**：0.252 遮罩版（第 9 張修好、第 13 張仍有一點）沒套用，教練決定才改（10/09 已告知，沒回）。
- **座位第 4～6 步的三個小決定**（教練已在雲端對話看過，不卡上線，不主動問）：後台「已入會／釋出」要不要確認視窗、取消預約後「想坐」要不要自動回來、洽談中見證被撤回洽談要不要中斷；另真功夫、真樂齡換掉的 9 項專業還沒被教練逐項確認、真功夫第四象限排序。
- **pxpipe**：教練 10/06 親口不裝，結案，換任何說法都不再提。
- **三缺行銷頁**：教練自己獨立製作，做好會自己告訴我（10/06 19:32 親口）。**不問價格／公開／數據來源／影片／網址／申請觀看通知**；文件 8 份已併進 bni-chapters master 備查。
- 座位清單內容待教練哪天提起再換：`real-age` 主軸、`real-kungfu` 第 4 象限、年底成立哪幾個（只是換 `data/seat_lists/*.json`，不卡任何程式）。
- 手機出門用行動網路輸入 Tailscale 100.x 位址連 RustDesk 實測（v264，教練要出門用時再測）
- RustDesk 直連實測：聯想→ACER（ACER 100.78.106.14:21118，ACER 離線就等醒來）、ACER→Mac 教練還沒回報（v263，教練要用時再測）；官方中繼 21117 修好後再驗證
- 聯想 `E:\Claude-Data\` 殘留 ai-class-1017.zip／ema1017.zip／pk2／zpk／cookie.tmp（刪檔鎖擋，需教練同意才清，v263）
- 怡靜群若回「沒有填121功能」→封存該群 session 重來（v264，教練或怡靜反映時處理）
- 小龍蝦一次處理多張名片照片：程式讀過用 card_splitter 切圖但沒實跑（v264，教練要時找一張多卡照片實跑）
- 大台南商圈示範版位林百貨/神農街換成建築/街景照（要從網路下載照片，09-26已問過一次，教練沒回）
- VPS升級LTS 2026.7.35（教練09-24：10/1左右月報會自動提醒，時間到再說）
- 367位前會員推薦人補查（BNI Connect帳密沒存在路徑大全，要教練本人登入一次；09-24已問過一次）
- 柯朝陽發票（教練09-24：延後約一年，不用管）
- 試金石商業化計畫書（教練09-24：還沒想到怎麼商品化，暫時不用管）
- 小二(test2)/OpenClaw 2.0評估（暫停，等官方修復）
- 小二Telegram輪詢異常（教練09-21：等小二成熟再處理）
- 聯想C碟WinSxS再瘦身4~5GB（要不要做，教練沒回）
- bni-chapters真誠分會網頁架構問題（教練還沒說明是哪個問題）
- 「教練都在想什麼」補更多素材（等教練提供）
- 其他LINE帳號比照搬遷（等教練指定帳號，SOP已備妥）
- 小龍蝦後台看不到中文名（教練裁示：看到陌生ID問了再回）
- coach888拖拉排序好不好用（等教練回饋）
- 「全世界最優秀的團隊計畫」報名連結（等教練給網址）
- 企業健身房正式建站（等教練交辦）
- 企業健身房4項文案修改（等教練交辦下一步）
- BNI小幫手實戰體驗（等教練親測）
- Coze舊機器人何時停用（等教練裁示）
- ACER 36.3GB備份刪除（需教練在ACER親自開對話）
- 赫米斯Telegram線登出登入時斷約2分鐘（綁使用者登入，要改成開機常駐系統服務才能根治；09-25已告知一次，教練沒要求處理）
- 手機遙控開機自動啟動（現在重開機就消失、要 AI 手動重跑；10/03 問過一次，教練只回「搞定了」沒回這題）
- 第一分會「陳迎薰、王純藝」：教練名單有、戰情表沒有，當新增夥伴加了、專業類別空白（教練名單寫投資型保單、行動美容；v282，教練沒再提就不問）
- 「100 個案例」整理成簡短文字版（教練 10/06：影片在 YouTube 非公開連結，整理需要時間，先知道就好；教練開始整理再動，不放影片連結與個資）
- `docs/source/` 之後有新原稿再補（教練或雲端貼清單才放，先查 README 索引）
- 雲端第三步的 5 項細節決定（預設值已選，見 `step3_done.md`；教練玩過有想法再說）

### 🔧 AI自己的工作清單（AI自行處理，做完不用跟教練報告細節）

> 📦 **更早162筆已完成列**：`handoff_archive/handoff_status_table_completed_archive_2026-09-18.md`；**09-24搬出的21筆結案列**：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| 🟢 | **座位功能三個低優先小改（雲端 10/06 夜查到，我已查證）** | ⏳驗收併入後 AI 自己處理 | ①座位地圖每載入就寫 90 次資料庫（`seat_map()` 內逐一 `sync_chapter`）→ 只在清單檔內容真的變了才寫（比對檔案 mtime／雜湊）；②座位標「已入會」後無畫面可改回空位（後台加「改回空位」，需確認視窗）；③後台「已入會／釋出」沒有確認視窗。都不卡上線，不問教練。 |
| 🟡 | **`workspace/CLAUDE.md` 的接力棒鏡像停在 10/01，吃額度又過期（10/06 v288 查證）** | ⏳AI 自己處理（額度緊繃時動手前先跟教練說一聲） | 查證：`ai.openclaw.cron-daemon` 每 5 分鐘都有跑 `sync_handoff_to_claudemd.sh`，是腳本 9/30 加的格式防呆（開頭 500 字必須有「新的一棒 vN」）自 10/01 起每次拒絕，`/tmp/sync_handoff.log` 已累積 1,050 次拒絕；現在接力棒標題沒有「新的一棒」字樣。鏡像段約 2.2 萬字、占 CLAUDE.md 一半以上，在 workspace 內工作時會載入。**建議做法**：10/02 開工改 v3 的本意就是只注入最新一棒，所以比較對的是拿掉鏡像（CLAUDE.md 換成一行指標、cron-daemon 停掉這一步），不是修防呆；改前要確認 `feed_junshi_handoff.sh` 第 317 行那段說明沒有仰賴它。 |
| 🔴 | **守則#07 輪詢偵測器半成品（10-06）** | ⏸被安全檢查擋下，已問教練一次沒回，不追問 | `scripts/stop_rules_master.py` `_D_EVERY` 數字誤設必填，線上版（`d63575338`）會放過「每小時查一次」；補法與回測方式見 v287 ②。 |
| 🟡 | **雲端寫給軍師的信（10-06）** | ✅Mac 端＋雲端規則已上線 | 雲端信放分支 `docs/to_junshi/`，Mac 端 `scripts/cloud_letters.sh list｜cat｜mark`，開工 hook 與「讀信」反射會叫；已開著的舊雲端對話要先 pull master 才會用新路徑。記憶 `reference_cloud_letters_to_junshi_path_2026-10-06`。 |
| 🟡 | **bni-chapters 雲端協作（10-06）** | 第三步已合併(`3a9ba09`)、座位評估已做(`518b731`)；座位第 1～3 步（分支 `claude/seats-step123`）待驗收 | 步驟見 v287 ①。基礎建設：`tests/`（假資料庫、`conftest.py` 擋掉通知教練）、環境變數 `BNI_CHAPTERS_DB`／`TRUST_GAME_DB`、雲端用 `CLAUDE.md` 規則；雲端只看得到專案，要給它資料請放 `docs/source/`（README 為索引）；`claude -p "訊息" --cloud session_01PpSC8vJP5FQUtK1M7grBuU` 可代傳訊息給雲端任務（要教練先同意）。 |
| 🟢 | **MEMORY.md 超過 200 行（約 204）＋記憶檔命名檢查提示 `project_netlify_deploy_quota_2026-07.md` 不合規** | ⏳AI 自己找時間做 | 合併已過時（⛔）與同主題的索引行，只留一行一則；改名時同步改索引連結。不問教練。 |
| 🟢 | **team 站分會／友好夥伴後續（10-05 v282）** | ⏳教練給第三～五分會名單才做 | team-bymyway 認座位功能已上線；友好夥伴在 team 站補照片不會同步進遊戲（可寫小同步腳本）；金質獎章得主未寫進探測器（只知等級、不知推薦人數，等教練給數字）；「分會之光 vs 分會精神」模板規則要不要改（教練沒問就不動） |
| 🟡 | **信任遊戲／分會座位（10-04 軍師）後續** | ✅探測器已上線（真鑽、真誠、真鑫；籌備會程式已支援但 0 座位）；積分表 v2 已交 | 見 v280「下一場開工先做」。**AI 自己的程式待辦（不問教練）**：「近三年」視窗（`trainings_json` 要改成連月份一起存才切得出來）、培訓分值表、遲到／早鳥接進探測器、領導標籤版面拿到截圖許可後親眼看一次、真鑫戰情表 24 人 vs 會期報告 17 人要核對（張晴晴、楊凱為戰情表是現任但不在報告；范郁琪、薛如媛戰情表標離會但在報告，座位以報告為準）、`scripts/reflex_coverage.py` 列出的幾個 10/01～10/03 記憶檔尚無反射去向。DnA 的啟動董事／支持與增長董事／區域董事分數教練沒定，不主動問。技術備忘沿用：技術備忘：bni-chapters 的 `chapter_members.claim_phones`（不是 NULL＝依菁英表建的座位；內容是菁英表手機，只留存不顯示、DB 不進 git、repo 私有）、`claimed_at`＝第一次補資料時間、`member_edit_log` 存舊資料可還原；前台不能刪座位，要下架請直接改 DB。柯朝陽、蘇志揚已離會，不在名單。 |
| 🟢 | 〈林士民〉shihmin 頁手機上形象照框偏窄（`img` 的 `height="552"` 屬性蓋過 CSS `aspect-ratio`，舊照片也是這樣） | ⏳低優先-沒要求不動 | 要改只需在 `.portrait img` 加 `height:auto`；教練只要求換照片，N7 不順手改。 |
| 🟢 | 記憶檔名不合規：`claude-brain/project_netlify_deploy_quota_2026-07.md`（commit hook 每次提示，應改 `<type>_<snake_case>.md`，描述用底線） | ⏳低優先-AI自己改 | 10/04 commit 時發現，舊檔非本場造成；改名時同步改 MEMORY.md 索引連結，不用問教練。 |
| 🔴 | **賈維斯成長計畫（反射條件）總進度（v265~v269）** | ✅第 1~4 步完成，剩 2 項等外部 | 第 1 級反射 hook＋小龍蝦外掛 reflex-prompt／member-context／coach-context／url-typo-guard；禮遇版人設；四位夥伴三種標準；試金石 97 案＋記憶 171 條全有去向。**剩**：①真實 LINE 流量驗證 `state/member_context.log` 第 4 欄 `sender:u…` ②聯想／宏碁回信驗收。測試法：外掛類走 `openclaw gateway call agent`（記憶 `feedback_openclaw_hook_fire_and_forget.md`），分身類封存群組 session 後用真實語音句前後對照。詳細見 `handoff_archive/handoff_v266_to_v267_and_goal_section_archived_2026-10-02.md`。 |
| 🟡 | **Mac 備份改四條（10-02 教練定，取代每小時）＋Amber 空間** | ✅四條都上線；⏳明早 08:10 首次點名備份待看 | 【10-02 11:40 完成】上限 QuotaGB=150 已生效；刪 3 天前 12 份（35→23，留 09-29 23:40 起），備份映像內用量 142→119GiB。密碼改用 `scripts/coach_password_dialog.sh`（sudo -A，教練看得到）。Amber 本身空間有沒有回升，下次看 Amber 通知（AI 分類 >15% 才恢復）。以下為原規劃：①點名正常才備份 `daily_team_rollcall.py backup_when_healthy`（launchd 環境實測 startbackup exit=0）②升級前必備份 反射 `R-BACKUP-BEFORE-UPGRADE`（14 例全對、回測 11/39091 全是真升級）③上限 150GB＋刪 3 天前 12 份：App 終端機分頁「備份設定：只差輸入密碼」跑 `scratchpad/tm_setup.sh`，教練輸入密碼後看 `tmutil listbackups|wc -l`（應 34→22 左右）與 `defaults read /Library/Preferences/com.apple.TimeMachine` 有無 Quota；scratchpad 會清掉，腳本要留就搬進 scripts/ ④排除 `.cache/.npm/.rustup`（約13GB，`.nvm` 刻意保留）。**明早 08:10 首次點名要看到「💾 備份：全員正常，已自動備份一次」**。教練頻率已自己改手動（AutoBackup=0）。記憶 `project_mac_backup_policy_good_state_and_pre_upgrade_2026-10-02.md`。 |
| 🟢 | `reflex_coverage.py` 記憶索引斷鏈 2 筆（聯想 bee1a7653 合併索引帶進來的 `feedback_single_html_work_download_images_and_zip_myself_2026-10-02`、`reference_rustdesk_direct_ip_over_tailscale_2026-10-01`，Mac 沒有這兩個檔） | ⏳待處理-低優先 | 從聯想 claude-brain 取回檔案或改索引；補進 memory_ledger。 |
| 🟢 | Claude 自動記憶索引 `~/.claude/projects/-Users-bymyway--openclaw/memory/MEMORY.md` 已 188 行（200 行起截斷），要壓到 140 行內（10-03 hook 提醒） | ⏳待處理-低優先 | 比照索引底部「📦 舊記憶主題分組彙整」做法，把 08~09 月已固化的 🔴 單篇合併成主題分組行；只合併索引行，不刪記憶檔。 |
| 🟡 | kong 的 `agents/kong/SOUL.md` 第 3 行寫「唯一指定模型 MiniMax M2.7」，但 `openclaw.json` 的 kong 實際是 `minimax/MiniMax-M3`（peipei 的 SOUL 06-03 已升 M3）（10-02 v269 發現） | ⏳待處理-低優先 | 設定檔與人設矛盾，無害但別讓 kong 以為自己被鎖在 M2.7。查 kong 升 M3 的授權日期（git log／記憶）後補一行更新紀錄，比照 peipei SOUL.md 第 6~8 行寫法；找不到授權紀錄就維持現狀不動。kong 是獨立 repo（`agents/kong`），改完在該 repo commit+push。 |
| 🟡 | **BNI簡報3份（藍圖／生態圈／商戰制勝密碼）底部字幕開頭被左下LOGO保護區蓋掉**（10-01聯想，v262） | ⏳等教練選（已問過1次，不追問） | 檔案在`D:\Users\Downloads\BNI版簡報\`。教練選「內縮排版」才改`scripts/pdf_to_branded_pptx.py`重跑；選「照現狀」就結案。poppler在聯想不在PATH（見v262）。 |
| 🟡 | **Tailscale雙機互連（聯想tree 100.95.122.29／Mac 100.91.228.91）＋RustDesk官方中繼21117故障** | ✅聯想→蘋果已通；⏳等RustDesk官方修復 | 聯想桌面捷徑「連蘋果電腦」＝TigerVNC。蘋果→聯想教練不需要（RDP已開、Windows密碼教練不記得，教練要用才自己設）。RustDesk不卸載。 |
| 🔴 | **策展網站全面GitHub化收尾（09-30教練交辦，10-01教練已切bypass＝授權）** | ⏳下一場直接做 | 工具`scripts/curated_git.py`已備妥：跑`ensure-all`補11站→接回`curation_process.py`三條上架路（github_note，大樹作品/全新店家/暫代頁覆蓋）→event-signup加`/hooks/github-curated`(HMAC)＋每repo掛webhook→聯想宏碁`feed_junshi_handoff.ps1`加「貼event /curated/網址→指路GitHub」＋Mac `projects/INDEX.md`策展卡→模擬聯想push驗證線上換新；順手清ema/huitou origin夾帶的GitHub金鑰。 |
| 🟡 | **團隊協作全面體檢（2026-09-24 Opus 5.5）：五項修法教練13:37說「執行」，已落地** | ⚠️持續追蹤-首次真實使用待觀察 | 完整報告`knowledges/2026-09-24_團隊協作全面體檢報告.md`。①每日08:10全隊點名`scripts/daily_team_rollcall.py`+launchd`ai.openclaw.daily-rollcall`(13:41實跑送達)；VPS/LINE健檢改為只在異常時通知②VPS看守Mac：VPS`/root/watch_mac.sh`每30分，Mac連續兩次連不上才通知(測試訊息message_id 3860送達)③上傳頁`kind`必填，`creation`全自動進coach888最新作品——**09-25首次真實作品實測，發現index.html判斷bug已修復**（個人創作常沒有index.html慣例檔名，改成剩一個html檔就自動採用，見v249），真實上架成功④產業鏈同主題同對話10分鐘防重複⑤VPS健檢拿掉1小時無活動誤報；赫米斯記憶檔金鑰是教練指示保留的寫法，不搬。commit`b076a80fc`+`777c9c7c4`。**VPS升級另見下一列**。VPS健檢缺天原因仍未查明，改由每日點名檢查「今天有沒有跑」。 |
| 🟡 | **雲端工作頁規則同步（2026-09-25 Opus 5.5，教練原則：同一套規則本機雲端一體適用，只有動到Mac本機的事例外）** | ✅已上線，兩條路實測通過 | 機制與SOP見記憶`reference_move_to_cloud_this_repo_2026-09-25.md`：`cloud_sync/`(全域規則+11技能副本，每則回覆結束自動更新)+`workspace/.claude/settings.json`(main)+外層`.claude/settings.json`+`cloud_bootstrap.sh`(master)。commit`1e0bea3ab`+`2db3d1330`(workspace)、`a0975a949`(外層)。**待修小bug**：`model_tier_advisor.sh`剛用/model切換後的第一則仍顯示舊模型(09-25切Opus後仍報sonnet-5)，雲端第一則顯示「未知模型」。外層master分岔已查證安全並合併推送`f517ec524`，v247「791d775d2未push」一句已過時。 |
| 🟡 | **公開交接棒「隨身軍師・一鍵接手」上線（2026-09-25，教練說「推」，後續修好AI相容性問題）** | ✅已上線，每次「總結」自動更新 | **主要網址（貼給任何AI）：`https://coach1973.github.io/ai-go/status.html`**；純文字備用：`status.md`。目的：教練Claude每週額度不夠，思考型問題分流到其他網頁版Opus，貼一個網址對方就知道規則＋目前工作狀態。🔴**真因查證（curl實測，不是猜的）**：一開始只做.md版，教練回報「其他AI說讀不到、被屏蔽」——查證GitHub Pages對.md副檔名回傳`content-type: text/markdown`，index.html回傳`text/html`；人爬蟲UA(GPTBot等)全部200無阻擋，不是robots/WAF——是多數AI內建讀網頁工具只認text/html。已建`scripts/render_public_status_html.py`(python-markdown轉換+bare URL自動連結)，`status.md`仍是唯一手改來源，`scripts/publish_public_status.sh`每次發布自動轉出`status.html`不會分岔。更新流程：`summary_upload_trigger.sh`第5步改寫`~/github_repos/ai-go/status.md`→跑`publish_public_status.sh`(機密掃描→轉HTML→再掃描→commit兩檔→push→確認網站換新版，等5分鐘)。只寫教練自己的事，不寫帳密/主機位址/路徑/他人個資。已收進coach888「工具類」第一項並改指向.html（伺服器狀態+靜態HTML都改，舊狀態備份`state/coach888_state_backup_20260925_110956.json`）。同場順便修正教練品牌數據「1.5萬位老闆」→「6,000+場演講、10萬人受眾」（教練親口訂正，5個檔案）。🔴**教練追問揪出遺漏**：status.html內文引用的另外兩份`coach-persona.md`/`system-prompt.md`本身也是同一個content-type問題，沒有一起修——已比照建`coach-persona.html`/`system-prompt.html`，三份都納入`publish_public_status.sh`自動轉出，`index.html`的「查看全文」連結也改指向.html（JS一鍵複製到剪貼簿的fetch()維持指向.md不變，複製出來才是純文字不是HTML標籤）。順便修好`publish_public_status.sh`驗證上線的迴圈：GitHub Pages CDN偶爾超過5分鐘才生效，push本身成功卻被誤判成失敗跳exit 1（已實際發生2次），改成push成功就算數，CDN慢只如實回報不當失敗。commit：workspace`445210e92`+`8f953cd14`+`5ea38190d`、ai-go`39b84c7`+`22bbe94`+`5114dc3`+`3f4273e`、coach888`79a7d81`+`03021cb`。 |
| 🟢 | 外層`~/.openclaw`本機git歷史紀錄跟GitHub版本編號對不齊（純本機書面整理，教練2026-09-24裁示：不是外洩、不是公開風險，AI自行找時間處理，不用再提） | ✅無風險-低優先-AI自主處理 | **教練2026-09-24明確裁示**：這不是安全問題（金鑰外洩早在9/19處理完畢，repo本身是私有的、沒有外部協作者，也已決定金鑰不rotate），純粹是這台Mac的git紀錄本子跟GitHub對不上編號的書面瑣事，沒有任何被公開查到的風險，也沒有立即性危害。**教練要求：AI不准再主動提這件事，覺得需要處理就自己找時間安靜做完，不要拿來討論、不要問、不要當成待辦逐場複誦**。哪天AI自己收拾好了，直接做、不用報告；沒收拾好也不影響教練現在用的任何功能，不追蹤、不升級語氣。技術細節（若AI自己要動手）：新版GitHub歷史已把`agent/auth-profiles.json`等金鑰檔從全部commit移除，本機若直接`git reset --hard origin/master`會把本機正在用的同名檔案從磁碟刪掉，須先備份+確認`.gitignore`涵蓋再處理，過去做法可參考`c07544815`的worktree cherry-pick模式。 |
| 🔧 | **AI技術備忘（不准拿去跟教練講）：這個repo的git歷史已被改寫，其他機器的本機clone要先同步才能push** | ⚠️任何機器的AI下次動這個repo前自己看 | 2026-09-19 06:45教練親自裁示後，軍師用`git-filter-repo`把`路徑大全_憑證層.md`+`agent/auth-profiles.json`+`agent/models.json(.bak)`4個含明文金鑰的檔案從全部16000+ commit歷史徹底清除+強制推送到GitHub(已用全新clone獨立驗證確認乾淨)。**任何其他機器(聯想Windows/ACER/VPS)如果有這個repo的本機clone，現在都跟GitHub遠端分岔了**——下次要push前必須先`git fetch origin && git reset --hard origin/main`(或直接砍掉重新clone)，絕對不能在沒同步的狀態下直接push，否則會把舊歷史(含外洩金鑰)重新推回去，等於這次白做。教練同時裁示：外洩的金鑰(MiniMax/Gemini)**不rotate**，「已經曝光不代表會被濫用，換的話動一髮牽全身」。完整過程見[[feedback_credential_layer_file_was_git_tracked_2026-09-19]]。 |
| 🔴🔴🔴🔴 | **全機必讀：Netlify圖片部署事故檢討報告** | ⚠️永久提醒 | 2026-07-25聯想機一件本該一次做對的事做了3次部署才成功（多扣30點credit），教練親自要求全機軍師都要吸收教訓，完整報告見`knowledges/2026-07-25_ai-talk圖片部署事故檢討報告_明明有SOP卻沒執行.md`。三條鐵律：①Netlify `_headers`不用`/*`萬用規則(除非站台永遠沒圖片) ②Windows打包zip給Netlify禁用PowerShell`Compress-Archive`(反斜線路徑會404)，改用.NET ZipArchive ③部署後驗證文字跟圖片要分開各自curl確認，圖片要專查Content-Type不能只看狀態碼 |
| ⚠️ | Netlify部署額度 | ⚠️持續追蹤 | credit制，「剩幾次」=credit餘額÷15(每次部署耗15點)。`state/netlify_deploy_quota.json`最新記錄剩50次(2026-08-05，jiesheng-leadership git-auto-deploy推送後)。這只是本地推算，建議教練有空時親自到Netlify後台billing頁面核對一次真實數字最保險 |
| 🔴🔴🔴 | **Netlify站分兩型，動手前必查是哪型(2026-08-05二度誤推)** | ⚠️永久提醒 | `feedback_netlify_deploy_zip_api.md`早就記載`jiesheng-leadership`是GitHub自動部署型(2026-06-09第一次血淚)，本場(2026-08-05)Sonnet 5仍然只想著「教練說先推GitHub」沒有觸發查證動作，導致同一個錯犯第二次。已補進記憶+更新MEMORY.md索引標題直接寫「動手前必查是哪型」。**新鐵律**：聽到「推GitHub」這類指令，只要牽涉Netlify網站，一律先查是不是自動部署型，不能拆開處理成「先推一半」 |
| 🔴🔴 | 聯想C槽94GB備份（`易数一键还原Windows系统备份`）**原訂計畫改變** | ⚠️持續追蹤-暫緩刪除 | 2026-07-25發現這份7/11舊備份剛在7/24真的被拿去做過一次系統還原（LINE junction事故+WMI/CIM異常，救回一台機器），證明它有實際救援價值，**不能照原計畫刪除**。建議教練確認今天新裝的OpenCode/CC Switch搬家+Advanced SystemCare移除都正常後，做一次新的一鍵備份取代這份舊的，新備份穩定觀察期滿才能考慮刪舊的，詳見[[project_lenovo_c_drive_slimdown_2026-07-11]]更新 |
| 🟡 | **shops.bymyway.com已拆除VPS依賴（2026-09-26）；09-27教練拍板全站統一event.bymyway.com/curated/，shops只剩舊連結轉址。VPS上舊檔案+GitHub孤兒repo收尾** | ⏳待處理-低優先 | 3家店(huitou/ema/hsinhan)已遷移到Mac本機+DNS切換完成，VPS(43.245.60.200)上`/var/www/shops/`原始檔案故意沒刪，當一段時間的rollback安全網，穩定觀察期(建議至少2週無異常)過了可以安全刪除。另外測試時意外建立的GitHub孤兒repo`coach1973/hsinhan-2`因手上token沒有`delete_repo`權限刪不掉，已無任何連結指向它、無害，之後若拿到有delete權限的token可順手清掉。詳見`knowledges/LETTER_VPS策展中心遷移過程說明_給Opus_2026-09-26.md`。**09-26 Opus審議**：遷移時shops路由沒比照/curated/的白名單，整個github_repos(含來賓名單.db)可被外人下載，已修(白名單+敏感副檔名防線，實測)，詳見信第八節。 |
| 🟡 | MEMORY.md超過OpenClaw 2萬字bootstrap上限(20,717字)且有1處UTF-8亂碼，跟HEARTBEAT.md同一類問題(2026-09-25查到，只查不動，優先度低於HEARTBEAT.md因為不影響小龍蝦即時反應) | ⏳待處理 | 用跟HEARTBEAT.md同樣手法瘦身：找出佔比最大的段落搬去handoff_archive或distill、備份原檔、確認新檔UTF-8正常。不用問教練，AI自己找時間做完即可 |
| 🟡 | 軍師自我要求：查證前先查「路徑大全」+盤點類任務要窮舉底層資料結構 | ⚠️永久提醒 | 教練v90當場糾正兩次查證不完整（VPS沒先查路徑大全就回報查不到、LINE帳號盤點漏算沒有名稱標籤的「龍蝦小助教」），教練明確期許「你是所有資訊的大總管，要自己想辦法完善」。已寫入試金石案例55，核心自我檢查：①任何「查不到/做不到」結論前先確認查過該環境萬用索引檔 ②盤點類任務直接數清楚底層資料結構(JSON物件key數)逐一核對，不能只挑印象中顯眼的幾筆 |

---

> 📦 v112～v267 各棒的封存檔名一覽已搬到 `handoff_archive/INDEX_舊棒封存指標_v112-v266.md`（v266~v267 另見 `handoff_v266_to_v267_and_goal_section_archived_2026-10-02.md`）（2026-10-02，主檔只留最新兩棒＋待辦表）
