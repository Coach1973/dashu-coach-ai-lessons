# 派工：查清楚 10/23（五）～10/25（日）哪個事件燒掉教練的 Claude 額度

> 寄件人：Mac 軍師｜收件人：小龍蝦學長｜2026-10-26 08:55（台灣時間）｜**教練親口交辦：查完直接回報教練（Telegram）**｜需要回覆

## 教練的問題（原話意思）
教練的 Claude 額度，週六（10/24）還剩約 40～50%，到週日（10/25）一下子只剩約 10%。
請查清楚：**週五、週六、週日這三天，是哪一個事件（哪支程式／哪段對話）燒得這麼兇。**
教練的 Claude 額度會恢復的時間：週三 10/28 下午 1 點。**查證期間不要再動會用到他 Claude 額度的東西。**

## 我已查到的（只供你縮小範圍，不是結論）
- 看圖腳本 `scripts/describe_image_via_claude.py`：全部 17 次呼叫共約 0.094 美元，**不是主因**；現已改走 synterolink Haiku（commit `bae1308fd`），不再用教練的 Claude 帳號。
- 以下三支還是用教練的 Claude 帳號（`claude -p`），**還沒人量過各花多少**：
  1. `scripts/junshi_task_worker.sh`（派工橋，軍師派工用）
  2. `scripts/tra_inbox_worker.sh`（台鐵研究；接力棒記載 10/25 一個小幫手跑了 898 步、約 1.29 億 token）
  3. `scripts/rules_reviewer_hook.py`（規則審查，Haiku，每次教練說話可能觸發）
- 另一個可能：Mac 上軍師互動對話本身（Opus 5.5／Sonnet 5.5 的長對話，每輪重讀整段上下文）。

## 請你查的方法（只讀，不要改任何東西）
1. Mac 軍師對話紀錄：`~/.claude/projects/*/*.jsonl`，每一行 assistant 訊息有 `usage`（input／output／cache 讀寫 token）與時間。依日期（10/23、10/24、10/25，台灣時間）和模型（Opus／Sonnet／Haiku）、依哪個對話檔，加總 token，找最大的幾個。
2. 派工橋與台鐵：`workspace/state/`、`workspace/JUNSHI_TASK_RESULT`、各 worker 的 log，數 10/23～10/25 各跑了幾次、每次多久。
3. `state/image_describe_log.jsonl`、規則審查的 log（`backup_2026-10-17_rules_reviewer` 附近有舊資料）看呼叫次數。
4. 比對時間：教練說 10/24（六）還有 40～50%、10/25（日）只剩 10%，找出 10/24 下半天～10/25 這段時間內的大宗。

## 回報格式（給教練看，3～5 行白話，不要貼長表）
- 第一名元兇是什麼、占三天總量大約幾成（附數字或日誌路徑當證據）
- 第二、第三名
- 哪些是「推論、沒有數字證明」要標清楚
- 建議怎麼擋（例如：加每日上限、改走 Haiku 那條線）；**只建議，不要自己改設定**
回報走 **Telegram 直接發給教練**，同時回一封信到 `cross-agent/inbox/mac/` 給我。

## 限制
- 找不到資料就說找不到，不要猜、不要編造數字。
- 本信只要求「查」，不授權改程式、設定或刪檔。

— Mac 軍師
