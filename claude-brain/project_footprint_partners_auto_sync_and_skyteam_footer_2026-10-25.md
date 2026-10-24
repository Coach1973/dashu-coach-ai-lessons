---
name: project-footprint-partners-auto-sync-and-skyteam-footer
description: 有公益足跡的網頁自動進真公益「足跡夥伴」（sync_peers.py，上架後自動跑）；顧問師天團頁尾第 4 個連結已補 40 頁；軍火庫前 32 位
metadata:
  type: project
---

**教練 2026-10-25 交辦**：①凡在顧問師天團、有我們製作個人品牌網頁的，頁尾一律多第 4 個連結「顧問師天團・人才軍火庫」（https://event.bymyway.com/curated/skyteam/），已補 40 頁（37 頁 commit 在各自倉庫、Sunny/Lior/Allen 先補）；TAVA 開工指令（tava-brand-web-playbook `8debecf`）固定頁尾也改四個。②有公益足跡（≥3 則）的網頁一律進 https://event.bymyway.com/curated/social-club/#peers ，並寫進自動化。

**做法**：`workspace/scripts/peers_footprints/`（`970815b46`、`e91b6d2f9`）：`fp_generic.py` 通用抽取（找「公益，是有足跡的。」區塊，不靠 class 名稱，找有年份、重複 ≥3 個的兄弟區塊）、`sync_peers.py <slug>|--scan|--force`、`fp_data.json`（名單資料，原六位在前）、`render_fp.py` 資料驅動；上架處理完 `curation_process.py` 會自動跑並 Telegram 通知；人名頭銜不對在 `sync_peers.py` 的 `OVERRIDE` 加一行。social-club `ff89798` 現有 23 位（22 卡＋吳錦昌）。

**抽不出來要人工（同一頁只通知一次）**：meihua（`ol.vline` 的 `<b>年份｜標題</b>` 格式）、8ccafe（足跡由 JS 的 charityList 產生）、hello-brand（找不到主圖）、wang-xiali（只有 2 則有年份）。排除：coachwu（＝social-good 那張）、111-wei（競選足跡）。

**軍火庫**：skyteam `30a8032`：陳和平移第 1、周睿麒（教練語音念「周瑞琪」，對到 zhou-ruiqi 頁）放鄒昆廷後、`FRONT` 24→32；invite 頁自己的 24 人名單沒動。
