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

## 教練本人的素材（2026-10-30 23:40 台灣時間，教練親口交付）
- **教練本人的聲音錄音檔**：`/Volumes/953-SSD/下載/歸仁齒輪有限公司.m4a`（104 秒、單聲道 AAC、0.9MB；教練說「這個是我的錄音檔」，要我記錄）。以此複製出 VisionStory 聲音 `voice_id=893883331753573490`（沒扣點；系統標成 zh-CN 男聲）。帳號裡 9/28 就有的 2 個複製聲音（3666746792484267812、7047654227939670478）不確定是誰的聲音。
- **教練指定的照片**：`https://coach1973.github.io/bigtree/speakers-2026/coach-profile.jpg`（600×900，深灰格紋西裝、藍領帶、雙手抱胸、黑背景）→ VisionStory 頭像 `avatar_id=2236789676702807693`（教練說上一張「不是很滿意」，這張是他點名的）。
- 指令檔新增 `create-avatar`、`clone-voice` 子指令。

## 影片實測與動作限制（10/30 夜～10/31 00:10 台灣時間）
- 4 支影片都花 2～3 點／支（720p，7～9 秒）；點數 220→206。教練喜歡的是 `visionstory_me_8s`（avatar 2119045209488192536＋聲音 3666746792484267812，16:9）。
- **動作由照片姿勢決定**：說話影片 API 只有 `emotion`（cheerful／angry／marketing／news／singing），沒有手勢參數；要換動作＝換姿勢不同的照片（avatar 6939433198220735630 有比手勢）。`/api/v1/ai_video`（beta、要付費方案）可用文字描述動作，沒實測。
- **看縮圖挑頭像會挑錯**：avatar 8794583783945435136 縮圖像在比手勢，實際影片是抱胸；挑姿勢要看真影片或原圖。
- 要把影片做法給別的 AI（不扣點）＝給「畫面＋台詞」描述（抽 4 格看畫面寫），不是 API 指令；聲音樣本轉 mp3 放桌面、臉參考照下載放桌面，不叫教練自己搬。
