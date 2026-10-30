---
name: project-nmda-members-page-and-staff-login-2026-10-30
description: NMDA 網站「會員資料」頁（會員自建檔案、10 種連結）＋工作人員帳密登入後台；LK888 圖片壓縮規格（長邊1000／webp q72）寫進腳本與一鍵注入
metadata:
  node_type: memory
  type: project
  originSessionId: 25515434-820c-4230-9b83-579b2a619219
  modified: 2026-10-30T07:36:26.189Z
---

教練 10/30 交辦：NMDA（https://event.bymyway.com/curated/nmda/）首頁加「會員資料」入口，會員自己建立檔案；後台要交給協會工作人員，給帳密登入頁與專用網址。

**做法**：照 [[project-nmda-board-team-page-2026-10-23]] 複製。`workspace/event-signup/nmda_members.py`（資料表 nmda_members、10 種連結照 mentor100 加領英）＋app.py `/nmda/members/*`；公開頁 `github_repos/nmda/members.html` 讀 `/api/nmda/members/board`。不做空座位、建置模式。測試 `venv/bin/python test_nmda_members.py`（36 項）。改完要 `launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp`。
**後台兩條路**：教練的簽章短址 `/nmda/members/a/<12字>`；工作人員 `https://event.bymyway.com/nmda/members/login`（帳號 admin，密碼只存雜湊在 nmda_members.py、明文在 /vault 憑證總覽；連錯 5 次鎖 10 分；session 鍵 nmda_members_admin，進不了 /admin）。五個網址已收進大樹作品集。
**LK888 壓縮**：`swap_slot_images.py` 預設長邊 1000／q72（約 80～110KB，原約 250KB）；`run_img_list.py` 出圖當下另存 `.web.webp`；`ai-go/lk888-prompt.md`、`lk888-inject.html`、`tava-brand-web-playbook` 都寫進同規格。
**坑**：在「開工」worktree 對話裡 Edit 改 ~/.openclaw/** 會被 hook 擋；教練 10/30 明說「不要再問、做完就好」→ 直接用終端機補丁（改前備份到 workspace/state/backup_*、path-limited commit），不要再問教練 worktree／主目錄（他聽不懂、會火大）。認圖先對人名：林晃誼（女）、吳尚謙（男）。

**Why:** 下次教練說「協會要加某某資料頁／後台交給別人」，直接複製這套；登入密碼好猜只靠鎖次數，教練決定換時再改。
**How to apply:** 相關：[[reference-worktree-session-edit-hook-blocks-openclaw-2026-10-15]]、[[feedback-new-admin-urls-auto-register-coach888-2026-10-10]]
