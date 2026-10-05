---
name: reference-lenovo-zoom-recordings-junction-to-d-2026-10-06
description: 聯想 Zoom 本機錄影位置：原路徑是 junction 指向 D:\Zoom，實際檔案在 D 槽；舊夾 Zoom.bak.20261006 待教練自己刪。教練問「Zoom 錄影在哪」或 C 槽空間時讀這篇
metadata:
  node_type: memory
  type: reference
  originSessionId: 2654e25c-37e5-4fd3-b1c8-0db4eb14b573
  modified: 2026-10-05T18:46:03.233Z
---

聯想（Windows）Zoom 本機錄影，Zoom 設定裡「儲存位置」仍是 `C:\Users\bymyw\OneDrive\Documents\Zoom`（Zoom 預設，每場一個資料夾，名稱＝錄影開始時間＋會議名稱，裡面有 `audio<會議號>.m4a`、`video<會議號>.mp4`、聊天文字檔），但 **2026-10-06 02:35 起這個路徑是 junction（目錄捷徑），實際檔案在 `D:\Zoom`**。以後錄的影音自動落在 D 槽，不用改 Zoom 設定、Zoom 更新也不會破壞。

- 搬移紀錄：36 個資料夾／71 檔／約 3.9 GB，robocopy 複製後逐檔 SHA-256 全部一致；經捷徑寫測試檔確實落在 D 槽。
- 舊資料夾曾改名 `Zoom.bak.20261006`（3.9 GB），**教練 10/06 02:45 已自己刪掉**（>1 GB 我不能自主刪）；刪後我查證 `D:\Zoom` 仍是 36 夾／71 檔、捷徑完好，C 槽剩 206 GB。已無待辦。
- C 槽其他位置（`C:\Users\bymyw` 排除 AppData、Public、ProgramData）沒有別的 Zoom 錄影，也沒有 ≥50 MB 的影音檔。
- 這裡的 `C:\Users\bymyw\OneDrive` 不是現行 OneDrive 同步根目錄（現行是 `D:\Users\Downloads\OneDrive`），所以這包從沒被雲端同步，搬動不影響雲端。
- D 槽另有 `D:\Users\Downloads\ZOOM`（雲端錄影下載的 `GMT*_Recording` 系列，另一批、本來就在 D）。
- 還原方法：刪掉 junction `Zoom`（用 `rmdir`，不是遞迴刪除）、把 `Zoom.bak.20261006` 改回 `Zoom`。

**Why:** 教練 10/06 02:25 問「以後錄音檔位置全部移到 D、C 槽還有多少類似檔案也移過去」。
**How to apply:** 教練問 Zoom 錄影在哪／找某個 audio 檔，先找 `D:\Zoom`（或原路徑）；不要把 junction 當成普通資料夾去 `Remove-Item -Recurse`（會連 D 槽內容一起刪，走 `scripts\delete_guard.ps1`）。相關：[[reference_lenovo_system_image_backups_2026-10-03]]、[[feedback_data_move_du_sh_verify]]。
