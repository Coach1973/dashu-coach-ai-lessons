---
name: project-line-per-user-memory-standardization-2026-08-14
description: 教練要求三個LINE帳號(龍蝦小助教/BNI小幫手/教練都在想什麼)每個用戶都要有專屬記憶空間，查證後發現main/default頻道從未真正運作過，已修復並驗證
metadata: 
  node_type: memory
  type: project
  originSessionId: 7c3bfad2-6f16-4c09-ab1c-23bcf3e61ae2
  modified: 2026-08-13T18:11:12.542Z
---

教練在[[feedback_line_identity_missing_from_people_md]]那次「您是哪一位」事故後，明確要求：三個LINE版小龍蝦（`main`/default「龍蝦小助教」、`bni_tainan`「大台南南區小幫手」、`jiaolian_thoughts`「教練都在想什麼」）**每一個用戶(含教練本人)都必須有專屬記憶空間**記住對話——這是「鐵板釘釘、非常強烈的要求」，不是建議。

**逐一查核結果(2026-08-14)**：
- `jiaolian_thoughts`：✅ 真的在跑，`agents/jiaolian_thoughts/clients/`下20個訪客各自有專屬`.md`檔，最新更新到8/13，內容是真實逐條累積的對話紀錄。另外seabiscuit.bymyway.com只是把這個agent的OpenClaw原生後台開了個友善子網域，看的是原生session瀏覽，跟這套clients/*.md是並行的兩套資料。
- `bni_tainan`：✅ 機制同樣在跑，目前只有1位訪客有記錄檔（帳號較新，用量少符合現況，不是bug）。
- `main`/default（龍蝦小助教，教練自己天天用的主頻道）：❌ **原本完全沒運作過**，不是教練被排除這麼簡單。

**真根因是兩層，缺一不可，只修第一層還是不會動**：
1. `hooks/line-user-memory/handler.js`寫死`COACH_LINE_IDS`排除清單，理由「教練有自己既有的memory系統」——這假設對bni_tainan/jiaolian_thoughts或許成立，對教練天天在用的default頻道完全不成立
2. **更深層、影響所有用戶的bug**：`parseSession()`原本靠`sessionKey.includes('line')`判斷頻道，但`main`帳號的sessionKey固定是`agent:main:main`（頻道段落被收斂掉，不像bni_tainan/jiaolian_thoughts是`agent:<id>:line:direct:<userId>`格式），這個字串裡從來沒有"line"，導致這支hook對main頻道的**所有人**（不只教練）從第一道關卡就`return null`，整個機制形同虛設。

**已修復**：改用`ctx.channelId`判斷頻道（跟`hooks/inbound-message-echo-log`已驗證過的正式欄位一致），sessionKey解析法留著當備援；同時移除`COACH_LINE_IDS`排除清單。用合成簽章webhook實測驗證：教練的LINE ID傳訊息後，`agents/main/clients/{教練LINE ID}.md`真的被建立且正確累積，測試假資料已清除。commit `d12bc391`（workspace的people.md/USER.md身份對照修復是另一筆`246e51766`，兩者疊加才是完整解法）。已比對bni_tainan/jiaolian_thoughts真實log確認channelId正確回傳"line"，改動不影響既有運作。

**Why**：教練的核心價值觀是「記住用戶的話才叫在乎」（[[feedback_coach_words_are_sacred]]同一條神經），三個LINE小龍蝦人格一致是他刻意訓練的結果，記憶標準不一致等於人格不一致的破口。

**How to apply**：往後任何新增的LINE帳號、或任何要判斷「這則訊息是哪個頻道/哪個agent」的hook，優先用`ctx.channelId`/`resolveChannel()`這類已經對照過`openclaw`原始碼(`message-hook-mappers.js`)驗證的欄位，不要只憑sessionKey字串包不包含關鍵字做判斷——main/default agent的sessionKey格式跟其他具名agent不一樣，這個坑以後新hook都可能踩到。
