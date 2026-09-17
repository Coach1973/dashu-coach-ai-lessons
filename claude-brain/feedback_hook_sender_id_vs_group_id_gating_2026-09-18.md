---
name: feedback-hook-sender-id-vs-group-id-gating-2026-09-18
description: industry-chain-sop hook誤鎖「只認孔大哥/佩佩老師本人Telegram ID」，但兩人助理實際跑在群組裡，教練本人在群組下指令時被悄悄擋掉，hook從未真正觸發過
metadata:
  type: feedback
---

任何伺服器端hook若設計成「只服務特定人本人」，要先查證那個人的AI助理實際運作場景是1對1私訊還是群組——群組裡任何一則訊息的sender可能是群組內任何成員（含教練本人），不會固定是那個人自己的ID。

**Why**：2026-09-16建立`hooks/industry-chain-sop/`時寫死`allowedSenderId`只認孔大哥(8689825759)/佩佩老師(8786886419)本人的Telegram ID，但查證發現兩人的AI助理實際上都跑在各自專屬Telegram群組（孔大哥群組`-5083547625`、佩佩老師群組`-5115910257`），教練本人直接在群組裡下指令測試時，`event.from`是教練自己的ID不是孔大哥/佩佩老師的ID，這條規則悄悄`return`擋掉，**hook從2026-09-16建立以來從未真正觸發成功過一次**（`hook.log`檔案一直不存在）。教練親口糾正：「這些指令都是我下的，不是佩佩老師下的，也不是孔大哥下的」，點破了設計者(軍師)對「本人」的定義跟實際使用場景不符。副作用：孔大哥的AI助理收到訊息後，因為hook沒攔截，自己土法煉鋼呼叫內建`image_generate`工具，落到minimax/image-01(不支援中文)的fallback，這正是先前「生成的圖沒有中文」問題的真正根因，跟SOP流程本身無關。

**How to apply**：2026-09-18已修復——把gating從`senderId`改成`groupId`（群組本身已經是受控私人群組，裡面任何人講都算數），用直接呼叫handler()的合成事件實測驗證TRIGGER/PROMPT正確產生，並用真實`generate_industry_chain.py`呼叫成功推送圖片到孔大哥群組(`-5083547625`)確認端到端可用。往後任何新hook若鎖定「服務某個特定人」，動手前先查證這個人的訊息實際上是1對1私訊還是群組訊息，群組場景一律改用`groupId`或`chatId`比對，不要用`senderId`比對本人身份。

相關：[[project_industry_chain_sop_four_way_2026-09-16]]
