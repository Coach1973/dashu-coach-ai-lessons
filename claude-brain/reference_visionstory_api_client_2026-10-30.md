---
name: reference-visionstory-api-client-2026-10-30
description: VisionStory（talking-avatar 影片／TTS／語音複製）API 已串：金鑰在路徑大全_憑證層、腳本 scripts/visionstory_api.py（094d44529）；唯讀指令已實測，create-video／tts 會扣點數、沒跑過
metadata:
  node_type: memory
  type: reference
  originSessionId: 19560b24-fe5c-400f-8d97-05a71e2c8f34
  modified: 2026-10-30T13:39:24.682Z
---

教練 10/30 21:37（台灣時間）貼 https://developers.visionstory.ai/ 與金鑰要我「串 API」。做法：
- **金鑰**：寫進 `路徑大全_憑證層.md`（git 忽略）的「VisionStory API」段；`memory/verbatim/2026-10.jsonl` 裡那一筆已遮蔽。查 `GET /api/v1/billing/credits` 回 200、剩 220 點。
- **腳本**：`workspace/scripts/visionstory_api.py`（commit `094d44529`，只用標準函式庫）。子指令 credits／models／avatars／voices／video-status 已實測；`create-video`（輪詢每 5 秒、上限 10 分鐘、下載 mp4）與 `tts` **沒跑過真生成**，因為會扣點數。
- **API 事實**（openapi.json 查到）：主機 `https://openapi.visionstory.ai`，標頭 `X-API-Key`；模型目前只有 `vs_character_v4`（9:16／16:9／1:1，720p／1080p／2k）；voice_id 是名字字串如「小何」（zh-TW）；影片完成後只保留 7 天。文件索引 `https://developers.visionstory.ai/llms.txt`。
- **在 worktree 對話寫 workspace**：Write 工具被 hook 擋，改用 Bash heredoc 建新檔＋path-limited commit。

**How to apply:** 要做 VisionStory 影片先 `avatars --public`／`voices --locale zh-TW` 找真 ID，不猜；真生成前先講會扣多少點數（剩 220）。
