---
name: reference-plaud-backup-and-local-transcribe-2026-10-08
description: 教練 Plaud 錄音 175 筆（約95小時）已全數下載到 SSD 並用本機 mlx-whisper 轉繁中；Plaud MCP 只讀不能刪；怎麼續跑、怎麼查進度、刪雲端前要驗什麼
metadata:
  type: reference
---

**位置（全在外接 SSD，不佔本機）**：`/Volumes/953-SSD/Plaud錄音備份/`
- `audio/` 175 筆音檔（mp3 146／ogg 28／m4a 1，共約 1.8 GB）；`plaud_text/` 每筆 Plaud 自己的逐字稿＋AI 筆記 json（101 筆有）；`local_text/` 本機轉錄結果（.txt 純文字＋.json 時間軸）；`驗證報告.csv` 每筆雲端 vs 本機長度比對（174 通過，1 筆是 Plaud 教學範例差 7 秒）；`清單_雲端原始.json`；`tools/` 腳本＋venv＋HF 模型快取＋pip 快取；`logs/`。
- 腳本：`tools/plaud_download.py`（可續跑，`.done` 標記）、`tools/plaud_transcribe.py`（可續跑，結果已存在就跳過；未命名的先轉）。續跑：`cd tools && TMPDIR=../tmp HF_HOME=./hf_cache ./venv/bin/python plaud_transcribe.py`。進度看 `logs/transcribe.log`。
- 模型 mlx-community/whisper-large-v3-turbo，實測約 9.6x 即時；全部約 9~10 小時。簡轉繁用 OpenCC s2twp，並把「B&I」修成 BNI。

**Plaud MCP 的事實（2026-10-08 查證）**：只有 login／logout／get_current_user／list_files／get_file／get_note／get_transcript，**沒有刪除**；刪雲端要教練自己在 Plaud App／網頁做。讀取從沒轉寫過的錄音只回空陣列、不觸發轉寫（不扣 300 分鐘額度）。claude.ai 網頁連接器已加（`claude.ai Plaud`），本機版 `plaud` 也在；這場之後的新對話才載得到工具，舊對話用 stdio 直接呼叫 `npx -y @plaud-ai/mcp@latest`（JSON-RPC，取得的是 UTC 時間，+8 才是台灣時間）。
**坑**：presigned 網址不吃 HEAD（403），要 GET；解析回應用 `<untrusted-user-data-ID>…</…>` 的 regex，不能用 `">\n"` 切（逐字稿內容會含）；本機 Muse.app 是 Meta 的 App，無可呼叫的語音模型。
**刪雲端前必做**：對照表全數驗證通過＋再備份第二份（刪了就只剩本機一份）；不到 1 分鐘的 7 筆裡 2 筆有正式名稱（會議記錄46秒、台北科大億光大樓55秒）要教練確認。

相關：[[reference_mac_downloads_on_external_ssd_2026-10-02]]
