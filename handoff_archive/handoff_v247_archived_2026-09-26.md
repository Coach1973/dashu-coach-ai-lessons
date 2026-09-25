## 🔴 給跨對話框軍師讀的總結摘要（2026-09-25 04:15，Mac桌面版，v247）

**本場主軸：教練登出再登入後，赫米斯桌面版自己跳出來，要求「登入時不要啟動」。軍師繞了一大圈（先查Telegram連線、推給macOS重開視窗、開系統設定叫教練自己關、連帶把視窗開到擴充塢副螢幕），教練點出「LINE/Telegram都不會，只有Hermes會」才找到真因。教練收尾痛批：同樣的錯什麼時候才不再犯——已從機制修根源。**

### 1. 赫米斯登入自動跳出：已修
真因`~/Library/LaunchAgents/ai.hermes.desktop.plist`寫`RunAtLoad=false`，但`KeepAlive.SuccessfulExit`在launchd規則裡隱含RunAtLoad，每次登入照跑`open Hermes.app`（`launchctl print`顯示runs=1）。改`KeepAlive=false`，重新載入模擬登入runs=0。原檔備份`~/.hermes/ai.hermes.desktop.plist.bak-2026-09-25`。Telegram線`ai.hermes.gateway`沒動。教練定義：**「赫米斯」＝Mac桌面版Hermes.app**，Telegram線不碰、不當選項問（第3次混淆，已放MEMORY.md索引最上方）。試金石案例82。

### 2. 副螢幕：是軍師造成的，已裝防呆
Wokyis擴充塢附的1280×720螢幕（接953GB SSD和連接埠，**不能叫教練拔**），用Time Machine快照比對，設定自9/21起沒變過；今天是軍師`open`系統設定落在那台。新增`scripts/main_display_guard_hook.sh`（PostToolUse：開App/視窗/改html後自動把副螢幕視窗搬回主螢幕）+`scripts/move_windows_to_main_display.sh`，實測通過。

### 3. 背景項目54項盤點，封存3項沒用的
kong/peipei四月舊版獨立gateway（已改由主gateway bindings服務）＋gateway舊bak，含金鑰，搬到`~/Library/LaunchAgents_archive_2026-09-25/`不進git，說明`_archive/launchagents_retired_20260925/README.md`。其餘52項都在用，教練：「有用就留，沒用的不要留」。

### 4. 根源修法（不加記憶，改機制）
①`pre_task_hook.sh`加「🩺故障診斷法」：教練描述故障就注入「先找對照組→推論先用指令推翻→自己修完才報→3~5行」②`stop_rules_master.py`加A2「叫教練自己動手」擋下（今天三句原話實測全擋；「只有您能」＋密碼/連結等正當情況放行）。

### 5. 🧭 模型分工默契（教練親定）
重大決策、找根因、設計機制用 Opus；庶務用 Sonnet。規則在`knowledges/模型分工規則_Opus與Sonnet.md`，由`scripts/model_tier_advisor.sh`（UserPromptSubmit）自動評估：**v2（教練要求看得見）：每則交辦回覆第一行都標「🟢 Sonnet 就能做／🟣 Opus 等級」**；Sonnet 標🟣先建議切換不動手，Sonnet 卡關停下建議切 Opus；Stop hook A3 沒標示就擋。8 種情況實測通過。教練：本期流量（週三13:00重算）到週五04:13已用50%。

### 6. 教練體驗雲端方案（$100/月），實際搬過一次+踩到本repo分岔陷阱
外層`~/.openclaw`repo卡兩關：①常年背景雜訊要先commit（逐一查證排除533MB漫畫素材大檔，已補`.gitignore`，沒查到機密）②本機分支跟遠端因9/19金鑰清除是真分岔（領先/落後各25），直接push會把舊金鑰歷史推回去——改用`move_to_cloud`的`skip_push:true`，雲端從遠端乾淨版本接手，教練今天的實際工作內容都在`workspace`子repo（沒有分岔問題）已正常commit。雲端對話框連結：https://claude.ai/code/session_018RBKxnNSzFi3t68hTMaR9t 。查證發現：雲端session在本機`list_sessions`/`get_session`完全查不到，是claude.ai端獨立系統，教練要找回雲端對話框目前只能靠瀏覽器開claude.ai/code，桌面版側邊欄會不會顯示AI端看不到自己畫面無法驗證。SOP已寫`reference_move_to_cloud_this_repo_2026-09-25.md`。

### 7. 🔴 攔下一則可疑的英文git指令，沒有照做push
教練切換雲端/本機時，這個對話框收到一句風格明顯不像教練平常口吻的英文指令「commit+push」，研判是操作雲端切換時誤觸/誤送。查證：commit的部分（2個DREAMS.md）安全，已做；push那部分因為就是上一條講的分岔陷阱、會有推回舊金鑰歷史的風險，沒有自己決定做，回頭跟教練確認過。**目前仍是本機commit`791d775d2`，還沒push，教練若之後想通了要不要處理外層repo分岔，再說。**

### 📋 下一場開工先做
沒有要問教練的事。`sfltool dumpbtm`要管理員密碼會跳視窗，**不要再跑**。外層`~/.openclaw`本機commit`791d775d2`還沒push（分岔陷阱，見上第7點），不用主動處理，教練提起再說。

### 🔑 本場commit
`65e4060e8`（試金石82）`bd56c5e3f`（副螢幕防呆）`cceb8ae12`（封存背景項目）`fc3a764af`（模型分工v2）（以上皆workspace repo）；外層`~/.openclaw` repo `791d775d2`（DREAMS.md，本機未push）；本次總結commit另計。

---
