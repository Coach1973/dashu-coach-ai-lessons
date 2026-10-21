---
name: reference-poster-swap-lk888-two-images-bahai-sop
description: 海報「換人換字」做法：巴哈用內建出圖失敗（Google 金鑰無效），改走 lk888 edits 一次帶模板＋照片；規則只改照片＋頭銜、獎杯不動（只有教練本人橫版寫乾淨世界）；AI 畫小字常錯改用 PIL 貼字
metadata:
  node_type: memory
  type: reference
  originSessionId: ccd59c81-2e63-56a1-88cd-c295cb66bc90
  modified: 2026-10-21T17:18:51.481Z
---

- **巴哈助理** ＝ 分身 peipei（Telegram「佩佩老師的巴哈助理」群；它自己是獨立 git 倉庫 `agents/peipei`）。10/22 教練請它製海報卡關：內建 `image_generate` 走 Google 出圖，回 HTTP 400「API key not valid」（`openclaw infer image providers --agent peipei` 看 Google configured 但金鑰無效，我沒去修金鑰）；巴哈還誤判「lk888 只能吃文字」。
- **解法**：lk888 `/v1/images/edits` 可一次帶多張圖（`image[]`）。腳本 `workspace/scripts/generate_poster_swap.py`（模板＋真人照＋prompt 檔，走 lk888_guard 收費閘門，實測一次成功）。
- **教練規則（10/22）**：只改兩處＝照片、頭銜；獎杯橫版直版一律不動不加字；唯一例外是教練本人那張橫版（單純金杯、立牌「大樹教練／創作者」、底座「乾淨世界」）。其餘模板元素全不動。
- **AI 畫小字常錯**（標誌「中華新媒鱧」、「乾澤世界」、獎座亂字）→ 不重畫（扣額度），用 PIL 貼正確繁中：橫版 `poster_text_overlay_fix.py`、直版 `poster_portrait_logo_fix.py`；補丁用邊緣取色漸層才不露方塊。STHeiti 的「淨」加粗會糊成「浮」，底座字不加粗。座標只適用該張海報。
- **交付給巴哈**：`agents/peipei/SOP_海報換人換字.md`＋`poster_prompts/`（通用橫版／直版 prompt、教練專用橫版 prompt、羅爵模板、教練照片裁切）；SOUL.md 只加一行指標（備份 `workspace/state/backup_SOUL_peipei_20261022.md`）。巴哈是否真的照 SOP 走，教練 10/22 01:18 說要去測、有問題再報。
- 教練說的「講座上的字」＝獎座（獎杯立牌）上的字（語音）。

## 教訓（10/22 07:03 教練問「你是怎麼溝通的？為何巴哈無法執行？」）
- 我只改了巴哈的檔案（SOP、SOUL 指標），**沒有告訴它、也沒驗證它讀到**。查到（transcript）：01:38 教練丟訊息後巴哈 22 秒回覆、**零個工具呼叫**，沒讀 SOP，重複 00:17 那場的舊說法（「Google 金鑰無效」「lk888 只能吃文字」）。原因（推論，未逐項證實）：`startupContext.applyOn=["new"]`，群組對話一直是同一場，改過的 SOUL.md 不會重新載入。
- **做法**：改完分身規則，要對它「正在跑的那場」發話並驗證：`openclaw agent --agent peipei --session-key "agent:peipei:telegram:group:-5115910257" --message-file <檔>`（不加 `--deliver`＝不送進群組，只進該場上下文、回覆印在終端機）。注意：這種命令列回合沒有 exec／終端機工具，只能確認它「聽懂」，不能驗證它「會跑腳本」。
- 10/22 07:3x 已發出更正訊息，巴哈回覆承認兩點說錯、說明收到照片後會跑 `generate_poster_swap.py`（橫 1536x1024／直 1024x1536）。群組內實際跑出圖尚未驗證。
