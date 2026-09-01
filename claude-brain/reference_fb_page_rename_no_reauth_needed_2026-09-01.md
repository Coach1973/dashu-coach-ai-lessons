---
name: reference_fb_page_rename_no_reauth_needed_2026-09-01
description: FB粉專改名字/大頭貼/簡介不影響Page ID跟已核發的Page Access Token，不用重新授權；只有新建全新粉專才需要重跑/me/accounts
metadata: 
  node_type: memory
  type: reference
  originSessionId: 529f493d-3a80-43be-815c-8e4a5987a014
  modified: 2026-09-01T08:52:46.127Z
---

Facebook的Page ID是永久不變的識別碼，粉專顯示名稱只是標籤。教練之後改任何一個粉專的名字、大頭貼、簡介，都不會動到`fb_automation/page_tokens_2026-09-01.json`裡記錄的Page ID或access_token，權杖照樣有效，不需要重新走一次Graph API Explorer的「Generate Access Token」授權流程。

唯一需要處理的情況：**教練新建一個全新的粉專**——因為`pages_show_list`權限本來就是「授權App讀取教練所有粉專清單」，新粉專會自動被涵蓋在內，只要重新呼叫一次`/me/accounts`就能抓到新粉專的token，不需要教練再手動點一次「Generate Access Token」。

Related: [[project_fb_fanpage_marketing_automation_2026-08-27]]（若已建立）、`路徑大全_憑證層.md`「FB Graph API」章節（2026-09-01已更新為14個粉專完全打通版本）
