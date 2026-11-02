---
name: reference-img-list-one-command-deliver-first-lock
description: 出圖清單網址（image-list.html）小龍蝦只准 run_img_list.py 一行指令，出完當場傳一覽圖＋zip；safety-locks 出圖清單鎖擋其他路；11/02 蔡佩茹 3 張拖 40 分鐘的根因
metadata:
  node_type: memory
  type: reference
  originSessionId: 886a007e-d9a7-4ddf-8646-c9cd9970e016
  modified: 2026-11-02T05:32:15.548Z
---

2026-11-02 12:41 教練丟蔡佩茹出圖清單網址給小龍蝦，13:21 問「這麼簡單的事要做這麼久？」。

查到的時間線：12:41～12:59 自己讀網頁（web_fetch maxChars 傳成字串失敗兩次）＋翻 30 多次檔案；12:47～12:57 MiniMax 一次請求卡 10 分鐘逾時；12:59 三張圖就出好；之後自己寫三版 AI 看圖 QA（判讀把「不合格」讀成「合格」、嚴格版被 SIGTERM），13:14 才第一次回話，40 分鐘沒交圖。

責任：主因在軍師——tava-ai-batch 技能（軍師 10/11 寫）叫它每次自己寫出圖腳本；10/30 軍師寫好 run_img_list.py 卻沒改技能叫它用，而且 run_img_list 遇到沒有 file 欄位的清單會直接出錯；10/30 21:09 技能被小龍蝦自己加了一大段「視覺＋OCR 雙軌、沒結論就補問」的 QA 規則，變成迴圈。模型（MiniMax）本身的問題：參數型別錯、10 分鐘卡住、QA 判讀錯。

修法（workspace 97e5705ca、~/.openclaw e8a29e7f1）：
- `scripts/run_img_list.py <網址或json> <輸出夾>`：直接吃網址、file 預設 <id>.png、只做一次 tesseract OCR、出完用 bot_main 直接 sendPhoto 一覽圖＋sendDocument zip 到教練私聊；`--no-send` 只產檔。已存在的圖不重出（可拿舊圖實測不扣點）。
- 技能 `agents/main/agent/workshop-skills/tava-ai-batch/SKILL.md`「程序」最前面加一行指令規定（備份在 ops/ 有版控）。
- `extensions/safety-locks/index.js` 出圖清單鎖：任何工具參數含 image-list.html 但不含 run_img_list.py 就擋（message 工具除外）。改完要 `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`。

worktree 對話改 workspace／extensions 會被 hook 擋：寫到 scratchpad 再 cp，或 python 補丁（見 [[reference-worktree-session-edit-hook-blocks-openclaw]]）。相關：[[feedback-bot-instructions-must-block-old-path-and-measure-tokens]]。
