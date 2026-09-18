---
name: industry-chain-sop
description: "孔大哥/佩佩老師說「XX的產業鍊SOP」時，伺服器端(Node.js)呼叫MiniMax組prompt+lk888生圖+推Telegram，不需要agent拿到exec工具權限"
metadata: {"openclaw":{"emoji":"🎨","events":["message:preprocessed"]}}
---

# Industry Chain SOP Hook（產業鍊圖生成，不需要exec/runtime工具）

## 背景

2026-09-16教練交辦BNI組隊計畫的產業服務鏈自動生圖技能（見workspace/SOUL.md「產業鍊SOP」
段落，main agent走那條路，因為main agent沒有工具權限限制）。孔大哥（kong）、佩佩老師
（peipei）本人透過自己的Telegram帳號跟各自的特助互動時，`tools.toolsBySender`把
`group:runtime`（exec）擋掉了（只有教練帳號id:6124913915是完整權限）——查`openclaw`官方
文件確認`group:automation`只有`heartbeat_respond`/`cron`/`gateway`，不含exec，所以「只開
一點點自動化權限」這條路走不通，唯一風險可控的做法是比照`bni-reminder-schedule`hook的
既有模式：伺服器端（Node.js，不受agent工具權限限制）直接代勞整個流程，孔大哥/佩佩老師
的agent工具權限完全不變。

## 觸發事件

`message:preprocessed`，跟`bni-reminder-schedule`同一個事件。

## 機制

1. 判斷sessionKey的accountId是`kong`或`peipei`
2. 判斷發送者是孔大哥（`8689825759`）或佩佩老師（`8786886419`）本人（2026-09-16從各自
   sessions目錄的真實sender_id統計出來，非教練提供，因為系統裡沒有記錄他們的ID）
3. 文字含「XX的產業鍊SOP」或「XX的產業鏈SOP」時抽出XX
4. 呼叫MiniMax API（`https://api.minimax.io/anthropic/v1/messages`，key讀自
   `agent/auth-profiles.json`的`minimax:default`profile）請它組一個符合鴻達醬油行範例
   格式的完整圖片生成prompt（中心角色+標題+目標客群+15~20個異業服務節點）
5. `execFile`呼叫`scripts/generate_industry_chain.py --prompt "<MiniMax生成的prompt>"
   --telegram-chat-id <發送者本人id> --telegram-account bot_kong（或bot_peipei）`，
   該腳本呼叫教練已付費的lk888 API（GPT Image 2）生圖後直接推送Telegram
6. 全程孔大哥/佩佩老師的agent不需要看到、也不需要有任何exec/fs工具權限

## 已知限制

- MiniMax組出來的prompt品質不保證跟main agent（Sonnet/Opus推理）一樣好，異業服務類別
  可能不夠精準，是刻意的取捨（教練要的是「風險可控」優先於「品質最佳」）
- 跟main agent一樣，lk888/GPT Image 2大約5~10%機率某個節點文字出錯，不自動重試（教練
  已表態不追求完美、不浪費付費額度）

## Log

`~/.openclaw/hooks/industry-chain-sop/hook.log`
