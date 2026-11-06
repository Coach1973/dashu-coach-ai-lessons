---
name: reference-bymyway-tutor-course-build-via-ajax-htc-video-tunnel-2026-11-06
description: bymyway.com 建 Tutor 課程的做法（編輯器壞了，改用教練登入狀態打 admin-ajax tutor_save_topic／tutor_save_lesson）；高價銷售課程影片走 htcvideo.bymyway.com 通道；課程 27448 現為私人
metadata:
  node_type: memory
  type: reference
  originSessionId: bdeee6a9-0e50-4df3-b787-d19ddb3c8f12
  modified: 2026-11-06T06:54:22.395Z
---

**高價銷售 12 週陪跑課程已建（2026-11-06 14:5x）**：課程 ID 27448，狀態「私人」（只有管理員看得到，沒公開），13 章節、77 堂課（64 支影片＋13 個「本週講義與作業」頁，附件 40 份、作業文字都在裡面）。真瀏覽器實測：課堂頁 `設立基礎`（1080p、22 分）可播，講義附件與作業文字都在。

**Tutor 3.9.15 在這個網站的坑**：wp-admin 的 `create-course` 與前台 `/dashboard/create-course/` 新版編輯器程式沒載入（畫面空白）；`tutor/v1` REST 對 cookie＋nonce 一律 403（要 Tutor API 金鑰）。**能用的是 admin-ajax**（教練在 Chrome 登入後，頁面內 fetch，`_tutor_nonce`＝`_tutorobject._tutor_nonce`，用 urlencoded）：
- 建章節 `tutor_save_topic`：欄位是 `title`＋`course_id`（不是 topic_title／topic_course_id，那組會回「標題必填」）
- 建課堂 `tutor_save_lesson`：`topic_id`、`course_id`、`title`、`description`、`video[source]=external_url`、`video[source_external_url]=<網址>`、`tutor_attachments[]=<媒體 id>`（多個就重複加）。用 `lesson_title` 會建出沒標題的課堂
- 課程本體 `tutor_update_course`：要 `course_id`、`post_author`（教練 WordPress 使用者 ID＝2）、`post_title`、`post_status`、`post_content`
- 刪章節 `tutor_delete_topic`（`topic_id`）**不會連課堂一起刪**，課堂要另外丟垃圾桶：從 `edit.php?post_type=lesson` 列表或編輯頁取 `submitdelete` 連結 GET 一次（跟隨轉址後的 404 是正常的）
- 草稿課程的課堂前台一律 404（Tutor 看課程狀態）；要預覽就把課程改「私人」，之後可改回

**影片通道**：Mac 只讀伺服器 `knowledges/高價銷售課程/htc_video_server.py`（127.0.0.1:5075，只送 ~/amber-Videos 的 mp4、Referer 必須是 bymyway.com、Range 可拖曳）＋ cloudflared 通道 `htc-video` → `htcvideo.bymyway.com`，launchd：`com.coach.htc-video-server`、`com.coach.htc-video-tunnel`。網址代碼對照表 `htc_videos.json`，課程規格 `htc_course_spec.json`。**限制**：Mac 關機、斷網、Amber 沒掛上，影片就播不出來。

**Why:** 教練 11/06 要求高價銷售課程掛在 bymyway.com、不另外付費；大於約 200MB 影片上傳會 500，所以影片不放媒體庫。
**How to apply:** 之後改課程（加章節、換影片、排解鎖）先走這組 ajax；未做：每週自動解鎖（Tutor Pro Content Drip）、作業改成 Tutor 作業題型、結業證書、價格與購買頁、TAVA 首頁、公開前要把影片防護從 Referer 檢查升級。相關：[[reference_bymyway_wp_upload_limit_and_tutor_auth_2026-11-06]]
