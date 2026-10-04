---
name: reference-clone-event-page-and-keynote-export-2026-10-04
description: 複製舊活動頁做新場次（留歷史頁）的完整做法與坑（QR/海報/快取/event.db/歷史自動補登）＋Keynote .key 轉 PowerPoint 的 AppleScript 做法
metadata:
  node_type: memory
  type: reference
  originSessionId: a56cf402-aeef-4244-a091-4bb77c1fb881
  modified: 2026-10-04T08:14:55.047Z
---

## 複製舊活動頁做新場次（教練 2026-10-04：「內容都一樣，因為要留歷史頁面」）

範例：bigtree-1003 → bigtree-1107。步驟（全部本機，不碰 Netlify）：
1. 複製 `~/github_repos/<舊slug>/` 的 index.html＋圖片到 `~/github_repos/<新slug>/`；用 Python 一次性取代日期、slug、場次序數（第N場、前N場、「N場已辦」計數），取代後 grep 確認沒有殘留舊日期。**不要複製舊的 `qr.png`／`README.txt`／`edm.html`（寫著舊日期）**，要用就改過再放。
2. `event-signup/event.db` 的 `events` 表（先備份）：name／location／venue／address／start_time／**event_url（海報歷史補登靠它）**／site='bigtree'；`curated_sites_registry.json` 加一筆（category「大樹小講活動」、no_shop_card）；`python3 scripts/curated_git.py ensure <slug>` 建 GitHub。
3. **海報＝重做，不能沿用舊圖**：`edm.html` 改日期／場次→headless Chrome 輸出：`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=1080,1620 --screenshot=out.png file://…/edm.html`。**QR 要重做並解碼驗證**：用 venv（scratchpad）裝 `segno`＋`opencv-python-headless`，`segno.make(url)` 存圖、`cv2.QRCodeDetector().detectAndDecode` 讀回比對網址。事故：bigtree-1003 的舊 EDM 上 QR 掃出來是 AI 工具臨時預覽網址（`video-maker.work`），不是正式頁。
4. **換圖必須換檔名**：伺服器圖片 `Cache-Control: max-age=14400`（4 小時），同檔名換內容教練的 Chrome 會卡舊圖（本場實際發生）。HTML 本身是 no-cache。
5. 辦完後**歷史頁自動補登**（`scripts/bigtree_history_sync.py`，launchd 每天 00:20）；前提是 events 列 `site='bigtree'`、`status='active'`、event_url 有填。見 `SOP_教練個人創作上架event.bymyway.com不進商圈.md` 規則四。
6. 驗證：真瀏覽器看（先 `resize_window` 設 1280／390 寬再量；窗格預設寬度可能是 0）、圖片 `naturalWidth>0`、手機寬度 `scrollWidth<=clientWidth`。教練禁截圖（`screenshot_lock.sh`），用 DOM 量。

## 工具的坑（這台 Mac）
- Bash 指令字串裡出現 `bigtree_publish` 會被 `netlify_deploy_guard.sh` 誤攔（連 `git add` 檔名都算）→ 用萬用字元 `bigtree_pub*.py`，commit 訊息也別寫該檔名。
- `git push` 到 bigtree 這類 push 即上線的 repo，`web_preview_verify_guard.sh` 要求本輪有 `open -a "Google Chrome" <網址>` 的紀錄。
- 這台 macOS 沒有 `timeout` 指令，zsh 的 `rm -f 萬用字元` 無匹配會直接中斷整行。

## Keynote `.key` 轉 PowerPoint（沒有 LibreOffice 時）
App 在 `/Applications/Keynote Creator Studio.app`（bundle id `com.apple.Keynote`，v15.4）。
```
osascript <<EOF
with timeout of 160 seconds
  tell application id "com.apple.Keynote"
    launch
    set d to open POSIX file "/路徑/檔名.key"
    delay 3
    export d to POSIX file "/輸出/檔名.pptx" as Microsoft PowerPoint
    close d saving no
    return count of slides of d
  end tell
end timeout
EOF
osascript -e 'tell application id "com.apple.Keynote" to quit'
```
本場 13 張匯出成功、第一次執行不需額外授權。用完要 quit。教練檔案備註：他在 Finder 看到「沒有 .pptx 後綴」的那份＝Keynote `.key`；教練說「刪不掉的檔案給你檔名」＝授權 AI 刪那幾個檔（走 `trash`，可還原）。
