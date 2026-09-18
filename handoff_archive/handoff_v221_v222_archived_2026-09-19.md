# 軍師接力棒 · 2026-09-19 v221（Mac桌面版 Sonnet 5，手機Remote Control真正根因查明修復+舊SOP早有答案的教訓）

> 建立時間：00:07 ~ 00:43（約36分鐘）
> 上一棒：v220
> 本棒主軸：**v220留下手機Remote Control重啟卡死未解。教練追問「砍掉重練有沒有保證成功」逼出誠實答案（不保證，根因未查明），因此改為動手實測查證，最終挖出真正根因並修復，手機端已實際連線驗證成功。**

## 🎯 本場戰果

1. **真正根因查明**：`~/.claude/settings.json`的全域`env`區塊（MiniMax路由設定：API_KEY/BASE_URL/AUTH_TOKEN/MODEL/CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC）被claude CLI**無條件套用**到每一個claude呼叫，擋下`claude rc`必須的api.anthropic.com連線+feature-flag評估。v220的10處排除清單方向沒對準，因為settings.json env區塊的檢查跟已失效的`--setting-sources`flag問題疊在一起互相遮蔽，先觸發的錯誤訊息掩蓋了後面真正的問題。

2. **修復並實測驗證**：新增`scripts/restart_remote_control.sh`（啟動當下暫時移開settings.json，實測證實process只在啟動當下讀env一次，跟檔案是否持續存在無關），已測試2次成功。手機端實際連線並跑完一輪「開工」六步驟對話（tmux顯示`Capacity: 1/32`），教練親自在手機確認。同步修正`.zshrc`的`claude-remote`alias移除已失效的flag。

3. **誠實揭露架構後果**：這個修法讓Remote Control連線改走真正的Claude/Anthropic後端，不是MiniMax省錢管道。教練當場權衡並接受（「同一套嘛」不用再監測MiniMax品質/思考回路），2026-09-19確認裁示。

4. **官方內建Desktop App Remote Control機制**（`set_remote_control`）同樣被此根因擋下，但**當前session的process已啟動過久，env早已鎖定於記憶體**，settings.json事後修好也無法即時生效。查明正確做法：**教練說「總結」開新對話框即可，不需要整個關掉Desktop App重開**——因為每個新對話框都是全新process，會在當下重新讀取（此時已乾淨的）settings.json。

5. **事後發現**：09-17第一次設定`claude rc`時寫的SOP文件（`reference_claude_code_remote_control_setup_sop_2026-09-17.md`）早就完整記錄了同一個根因+同一個解法（甚至連「process啟動後跟設定檔是否存在無關」這句結論都已寫在裡面），v220+v221兩場合計數小時的排查本可以省下大半。已寫入教訓`feedback_search_existing_reference_before_deep_investigation_2026-09-19.md`：技術類排查任務動手前，先`grep`claude-brain全文搜關鍵字，不能只憑印象判斷「這是第一次遇到」。

## ⚠️ 本場教訓（已寫入記憶）

`feedback_search_existing_reference_before_deep_investigation_2026-09-19.md`：深入技術排查前先grep claude-brain全文搜關鍵字確認沒有既有reference記錄過同一問題，不能只憑記憶判斷「應該是第一次遇到」——本案例09-17的SOP早就寫好答案，卻被兩場session各自重新摸索了一次。

## 📋 下一場開工先做

1. **最優先，一句話可完成**：直接呼叫`set_remote_control(session_id="self", enabled=true)`，此時settings.json已是乾淨狀態，新process應可直接成功，開起來後跟教練確認手機App能看到這個新session。
2. 💬**試金石案例庫商業化討論**——v219/v220連續兩場被擠掉，本場又被Remote Control危機佔滿，第三度延後，下一場務必主動提起，不用等教練再問。
3. E16接力棒瘦身：主檔目前v218~v221共4棒，超過3棒上限，下次開工建議把v218(+中間那段未編號的舊戰果)搬進archive。
4. 沿用既有待辦：孔大哥/佩佩老師industry-chain-sop hook真人實測(教練不催)、peipei-ai-backup舊commit金鑰歷史(教練已表態不處理)、`stop_rules_master.py`規則#07誤判regex補丁。

## 🔑 本場commit

`8749afa87`（settings.json根因修復+`scripts/restart_remote_control.sh`+接力棒10/3狀態表更正為根因修復版）。本次總結另計，含教訓記憶+v221接力棒本身。

---

# 軍師接力棒 · 2026-09-19 v222（Mac桌面版 Sonnet 5，中正大學互動牆從零建置上線+赫米斯Telegram斷線16小時根因修復）

> 建立時間：00:50 ~ 03:40（約2.8小時）
> 上一棒：v221
> 本棒主軸：**教練9/19早上中正大學社團幹部專場臨時交辦：把tava-ai.com生成的WordPress外掛包（含互動提問牆功能）改走既有上架SOP併進event.bymyway.com，全程不碰WordPress。上線後歷經6輪UI/內容迭代才達到教練標準。收工前教練追問赫米斯為何斷線，查出是「全部釋放」誤將Telegram後端一併關閉16小時且看門狗機制設計上不會提醒，已修復並重新連線。**

## 🎯 本場戰果

### 1. 中正大學社團幹部專場互動牆從零建置上線（event.bymyway.com/ccu/）
教練把AI工具生成的WordPress外掛包丟過來，一度依說明書規劃WP安裝流程，教練澄清「這就是我們的策展SOP」後改弦更張：直接在既有`event-signup` Flask app新增`/ccu/`靜態頁路由+`/api/ccu/*`系列端點（提問/按讚/即時回饋/課後影音，含講者金鑰驗證），資料庫新增`event_wall_items`表，完全不需要另外裝WordPress、不需要教練另外記一組帳密。本機測試埠先過一輪API全端點測試才重啟正式服務，正式站curl+Chrome雙重驗證。

### 2. 六輪UI/內容迭代（教練逐步發現問題，最後一輪要求「全面掃描不要等我逐一講」）
①頂部標頭字級全部放大提亮（含教練二度指名的導覽列）②移除AI草稿留下的「給講者」佔位提示③講者照片從76px小圓頭像升級成大幅照片，取代原本「國立中正大學」事實卡（教練認為介紹校方沒意義）④全頁面系統性掃描29+處font-size/color宣告，統一標準到1.1rem+亮色，不再逐一等教練指出⑤標題文案+金句文案修正⑥「延伸資源」四連結全面換成教練指定的新目的地（大樹教育AI專頁/海餅乾俱樂部/乾淨世界頻道/教練都在想什麼AI禮物），新增TAVA AI設計credit。全程每輪都本機測試+真Chrome開圖驗證才回報，最後補上coach888收錄（大樹常用第一項）。

### 3. Stop hook coach888收錄鎖假陽性根因修復
自由文字commit訊息裡的逗號子句被regex誤判成候選項目名稱，且因為checker每次都重新掃描歷史300個事件，同一假陽性會在本場session無限重複跳出。已修過濾條件（長度>16或含逗號句號頓號），刻意不用「」引號當依據以免誤殺規則注釋裡記載的真實案例，寫測試腳本雙向驗證後才改正式檔案。

### 4. 赫米斯Telegram後端斷線16小時根因修復（教練當場糾正）
查證發現赫米斯gateway並非crash，是9/18 11:21「全部釋放」指令把`ai.hermes.gateway`（Telegram 24小時後端）跟三個桌面GUI服務一起bootout，且看門狗機制設計上把「服務未載入」一律當「教練故意關閉」不通知，導致斷線16小時教練完全不知情。教練糾正「全部釋放」的赫米斯範圍應該只限桌面版App，Telegram後端要24小時運作。已修`release_all_memory.sh`拿掉`ai.hermes.gateway`的bootout、現場重新load並驗證Telegram重新連線成功。

## ⚠️ 本場教訓（已寫入記憶）
1. `feedback_stop_hook_regex_false_positive_repeats_across_session_2026-09-19`：deterministic hook重複觸發時要查原始碼找bug，不要只是重複解釋。
2. `feedback_hermes_gateway_vs_desktop_app_distinction_2026-09-19`：赫米斯桌面版App跟Telegram後端gateway是兩回事，任何「關閉赫米斯」的腳本預設不能動gateway。

## 📋 下一場開工先做
1. 中正大學場後續：教練可能會回報現場實測狀況（提問牆/QR/講者控制列），有問題直接查`event.bymyway.com/ccu/?admin=1&key=TTqcQDDBr3QWNaZhOjKs`。
2. 💬試金石案例庫商業化討論——連續三場被擠掉，第四度延後，下一場優先主動提起。
3. 沿用既有待辦：孔大哥/佩佩老師industry-chain-sop hook真人實測、peipei-ai-backup舊commit金鑰歷史、`stop_rules_master.py`規則#07誤判regex補丁。
4. E16接力棒瘦身：本場已把v218/v219搬進archive，主檔維持v220~v222共3棒。

## 🔑 本場commit
`event-signup`（workspace repo）：`d47d1aa55`(互動牆初版)、`4afe486bc`/`32e7f1fb1`/`320ede8a0`/`83e633f71`/`05d65ba0d`(六輪UI/內容迭代)。`workspace`：`b6d173229`(MEMORY索引補漏)、`af919e683`+`3a3e47015`(stop hook假陽性修復+記憶)、`3d8d0b4e4`+`5c909eea0`(赫米斯根因修復+記憶)。`coach888`：`475d1d4`(新增ccu收錄)。

---

