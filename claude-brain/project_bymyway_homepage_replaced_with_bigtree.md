---
name: project-bymyway-homepage-replaced-with-bigtree
description: bymyway.com 首頁正式換成 BigTree 講座頁，舊首頁保留在 /old/，技術細節與復原方法
metadata: 
  node_type: memory
  type: project
  originSessionId: 2989d377-322b-4a22-a511-60d11dcf12e3
---

# bymyway.com 首頁換版（2026-07-03 深夜執行）

## 現況（已上線）

- **新首頁**：`https://www.bymyway.com/`（直接顯示，不用加 `/bigtree/`）— 內容是 BigTree 講座系列黑金風格頁，Elementor Canvas 模板，無大樹教育原表頭
- **舊首頁**：`https://www.bymyway.com/old/`（page_id 25066，slug 從 `home` 改成 `old`，admin 標題改成「首頁（舊版）」，內容完全沒動）
- 技術機制：WordPress `page_on_front` 設定從 25066 切換成 27393（BigTree 頁面），跟一般子頁 iframe 部署共用同一套自動站 SOP，只是這次改的是「首頁指標」而非新建子頁

## 本次連帶內容修改（BigTree 頁面本身，在 `Coach1973/bigtree` repo `speakers-2026/index.html`）

1. 導覽列右上角 CTA 從「立即聯繫」改成「登入課程」，連到 `bymyway.com/dashboard`（查證得知這是 bymyway 現有 Astra 主題帳號圖示的真實連結，Tutor LMS 學員後台）
2. 頁面最下方新增「精選影片」區塊，嵌入 YouTube 影片 `zL4InI7s96Q`（《大樹教練短片2016》）——這支影片是我從現有舊首頁原始碼裡查證找到的（唯一一支、位置在頁面79.8%處），不是憑空猜的

## 踩過的坑：GitHub Pages 部署偶發失敗

第一次 push（commit `bd1e3e7`）後，GitHub Pages 自動部署 job 失敗，錯誤訊息「Deployment failed, try again later」（用 `gh run view --log-failed` 查到），純屬 GitHub 系統暫時性問題，跟內容無關。解法：補一個空白 commit（`f244937`）觸發全新部署，第二次成功。**下次遇到 push 完线上没更新，先查 `gh run list --repo Coach1973/bigtree` 看 pages build 是不是失敗，不要一直懷疑自己內容錯。**

## 復原方法（30秒內可逆）

如果要恢復舊首頁：把 WordPress 設定 `page_on_front` 改回 `25066` 即可，兩邊頁面資料都還在，沒有刪除任何東西。

```python
POST /wp-json/wp/v2/settings {"page_on_front": 25066}
```

## Why

教練看完 BigTree 講座頁效果後主動決定「這個最新做出來的頁面取代 bymyway 首頁」，是教練的主動升級決策，不是被要求才做。

## 關聯

[[project_speakers2026_bigtree_launch]]（BigTree 頁面誕生過程）、`knowledges/SOP_bymyway_auto_site.md`（自動站部署完整 SOP，含 wp_client.py 工具路徑）
