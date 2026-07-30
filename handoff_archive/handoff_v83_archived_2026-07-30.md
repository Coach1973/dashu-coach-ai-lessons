# 軍師接力棒 · 2026-07-26 v83（Mac桌面版 Sonnet 5，系統權限缺口正式解決+開工額度瘦身58%+教練雙LINE身份釐清）

> 建立時間：2026-07-26 深夜～07-27 凌晨（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v82（Mac桌面版Sonnet5，結繩領導學戰報系統上線）
> 本棒主軸：**接續v82尾聲留下的兩個未解問題：①系統權限缺口(public agent沒有工具限制)②圖片OCR工具。本場教練先轉發小龍蝦整理的LINE綁定時間軸研究，逐行查證全部準確後，發現OpenClaw原生`tools.toolsBySender`機制，比之前設計的「移除exec+hook替代」方案更直接，當場實作+驗證+commit，權限缺口正式解決。教練釐清「鎖權限不能連個人化服務都擋掉」，新增line-user-memory hook補上訪客記憶功能。教練親測時意外發現自己有第二個LINE身份「贏家思路」，也一併加入白名單。教練接著要求評估「開工」占用多少KB，實測抓出接力棒被workspace/CLAUDE.md與六步驟hook重複注入的問題，修好後單場注入降58%，順手清理MEMORY.md索引裡7條已解決的舊記憶。教練詢問接力棒實際內容，也詢問小龍蝦後台為何不顯示中文名稱——查證後確認是OpenClaw原生介面已知限制，評估自建頁面成本後教練裁示不做，改用隨問隨查方式。OCR工具本場雖未動，但交接棒走出v83後終端機那邊07:01已抽出通用工具完成（commit `1488b6c68`），13:36 教練親自驗收，標記為「已完成」。**

## 🎯 本場戰果

### 1. 🔴🔴🔴 系統權限缺口正式解決：OpenClaw原生`tools.toolsBySender`取代卡關已久的exec移除方案
教練轉發一份小龍蝦整理的「LINE龍蝦小助教綁定教練ID完整時間軸」，逐行核對`verbatim/*.jsonl`原始記錄+`.memsearch`檔案，確認每一筆引用(含精確行號、教練原話)全部準確。但該文件建議的解法（把`allowFrom`限縮成只有教練ID）會打臉教練同一份文件自己引用的SOP、也會打斷BNI會員/121位好友的開放聊天功能，予以指出並修正方向。上網查證(WebSearch+直接讀本機安裝的OpenClaw原始碼`/opt/homebrew/lib/node_modules/openclaw/dist`確認非文件想像)找到`tools.toolsBySender`：可依發送者ID分別設定`deny`/`alsoAllow`，且證實運作在**主要工具判斷流程**(非僅sandbox模式)。為`bni_tainan`/`jiaolian_thoughts`兩帳號設定：教練LINE ID(`id:U895a0ad8...`)保留完整權限，`"*"`(其他所有人)deny掉`group:runtime`(exec/process)+`group:fs`(read/write/edit)+`group:automation`(cron/gateway)。同時修好`knowledge-search-inject`/`bni-calendar-inject`兩支hook缺少`path`欄位的註冊bug並正式啟用(之前一直是"disabled"從未被驗證過會不會觸發，這次修好bug後兩者都顯示`✓ready`)，確保知識庫問答功能在鎖權限後仍正常運作。commit `fb222757`。

### 2. 🔴🔴🔴 教練提醒「鎖權限不能連個人化服務都擋掉」，新增line-user-memory hook
教練指出要像VPS版小龍蝦一樣，訪客仍要能被記住喜好、能搜尋、能對話、能被分析圖片——單純deny整組`group:fs`會連這些合理功能都砍掉。查證VPS版做法(`clients/{id}.md`per-user檔案)後，設計新hook`line-user-memory`：**完全不給agent任何write/exec工具**，改由Node.js伺服器端(不受LLM對話內容影響)幫每位訪客維護`agents/<accountId>/clients/{userId}.md`，每則訊息自動讀取歷史+注入context+append新內容。教練本人(含後述第二身份)排除在外。本機模擬呼叫測試3種情境(新用戶首次/二次讀到歷史/教練身份正確跳過)全部通過才commit。

### 3. 🎯 教練測試「龍蝦小助教」意外發現第二LINE身份「贏家思路」
教練逐一測試三個LINE帳號，小幫手/教練都在想什麼皆正常，但測試「龍蝦小助教」(default帳號，綁`main` agent)觸發陌生人配對碼。查證這組ID(`U168903487f0ba2b666ddc62b854de351`)，直接呼叫LINE API確認displayName是「贏家思路」——教練確認這是他自己的第二個LINE帳號。已核准該配對碼(僅此帳號一次性approve，non-broadcast)，並把這組ID也加進`bni_tainan`/`jiaolian_thoughts`的toolsBySender白名單，確保教練用任一身份測試都保有完整權限。**教練明確裁示：「龍蝦小助教」維持個人專用，不比照另外兩個帳號開放allowFrom:["\*"]**——因main agent本身無工具層級限制，開放給陌生人風險遠高於已鎖權限的bni_tainan/jiaolian_thoughts。

### 4. 🎯🎯 開工KB額度評估+瘦身58%
教練要求實測「開工」占用多少KB(對應對話1M上限)。逐項量測後發現：①`workspace/CLAUDE.md`本身已由既有`sync_handoff_to_claudemd.sh`每5分鐘自動鏡像接力棒全文，桌面版啟動讀CLAUDE.md就會看到；②六步驟hook(`feed_junshi_handoff.sh`)卻又完整cat一次同一份接力棒——等於同一份東西送兩次；③`claude-sessions/`最新session總結機制已死掉18天(卡在07-08一次性匯入，注入的是07-01一場無關的ACER設定總結)。修復：接力棒改成先比對sync marker時間戳，確認CLAUDE.md鏡像是最新的才用短版指向(不重複貼)，若鏡像不新鮮則安全退回完整貼上(**接力棒內容本身完全沒被簡化，教練2026-05-29的「接力棒不可簡化」鐵律沒有被違反，只是不重複送**)；砍掉死掉的session總結注入；試金石案例3→2；memory最新日改尾端約6000字。本機實測：故意把sync marker調到過期狀態，確認安全網真的會退回完整貼上才commit。單場注入從49,593 bytes降到20,588 bytes(降58%)。另外配合教練確認，把`MEMORY.md`索引裡7條已完全解決、跟現有待辦無牽連的舊專案記憶退休(31,497→30,052 bytes，原始檔案保留磁碟未刪)。commit `e9144daf8`(六步驟)+`12e7b6b54`(MEMORY.md)。

### 5. 🎯 教練詢問接力棒內容+小龍蝦後台中文名稱問題查證
教練直接問「接力棒的內容是什麼」，用白話向教練說明接力棒=「現在還欠什麼」的追蹤表+「最近做了什麼」的詳細日記兩塊構成。另外教練反映小龍蝦後台(OpenClaw原生「控制」Control UI)一直看不到用戶中文名稱，查證CLI選項+GitHub議題(至少8個開發者提過同樣需求，官方均未解決)確認這是原生介面本身的功能缺口，不是設定漏掉，也澄清`seabiscuit.bymyway.com`其實只是同一套原生介面的另一個網址別名，不是獨立打造的頁面。評估「另建自訂頁面」的時間(30~90分鐘)/token成本後，教練裁示**不建頁面，看到陌生ID直接問軍師查`state/{account}_line_id_map.json`對照表即可**。

## 📋 下一場直接開工任務

**🔴🔴🔴 BNI大台南小幫手「主動提醒」功能**（工作總表最熱項目，v77 已設計好整套事件驅動流程 cron `--at --delete-after-run` 架構，方向清楚動手即可，不再傾向空泛討論）：教練提出「BNI 會員加入/業績達標/特定節日/會議前 1 小時」等情境要主動打給對方。詳見v77設計文件。註：v83 接力棒本來寫「OCR 通用工具」但實際上 07:01 終端機那邊已抽出 `tools/ocr-extract/ocr_extract.py` 完成（commit `1488b6c68`），且 13:34 教練已親自在終端機跟軍師確認「未來會用 OCR 取代燒 Token 視覺看圖方式」，本場順手換成下一個真正待辦。

## 🔑 本場關鍵檔案索引
- `openclaw.json`：新增`agents.list[bni_tainan/jiaolian_thoughts].tools.toolsBySender`(教練兩個LINE身份白名單+`*`deny規則)、`hooks.internal.entries`修好path+啟用knowledge-search-inject/bni-calendar-inject/line-user-memory
- `hooks/line-user-memory/{HOOK.md,handler.js}`：新hook，訪客個人化記憶不靠write工具
- `scripts/feed_junshi_handoff.sh`：接力棒防重複注入安全網設計+死code清理+試金石/memory瘦身
- `claude-brain/MEMORY.md`：退休7條舊記憶
- `handoff_archive/handoff_v72_to_v81_archived_2026-07-26.md`：v81併入封存
- commit序列：`fb222757`(權限鎖+line-user-memory) → `e9144daf8`(六步驟瘦身) → `12e7b6b54`(MEMORY.md瘦身)

---

> 📦 **v82及更早的完整接力棒內容已封存**：`handoff_archive/handoff_v82_archived_2026-07-28.md`（v82單獨一份）+ `handoff_archive/handoff_v72_to_v81_archived_2026-07-26.md`（v72~v81）
> 瘦身原因：教練2026-07-26指出接力棒檔案太大，每次「開工」自動注入會吃掉新對話框大量額度，
> 只保留最新2棒(v84/v83)在主檔，舊棒需要查歷史時才去讀封存檔，不再每次自動注入。
