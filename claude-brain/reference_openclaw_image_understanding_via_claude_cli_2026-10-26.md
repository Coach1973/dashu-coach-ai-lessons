---
name: reference-openclaw-image-understanding-via-claude-cli-2026-10-26
description: 巴哈等小龍蝦分身收到圖片一直卡住的根因（MiniMax 看圖 2056／回空白）與改法：tools.media 的 CLI 看圖交給 Claude；用量、上限、怎麼驗證、怎麼調
metadata:
  node_type: memory
  type: reference
  originSessionId: 36eddc83-dbc1-4766-a862-fef378a60de5
  modified: 2026-10-25T17:51:21.944Z
---

**症狀**：巴哈（peipei）群組有人傳圖就不動；日誌出現 `image: failed (0/1) reason=MiniMax VLM API error (2056)` 或 `MiniMax VLM returned no content`。10/25～10/26 兩天 18 次全失敗、日誌沒看到成功。

**根因**：MiniMax-M3 在 openclaw.json 只收文字（`input:["text"]`），圖片固定走另一條 MiniMax 看圖 API（plugin `MiniMax-VL-01`）。它失敗（額度碼 2056 十次、空白八次）後，巴哈沒有放手而是卡在重試，後面的訊息一起被擋（看門員 10/26 01:33 才偵測到）。

**改法（教練 10/26 01:45 核可）**：openclaw.json `tools.media.image.preferredModel = "cli:/Users/bymyway/.openclaw/workspace/scripts/describe_image_via_claude.py"`＋`tools.media.models` 加一筆 type=cli、capabilities=["image"]、args `{{AttachmentPath}} {{MaxChars}}`。腳本呼叫 `claude -p`（claude-sonnet-5-5，只開 Read 工具、空資料夾、不載入設定與 hook），**任何失敗都印一句固定中文並結束碼 0**，小龍蝦就不會判失敗、不會卡。每小時上限 40（`HOURLY_CAP`），用量記在 `workspace/state/image_describe_log.jsonl`。實測一張 3MB 圖：10 秒、約 1 萬輸入＋450 輸出、0.023 美元。花 Claude 方案額度，不花 MiniMax、不動 LK888 出圖。commit workspace `6117f85c0`、outer `06c2a0151`。

**How to apply**：巴哈又說看不到圖→先看 `image_describe_log.jsonl` 最後幾筆的 `why`（timeout／hourly_cap／empty_or_error）；Claude 額度吃緊（10/26 教練 5 小時 83%、本週 84%）就調低 HOURLY_CAP。設定可熱重載，不用重啟。`openclaw infer image describe` 不會走這條 CLI，不能拿來測；要測就真的傳圖給 @coachwu_lenovo_bot。整條路 10/26 還沒用真實訊息驗證。

相關：[[reference-peipei-group-context-overflow-blocks-main-lane]]、[[feedback-bot-instructions-must-block-old-path-and-measure-tokens-2026-10-25]]
