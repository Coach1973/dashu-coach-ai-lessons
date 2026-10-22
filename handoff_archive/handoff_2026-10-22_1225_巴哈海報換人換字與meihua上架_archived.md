## 🔴 給跨對話框軍師讀的總結摘要（2026-10-22 12:25 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Sonnet 5.5；教練說「總結」；本段 10/22 00:28～12:25，對話容量約 29%）

**主軸：巴哈助理海報「換人換字」卡關解決＋寫成規則；TAVA 李美花頁打包並上架 meihua。**
- **巴哈出不了圖的根因**：內建 `image_generate` 走 Google，金鑰無效（HTTP 400，沒修）；巴哈還誤判「lk888 只能吃文字」。lk888 `/v1/images/edits` 可一次帶多張圖 → 新腳本 `scripts/generate_poster_swap.py`（commit `a0cf115de`），橫版／直版海報實測成功。成品在 `claude-brain/data/poster_bigtree_coach_v3_20261022.png`（橫）、`..._portrait_v1_20261022.png`（直）。
- **AI 畫小字常錯**（標誌、獎座、底座「乾淨世界」）→ 不重畫，用 PIL 貼字：`poster_text_overlay_fix.py`（橫）、`poster_portrait_logo_fix.py`（直）；座標只適用該張海報。
- **教練規則**：只改照片＋頭銜；右邊獎杯橫直版都不動、不加字；只有教練本人那張橫版寫「乾淨世界」。已寫進巴哈 `agents/peipei/SOP_海報換人換字.md`＋`poster_prompts/`（巴哈倉庫 `a002732`、`d8fecae`）。
- **我的溝通漏洞（教練 07:03 質問）**：只改檔案沒告訴巴哈也沒驗證；巴哈 01:38 零工具呼叫、重複舊說法。查到原因推論為 `applyOn=["new"]`，對話延續時新規則不載入。補救：`openclaw agent --agent peipei --session-key ... --message-file`（不加 `--deliver`）對它那場對話發更正，巴哈承認兩點錯誤。教訓已進記憶 `reference_poster_swap_lk888_two_images_bahai_sop_2026-10-22.md`。
- **李美花 meihua 上架**：教練給 TAVA 網址，我打包成單檔 zip 並走策展 SOP（`kind=shop`）。系統處理成功、線上 200、GitHub `Coach1973/meihua`；自動分類猜成「衣」（因「生技」），改為「食」並補地址（`bbed5eb`、`b720e7015`），線上商圈頁已確認。
- **教練原話線索**：「你是怎麼溝通的？為何巴哈無法執行任務？」→ 他在意的是我有沒有「真的把事情送到對方並確認」，不是我寫了什麼檔。

### 📋 下一場開工先做（以本棒為準）
1. 巴哈海報實測：教練去群組測；看 peipei 原始紀錄確認它真的跑了 `generate_poster_swap.py`、獎杯沒被動（群組內出圖尚未驗證）。
2. meihua 是否進「大樹作品一覽」：名冊標 in_works，但作品一覽頁沒搜到，尚未確認。
   ✅ **推播許可旗標漏洞已修（10/22 台灣時間 12:34，workspace `c28f26cd6`、outer `c34679888`）**：旗標檔改寫「內容＝時間戳」，閘門只看內容不看修改時間；許可用 `scripts/line_push_approve.sh`、作廢 `--revoke`（`touch` 不再有效）。三個閘門（LINE 外掛 JS／`send_line_push.py`／event-signup）都改了，gateway 與 event-webapp 已重啟；實測：運作中 gateway 對假目標推播＝403 擋下，「舊內容＋新修改時間」的殘檔（就是 10/20 漏洞）也擋。外掛更新洗掉閘門時，每日點名會把舊 V1 自動升級成 V2。

🙋 要教練決定：無新增。
🤫 等教練自己提起：公開倉庫是否放守則全文（沿用）。
🔧 AI 自己的清單：①`curation_process.py` 的 `CATEGORY_KEYWORDS` 把「生技」歸到「衣」（內建 image_generate 的 Google 金鑰無效也沒修，其他分身同樣會失敗）；②改任何分身規則後，要對它「正在跑的那場」發話並驗證；③本場記憶只新增 1 檔。
