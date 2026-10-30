---
name: reference-swap-slot-images-after-publish-flow-2026-10-30
description: 個人品牌網頁出圖流程改版：TAVA 只做網頁＋出圖清單（位置寫成 img data-slot=IMG-編號），教練上傳策展中心後說「○○ 已上架，換圖」，我跑 swap_slot_images.py 把小龍蝦出好的圖壓 webp 內嵌換進去、push 上線；林晃誼頁 lin-hunang-yi 為首例
metadata:
  node_type: memory
  type: reference
  originSessionId: 972c1bc8-aa67-4f97-a8bc-39bd61222b6a
  modified: 2026-10-30T05:18:51.670Z
---

教練 10/30 13:12 嫌「下載圖→傳 TAVA→打包→再上傳」太花時間，要我直接從小龍蝦讀圖換進已上架網頁。做法（林晃誼頁 `lin-hunang-yi` 實測通過，網頁 commit `2ecdceb`，線上 curl 驗過 4 張都在、待換圖字卡 0）：

- **腳本**：`workspace/scripts/swap_slot_images.py <短網址> [--dry-run] [--map IMG-003=alt:關鍵字]`（commit `22562ebef`）。來源圖 `~/.openclaw/media/outbound/IMG-00N*.png`（小龍蝦出的圖落在這；保留多久沒查證，換圖時順手備份到 `~/Pictures/<短網址>_AI原圖_<日期>/`）。找位置順序：`<img data-slot="IMG-001">` → 舊版 `div.ill`＋「待換圖 IMG-00N」字卡（整塊換成圖，圖說「AI 繪製示意插畫」）→ `--map` 指定 alt 關鍵字；對到不是剛好 1 個就不換。圖壓長邊 1600、webp 82、base64 內嵌，網頁 5.93→7.23MB。
- **開工指令已改**（playbook `0e5e814`）：完整版、精簡版、製作經驗、交付檢查加「出圖位置寫成 data-slot 編號、不加待換圖字卡、不用等圖傳回」；`ai-go/lk888-inject.html`（`07d6a3c`）加一行「做個人品牌網頁請改走開工指令」。教練只要把開工指令貼給 TAVA。
- **觸發**：反射 `R-SWAP-SLOT-IMAGES-AFTER-PUBLISH`（教練說「已上架…換圖」）。

**注意**：策展網頁常是 5MB 以上單檔含上百張 base64，**絕對不整檔 Read**，只用腳本／搜尋。腳本只負責「換」，圖還是由小龍蝦出（清單裡「實景修飾」類要帶參考照片，`run_img_list.py` 只做概念類，我沒自動化這段）。人像修圖（IMG-003、004）我對照原圖看過人物一致，但沒法保證神似，請教練看一眼主視覺。短網址 `lin-hunang-yi` 拼字是登記時的樣子，沒改。`ai-go` 倉庫的 `index.html` 有別人未提交的修改，我沒碰。

**Why:** 教練不當搬運工、要省時間又省 token；實測人工流程動手約 10～15 分鐘，換圖本身只剩一句話。**How to apply:** 教練說某頁已上架要換圖 → 先 `--dry-run` 看位置、再正式跑 → curl 線上版＋拼一張總覽看過。相關：[[reference_delegate_to_xiaolongxia_openclaw_agent_and_run_img_list_2026-10-30]]、[[feedback_verify_only_changed_element_one_screenshot_2026-10-27]]。
