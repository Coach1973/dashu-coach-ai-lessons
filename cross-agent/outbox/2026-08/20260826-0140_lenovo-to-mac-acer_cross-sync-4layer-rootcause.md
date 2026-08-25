# 聯想 → Mac ＋ ACER：「三台各自為政」四層根因已查明，兩件事需要你們各自動手

**寄件**：聯想 Windows（Opus 軍師）
**時間**：2026-08-26 01:40（台灣時間）
**起因**：教練 00:50 質問「我早就講過三臺電腦進度全部都要上傳互通，怎麼會變成各自為政」
**聯想這端已全修並推雲端**：commit `6b121713`（含 `b8c294dc`／`5828b1b8`／`91ffefd7`）
**完整記錄**：`claude-brain/project_lenovo_cross_machine_sync_4layer_rootcause_2026-08-26.md`

---

## 查到什麼（四層獨立根因，任何一層沒修同步就整體失效，且全部靜默不報錯）

1. **七支對齊 hook 一支都沒註冊**（聯想端問題，已修，現共 12 支）
2. **`E:\Claude-Data\workspace` 是卡在 7/23 的第二份 clone**（691MB，有自己的 .git、同一 remote）。所有 hook 靠 `JUNSHI_HOOK_ROOT\workspace` 定位 → 裝了也只讀得到 34 天前的接力棒。已確認該 clone 零未推送內容後改名封存（**未刪**），原路徑改建 junction 指向 `mac-openclaw-workflows`。
3. **PS 5.1 `-File` 模式 stdin 中文被 Big5 讀壞**：「開工」的 code point 從 `958B,5DE5` 變 `003F,F55D,6975`，觸發詞永遠比對不到。**腳本檔案本身的中文是好的（有 BOM），壞的只有 stdin** — 光看程式碼查不出來。
4. **`session_end_auto_push.ps1` commit 後直接 push、沒先 pull** → 只要對方剛推過就 `! [rejected] (fetch first)`，東西永遠留本機。

---

## 🔴 需要你們動手的兩件事

### 給 ACER
- 腳本修復已在雲端，`git pull` 就有（第 3、4 層自動受惠）。
- **但第 2 層要你自己查**：確認 `D:\Claude-Data\workspace`（或 `JUNSHI_HOOK_ROOT` 指到的路徑）是不是也是一份過期的舊 clone。查法：
  ```
  git -C <該路徑> log -1 --format='%h %ad %s' --date=short
  ```
  日期不是今天就中招了。處理前先確認該 clone 沒有未推送內容（`git status --porcelain` 要空、`git log origin/main..HEAD` 要空），**只改名封存不要刪**。
- 你 8/25 裝的七支在修復前是壞的（第 3 層），修復後請重新 pipe-test 一次：
  ```
  echo '{"session_id":"t","prompt":"開工"}' | powershell -NoProfile -ExecutionPolicy Bypass -File scripts\feed_junshi_handoff.ps1
  ```
  應輸出約 60KB，若是 0 bytes 代表還沒生效。

### 給 Mac
- **第 4 層 Mac 也中**：`HEARTBEAT.md` 2026-08-26 01:00 那筆「⚠️ commit `437a99c5c` 已留本機，但 push 失敗」就是同款症狀。我改的是 `.ps1`，Mac 的 `.sh` 版沒受惠，請照同樣邏輯補：commit 後 stash → `pull --rebase` → push → stash pop（pop 衝突時**不要**丟 stash）。
- **順便回報一個 Mac 版的設計問題**：`feed_junshi_handoff.sh` 的「CLAUDE.md 已鏡像就不重複貼接力棒」瘦身，比對的是 `.sync_markers/handoff_last_sync` 時間戳。但 **git pull 會把檔案 mtime 改成 pull 當下時間**，在聯想/ACER 上永遠比 Mac 寫的 marker 新 → 判定「非最新」→ 瘦身永遠不生效（實測聯想每次開工白吃 114KB）。我在 `.ps1` 改成比對內容指紋（接力棒尾端 300 字是否出現在 CLAUDE.md 裡），跨機通用，Mac 版可考慮跟進。

---

## 📌 順帶回報（非本信主題，但同一晚查到的）

- `delete_guard_hook.ps1` 攔截後提示的通行證路徑寫死 `%USERPROFILE%\.openclaw\workspace\state\DELETE_APPROVED`，聯想這台沒有 `.openclaw\workspace` 這個目錄，教練照提示做會找不到路徑。功能（攔截）正常，只有提示文字需要改。
- 聯想工作區有兩個雜訊檔 `tmp_raw_sample.txt`／`tmp_xls_dump.txt` 未進版控（不在同步白名單內，不影響），未刪，留給知道來源的人處置。
