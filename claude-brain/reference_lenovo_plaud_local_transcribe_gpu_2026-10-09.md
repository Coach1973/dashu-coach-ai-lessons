---
name: reference-lenovo-plaud-local-transcribe-gpu-2026-10-09
description: 聯想(Windows)本機轉錄 Plaud 錄音的做法：D:\Plaud轉錄工具（faster-whisper large-v3-turbo＋RTX 3050 Ti，約12倍即時）；Plaud MCP 不能觸發轉錄、轉錄扣點，所以教練要我自己轉；Plaud 原始 .opus 是無檔頭的 80 位元組封包要先包成 ogg
metadata:
  type: reference
---

**教練 2026-10-09 糾正**：「逐字稿是你的任務，因為讓它轉是要扣點數的」「軍師有寫 Plaud 技能，沒理由你不會，去雲端找」。我一開始只回「Plaud 還沒轉、要不要裝工具」，是失職——該先去找軍師已寫好的做法再動手。

**哪裡找**：雲端 repo `mac-openclaw-workflows`：`cloud_sync/skills/plaud-*/SKILL.md`（read/find/browse/digest/export/followup/shared，只能讀）＋`claude-brain/reference_plaud_backup_and_local_transcribe_2026-10-08.md`（Mac 版：下載音檔→本機 mlx-whisper→OpenCC s2twp→「B&I」改 BNI）。本機 clone 若有衝突檔（UU）不要 pull，用 `git fetch` ＋ `git show origin/main:路徑` 唯讀。

**聯想做法（已實測，92 分鐘只要 6.7 分鐘）**
- 工具在 `D:\Plaud轉錄工具\`：`venv`（faster-whisper、nvidia-cublas/cudnn-cu12、opencc）、`hf_cache`（模型 1.6GB）、`transcribe.py`（短檔）、`transcribe_chunked.py`（長檔，10 分鐘一段）、`raw_opus_to_ogg.py`。輸出放 `E:\Claude-Data\Plaud逐字稿\`（txt，UTF-8 帶 BOM，每行 `[HH:MM:SS]`）。
- 流程：`get_file` 取 presigned 連結 → `curl` GET 下載（不吃 HEAD）→ 轉錄。
- 坑 1：`av` 要 `<17`（19 版 faster-whisper 讀音檔報 `metadata_errors`）。
- 坑 2：Plaud 的 `oc_au_*.opus` 沒有 Ogg 檔頭，是固定 80 位元組的 Opus 封包（32kbps、20ms，檔案大小÷80×0.02＝錄音秒數可驗證），要用 `raw_opus_to_ogg.py` 包成 ogg 才讀得了；`oc_at_*.mp3` 可直接轉。
- 坑 3：整段 90 分鐘一次轉會 `Unable to allocate 1.54 GiB`——分頁檔被固定 4GB、瀏覽器吃掉記憶體，可用上限一度只剩 7GB；改 10 分鐘一段（交界處字可能被切）。
- Plaud MCP 沒有觸發轉錄的工具；讀沒轉過的錄音只回空陣列。
- 不會分辨說話者；專有名詞會有同音字誤差。
