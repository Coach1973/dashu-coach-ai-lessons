# 「首批足跡夥伴」區塊產生器（2026-10-16，教練交辦）

把各人專屬頁（~/github_repos/<slug>/index.html）裡的「公益足跡」逐字擷取，做成真公益俱樂部頁（~/github_repos/social-club）的「首批足跡夥伴」區塊。

- `extract_fp.py`：抽文字（數字、足跡時間軸、出處連結）與主圖；`person(...)` 新增一位＝加一行＋一個抽取函式。圖存到 social-club/assets/people/。
- `render_fp.py`：產生區塊 HTML/CSS 並可重複執行地放進 social-club/index.html（用 `PEERS-START/END` 標記；環境變數 `SC_BASE` 指定要改哪一份，先改預覽副本、驗過再覆蓋正式資料夾）。
- `patch_footers.py`：五位個人頁頁尾補「招募志工團隊／真公益／真公益・企業家俱樂部」（與 social-good 頁尾一致）。
- `serve.py`：本機預覽（`python3 serve.py <預覽根目錄> 8123`，/curated/<slug>/ 對應資料夾，/static/ 讀 static_dl/）。

注意：頂部選單每加一項，要先量寬度（20px 字）；這次加「足跡夥伴」後漢堡選單門檻從 1180 提到 1260（CSS 與 nav-burger 的 data-bp 兩處一起改）。
