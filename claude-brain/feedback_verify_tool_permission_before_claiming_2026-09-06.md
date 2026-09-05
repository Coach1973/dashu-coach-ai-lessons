---
name: feedback-verify-tool-permission-before-claiming-2026-09-06
description: 軍師寫SOP時斷言「小龍蝦沒有exec/fs工具權限」是錯的——查openclaw.json main agent沒設限制+教練當場實測ls -la成功，證實小龍蝦確實有終端機能力
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 30a88aa3-1421-4583-ad1b-b19b8a636b7f
  modified: 2026-09-05T16:58:43.782Z
---

2026-09-06寫「策展SOP」文件時，軍師直接斷言「小龍蝦（main agent）本身沒有檔案系統/執行指令的工具權限」，理由寫的是「toolsBySender已鎖exec/fs」——但這句話其實是把`kong`/`peipei`/`bni_tainan`/`jiaolian_thoughts`那幾個agent的限制規則，錯誤套用到`main`身上。

教練追問「小龍蝦不能做這件事嗎？只有我的帳號才能觸發，應該沒問題」，逼著回頭真的去查`openclaw.json`，發現：
- `kong`/`peipei`/`bni_tainan`/`jiaolian_thoughts`四個agent都明確寫死`toolsBySender`：`"*"`（除教練指定帳號外的所有人）deny `group:runtime`/`group:fs`/`group:automation`
- `main`（小龍蝦）的agent定義**完全沒有`tools`區塊**，沒有任何toolsBySender限制規則

**但**`SOUL.md`裡確實有一整套「派工單」機制（2026-08-24教練交辦），小龍蝦遇到需要動系統的任務是寫信給軍師代勞，不是自己執行——這套機制存在的前提，理論上代表小龍蝦做不到。兩邊證據互相矛盾，**最終沒有定論**，需要教練實測（直接叫小龍蝦跑一個終端機指令）才能確認真相。

**✅ 同一場對話當晚實測結果**：教練直接跟小龍蝦說「幫我用終端機跑ls -la」，小龍蝦真的執行了，回報251個項目、26.5MB、逐檔列出最新異動時間，還主動做環境快檢。**證實小龍蝦確實有終端機/exec能力**，openclaw.json的設定判斷是對的；SOUL.md的派工單機制不是「做不到才寫信」，比較可能是教練刻意設計的分工偏好。之後任何文件寫「小龍蝦能不能做XX系統操作」，可直接引用這次實測結果，不用再說矛盾未解。

**Why**：查證permission/能力邊界類的斷言時，直接照抄「感覺類似的其他agent限制規則」很容易套用到錯誤的對象上——`main`、`kong`、`peipei`、`bni_tainan`四個agent的id、限制設計目的都不同，不能因為都是「OpenClaw agent」就假設限制規則一樣。

**How to apply**：
1. 之後任何要斷言「某個agent沒有XX工具權限」的敘述，**先用`grep -n "toolsBySender" -A 20 openclaw.json`實際找到那個agent自己的定義區塊**，不要憑記憶或憑「應該跟其他類似的agent一樣」推論
2. 如果查到的設定跟實際觀察到的行為（例如SOUL.md寫的派工單機制）互相矛盾，誠實回報「兩邊證據對不上，需要實測」，不要選一邊當結論硬答
3. 這類「權限/能力邊界」的斷言，一旦寫進SOP文件被其他機器/AI引用（這次已經寫進`reference_curation_sop_2026-09-06.md`給Hermes讀），錯誤會被複製擴散，比單純聊天講錯更需要謹慎

Related: [[feedback_verify_dont_relay_secondhand_claims]]（同一類「沒有一手驗證就下斷言」教訓，但那篇講的是轉述別人的記憶檔案，這篇是把A agent的設定誤用在B agent身上）
