---
name: reference_mac_downloads_on_external_ssd_2026-10-02
description: Mac「下載」改放外接SSD：~/Downloads 是捷徑指向 /Volumes/953-SSD/下載；舊資料夾 ~/Downloads.bak.20261002 保留到 10/09；本機瘦身已刪項目清單
metadata:
  type: reference
---
2026-10-02 教練要「本機只留重要的，會長大的資料放外接 SSD」（比照聯想 Chrome→E槽）。

- `~/Downloads` → 捷徑指向 `/Volumes/953-SSD/下載`（APFS、USB、disksleep=0）。搬前 658 檔、內容差異 0。要先 `chmod -a "group:everyone deny delete" ~/Downloads` 才能改名（macOS 預設鎖）。
- 舊資料夾 `~/Downloads.bak.20261002`（1.1GB）保留 7 天，**10/09 後**確認無異狀再刪（比照 LINE 搬家鐵律）。
- SSD 沒接上＝下載失敗；每日點名已加「外接SSD」檢查（daily_team_rollcall.py）。
- 已刪（教練當場同意）：Claude-3p 舊資料 10GB（SSD 有份 `Mac本機搬移_20261002/`）、ByeType 4.6GB、whisper large/medium 3GB、uv/puppeteer/opencode 快取 4GB、9/19 工作資料夾舊備份 6.7GB（SSD 有份）。
- **不能刪**：`~/.cache/whisper/base.pt`（小龍蝦 Telegram 語音轉文字 `openclaw.json tools.media` 用 base）、`~/.cache/huggingface`（名片 OCR PaddleOCR＋記憶搜尋 bge-m3）。
- 刪完空間不會馬上變多：時光機本機快照(約27份)還留著，約一天內到期才釋放。

待做：Chrome 資料搬 SSD（要關 Chrome）、26.7.1 系統更新（教練定時段）。相關：[[project_mac_backup_policy_good_state_and_pre_upgrade_2026-10-02]]

**13:37 追加：Chrome 資料也搬了**：`~/Library/Application Support/Google/Chrome` → 捷徑指向 `/Volumes/953-SSD/Mac應用資料/Chrome`（8671 檔、內容差異 0，重開 Chrome 後新寫入的檔案出現在 SSD 那份）。舊夾 `Chrome.bak.20261002`（5.2GB）保留到 **10/09** 後刪。SSD 沒接上 Chrome 會打不開。

**10/16 追加（教練當場糾正「圖明明在下載資料夾你怎麼找不到」）**：`~/Downloads` 是捷徑，`ls -lt ~/Downloads` 和 `find ~/Downloads`（沒加 -L）只會看到捷徑本身、當成空的。找檔一律用 `ls -lt ~/Downloads/`（結尾斜線）或 `find -L ~/Downloads/`，或直接 `/Volumes/953-SSD/下載/`。源頭已修：`knowledges/反射索引.json` 的「下載資料夾」反射原本寫「ls ~/Downloads」，現在寫明捷徑與斜線（情境目錄由腳本重產）。
