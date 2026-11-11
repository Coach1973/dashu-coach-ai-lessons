---
name: project-go-portal-dashu-entry
description: 大樹入口 event.bymyway.com/curated/go/ ＝教練唯一總入口（六大系列＋最常用＋全搜尋）；改分類改 build_go_portal.py；線上驗證用 playwright 無頭 Chrome
metadata:
  node_type: memory
  type: project
  originSessionId: 0e530d37-7b2a-413e-b09b-ce6d5eb2483a
  modified: 2026-11-11T02:21:52.576Z
---

2026-11-11 教練交辦「只開一個頁面就知道點哪個」→ 上線 https://event.bymyway.com/curated/go/ （倉庫 ~/github_repos/go 私有；改了 push 就上線）。

- 分類邏輯（反推結果）：教練原本三把尺混用（哪個計劃／做什麼用／什麼時候），新入口只用「六大系列」：團隊計劃（含網頁一鍵導入、生圖一鍵注入、反向技能書 14 招示範）、漫畫（與團隊同脈絡）、榮樹下、BNI、賈維斯對話檢討、大樹常用・里程碑。
- 改分類／加項目：改 `workspace/scripts/build_go_portal.py` 的 SERIES，跑 `python3 scripts/build_go_portal.py ~/github_repos/go`，到倉庫 commit＋push。新 Claude 報告要進時間軸 → 補 `scripts/go_portal_artifacts.json`。
- 最常用＝Chrome 近 75 天開過天數×2＋點擊次數；本頁點擊記在 /api/coach888/click 前綴 go::。
- 「14 個特效」＝ event.bymyway.com/curated/rs-demo/（反向技能書 14 招示範）。

**Why:** 教練作品多到找不到，作品集 75 天開 29 天但常用只約 40 頁。
**How to apply:** 教練說「入口」「go 那頁」「總入口」就是這頁；內建瀏覽器不准開外部網址，線上驗證用 workspace/scripts/node_modules/playwright-core＋Google Chrome 無頭跑。相關 [[reference_works_map_page_and_sticky_header_preflight_2026-11-09]]
